"""P2-04 (#246): Terraform provisioning and reframe bootstrap. L1, L2.

The static checks read the Terraform as text. `terraform validate` runs when
Terraform 1.10 or later is on the PATH (CI installs a pinned version); it
plans nothing and needs no AWS credentials.
"""

import contextlib
import io
import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import reframe_v2
from reframe_v2 import cli
from reframe_v2.bootstrap import BootstrapError, bootstrap_policy, write_terraform
from reframe_v2.resources import ResourceError
from reframe_v2.resources_file import load

TERRAFORM = Path(reframe_v2.__file__).parent / "terraform"


def text(*parts):
    return (TERRAFORM.joinpath(*parts)).read_text()


class PolicyTests(unittest.TestCase):
    def test_every_change_is_scoped_to_reframe_names_or_the_reframe_tag(self):
        tagged = ({"StringEquals": {"aws:RequestTag/ManagedBy": "reframe"}}, {"StringEquals": {"aws:ResourceTag/ManagedBy": "reframe"}})
        for statement in bootstrap_policy()["Statement"]:
            actions = statement["Action"] if isinstance(statement["Action"], list) else [statement["Action"]]
            self.assertFalse(any("*" in a for a in actions), statement["Sid"])
            if statement["Sid"] == "ReadOnlyChecks":
                continue
            resources = statement["Resource"] if isinstance(statement["Resource"], list) else [statement["Resource"]]
            by_name = all("reframe-*" in r for r in resources)
            self.assertTrue(by_name or statement.get("Condition") in tagged, statement["Sid"])

    def test_the_read_only_statement_only_reads(self):
        statement = next(s for s in bootstrap_policy()["Statement"] if s["Sid"] == "ReadOnlyChecks")
        self.assertTrue(all(re.search(r":(Get|Simulate|Describe)", a) for a in statement["Action"]))

    def test_roles_are_passed_to_transform_and_neptune_only(self):
        statement = next(s for s in bootstrap_policy()["Statement"] if s["Action"] == "iam:PassRole")
        self.assertEqual(statement["Condition"],
                         {"StringEquals": {"iam:PassedToService": ["transform.amazonaws.com", "rds.amazonaws.com"]}})

    def test_creating_requires_the_reframe_tag_and_deleting_requires_it_on_the_resource(self):
        statements = {s["Sid"]: s for s in bootstrap_policy()["Statement"]}
        create = statements["CreateReframeNetworkAndGraphOnlyWhenTagged"]
        self.assertTrue(all(":Create" in a for a in create["Action"]))
        change = statements["ChangeOnlyWhatReframeTagged"]
        self.assertIn("rds:DeleteDBCluster", change["Action"])
        self.assertEqual(change["Condition"], {"StringEquals": {"aws:ResourceTag/ManagedBy": "reframe"}})

    def test_no_transform_action_is_guessed(self):
        actions = [a for s in bootstrap_policy()["Statement"] for a in (s["Action"] if isinstance(s["Action"], list) else [s["Action"]])]
        self.assertFalse(any(a.startswith("transform:") for a in actions))


