"""`reframe export --to xlsx`: the reconciled results as one Excel workbook (docs/sharing.md, section 7, S-12).

Built from the same data as the reconciliation page (reconciled.collect_reconciled), so the workbook and the page always
agree, with the reviewers' marks from the review downloads in a context folder. Every cell is cleaned as `reframe publish`
cleans its copy; if anything is left, nothing is written. It runs nothing and uses neither AWS nor Claude.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import RunFolder, iso
from reframe.report import workbook

DECISION = {"agreed": "Agreed by both tools", "merged": "Merged from both tools", "aws": "AWS Transform was right", "claude": "Claude's plugin was right",
            "rewritten": "Rewritten from the code", "kept": "Kept: the code supports it", "rejected": "Rejected: the code does not support it",
            "needs_sme": "Waiting for an SME"}
KIND = {"business": "Business rule", "validation": "Validation", "compliance": "Compliance", "error_handling": "Error handling", "display": "Display",
        "technical": "Technical step", "side_effect": "Side effect", "leftover": "Leftover"}
TOUCH = {"money": "money", "card_data": "card data", "personal_data": "personal data", "security": "security", "audit": "audit",
         "updates_records": "record updates", "reporting_only": "reporting only"}
REACHED = {"yes": "Yes", "no": "No: the code never runs", "unknown": "Not shown by the source"}
MARK = {"agree": "Agree", "change": "Needs change", "question": "Question"}
TOOLS = {"aws": "AWS Transform", "claude": "Claude"}
REVIEW = ["Mark", "Reviewers' marks", "Key"]
NOT_READ_BACK = ("This workbook is for reading and planning; Reframe does not read it back. Answer the SME list in reconcile/questions.csv, "
                 "and mark items on the reconciliation page and download your review; reframe reconcile --context <folder> reads both.")


def default_path(folder: RunFolder) -> Path:
    return folder.path(f"outputs/reconcile/{folder.state.get('project') or 'run'}-{folder.root.name}-requirements.xlsx")


def marks(folder: RunFolder, context: Path | None, aliases: dict[str, str] | None = None) -> dict[str, Any]:
    """The reviewers' marks on the reconciled review in the context folder's downloads: combined by key, each reviewer's
    own, the sign-offs, and the files read or ignored. `aliases` maps a key as a published copy names it (cleaned) to the
    key the run uses, so marks downloaded from either page combine."""
    from reframe.reconcile import inputs, reviews
    if context is None:
        return {"combined": {}, "signoffs": [], "read": [], "ignored": []}
    aliases = aliases or {}
    got = reviews.read(folder, context)
    for r in got["reviews"]:
        r["marks"] = [{**m, "key": aliases.get(m["key"], m["key"])} for m in r["marks"]]
        r["signoffs"] = [{**x, "function": aliases.get(x["function"], x["function"])} for x in r.get("signoffs") or []]
    mine = [r for r in got["reviews"] if reviews.page_of(r["tool"]) == "reconciled"]
    ignored = got["ignored"] + [{"file": r["file"], "why": f"a review of {reviews.PAGES[reviews.page_of(r['tool'])]}, not the reconciled review"}
                                for r in got["reviews"] if r not in mine]
    return {"combined": inputs.combine(mine), "signoffs": inputs.signoffs(mine), "ignored": ignored,
            "read": [{"file": r["file"], "reviewer": r["reviewer"], "marks": len(r["marks"])} for r in mine]}


def _review(key: str, combined: dict[str, Any]) -> list[str]:
    m = combined.get(key)
    if not m:
        return ["", "", key]
    each = [f"{g['reviewer'] or 'A reviewer'}: {MARK.get(g['status'], g['status'])}" + (f" ({g['comment']})" if g["comment"].strip() else "")
            for g in m["by"]]
    return [MARK.get(m["status"], m["status"]), each, key]


def _example(x: dict[str, Any]) -> str:
    given = ", ".join(f"{g['field']} {g['value']}" for g in x.get("given") or [])
    return (f"Given {given}, then " if given else "Then ") + str(x.get("then", ""))


def sheets(data: dict[str, Any], review: dict[str, Any]) -> list[dict[str, Any]]:
    """The workbook's sheets from the reconciliation page's data and the reviewers' marks."""
    combined = review["combined"]
    domains = {d["key"]: d for d in data["domains"]}
    functions = {f["id"]: f for f in data["functions"]}
    capabilities = {c["id"]: c for c in data["capabilities"]}
    rules = {r["key"]: r for r in data["rules"]}
    domain_of = lambda fid: (domains.get((functions.get(fid) or {}).get("domain")) or {}).get("name", "")  # noqa: E731
    function_of = lambda fid: (functions.get(fid) or {}).get("name", "")  # noqa: E731
    capability_of = lambda cid: (f"{capabilities[cid]['number']}. {capabilities[cid]['title']}" if cid in capabilities else "")  # noqa: E731
    reqs_in = lambda fid: [r for r in data["requirements"] if r["function"] == fid]  # noqa: E731
    signed: dict[str, list[str]] = {}
    for x in review["signoffs"]:
        signed.setdefault(x["function"], []).append(f"{x['reviewer'] or 'A reviewer'}" + (f", {str(x['at'])[:10]}" if x.get("at") else "")
                                                     + (f" ({x['comment']})" if x.get("comment") else ""))
    for fid, given in (data.get("signoffs") or {}).items():  # read by the last round, from the context folder it used
        for x in given:
            line = f"{x['reviewer'] or 'A reviewer'}" + (f", {str(x['at'])[:10]}" if x.get("at") else "") + (f" ({x['comment']})" if x.get("comment") else "")
            if line not in signed.get(fid, []):
                signed.setdefault(fid, []).append(line)

    domain_rows = [[d["name"], d.get("kind", ""), d.get("description", ""), len(d["functions"]),
                    sum(len(reqs_in(fid)) for fid in d["functions"])] for d in data["domains"]]
    function_rows = [[domain_of(f["id"]), f["name"], f.get("description", ""), f.get("risk", ""), len(f["capabilities"]), len(reqs_in(f["id"])),
                      sum(1 for r in data["rules"] if r["function"] == f["id"]), signed.get(f["id"], []), f["id"]] for f in data["functions"]]
    capability_rows = [[domain_of(c["function"]), function_of(c["function"]), c["number"], c["title"], c.get("story", ""), c.get("risk", ""),
                        ", ".join(TOUCH.get(t, t) for t in c.get("touches") or []), len(c["requirements"]), len(c["questions"]), len(c.get("tables") or []),
                        *_review(c["id"], combined)] for c in data["capabilities"]]
    requirement_rows = []
    for q in data["requirements"]:
        behind = [rules[k] for k in q["rules"] if k in rules]
        lines = list(dict.fromkeys(e for r in behind for e in r["evidence"]))
        requirement_rows.append([domain_of(q["function"]), function_of(q["function"]), capability_of(q["capability"]), q["code"],
                                 "Non-functional" if q["kind"] == "N" else "Functional", q.get("pattern", ""), q["text"],
                                 [f"{r['id']}: {r['name']}" for r in behind], ", ".join(q.get("programs") or []), lines,
                                 "Yes" if q.get("kept") else "", *_review(q["key"], combined)])
    rule_rows = []
    order = {f["id"]: i for i, f in enumerate(data["functions"])}
    kinds = list(KIND)
    for r in sorted(data["rules"], key=lambda r: (order.get(r["function"], len(order)), kinds.index(r["kind"]) if r.get("kind") in kinds else len(kinds))):
        reached = REACHED.get(r.get("reachable", ""), r.get("reachable", ""))
        rule_rows.append([domain_of(r["function"]), function_of(r["function"]), r["id"], r["name"], r["text"], KIND.get(r.get("kind", ""), r.get("kind", "")),
                          DECISION.get(r["decision"], r["decision"]), r.get("why", ""), r.get("confidence", ""), r.get("confidence_why", ""), r["program"],
                          r["evidence"], reached, r.get("entry") or [], r.get("depends", ""), [_example(x) for x in r.get("examples") or []],
                          ", ".join(r.get("requirements") or []),
                          (("Looks deliberate: " if r.get("defect_call") == "deliberate" else "Looks unintended: " if r.get("defect_call") else "") + r["defect"])
                          if r.get("defect") else "",
                          [f"{TOOLS.get(o['tool'], o['tool'])} {o.get('id') or ''}: {o.get('name') or o.get('text', '')}".replace("  ", " ") for o in r.get("originals") or []],
                          r.get("round", ""), [f"{a.get('reviewer') or 'A reviewer'}" + (f", {str(a.get('at'))[:10]}" if a.get("at") else "") for a in r.get("agreed_by") or []],
                          *_review(r["key"], combined)])
    table_rows = []
    for c in data["capabilities"]:
        for t in c.get("tables") or []:
            conditions = t.get("conditions") or []
            for row in t.get("rows") or []:
                rule = rules.get(row.get("rule", ""))
                table_rows.append([domain_of(c["function"]), function_of(c["function"]), capability_of(c["id"]), t.get("title", ""), "Rule",
                                   "; ".join(f"{k} = {v}" for k, v in zip(conditions, row.get("values") or [])), t.get("outcome", ""), row.get("outcome", ""),
                                   f"{rule['id']}: {rule['name']}" if rule else row.get("rule_id", "")])
            for gap in t.get("gaps") or []:
                table_rows.append([domain_of(c["function"]), function_of(c["function"]), capability_of(c["id"]), t.get("title", ""), "Gap",
                                   "; ".join(f"{k} = {v}" for k, v in zip(conditions, gap.get("values") or [])), t.get("outcome", ""), gap.get("note", ""), ""])
    question_rows = [[domain_of(q["function"]), function_of(q["function"]), capability_of(q["capability"]), q["code"], q["text"], q.get("status", ""),
                      *_review(q["key"], combined)] for q in data["questions"]]
    sme_rows = [[q.get("id", ""), q.get("kind", ""), q.get("call", ""), q.get("question", ""), q.get("owner", ""), q.get("status", ""),
                 q.get("answer") or q.get("settled_answer") or "", q.get("settled_by") or q.get("answered_in") or "", q.get("from") or [], q.get("evidence") or []]
                for q in data.get("sme") or []]

    rec, source = data.get("reconcile") or {}, data.get("source") or {}
    about = [["What this is", "Recommended by Reframe from both assessments: AWS Transform's and Claude's rules reconciled against the source code, with "
                              "requirements written from them. It is model output, for people to review."],
             ["Project", data.get("project") or ""], ["Run", data.get("run") or ""],
             ["Source", source.get("name") or ""], ["Commit", source.get("commit") or ""], ["Source SHA-256", source.get("sha256") or ""],
             ["Reconciliation round", rec.get("round", "")], ["Reconciled", data.get("retrieved_at") or ""], ["Written", data.get("generated_at") or ""],
             ["Domains", len(data["domains"])], ["Business functions", len(data["functions"])], ["Capabilities", len(data["capabilities"])],
             ["Requirements", len(data["requirements"])], ["Business rules", len(data["rules"])], ["Decision table rows and gaps", len(table_rows)],
             ["Open questions", len(data["questions"])], ["SME list", len(sme_rows)],
             ["Review downloads read", [f"{r['file']}: {r['reviewer'] or 'no name'}, {r['marks']} marks" for r in review["read"]] or "none"],
             ["Review downloads ignored", [f"{i['file']}: {i['why']}" for i in review["ignored"]] or "none"],
             ["Marks", "Mark combines every reviewer's marks as the next round does: Needs change, then Question, then Agree. Reviewers' marks lists each one."],
             ["Read back", NOT_READ_BACK]]
    wide = {"Requirement": 70, "Rule": 70, "Question": 70, "User story": 60, "Description": 60, "Value": 100, "Reason": 50, "Why this confidence": 50}
    return [
        {"name": "About", "headers": ["Item", "Value"], "rows": about, "widths": {"Item": 28, "Value": 100}},
        {"name": "Domains", "headers": ["Domain", "Kind", "Description", "Business functions", "Requirements"], "rows": domain_rows, "widths": wide},
        {"name": "Business functions", "headers": ["Domain", "Business function", "Description", "Risk", "Capabilities", "Requirements", "Business rules",
                                                   "Signed off by", "Key"], "rows": function_rows, "widths": wide},
        {"name": "Capabilities", "headers": ["Domain", "Business function", "Number", "Capability", "User story", "Risk", "Touches", "Requirements",
                                             "Open questions", "Decision tables", *REVIEW], "rows": capability_rows, "widths": wide},
        {"name": "Requirements", "headers": ["Domain", "Business function", "Capability", "ID", "Type", "Pattern", "Requirement", "Business rules",
                                             "Programs", "Source lines", "Kept from a review", *REVIEW], "rows": requirement_rows, "widths": wide},
        {"name": "Business rules", "headers": ["Domain", "Business function", "ID", "Name", "Rule", "Kind", "Decision", "Reason", "Confidence",
                                               "Why this confidence", "Program", "Source lines", "Code runs", "Reached from", "Depends on", "Examples",
                                               "Requirements", "Possible defect", "From", "Round", "Agreed by", *REVIEW], "rows": rule_rows, "widths": wide},
        {"name": "Decision tables", "headers": ["Domain", "Business function", "Capability", "Table", "Row", "Conditions", "Outcome of", "Outcome",
                                                "Business rule"], "rows": table_rows, "widths": wide},
        {"name": "Open questions", "headers": ["Domain", "Business function", "Capability", "ID", "Question", "Status", *REVIEW],
         "rows": question_rows, "widths": wide},
        {"name": "SME list", "headers": ["ID", "Kind", "Defect call", "Question", "Owner", "Status", "Answer", "Settled by", "From", "Evidence"],
         "rows": sme_rows, "widths": wide},
    ]


