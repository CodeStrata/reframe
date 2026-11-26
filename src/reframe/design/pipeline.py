"""Pipeline 4, stage D9: a design round (docs/pipeline-4.md, section 4, P4-09).

A round runs every stage in order: the screen inventory and the flow (no model), the journeys, the modern screens, the
prototype (no model), the final specifications, the design page and the package (no model). Each model stage keeps each
part with what it was made from, so a round redoes only the parts whose input changed, and says why.

The design context folder (given once with --context and remembered for later rounds; otherwise the run's own
inputs/design/) is read and each piece sent only to
the parts it touches:

| In the context folder | Goes to |
|---|---|
| `personas.md` | every domain's journeys |
| `decisions.md`, one decision per heading | the journeys, screens and specifications whose screens, functions, capabilities or rules it names |
| `design-system/components.md`, `tokens.json` | the modern screens' components; the prototype's colours and font |
| `style-reference/` | every domain's modern screens; the package's house conventions |
| Prototype review downloads | *Needs change* and *Question* marks to the domain that designed the screen; *Agree* keeps it |
| Reconciliation review downloads with sign-offs | the function's capabilities become final, with no model step |
| `target-architecture.md` | the package's stack sections |

A change to the reconciliation (a new round of pipeline 3) reaches the parts whose requirements or rules changed; a new
target stack (--stack) redoes the data contracts' types and the package, with no model step.

Each round writes design/changes-<round>.md (what was redone and why, what was kept) and the package's CHANGES.md from
it. `--plan` says what a round would redo, and why, without running a model step.

    python -m reframe.design.pipeline [--run <run>] [--context <folder>] [--stack "<front end>; <back end>; <data>"] [--plan]
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from reframe.core.runfolder import iso

WORDS = {
    "journeys": {"capabilities": "the requirements changed", "screens": "the domain's screens changed", "other_screens": "other domains' screens changed",
                 "flow": "the screen flow changed", "domain": "the domain's functions changed", "personas": "personas.md changed",
                 "decisions": "decisions that name it changed"},
    "screens": {"legacy_screens": "the domain's legacy screens changed", "rules": "the rules changed", "journeys": "its journeys changed",
                "requirements": "the requirements changed", "components": "the design system changed", "review_marks": "prototype marks on its screens changed",
                "decisions": "decisions that name it changed", "style_reference": "the style reference changed", "domain": "the domain changed"},
    "specs": {"requirements": "the requirements changed", "rules": "the rules changed", "screens": "the screens that serve it changed",
              "capabilities": "the capabilities changed", "decisions": "decisions that name it changed"},
    "": {"new": "new", "problems": "it failed Reframe's checks last round", "unrecorded": "an input changed (the earlier round did not record which)", "method": "Reframe's method changed"},
}
TEXT = (".md", ".txt", ".css", ".scss", ".html", ".htm", ".json", ".ts", ".tsx", ".js", ".jsx", ".java", ".kt", ".cs", ".py", ".go", ".xml", ".yaml", ".yml")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


# ---- the context folder ------------------------------------------------------------------------------------------------

def decisions_of(text: str) -> list[dict[str, str]]:
    """decisions.md as one decision per heading (any level), with its text."""
    found: list[dict[str, str]] = []
    title = ""
    body: list[str] = []
    for line in text.splitlines():
        m = re.match(r"^#{1,6}\s+(.+)$", line)
        if m:
            if title or "".join(body).strip():
                found.append({"title": title or "Decision", "text": "\n".join(body).strip()})
            title, body = m.group(1).strip(), []
        else:
            body.append(line)
    if title or "".join(body).strip():
        found.append({"title": title or "Decision", "text": "\n".join(body).strip()})
    return [d for d in found if d["text"] or d["title"]]


def style_reference(folder: Path) -> list[dict[str, str]]:
    """The style reference: each file's name, and the text of text files (4,000 characters each, 20,000 in all)."""
    found, room = [], 20000
    for p in sorted(x for x in folder.rglob("*") if x.is_file() and not x.name.startswith(".")):
        entry = {"file": p.relative_to(folder).as_posix()}
        if p.suffix.lower() in TEXT and room > 0:
            text = p.read_text(errors="replace")[:min(4000, room)]
            room -= len(text)
            entry["text"] = text
        found.append(entry)
    return found


