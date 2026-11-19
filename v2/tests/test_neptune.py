"""P2-06 (#250): reuse an existing Neptune graph by name, or create one in the default VPC. L1, L2.

Everything runs against a fake reader or a recorded fake of the AWS CLI;
nothing contacts AWS. The account id and resource ids are documentation
examples.
"""

import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from reframe_v2 import cli
from reframe_v2.neptune import (
    CONFIGURATION_KEYS,
    AwsCliGraphReader,
    GraphError,
    ask,
    candidates,
    choose,
    default_network,
    terraform_variables,
    write_variables,
)
from reframe_v2.resources_file import ReaderError
from reframe_v2.state_store import Result

ACCOUNT = "111122223333"
BUCKET = "reframe-sample-source"
GOOD = {
    "DBClusterIdentifier": "sample-graph",
    "DBClusterArn": f"arn:aws:rds:us-east-1:{ACCOUNT}:cluster:sample-graph",
    "DbClusterResourceId": "cluster-SAMPLE",
    "Engine": "neptune",
    "EngineVersion": "1.4.5.1",
    "Status": "available",
    "Port": 8182,
    "DBClusterMembers": [{"DBInstanceIdentifier": "sample-graph-1"}],
    "IAMDatabaseAuthenticationEnabled": True,
    "StorageEncrypted": True,
    "ServerlessV2ScalingConfiguration": {"MinCapacity": 1.0, "MaxCapacity": 8.0},
    "DBSubnetGroup": "sample-subnets",
    "VpcSecurityGroups": [{"VpcSecurityGroupId": "sg-graph", "Status": "active"}],
    "AssociatedRoles": [{"RoleArn": f"arn:aws:iam::{ACCOUNT}:role/sample-loader", "Status": "ACTIVE"}],
}
GROUPS = {
    "sg-graph": {"GroupId": "sg-graph", "IpPermissions": [
        {"IpProtocol": "tcp", "FromPort": 8182, "ToPort": 8182, "UserIdGroupPairs": [{"GroupId": "sg-app"}]}]},
    "sg-app": {"GroupId": "sg-app", "IpPermissionsEgress": [
        {"IpProtocol": "tcp", "FromPort": 8182, "ToPort": 8182, "UserIdGroupPairs": [{"GroupId": "sg-graph"}]}]},
}


class FakeReader:
    def __init__(self):
        self.clusters_found = [copy.deepcopy(GOOD)]
        self.groups = copy.deepcopy(GROUPS)
        self.readable = {(f"arn:aws:iam::{ACCOUNT}:role/sample-loader", BUCKET)}
        self.subnet_groups = {"sample-subnets": {"VpcId": "vpc-graph", "Subnets": [
            {"SubnetIdentifier": "subnet-a", "SubnetAvailabilityZone": {"Name": "us-east-1a"}, "SubnetStatus": "Active"},
            {"SubnetIdentifier": "subnet-b", "SubnetAvailabilityZone": {"Name": "us-east-1b"}, "SubnetStatus": "Active"}]}}
        self.tables = {"vpc-graph": {"subnet-a": "rtb-graph", "subnet-b": "rtb-graph"},
                       "vpc-default": {"subnet-d1": "rtb-main", "subnet-d2": "rtb-main", "subnet-d3": "rtb-main"}}
        self.endpoints = {"vpc-graph": {"rtb-graph"}, "vpc-default": set()}
        self.vpc = "vpc-default"
        self.subnets = [("subnet-d3", "us-east-1c"), ("subnet-d2", "us-east-1b"), ("subnet-d1", "us-east-1a")]
        self.calls = []

    def account(self):
        return ACCOUNT

    def clusters(self):
        self.calls.append("clusters")
        return self.clusters_found

    def subnet_group(self, name):
        if name not in self.subnet_groups:
            raise ReaderError("DBSubnetGroupNotFoundFault")
        return self.subnet_groups[name]

    def security_groups(self, ids):
        return [self.groups[i] for i in ids if i in self.groups]

    def can_read(self, role_arn, bucket, account):
        self.calls.append(("can_read", account))
        return (role_arn, bucket) in self.readable

    def default_vpc(self):
        return self.vpc

    def default_subnets(self, vpc_id):
        return self.subnets

    def route_tables(self, vpc_id, subnet_ids):
        known = self.tables.get(vpc_id, {})
        return {s: known[s] for s in subnet_ids if s in known}

    def s3_endpoint_route_tables(self, vpc_id):
        return self.endpoints.get(vpc_id, set())


