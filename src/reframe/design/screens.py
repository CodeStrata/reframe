"""Pipeline 4, stage D4: modern screens and their mapping (docs/pipeline-4.md, section 4, P4-05).

One headless Claude step per domain designs the modern screens for its journeys, from the design system's components,
and maps every legacy screen, data field and function key of the domain to what replaces it: kept, merged, split,
dropped or new, with the reason. Per domain, not per journey, so that a screen many journeys share (the sign-on, a menu)
is designed once, and a list and its detail can become one screen.

Each step is given its domain's legacy screens (each data field with its label, length and attributes, and each key
with where it leads), the rules its programs apply (validations, messages, displays, business rules, compliance), its
journeys with their requirements, and the component list. Reframe checks every answer:

- every component is from the design system, every id is unique, every rule and requirement key cited exists;
- every legacy screen, data field and key of the domain is mapped exactly once, and what it becomes exists;
- every validation rule a legacy screen's program applies is shown by a component of a modern screen that replaces it;
- every legacy screen in the domain's journeys is replaced by a modern screen.

A failed answer is asked once more with the reasons; what still fails is kept and listed. Across domains, every screen
a component leads to must exist. A domain whose input is unchanged keeps its design.

    python -m reframe.design.screens [--run <run>] [--context <folder>]

writes design/modern.json and outputs/design/modern.html.
"""

from __future__ import annotations

import hashlib
import json
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

FILE = "design/modern.json"
METHOD = "screens-1"
PARALLEL = 4
RULE_KINDS = ("validation", "error_handling", "display", "business", "compliance")
HOW = ("kept", "merged", "split", "dropped", "new")

# Reframe's own design system (docs/pipeline-4.md, section 5): plain, accessible components; design-system/components.md
# in the context folder replaces the list.
COMPONENTS = {
    "page": "a screen of the new application", "section": "a titled group of components", "form": "a set of inputs submitted together",
    "text": "a text input", "number": "a number input", "money": "an amount input with currency", "date": "a date input",
    "select": "a choice from a fixed list", "checkbox": "a yes/no choice", "radio": "one of a few choices", "password": "a hidden input",
    "search": "a search box", "display": "a read-only value", "table": "rows and columns, with paging and row actions",
    "list": "a list of items", "tabs": "panels shown one at a time", "button": "an action", "link": "navigation to another screen",
    "message": "an error, warning, success or information message", "dialog": "a confirmation or a short task over the screen",
    "nav": "the application's navigation", "header": "the application's header",
}

SCHEMA = {"type": "object", "required": ["screens", "mapping"], "properties": {
    "screens": {"type": "array", "items": {"type": "object", "required": ["id", "title", "purpose", "journeys", "replaces", "components"], "properties": {
        "id": {"type": "string"}, "title": {"type": "string"}, "purpose": {"type": "string"},
        "journeys": {"type": "array", "items": {"type": "string"}}, "replaces": {"type": "array", "items": {"type": "string"}},
        "components": {"type": "array", "items": {"type": "object", "required": ["id", "type", "label"], "properties": {
            "id": {"type": "string"}, "type": {"type": "string"}, "label": {"type": "string"}, "section": {"type": "string"},
            "shows": {"type": "string"}, "validation": {"type": "string"}, "goes_to": {"type": "string"}, "keyboard": {"type": "string"},
            "rules": {"type": "array", "items": {"type": "string"}}, "requirements": {"type": "array", "items": {"type": "string"}}}}}}}},
    "mapping": {"type": "array", "items": {"type": "object", "required": ["legacy_screen", "legacy", "kind", "how", "becomes", "why"], "properties": {
        "legacy_screen": {"type": "string"}, "legacy": {"type": "string"}, "kind": {"type": "string", "enum": ["screen", "field", "key"]},
        "how": {"type": "string", "enum": list(HOW)}, "becomes": {"type": "string"}, "why": {"type": "string"}}}}}}

