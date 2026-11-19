"""Record and reference value types."""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from typing import Any

from reframe_v2.model.hashing import content_hash

RECORD_TYPES = (
    "project_policy",
    "source_snapshot",
    "claim_evidence",
    "human_input",
    "context_map",
    "canonical_design",
    "findings_assumptions",
    "operations_ledger",
    "artifact_graph",
    "readiness",
)

SCHEMA_VERSION = 1


@dataclass(frozen=True, order=True)
class Ref:
    """An exact version of a record."""

    id: str
    revision: int
    content_hash: str

    def as_json(self) -> dict[str, Any]:
        return {"id": self.id, "revision": self.revision, "content_hash": self.content_hash}

    @classmethod
    def from_json(cls, value: dict[str, Any]) -> Ref:
        return cls(value["id"], value["revision"], value["content_hash"])


@dataclass(frozen=True)
class Record:
    """One immutable version of a record. The body is held as canonical JSON text, so it cannot be changed in place."""

    record_type: str
    id: str
    revision: int
    depends_on: tuple[Ref, ...]
    _body: str = field(repr=False)
    content_hash: str

    @property
    def schema(self) -> str:
        return f"{self.record_type}/{SCHEMA_VERSION}"

    @property
    def body(self) -> dict[str, Any]:
        """A copy of the body; changing it never changes the record."""
        return json.loads(self._body)

    @property
    def ref(self) -> Ref:
        return Ref(self.id, self.revision, self.content_hash)

    def as_json(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "record_type": self.record_type,
            "id": self.id,
            "revision": self.revision,
            "content_hash": self.content_hash,
            "depends_on": [ref.as_json() for ref in self.depends_on],
            "body": self.body,
        }


def hashed_content(record_type: str, record_id: str, depends_on: tuple[Ref, ...], body: dict[str, Any]) -> dict[str, Any]:
    """What a content hash covers: everything except the revision number and the hash itself."""
    return {
        "schema": f"{record_type}/{SCHEMA_VERSION}",
        "record_type": record_type,
        "id": record_id,
        "depends_on": [ref.as_json() for ref in sorted(depends_on)],
        "body": copy.deepcopy(body),
    }


def hash_of(record_type: str, record_id: str, depends_on: tuple[Ref, ...], body: dict[str, Any]) -> str:
    return content_hash(hashed_content(record_type, record_id, depends_on, body))
