"""SC-06: a mainframe expert's own check of an audit sample (docs/pipeline-3.md, section 8.13). No model.

The accuracy audit (P3-11) is judged by two Claude steps and settled by the owner. This gives the same sample to a person
who knows mainframe code, blind: each rule with the source lines it cites, and nothing about how it was decided, how
sure Reframe is, or what the judges said. Their verdicts come back as a CSV, and Reframe reports how often they agree
with the judges and with the audit's final verdicts, and the rules they call wrong.

    python -m reframe.reconcile.expert pack <empty folder> [--run <run>] [--size 40 --seed 7]
    python -m reframe.reconcile.expert read <verdicts.csv> --expert <name> [--run <run>]

`pack` uses the audit's own sample when there is one, so the expert's verdicts can be set beside the judges'; without
one it draws a sample of its own. The pack is cleaned as `reframe publish` cleans a copy, since it goes to someone
outside the team.
"""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from reframe.core.runfolder import RunFolder, iso
from reframe.reconcile import audit

FOLDER = audit.FOLDER
COLUMNS = ["id", "program", "rule", "verdict", "defect", "comment", "lines_read"]
CITE = re.compile(r"^(?P<path>.+?):(?P<start>\d+)(?:-(?P<end>\d+))?$")
CONTEXT = 2  # lines shown around each cited range
LONGEST = 60  # lines of one cited range shown at most

GUIDE = """For each rule, read the cited lines (and anything else in the source you need), then give:

- **verdict**: `correct` if every statement in the rule is true of what the code does when it runs; `minor` if it is true in
  substance but a detail is wrong or missing (a value, a condition, a message); `wrong` if the code does not do it, or
  the code it describes can never run; `unsure` if the source shown is not enough to say.
- **defect** (only where a rule shows a *possible defect*): `real` if the code does what the note says and it looks
  unintended; `not_a_defect` if it does not, or it is plainly intended; `unsure` otherwise. Leave it empty elsewhere.
- **comment**: what in the code decided it, in a sentence or two. **lines_read**: the lines you relied on, as
  `<path>:<start>-<end>`, separated by spaces.

Judge only what the code does. You are not told how each rule was written or how sure anyone is of it, on purpose."""


def _excerpt(legacy: Path, cite: str) -> dict[str, Any]:
    m = CITE.match(str(cite).strip())
    root = legacy.resolve()
    target = (legacy / m["path"]).resolve() if m else None
    if not m or target is None or not target.is_relative_to(root) or not target.is_file():
        return {"cite": cite, "lines": [], "missing": True}
    lines = target.read_text(errors="replace").splitlines()
    start, end = int(m["start"]), int(m["end"] or m["start"])
    shown_end = min(end, start + LONGEST - 1)
    first, last = max(1, start - CONTEXT), min(len(lines), shown_end + CONTEXT)
    return {"cite": cite, "missing": False, "cut": end > shown_end,
            "lines": [{"n": n, "text": lines[n - 1], "cited": start <= n <= end} for n in range(first, last + 1)]}


def items_for(folder: RunFolder, size: int = 40, seed: int = 7) -> tuple[list[dict[str, Any]], str]:
    """The items to give the expert, and where they came from: the audit's sample when there is one."""
    saved = folder.load(f"{FOLDER}/sample.json")
    if saved:
        return saved["items"], f"the accuracy audit's sample (seed {saved.get('seed')})"
    return audit.draw(audit.candidates(folder), size, seed), f"a sample of its own (size {size}, seed {seed})"


def blind(item: dict[str, Any], with_note: bool) -> dict[str, Any]:
    """What the expert sees: the rule, its program and its cited lines; a unit's defect note once. Never the decision,
    the kind, the confidence, the tools' own rules or the judges' answers."""
    return {"id": item["id"], "program": item["program"], "rule": item["rule"], "cites": list(item["cites"]),
            "defect_note": item["defect_note"] if with_note else ""}