class TerraformTextTests(unittest.TestCase):
    def test_every_bucket_is_encrypted_versioned_private_and_owner_enforced(self):
        for module in ("state_bucket", "repo"):
            body = text("modules", module, "main.tf")
            buckets = re.findall(r'resource "aws_s3_bucket" "(\w+)"', body)
            self.assertEqual(len(buckets), 1, module)
            name = buckets[0]
            for kind in ("aws_s3_bucket_server_side_encryption_configuration", "aws_s3_bucket_versioning",
                         "aws_s3_bucket_public_access_block", "aws_s3_bucket_ownership_controls"):
                self.assertIn(f'resource "{kind}" "{name}"', body, f"{module}: {kind}")
            self.assertEqual(body.count("= true"), 4, f"{module}: all four public access settings")
            self.assertIn('status = "Enabled"', body)

    def test_the_sandbox_role_denies_reads_outside_its_bucket(self):
        body = text("modules", "repo", "main.tf")
        deny = body[body.index('sid           = "DenyReadsOutsideSource"'):]
        self.assertIn('effect        = "Deny"', deny)
        self.assertIn("not_resources", deny.split("}")[0])

    def test_every_composition_sets_the_three_default_tags(self):
        for composition in ("bootstrap", "project"):
            body = text(composition, "main.tf")
            tags = body[body.index("default_tags"):]
            for tag in ("ManagedBy      = \"reframe\"", "ReframeProject", "ReframeRun"):
                self.assertIn(tag, tags, composition)

    def test_project_state_is_in_the_state_bucket_with_locking(self):
        body = text("project", "main.tf")
        self.assertIn('backend "s3"', body)
        self.assertIn("use_lockfile = true", body)
        self.assertNotIn("dynamodb", body)

    def test_bedrock_invoke_never_uses_a_wildcard(self):
        body = text("modules", "bedrock_invoke", "main.tf")
        self.assertIn('actions   = ["bedrock:InvokeModel", "bedrock:InvokeModelWithResponseStream"]', body)
        self.assertIn("resources = var.model_arns", body)

    def test_no_credentials_or_accounts_are_written(self):
        for path in TERRAFORM.rglob("*.tf"):
            body = path.read_text()
            self.assertIsNone(re.search(r"\b[0-9]{12}\b|access_key|secret_key|profile\s*=", body), path.name)


class NeptuneTextTests(unittest.TestCase):
    """What AWS checks for a reimagine connector (v1, #206), and building from nothing."""

    body = text("modules", "neptune_graph", "main.tf")

    def test_the_cluster_meets_what_aws_checks(self):
        for line in ("iam_database_authentication_enabled = true", "storage_encrypted                   = true",
                     "serverless_v2_scaling_configuration", 'instance_class     = "db.serverless"', 'default     = "1.4.5.1"',
                     "AWS requires Neptune engine 1.4.5.1 or later"):
            self.assertIn(line, self.body)

    def test_nothing_is_assumed_to_exist(self):
        for resource in ("aws_vpc", "aws_subnet", "aws_route_table", "aws_vpc_endpoint", "aws_security_group",
                         "aws_neptune_subnet_group", "aws_neptune_cluster", "aws_iam_role"):
            self.assertIn(f'resource "{resource}" ', self.body)
        self.assertNotRegex(self.body, r'data "aws_(vpc|subnet|subnets|security_group|neptune_cluster)" ')
        self.assertIn("count             = 2", self.body)
        self.assertIn("data.aws_availability_zones.available.names[count.index]", self.body)

    def test_the_network_is_private_and_the_graph_reachable_only_from_the_connector(self):
        self.assertNotIn("aws_internet_gateway", self.body)
        self.assertNotIn("aws_nat_gateway", self.body)
        self.assertNotIn("0.0.0.0/0", self.body)
        ingress = self.body[self.body.index('resource "aws_vpc_security_group_ingress_rule"'):]
        self.assertIn("referenced_security_group_id = aws_security_group.app.id", ingress.split("}")[0])

    def test_the_bulk_loader_reads_only_the_source_bucket(self):
        loader = self.body[self.body.index('data "aws_iam_policy_document" "loader" {'):]
        self.assertIn('actions   = ["s3:GetObject", "s3:ListBucket"]', loader.split("resource")[0])
        self.assertIn('identifiers = ["rds.amazonaws.com"]', self.body)

    def test_the_connector_configuration_uses_the_keys_aws_accepted(self):
        from reframe_v2.resources_file import REIMAGINE_CONNECTOR_TYPE
        self.assertEqual(REIMAGINE_CONNECTOR_TYPE, "mainframe_modernization|reimagine|1")
        output = self.body[self.body.index('output "connector_configuration"'):]
        keys = re.findall(r"^    (\w+)\s+=", output, re.M)
        self.assertEqual(sorted(keys), sorted(["s3BucketArn", "neptuneClusterArn", "neptuneClusterResourceId",
                                               "neptuneBulkUploadRoleArn", "vpcSubnetIds", "vpcSecurityGroupId"]))

    def test_the_connector_role_matches_what_the_console_generates(self):
        role = text("modules", "reimagine_role", "main.tf")
        self.assertIn('values   = ["arn:${local.p}:transform:${local.region}:${local.account}:connector/*"]', role)
        self.assertIn('resources = ["${local.bucket}/transform-output/neptune-quads/*"]', role)
        self.assertIn('"neptune-db:StartLoaderJob"', role)
        self.assertNotIn('actions   = ["s3:*"]', role)

    def test_the_graph_is_only_built_when_asked(self):
        project = text("project", "main.tf")
        self.assertIn("count          = var.reimagine ? 1 : 0", project)
        self.assertIn("default     = false", project[project.index('variable "reimagine"'):])


