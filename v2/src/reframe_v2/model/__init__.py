"""The canonical model: versioned records and the rules that keep versions honest (specification section 6)."""

from reframe_v2.model.hashing import canonical_json, content_hash
from reframe_v2.model.records import RECORD_TYPES, Record, Ref
from reframe_v2.model.schemas import SchemaError, catalog, validate
from reframe_v2.model.store import (
    ApprovalState,
    IntegrityError,
    MixedVersionError,
    UnknownVersionError,
    VersionError,
    VersionStore,
)

__all__ = [
    "RECORD_TYPES",
    "ApprovalState",
    "IntegrityError",
    "MixedVersionError",
    "Record",
    "Ref",
    "SchemaError",
    "UnknownVersionError",
    "VersionError",
    "VersionStore",
    "canonical_json",
    "catalog",
    "content_hash",
    "validate",
]