PROMPT = """Read {input}. It holds one business domain of a legacy mainframe application being modernized, not lifted and shifted: its 3270 screens (each data field with its label, length and attributes, and each function key with where it leads), the business rules the screens' programs apply, the user journeys through the screens with the requirements they serve, and the components of the design system. The legacy source is under {legacy}/ if you need it; do not change anything.

Design the modern screens for this domain's journeys, and map the legacy screens to them.

Screens ("screens"): each with an "id" (S- and a few words, such as S-ACCOUNT-VIEW), "title", "purpose", the "journeys" it serves (their ids), the legacy screens it "replaces" (map names), and its "components". Each component has an "id" unique in the screen, a "type" from "components" exactly, a "label", and as needed: "section" (the group it is in), "shows" (the data it shows or takes), "validation" (what is checked and the message, in the rule's words), "goes_to" (for a button or link: the id of the screen it opens), "keyboard" (a shortcut), "rules" (the keys of the rules it applies or shows) and "requirements" (the keys of the requirements it serves).
- Do not recreate poor 3270 usability: no typed option codes or selection letters where a link, button or row action will do; no paging keys where a table pages; show related things together.
- Never hide a validation in the screen only: every validation rule of a legacy screen's program must be cited by a component of a modern screen that replaces it.
- Keep keyboard-heavy work fast: give shortcuts where people repeat a task, and keep a logical tab order.
- Meet WCAG 2.2 AA: every input has a visible label; errors say what to fix.
- The header fields every legacy screen repeats (transaction, program, date, time, titles) become the application's header and navigation once, not per screen.

If the file lists "other_domains_screens", other domains designed those screens: link to them by those ids, and reuse a shared screen (one that replaces nothing, such as the application's header and navigation) by its id and component ids rather than designing your own.

If the file lists "review_marks", reviewers marked these screens or components *Needs change* or *Question* in the prototype: change the design to answer each comment, and keep what they did not mark. If it lists "decisions", the owner made them: follow each one that applies. If it lists "style_reference", it is the house's own examples: follow their look and patterns where the design system does not say.

Mapping ("mapping"): one entry for every legacy screen (kind "screen"), every data field (kind "field", the field name as listed) and every function key (kind "key", such as F3) listed under "legacy_screens", exactly once each: "how" it is carried (kept, merged, split, dropped, new), what it "becomes" (a screen id for a screen, "<screen id>/<component id>" for a field or key, or empty when dropped) and "why". A component with no legacy counterpart needs no mapping entry; say "new" in its purpose if useful.

Use only keys listed. Answer only with the JSON."""

RETRY = """Your answer failed Reframe's checks. Answer again with the whole JSON, fixing these:

{problems}"""


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:16]


# ---- inputs ------------------------------------------------------------------------------------------------------------

def components(context: Path | None) -> dict[str, str]:
    """The design system's components: Reframe's own, or a context folder's design-system/components.md, one per line as
    "- name: what it is"."""
    path = context / "design-system" / "components.md" if context else None
    if path and path.is_file():
        found = {}
        for line in path.read_text().splitlines():
            if line.strip().startswith("-") and ":" in line:
                name, _, what = line.strip("- ").partition(":")
                found[name.strip().lower()] = what.strip()
        if found:
            return found
    return dict(COMPONENTS)


def legacy_items(screen: dict[str, Any], flow: dict[str, Any]) -> dict[str, Any]:
    """A legacy screen as the step sees it: its data fields with labels, and its keys with where they lead."""
    from reframe.design.journeys import screen_brief
    brief = screen_brief(screen, True)
    labels = {i["field"]: i["label"] for i in brief["inputs"]}
    fields = [{"field": f["name"], "kind": f["kind"], "label": labels.get(f["name"], ""), "length": f["length"],
               "attributes": f["attributes"]} for f in screen["fields"] if f["name"] and f["kind"] in ("input", "output")]
    targets = defaultdict(set)
    for k in flow.get("keys") or []:
        if k["screen"] == screen["map"]:
            targets[k["key"]].update(k["to"])
    says = {k["key"]: k["says"] for k in screen["keys"]["shown"]}
    keys = sorted({k["key"] for k in screen["keys"]["shown"]} | {k["key"] for k in screen["keys"]["handled"]})
    return {"screen": screen["map"], "title": screen["title"], "programs": brief["programs"], "fields": fields,
            "keys": [{"key": k, "says": says.get(k, ""), "leads_to": sorted(targets.get(k, ()))} for k in keys]}


