"""Pipeline 3, stages R2 and R3: identical pairs agreed, and the units of decision batched with an estimate
(docs/pipeline-3.md, section 4).

The comparison's pairs are many-to-one: many AWS Transform rules pair with one broader Claude rule (spike P3-01, finding 2).
So a **group** is one Claude rule with every AWS rule paired with it. A group whose pairs are all "same" is agreed without an
agent (R2); any other group, and every rule in no pair, is a **unit** for stage R4.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import defaultdict
from typing import Any

BATCH_RULES = 12       # input rules in a batch
SMALL_PROGRAM = 6      # a program with fewer input rules is packed with others
PROGRAMS_PER_BATCH = 3
PARALLEL = 4           # batches run at once
# Measured in spike P3-01: a batch took 56 to 171 seconds and $0.51 to $1.15 at API prices.
MINUTES_PER_BATCH = (1, 3)
USD_PER_BATCH = (0.5, 1.15)
CHANGE_MARKS = ("change", "question")
RECONCILED = "rec/"   # the keys of recommended rules on the reconciliation page: rec/<unit>/<n>
# The decision step's method: part of every unit's hash, so a change to its prompt or schema decides every unit again
# (docs/pipeline-3.md, section 8.2).
METHOD = "part-2"


def one_tool(folder, prompt: str, swaps: tuple[tuple[str, str], ...]) -> str:
    """A prompt in the words of a Claude-only run (docs/release-1.md, section 2); a run with both tools gets it unchanged."""
    if folder.state.get("tools") != "claude":
        return prompt
    for old, new in swaps:
        prompt = prompt.replace(old, new)
    return prompt


def reconciled_key(unit: str, n: int) -> str:
    return f"{RECONCILED}{unit}/{n}"


def named_rules(answer: dict[str, Any]) -> list[str]:
    """The rule keys an answered question names in its "rules" column (the SME list writes them), split on spaces,
    commas or semicolons."""
    value = answer.get("rules") or ""
    items = value if isinstance(value, list) else re.split(r"[\s,;]+", str(value))
    return [str(k).strip() for k in items if str(k).strip()]


def answers_for(members: list[str], answers: list[dict[str, Any]], known: set[str]) -> list[dict[str, Any]]:
    """The answered questions a unit is given: those naming one of its rules, and those naming no rule Reframe knows,
    which every unit is given (docs/pipeline-3.md, stage R4, Running again)."""
    mine = set(members)
    return [a for a in answers if not (set(named_rules(a)) & known) or set(named_rules(a)) & mine]


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


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:16]


def units(inputs: dict[str, Any]) -> list[dict[str, Any]]:
    """R3: every group not agreed, and every rule in no pair. Each unit carries a hash of what it is given: its rules,
    their marks, the documents and the answered questions that bear on it. A later run keeps the decisions of units
    whose hash did not change, so one more answer redoes only the units whose rules it names."""
    rules, marks, ctx = inputs["rules"], inputs["context"]["marks"], inputs["context"]
    background = _hash({"documents": ctx["documents"], "method": METHOD})
    known = set(rules)
    found = []

    def unit(key: str, kind: str, members: list[str], pairs: list[dict[str, Any]]) -> dict[str, Any]:
        content = {"kind": kind, "rules": [rules[k] for k in members],
                   "pairs": [{"aws": p["aws"], "claude": p["claude"], "relation": p["relation"], "reason": p.get("reason", "")} for p in pairs],
                   "marks": {k: {f: v for f, v in marks[k].items() if f != "by"} for k in members if k in marks and marks[k]["status"] in CHANGE_MARKS},
                   "answers": answers_for(members, ctx.get("answers") or [], known)}
        program = rules[members[0]]["program"] or next((rules[k]["program"] for k in members if rules[k]["program"]), "")
        # What reopens a unit a reviewer agreed with: its rules, pairs, marks and the answers that name its rules; not a
        # document or an answer naming no rule, and not a change of method (section 8.11).
        core = {**content, "answers": [a for a in content["answers"] if set(named_rules(a)) & set(members)]}
        return {"key": key, "program": program, **content, "hash": _hash([content, background]), "core": _hash(core)}

    agreed_claude = {r["covers"][1] for r in agreed(inputs)}
    for claude, pairs in sorted(groups(inputs["pairs"]).items()):
        if claude not in agreed_claude:
            found.append(unit(f"group:{claude}", "group", [claude] + [p["aws"] for p in pairs], pairs))
    paired = {p["aws"] for p in inputs["pairs"]} | {p["claude"] for p in inputs["pairs"]}
    for key, rule in sorted(rules.items()):
        if key not in paired:
            found.append(unit(f"{rule['tool']}:{key}", f"{rule['tool']}_only", [key], []))
    return found


def lock(found: list[dict[str, Any]], saved: dict[str, Any], agreed: dict[str, Any]) -> list[str]:
    """Agree keeps a rule (section 8.11). A unit whose recommended rules were all marked Agree is locked: it keeps its
    decision while its core inputs are unchanged. A unit with some rules agreed carries them as "agreed_rules", for the
    step to keep their wording unless the code contradicts it. Returns the keys of the units locked."""
    locked = []
    for u in found:
        prev = saved.get(u["key"]) or {}
        made = prev.get("rules") or []
        yes = [n for n in range(1, len(made) + 1) if reconciled_key(u["key"], n) in agreed]
        if made and len(yes) == len(made) and prev.get("core") == u["core"]:
            u["locked"] = True
            locked.append(u["key"])
        elif yes:
            u["agreed_rules"] = [{"text": made[n - 1].get("text", ""), "covers": made[n - 1].get("covers") or []} for n in yes]
    return locked


def batches(found: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Units batched by program, so a batch reads one program's code once (spike P3-01, finding 6): up to BATCH_RULES input
    rules a batch; programs with fewer than SMALL_PROGRAM rules packed together, up to PROGRAMS_PER_BATCH a batch. A group
    larger than a batch is a batch of its own."""
    by_program: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for u in found:
        by_program[u["program"]].append(u)
    size = lambda us: sum(len(u["rules"]) for u in us)  # noqa: E731
    made: list[list[dict[str, Any]]] = []
    small: list[list[dict[str, Any]]] = []
    for program in sorted(by_program):
        members = by_program[program]
        if size(members) < SMALL_PROGRAM:
            small.append(members)
            continue
        current: list[dict[str, Any]] = []
        for u in sorted(members, key=lambda u: -len(u["rules"])):
            if current and size(current) + len(u["rules"]) > BATCH_RULES:
                made.append(current)
                current = []
            current.append(u)
        if current:
            made.append(current)
    packs: list[list[list[dict[str, Any]]]] = []
    for members in sorted(small, key=lambda us: -size(us)):
        for pack in packs:
            if len(pack) < PROGRAMS_PER_BATCH and sum(size(m) for m in pack) + size(members) <= BATCH_RULES:
                pack.append(members)
                break
        else:
            packs.append([members])
    made += [[u for members in pack for u in members] for pack in packs]
    return [{"number": n, "programs": sorted({u["program"] for u in us}), "units": [u["key"] for u in us], "rules": size(us)}
            for n, us in enumerate(made, 1)]


def estimate(found: list[dict[str, Any]], batched: list[dict[str, Any]], agreed_rules: list[dict[str, Any]]) -> dict[str, Any]:
    kinds: dict[str, int] = defaultdict(int)
    for u in found:
        kinds[u["kind"]] += 1
    rounds = math.ceil(len(batched) / PARALLEL)
    return {"agreed": len(agreed_rules), "units": dict(kinds), "input_rules": sum(len(u["rules"]) for u in found), "batches": len(batched),
            "parallel": PARALLEL, "minutes_low": rounds * MINUTES_PER_BATCH[0], "minutes_high": rounds * MINUTES_PER_BATCH[1],
            "usd_low": round(len(batched) * USD_PER_BATCH[0]), "usd_high": round(len(batched) * USD_PER_BATCH[1])}
