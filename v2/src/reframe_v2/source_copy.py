"""The source copy AWS reads: the snapshot archive written once to the declared prefix of the project bucket (P1-05).

The envelope's one data-plane write in stage D. The key is named from the archive's hash, so the same
snapshot always lands at the same key, and a copy already there with the same SHA-256 is reused, never
written again. The write is allowed only under the resources file's declared prefixes (check_write).
An intent is recorded before the write and a receipt after; an earlier write whose outcome is unknown
is settled from S3's own record of the object (head-object), never by writing again blindly.
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from reframe_v2.resources_file import Resources, check_write
from reframe_v2.state_store import PASSED_ENVIRONMENT, Result, Runner, run_subprocess


class CopyError(Exception):
    """The copy could not be made or checked; the message says why."""


class CopyUncertain(CopyError):
    """A write may or may not have happened; it is settled from S3's state before anything else."""


@dataclass(frozen=True)
class SourceCopy:
    bucket: str
    key: str
    sha256: str
    """"sha256:<hex>" of the archive."""
    version_id: str | None
    reused: bool

    @property
    def uri(self) -> str:
        return f"s3://{self.bucket}/{self.key}"


def key_for(resources: Resources, archive_sha256: str) -> str:
    prefix = resources.write_prefixes[0] if resources.write_prefixes else ""
    return f"{prefix}source/{archive_sha256.split(':', 1)[-1][:16]}.zip"


class S3Writer:
    """head-object and put-object through the AWS CLI with the engineer's own sign-in."""

    def __init__(self, region: str, profile: str | None, *, runner: Runner = run_subprocess,
                 parent_environment: dict[str, str] | None = None, timeout_seconds: float = 300) -> None:
        self.region, self.profile, self.runner, self.timeout = region, profile, runner, timeout_seconds
        source = os.environ if parent_environment is None else parent_environment
        self.env = {name: source[name] for name in PASSED_ENVIRONMENT if name in source}
        self.env["AWS_PAGER"] = ""

    def _aws(self, *arguments: str) -> Result:
        argv = ["aws", "s3api", *arguments, "--region", self.region, "--output", "json", "--no-cli-pager"]
        if self.profile:
            argv += ["--profile", self.profile]
        return self.runner(argv, self.env, self.timeout)

    def head(self, bucket: str, key: str, owner: str) -> dict | None:
        try:
            result = self._aws("head-object", "--bucket", bucket, "--key", key, "--expected-bucket-owner", owner, "--checksum-mode", "ENABLED")
        except (subprocess.TimeoutExpired, OSError) as error:
            raise CopyError(f"head-object did not complete ({type(error).__name__})") from None
        if result.returncode != 0:
            if "(404)" in result.stderr or "Not Found" in result.stderr or "(NoSuchKey)" in result.stderr:
                return None
            raise CopyError("head-object failed; sign in again if the session expired, then rerun")
        return json.loads(result.stdout or "{}")

    def put(self, bucket: str, key: str, owner: str, data: bytes, digest_hex: str) -> dict:
        checksum = base64.b64encode(bytes.fromhex(digest_hex)).decode()
        with tempfile.NamedTemporaryFile(prefix="reframe-source-", suffix=".zip") as body:
            body.write(data)
            body.flush()
            try:
                result = self._aws("put-object", "--bucket", bucket, "--key", key, "--body", body.name, "--expected-bucket-owner", owner,
                                   "--checksum-sha256", checksum, "--metadata", f"reframe-sha256={digest_hex}")
            except (subprocess.TimeoutExpired, OSError) as error:
                raise CopyUncertain(f"put-object did not complete ({type(error).__name__}); the write is UNCERTAIN") from None
        if result.returncode != 0:
            raise CopyUncertain("put-object failed after it was sent; settle it from S3's state")
        return json.loads(result.stdout or "{}")


def _matches(head: dict | None, digest_hex: str) -> bool:
    if not head:
        return False
    metadata = {k.casefold(): v for k, v in (head.get("Metadata") or {}).items()}
    checksum = head.get("ChecksumSHA256")
    return metadata.get("reframe-sha256") == digest_hex or (
        isinstance(checksum, str) and checksum == base64.b64encode(bytes.fromhex(digest_hex)).decode())


def ensure_copy(writer: S3Writer, resources: Resources, archive: bytes, archive_sha256: str, folder) -> SourceCopy:
    """Write the archive once, or reuse the copy already there. folder is the job's ProjectFolder."""
    digest_hex = archive_sha256.split(":", 1)[-1]
    key = key_for(resources, archive_sha256)
    check_write(resources, resources.bucket, key)
    receipt = folder.load("changes/source-copy.receipt.json")
    if receipt is not None and receipt.get("key") == key:
        return SourceCopy(resources.bucket, key, archive_sha256, receipt.get("version_id"), True)
    head = writer.head(resources.bucket, key, resources.account)
    if _matches(head, digest_hex):
        # Already in S3 with the same bytes, including a write recorded as uncertain: settled from S3's own state.
        folder.save("changes/source-copy.receipt.json", {"key": key, "sha256": archive_sha256, "version_id": head.get("VersionId"),
                                                         "settled_from": "head-object" if folder.exists("changes/source-copy.intent.json") else "reused"})
        return SourceCopy(resources.bucket, key, archive_sha256, head.get("VersionId"), True)
    if head is not None:
        raise CopyError("an object with different content is already at the source key; nothing was overwritten")
    if folder.exists("changes/source-copy.intent.json"):
        raise CopyUncertain("an earlier source write has an intent and no receipt. S3 holds no copy, so it did not land; "
                            "nothing is re-sent automatically. To allow one more attempt, a person removes "
                            "changes/source-copy.intent.json from the project folder and reruns")
    folder.save("changes/source-copy.intent.json", {"operation": "s3 put-object", "key": key, "sha256": archive_sha256, "bytes": len(archive)})
    reply = writer.put(resources.bucket, key, resources.account, archive, digest_hex)
    folder.save("changes/source-copy.receipt.json", {"key": key, "sha256": archive_sha256, "version_id": reply.get("VersionId"),
                                                     "etag": reply.get("ETag")})
    return SourceCopy(resources.bucket, key, archive_sha256, reply.get("VersionId"), False)