def mapping_items(legacy: list[dict[str, Any]]) -> set[tuple[str, str, str]]:
    """(legacy screen, item, kind) for every screen, data field and key the mapping must carry."""
    found = set()
    for s in legacy:
        found.add((s["screen"], s["screen"], "screen"))
        found.update((s["screen"], f["field"], "field") for f in s["fields"])
        found.update((s["screen"], k["key"], "key") for k in s["keys"])
    return found


def domain_input(key: str, name: str, mine: list[str], screens: dict[str, Any], flow: dict[str, Any], journeys: list[dict[str, Any]],
                 rules: list[dict[str, Any]], requirements: dict[str, Any], parts: dict[str, str]) -> dict[str, Any]:
    by_map = {s["map"]: s for s in screens["screens"]}
    legacy = [legacy_items(by_map[m], flow) for m in mine if m in by_map]
    programs = {p for s in legacy for p in s["programs"]}
    texts = {}
    for fid, body in (requirements.get("functions") or {}).items():
        page = "rec/" + (fid or "unassigned")
        for cap in body.get("capabilities") or []:
            for r in cap.get("requirements") or []:
                texts[f"{page}/{r['code']}"] = r["text"][:200]
    here = [j for j in journeys if j.get("domain") == key]  # this domain's journeys; a screen they share is designed in its own domain
    wanted = sorted({k for j in here for k in j["requirements"]})
    return {"domain": name, "legacy_screens": legacy,
            "rules": [{"key": r["key"], "program": r["program"], "kind": r.get("kind", ""), "name": r.get("name", ""), "text": r["text"][:240]}
                      for r in rules if str(r.get("program", "")).upper() in programs and r.get("kind") in RULE_KINDS],
            "journeys": [{"id": j["id"], "name": j["name"], "role": j["role"], "goal": j["goal"],
                          "steps": [{"screen": s["screen"], "action": s["action"]} for s in j["steps"]]} for j in here],
            "requirements": [{"key": k, "text": texts.get(k, "")} for k in wanted],
            "components": parts}


# ---- checks ------------------------------------------------------------------------------------------------------------

