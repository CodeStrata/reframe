"""Running on client-owned resources (FR-02, section 8; P2-02).

With --resources <file>, a run uses resources the client owns. Reframe checks
them read-only before any job starts and reports every problem at once. It
never tags them, records them as its own or deletes them; the only writes
allowed are the declared data-plane writes: source upload and outputs under
the bucket's declared prefixes, and project state under the state bucket's.
AWS Transform jobs and their records are the other allowed write, governed
by the Transform adapter and the execution envelope.

With neither --provision nor --resources, Reframe lists what the run needs
and stops (what_the_run_needs).

Connector types are the ones AWS reported for the live connectors v1 used
(16 and 17 November 2026), and the connector record's fields are the ones
v1 read from get_resource; nothing here is a guess.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from reframe_v2.model.schemas import SchemaError, validate_document
from reframe_v2.resources import Manifest, ResourceError
from reframe_v2.state_store import PASSED_ENVIRONMENT, Result, Runner, run_subprocess

ASSESSMENT_CONNECTOR_TYPE = "mainframe_modernization|s3|2"
REIMAGINE_CONNECTOR_TYPE = "mainframe_modernization|reimagine|1"
STACK_READY = frozenset({"CREATE_COMPLETE", "UPDATE_COMPLETE"})


@dataclass(frozen=True)
class Resources:
    account: str
    region: str
    state_bucket: str
    state_prefixes: tuple[str, ...]
    bucket: str
    write_prefixes: tuple[str, ...]
    sandbox_role: str
    workspace_id: str
    assessment_connector: str
    reimagine_connector: str | None
    neptune_stack: str | None

    @property
    def client_owned_ids(self) -> frozenset[str]:
        ids = {self.state_bucket, self.bucket, self.sandbox_role, self.workspace_id, self.assessment_connector}
        ids |= {value for value in (self.reimagine_connector, self.neptune_stack) if value}
        return frozenset(ids)


def load(document: dict[str, Any]) -> Resources:
    """Validate a resources file and return what it names. Every schema problem is listed."""
    try:
        validate_document("resources_file", document)
    except SchemaError as error:
        raise ResourceError(str(error)) from None
    transform, stack = document["transform"], document["neptune_stack"]
    if (transform["reimagine_connector"] is None) != (stack is None):
        raise ResourceError("a reimagine connector and its Neptune stack are named together, or neither is")
    return Resources(
        document["account"], document["region"],
        document["state_bucket"]["name"], tuple(document["state_bucket"]["write_prefixes"]),
        document["bucket"]["name"], tuple(document["bucket"]["write_prefixes"]),
        document["sandbox_role"]["name"], transform["workspace_id"], transform["assessment_connector"],
        transform["reimagine_connector"], stack["name"] if stack else None,
    )


def load_file(path: Path) -> Resources:
    try:
        return load(json.loads(path.read_text(encoding="utf-8")))
    except ValueError as error:
        raise ResourceError(f"{path} is not JSON: {error}") from None


# What the run needs -----------------------------------------------------------


def what_the_run_needs(reimagine: bool, backend: str) -> list[str]:
    """Section 8's resources, for a run started with neither --provision nor --resources. Reframe stops after listing them."""
    needs = [
        "Reframe state bucket for the account and region (administrator, once, or reframe bootstrap --terraform)",
        "S3 bucket for this repository: encrypted, versioned, public access blocked",
        "Sandbox IAM role that denies reads outside that bucket",
        "AWS Transform workspace with an assessment connector",
    ]
    if reimagine:
        needs += ["Neptune Serverless knowledge graph (cluster, subnets, security group, bulk-loader role)",
                  "Reimagine connector and its IAM role (one per workspace)"]
    if backend == "bedrock":
        needs += ["Bedrock access to the pinned Claude models in the run's region (administrator, once)",
                  "Bedrock invoke permission on the pinned models or inference profiles only"]
    return needs + ["Then rerun with --provision, or with --resources <file> naming client-owned resources"]


