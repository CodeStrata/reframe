"""P2-02 (#244): running on client-owned resources named in a resources file. L2.

Read-only checks run against a fake reader and a recorded fake of the AWS
CLI; nothing contacts AWS. The account id below is a documentation example.
"""

import copy
import json
import unittest

from reframe_v2.resources import LifecycleOwner, Manifest, ManifestEntry, ResourceError
from reframe_v2.resources_file import (
    ASSESSMENT_CONNECTOR_TYPE,
    REIMAGINE_CONNECTOR_TYPE,
    AwsCliReader,
    BucketFacts,
    ReaderError,
    check,
    check_manifest,
    check_write,
    load,
    may_tag,
    what_the_run_needs,
)
from reframe_v2.state_store import Result

ACCOUNT = "111122223333"
DOCUMENT = {
    "schema": "resources_file/1",
    "account": ACCOUNT,
    "region": "us-east-1",
    "state_bucket": {"name": "sample-reframe-state", "write_prefixes": ["projects/sample/"]},
    "bucket": {"name": "sample-source-bucket", "write_prefixes": ["reframe/"]},
    "sandbox_role": {"name": "sample-sandbox-role"},
    "transform": {"workspace_id": "ws-sample", "assessment_connector": "conn-assess", "reimagine_connector": "conn-reimagine"},
    "neptune_stack": {"name": "sample-neptune"},
}
GOOD_BUCKET = BucketFacts("us-east-1", "Enabled", "AES256", True)


def connector(kind, status="ACTIVE", account=ACCOUNT):
    return {"connectorType": kind, "accountConnection": {"awsAccountConnection": {"status": status, "accountId": account}}}


class FakeReader:
    def __init__(self):
        self.account = ACCOUNT
        self.buckets = {"sample-reframe-state": GOOD_BUCKET, "sample-source-bucket": GOOD_BUCKET}
        self.roles = {"sample-sandbox-role"}
        self.refused = set()
        self.connectors = {"conn-assess": connector(ASSESSMENT_CONNECTOR_TYPE), "conn-reimagine": connector(REIMAGINE_CONNECTOR_TYPE)}
        self.stacks = {"sample-neptune": "CREATE_COMPLETE"}
        self.broken = set()
        self.calls = []

    def _call(self, name):
        self.calls.append(name)
        if name in self.broken:
            raise ReaderError("synthetic failure")

    def caller_account(self):
        self._call("account")
        return self.account

    def bucket(self, name, account):
        self._call("bucket")
        return self.buckets.get(name)

    def role_exists(self, name):
        self._call("role")
        return name in self.roles

    def denied(self, checks):
        self._call("denied")
        return [item for item in checks if item[0] in self.refused]

    def connector(self, workspace_id, connector_id):
        self._call("connector")
        return self.connectors.get(connector_id)

    def stack_status(self, name):
        self._call("stack")
        return self.stacks.get(name)


class LoadTests(unittest.TestCase):
    def test_a_valid_file_loads(self):
        resources = load(DOCUMENT)
        self.assertEqual(resources.write_prefixes, ("reframe/",))
        self.assertIn("sample-neptune", resources.client_owned_ids)

    def test_schema_problems_are_refused(self):
        changes = [
            lambda d: d.update(account="12345"),
            lambda d: d["bucket"].update(write_prefixes=[]),
            lambda d: d["bucket"].update(write_prefixes=["no-trailing-slash"]),
            lambda d: d["bucket"].update(write_prefixes=["../escape/"]),
            lambda d: d.update(extra=True),
            lambda d: d["transform"].pop("assessment_connector"),
        ]
        for change in changes:
            document = copy.deepcopy(DOCUMENT)
            change(document)
            with self.subTest(document=document), self.assertRaises(ResourceError):
                load(document)

    def test_reimagine_and_neptune_come_together(self):
        document = copy.deepcopy(DOCUMENT)
        document["neptune_stack"] = None
        with self.assertRaises(ResourceError):
            load(document)
        document["transform"]["reimagine_connector"] = None
        self.assertIsNone(load(document).neptune_stack)


