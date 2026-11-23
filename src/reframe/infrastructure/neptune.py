"""The Neptune graph: a new one, or an existing cluster used exactly as it is (specification section 4, stage 2).

Reframe lists the region's Neptune clusters with read-only calls and checks each against what the
reimagine connector needs. A usable cluster can be chosen; it is client-owned, so Reframe never tags,
changes or deletes it, and teardown never lists it. Every other cluster is shown with each thing it lacks.
Ported from the earlier build's checks; the needs are the ones AWS accepted for the reimagine connector.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from reframe.core.errors import NotSent, Outcome, Stop
from reframe.core.shell import Aws

MINIMUM_ENGINE = (1, 4, 5, 1)
SHARING_NOTE = "If another reimagine connector already uses a cluster, both write into the same graph."
OWNERSHIP_NOTE = "An existing cluster is used as it is: Reframe never tags, changes or deletes it, and teardown leaves it alone."
NEW_GRAPH_NOTE = ("A new graph gets its own private network (a VPC, two subnets, a route table and an S3 gateway endpoint, "
                  "with no internet gateway or NAT). Neptune bills from the moment it is created until reframe teardown.")


@dataclass(frozen=True)
class Candidate:
    name: str
    problems: tuple[str, ...]
    cluster_arn: str = ""
    cluster_resource_id: str = ""
    configuration: dict[str, str] | None = None

    @property
    def usable(self) -> bool:
        return not self.problems and self.configuration is not None


def engine(version: Any) -> tuple[int, ...] | None:
    try:
        return tuple(int(part) for part in str(version).split("."))
    except ValueError:
        return None


def _covers(permission: dict[str, Any], port: int) -> bool:
    if permission.get("IpProtocol") == "-1":
        return True
    if permission.get("IpProtocol") != "tcp":
        return False
    low, high = permission.get("FromPort"), permission.get("ToPort")
    return isinstance(low, int) and isinstance(high, int) and low <= port <= high


class Reader:
    """Read-only AWS CLI questions about Neptune and its network."""

    def __init__(self, aws: Aws) -> None:
        self.aws = aws

    def clusters(self) -> list[dict[str, Any]]:
        reply = self.aws.read("neptune", "describe-db-clusters", "--filters", "Name=engine,Values=neptune")
        return [c for c in reply.get("DBClusters") or [] if c.get("Engine") == "neptune"]

    def subnet_group(self, name: str) -> dict[str, Any]:
        groups = self.aws.read("neptune", "describe-db-subnet-groups", "--db-subnet-group-name", name).get("DBSubnetGroups") or []
        if len(groups) != 1:
            raise NotSent("describe-db-subnet-groups returned an unexpected number of groups")
        return groups[0]

    def security_groups(self, ids: list[str]) -> list[dict[str, Any]]:
        return self.aws.read("ec2", "describe-security-groups", "--group-ids", *ids).get("SecurityGroups") or [] if ids else []

    def can_read(self, role_arn: str, bucket: str, account: str) -> bool:
        context = f"ContextKeyName=aws:ResourceAccount,ContextKeyValues={account},ContextKeyType=string"
        for action, resource in (("s3:GetObject", f"arn:aws:s3:::{bucket}/*"), ("s3:ListBucket", f"arn:aws:s3:::{bucket}")):
            reply = self.aws.read("iam", "simulate-principal-policy", "--policy-source-arn", role_arn, "--action-names", action,
                                  "--resource-arns", resource, "--context-entries", context)
            results = reply.get("EvaluationResults") or []
            if not results or any(item.get("EvalDecision") != "allowed" for item in results):
                return False
        return True

    def route_tables(self, vpc_id: str, subnet_ids: list[str]) -> dict[str, str]:
        tables = self.aws.read("ec2", "describe-route-tables", "--filters", f"Name=vpc-id,Values={vpc_id}").get("RouteTables") or []
        explicit, main = {}, None
        for table in tables:
            for association in table.get("Associations") or []:
                if association.get("Main"):
                    main = table.get("RouteTableId")
                elif association.get("SubnetId"):
                    explicit[association["SubnetId"]] = table.get("RouteTableId")
        found = {subnet: explicit.get(subnet) or main for subnet in subnet_ids}
        return {subnet: str(table) for subnet, table in found.items() if table}

    def s3_endpoint_route_tables(self, vpc_id: str) -> set[str]:
        reply = self.aws.read("ec2", "describe-vpc-endpoints", "--filters", f"Name=vpc-id,Values={vpc_id}",
                              f"Name=service-name,Values=com.amazonaws.{self.aws.region}.s3", "Name=vpc-endpoint-type,Values=Gateway")
        return {str(t) for e in reply.get("VpcEndpoints") or [] if str(e.get("State", "available")).lower() == "available"
                for t in e.get("RouteTableIds") or []}


def _connector_group(reader: Reader, cluster_groups: list[str], port: int) -> tuple[str | None, str | None]:
    groups = reader.security_groups(cluster_groups)
    sources = sorted({pair["GroupId"] for group in groups for permission in group.get("IpPermissions") or []
                      if _covers(permission, port) for pair in permission.get("UserIdGroupPairs") or [] if pair.get("GroupId")})
    if not sources:
        return None, f"no security group is allowed to reach it on port {port}"
    for source in reader.security_groups(sources):
        for permission in source.get("IpPermissionsEgress") or []:
            if not _covers(permission, port):
                continue
            to_cluster = {pair.get("GroupId") for pair in permission.get("UserIdGroupPairs") or []} & set(cluster_groups)
            anywhere = any(item.get("CidrIp") == "0.0.0.0/0" for item in permission.get("IpRanges") or [])
            if to_cluster or anywhere:
                return source["GroupId"], None
    return None, f"no security group allowed to reach it may also send to it on port {port}"


def judge(reader: Reader, cluster: dict[str, Any], bucket: str, account: str) -> Candidate:
    """Every problem is reported, never just the first."""
    name = str(cluster.get("DBClusterIdentifier") or "")
    problems: list[str] = []
    if cluster.get("Status") != "available":
        problems.append(f"it is {cluster.get('Status') or 'in an unknown state'}, not available")
    if not cluster.get("DBClusterMembers"):
        problems.append("it has no instances")
    version = engine(cluster.get("EngineVersion"))
    if version is None or version < MINIMUM_ENGINE:
        problems.append(f"engine {cluster.get('EngineVersion')} is older than the 1.4.5.1 AWS requires")
    if cluster.get("IAMDatabaseAuthenticationEnabled") is not True:
        problems.append("IAM authentication is off")
    if cluster.get("StorageEncrypted") is not True:
        problems.append("storage is not encrypted")
    if not cluster.get("ServerlessV2ScalingConfiguration"):
        problems.append("it is not Serverless")
    subnets: list[str] = []
    try:
        group = reader.subnet_group(str(cluster.get("DBSubnetGroup") or ""))
        vpc_id = str(group.get("VpcId") or "")
        listed = [s for s in group.get("Subnets") or [] if s.get("SubnetStatus", "Active") == "Active"]
        subnets = sorted(str(s["SubnetIdentifier"]) for s in listed if s.get("SubnetIdentifier"))
        if len({(s.get("SubnetAvailabilityZone") or {}).get("Name") for s in listed} - {None}) < 2:
            problems.append("its subnets are not in two Availability Zones")
        tables = reader.route_tables(vpc_id, subnets)
        if set(tables.values()) - reader.s3_endpoint_route_tables(vpc_id) or len(tables) < len(subnets):
            problems.append("its subnets have no S3 gateway endpoint")
    except NotSent as error:
        problems.append(f"its network could not be read ({str(error)[:120]})")
    group_id = None
    try:
        port = int(cluster.get("Port") or 8182)
        cluster_groups = sorted(g["VpcSecurityGroupId"] for g in cluster.get("VpcSecurityGroups") or []
                                if g.get("Status", "active") == "active" and g.get("VpcSecurityGroupId"))
        group_id, problem = _connector_group(reader, cluster_groups, port)
        if problem:
            problems.append(problem)
    except NotSent as error:
        problems.append(f"its security groups could not be read ({str(error)[:120]})")
    loader = None
    roles = sorted(r["RoleArn"] for r in cluster.get("AssociatedRoles") or [] if r.get("Status") == "ACTIVE" and r.get("RoleArn"))
    try:
        loader = next((role for role in roles if reader.can_read(role, bucket, account)), None)
        if loader is None:
            problems.append("no bulk-loader role on it can read the run's source bucket")
    except NotSent as error:
        problems.append(f"its bulk-loader role could not be checked ({str(error)[:120]})")
    arn, resource_id = str(cluster.get("DBClusterArn") or ""), str(cluster.get("DbClusterResourceId") or "")
    if problems:
        return Candidate(name, tuple(problems), arn, resource_id)
    configuration = {"s3BucketArn": f"arn:aws:s3:::{bucket}", "neptuneClusterArn": arn, "neptuneClusterResourceId": resource_id,
                     "neptuneBulkUploadRoleArn": str(loader), "vpcSubnetIds": ",".join(subnets), "vpcSecurityGroupId": str(group_id)}
    return Candidate(name, (), arn, resource_id, configuration)


def candidates(reader: Reader, bucket: str, account: str) -> list[Candidate]:
    return sorted((judge(reader, cluster, bucket, account) for cluster in reader.clusters()), key=lambda c: c.name)


def describe(found: list[Candidate]) -> str:
    if not found:
        return "No Neptune cluster exists in this region.\n"
    lines = []
    for number, candidate in enumerate(found, 1):
        state = "can be used" if candidate.usable else "cannot be used: " + "; ".join(candidate.problems)
        lines.append(f"  {number}. {candidate.name}: {state}")
    return "Neptune clusters in this region:\n" + "\n".join(lines) + "\n"


def choose(found: list[Candidate], graph: str | None, mode: str, prompt: Callable[[str], str] | None,
           say: Callable[[str], None]) -> Candidate | None:
    """None means a new graph. --graph new|existing|<name>; with no --graph, interactive mode asks and autonomous creates."""
    if graph == "new" or (graph is None and mode == "autonomous"):
        return None
    if graph not in (None, "existing"):
        match = next((c for c in found if c.name == graph), None)
        if match is None:
            raise Stop(Outcome.REFUSED, f"there is no Neptune cluster named {graph} in this region")
        if not match.usable:
            raise Stop(Outcome.REFUSED, f"{graph} cannot be used: " + "; ".join(match.problems))
        return match
    say(describe(found))
    usable = [c for c in found if c.usable]
    if not usable:
        say("None can be used as it is, so Reframe will create a new graph.\n" + NEW_GRAPH_NOTE + "\n")
        return None
    if prompt is None:
        raise Stop(Outcome.WAITING_HUMAN, "choosing a Neptune cluster needs a terminal; pass --graph new or --graph <name>")
    say(OWNERSHIP_NOTE + "\n" + SHARING_NOTE + "\n" + NEW_GRAPH_NOTE + "\n")
    while True:
        try:
            answer = prompt("Type the number or name of the cluster to use, or press Enter for a new graph: ").strip()
        except EOFError:
            raise Stop(Outcome.WAITING_HUMAN, "no Neptune choice was given") from None
        if not answer:
            return None
        match = found[int(answer) - 1] if answer.isdigit() and 0 < int(answer) <= len(found) else next(
            (c for c in found if c.name == answer), None)
        if match is not None and match.usable:
            return match
        say("That cluster cannot be used. " + ("; ".join(match.problems) if match else "No such cluster.") + "\n")


def terraform_variables(chosen: Candidate | None) -> dict[str, Any]:
    if chosen is None:
        return {"existing_graph": None}
    return {"existing_graph": {"name": chosen.name, "cluster_arn": chosen.cluster_arn, "cluster_resource_id": chosen.cluster_resource_id,
                               "configuration": dict(chosen.configuration or {})}}
