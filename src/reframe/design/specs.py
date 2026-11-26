"""Pipeline 4, stage D6: the final specifications, one per capability (docs/pipeline-4.md, section 4, P4-07).

Reframe assembles each specification from what the earlier stages decided, with no model:

- the final requirements: the reconciled requirements, as the last reconciliation round left them (marks applied, *Agree*
  kept word for word);
- the business rules, with their kind, confidence, worked examples and evidence, each classed as a business rule,
  formatting, error handling, a side effect, a historical artifact or a design note (from its kind);
- acceptance criteria, Given/When/Then, from the rules' worked examples, each citing its rule and the requirements it checks;
- the screen specifications: the modern screens (stage D4) whose components serve the capability, and their journeys;
- the data contracts: the copybooks the capability's programs use, as typed records (contracts.py);
- the decision tables from the reconciliation, each row citing its rule, with the combinations no rule covers as gaps;
- the open questions: the SME list's open entries on the capability's rules.

One headless Claude step per function (in batches of capabilities) writes only what needs words: a summary, acceptance
criteria for each requirement no worked example covers, and a design note for each technical rule. Reframe checks every
answer (every capability answered, every such requirement given a criterion that cites its rules, every technical rule a
note); a failed answer is asked once more with the reasons. A batch whose input is unchanged keeps its answer.

A capability in a signed-off function is final; every other is draft. Reframe then checks every specification: every
requirement, rule, screen and copybook cited exists, and every requirement of the capability is in it with a criterion.

    python -m reframe.design.specs [--run <run>] [--stack "<front end>; <back end>; <data>"]

writes design/specs.json, design/contracts.json, design/specs/<capability>.json and the design page,
outputs/design/index.html.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from reframe.design import contracts as data_contracts

FILE = "design/specs.json"
CONTRACTS = "design/contracts.json"
STACK = "design/stack.json"
SPECS = "design/specs"
METHOD = "specs-1"
PARALLEL = 4
BATCH = 12  # capabilities per step

# Each rule's class, from its kind (P3-21): the forward build keeps business rules exactly, may restyle formatting, and
# asks before carrying a historical artifact; technical steps become design notes.
CLASS = {"business": "business rule", "validation": "business rule", "compliance": "business rule", "display": "formatting",
         "error_handling": "error handling", "side_effect": "side effect", "leftover": "historical artifact", "technical": "design note"}
CLASS_ORDER = ("business rule", "side effect", "error handling", "formatting", "historical artifact", "design note")

SCHEMA = {"type": "object", "required": ["capabilities"], "properties": {
    "capabilities": {"type": "array", "items": {"type": "object", "required": ["key", "summary", "acceptance", "design_notes"], "properties": {
        "key": {"type": "string"}, "summary": {"type": "string"},
        "acceptance": {"type": "array", "items": {"type": "object", "required": ["requirement", "rules", "given", "when", "then"], "properties": {
            "requirement": {"type": "string"}, "rules": {"type": "array", "items": {"type": "string"}},
            "given": {"type": "string"}, "when": {"type": "string"}, "then": {"type": "string"}}}},
        "design_notes": {"type": "array", "items": {"type": "object", "required": ["rule", "note"], "properties": {
            "rule": {"type": "string"}, "note": {"type": "string"}}}}}}}}}

PROMPT = """Read {input}. It holds capabilities of one business function of a legacy mainframe application being modernized: each with its requirements (EARS), the business rules behind them (with their kind) and the modern screens that serve it. The legacy source is under {legacy}/ if you need it; do not change anything.

For each capability listed, write the parts of its final specification that need words:

- "summary": two or three sentences for the team building the new application: what the capability does, for whom, and what it must never get wrong. Plain words; name programs or files only where the business does.
- "acceptance": a Given/When/Then acceptance criterion for each requirement listed under "needs_criteria" (at least one each), each naming the "requirement" (its code) and the "rules" (keys) it checks, taken from that requirement's own rules. Make them testable, with the concrete values the rule text gives (messages word for word, limits, codes); do not invent behaviour the rules do not state. The other requirements already have criteria from the rules' worked examples.
- "design_notes": one note for each rule listed under "technical_rules", naming the "rule" key: what the new application needs from that technical step (a keyed lookup, a sorted extract, a scheduled job, a message to another system), without the mainframe mechanics (VSAM, CICS, JCL, COMMAREA) unless there is no other way to say it.