class CheckTests(unittest.TestCase):
    def test_fit_resources_pass(self):
        report = check(load(DOCUMENT), FakeReader())
        self.assertTrue(report.ok, report.text())

    def test_every_problem_is_reported_at_once(self):
        reader = FakeReader()
        reader.buckets["sample-source-bucket"] = BucketFacts("eu-west-1", "Suspended", None, False)
        reader.roles.clear()
        reader.refused.add("s3:PutObject")
        reader.connectors["conn-reimagine"] = connector(REIMAGINE_CONNECTOR_TYPE, status="PENDING")
        reader.stacks["sample-neptune"] = "ROLLBACK_COMPLETE"
        report = check(load(DOCUMENT), reader)
        resources = [p.resource for p in report.problems]
        self.assertEqual(resources.count("bucket"), 4)
        for name in ("sandbox role", "permissions", "reimagine connector", "Neptune stack"):
            self.assertIn(name, resources)
        self.assertIn("no job was started and nothing was changed", report.text())

    def test_wrong_account_and_wrong_connector_type_fail(self):
        reader = FakeReader()
        reader.account = "444455556666"
        reader.connectors["conn-assess"] = connector(REIMAGINE_CONNECTOR_TYPE)
        problems = {p.resource for p in check(load(DOCUMENT), reader).problems}
        self.assertEqual(problems, {"account", "assessment connector"})

    def test_a_check_that_cannot_be_made_is_a_problem_never_a_pass(self):
        reader = FakeReader()
        reader.broken.add("denied")
        report = check(load(DOCUMENT), reader)
        self.assertFalse(report.ok)
        self.assertIn("not assumed fit", report.problems[0].message)

    def test_the_reader_offers_no_changes(self):
        mutating = [name for name in dir(AwsCliReader) if name.startswith(("put", "create", "delete", "tag", "update"))]
        self.assertEqual(mutating, [])


class ClientOwnedRuleTests(unittest.TestCase):
    def test_writes_only_under_declared_prefixes(self):
        resources = load(DOCUMENT)
        check_write(resources, "sample-source-bucket", "reframe/run-1/source.zip")
        check_write(resources, "sample-reframe-state", "projects/sample/ledger/journal/000000000001.json")
        for bucket, key in (("sample-source-bucket", "other/x"), ("sample-source-bucket", "reframe/../x"),
                            ("sample-reframe-state", "projects/other/x"), ("unknown-bucket", "reframe/x")):
            with self.subTest(bucket=bucket, key=key), self.assertRaises(ResourceError):
                check_write(resources, bucket, key)

    def test_client_owned_resources_are_never_in_the_manifest_or_tagged(self):
        resources = load(DOCUMENT)
        manifest = Manifest("sample")
        manifest.record(ManifestEntry("reframe-owned-thing", "s3_bucket", LifecycleOwner.TERRAFORM, True, "sample", "run-1"))
        check_manifest(manifest, resources)
        manifest.record(ManifestEntry("sample-source-bucket", "s3_bucket", LifecycleOwner.TERRAFORM, True, "sample", "run-1"))
        with self.assertRaises(ResourceError):
            check_manifest(manifest, resources)
        self.assertFalse(may_tag(resources, "conn-reimagine"))
        self.assertTrue(may_tag(resources, "reframe-owned-thing"))


class NeedsTests(unittest.TestCase):
    def test_neither_option_lists_what_the_run_needs(self):
        basic = what_the_run_needs(reimagine=False, backend="claude-cli")
        full = what_the_run_needs(reimagine=True, backend="bedrock")
        self.assertTrue(basic[-1].startswith("Then rerun with --provision"))
        self.assertFalse(any("Neptune" in line or "Bedrock" in line for line in basic))
        self.assertTrue(any("Neptune" in line for line in full) and any("Bedrock" in line for line in full))


class CliReader:
    """Recorded replies of read-only AWS CLI calls."""

    def __init__(self, replies):
        self.replies, self.calls = replies, []

    def __call__(self, argv, env, timeout):
        self.calls.append(argv)
        key = " ".join(argv[1:3])
        reply = self.replies[key]
        return reply(argv) if callable(reply) else reply


def ok(value):
    return Result(0, json.dumps(value), "")


def fail(code, op):
    return Result(254, "", f"An error occurred ({code}) when calling the {op} operation: synthetic")