def page(rows: list[dict[str, Any]], project: str, origin: str) -> str:
    def code(ex: dict[str, Any]) -> str:
        if ex["missing"]:
            return f"<p class='missing'>{html.escape(ex['cite'])}: not in the snapshot</p>"
        body = "".join(f"<span class='{'hit' if ln['cited'] else 'ctx'}'><b>{ln['n']:>5}</b> {html.escape(ln['text'])}</span>\n" for ln in ex["lines"])
        return (f"<div class='cite'>{html.escape(ex['cite'])}" + (" (first lines shown)" if ex.get("cut") else "") + f"</div><pre>{body}</pre>")
    items = "".join(
        f"<section id='{r['id']}'><h2>{r['id']} <small>{html.escape(r['program'])}</small></h2><p class='rule'>{html.escape(r['rule'])}</p>"
        + (f"<p class='note'><b>Possible defect:</b> {html.escape(r['defect_note'])}</p>" if r["defect_note"] else "")
        + "".join(code(ex) for ex in r["excerpts"]) + "</section>" for r in rows)
    guide = html.escape(GUIDE).replace("\n\n", "</p><p>").replace("\n", " ")
    guide = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", re.sub(r"`(.+?)`", r"<code>\1</code>", guide))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Expert check: {html.escape(project)}</title><style>