def gather(folder, context: Path | None) -> dict[str, Any]:
    """Everything the context folder gives a round, and each file's hash (to say which changed since the last round)."""
    from reframe.design.prototype import TOOL
    from reframe.reconcile import reviews
    got: dict[str, Any] = {"decisions": [], "style": [], "marks": {}, "journey_signoffs": [], "signoffs": [], "tokens": None, "files": {}, "ignored": []}
    if not context or not context.is_dir():
        return got
    got["files"] = {p.relative_to(context).as_posix(): _sha(p) for p in sorted(context.rglob("*")) if p.is_file() and not p.name.startswith(".")}
    if (context / "decisions.md").is_file():
        got["decisions"] = decisions_of((context / "decisions.md").read_text())
    if (context / "style-reference").is_dir():
        got["style"] = style_reference(context / "style-reference")
    tokens = context / "design-system" / "tokens.json"
    if tokens.is_file():
        try:
            got["tokens"] = json.loads(tokens.read_text())
        except ValueError:
            got["ignored"].append({"file": "design-system/tokens.json", "why": "not JSON"})
    read = reviews.read(folder, context)
    got["ignored"] += read["ignored"]
    for r in read["reviews"]:
        if r["tool"] == TOOL:
            for m in r["marks"]:
                entry = got["marks"].setdefault(m["key"], {"key": m["key"], "statuses": [], "comments": []})
                entry["statuses"].append(m["status"])
                if m["comment"].strip():
                    entry["comments"].append(f"{r['reviewer'] or 'A reviewer'}: {m['comment'].strip()}")
            got["journey_signoffs"] += [{**x, "reviewer": r["reviewer"]} for x in r.get("signoffs") or []]
        elif reviews.page_of(r["tool"]) == "reconciled":
            got["signoffs"] += [{"function": x["function"], "reviewer": r["reviewer"], "at": x["at"], "comment": x["comment"], "file": r["file"]}
                                for x in r.get("signoffs") or [] if x["function"].startswith("rec/")]
    return got