def problems(answer: dict[str, Any] | None, data: dict[str, Any]) -> list[str]:
    if not isinstance(answer, dict):
        return ["no answer"]
    found = []
    parts = set(data["components"])
    rules = {r["key"]: r for r in data["rules"]}
    reqs = {r["key"] for r in data["requirements"]}
    legacy = {s["screen"]: s for s in data["legacy_screens"]}
    journeys = {j["id"] for j in data["journeys"]}
    ids, component_ids = set(), set()
    cited_by_replacing: dict[str, set[str]] = defaultdict(set)
    for s in answer.get("screens") or []:
        sid = s.get("id", "")
        if not sid or sid in ids:
            found.append(f'screen id "{sid}" is empty or used twice')
        ids.add(sid)
        for j in s.get("journeys") or []:
            if j not in journeys:
                found.append(f'{sid}: journey "{j}" is not listed')
        for m in s.get("replaces") or []:
            if m not in legacy:
                found.append(f'{sid}: "{m}" is not a legacy screen of this domain')
        seen = set()
        for c in s.get("components") or []:
            cid = c.get("id", "")
            if not cid or cid in seen:
                found.append(f'{sid}: component id "{cid}" is empty or used twice')
            seen.add(cid)
            component_ids.add(f"{sid}/{cid}")
            if str(c.get("type", "")).lower() not in parts:
                found.append(f'{sid}/{cid}: type "{c.get("type")}" is not a component of the design system')
            for k in c.get("rules") or []:
                if k not in rules:
                    found.append(f'{sid}/{cid}: rule "{k}" is not listed')
                for m in s.get("replaces") or []:
                    cited_by_replacing[m].add(k)
            for k in c.get("requirements") or []:
                if k not in reqs:
                    found.append(f'{sid}/{cid}: requirement "{k}" is not listed')
    for o in data.get("other_domains_screens") or []:  # a shared screen another domain designed: its components can be mapped into
        ids.add(o["id"])
        component_ids.update(f"{o['id']}/{c}" for c in o.get("components") or [])
    expected = mapping_items(data["legacy_screens"])
    given: dict[tuple[str, str, str], int] = defaultdict(int)
    for m in answer.get("mapping") or []:
        item = (m.get("legacy_screen", ""), m.get("legacy", ""), m.get("kind", ""))
        given[item] += 1
        if item not in expected:
            found.append(f'mapping: {item[2]} "{item[1]}" on {item[0]} is not a legacy {item[2]} listed')
            continue
        becomes, how = m.get("becomes", ""), m.get("how", "")
        if how == "dropped":
            continue
        if item[2] == "screen" and becomes not in ids:
            found.append(f'mapping: screen {item[0]} becomes "{becomes}", which is not a screen id')
        elif item[2] != "screen" and becomes not in component_ids and becomes not in ids:
            found.append(f'mapping: {item[2]} {item[1]} on {item[0]} becomes "{becomes}", which is not "<screen id>/<component id>"')
    for item in sorted(expected):
        if given.get(item, 0) == 0:
            found.append(f"mapping: {item[2]} {item[1]} on {item[0]} is not mapped")
        elif given[item] > 1:
            found.append(f"mapping: {item[2]} {item[1]} on {item[0]} is mapped {given[item]} times")
    for m, s in legacy.items():
        for r in data["rules"]:
            if r["kind"] == "validation" and r["program"] in s["programs"] and r["key"] not in cited_by_replacing.get(m, set()):
                found.append(f"validation rule {r['key']} of {m} is shown by no component of a screen that replaces {m}")
    in_journeys = {st["screen"] for j in data["journeys"] for st in j["steps"]} & set(legacy)
    replaced = {m for s in answer.get("screens") or [] for m in s.get("replaces") or []}
    for m in sorted(in_journeys - replaced):
        found.append(f"legacy screen {m} is in a journey but no modern screen replaces it")
    return found


def shared_screens(domains: dict[str, Any]) -> tuple[list[dict[str, Any]], set[str]]:
    """Screens two or more domains designed under one id that replace no legacy screen (the application's header and
    navigation, say) become one shared screen with every domain's components (the first of an id wins), so each domain's
    mapping into them still holds. Returns the shared screens and the ids designed twice that do replace legacy screens."""
    by_id: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for key, d in sorted(domains.items()):
        for s in d["screens"]:
            by_id[s["id"]].append((key, s))
    shared, clashes = [], set()
    for sid, found in by_id.items():
        if len(found) < 2:
            continue
        if any(s.get("replaces") for _, s in found):
            clashes.add(sid)
            continue
        parts, seen = [], set()
        for _, s in found:
            for c in s.get("components") or []:
                if c.get("id") not in seen:
                    seen.add(c.get("id"))
                    parts.append(c)
        first = found[0][1]
        shared.append({**first, "components": parts, "journeys": sorted({j for _, s in found for j in s.get("journeys") or []}),
                       "domains": [k for k, _ in found]})
    return shared, clashes


def all_screens(domains: dict[str, Any]) -> list[dict[str, Any]]:
    """Every modern screen once: each domain's own, then the shared ones."""
    shared, _ = shared_screens(domains)
    ids = {s["id"] for s in shared}
    return [{**s, "domain": d["name"]} for d in domains.values() for s in d["screens"] if s["id"] not in ids] + \
           [{**s, "domain": "Shared"} for s in shared]