class CandidateTests(unittest.TestCase):
    def test_a_fit_cluster_is_offered_with_the_six_connector_values(self):
        [found] = candidates(FakeReader(), BUCKET)
        self.assertTrue(found.usable, found.problems)
        self.assertEqual(sorted(found.configuration), sorted(CONFIGURATION_KEYS))
        self.assertEqual(found.configuration["vpcSubnetIds"], "subnet-a,subnet-b")
        self.assertEqual(found.configuration["vpcSecurityGroupId"], "sg-app")
        self.assertEqual(found.configuration["s3BucketArn"], f"arn:aws:s3:::{BUCKET}")
        self.assertEqual(found.configuration["neptuneBulkUploadRoleArn"], f"arn:aws:iam::{ACCOUNT}:role/sample-loader")

    def test_every_unmet_requirement_is_named_at_once(self):
        reader = FakeReader()
        reader.clusters_found[0].update({"Status": "stopped", "DBClusterMembers": [], "EngineVersion": "1.3.2.1",
                                         "IAMDatabaseAuthenticationEnabled": False, "StorageEncrypted": False,
                                         "ServerlessV2ScalingConfiguration": None})
        [found] = candidates(reader, BUCKET)
        self.assertFalse(found.usable)
        text = " ".join(found.problems)
        for expected in ("stopped", "no instances", "1.4.5.1", "IAM authentication", "not encrypted", "not Serverless"):
            self.assertIn(expected, text)
        self.assertIsNone(found.configuration)

    def test_engine_versions_compare_as_numbers(self):
        reader = FakeReader()
        reader.clusters_found[0]["EngineVersion"] = "1.10.0.0"
        self.assertTrue(candidates(reader, BUCKET)[0].usable)

    def test_one_zone_and_no_s3_endpoint_are_problems(self):
        reader = FakeReader()
        reader.subnet_groups["sample-subnets"]["Subnets"][1]["SubnetAvailabilityZone"]["Name"] = "us-east-1a"
        reader.endpoints["vpc-graph"] = set()
        problems = " ".join(candidates(reader, BUCKET)[0].problems)
        self.assertIn("two Availability Zones", problems)
        self.assertIn("S3 gateway endpoint", problems)

    def test_the_connector_needs_a_group_the_cluster_lets_in_and_that_can_send(self):
        reader = FakeReader()
        reader.groups["sg-graph"]["IpPermissions"] = [{"IpProtocol": "tcp", "FromPort": 8182, "ToPort": 8182,
                                                       "IpRanges": [{"CidrIp": "10.0.0.0/16"}]}]
        self.assertIn("no security group is allowed", " ".join(candidates(reader, BUCKET)[0].problems))
        reader = FakeReader()
        reader.groups["sg-app"]["IpPermissionsEgress"] = [{"IpProtocol": "tcp", "FromPort": 443, "ToPort": 443,
                                                           "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]
        self.assertIn("may also send", " ".join(candidates(reader, BUCKET)[0].problems))
        reader = FakeReader()
        reader.groups["sg-app"]["IpPermissionsEgress"] = [{"IpProtocol": "-1", "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]
        self.assertTrue(candidates(reader, BUCKET)[0].usable)

    def test_a_loader_that_cannot_read_the_bucket_is_a_problem(self):
        reader = FakeReader()
        reader.readable = set()
        problems = " ".join(candidates(reader, BUCKET)[0].problems)
        self.assertIn(f"can read the bucket {BUCKET}", problems)
        self.assertIn("--bucket", problems)
        self.assertIn(("can_read", ACCOUNT), reader.calls)

    def test_a_read_that_fails_is_a_problem_never_a_pass(self):
        reader = FakeReader()
        reader.clusters_found[0]["DBSubnetGroup"] = "missing"
        found = candidates(reader, BUCKET)[0]
        self.assertFalse(found.usable)
        self.assertIn("could not be read", " ".join(found.problems))

    def test_clusters_are_listed_by_name(self):
        reader = FakeReader()
        other = copy.deepcopy(GOOD)
        other["DBClusterIdentifier"] = "another-graph"
        reader.clusters_found.append(other)
        self.assertEqual([c.name for c in candidates(reader, BUCKET)], ["another-graph", "sample-graph"])


class NetworkTests(unittest.TestCase):
    def test_two_default_subnets_in_different_zones_and_the_tables_lacking_an_endpoint(self):
        network = default_network(FakeReader())
        self.assertTrue(network.usable)
        self.assertEqual(network.subnet_ids, ("subnet-d1", "subnet-d2"))
        self.assertEqual(network.s3_endpoint_route_table_ids, ("rtb-main",))

    def test_an_existing_endpoint_is_not_created_again(self):
        reader = FakeReader()
        reader.endpoints["vpc-default"] = {"rtb-main"}
        self.assertEqual(default_network(reader).s3_endpoint_route_table_ids, ())

    def test_no_default_vpc_stops_rather_than_build_a_network(self):
        reader = FakeReader()
        reader.vpc = None
        network = default_network(reader)
        self.assertFalse(network.usable)
        with self.assertRaises(GraphError) as raised:
            terraform_variables(None, network)
        self.assertIn("no default VPC", str(raised.exception))

    def test_one_zone_is_not_enough(self):
        reader = FakeReader()
        reader.subnets = [("subnet-d1", "us-east-1a")]
        self.assertFalse(default_network(reader).usable)


class ChoiceTests(unittest.TestCase):
    def test_the_person_chooses_by_name(self):
        found = candidates(FakeReader(), BUCKET)
        said = []
        chosen = ask(found, lambda _: "sample-graph", said.append)
        self.assertEqual(chosen.name, "sample-graph")
        self.assertIn("never tags, changes or deletes it", "".join(said))
        self.assertIn("until P2 proves", "".join(said))

    def test_enter_means_a_new_graph(self):
        self.assertIsNone(ask(candidates(FakeReader(), BUCKET), lambda _: "", lambda _: None))

    def test_a_wrong_name_is_asked_again(self):
        answers = iter(["nope", "sample-graph"])
        said = []
        chosen = ask(candidates(FakeReader(), BUCKET), lambda _: next(answers), said.append)
        self.assertEqual(chosen.name, "sample-graph")
        self.assertIn("no Neptune cluster named nope", "".join(said))

    def test_no_usable_cluster_is_never_offered(self):
        reader = FakeReader()
        reader.clusters_found[0]["StorageEncrypted"] = False
        asked = []
        self.assertIsNone(ask(candidates(reader, BUCKET), asked.append, lambda _: None))
        self.assertEqual(asked, [])
        with self.assertRaises(GraphError):
            choose(candidates(reader, BUCKET), use="sample-graph")

    def test_answers_given_up_front(self):
        found = candidates(FakeReader(), BUCKET)
        self.assertEqual(choose(found, use="sample-graph").name, "sample-graph")
        self.assertIsNone(choose(found, new=True))
        with self.assertRaises(GraphError):
            choose(found, use="sample-graph", new=True)

    def test_variables_for_each_choice(self):
        found = candidates(FakeReader(), BUCKET)
        existing = terraform_variables(found[0], None)
        self.assertIsNone(existing["graph_network"])
        self.assertEqual(sorted(existing["existing_graph"]["configuration"]), sorted(CONFIGURATION_KEYS))
        new = terraform_variables(None, default_network(FakeReader()))
        self.assertIsNone(new["existing_graph"])
        self.assertEqual(new["graph_network"], {"vpc_id": "vpc-default", "subnet_ids": ["subnet-d1", "subnet-d2"],
                                                "s3_endpoint_route_table_ids": ["rtb-main"]})

    def test_an_existing_file_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "graph.tfvars.json"
            path.write_text("keep")
            with self.assertRaises(GraphError):
                write_variables(path, {"reimagine": True})
            self.assertEqual(path.read_text(), "keep")


def ok(value):
    return Result(0, json.dumps(value), "")


class CliReader:
    def __init__(self, replies):
        self.replies, self.calls = replies, []

    def __call__(self, argv, env, timeout):
        self.calls.append(argv)
        reply = self.replies[" ".join(argv[1:3])]
        return reply(argv) if callable(reply) else reply


class AwsCliGraphReaderTests(unittest.TestCase):
    def reader(self):
        replies = {
            "sts get-caller-identity": ok({"Account": ACCOUNT, "Arn": f"arn:aws:sts::{ACCOUNT}:assumed-role/SampleRole/s"}),
            "neptune describe-db-clusters": ok({"DBClusters": [GOOD, {**GOOD, "Engine": "aurora-postgresql"}]}),
            "neptune describe-db-subnet-groups": ok({"DBSubnetGroups": [FakeReader().subnet_groups["sample-subnets"]]}),
            "ec2 describe-security-groups": lambda argv: ok({"SecurityGroups": [GROUPS[g] for g in argv[argv.index("--group-ids") + 1:]
                                                                                if g in GROUPS]}),
            "iam simulate-principal-policy": ok({"EvaluationResults": [{"EvalDecision": "allowed"}]}),
            "ec2 describe-vpcs": ok({"Vpcs": [{"VpcId": "vpc-default", "IsDefault": True}]}),
            "ec2 describe-subnets": ok({"Subnets": [{"SubnetId": "subnet-d1", "AvailabilityZone": "us-east-1a", "State": "available"},
                                                    {"SubnetId": "subnet-d2", "AvailabilityZone": "us-east-1b", "State": "available"}]}),
            "ec2 describe-route-tables": ok({"RouteTables": [
                {"RouteTableId": "rtb-main", "Associations": [{"Main": True}]},
                {"RouteTableId": "rtb-graph", "Associations": [{"SubnetId": "subnet-a"}, {"SubnetId": "subnet-b"}]}]}),
            "ec2 describe-vpc-endpoints": ok({"VpcEndpoints": [{"State": "Available", "RouteTableIds": ["rtb-graph"]}]}),
        }
        runner = CliReader(replies)
        return AwsCliGraphReader("us-east-1", "sample-profile", runner=runner, parent_environment={"HOME": "/h"}), runner

    def test_only_read_only_calls_are_made(self):
        reader, runner = self.reader()
        [found] = candidates(reader, BUCKET)
        self.assertTrue(found.usable, found.problems)
        network = default_network(reader)
        self.assertEqual(network.subnet_ids, ("subnet-d1", "subnet-d2"))
        self.assertEqual(network.s3_endpoint_route_table_ids, ("rtb-main",))
        verbs = {argv[2] for argv in runner.calls}
        self.assertTrue(all(v.startswith(("describe-", "get-", "simulate-")) for v in verbs), verbs)

    def test_the_loader_check_supplies_the_resource_account(self):
        reader, runner = self.reader()
        candidates(reader, BUCKET)
        simulate = [argv for argv in runner.calls if argv[2] == "simulate-principal-policy"]
        self.assertEqual(len(simulate), 2)
        for argv in simulate:
            self.assertIn(f"ContextKeyName=aws:ResourceAccount,ContextKeyValues={ACCOUNT},ContextKeyType=string", argv)
            self.assertEqual(argv[argv.index("--policy-source-arn") + 1], f"arn:aws:iam::{ACCOUNT}:role/sample-loader")


class CliTests(unittest.TestCase):
    def run_graph(self, reader, *, use=None, new=False, tfvars=None, interactive=False, answer=""):
        args = SimpleNamespace(region="us-east-1", profile="sample", bucket=BUCKET, use=use, new=new, tfvars=tfvars)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.run_graph(args, reader=reader, prompt=lambda _: answer, interactive=interactive)
        return code, out.getvalue(), err.getvalue()

    def test_without_a_terminal_a_usable_cluster_waits_for_an_answer(self):
        code, out, err = self.run_graph(FakeReader())
        self.assertEqual(code, 4)
        self.assertIn("sample-graph: can serve", out)
        self.assertIn("--use", err)

    def test_use_writes_the_existing_graph_variables(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "graph.tfvars.json"
            code, out, _ = self.run_graph(FakeReader(), use="sample-graph", tfvars=path)
            self.assertEqual(code, 0)
            self.assertIn("will not tag, change or delete it", out)
            self.assertEqual(json.loads(path.read_text())["existing_graph"]["cluster_resource_id"], "cluster-SAMPLE")

    def test_new_and_enter_both_choose_the_default_vpc(self):
        code, out, _ = self.run_graph(FakeReader(), new=True)
        self.assertEqual(code, 0)
        self.assertIn("default VPC", out)
        code, out, _ = self.run_graph(FakeReader(), interactive=True, answer="")
        self.assertEqual(code, 0)
        self.assertIn('"vpc_id": "vpc-default"', out)

    def test_no_cluster_and_no_default_vpc_is_refused(self):
        reader = FakeReader()
        reader.clusters_found, reader.vpc = [], None
        code, out, err = self.run_graph(reader)
        self.assertEqual(code, 3)
        self.assertIn("No Neptune cluster exists", out)
        self.assertIn("no default VPC", err)

    def test_an_unusable_choice_is_refused(self):
        reader = FakeReader()
        reader.clusters_found[0]["IAMDatabaseAuthenticationEnabled"] = False
        code, _, err = self.run_graph(reader, use="sample-graph")
        self.assertEqual(code, 3)
        self.assertIn("IAM authentication", err)

    def test_use_and_new_together_are_a_usage_error(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as stop:
            cli.main(["graph", "--profile", "p", "--region", "us-east-1", "--bucket", BUCKET, "--use", "x", "--new"])
        self.assertEqual(stop.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
