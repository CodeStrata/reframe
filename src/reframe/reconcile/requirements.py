"""Pipeline 3, stage R6: recommended requirements (docs/pipeline-3.md, section 4).

The recommended rules (agreed by both tools, or decided against the source in stage R4) are placed in AWS Transform's
frame of domains and business functions: a rule goes to the function of the AWS rules it covers, a rule only Claude
found to the function whose programs hold its program, and the rest under Unassigned programs. A headless step per
function (larger ones in parts) writes capabilities and requirements from that function's rules only. Reframe checks
that every requirement cites at least one of the rules it was given; one that cites none is dropped and counted. Units
still waiting for an SME are carried as open questions on a capability. Everything is marked as recommended by Reframe.

Written to outputs/reconcile/rules.json and outputs/reconcile/requirements.json.
"""

from __future__ import annotations

import hashlib
import json
import threading
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from reframe.core.runfolder import RunFolder, iso
from reframe.reconcile.units import PARALLEL, reconciled_key

LABEL = "recommended by Reframe from both assessments"
PART_RULES = 60
PATTERNS = ["ubiquitous", "event-driven", "state-driven", "unwanted behaviour", "optional feature", "complex"]
UNASSIGNED = {"key": "unassigned-programs", "name": "Unassigned programs", "kind": "unassigned",
              "description": "Programs in no business function of AWS Transform's frame."}

SCHEMA = {"type": "object", "required": ["capabilities"], "properties": {"capabilities": {"type": "array", "items": {
    "type": "object", "required": ["title", "story", "requirements", "questions"],
    "properties": {
        "title": {"type": "string"}, "story": {"type": "string"},
        "requirements": {"type": "array", "items": {"type": "object", "required": ["kind", "pattern", "text", "rules"], "properties": {
            "kind": {"type": "string", "enum": ["functional", "non-functional"]}, "pattern": {"type": "string", "enum": PATTERNS},
            "text": {"type": "string"}, "rules": {"type": "array", "items": {"type": "string"}}}}},
        "questions": {"type": "array", "items": {"type": "string"}}}}}}}

PROMPT = """Read {input}. It holds one business function of a legacy system, as AWS Transform named it, with its recommended business rules: rules Reframe reconciled from two assessments of the same source and checked against the code. Each rule has an id (R1, R2, ...). It may also hold open items (U1, U2, ...): parts of the function the code could not settle, each with the question a subject-matter expert must answer.

Write this function's capabilities and requirements:
- each capability is a user story ("As a ..., I want ..., so that ...") with a short title;
- each capability has requirements, each one sentence in EARS form ("The system shall ...", "When ..., the system shall ...", "While ..., the system shall ...", "If ..., then the system shall ...", "Where ..., the system shall ..."), with its kind (functional or non-functional) and EARS pattern;
- every requirement lists in "rules" the ids of the rules it comes from;
- put each open item's id in "questions" of the capability it holds up.

Use only what is in the file: do not invent behaviour, values, systems or rules. Every requirement must come from at least one rule. Cover every rule at least once, and place every open item once. Keep the rules' wording of values and conditions, in plain business language. Answer only with the JSON."""


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:16]


# ---- the recommended rules --------------------------------------------------------------------------------------------

