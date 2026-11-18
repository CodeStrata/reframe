"""The version store: how records are committed, read, re-imported and checked (specification section 6, rules).

- Completed versions are immutable. A change creates a new revision; a failed
  attempt is recorded without overwriting completed work.
- Re-importing identical evidence is idempotent.
- Approvals and acceptance bind to an exact version. A change to anything an
  approval rests on marks that approval stale.
- A set of versions, such as a package, cannot mix versions of one record.

Records are held as canonical JSON text, the way a bucket or file backend
holds them, and every read checks the stored text against its content hash.
This in-memory store defines the rules; durable backends (section 8) must
pass the same tests.
"""

from __future__ import annotations

import enum
import json
from dataclasses import dataclass
from typing import Any

from reframe_v2.model.hashing import canonical_json
from reframe_v2.model.records import RECORD_TYPES, SCHEMA_VERSION, Record, Ref, hash_of
from reframe_v2.model.schemas import validate


class VersionError(Exception):
    """A version rule would be broken."""


class UnknownVersionError(VersionError):
    """A reference names a record version that does not exist, or exists with other content."""


class MixedVersionError(VersionError):
    """A set of versions contains two revisions of the same record."""


class IntegrityError(VersionError):
    """Stored content no longer matches its content hash. The damaged copy is kept, never rehashed."""


class ApprovalState(enum.Enum):
    CURRENT = "CURRENT"
    STALE = "STALE"


@dataclass(frozen=True)
class FailedAttempt:
    record_type: str
    record_id: str
    reason: str
    attempted_hash: str | None
    latest_revision: int