# Read-only facts --------------------------------------------------------------


class ReaderError(Exception):
    """A read-only check could not be made. The resource is not assumed fit."""


@dataclass(frozen=True)
class BucketFacts:
    """A bucket the named account owns (a bucket owned by anyone else is never reported as found)."""

    region: str
    versioning: str | None
    encryption: str | None
    public_access_blocked: bool


class Reader(Protocol):
    def caller_account(self) -> str: ...
    def bucket(self, name: str, account: str) -> BucketFacts | None: ...
    def role_exists(self, name: str) -> bool: ...
    def denied(self, checks: list[tuple[str, str]]) -> list[tuple[str, str]]: ...
    def connector(self, workspace_id: str, connector_id: str) -> dict[str, Any] | None: ...
    def stack_status(self, name: str) -> str | None: ...


@dataclass(frozen=True)
class Problem:
    resource: str
    message: str


@dataclass(frozen=True)
class CheckReport:
    problems: tuple[Problem, ...]
    checked: tuple[str, ...] = field(default=())

    @property
    def ok(self) -> bool:
        return not self.problems

    def text(self) -> str:
        if self.ok:
            return "Every client-owned resource passed its read-only checks; nothing was changed."
        lines = [f"- {p.resource}: {p.message}" for p in self.problems]
        return "These client-owned resources cannot be used yet; no job was started and nothing was changed:\n" + "\n".join(lines)


def check(resources: Resources, reader: Reader) -> CheckReport:
    """Every read-only check, all problems reported together. Makes no change in AWS."""
    problems: list[Problem] = []
    checked: list[str] = []

    def attempt(resource: str, test) -> None:
        checked.append(resource)
        try:
            for message in test():
                problems.append(Problem(resource, message))
        except ReaderError as error:
            problems.append(Problem(resource, f"could not be checked ({error}); it is not assumed fit"))

    def account():
        found = reader.caller_account()
        if found != resources.account:
            yield "the signed-in profile is for a different account than the resources file names"

    def bucket(name: str, label: str):
        def test():
            facts = reader.bucket(name, resources.account)
            if facts is None:
                yield f"{label} not found"
                return
            if facts.region != resources.region:
                yield f"{label} is in {facts.region}, not {resources.region}"
            if facts.versioning != "Enabled":
                yield f"{label} does not have versioning enabled"
            if facts.encryption not in ("AES256", "aws:kms", "aws:kms:dsse"):
                yield f"{label} has no default encryption"
            if not facts.public_access_blocked:
                yield f"{label} does not block all public access"
        return test

    def role():
        if not reader.role_exists(resources.sandbox_role):
            yield "sandbox role not found"

    def permissions():
        wanted = []
        for name, prefixes in ((resources.bucket, resources.write_prefixes), (resources.state_bucket, resources.state_prefixes)):
            wanted.append(("s3:ListBucket", f"arn:aws:s3:::{name}"))
            for prefix in prefixes:
                wanted += [("s3:GetObject", f"arn:aws:s3:::{name}/{prefix}*"), ("s3:PutObject", f"arn:aws:s3:::{name}/{prefix}*")]
        for action, resource in reader.denied(wanted):
            yield f"the signed-in profile is not allowed {action} on {resource.removeprefix('arn:aws:s3:::')}"

    def connector(connector_id: str, expected_type: str, label: str):
        def test():
            record = reader.connector(resources.workspace_id, connector_id)
            if record is None:
                yield f"{label} not found in the workspace"
                return
            if record.get("connectorType") != expected_type:
                yield f"{label} is of type {record.get('connectorType')!r}, not {expected_type}"
            connection = (record.get("accountConnection") or {}).get("awsAccountConnection") or {}
            if connection.get("status") != "ACTIVE":
                yield f"{label} is not active for this account (status {connection.get('status')!r})"
            if connection.get("accountId") != resources.account:
                yield f"{label} is connected to a different account"
        return test

    def stack():
        status = reader.stack_status(resources.neptune_stack)
        if status is None:
            yield "Neptune stack not found"
        elif status not in STACK_READY:
            yield f"Neptune stack is {status}, not ready"

    attempt("account", account)
    attempt("state bucket", bucket(resources.state_bucket, "state bucket"))
    attempt("bucket", bucket(resources.bucket, "bucket"))
    attempt("sandbox role", role)
    attempt("permissions", permissions)
    attempt("assessment connector", connector(resources.assessment_connector, ASSESSMENT_CONNECTOR_TYPE, "assessment connector"))
    if resources.reimagine_connector:
        attempt("reimagine connector", connector(resources.reimagine_connector, REIMAGINE_CONNECTOR_TYPE, "reimagine connector"))
        attempt("Neptune stack", stack)
    return CheckReport(tuple(problems), tuple(checked))


