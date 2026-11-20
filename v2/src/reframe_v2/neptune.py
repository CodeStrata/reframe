"""Reuse an existing Neptune graph by name, or create one in its own private network (section 8; P2-06, P2-08).

Before a graph is created, Reframe lists the region's Neptune clusters with
read-only calls and checks each against what the reimagine connector needs.
A usable cluster is offered by name; the person chooses it, or chooses a new
graph. A chosen cluster is client-owned: Reframe never tags, changes or
deletes it. A new graph gets its own private network, as AWS's own Neptune
template builds one (#259); no existing network is read, used or changed.

The requirements are the ones v1 recorded for the reimagine connector (#206)
and the ones AWS's own Neptune template provides: nothing here is a guess
about a new AWS rule. The connector configuration keys are the six AWS
accepted for v1's connector.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from reframe_v2.resources_file import AwsCliReader, ReaderError
from reframe_v2.state_store import Runner, run_subprocess

MINIMUM_ENGINE = (1, 4, 5, 1)
CONFIGURATION_KEYS = ("s3BucketArn", "neptuneClusterArn", "neptuneClusterResourceId", "neptuneBulkUploadRoleArn",
                      "vpcSubnetIds", "vpcSecurityGroupId")
SHARING_NOTE = ("Section 8: each repository gets its own graph until P2 proves that two can share one safely. "
                "If another reimagine connector already uses this cluster, both write into the same graph.")
OWNERSHIP_NOTE = "Reframe uses it as it is: it never tags, changes or deletes it, and teardown leaves it alone."
NEW_GRAPH_NOTE = ("A new graph gets its own private network: a VPC, two subnets in different Availability Zones, "
                  "a route table and an S3 gateway endpoint, with no internet gateway or NAT. The network has no charge, "
                  "and teardown removes it with the graph. Neptune bills from the moment it is created.")


class GraphError(Exception):
    """No choice was made; nothing was written and nothing in AWS changed."""


class GraphReader(Protocol):
    """Read-only questions about Neptune and the network. None of them changes anything."""

    def account(self) -> str: ...
    def clusters(self) -> list[dict[str, Any]]: ...
    def subnet_group(self, name: str) -> dict[str, Any]: ...
    def security_groups(self, ids: list[str]) -> list[dict[str, Any]]: ...
    def can_read(self, role_arn: str, bucket: str, account: str) -> bool: ...
    def route_tables(self, vpc_id: str, subnet_ids: list[str]) -> dict[str, str]: ...
    def s3_endpoint_route_tables(self, vpc_id: str) -> set[str]: ...


@dataclass(frozen=True)
class Candidate:
    """One existing Neptune cluster and whether the reimagine connector can use it."""

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


def _connector_group(reader: GraphReader, cluster_groups: list[str], port: int) -> tuple[str | None, str | None]:
    """A security group the cluster lets in on its port, and that may send to it. Returns (group, problem)."""
    groups = reader.security_groups(cluster_groups)
    sources = sorted({pair["GroupId"] for group in groups for permission in group.get("IpPermissions") or []
                      if _covers(permission, port) for pair in permission.get("UserIdGroupPairs") or [] if pair.get("GroupId")})
    if not sources:
        return None, f"no security group is allowed to reach it on port {port}, so the connector has none to use"
    for source in reader.security_groups(sources):
        for permission in source.get("IpPermissionsEgress") or []:
            if not _covers(permission, port):
                continue
            to_cluster = {pair.get("GroupId") for pair in permission.get("UserIdGroupPairs") or []} & set(cluster_groups)
            anywhere = any(item.get("CidrIp") == "0.0.0.0/0" for item in permission.get("IpRanges") or [])
            if to_cluster or anywhere:
                return source["GroupId"], None
    return None, f"no security group allowed to reach it may also send to it on port {port}"


def judge(reader: GraphReader, cluster: dict[str, Any], bucket: str, account: str) -> Candidate:
    """Check one cluster against what the reimagine connector needs. Every problem is reported, never just the first."""
    name = str(cluster.get("DBClusterIdentifier") or "")
    problems: list[str] = []
    status = cluster.get("Status")
    if status != "available":
        problems.append(f"it is {status or 'in an unknown state'}, not available")
    if not cluster.get("DBClusterMembers"):
        problems.append("it has no instances")
    version = engine(cluster.get("EngineVersion"))
    if version is None or version < MINIMUM_ENGINE:
        problems.append(f"engine {cluster.get('EngineVersion')} is older than the 1.4.5.1 AWS requires")
    if cluster.get("IAMDatabaseAuthenticationEnabled") is not True:
        problems.append("IAM authentication is off; AWS requires it")
    if cluster.get("StorageEncrypted") is not True:
        problems.append("storage is not encrypted; AWS requires it")
    if not cluster.get("ServerlessV2ScalingConfiguration"):
        problems.append("it is not Serverless; AWS requires a serverless scaling configuration")

    subnets: list[str] = []
    try:
        group = reader.subnet_group(str(cluster.get("DBSubnetGroup") or ""))
        vpc_id = str(group.get("VpcId") or "")
        listed = [s for s in group.get("Subnets") or [] if s.get("SubnetStatus", "Active") == "Active"]
        subnets = sorted(str(s["SubnetIdentifier"]) for s in listed if s.get("SubnetIdentifier"))
        zones = {(s.get("SubnetAvailabilityZone") or {}).get("Name") for s in listed} - {None}
        if len(zones) < 2:
            problems.append("its subnets are not in two Availability Zones")
        tables = reader.route_tables(vpc_id, subnets)
        lacking = sorted(set(tables.values()) - reader.s3_endpoint_route_tables(vpc_id))
        if lacking or len(tables) < len(subnets):
            problems.append("its subnets have no S3 gateway endpoint, which the bulk loader needs")
    except ReaderError as error:
        problems.append(f"its network could not be read ({error})")

    group_id = None
    try:
        port = int(cluster.get("Port") or 8182)
        cluster_groups = sorted(g["VpcSecurityGroupId"] for g in cluster.get("VpcSecurityGroups") or []
                                if g.get("Status", "active") == "active" and g.get("VpcSecurityGroupId"))
        group_id, problem = _connector_group(reader, cluster_groups, port)
        if problem:
            problems.append(problem)
    except ReaderError as error:
        problems.append(f"its security groups could not be read ({error})")

    loader = None
    roles = sorted(r["RoleArn"] for r in cluster.get("AssociatedRoles") or [] if r.get("Status") == "ACTIVE" and r.get("RoleArn"))
    try:
        loader = next((role for role in roles if reader.can_read(role, bucket, account)), None)
        if loader is None:
            problems.append(f"no bulk-loader role on it can read the bucket {bucket}; "
                            "name a bucket its loader role reads with --bucket")
    except ReaderError as error:
        problems.append(f"its bulk-loader role could not be checked ({error})")

    arn, resource_id = str(cluster.get("DBClusterArn") or ""), str(cluster.get("DbClusterResourceId") or "")
    if problems:
        return Candidate(name, tuple(problems), arn, resource_id)
    configuration = {"s3BucketArn": f"arn:aws:s3:::{bucket}", "neptuneClusterArn": arn,
                     "neptuneClusterResourceId": resource_id, "neptuneBulkUploadRoleArn": str(loader),
                     "vpcSubnetIds": ",".join(subnets), "vpcSecurityGroupId": str(group_id)}
    return Candidate(name, (), arn, resource_id, configuration)


def candidates(reader: GraphReader, bucket: str) -> list[Candidate]:
    """Every Neptune cluster in the region, judged, sorted by name."""
    account = reader.account()
    return sorted((judge(reader, cluster, bucket, account) for cluster in reader.clusters()), key=lambda c: c.name)


def describe(found: list[Candidate]) -> str:
    if not found:
        return "No Neptune cluster exists in this region.\n"
    lines = []
    for candidate in found:
        if candidate.usable:
            lines.append(f"  {candidate.name}: can serve the reimagine connector")
        else:
            lines.append(f"  {candidate.name}: cannot be used, because " + "; ".join(candidate.problems))
    return "Neptune clusters in this region:\n" + "\n".join(lines) + "\n"


def choose(found: list[Candidate], *, use: str | None = None, new: bool = False) -> Candidate | None:
    """Apply an answer given up front: --use <name> or --new. None means a new graph."""
    if use is not None and new:
        raise GraphError("choose either --use or --new, not both")
    if new:
        return None
    if use is None:
        raise GraphError("no answer was given")
    match = next((c for c in found if c.name == use), None)
    if match is None:
        raise GraphError(f"there is no Neptune cluster named {use} in this region")
    if not match.usable:
        raise GraphError(f"{use} cannot be used, because " + "; ".join(match.problems))
    return match


def ask(found: list[Candidate], prompt: Callable[[str], str], say: Callable[[str], None]) -> Candidate | None:
    """Ask the person which usable cluster to use, by name, or Enter for a new graph. None means a new graph."""
    say(describe(found))
    usable = [c for c in found if c.usable]
    if not usable:
        say("None can be used, so Reframe will create a new graph.\n")
        return None
    say(SHARING_NOTE + "\n" + OWNERSHIP_NOTE + "\n")
    names = ", ".join(c.name for c in usable)
    while True:
        try:
            answer = prompt(f"Type the name of the cluster to use ({names}), or press Enter to create a new graph: ").strip()
        except EOFError:
            raise GraphError("no answer was given") from None
        if not answer:
            return None
        try:
            return choose(found, use=answer)
        except GraphError as error:
            say(f"{error}\n")


def terraform_variables(chosen: Candidate | None) -> dict[str, Any]:
    """The project composition's variables for the choice. Nothing is created by writing them."""
    if chosen is not None:
        if not chosen.usable or chosen.configuration is None:
            raise GraphError(f"{chosen.name} cannot be used")
        return {"reimagine": True, "existing_graph": {"cluster_arn": chosen.cluster_arn,
                                                      "cluster_resource_id": chosen.cluster_resource_id,
                                                      "configuration": dict(chosen.configuration)}}
    return {"reimagine": True, "existing_graph": None}