def export(folder: RunFolder, target: Path | None = None, context: Path | None = None) -> dict[str, Any]:
    """Write the workbook; returns where, and the counts. Refuses if the reconciliation is not done, or if a cell still
    holds an identifier after cleaning (nothing is written)."""
    from reframe.report.publish import Cleaner
    from reframe.report.reconciled import collect_reconciled
    rec = folder.state.get("reconcile") or {}
    if rec.get("status") != "DONE" or not folder.exists("outputs/reconcile/requirements.json"):
        raise Stop(Outcome.REFUSED, "this run has no finished reconciliation to export; reframe reconcile makes it")
    data = collect_reconciled(folder)
    cleaner = Cleaner(folder)
    # a download from a published copy names items by their cleaned keys (an AWS Transform ID becomes a stand-in)
    keys = ([x["key"] for part in ("requirements", "rules", "questions") for x in data[part]] + [c["id"] for c in data["capabilities"]]
            + [f["id"] for f in data["functions"]])
    review = marks(folder, context, {cleaner.clean(k): k for k in keys if cleaner.clean(k) != k})
    found = sheets(data, review)
    left = []
    for s in found:
        cleaned_rows = []
        for n, row in enumerate(s["rows"], start=2):
            cells = [v if isinstance(v, int) else cleaner.clean(workbook.text(v)) for v in row]
            for v in cells:
                if not isinstance(v, int) and (what := cleaner.left(v)):
                    left.append(f"{s['name']} row {n}: {', '.join(what)}")
                    break
            cleaned_rows.append(cells)
        s["rows"] = cleaned_rows
    if left:
        raise Stop(Outcome.REFUSED, "the workbook would still hold identifiers after cleaning, so nothing was written: " + "; ".join(left[:5])
                   + (f"; and {len(left) - 5} more" if len(left) > 5 else ""))
    path = target or default_path(folder)
    if path.is_dir() or path.suffix.lower() != ".xlsx":  # a folder, existing or not, gets the default file name
        path = path / default_path(folder).name
    workbook.write(path, found, title=f"Reframe: {data.get('project') or 'run'} requirements, run {folder.root.name}", active="Requirements")
    path.chmod(0o600)
    counts = {s["name"]: len(s["rows"]) for s in found if s["name"] != "About"}
    folder.event("exported", to="xlsx", path=str(path), marks=len(review["combined"]), **{k.lower().replace(" ", "_"): v for k, v in counts.items()})
    return {"path": path, "counts": counts, "read": review["read"], "ignored": review["ignored"], "marks": len(review["combined"]), "at": iso()}