# What Reframe may change ------------------------------------------------------


def check_write(resources: Resources, bucket: str, key: str) -> None:
    """Allow a data-plane write only under a declared prefix of a declared bucket."""
    allowed = {resources.bucket: resources.write_prefixes, resources.state_bucket: resources.state_prefixes}
    prefixes = allowed.get(bucket)
    if prefixes is None:
        raise ResourceError(f"{bucket} is not a bucket this run may write to")
    if ".." in key.split("/") or not any(key.startswith(prefix) for prefix in prefixes):
        raise ResourceError(f"{key} is outside the declared write prefixes of {bucket}; client-owned data is not touched")


def check_manifest(manifest: Manifest, resources: Resources) -> None:
    """Client-owned resources never enter Reframe's manifest, so nothing Reframe owns can be confused with them."""
    claimed = sorted(set(manifest.entries) & resources.client_owned_ids)
    if claimed:
        raise ResourceError("client-owned resources are never recorded as Reframe's: " + ", ".join(claimed))


def may_tag(resources: Resources, resource_id: str) -> bool:
    """Client-owned resources are never tagged."""
    return resource_id not in resources.client_owned_ids


# The AWS CLI reader -----------------------------------------------------------


class AwsCliReader:
    """Reader over read-only AWS CLI calls, with the run's profile and region and no shell.

    Connector records come from the AWS Transform adapter's read-only get_resource, passed in
    as read_connector, so this reader never starts the MCP server itself.
    """

    def __init__(self, region: str, profile: str | None, read_connector, *, runner: Runner = run_subprocess,
                 parent_environment: dict[str, str] | None = None, timeout_seconds: float = 60) -> None:
        self.region, self.profile, self.read_connector = region, profile, read_connector
        self.runner, self.timeout = runner, timeout_seconds
        source = os.environ if parent_environment is None else parent_environment
        self.env = {name: source[name] for name in PASSED_ENVIRONMENT if name in source}
        self.env["AWS_PAGER"] = ""
        self._caller_arn: str | None = None

    def _aws(self, *arguments: str, missing: tuple[str, ...] = ()) -> dict[str, Any] | None:
        argv = ["aws", *arguments, "--region", self.region, "--output", "json", "--no-cli-pager"]
        if self.profile:
            argv += ["--profile", self.profile]
        try:
            result: Result = self.runner(argv, self.env, self.timeout)
        except (subprocess.TimeoutExpired, OSError) as error:
            raise ReaderError(f"{arguments[0]} {arguments[1]} did not complete ({type(error).__name__})") from None
        if result.returncode != 0:
            if any(f"({code})" in result.stderr for code in missing):
                return None
            code = result.stderr.split("(", 1)[1].split(")", 1)[0] if "An error occurred (" in result.stderr else "unknown error"
            raise ReaderError(f"{arguments[0]} {arguments[1]} failed: {code}")
        try:
            value = json.loads(result.stdout or "{}")
        except ValueError:
            raise ReaderError(f"{arguments[0]} {arguments[1]} returned a reply that is not JSON") from None
        if not isinstance(value, dict):
            raise ReaderError(f"{arguments[0]} {arguments[1]} returned an unexpected reply")
        return value

    def caller_account(self) -> str:
        identity = self._aws("sts", "get-caller-identity")
        self._caller_arn = identity.get("Arn")
        return str(identity.get("Account", ""))

    def bucket(self, name: str, account: str) -> BucketFacts | None:
        # With an expected owner, head-bucket succeeds only for a bucket that account owns. A 403 means
        # another owner or no permission to look: either way it is reported as not checkable, never as fine.
        if self._aws("s3api", "head-bucket", "--bucket", name, "--expected-bucket-owner", account,
                     missing=("404", "NoSuchBucket")) is None:
            return None
        location = self._aws("s3api", "get-bucket-location", "--bucket", name)
        region = location.get("LocationConstraint") or "us-east-1"
        versioning = self._aws("s3api", "get-bucket-versioning", "--bucket", name).get("Status")
        encryption = self._aws("s3api", "get-bucket-encryption", "--bucket", name,
                               missing=("ServerSideEncryptionConfigurationNotFoundError",))
        rules = ((encryption or {}).get("ServerSideEncryptionConfiguration") or {}).get("Rules") or []
        algorithm = ((rules[0].get("ApplyServerSideEncryptionByDefault") or {}).get("SSEAlgorithm")) if rules else None
        block = self._aws("s3api", "get-public-access-block", "--bucket", name, missing=("NoSuchPublicAccessBlockConfiguration",))
        settings = (block or {}).get("PublicAccessBlockConfiguration") or {}
        blocked = all(settings.get(key) is True for key in ("BlockPublicAcls", "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"))
        return BucketFacts(region, versioning, algorithm, blocked)

    def role_exists(self, name: str) -> bool:
        return self._aws("iam", "get-role", "--role-name", name, missing=("NoSuchEntity",)) is not None

    def _principal(self) -> str:
        """The IAM role or user behind the signed-in session, for the read-only policy simulator."""
        if self._caller_arn is None:
            self.caller_account()
        arn = self._caller_arn or ""
        parts = arn.split(":")
        if len(parts) == 6 and parts[2] == "sts" and parts[5].startswith("assumed-role/"):
            role_name = parts[5].split("/")[1]
            role = self._aws("iam", "get-role", "--role-name", role_name)
            return (role.get("Role") or {}).get("Arn") or ""
        if len(parts) == 6 and parts[2] == "iam":
            return arn
        raise ReaderError("the signed-in identity is not an IAM role or user the policy simulator can check")

    def denied(self, checks: list[tuple[str, str]]) -> list[tuple[str, str]]:
        principal = self._principal()
        refused = []
        for action, resource in checks:
            reply = self._aws("iam", "simulate-principal-policy", "--policy-source-arn", principal,
                              "--action-names", action, "--resource-arns", resource)
            results = reply.get("EvaluationResults") or []
            if not results or any(item.get("EvalDecision") != "allowed" for item in results):
                refused.append((action, resource))
        return refused

    def connector(self, workspace_id: str, connector_id: str) -> dict[str, Any] | None:
        return self.read_connector(workspace_id, connector_id)

    def stack_status(self, name: str) -> str | None:
        reply = self._aws("cloudformation", "describe-stacks", "--stack-name", name, missing=("ValidationError",))
        if reply is None:
            return None
        stacks = reply.get("Stacks") or []
        if len(stacks) != 1:
            raise ReaderError("describe-stacks returned an unexpected number of stacks")
        return stacks[0].get("StackStatus")


def transform_connector_reader(client):
    """read_connector for AwsCliReader, through the Transform adapter's read-only get_resource, with v1's recorded arguments."""
    from reframe_v2.transform import TransformError

    def read(workspace_id: str, connector_id: str) -> dict[str, Any] | None:
        # A failed read is never taken to mean "not found": the connector is reported as not checkable.
        try:
            return client.call("get_resource", {"resource": "connector", "workspaceId": workspace_id, "connectorId": connector_id})
        except TransformError as error:
            raise ReaderError(f"the connector could not be read ({error})") from None

    return read