class VersionStore:
    def __init__(self) -> None:
        self._data: dict[tuple[str, int], str] = {}
        self._order: list[tuple[str, int]] = []
        self._heads: dict[str, int] = {}
        self._types: dict[str, str] = {}
        self._attempts: list[FailedAttempt] = []

    # Writing -----------------------------------------------------------------

    def commit(
        self, record_type: str, record_id: str, body: dict[str, Any], depends_on: tuple[Ref, ...] | list[Ref] = ()
    ) -> Record:
        """Store a new version, or return the latest one unchanged when the content is identical."""
        if record_type not in RECORD_TYPES:
            raise VersionError(f"unknown record type {record_type!r}")
        deps = tuple(sorted(set(depends_on)))
        self._check_dependencies(record_id, deps)
        content = hash_of(record_type, record_id, deps, body)
        head = self._heads.get(record_id, 0)
        if head:
            if self._types[record_id] != record_type:
                raise VersionError(f"{record_id} is a {self._types[record_id]} record, not {record_type}")
            latest = self.get(record_id, head)
            if latest.content_hash == content:
                return latest
        record_json = self._record_json(record_type, record_id, head + 1, deps, body, content)
        validate(record_json)
        return self._write(record_json)

    def import_record(self, record_json: dict[str, Any]) -> Record:
        """Bring in a record exported from another store. Identical content is a no-op; anything else must be the next revision."""
        validate(record_json)
        record_type, record_id, revision = record_json["record_type"], record_json["id"], record_json["revision"]
        if record_json["schema"] != f"{record_type}/{SCHEMA_VERSION}":
            raise VersionError(f"{record_id}: schema {record_json['schema']} is not supported")
        deps = tuple(sorted(Ref.from_json(ref) for ref in record_json["depends_on"]))
        expected = hash_of(record_type, record_id, deps, record_json["body"])
        if expected != record_json["content_hash"]:
            raise IntegrityError(f"{record_id} revision {revision}: content does not match its hash; nothing imported")
        if (record_id, revision) in self._data:
            existing = self.get(record_id, revision)
            if existing.content_hash == expected:
                return existing
            raise VersionError(f"{record_id} revision {revision} already exists with other content; completed versions are immutable")
        head = self._heads.get(record_id, 0)
        if head and self._types[record_id] != record_type:
            raise VersionError(f"{record_id} is a {self._types[record_id]} record, not {record_type}")
        if revision != head + 1:
            raise VersionError(f"{record_id}: revision {revision} cannot follow revision {head}")
        self._check_dependencies(record_id, deps)
        return self._write(self._record_json(record_type, record_id, revision, deps, record_json["body"], expected))

    def record_failed_attempt(
        self, record_type: str, record_id: str, reason: str, body: dict[str, Any] | None = None
    ) -> FailedAttempt:
        """Record that producing a new version failed. Completed versions are left exactly as they were."""
        attempted = hash_of(record_type, record_id, (), body) if body is not None else None
        attempt = FailedAttempt(record_type, record_id, reason, attempted, self._heads.get(record_id, 0))
        self._attempts.append(attempt)
        return attempt

    # Reading -----------------------------------------------------------------

    def get(self, record_id: str, revision: int) -> Record:
        try:
            text = self._data[(record_id, revision)]
        except KeyError:
            raise UnknownVersionError(f"{record_id} revision {revision} does not exist") from None
        stored = json.loads(text)
        deps = tuple(sorted(Ref.from_json(ref) for ref in stored["depends_on"]))
        actual = hash_of(stored["record_type"], stored["id"], deps, stored["body"])
        if actual != stored["content_hash"] or stored["revision"] != revision or stored["id"] != record_id:
            raise IntegrityError(f"{record_id} revision {revision} is damaged; it is kept as found and must be regenerated or restored")
        return Record(stored["record_type"], record_id, revision, deps, canonical_json(stored["body"]).decode("utf-8"), actual)

    def resolve(self, ref: Ref) -> Record:
        """The exact version a reference names; refuses a reference whose hash does not match."""
        record = self.get(ref.id, ref.revision)
        if record.content_hash != ref.content_hash:
            raise UnknownVersionError(f"{ref.id} revision {ref.revision} has other content than the reference names")
        return record

    def latest(self, record_id: str) -> Record:
        head = self._heads.get(record_id)
        if not head:
            raise UnknownVersionError(f"{record_id} does not exist")
        return self.get(record_id, head)

    def history(self, record_id: str) -> list[Record]:
        return [self.get(record_id, revision) for revision in range(1, self._heads.get(record_id, 0) + 1)]

    def failed_attempts(self, record_id: str | None = None) -> list[FailedAttempt]:
        return [attempt for attempt in self._attempts if record_id in (None, attempt.record_id)]

    def export(self) -> list[dict[str, Any]]:
        """Every version in the order it was stored, so dependencies always come first and an import can replay it."""
        return [self.get(record_id, revision).as_json() for record_id, revision in self._order]

    # Version rules -----------------------------------------------------------

    def stale_reasons(self, ref: Ref) -> list[str]:
        """Why a version, or anything it rests on, has been superseded. Empty when it is current."""
        reasons: list[str] = []
        seen: set[Ref] = set()
        pending = [ref]
        while pending:
            current = pending.pop()
            if current in seen:
                continue
            seen.add(current)
            record = self.resolve(current)
            head = self._heads[current.id]
            if head > current.revision:
                reasons.append(f"{current.id} revision {current.revision} was superseded by revision {head}")
            pending.extend(record.depends_on)
        return sorted(reasons)

    def approval_state(self, approval: Record) -> ApprovalState:
        """An approval is current only while the exact version it binds to, and everything that rests on, is current."""
        body = approval.body
        if approval.record_type != "human_input" or "binds_to" not in body:
            raise VersionError(f"{approval.id} is not an approval bound to a version")
        return ApprovalState.STALE if self.stale_reasons(Ref.from_json(body["binds_to"])) else ApprovalState.CURRENT

    def check_version_set(self, refs: list[Ref] | tuple[Ref, ...]) -> tuple[Ref, ...]:
        """The full set of versions these references rest on. Refuses two revisions of one record anywhere in it."""
        closure: dict[Ref, None] = {}
        pending = list(refs)
        while pending:
            current = pending.pop()
            if current in closure:
                continue
            closure[current] = None
            pending.extend(self.resolve(current).depends_on)
        by_id: dict[str, set[int]] = {}
        for ref in closure:
            by_id.setdefault(ref.id, set()).add(ref.revision)
        mixed = {record_id: sorted(revisions) for record_id, revisions in by_id.items() if len(revisions) > 1}
        if mixed:
            details = "; ".join(f"{record_id} revisions {revisions}" for record_id, revisions in sorted(mixed.items()))
            raise MixedVersionError(f"the set mixes versions: {details}")
        return tuple(sorted(closure))

    # Internals ---------------------------------------------------------------

    def _check_dependencies(self, record_id: str, deps: tuple[Ref, ...]) -> None:
        for ref in deps:
            if ref.id == record_id:
                raise VersionError(f"{record_id} cannot depend on itself")
            self.resolve(ref)
        ids = [ref.id for ref in deps]
        if len(ids) != len(set(ids)):
            raise MixedVersionError(f"{record_id} depends on two revisions of one record")

    @staticmethod
    def _record_json(
        record_type: str, record_id: str, revision: int, deps: tuple[Ref, ...], body: dict[str, Any], content: str
    ) -> dict[str, Any]:
        return {
            "schema": f"{record_type}/{SCHEMA_VERSION}",
            "record_type": record_type,
            "id": record_id,
            "revision": revision,
            "content_hash": content,
            "depends_on": [ref.as_json() for ref in deps],
            "body": json.loads(canonical_json(body)),
        }

    def _write(self, record_json: dict[str, Any]) -> Record:
        key = (record_json["id"], record_json["revision"])
        if key in self._data:
            raise VersionError(f"{key[0]} revision {key[1]} already exists; completed versions are immutable")
        self._data[key] = canonical_json(record_json).decode("utf-8")
        self._order.append(key)
        self._heads[key[0]] = key[1]
        self._types[key[0]] = record_json["record_type"]
        return self.get(*key)
