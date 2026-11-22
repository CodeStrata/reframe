import unittest

from reframe.core.errors import Stop
from reframe.infrastructure import neptune

GOOD = {"DBClusterIdentifier": "graph-a", "Status": "available", "DBClusterMembers": [{}], "EngineVersion": "1.4.5.1",
        "IAMDatabaseAuthenticationEnabled": True, "StorageEncrypted": True, "ServerlessV2ScalingConfiguration": {"MaxCapacity": 8},
        "DBSubnetGroup": "sg-group", "Port": 8182, "VpcSecurityGroups": [{"VpcSecurityGroupId": "sg-cluster", "Status": "active"}],
        "AssociatedRoles": [{"RoleArn": "arn:aws:iam::000000000000:role/loader", "Status": "ACTIVE"}],
        "DBClusterArn": "arn:aws:rds:us-east-1:000000000000:cluster:graph-a", "DbClusterResourceId": "cluster-X"}


class FakeReader:
    def __init__(self, clusters, can_read=True):
        self._clusters, self._can_read = clusters, can_read

    def clusters(self):
        return self._clusters

    def subnet_group(self, name):
        return {"VpcId": "vpc-1", "Subnets": [{"SubnetIdentifier": "s1", "SubnetAvailabilityZone": {"Name": "a"}},
                                               {"SubnetIdentifier": "s2", "SubnetAvailabilityZone": {"Name": "b"}}]}

    def security_groups(self, ids):
        if ids == ["sg-cluster"]:
            return [{"GroupId": "sg-cluster", "IpPermissions": [{"IpProtocol": "tcp", "FromPort": 8182, "ToPort": 8182,
                                                                 "UserIdGroupPairs": [{"GroupId": "sg-app"}]}]}]
        return [{"GroupId": "sg-app", "IpPermissionsEgress": [{"IpProtocol": "-1", "IpRanges": [{"CidrIp": "0.0.0.0/0"}]}]}]

    def can_read(self, role, bucket, account):
        return self._can_read

    def route_tables(self, vpc, subnets):
        return {s: "rt-1" for s in subnets}

    def s3_endpoint_route_tables(self, vpc):
        return {"rt-1"}


class NeptuneTest(unittest.TestCase):
    def test_usable_cluster_gives_all_six_values(self):
        found = neptune.candidates(FakeReader([GOOD]), "reframe-x-src", "000000000000")
        self.assertTrue(found[0].usable)
        self.assertEqual(set(found[0].configuration), {"s3BucketArn", "neptuneClusterArn", "neptuneClusterResourceId",
                                                       "neptuneBulkUploadRoleArn", "vpcSubnetIds", "vpcSecurityGroupId"})
        self.assertEqual(found[0].configuration["vpcSecurityGroupId"], "sg-app")

    def test_every_problem_listed(self):
        old = {**GOOD, "DBClusterIdentifier": "old", "EngineVersion": "1.2.0.0", "StorageEncrypted": False}
        found = neptune.candidates(FakeReader([old], can_read=False), "b", "a")
        self.assertFalse(found[0].usable)
        text = "; ".join(found[0].problems)
        for expected in ("older than", "not encrypted", "loader role"):
            self.assertIn(expected, text)

    def test_choice_rules(self):
        found = neptune.candidates(FakeReader([GOOD]), "b", "a")
        say = lambda text: None
        self.assertIsNone(neptune.choose(found, None, "autonomous", None, say))
        self.assertIsNone(neptune.choose(found, "new", "interactive", None, say))
        self.assertEqual(neptune.choose(found, "graph-a", "autonomous", None, say).name, "graph-a")
        self.assertEqual(neptune.choose(found, None, "interactive", lambda p: "1", say).name, "graph-a")
        self.assertIsNone(neptune.choose(found, "existing", "autonomous", lambda p: "", say))
        with self.assertRaises(Stop):
            neptune.choose(found, "missing", "autonomous", None, say)

    def test_terraform_variables(self):
        self.assertEqual(neptune.terraform_variables(None), {"existing_graph": None})
        chosen = neptune.candidates(FakeReader([GOOD]), "b", "a")[0]
        self.assertEqual(neptune.terraform_variables(chosen)["existing_graph"]["name"], "graph-a")


if __name__ == "__main__":
    unittest.main()