If the file lists "decisions", the owner made them: follow each one that applies to these capabilities.

Use only the keys listed. Answer only with the JSON."""

RETRY = """Your answer failed Reframe's checks. Answer again with the whole JSON, fixing these:

{problems}"""


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:16]


def page_of(fid: str) -> str:
    return "rec/" + (fid or "unassigned")


def slug(text: str) -> str:
    return re.sub(r"-+", "-", "".join(c if c.isalnum() else "-" for c in text)).strip("-")[:80] or "x"


# ---- assembled with no model -------------------------------------------------------------------------------------------

def class_of(kind: str) -> str:
    return CLASS.get(kind or "", "business rule")


def requirement_class(rules: list[dict[str, Any]]) -> str:
    """A requirement's class: the first of its rules' classes in CLASS_ORDER."""
    found = {class_of(r.get("kind", "")) for r in rules}
    return next((c for c in CLASS_ORDER if c in found), "business rule")


TRIGGER = re.compile(r"^\s*(?:WHEN|IF|WHILE|WHERE)\s+(.+?),\s*(?:THEN\s+)?THE\s", re.I | re.S)
SUBJECT = re.compile(r"^\s*THE\s+(.+?)\s+SHALL\b", re.I | re.S)


def when_of(rule: dict[str, Any]) -> str:
    """The trigger of a rule in EARS form ("WHEN x, THE y SHALL z" gives "x"), or "<y> runs"."""
    text = rule.get("text", "")
    m = TRIGGER.match(text)
    if m:
        return re.sub(r"\s+", " ", m.group(1)).strip()
    m = SUBJECT.match(text)
    subject = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    return f"{subject} runs" if m else f"{rule.get('name') or 'the rule'} applies"


def given_of(example: dict[str, Any]) -> str:
    given = [f"{g.get('field', '')}: {g.get('value', '')}" for g in example.get("given") or []]
    return "; ".join(given) if given else "no particular input"


def example_criteria(reqs: list[dict[str, Any]], rules: dict[str, Any]) -> list[dict[str, Any]]:
    """A criterion for each worked example of the capability's rules, citing its rule and every requirement of the
    capability that rule is behind."""
    behind: dict[str, list[str]] = defaultdict(list)
    for q in reqs:
        for k in q["rules"]:
            behind[k].append(q["code"])
    found = []
    for k, codes in behind.items():
        r = rules.get(k) or {}
        for i, x in enumerate(r.get("examples") or [], 1):
            found.append({"requirements": codes, "rules": [k], "given": given_of(x), "when": when_of(r), "then": str(x.get("then", "")),
                          "from": f"worked example {i} of the rule"})
    return found


def runs_as(rules: list[dict[str, Any]], online: set[str]) -> str:
    """How the capability runs in the new application: online (behind screens), as a scheduled job (from JCL), or both;
    a service when the source shows neither."""
    entries = [e.lower() for r in rules for e in r.get("entry") or []]
    on = any("/csd/" in e or e.endswith(".csd") for e in entries) or any(str(r.get("program", "")).upper() in online for r in rules)
    job = any(re.search(r"/(jcl|proc|scheduler)/|\.jcl\b|\.prc\b", e) for e in entries)
    return "online and scheduled job" if on and job else "online" if on else "scheduled job" if job else "service"


def screens_for(key: str, codes: set[str], rule_keys: set[str], modern: dict[str, Any], journeys: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    """The modern screens that serve a capability: those with a component citing one of its requirements or rules, or in
    a journey that lists it; each with only the components that serve it. And the journeys."""
    mine = [j["id"] for j in journeys if key in (j.get("capabilities") or [])]
    mapping: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for d in (modern.get("domains") or {}).values():
        for m in d.get("mapping") or []:
            mapping[m.get("legacy_screen", "")][m.get("how", "")] += 1
    found = []
    for s in modern.get("screens") or []:
        parts = [c for c in s.get("components") or [] if set(c.get("requirements") or []) & codes or set(c.get("rules") or []) & rule_keys]
        if not parts and not set(s.get("journeys") or []) & set(mine):
            continue
        if not parts and not s.get("replaces"):
            continue  # the shared header and navigation, in every journey
        how: dict[str, int] = defaultdict(int)
        for m in s.get("replaces") or []:
            for h, n in mapping.get(m, {}).items():
                how[h] += n
        found.append({"id": s["id"], "title": s.get("title", ""), "purpose": s.get("purpose", ""), "replaces": s.get("replaces") or [],
                      "journeys": [j for j in s.get("journeys") or [] if j in mine], "prototype": f"prototype/index.html#/{s['id']}",
                      "mapping": dict(how),
                      "components": [{k: c[k] for k in ("id", "type", "label", "section", "shows", "validation", "goes_to", "keyboard", "rules", "requirements") if c.get(k)}
                                     for c in parts]})
    return found, mine


def questions_for(rule_keys: list[str], rules: dict[str, Any], sme: list[dict[str, Any]], own: list[Any]) -> list[dict[str, Any]]:
    """The SME list's open questions on the capability's rules (matched through the input rules each recommended rule
    covers), and the capability's own questions from the requirements."""
    covers = {c: k for k in rule_keys for c in (rules.get(k) or {}).get("covers") or []}
    found = []
    for q in sme:
        if q.get("status") != "open":
            continue
        on = sorted({covers[c] for c in q.get("rules") or [] if c in covers})
        if on:
            found.append({"id": q["id"], "question": q["question"], "owner": q.get("owner", ""), "rules": on})
    for q in own or []:
        found.append({"id": "", "question": q if isinstance(q, str) else q.get("question", str(q)), "owner": "", "rules": []})
    return found