def write_variables(path: Path, variables: dict[str, Any]) -> None:
    """Write the variables to a new file; an existing file is refused, never overwritten."""
    try:
        with path.open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(variables, indent=2) + "\n")
    except FileExistsError:
        raise GraphError(f"{path} already exists; nothing was written") from None


class AwsCliGraphReader(AwsCliReader):
    """GraphReader over read-only AWS CLI calls, with the run's profile and region and no shell."""

    def __init__(self, region: str, profile: str | None, *, runner: Runner = run_subprocess,
                 parent_environment: dict[str, str] | None = None, timeout_seconds: float = 60) -> None:
        super().__init__(region, profile, None, runner=runner, parent_environment=parent_environment,
                         timeout_seconds=timeout_seconds)

    def account(self) -> str:
        return self.caller_account()

    def clusters(self) -> list[dict[str, Any]]:
        reply = self._aws("neptune", "describe-db-clusters", "--filters", "Name=engine,Values=neptune")
        return [c for c in reply.get("DBClusters") or [] if c.get("Engine") == "neptune"]

    def subnet_group(self, name: str) -> dict[str, Any]:
        reply = self._aws("neptune", "describe-db-subnet-groups", "--db-subnet-group-name", name)
        groups = reply.get("DBSubnetGroups") or []
        if len(groups) != 1:
            raise ReaderError("describe-db-subnet-groups returned an unexpected number of groups")
        return groups[0]

    def security_groups(self, ids: list[str]) -> list[dict[str, Any]]:
        if not ids:
            return []
        return self._aws("ec2", "describe-security-groups", "--group-ids", *ids).get("SecurityGroups") or []

    def can_read(self, role_arn: str, bucket: str, account: str) -> bool:
        # AWS's template conditions the loader's S3 access on aws:ResourceAccount, which the simulator
        # only evaluates when given; the bucket is in the signed-in account (Reframe checks that separately).
        context = f"ContextKeyName=aws:ResourceAccount,ContextKeyValues={account},ContextKeyType=string"
        for action, resource in (("s3:GetObject", f"arn:aws:s3:::{bucket}/*"), ("s3:ListBucket", f"arn:aws:s3:::{bucket}")):
            reply = self._aws("iam", "simulate-principal-policy", "--policy-source-arn", role_arn, "--action-names", action,
                              "--resource-arns", resource, "--context-entries", context)
            results = reply.get("EvaluationResults") or []
            if not results or any(item.get("EvalDecision") != "allowed" for item in results):
                return False
        return True

    def route_tables(self, vpc_id: str, subnet_ids: list[str]) -> dict[str, str]:
        """Each subnet's route table: its explicit association, or else the VPC's main table."""
        tables = self._aws("ec2", "describe-route-tables", "--filters", f"Name=vpc-id,Values={vpc_id}").get("RouteTables") or []
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
        reply = self._aws("ec2", "describe-vpc-endpoints", "--filters", f"Name=vpc-id,Values={vpc_id}",
                          f"Name=service-name,Values=com.amazonaws.{self.region}.s3", "Name=vpc-endpoint-type,Values=Gateway")
        return {str(t) for e in reply.get("VpcEndpoints") or [] if e.get("State", "available").lower() == "available"
                for t in e.get("RouteTableIds") or []}