class AwsCliReaderTests(unittest.TestCase):
    def reader(self, **overrides):
        replies = {
            "sts get-caller-identity": ok({"Account": ACCOUNT, "Arn": f"arn:aws:sts::{ACCOUNT}:assumed-role/SampleRole/session"}),
            "s3api head-bucket": ok({"BucketRegion": "us-east-1"}),
            "s3api get-bucket-location": ok({"LocationConstraint": None}),
            "s3api get-bucket-versioning": ok({"Status": "Enabled"}),
            "s3api get-bucket-encryption": ok({"ServerSideEncryptionConfiguration": {"Rules": [{"ApplyServerSideEncryptionByDefault": {"SSEAlgorithm": "AES256"}}]}}),
            "s3api get-public-access-block": ok({"PublicAccessBlockConfiguration": {k: True for k in ("BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets")}}),
            "iam get-role": ok({"Role": {"Arn": f"arn:aws:iam::{ACCOUNT}:role/aws-reserved/sso.amazonaws.com/SampleRole"}}),
            "iam simulate-principal-policy": ok({"EvaluationResults": [{"EvalDecision": "allowed"}]}),
            "cloudformation describe-stacks": ok({"Stacks": [{"StackStatus": "UPDATE_COMPLETE"}]}),
        }
        replies.update(overrides)
        cli = CliReader(replies)
        connectors = {"conn-assess": connector(ASSESSMENT_CONNECTOR_TYPE), "conn-reimagine": connector(REIMAGINE_CONNECTOR_TYPE)}
        return AwsCliReader("us-east-1", "sample-profile", lambda w, c: connectors.get(c), runner=cli,
                            parent_environment={"HOME": "/h", "AWS_SECRET_ACCESS_KEY": "x"}), cli

    def test_fit_resources_pass_through_read_only_calls(self):
        reader, cli = self.reader()
        self.assertTrue(check(load(DOCUMENT), reader).ok)
        commands = {" ".join(argv[1:3]) for argv in cli.calls}
        self.assertTrue(all(c.split()[1].startswith(("get-", "head-", "describe-", "simulate-")) for c in commands), commands)
        simulate = next(argv for argv in cli.calls if argv[2] == "simulate-principal-policy")
        self.assertIn("aws-reserved/sso.amazonaws.com/SampleRole", simulate[simulate.index("--policy-source-arn") + 1])

    def test_missing_resources_are_found_missing(self):
        reader, _ = self.reader(**{"s3api head-bucket": fail("404", "HeadBucket"),
                                   "cloudformation describe-stacks": fail("ValidationError", "DescribeStacks")})
        messages = [p.message for p in check(load(DOCUMENT), reader).problems]
        self.assertIn("bucket not found", messages)
        self.assertIn("Neptune stack not found", messages)

    def test_another_owners_bucket_is_never_reported_fine(self):
        reader, _ = self.reader(**{"s3api head-bucket": fail("403", "HeadBucket")})
        problems = check(load(DOCUMENT), reader).problems
        self.assertTrue(any(p.resource == "bucket" and "not assumed fit" in p.message for p in problems))

    def test_missing_encryption_and_public_block_are_problems(self):
        reader, _ = self.reader(**{"s3api get-bucket-encryption": fail("ServerSideEncryptionConfigurationNotFoundError", "GetBucketEncryption"),
                                   "s3api get-public-access-block": fail("NoSuchPublicAccessBlockConfiguration", "GetPublicAccessBlock")})
        messages = [p.message for p in check(load(DOCUMENT), reader).problems]
        self.assertIn("bucket has no default encryption", messages)
        self.assertIn("bucket does not block all public access", messages)

    def test_a_denied_permission_is_named(self):
        def simulate(argv):
            action = argv[argv.index("--action-names") + 1]
            return ok({"EvaluationResults": [{"EvalDecision": "implicitDeny" if action == "s3:PutObject" else "allowed"}]})
        reader, _ = self.reader(**{"iam simulate-principal-policy": simulate})
        messages = [p.message for p in check(load(DOCUMENT), reader).problems]
        self.assertIn("the signed-in profile is not allowed s3:PutObject on sample-source-bucket/reframe/*", messages)

    def test_the_environment_is_allowlisted(self):
        reader, cli = self.reader()
        reader.caller_account()
        self.assertEqual(reader.env, {"HOME": "/h", "AWS_PAGER": ""})
        self.assertEqual(cli.calls[0][cli.calls[0].index("--profile") + 1], "sample-profile")


if __name__ == "__main__":
    unittest.main()