body{{font:16px/1.5 system-ui,sans-serif;max-width:60rem;margin:2rem auto;padding:0 1rem;color:#1b1b1f;background:#fff}}
h1{{font-size:1.6rem}} h2{{font-size:1.15rem;margin:2rem 0 .3rem}} small{{color:#5b5b66;font-weight:400}}
.rule{{font-size:1.05rem}} .note{{background:#fff4e5;padding:.5rem .75rem;border-radius:6px}}
.cite{{font:600 .85rem ui-monospace,monospace;color:#3a3a48;margin-top:.75rem}} .missing{{color:#a4161a}}
pre{{background:#f6f6f9;padding:.6rem;border-radius:6px;overflow-x:auto;font:.85rem/1.45 ui-monospace,monospace}}
.hit{{background:#fff3b0}} .ctx{{color:#5b5b66}} b{{font-weight:600}} section{{border-top:1px solid #e3e3ea}}
@media (prefers-color-scheme: dark){{body{{background:#121217;color:#e9e9ef}} pre{{background:#1d1d25}} .hit{{background:#4a4200}}
.note{{background:#3a2a10}} small,.ctx{{color:#a3a3b2}} .cite{{color:#c9c9d6}} section{{border-color:#2c2c38}}}}
</style></head><body><h1>Expert check: {html.escape(project)}</h1>
<p>{len(rows)} business rules written about this legacy system, from {html.escape(origin)}. Record your verdicts in <code>verdicts.csv</code>.</p>
<p>{guide}</p>{items}</body></html>
"""


def pack(folder: RunFolder, out: Path, size: int = 40, seed: int = 7) -> dict[str, Any]:
    """Write the expert's pack into an empty folder: index.html, verdicts.csv, README.md and pack.json."""
    from reframe.claude.workspace import paths
    from reframe.report.publish import Cleaner
    if ((folder.state.get("reconcile") or {}).get("status")) != "DONE":
        raise SystemExit(f"run {folder.root.name}: the reconciliation is not done; reframe reconcile first")
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f"{out} is not empty; give an empty folder, so a filled-in verdicts.csv is never overwritten")
    items, origin = items_for(folder, size, seed)
    with_note = audit.noted(items)
    legacy = paths(folder)["legacy"]
    rows = [{**blind(i, i["id"] in with_note), "excerpts": [_excerpt(legacy, c) for c in i["cites"]]} for i in items]
    project = folder.state.get("project") or "the application"
    cleaner = Cleaner(folder)
    sheet = io.StringIO()
    writer = csv.writer(sheet)
    writer.writerow(COLUMNS)
    for r in rows:
        writer.writerow([r["id"], r["program"], r["rule"][:200], "", "", "", ""])
    snapshot = (folder.load("snapshot.json") or {}).get("sha256", "")
    files = {"index.html": page(rows, project, origin), "verdicts.csv": sheet.getvalue(),
             "README.md": f"# Expert check: {project}\n\nOpen `index.html`, judge each rule against the source lines shown, and fill in "
                          f"`verdicts.csv`; send it back.\n\n{GUIDE}\n\nThe rules come from {origin}. The source is the snapshot "
                          f"with SHA-256 `{snapshot[:16]}`.\n",
             "pack.json": json.dumps({"format": "reframe-expert-pack/1", "run": folder.root.name, "project": project, "made_at": iso(),
                                      "snapshot_sha256": snapshot, "origin": origin, "items": [r["id"] for r in rows]}, indent=1) + "\n"}
    left: list[str] = []
    out.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        cleaned = cleaner.clean(text)
        left += [f"{name}: {what}" for what in cleaner.left(cleaned)]
        (out / name).write_text(cleaned)
    folder.save(f"{FOLDER}/expert-pack.json", {"made_at": iso(), "origin": origin, "items": [i["id"] for i in items],
                                               "keys": {i["id"]: i["key"] for i in items}})
    return {"path": str(out), "items": len(rows), "origin": origin, "defect_notes": len(with_note), "left": left}


def read_verdicts(text: str, ids: set[str]) -> tuple[dict[str, dict[str, str]], list[str]]:
    """The verdicts in a returned CSV, and what is wrong with it. Rows for unknown items are named, not used."""
    found: dict[str, dict[str, str]] = {}
    problems = []
    for n, row in enumerate(csv.DictReader(io.StringIO(text.lstrip("﻿"))), 2):
        item = (row.get("id") or "").strip()
        if not item:
            continue
        verdict = (row.get("verdict") or "").strip().lower()
        defect = (row.get("defect") or "").strip().lower().replace(" ", "_")
        if item not in ids:
            problems.append(f"line {n}: {item} is not in the pack")
        elif verdict and verdict not in audit.VERDICTS:
            problems.append(f"line {n}: {item}'s verdict {verdict!r} is not one of {', '.join(audit.VERDICTS)}")
        elif defect and defect not in audit.DEFECTS:
            problems.append(f"line {n}: {item}'s defect {defect!r} is not one of {', '.join(audit.DEFECTS)}")
        elif verdict:
            found[item] = {"verdict": verdict, "defect": defect, "comment": (row.get("comment") or "").strip(),
                           "lines_read": (row.get("lines_read") or "").strip()}
    return found, problems


def compare(items: list[dict[str, Any]], expert: dict[str, dict[str, str]], judged: dict[str, dict[str, Any]],
            finals: dict[str, dict[str, str]]) -> dict[str, Any]:
    """The expert's figures, and how often they agree with each judge and with the audit's final verdict."""
    recommended = [i for i in items if i["kind"] != "rejected" and i["id"] in expert]
    counts = Counter(expert[i["id"]]["verdict"] for i in recommended)
    n = len(recommended)
    out: dict[str, Any] = {"items": len(items), "answered": len(expert), "recommended": {
        "items": n, **{v: counts.get(v, 0) for v in audit.VERDICTS},
        "correct_share": round(counts.get("correct", 0) / n, 2) if n else None,
        "correct_or_minor_share": round((counts.get("correct", 0) + counts.get("minor", 0)) / n, 2) if n else None}}
    rejected = [i for i in items if i["kind"] == "rejected" and i["id"] in expert]
    out["rejections_upheld"] = {"upheld": sum(expert[i["id"]]["verdict"] in ("wrong", "unsure") for i in rejected), "of": len(rejected)}
    answered = [i for i in items if i["id"] in expert]
    agreement = {}
    for label in sorted(judged):
        theirs = {i["id"]: (judged[label]["answers"].get(i["id"]) or {}).get("verdict") for i in answered}
        agreement[label] = {"agreed": sum(theirs[i["id"]] == expert[i["id"]]["verdict"] for i in answered), "of": len(answered)}
    if finals:
        settled = [i for i in answered if (finals.get(i["id"]) or {}).get("verdict") not in (None, "unsettled")]
        agreement["final"] = {"agreed": sum(finals[i["id"]]["verdict"] == expert[i["id"]]["verdict"] for i in settled), "of": len(settled)}
    out["agreement"] = agreement
    out["differs_from_final"] = [{"id": i["id"], "kind": audit.KINDS[i["kind"]], "confidence": i.get("confidence", ""),
                                  "final": finals[i["id"]]["verdict"], "expert": expert[i["id"]]["verdict"], "comment": expert[i["id"]]["comment"]}
                                 for i in answered if finals and (finals.get(i["id"]) or {}).get("verdict") not in (None, "unsettled", expert[i["id"]]["verdict"])]
    out["wrong"] = [{"id": i["id"], "kind": audit.KINDS[i["kind"]], "confidence": i.get("confidence", ""), "rule": i["rule"],
                     "comment": expert[i["id"]]["comment"]} for i in recommended if expert[i["id"]]["verdict"] == "wrong"]
    return out


def read(folder: RunFolder, sheet: Path, name: str) -> dict[str, Any]:
    """Read an expert's verdicts.csv back: keep it, and write their figures beside the audit's."""
    made = folder.load(f"{FOLDER}/expert-pack.json")
    if not made:
        raise SystemExit("no expert pack was made for this run; python -m reframe.reconcile.expert pack <folder> first")
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9 ._-]{0,40}", name):
        raise SystemExit("--expert is a short name: letters, digits, spaces, dots, hyphens")
    items_by_id = {i["id"]: i for i in (items_for(folder)[0])}
    items = [items_by_id[i] for i in made["items"] if i in items_by_id]
    expert, problems = read_verdicts(sheet.read_text(errors="replace"), {i["id"] for i in items})
    if problems:
        raise SystemExit("verdicts.csv has problems, nothing was read:\n  " + "\n  ".join(problems[:20]))
    judged = {label: {"answers": (folder.load(f"{FOLDER}/judge-{label}.json") or {}).get("answers") or {}}
              for label in sorted({p.stem.removeprefix("judge-") for p in folder.path(FOLDER).glob("judge-*.json")})}
    finals = (folder.load(f"{FOLDER}/audit.json") or {}).get("final") or {}
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    result = {"expert": name, "read_at": iso(), "origin": made["origin"], **compare(items, expert, judged, finals)}
    folder.save(f"{FOLDER}/expert-{slug}.json", {"verdicts": expert, "figures": result})
    return result


def main(argv: list[str] | None = None) -> int:
    from reframe.core.commands import find_run
    parser = argparse.ArgumentParser(prog="python -m reframe.reconcile.expert", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="action", required=True)
    p = sub.add_parser("pack", help="write the blind pack for an expert into an empty folder")
    p.add_argument("folder")
    p.add_argument("--run")
    p.add_argument("--size", type=int, default=40, help="the sample size when the run has no audit sample (default 40)")
    p.add_argument("--seed", type=int, default=7, help="the seed when the run has no audit sample (default 7)")
    r = sub.add_parser("read", help="read an expert's verdicts.csv back")
    r.add_argument("verdicts")
    r.add_argument("--expert", required=True, help="the expert's name or initials, as the figures name them")
    r.add_argument("--run")
    args = parser.parse_args(argv)
    folder = find_run(args.run)
    if args.action == "pack":
        made = pack(folder, Path(args.folder).expanduser().resolve(), args.size, args.seed)
        print(f"Pack for an expert: {made['items']} rules from {made['origin']}, {made['defect_notes']} with a possible defect, in {made['path']}. "
              "Send the folder; they open index.html and fill in verdicts.csv.")
        for left in made["left"]:
            print(f"  check before sending: {left}")
        return 0
    result = read(folder, Path(args.verdicts).expanduser(), args.expert)
    rec = result["recommended"]
    print(f"{result['expert']}: of {rec['items']} recommended rules, {rec['correct']} correct, {rec['minor']} minor, {rec['wrong']} wrong, "
          f"{rec['unsure']} unsure" + (f" ({rec['correct_share']:.0%} correct)." if rec["correct_share"] is not None else "."))
    for label, a in result["agreement"].items():
        print(f"  agrees with {'the audit' if label == 'final' else 'judge ' + label} on {a['agreed']} of {a['of']}")
    for d in result["differs_from_final"]:
        print(f"  {d['id']} ({d['kind']}, {d['confidence'] or 'no'} confidence): the audit says {d['final']}, the expert {d['expert']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
