"""Pipeline 3, part 2: worked examples for each recommended rule (docs/pipeline-3.md, section 8.7).

Each rule has one to three examples: a "given" (inputs, as field and value) and a "then" (the outcome), using the
values, codes and messages the code has. Reframe checks that every quoted value in an example (a message, a code in
quotes) appears in a file the decision cites; numbers are not checked, since an example may use any amount. An example
that fails is removed and counted on its own rule; a rule keeps its decision even when all its examples are removed.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from reframe.reconcile.decide import CITE, EXAMPLE_GUIDE as GUIDE, EXAMPLES as SCHEMA  # noqa: F401

QUOTED = re.compile(r"'([^']+)'|\"([^\"]+)\"")
PLACEHOLDER = re.compile(r"<[^>]*>|\.\.\.|…")


def _normal(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().upper()


def cited_text(cites: list[str], legacy: Path) -> str:
    """The text of every file the decision cites, normalized for matching."""
    root, seen, parts = legacy.resolve(), set(), []
    for cite in cites:
        m = CITE.match(str(cite).strip())
        path = (legacy / (m["path"] if m else str(cite).split(":")[0])).resolve()
        if path in seen or not path.is_relative_to(root) or not path.is_file():
            continue
        seen.add(path)
        parts.append(_normal(path.read_text(errors="replace")))
    return "\n".join(parts)


def quoted_values(example: dict[str, Any]) -> list[str]:
    texts = [str(g.get("value", "")) for g in example.get("given") or [] if isinstance(g, dict)] + [str(example.get("then", ""))]
    found = []
    for text in texts:
        for m in QUOTED.finditer(text):
            found.append(m.group(1) or m.group(2))
    return found


def holds(value: str, source: str) -> bool:
    """A quoted value is in the source if each of its parts (split at placeholders such as <name> or ...) is."""
    parts = [_normal(p) for p in PLACEHOLDER.split(value)]
    parts = [p for p in parts if p]
    return all(p in source for p in parts)


def check(examples: list[dict[str, Any]] | None, cites: list[str], legacy: Path) -> tuple[list[dict[str, Any]], int]:
    """(the examples kept, the number removed)."""
    source = cited_text(cites, legacy)
    kept, removed = [], 0
    for ex in (examples or [])[:3]:
        if not isinstance(ex, dict) or not str(ex.get("then", "")).strip():
            removed += 1
            continue
        if all(holds(v, source) for v in quoted_values(ex)):
            kept.append({"given": [{"field": str(g.get("field", "")), "value": str(g.get("value", ""))} for g in ex.get("given") or [] if isinstance(g, dict)],
                         "then": str(ex["then"])})
        else:
            removed += 1
    return kept, removed + max(0, len(examples or []) - 3)


def check_rules(rules: list[dict[str, Any]], cites: list[str], legacy: Path) -> tuple[list[dict[str, Any]], int]:
    """Every rule of a decision with its examples checked, each rule with its own count of examples removed (P3-27);
    returns the rules and the examples removed in all."""
    out, removed = [], 0
    for r in rules or []:
        kept, lost = check(r.get("examples"), cites, legacy)
        out.append({**r, "examples": kept, "examples_removed": lost})
        removed += lost
    return out, removed
