"""Pipeline 4, stage D9: what each part of the design was made from, so a round can say why it redid a part (P4-09).

Each model stage keeps, beside a part's hash, a hash of each piece of its input ("parts"). When the input changes, the
pieces whose hash changed are why the part is redone; the round's changes-<round>.md says so in words.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()[:16]


def parts(data: dict[str, Any], method: str) -> dict[str, str]:
    return {**{k: _hash(v) for k, v in data.items()}, "method": method}


def changed(before: dict[str, Any] | None, now: dict[str, str]) -> list[str]:
    """The pieces of the input that differ from what the kept part was made from: ["new"] for a part not made before."""
    if not before:
        return ["new"]
    old = before.get("parts")
    if not old:
        return ["unrecorded"]
    found = sorted({k for k in now if old.get(k) != now[k]} | {k for k in old if k not in now})
    return found or ["unrecorded"]


def summary(todo: list[tuple[str, list[str]]], kept: list[str]) -> dict[str, Any]:
    return {"redone": [{"name": name, "changed": why} for name, why in todo], "kept": sorted(kept)}