def assemble(folder, legacy: Path | None, signoffs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Every capability's specification without the model's parts, and what the model step is to write for each."""
    requirements = folder.load("outputs/reconcile/requirements.json") or {}
    rules = {r["key"]: r for r in (folder.load("outputs/reconcile/rules.json") or {}).get("rules") or []}
    modern = folder.load("design/modern.json") or {}
    journeys = (folder.load("design/journeys.json") or {}).get("journeys") or []
    inventory = folder.load("design/screens.json") or {}
    flow = folder.load("design/flow.json") or {}
    sme = (folder.load("reconcile/questions.json") or {}).get("questions") or []
    signed: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for x in list((folder.state.get("reconcile") or {}).get("signoffs") or []) + list(signoffs or []):
        signed[x["function"]].append({"reviewer": x.get("reviewer", ""), "at": x.get("at", ""), "comment": x.get("comment", "")})
    online = {p["name"].upper() for s in inventory.get("screens") or [] for p in s.get("programs") or []} | \
             {str(t.get("program", "")).upper() for t in flow.get("transactions") or []}
    uses = data_contracts.uses(legacy) if legacy and legacy.is_dir() else {}
    domain_of = {f: d for d in requirements.get("domains") or [] for f in d.get("functions") or []}
    names = requirements.get("names") or {}
    found = []
    for fid, body in (requirements.get("functions") or {}).items():
        page = page_of(fid)
        domain = domain_of.get(fid) or {}
        for cap in body.get("capabilities") or []:
            key = f"{page}#{cap['number']}"
            reqs = cap.get("requirements") or []
            rule_keys = list(dict.fromkeys(k for q in reqs for k in q.get("rules") or []))
            mine = [rules[k] for k in rule_keys if k in rules]
            codes = {f"{page}/{q['code']}" for q in reqs}
            screens, journey_ids = screens_for(key, codes, set(rule_keys), modern, journeys)
            programs = sorted({str(r.get("program", "")).upper() for r in mine if r.get("program")})
            books: dict[str, dict[str, Any]] = {}
            for p in programs:
                for b, role in (uses.get(p) or {}).items():
                    entry = books.setdefault(b, {"copybook": b, "role": role, "programs": []})
                    entry["programs"].append(p)
                    if role == "file record":
                        entry["role"] = role
            criteria = example_criteria(reqs, rules)
            covered = {c for x in criteria for c in x["requirements"]}
            found.append({
                "key": key, "function": fid, "function_name": (names.get(fid) or {}).get("name", fid), "domain": domain.get("name", "No domain"),
                "domain_key": domain.get("key", ""), "number": cap["number"], "title": cap.get("title", ""), "story": cap.get("story", ""),
                "risk": cap.get("risk", ""), "touches": cap.get("touches") or [],
                "status": "final" if signed.get(page) else "draft", "signed_off": signed.get(page) or [],
                "runs_as": runs_as(mine, online),
                "requirements": [{"key": f"{page}/{q['code']}", "code": q["code"], "kind": q.get("kind", ""), "pattern": q.get("pattern", ""), "text": q["text"],
                                  "rules": q.get("rules") or [], "class": requirement_class([rules[k] for k in q.get("rules") or [] if k in rules])} for q in reqs],
                "rules": [{"key": r["key"], "name": r.get("name", ""), "kind": r.get("kind", ""), "class": class_of(r.get("kind", "")),
                           "confidence": r.get("confidence", ""), "decision": r.get("decision", ""), "program": r.get("program", ""), "text": r["text"],
                           "examples": r.get("examples") or [], "evidence": r.get("evidence") or []} for r in mine],
                "acceptance": criteria,
                "needs_criteria": [q["code"] for q in reqs if q["code"] not in covered],
                "technical_rules": [r["key"] for r in mine if r.get("kind") == "technical"],
                "screens": screens, "journeys": journey_ids,
                "contracts": sorted(books.values(), key=lambda b: (b["role"] != "file record", b["copybook"])),
                "tables": cap.get("tables") or [],
                "questions": questions_for(rule_keys, rules, sme, cap.get("questions") or []),
            })
    return {"specs": found, "rules": rules, "books": sorted({b["copybook"] for s in found for b in s["contracts"]})}


# ---- the model's part --------------------------------------------------------------------------------------------------

def batches(specs: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    """Per function, in batches of capabilities; a function with nothing to write needs a summary still."""
    by_fn: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in specs:
        by_fn[s["function"]].append(s)
    found = []
    for fid, mine in by_fn.items():
        for i in range(0, len(mine), BATCH):
            found.append((f"{fid}#{i // BATCH + 1}" if len(mine) > BATCH else fid, mine[i:i + BATCH]))
    return found


def batch_input(mine: list[dict[str, Any]]) -> dict[str, Any]:
    first = mine[0]
    return {"function": first["function_name"], "domain": first["domain"], "capabilities": [{
        "key": s["key"], "title": s["title"], "story": s["story"], "runs_as": s["runs_as"],
        "requirements": [{"code": q["code"], "text": q["text"], "rules": q["rules"]} for q in s["requirements"]],
        "rules": [{"key": r["key"], "kind": r["kind"], "name": r["name"], "text": r["text"][:400]} for r in s["rules"]],
        "screens": [x["title"] for x in s["screens"]],
        "needs_criteria": s["needs_criteria"], "technical_rules": s["technical_rules"]} for s in mine]}


def batch_parts(data: dict[str, Any]) -> dict[str, str]:
    """What a batch was made from, piece by piece, so a round can say why it was redone."""
    from reframe.design import rounds
    caps = data["capabilities"]
    return rounds.parts({"requirements": [c["requirements"] for c in caps], "rules": [c["rules"] for c in caps], "screens": [c["screens"] for c in caps],
                         "capabilities": [{k: c[k] for k in ("key", "title", "story", "runs_as", "needs_criteria", "technical_rules")} for c in caps],
                         **{k: v for k, v in data.items() if k not in ("capabilities", "function", "domain")}}, METHOD)


def problems(answer: dict[str, Any] | None, data: dict[str, Any]) -> list[str]:
    if not isinstance(answer, dict):
        return ["no answer"]
    found = []
    caps = {c["key"]: c for c in data["capabilities"]}
    given: dict[str, int] = defaultdict(int)
    for a in answer.get("capabilities") or []:
        key = a.get("key", "")
        given[key] += 1
        cap = caps.get(key)
        if not cap:
            found.append(f'capability "{key}" is not listed')
            continue
        if not str(a.get("summary", "")).strip():
            found.append(f"{key}: the summary is empty")
        behind = {q["code"]: set(q["rules"]) for q in cap["requirements"]}
        met = set()
        for i, x in enumerate(a.get("acceptance") or [], 1):
            code = x.get("requirement", "")
            if code not in behind:
                found.append(f'{key}: acceptance criterion {i} names requirement "{code}", which is not one of this capability')
                continue
            wrong = [k for k in x.get("rules") or [] if k not in behind[code]]
            if not x.get("rules") or wrong:
                found.append(f"{key}: acceptance criterion {i} for {code} must cite that requirement's own rules" + (f' (not {", ".join(wrong)})' if wrong else ""))
                continue
            if not all(str(x.get(p, "")).strip() for p in ("given", "when", "then")):
                found.append(f"{key}: acceptance criterion {i} for {code} needs a given, a when and a then")
                continue
            met.add(code)
        for code in cap["needs_criteria"]:
            if code not in met:
                found.append(f"{key}: requirement {code} has no acceptance criterion")
        technical = set(cap["technical_rules"])
        noted = set()
        for n in a.get("design_notes") or []:
            if n.get("rule") not in technical:
                found.append(f'{key}: design note on "{n.get("rule")}", which is not one of this capability\'s technical rules')
            elif str(n.get("note", "")).strip():
                noted.add(n["rule"])
        for k in cap["technical_rules"]:
            if k not in noted:
                found.append(f"{key}: technical rule {k} has no design note")
    for key in caps:
        if given.get(key, 0) == 0:
            found.append(f"capability {key} is not answered")
        elif given[key] > 1:
            found.append(f"capability {key} is answered {given[key]} times")
    return found


# ---- the specification, checked ----------------------------------------------------------------------------------------

def finish(spec: dict[str, Any], written: dict[str, Any] | None) -> dict[str, Any]:
    """A specification with the model's parts added, and its acceptance criteria numbered."""
    written = written or {}
    out = {k: v for k, v in spec.items() if k not in ("needs_criteria", "technical_rules")}
    out["summary"] = written.get("summary", "")
    criteria = list(spec["acceptance"]) + [{"requirements": [x["requirement"]], "rules": x.get("rules") or [], "given": x["given"], "when": x["when"],
                                            "then": x["then"], "from": "written from the rule"} for x in written.get("acceptance") or []
                                           if x.get("requirement") in {q["code"] for q in spec["requirements"]}]
    for i, x in enumerate(criteria, 1):
        x["id"] = f"AC-{i:02d}"
        x["key"] = f"{spec['key']}/AC-{i:02d}"
    out["acceptance"] = criteria
    out["design_notes"] = [{"rule": n["rule"], "note": n["note"]} for n in written.get("design_notes") or [] if n.get("rule") in spec["technical_rules"]]
    by_code = defaultdict(list)
    for x in criteria:
        for code in x["requirements"]:
            by_code[code].append(x["id"])
    for q in out["requirements"]:
        q["criteria"] = by_code.get(q["code"], [])
    out["gaps"] = sum(len(t.get("gaps") or []) for t in spec["tables"])
    return out


def check(spec: dict[str, Any], source: dict[str, Any], rules: dict[str, Any], screens: set[str], books: dict[str, Any]) -> list[str]:
    """Every requirement, rule, screen and copybook a specification cites exists; every requirement of the capability is
    in it, with an acceptance criterion; every technical rule has a design note."""
    key, found = spec["key"], []
    wanted = {q["code"] for q in source.get("requirements") or []}
    have = {q["code"] for q in spec["requirements"]}
    found += [f"{key}: requirement {c} is not in the specification" for c in sorted(wanted - have)]
    for q in spec["requirements"]:
        found += [f"{key}: {q['code']} cites rule {k}, which does not exist" for k in q["rules"] if k not in rules]
        if not q["criteria"]:
            found.append(f"{key}: {q['code']} has no acceptance criterion")
    for x in spec["acceptance"]:
        found += [f"{key}: {x['id']} cites rule {k}, which does not exist" for k in x["rules"] if k not in rules]
    found += [f"{key}: screen {s['id']} does not exist" for s in spec["screens"] if s["id"] not in screens]
    found += [f"{key}: copybook {b['copybook']} is not a contract" for b in spec["contracts"] if b["copybook"] not in books]
    for t in spec["tables"]:
        found += [f"{key}: decision table \"{t.get('title', '')}\" cites rule {r['rule']}, which does not exist" for r in t.get("rows") or []
                  if r.get("rule") and r["rule"] not in rules]
    noted = {n["rule"] for n in spec["design_notes"]}
    found += [f"{key}: technical rule {r['key']} has no design note" for r in spec["rules"] if r["kind"] == "technical" and r["key"] not in noted]
    return found


# ---- run ---------------------------------------------------------------------------------------------------------------

def stack_of(folder, stack: str | None) -> dict[str, Any] | None:
    """The target stack: the one given now (recorded with when), or the one recorded before; never a default."""
    from reframe.core.runfolder import iso
    if stack:
        given = {"stack": stack, **data_contracts.parse_stack(stack), "given_by": "the engineer (--stack)", "at": iso()}
        before = folder.load(STACK) or {}
        if before.get("stack") != stack:
            folder.save(STACK, given)
        return folder.load(STACK)
    return folder.load(STACK) or None


def run(folder, claude, stack: str | None = None, more=None, plan_only: bool = False, signoffs: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """D6. `more(name, data)` gives a batch's extra input for a round (the decisions that name its capabilities);
    `signoffs` adds sign-offs read in the round; `plan_only` says what would be redone, and why, without a step."""
    from reframe.claude.steps import stop_for
    from reframe.design import rounds
    from reframe.claude.workspace import paths
    places = paths(folder)
    project = folder.state["project"]
    if not (folder.load("outputs/reconcile/requirements.json") or {}).get("functions"):
        raise ValueError("run the reconciliation first")
    if not folder.load("design/modern.json"):
        raise ValueError("run the screen inventory, the flow, the journeys and the modern screens first")
    target = stack_of(folder, None if plan_only else stack)
    types = data_contracts.stack_types(target)
    built = assemble(folder, places["legacy"], signoffs)
    books = data_contracts.contracts(places["legacy"], set(built["books"]), types)
    if not plan_only:
        folder.save(CONTRACTS, {"stack": target, "notes": types["notes"], "contracts": books})
    saved = folder.load(FILE, {}) or {}
    kept, log = saved.get("batches") or {}, saved.get("log") or []
    folder_in = places["analysis"] / "reframe" / "design"
    folder_in.mkdir(parents=True, exist_ok=True)
    lock, stopped, todo, why = threading.Lock(), [], [], []
    plan = batches(built["specs"])
    for name, mine in plan:
        data = batch_input(mine)
        data.update(more(name, data) if more else {})
        digest = _hash([data, METHOD])
        before = kept.get(name) or {}
        if before.get("hash") != digest or before.get("problems"):
            todo.append((name, data, digest))
            why.append((name, rounds.changed(before or None, batch_parts(data)) if before.get("hash") != digest else ["problems"]))
    told = rounds.summary(why, [n for n, _ in plan if n not in {x[0] for x in todo}])
    if plan_only:
        return {"round": told}

    def one(item) -> None:
        name, data, digest = item
        if stopped:
            return
        safe = slug(name)[:50] + "-" + hashlib.sha256(name.encode()).hexdigest()[:6]  # unique: batches of one function share a long name
        path = folder_in / f"specs-{safe}.json"
        path.write_text(json.dumps(data, indent=1))
        prompt = PROMPT.format(input=f"analysis/{project}/{path.relative_to(places['analysis']).as_posix()}", legacy=f"legacy/{project}")
        answer, wrong, attempts = None, ["no answer"], 0
        for attempt in (1, 2):
            attempts = attempt
            step = claude.run(f"specs-{safe}{'-retry' if attempt == 2 else ''}",
                              prompt if attempt == 1 else prompt + "\n\n" + RETRY.format(problems="\n".join(f"- {p}" for p in wrong[:80])),
                              timeout=3600, schema=SCHEMA)
            with lock:
                log.append({"batch": name, "attempt": attempt, **{k: v for k, v in step.as_json().items() if k in ("ok", "seconds", "tokens", "cost_usd", "problem")}})
            if not step.ok:
                if step.problem in ("limit", "signin"):
                    with lock:
                        stopped.append(step)
                    return
                wrong = [f"the step did not finish ({step.problem})"]
                continue
            answer = claude.structured(step)
            wrong = problems(answer, data)
            if not wrong:
                break
        with lock:
            kept[name] = {"hash": digest, "parts": batch_parts(data), "attempts": attempts, "capabilities": [c["key"] for c in data["capabilities"]],
                          "answer": {a.get("key"): a for a in (answer or {}).get("capabilities") or [] if isinstance(a, dict)}, "problems": wrong}
            folder.save(FILE, {"batches": kept, "log": log})

    with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
        list(pool.map(one, todo))
    folder.save(FILE, {"batches": kept, "log": log})
    if stopped:
        raise stop_for(stopped[0], "the final specifications")
    written = {k: a for name, _ in plan for k, a in ((kept.get(name) or {}).get("answer") or {}).items()}
    requirements = folder.load("outputs/reconcile/requirements.json") or {}
    sources = {f"{page_of(fid)}#{c['number']}": c for fid, body in requirements["functions"].items() for c in body.get("capabilities") or []}
    screen_ids = {s["id"] for s in (folder.load("design/modern.json") or {}).get("screens") or []}
    specs, found = [], []
    for spec in built["specs"]:
        done = finish(spec, written.get(spec["key"]))
        found += check(done, sources[spec["key"]], built["rules"], screen_ids, books)
        specs.append(done)
    folder.path(SPECS).mkdir(parents=True, exist_ok=True)
    for old in folder.path(SPECS).glob("*.json"):
        old.unlink()
    for s in specs:
        folder.save(f"{SPECS}/{slug(s['function'])}-{s['number']}.json", s)
    batch_problems = [f"{name}: {p}" for name, _ in plan for p in (kept.get(name) or {}).get("problems") or []]
    value = {"batches": kept, "log": log, "stack": target, "stack_notes": types["notes"],
             "specs": [{k: s[k] for k in ("key", "function", "function_name", "domain", "number", "title", "status", "runs_as")} for s in specs],
             "counts": counts(specs, books),
             "problems": batch_problems + found,
             "steps": len(todo), "cost_usd": round(sum(x.get("cost_usd") or 0 for x in log), 2)}
    folder.save(FILE, value)
    value["full"] = specs
    value["contracts"] = books
    value["round"] = told
    return value


def counts(specs: list[dict[str, Any]], books: dict[str, Any]) -> dict[str, Any]:
    criteria = [x for s in specs for x in s["acceptance"]]
    return {"capabilities": len(specs), "final": sum(1 for s in specs if s["status"] == "final"), "draft": sum(1 for s in specs if s["status"] == "draft"),
            "requirements": sum(len(s["requirements"]) for s in specs), "rules": len({r["key"] for s in specs for r in s["rules"]}),
            "criteria": len(criteria), "from_examples": sum(1 for x in criteria if x["from"].startswith("worked")),
            "written": sum(1 for x in criteria if x["from"].startswith("written")), "design_notes": sum(len(s["design_notes"]) for s in specs),
            "contracts": len(books), "tables": sum(len(s["tables"]) for s in specs), "gaps": sum(s["gaps"] for s in specs),
            "questions": len({q["id"] or q["question"] for s in specs for q in s["questions"]}),
            "classes": {c: sum(1 for s in specs for r in s["rules"] if r["class"] == c) for c in CLASS_ORDER},
            "runs_as": {k: sum(1 for s in specs if s["runs_as"] == k) for k in ("online", "scheduled job", "online and scheduled job", "service")}}


def main(argv: list[str] | None = None) -> int:
    import argparse
    from reframe.core.errors import Stop
    from reframe.core.runfolder import find_run
    from reframe.design import designpage
    from reframe.reconcile.pipeline import claude_code
    parser = argparse.ArgumentParser(prog="python -m reframe.design.specs", description="The final specifications (P4-07)")
    parser.add_argument("--run", help="the run (default: the latest run)")
    parser.add_argument("--stack", help='the target stack, "<front end>; <back end>; <data>"; recorded in the run')
    parser.add_argument("--auth", choices=("subscription", "bedrock"), default="subscription")
    args = parser.parse_args(argv)
    folder = find_run(args.run)
    from reframe.claude import preflight
    report = preflight.check(args.auth)
    if not report.ok:
        print(report.problems())
        return 2
    try:
        value = run(folder, claude_code(folder, args.auth), args.stack)
    except Stop as stop:
        print(stop.message)
        return 3
    page = designpage.draw(folder, value)
    print(json.dumps({"counts": value["counts"], "stack": (value["stack"] or {}).get("stack"), "problems": value["problems"][:20],
                      "problem_count": len(value["problems"]), "steps": value["steps"], "cost_usd": value["cost_usd"], "page": str(page)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