def open_marks(marks: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Marks that ask for a change, by modern screen: Needs change or Question takes precedence over Agree."""
    found: dict[str, list[dict[str, Any]]] = {}
    for key, m in sorted(marks.items()):
        status = "change" if "change" in m["statuses"] else "question" if "question" in m["statuses"] else "agree"
        if status == "agree" or not key.startswith("design/"):
            continue
        screen, _, component = key[len("design/"):].partition("/")
        found.setdefault(screen, []).append({"screen": screen, "component": component, "status": "Needs change" if status == "change" else "Question",
                                             "comments": m["comments"]})
    return found


def _names(decision: dict[str, str], names: set[str]) -> bool:
    text = f"{decision['title']}\n{decision['text']}"
    for n in names:
        if not n:
            continue
        if re.fullmatch(r"[A-Z0-9-]+", n):
            if re.search(rf"(?<![\w-]){re.escape(n)}(?![\w-])", text):
                return True
        elif n.lower() in text.lower():
            return True
    return False


# ---- routing -----------------------------------------------------------------------------------------------------------

def routers(folder, got: dict[str, Any], routed: set[str] | None = None):
    """The extra input each stage's parts get this round; the titles of the decisions handed out go into `routed`."""
    from reframe.design import package
    modern = folder.load("design/modern.json") or {}
    designed = {key: {s["id"] for s in d.get("screens") or []} for key, d in (modern.get("domains") or {}).items()}
    for s in modern.get("screens") or []:  # a shared screen belongs to every domain that designed it
        for key in s.get("domains") or []:
            designed.setdefault(key, set()).add(s["id"])
    registry = folder.load(package.IDS, {}) or {}
    codes, rule_ids = registry.get("functions") or {}, registry.get("rules") or {}
    marks = open_marks(got["marks"])
    decisions = got["decisions"]

    def picked(names_: set[str]) -> dict[str, Any]:
        mine = [d for d in decisions if _names(d, names_)]
        if routed is not None:
            routed.update(d["title"] for d in mine)
        return {"decisions": mine} if mine else {}

    def journeys(key: str, data: dict[str, Any]) -> dict[str, Any]:
        found = {s["screen"] for s in data["screens"]} | {f["name"] for f in data["domain"]["functions"]} | {c["title"] for c in data["capabilities"]}
        return picked(found)

    def screens(key: str, data: dict[str, Any]) -> dict[str, Any]:
        mine = designed.get(key, set())
        found = {s["screen"] for s in data["legacy_screens"]} | mine
        extra = picked(found | {data["domain"]})
        review = [m for sid in sorted(mine) for m in marks.get(sid, [])]
        if review:
            extra["review_marks"] = review
        if got["style"]:
            extra["style_reference"] = got["style"]
        return extra

    def specs(name: str, data: dict[str, Any]) -> dict[str, Any]:
        found = {data["function"]}
        for c in data["capabilities"]:
            fid, _, number = c["key"][len("rec/"):].rpartition("#")
            code = codes.get(fid)
            found.add(c["title"])
            if code:
                found.add(f"{code}-C{int(number):02d}")
                found |= {f"{code}-{q['code']}" for q in c["requirements"]}
            found |= {rule_ids[r["key"]] for r in c["rules"] if r["key"] in rule_ids}
        return picked(found)

    return journeys, screens, specs


# ---- the round ---------------------------------------------------------------------------------------------------------

def words(stage: str, keys: list[str]) -> str:
    return "; ".join(dict.fromkeys(WORDS[stage].get(k) or WORDS[""].get(k) or k for k in keys))


def shown_context(folder, context: Path | None) -> str:
    """The context folder as the round's notes name it: inside the run, its path from the run folder (inputs/design);
    elsewhere, its name alone. The notes go into the package that is handed over, so they never hold a local path."""
    if not context:
        return ""
    try:
        return context.resolve().relative_to(folder.root.resolve()).as_posix()
    except ValueError:
        return f"{context.name} (outside the run folder)"


def changes_md(n: int, report: dict[str, Any]) -> str:
    out = [f"# Design round {n}", "", f"{report['at'][:10]}. Context folder: {report.get('context_shown') or 'none'}.", ""]
    ctx = report["context_files"]
    if ctx["added"] or ctx["changed"] or ctx["removed"]:
        out += ["## The context", ""] + [f"- Added {f}" for f in ctx["added"]] + [f"- Changed {f}" for f in ctx["changed"]] + [f"- Removed {f}" for f in ctx["removed"]] + [""]
    for stage, title in (("journeys", "Journeys"), ("screens", "Modern screens"), ("specs", "Final specifications")):
        r = report["stages"].get(stage) or {"redone": [], "kept": []}
        out += [f"## {title}", ""]
        out += [f"- Made: {x['name'] or 'No domain'} (new)." if x["changed"] == ["new"] else f"- Redone: {x['name'] or 'No domain'}, because {words(stage, x['changed'])}."
                for x in r["redone"]]
        out.append(f"- Kept: {len(r['kept'])}" + (f" ({', '.join(k or 'No domain' for k in r['kept'][:12])}{' …' if len(r['kept']) > 12 else ''})" if r["kept"] else "") + ".")
        out.append("")
    if report.get("signoffs"):
        out += ["## Sign-offs read", ""] + [f"- {x['function'][len('rec/'):]}, by {x['reviewer'] or 'a reviewer'}: its capabilities are final." for x in report["signoffs"]] + [""]
    if report.get("journey_signoffs"):
        out += ["## Journeys signed off in the prototype", ""] + [f"- {x['function'][len('design/'):]} by {x['reviewer'] or 'a reviewer'}." for x in report["journey_signoffs"]] + [""]
    if report.get("unrouted"):
        out += ["## Decisions that name nothing Reframe knows", "", "They are in the package's product description only.", ""] + [f"- {d}" for d in report["unrouted"]] + [""]
    if report.get("package"):
        p = report["package"]
        out += ["## The package", "", f"- v{p['version']}" + (" (new)." if p["new"] else " (unchanged).")]
    if report.get("ignored"):
        out += ["", "## Files not read", ""] + [f"- {x['file']}: {x['why']}" for x in report["ignored"]]
    return "\n".join(out).rstrip() + "\n"


def run(folder, claude, context: Path | None = None, stack: str | None = None, plan_only: bool = False) -> dict[str, Any]:
    from reframe.claude.workspace import paths
    from reframe.design import designpage, flow, flowpage, inventory, journeypage, journeys, legacy, modernpage, package, prototype, screens, specs
    state = folder.state.get("design") or {}
    from reframe.core.runfolder import default_context
    context = context or (Path(state["context"]) if state.get("context") else None) or default_context(folder, "design")
    if context and not context.is_dir():
        raise ValueError(f"the context folder {context} does not exist")
    number = state.get("round", 0) if state.get("status") == "running" else state.get("round", 0) + 1
    got = gather(folder, context)
    routed: set[str] = set()
    for_journeys, for_screens, for_specs = routers(folder, got, routed)
    before = state.get("context_files") or {}
    report: dict[str, Any] = {"at": iso(), "context": str(context) if context else "", "context_shown": shown_context(folder, context), "stages": {},
                              "context_files": {"added": sorted(set(got["files"]) - set(before)), "removed": sorted(set(before) - set(got["files"])),
                                                "changed": sorted(f for f in got["files"] if f in before and before[f] != got["files"][f])},
                              "signoffs": got["signoffs"], "journey_signoffs": got["journey_signoffs"], "ignored": got["ignored"]}
    if plan_only:
        report["stages"]["journeys"] = journeys.run(folder, claude, context, for_journeys, plan_only=True)["round"]
        report["stages"]["screens"] = screens.run(folder, claude, context, for_screens, plan_only=True)["round"]
        report["stages"]["specs"] = specs.run(folder, claude, stack, for_specs, plan_only=True, signoffs=got["signoffs"])["round"]
        report["note"] = "Screens and specifications whose journeys or screens a redone part changes are redone too; this plan cannot see those yet."
        return report
    folder.update(design={**state, "round": number, "status": "running", "context": str(context) if context else "", "started_at": iso()})
    legacy_folder = paths(folder)["legacy"]
    found = inventory.inventory(legacy_folder)
    folder.save("design/screens.json", found)
    legacy.draw_all(folder, found)
    linked = flow.flow(legacy_folder, found)
    linked["problems"] = flow.check(linked, legacy_folder)
    folder.save("design/flow.json", linked)
    flowpage.draw(folder, found, linked)
    value = journeys.run(folder, claude, context, for_journeys)
    journeypage.draw(folder, value)
    report["stages"]["journeys"] = value["round"]
    for_journeys, for_screens, for_specs = routers(folder, got, routed)
    value = screens.run(folder, claude, context, for_screens)
    modernpage.draw(folder, value)
    report["stages"]["screens"] = value["round"]
    data = prototype.build(folder.load("design/screens.json"), folder.load("design/modern.json"), folder.load("design/journeys.json"),
                           (folder.load("outputs/reconcile/rules.json") or {}).get("rules") or [], folder.state.get("project") or "")
    prototype.draw(folder, data, got["tokens"])
    for_journeys, for_screens, for_specs = routers(folder, got, routed)
    value = specs.run(folder, claude, stack, for_specs, signoffs=got["signoffs"])
    designpage.draw(folder, value)
    report["stages"]["specs"] = value["round"]
    report["problems"] = value["problems"]
    report["unrouted"] = [d["title"] for d in got["decisions"] if d["title"] not in routed]
    notes = changes_md(number, report).split("\n", 2)[2]
    report["package"] = package.run(folder, context, notes)
    text = changes_md(number, report)
    folder.path(f"design/changes-{number}.md").write_text(text)
    folder.update(design={**(folder.state.get("design") or {}), "round": number, "status": "done", "finished_at": iso(), "context_files": got["files"],
                          "last": {k: {"redone": len(v["redone"]), "kept": len(v["kept"])} for k, v in report["stages"].items()}})
    report["round"] = number
    report["changes"] = str(folder.path(f"design/changes-{number}.md"))
    return report


def main(argv: list[str] | None = None) -> int:
    import argparse
    from reframe.core.errors import Stop
    from reframe.core.runfolder import find_run
    from reframe.reconcile.pipeline import claude_code
    parser = argparse.ArgumentParser(prog="python -m reframe.design.pipeline", description="A design round (P4-09)")
    parser.add_argument("--run", help="the run (default: the latest run)")
    parser.add_argument("--context", help="the design context folder; remembered for later rounds")
    parser.add_argument("--stack", help='the target stack, "<front end>; <back end>; <data>"')
    parser.add_argument("--plan", action="store_true", help="say what a round would redo, and why, without a model step")
    parser.add_argument("--auth", choices=("subscription", "bedrock"), default="subscription")
    args = parser.parse_args(argv)
    folder = find_run(args.run)
    context = Path(args.context).expanduser() if args.context else None
    if not args.plan:
        from reframe.claude import preflight
        report = preflight.check(args.auth)
        if not report.ok:
            print(report.problems())
            return 2
    try:
        value = run(folder, None if args.plan else claude_code(folder, args.auth), context, args.stack, args.plan)
    except Stop as stop:
        print(stop.message)
        return 3
    print(json.dumps({k: v for k, v in value.items() if k not in ("problems",)} | {"problem_count": len(value.get("problems") or [])}, indent=1, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