def links_across(domains: dict[str, Any]) -> dict[str, list[str]]:
    """By domain: links to a screen no domain designed, and screens designed twice that replace legacy screens."""
    ids = {s["id"] for s in all_screens(domains)}
    _, clashes = shared_screens(domains)
    found: dict[str, list[str]] = defaultdict(list)
    for key, d in domains.items():
        for s in d["screens"]:
            if s["id"] in clashes:
                found[key].append(f'screen id "{s["id"]}" is also used by another domain; choose another id')
            for c in s.get("components") or []:
                if c.get("goes_to") and c["goes_to"] not in ids:
                    found[key].append(f'{s["id"]}/{c["id"]} goes to "{c["goes_to"]}", which is no screen; use one of the ids listed under "other_domains_screens"')
    return dict(found)


# ---- run ---------------------------------------------------------------------------------------------------------------

def run(folder, claude, context: Path | None = None, more=None, plan_only: bool = False) -> dict[str, Any]:
    """D4 for every domain whose input changed. `more(key, data)` gives a domain's extra input for a round (prototype
    marks on its screens, the decisions that name it, the style reference); `plan_only` says what would be redone."""
    from reframe.claude.steps import stop_for
    from reframe.design import rounds
    from reframe.claude.workspace import paths
    from reframe.design.journeys import domains_of_screens
    places = paths(folder)
    project = folder.state["project"]
    screens, flow, journeyed = folder.load("design/screens.json"), folder.load("design/flow.json"), folder.load("design/journeys.json")
    requirements = folder.load("outputs/reconcile/requirements.json") or {}
    rules = (folder.load("outputs/reconcile/rules.json") or {}).get("rules") or []
    if not screens or not flow or not journeyed or not journeyed.get("journeys"):
        raise ValueError("run the screen inventory, the screen flow and the journeys first")
    parts = components(context)
    by_domain = domains_of_screens(screens, rules, requirements)
    names = {d["key"]: d["name"] for d in requirements.get("domains") or []} | {"": "No domain"}
    saved = folder.load(FILE, {}) or {}
    kept, log = saved.get("domains") or {}, saved.get("log") or []
    folder_in = places["analysis"] / "reframe" / "design"
    folder_in.mkdir(parents=True, exist_ok=True)
    lock, stopped, todo, inputs, why = threading.Lock(), [], [], {}, []
    for key, mine in sorted(by_domain.items()):
        data = domain_input(key, names.get(key, key), mine, screens, flow, journeyed["journeys"], rules, requirements, parts)
        data.update(more(key, data) if more else {})
        digest = _hash([data, METHOD])
        inputs[key] = (data, digest)
        before = kept.get(key) or {}
        if before.get("hash") != digest or before.get("problems"):
            todo.append((key, data, digest))
            why.append((key, rounds.changed(before or None, rounds.parts(data, METHOD)) if before.get("hash") != digest else ["problems"]))
        elif before and not before.get("parts") and not plan_only:  # kept, but made before rounds recorded its pieces (P4-10)
            before["parts"] = rounds.parts(data, METHOD)
    plan = rounds.summary(why, [k for k in by_domain if k not in {t[0] for t in todo}])
    if plan_only:
        return {"round": plan}

    def one(item, across: list[str] | None = None) -> None:
        key, data, digest = item
        if stopped:
            return
        safe = "".join(c if c.isalnum() else "-" for c in (key or "no-domain")).strip("-")[:50]
        path = folder_in / f"screens-{safe}{'-links' if across else ''}.json"
        path.write_text(json.dumps(data, indent=1))
        prompt = PROMPT.format(input=f"analysis/{project}/{path.relative_to(places['analysis']).as_posix()}", legacy=f"legacy/{project}")
        answer, wrong, attempts = None, across or ["no answer"], 0
        for attempt in ((3,) if across else (1, 2)):  # the links pass: one more ask, with every other domain's screens
            attempts = attempt
            step = claude.run(f"screens-{safe}{'-links' if across else '-retry' if attempt == 2 else ''}",
                              prompt if attempt == 1 else prompt + "\n\n" + RETRY.format(problems="\n".join(f"- {p}" for p in wrong[:80])),
                              timeout=3600, schema=SCHEMA)
            with lock:
                log.append({"domain": key, "attempt": attempt, **{k: v for k, v in step.as_json().items() if k in ("ok", "seconds", "tokens", "cost_usd", "problem")}})
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
        if across and answer is None:
            return  # the links pass did not finish: keep the domain's first design
        with lock:
            kept[key] = {"hash": digest, "parts": rounds.parts(data, METHOD), "name": data["domain"], "legacy": [s["screen"] for s in data["legacy_screens"]], "attempts": attempts,
                         "screens": (answer or {}).get("screens") or [], "mapping": (answer or {}).get("mapping") or [], "problems": wrong}
            folder.save(FILE, {"domains": kept, "log": log})

    with ThreadPoolExecutor(max_workers=PARALLEL) as pool:
        list(pool.map(one, todo))
    folder.save(FILE, {"domains": kept, "log": log})
    if stopped:
        raise stop_for(stopped[0], "the modern screens")
    # the links pass: a domain that links to screens no domain designed, or reuses another's id, is asked once more,
    # with every other domain's screens listed; it ran in parallel and could not see them
    across = links_across(kept)
    repairs = []
    for key, found in sorted(across.items()):
        if (kept.get(key) or {}).get("links_pass") == inputs[key][1]:
            continue  # already asked for this input
        others = [{"id": s["id"], "title": s["title"], "replaces": s.get("replaces") or [], "domain": s["domain"],
                   **({"components": [c.get("id") for c in s.get("components") or []]} if not s.get("replaces") else {})}
                  for s in all_screens({k: d for k, d in kept.items() if k != key})]
        repairs.append(((key, {**inputs[key][0], "other_domains_screens": others}, inputs[key][1]), found))
    for item, found in repairs:
        one(item, found)
        if stopped:
            break
        kept[item[0]]["links_pass"] = item[2]
    folder.save(FILE, {"domains": kept, "log": log})
    if stopped:
        raise stop_for(stopped[0], "the modern screens")
    across = links_across(kept)
    mapping = [m for d in kept.values() for m in d["mapping"]]
    value = {"domains": kept, "log": log, "components": parts, "screens": all_screens(kept),
             "counts": {"screens": sum(len(d["screens"]) for d in kept.values()), "mapped": len(mapping),
                        "how": {h: sum(1 for m in mapping if m.get("how") == h) for h in HOW}},
             "problems": [f"{d['name']}: {p}" for d in kept.values() for p in d["problems"]]
             + [f"{kept[k]['name']}: {p}" for k, found in across.items() for p in found],
             "steps": len(todo), "cost_usd": round(sum(x.get("cost_usd") or 0 for x in log), 2)}
    folder.save(FILE, value)
    return {**value, "round": plan}


def main(argv: list[str] | None = None) -> int:
    import argparse
    from reframe.core.errors import Stop
    from reframe.core.runfolder import find_run
    from reframe.design import modernpage
    from reframe.reconcile.pipeline import claude_code
    parser = argparse.ArgumentParser(prog="python -m reframe.design.screens", description="Modern screens and their mapping (P4-05)")
    parser.add_argument("--run", help="the run (default: the latest run)")
    parser.add_argument("--context", help="a folder with design-system/components.md")
    parser.add_argument("--auth", choices=("subscription", "bedrock"), default="subscription")
    args = parser.parse_args(argv)
    folder = find_run(args.run)
    from reframe.claude import preflight
    report = preflight.check(args.auth)
    if not report.ok:
        print(report.problems())
        return 2
    try:
        value = run(folder, claude_code(folder, args.auth), Path(args.context).expanduser() if args.context else None)
    except Stop as stop:
        print(stop.message)
        return 3
    page = modernpage.draw(folder, value)
    print(json.dumps({"counts": value["counts"], "problems": value["problems"][:20], "problem_count": len(value["problems"]), "steps": value["steps"],
                      "cost_usd": value["cost_usd"], "page": str(page)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
