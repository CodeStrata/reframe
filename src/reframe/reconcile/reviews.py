"""Pipeline 3, part 2: several reviewers' files (docs/pipeline-3.md, section 8.11).

`reframe review --context <folder>` reads every review download in a folder, without running anything or copying
anything into the Claude workspace, and shows each reviewer's marks and coverage of the page they reviewed, their
sign-offs, and the items two reviewers marked differently. It writes reconcile/reviews.json. The next round of the
reconciliation combines the same files (inputs.combine): Needs change and Question take precedence over Agree, and each
comment is kept with its reviewer's name. A download made on a copy from `reframe publish` names items by cleaned keys;
both read it with the run's own keys (as_run_keys, P3-25).
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from reframe.core.runfolder import RunFolder, iso
from reframe.reconcile import inputs

PAGES = {"aws": "AWS Transform's review", "claude": "Claude's review", "reconciled": "the reconciled review"}


def page_of(tool: str) -> str:
    t = tool.lower()
    return "reconciled" if "reconcil" in t else "claude" if "claude" in t else "aws"


def _tools(folder: RunFolder) -> dict[str, dict[str, Any]]:
    """AWS Transform's and Claude's review pages' data; empty for a page the run cannot build."""
    from reframe.report.build import collect, collect_claude
    found: dict[str, dict[str, Any]] = {}
    for page, load in (("aws", lambda: collect(folder)), ("claude", lambda: collect_claude(folder))):
        try:
            found[page] = load()
        except (OSError, ValueError, KeyError, TypeError):
            found[page] = {}
    return found


def page_items(folder: RunFolder) -> dict[str, set[str]]:
    """The keys a reviewer can mark on each page: requirements, business rules and open questions."""
    return _items(folder, _tools(folder))


def _items(folder: RunFolder, tools: dict[str, dict[str, Any]]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for page, data in tools.items():
        found[page] = ({r["key"] for r in data.get("requirements") or []} | {r["key"] for r in data.get("rules") or [] if r.get("disposition", "captured") == "captured"}
                       | {q["key"] for q in data.get("questions") or []})
    made = (folder.load("outputs/reconcile/rules.json") or {}).get("rules") or []
    written = (folder.load("outputs/reconcile/requirements.json") or {}).get("functions") or {}
    keys = {r["key"] for r in made}
    for fid, body in written.items():
        page_fid = "rec/" + (fid or "unassigned")
        for cap in body.get("capabilities") or []:
            keys |= {f"{page_fid}/{r['code']}" for r in cap.get("requirements") or []} | {f"{page_fid}/{q['code']}" for q in cap.get("questions") or []}
            keys.add(f"{page_fid}#{cap['number']}")
    found["reconciled"] = keys
    return found


def run_keys(folder: RunFolder) -> dict[str, str]:
    """Every key a review download can name on any of the three pages (marked items, capabilities and the functions
    signed off), as a copy made by `reframe publish` names it -> the key the run uses; only the keys cleaning changes."""
    from reframe.report.publish import run_keys as cleaned
    tools = _tools(folder)
    keys = set().union(*_items(folder, tools).values())
    for data in tools.values():
        keys |= ({r["key"] for r in data.get("rules") or []} | {c["id"] for c in data.get("capabilities") or []}
                 | {f["id"] for f in data.get("functions") or []})
    written = (folder.load("outputs/reconcile/requirements.json") or {}).get("functions") or {}
    keys |= {"rec/" + f["id"] for f in tools["aws"].get("functions") or []} | {"rec/" + (fid or "unassigned") for fid in written}
    return cleaned(folder, keys)


def as_run_keys(folder: RunFolder, found: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Review downloads with their marks' keys and sign-offs' functions named as the run names them, so a review of a
    published copy reads like a review of the run's own page (section 8.11)."""
    aliases = run_keys(folder) if found else {}
    if not aliases:
        return found
    return [{**r, "marks": [{**m, "key": aliases.get(m["key"], m["key"])} for m in r["marks"]],
             "signoffs": [{**x, "function": aliases.get(x["function"], x["function"])} for x in r.get("signoffs") or []]} for r in found]


def read(folder: RunFolder, context: Path) -> dict[str, Any]:
    sha = (folder.load("snapshot.json") or {}).get("sha256")
    reviews, ignored = [], []
    for path in sorted(p for p in context.rglob("*") if p.is_file() and not p.name.startswith(".") and p.suffix.lower() in (".json", ".csv")):
        name = path.relative_to(context).as_posix()
        try:
            review = inputs.review_file(path, name)
        except (OSError, ValueError, KeyError, UnicodeDecodeError) as error:
            ignored.append({"file": name, "why": f"could not be read ({type(error).__name__})"})
            continue
        if review is None:
            continue
        if review.get("unusable"):
            ignored.append({"file": name, "why": review["unusable"]})
        elif review["sha256"] != sha:
            ignored.append({"file": name, "why": "a review of another snapshot"})
        else:
            reviews.append(review)
    return {"reviews": as_run_keys(folder, reviews), "ignored": ignored}


def summary(folder: RunFolder, context: Path) -> dict[str, Any]:
    """Each reviewer's coverage and sign-offs, and where reviewers disagree; written to reconcile/reviews.json."""
    got = read(folder, context)
    items = page_items(folder)
    reviewers = []
    for r in got["reviews"]:
        page = page_of(r["tool"])
        marked = {m["key"] for m in r["marks"]}
        total = len(items.get(page) or ())
        reviewers.append({"file": r["file"], "reviewer": r["reviewer"], "page": page, "format": r["format"],
                          "marks": dict(Counter(m["status"] for m in r["marks"])), "marked": len(marked),
                          "items": total, "coverage": round(len(marked & items.get(page, set())) / total, 3) if total else 0.0,
                          "signoffs": [{"function": x["function"], "name": x["name"], "at": x["at"]} for x in r.get("signoffs") or []]})
    combined = inputs.combine(got["reviews"])
    disagreements = [{"key": k, "marks": [{"reviewer": g["reviewer"], "status": g["status"], "comment": g["comment"], "file": g["file"]} for g in m["by"]],
                      "combined": m["status"]}
                     for k, m in sorted(combined.items()) if len({g["status"] for g in m["by"]}) > 1]
    value = {"read_at": iso(), "folder": str(context), "reviewers": reviewers, "disagreements": disagreements, "ignored": got["ignored"],
             "marks": len(combined)}
    folder.save("reconcile/reviews.json", value)
    return value
