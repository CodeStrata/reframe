"""AWS's traceability file for one business function (spec/<Domain>/<Function>/traceability.yaml).

Recorded shape (spike 1): function, generated_at, summary (total_rules, captured, not_applicable, ...,
requirement_reconciliation) and rules, each with rule_id, program, disposition, reason and the requirements
it backs. Only safe_load is used; anything that is not a mapping reads as empty.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load(path: Path) -> dict[str, Any]:
    try:
        value = yaml.safe_load(path.read_text(errors="replace"))
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}