def recommended_rules(gathered: dict[str, Any], found: list[dict[str, Any]], kept: dict[str, Any], agreed: list[dict[str, Any]],
                      described: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Every recommended rule, with its decision, where it came from (rec/<unit>/<n>) and the confidence Reframe sets
    (section 8.5): from its unit's decision, or for a rule both tools agree on, from its description (stage R2b)."""
    from reframe.reconcile.confidence import facts
    rules = gathered["rules"]
    described = described or {}

    def name(covers: list[str]) -> str:
        named = [rules[k] for k in covers if k in rules]
        aws = [r for r in named if r["tool"] == "aws"]
        return ((aws or named or [{}])[0]).get("name", "")

    made = []
    for r in agreed:
        rule = {"key": reconciled_key(r["key"], 1), "unit": r["key"], "n": 1, "text": r["text"], "name": r.get("name") or name(r["covers"]),
                "covers": r["covers"], "program": r["program"], "decision": "agreed", "reason": r["reason"], "model_confidence": r.get("confidence", ""),
                "evidence": r["evidence"], "context": [], "round": 0, "changed": False, "defect": "", "unit_rules": 1}
        about = described.get(r["key"]) or {}
        made.append({**rule, **facts(rule, about), "kind": about.get("kind") or "", "examples": about.get("examples") or [],
                     "examples_removed": about.get("examples_removed", 0)})
    for u in found:
        d = kept.get(u["key"]) or {}
        for n, rule in enumerate(d.get("rules") or [], 1):
            made_rule = {"key": reconciled_key(u["key"], n), "unit": u["key"], "n": n, "text": rule.get("text", ""), "name": name(rule.get("covers") or []),
                         "covers": list(rule.get("covers") or []), "program": u["program"], "decision": d.get("decision"), "reason": d.get("reason", ""),
                         "evidence": d.get("evidence") or [], "context": d.get("context") or [],
                         "round": d.get("round"), "changed": bool(d.get("changed")), "defect": d.get("defect", ""), "unit_rules": len(d.get("rules") or []),
                         "conflict": any(p.get("relation") == "conflicting" for p in u.get("pairs") or []), "kind": rule.get("kind") or "",
                         "examples": rule.get("examples") or [], "examples_removed": d.get("examples_removed", 0) if n == 1 else 0}
            made.append({**made_rule, **facts(made_rule, d)})
    return made


def open_units(found: list[dict[str, Any]], kept: dict[str, Any]) -> list[dict[str, Any]]:
    return [{"unit": u["key"], "program": u["program"], "question": (kept.get(u["key"]) or {}).get("question", ""), "rules": [r["key"] for r in u["rules"]]}
            for u in found if (kept.get(u["key"]) or {}).get("decision") == "needs_sme"]


# ---- the frame --------------------------------------------------------------------------------------------------------

def frame(folder: RunFolder) -> dict[str, Any]:
    """AWS Transform's domains and functions, and which functions each program sits in."""
    from reframe.report.build import collect
    from reframe.report.compare import _programs_aws
    aws = collect(folder)
    by_program: dict[str, list[str]] = defaultdict(list)
    for fid, programs in sorted(_programs_aws(aws).items()):
        for p in programs:
            by_program[p].append(fid)
    return {"domains": aws["domains"], "functions": {f["id"]: f for f in aws["functions"]}, "by_program": dict(by_program)}


def place(covers: list[str], unit_rules: list[str], program: str, rules: dict[str, Any], framed: dict[str, Any]) -> str:
    """The AWS function a recommended rule (or open unit) belongs in: that of the AWS rules it covers, else that of the
    AWS rules in its unit, else the function whose programs hold its program; "" for Unassigned programs."""
    for keys in (covers, unit_rules):
        functions = Counter(rules[k]["function"] for k in keys if k in rules and rules[k]["tool"] == "aws" and rules[k].get("function") in framed["functions"])
        if functions:
            return functions.most_common(1)[0][0]
    return (framed["by_program"].get(str(program).upper()) or [""])[0]


# ---- one function -----------------------------------------------------------------------------------------------------

def check(raw: dict[str, Any], ids: dict[str, str], open_ids: dict[str, str]) -> tuple[list[dict[str, Any]], int, set[str]]:
    """Requirements kept with the rule keys they cite; one citing no given rule dropped and counted. Returns the
    capabilities, the number dropped and the open units placed."""
    dropped, placed, caps = 0, set(), []
    for cap in raw.get("capabilities") or []:
        requirements = []
        for req in cap.get("requirements") or []:
            cited = [ids[r] for r in req.get("rules") or [] if r in ids]
            if not cited or req.get("kind") not in ("functional", "non-functional"):
                dropped += 1
                continue
            requirements.append({"kind": req["kind"], "pattern": req.get("pattern", ""), "text": req.get("text", ""), "rules": list(dict.fromkeys(cited))})
        questions = [open_ids[q] for q in cap.get("questions") or [] if q in open_ids and open_ids[q] not in placed]
        placed.update(questions)
        if requirements or questions:
            caps.append({"title": cap.get("title", ""), "story": cap.get("story", ""), "requirements": requirements, "questions": questions})
    return caps, dropped, placed


def write_function(folder: RunFolder, claude, places: dict[str, Any], fid: str, function: dict[str, Any], members: list[dict[str, Any]],
                   waiting: list[dict[str, Any]], log: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, Any]:
    project = folder.state["project"]
    folder_in = places["analysis"] / "reframe" / "reconcile"
    folder_in.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() else "-" for c in fid).strip("-")[:60] or "unassigned"
    parts = [members[i:i + PART_RULES] for i in range(0, len(members), PART_RULES)] or [[]]
    caps: list[dict[str, Any]] = []
    dropped, placed = 0, set()
    for n, part in enumerate(parts, 1):
        if not part:
            break
        ids = {f"R{i}": r["key"] for i, r in enumerate(part, 1)}
        here = waiting if n == len(parts) else []
        open_ids = {f"U{i}": w["unit"] for i, w in enumerate(here, 1)}
        data = {"function": {"name": function["name"], "description": function.get("description", "")},
                "rules": [{"id": i, "program": r["program"], "name": r["name"], "kind": r.get("kind", ""), "text": r["text"]} for i, r in zip(ids, part)],
                "open_items": [{"id": i, "program": w["program"], "question": w["question"]} for i, w in zip(open_ids, here)]}
        path = folder_in / f"req-{safe}-{n}.json"
        path.write_text(json.dumps(data, indent=1))
        name = f"req-{safe}-{n}"
        step = claude.run(name, PROMPT.format(input=f"analysis/{project}/{path.relative_to(places['analysis']).as_posix()}"), timeout=3600, schema=SCHEMA)
        log.append({"step": name, **{k: v for k, v in step.as_json().items() if k in ("ok", "seconds", "tokens", "cost_usd", "problem")}})
        if not step.ok:
            return None, step
        got, lost, put = check(claude.structured(step) or {}, ids, open_ids)
        caps += got
        dropped += lost
        placed |= put
    missing = [w["unit"] for w in waiting if w["unit"] not in placed]
    if missing:  # an open unit the step did not place is still carried, on a capability of its own
        caps.append({"title": "Waiting for a subject-matter expert", "story": "", "requirements": [], "questions": missing})
    return {"capabilities": caps, "dropped": dropped}, None


