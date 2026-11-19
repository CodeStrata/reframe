"""Canonical JSON and content hashes (NFR-08: the same content always has the same hash)."""

from __future__ import annotations

import hashlib
import json
from typing import Any


def canonical_json(value: Any) -> bytes:
    """UTF-8 JSON with sorted keys and no insignificant whitespace.

    Floats are refused: amounts and counts in the model are integers or
    decimal strings, so a hash never depends on float formatting.
    """
    _refuse_floats(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def content_hash(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value)).hexdigest()


def _refuse_floats(value: Any) -> None:
    if isinstance(value, float):
        raise ValueError("floats are not allowed in canonical records; use an integer or a decimal string")
    if isinstance(value, dict):
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("record keys must be strings")
            _refuse_floats(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _refuse_floats(item)