@unittest.skipUnless(shutil.which("terraform"), "Terraform is not installed; CI runs this with a pinned version")
class TerraformValidateTests(unittest.TestCase):
    def test_both_compositions_validate(self):
        version = subprocess.run(["terraform", "version", "-json"], capture_output=True, text=True)
        try:
            found = tuple(int(x) for x in json.loads(version.stdout)["terraform_version"].split(".")[:2])
        except (ValueError, KeyError):
            self.skipTest("Terraform is too old to report its version as JSON")
        if found < (1, 10):
            self.skipTest(f"Terraform {found} is older than 1.10")
        with tempfile.TemporaryDirectory() as folder:
            out = Path(folder) / "tf"
            write_terraform(out)
            for composition in ("bootstrap", "project"):
                for command in (["init", "-backend=false", "-input=false"], ["validate"]):
                    result = subprocess.run(["terraform", f"-chdir={out / composition}", *command], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, f"{composition} {command[0]}: {result.stderr}")


class WriteTests(unittest.TestCase):
    def test_the_files_are_written_without_any_aws_call(self):
        with tempfile.TemporaryDirectory() as folder, mock.patch("subprocess.run", side_effect=AssertionError("no process")):
            written = write_terraform(Path(folder) / "out")
            names = sorted(str(p.relative_to(Path(folder) / "out")) for p in written)
        self.assertEqual(names, ["README.md", "bootstrap/main.tf", "modules/bedrock_invoke/main.tf",
                                 "modules/neptune_graph/main.tf", "modules/reimagine_role/main.tf", "modules/repo/main.tf",
                                 "modules/state_bucket/main.tf", "project/main.tf", "resources.template.json"])

    def test_a_folder_with_files_is_refused(self):
        with tempfile.TemporaryDirectory() as folder:
            (Path(folder) / "keep.txt").write_text("x")
            with self.assertRaises(BootstrapError):
                write_terraform(Path(folder))
            self.assertEqual([p.name for p in Path(folder).iterdir()], ["keep.txt"])

    def test_the_template_is_refused_until_it_is_filled_in(self):
        with tempfile.TemporaryDirectory() as folder:
            write_terraform(Path(folder) / "out")
            template = json.loads((Path(folder) / "out" / "resources.template.json").read_text())
        with self.assertRaises(ResourceError):
            load(template)


class CliTests(unittest.TestCase):
    def test_bootstrap_print_and_terraform(self):
        with tempfile.TemporaryDirectory() as folder:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(cli.main(["bootstrap", "--print", "--terraform", str(Path(folder) / "tf")]), 0)
            self.assertIn('"Sid": "ReframeRoles"', out.getvalue())
            self.assertIn("No AWS change was made", out.getvalue())
            err = io.StringIO()
            with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
                self.assertEqual(cli.main(["bootstrap", "--print", "--terraform", str(Path(folder) / "tf")]), 3)
            self.assertIn("not an empty folder", err.getvalue())

    def test_bootstrap_needs_print(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as stop:
            cli.main(["bootstrap"])
        self.assertEqual(stop.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