# ---- R6 ----------------------------------------------------------------------------------------------------------------

def build(folder: RunFolder, claude, gathered: dict[str, Any], found: list[dict[str, Any]], kept: dict[str, Any], agreed: list[dict[str, Any]],
          sme: dict[str, Any], described: dict[str, Any] | None = None) -> dict[str, Any]:
    """The recommended requirements. A function whose rules and open units are unchanged keeps what it had."""
    from reframe.claude.steps import stop_for
    from reframe.claude.workspace import paths
    places = paths(folder)
    rules = gathered["rules"]
    made = recommended_rules(gathered, found, kept, agreed, described if described is not None else folder.load("reconcile/described.json", {}) or {})
    waiting = open_units(found, kept)
    framed = frame(folder)
    by_function: dict[str, list[dict[str, Any]]] = defaultdict(list)
    open_by_function: dict[str, list[dict[str, Any]]] = defaultdict(list)
    unit_rules = {u["key"]: [r["key"] for r in u["rules"]] for u in found} | {r["key"]: r["covers"] for r in agreed}
    for r in made:
        r["function"] = place(r["covers"], unit_rules.get(r["unit"], []), r["program"], rules, framed)
        by_function[r["function"]].append(r)
    for w in waiting:
        w["function"] = place(w["rules"], [], w["program"], rules, framed)
        open_by_function[w["function"]].append(w)
    folder.save("outputs/reconcile/rules.json", {"label": LABEL, "generated_at": iso(), "rules": made, "open": waiting})

    saved = (folder.load("outputs/reconcile/requirements.json") or {}).get("functions") or {}
    log = folder.load("reconcile/requirements-steps.json", []) or []
    lock, stopped, written = threading.Lock(), [], {}
    todo = []
    for fid in sorted(set(by_function) | set(open_by_function)):
        members = sorted(by_function.get(fid, []), key=lambda r: (r["program"], r["key"]))
        here = sorted(open_by_function.get(fid, []), key=lambda w: w["unit"])
        function = framed["functions"].get(fid) or {"name": UNASSIGNED["name"], "description": UNASSIGNED["description"]}
        digest = _hash([function["name"], [{k: r[k] for k in ("key", "text", "program")} for r in members], [{k: w[k] for k in ("unit", "question")} for w in here]])
        if (saved.get(fid) or {}).get("hash") == digest and "raw" in saved[fid]:
            written[fid] = {k: saved[fid][k] for k in ("hash", "dropped", "raw")}
        else:
            todo.append((fid, function, members, here, digest))

    def one(item) -> None:
        fid, function, members, here, digest = item
        if stopped:
            return
        if not members:  # only open units: no step, a capability that carries them
            value: dict[str, Any] | None = {"capabilities": [{"title": "Waiting for a subject-matter expert", "story": "", "requirements": [],
                                                              "questions": [w["unit"] for w in here]}], "dropped": 0}
            stop = None
        else:
            value, stop = write_function(folder, claude, places, fid, function, members, here, log)
        with lock:
            folder.save("reconcile/requirements-steps.json", log)
            if stop is not None:
                stopped.append(stop)
                return
            written[fid] = {"hash": digest, "dropped": value["dropped"], "raw": value["capabilities"]}
            folder.save("outputs/reconcile/requirements.json", {"label": LABEL, "complete": False, "functions": {**saved, **written}})

    with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
        list(pool.map(one, todo))
    if stopped:
        raise stop_for(stopped[0], "the reconciliation's recommended requirements")

    sme_of = {k: q for q in sme.get("questions") or [] for k in q["originals"]}
    open_of = {w["unit"]: w for w in waiting}
    functions = {}
    for fid in sorted(written, key=lambda f: (f == "", f)):
        counters = Counter()
        caps = []
        for c_index, cap in enumerate(written[fid]["raw"], 1):
            reqs = []
            for req in cap["requirements"]:
                counters[req["kind"]] += 1
                reqs.append({**req, "code": f"REQ-{'F' if req['kind'] == 'functional' else 'N'}-{counters[req['kind']]:03d}"})
            qs = []
            for unit in cap["questions"]:
                listed = sme_of.get(f"r4:{unit}") or {}
                counters["question"] += 1
                qs.append({"code": listed.get("id") or f"OQ-{counters['question']:03d}", "unit": unit, "rules": open_of.get(unit, {}).get("rules", []),
                           "text": listed.get("question") or open_of.get(unit, {}).get("question", ""), "status": listed.get("status", "open")})
            caps.append({"number": c_index, "title": cap["title"], "story": cap["story"], "requirements": reqs, "questions": qs})
        functions[fid] = {**written[fid], "capabilities": caps}
    cited = {k for f in functions.values() for c in f["capabilities"] for q in c["requirements"] for k in q["rules"]}
    value = {"label": LABEL, "complete": True, "generated_at": iso(), "functions": functions,
             "domains": [{"key": d["key"], "name": d["name"], "description": d.get("description", ""), "kind": d["kind"],
                          "functions": [f for f in d["functions"] if f in functions]} for d in framed["domains"]]
                        + ([{**UNASSIGNED, "functions": [""]}] if "" in functions else []),
             "names": {fid: {"name": (framed["functions"].get(fid) or UNASSIGNED)["name"], "description": (framed["functions"].get(fid) or UNASSIGNED).get("description", "")}
                       for fid in functions},
             "dropped": sum(f["dropped"] for f in functions.values()), "rules_cited": len(cited), "rules_total": len(made),
             "requirements": sum(len(c["requirements"]) for f in functions.values() for c in f["capabilities"])}
    value["domains"] = [d for d in value["domains"] if d["functions"]]
    folder.save("outputs/reconcile/requirements.json", value)
    return value
