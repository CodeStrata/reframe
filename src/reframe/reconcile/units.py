"""Pipeline 3, stage R2: identical pairs agreed (docs/pipeline-3.md, section 4).

The comparison's pairs are many-to-one: many AWS Transform rules pair with one broader Claude rule (spike P3-01, finding 2).
So a **group** is one Claude rule with every AWS rule paired with it. A group whose pairs are all "same" is agreed without an
agent (R2); any other group, and every rule in no pair, is a **unit** for stage R4.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any

CHANGE_MARKS = ("change", "question")


def groups(pairs: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    found: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for p in pairs:
        found[p["claude"]].append(p)
    return dict(found)


def _marked(keys: list[str], marks: dict[str, Any]) -> dict[str, Any]:
    return {k: marks[k] for k in keys if k in marks and marks[k]["status"] in CHANGE_MARKS}


def agreed(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    """R2: each group whose pairs are all "same", and that nobody marked Needs change or Question, becomes recommended rules
    without an agent: AWS Transform's text, citing both rules and both tools' source citations."""
    rules, marks = inputs["rules"], inputs["context"]["marks"]
    found = []
    for claude, pairs in groups(inputs["pairs"]).items():
        keys = [claude] + [p["aws"] for p in pairs]
        if any(p["relation"] != "same" for p in pairs) or _marked(keys, marks):
            continue
        for p in pairs:
            aws = rules[p["aws"]]
            found.append({"key": f"agreed:{p['aws']}", "decision": "agreed", "text": aws["text"], "name": aws["name"], "covers": [p["aws"], claude],
                          "program": aws["program"], "function": aws["function"], "evidence": aws["cites"] + rules[claude]["cites"],
                          "reason": "Both tools describe this rule the same way (the comparison's pairing: " + str(p.get("reason", "")).strip() + ")",
                          "confidence": p.get("confidence", "high"), "round": 0})
    return found
