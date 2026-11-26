"""Pipeline 3, stage R7: the reconciliation page (docs/pipeline-3.md, section 4).

outputs/reconcile/index.html, in the review layout the other two reviews use (template.html), from pipeline 3's
results: the recommended rules with their decisions, the recommended requirements in AWS Transform's frame, and the SME
list. Each rule shows its decision, reason, confidence and evidence (the cited lines, read from the snapshot), the AWS
and Claude rules it came from side by side, and the context it used. Every requirement, rule and carried question can be
marked Agree, Needs change or Question, and the marks downloaded: the next round, or pipeline 4, reads them.
"""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path
from typing import Any

from reframe.core.runfolder import RunFolder, iso

TOOL = {"key": "reconciled", "name": "Reframe's reconciliation", "short": "Reframe", "generated": True,
        "generated_note": "Recommended by Reframe from both assessments: AWS Transform's and Claude's rules reconciled against the source code, "
                          "with requirements written from them. It is model output, for people to review."}
TOOL_ONE = {**TOOL, "generated_note": "Recommended by Reframe from Claude's assessment: every rule checked against the source code, with "
                                       "requirements written from the rules the code supports. It is model output, for people to review."}
EARS = {"ubiquitous": "Ubiquitous", "event-driven": "Event-driven", "state-driven": "State-driven", "unwanted behaviour": "Unwanted",
        "optional feature": "Optional", "complex": "Complex"}
EXCERPT_LINES = 40
PAGE = "outputs/reconcile/index.html"


def _excerpt(legacy: Path, cite: str) -> dict[str, Any] | None:
    from reframe.reconcile.decide import CITE
    m = CITE.match(str(cite).strip())
    if not m:
        return None
    path = (legacy / m["path"]).resolve()
    if not path.is_relative_to(legacy.resolve()) or not path.is_file():
        return None
    lines = path.read_text(errors="replace").splitlines()
    start, end = int(m["start"]), int(m["end"] or m["start"])
    shown = lines[start - 1:min(end, start - 1 + EXCERPT_LINES)]
    return {"path": m["path"], "start": start, "end": end, "lines": shown, "cut": end - start + 1 > len(shown)}


def collect_reconciled(folder: RunFolder) -> dict[str, Any]:
    from reframe.claude.workspace import paths
    from reframe.report.build import collect, collect_claude
    from reframe.report.compare import _links
    made = folder.load("outputs/reconcile/rules.json") or {}
    written = folder.load("outputs/reconcile/requirements.json") or {}
    sme = folder.load("reconcile/questions.json") or {}
    gathered = folder.load("reconcile/inputs/inputs.json") or {}
    state = folder.state
    rec = state.get("reconcile") or {}
    legacy = paths(folder)["legacy"]
    alone = state.get("tools") == "claude"  # a Claude-only run: Claude's frame, and no AWS review or comparison to link to
    aws_data, claude_data = collect(folder), collect_claude(folder)
    aws_links, claude_links = _links(aws_data, "../report/index.html"), _links(claude_data, "../claude/report/index.html")
    tech = {f["id"]: f.get("technical") for f in (claude_data if alone else aws_data)["functions"]}
    inputs = gathered.get("rules") or {}
    agreed = (gathered.get("context") or {}).get("agreed") or {}

    fn_id = lambda fid: "rec/" + (fid or "unassigned")  # noqa: E731
    rules = []
    evidence: dict[str, Any] = {}
    for r in made.get("rules") or []:
        for cite in list(r["evidence"]) + list(r.get("entry") or []) + list(r.get("defect_evidence") or []):
            if cite not in evidence:
                evidence[cite] = _excerpt(legacy, cite)
        originals = [{"tool": inputs[k]["tool"], "key": k, "id": inputs[k].get("id"), "name": inputs[k].get("name", ""), "text": inputs[k].get("text", ""),
                      "program": inputs[k].get("program", ""), "link": (aws_links if inputs[k]["tool"] == "aws" else claude_links).get(k)}
                     for k in r["covers"] if k in inputs]
        rules.append({"key": r["key"], "function": fn_id(r.get("function")), "id": f"{r['unit']} #{r['n']}", "name": r["name"], "text": r["text"],
                      "program": r["program"], "disposition": "captured", "reason": "", "requirements": [],
                      "confidence": r.get("confidence", ""), "decision": r["decision"], "why": r.get("reason", ""), "evidence": r["evidence"],
                      "originals": originals, "round": r.get("round"), "context": r.get("context") or [], "defect": r.get("defect") or "",
                      "changed": r.get("changed", False), "confidence_why": r.get("confidence_why", ""), "model_confidence": r.get("model_confidence", ""),
                      "reachable": r.get("reachable", ""), "entry": r.get("entry") or [], "depends": r.get("depends", ""), "unit": r["unit"], "n": r.get("n", 1),
                      "unit_rules": r.get("unit_rules", 1), "conflict": r.get("conflict", False), "kind": r.get("kind", ""),
                      "examples": r.get("examples") or [], "agreed_by": agreed.get(r["key"]) or [], "defect_call": r.get("defect_call", ""), "defect_evidence": r.get("defect_evidence") or []})
    rule_by_key = {r["key"]: r for r in rules}

    names = written.get("names") or {}
    domains, functions, capabilities, requirements, questions = [], [], [], [], []
    for d in written.get("domains") or []:
        domain = {"key": d["key"], "name": d["name"], "description": d.get("description", ""), "kind": d.get("kind", "business"), "functions": []}
        for fid in d["functions"]:
            body = (written.get("functions") or {}).get(fid) or {"capabilities": []}
            fid_page = fn_id(fid)
            cited: set[str] = set()
            entry = {"id": fid_page, "domain": d["key"], "name": (names.get(fid) or {}).get("name", fid), "description": (names.get(fid) or {}).get("description", ""),
                     "risk": body.get("risk", ""),
                     "capabilities": [], "notes": [], "summary": {}, "set_aside": [],
                     "technical": tech.get(fid) or {"programs": [], "jobs": [], "screens": [], "data_stores": []}}
            for cap in body["capabilities"]:
                cid = f"{fid_page}#{cap['number']}"
                capability = {"id": cid, "function": fid_page, "number": cap["number"], "title": cap["title"], "story": cap.get("story", ""),
                              "fields": {}, "other": "", "requirements": [], "questions": [], "risk": cap.get("risk", ""), "touches": cap.get("touches") or [],
                              "tables": [{**t, "rows": [{**row, "rule_id": rule_by_key[row["rule"]]["id"] if row["rule"] in rule_by_key else ""} for row in t["rows"]]}
                                         for t in cap.get("tables") or []]}
                for req in cap["requirements"]:
                    key = f"{fid_page}/{req['code']}"
                    keys = [k for k in req["rules"] if k in rule_by_key]
                    cited.update(keys)
                    for k in keys:
                        rule_by_key[k]["requirements"].append(req["code"])
                    requirements.append({"key": key, "code": req["code"], "kind": "N" if req["kind"] == "non-functional" else "F",
                                         "pattern": EARS.get(req.get("pattern", ""), req.get("pattern", "")), "text": req["text"], "capability": cid,
                                         "function": fid_page, "rules": keys, "programs": sorted({rule_by_key[k]["program"] for k in keys} - {""}),
                                         "agreed_by": agreed.get(key) or [], "kept": bool(req.get("agreed"))})
                    capability["requirements"].append(key)
                for q in cap["questions"]:
                    key = f"{fid_page}/{q['code']}"
                    questions.append({"key": key, "code": q["code"], "text": q["text"], "owner": "Subject-matter expert", "unverified": False,
                                      "capability": cid, "function": fid_page, "status": q.get("status", "open")})
                    capability["questions"].append(key)
                capabilities.append(capability)
                entry["capabilities"].append(cid)
            entry["other_rules"] = [r["key"] for r in rules if r["function"] == fid_page and r["key"] not in cited]
            functions.append(entry)
            domain["functions"].append(fid_page)
        domains.append(domain)

    decided = Counter(r["decision"] for r in rules)
    units = Counter()
    for d in (folder.load("reconcile/decisions.json", {}) or {}).values():
        units[d.get("decision")] += 1
    snapshot = folder.load("snapshot.json") or {}
    sme_list = [{k: q.get(k) for k in ("id", "kind", "call", "question", "owner", "status", "rules", "originals", "from", "evidence", "settled_by",
                                       "settled_answer", "answer", "answered_in")} for q in sme.get("questions") or []]
    for q in sme_list:
        q["holds_up"] = [{"key": k, "tool": inputs[k]["tool"], "name": inputs[k].get("name", ""), "program": inputs[k].get("program", ""),
                          "link": (aws_links if inputs[k]["tool"] == "aws" else claude_links).get(k)} for k in q["rules"] or [] if k in inputs][:20]
    return {
        "generated_at": iso(), "run": folder.root.name, "project": state.get("project"), "tool": TOOL_ONE if alone else TOOL,
        "source": {"form": snapshot.get("form"), "commit": snapshot.get("commit"), "files": snapshot.get("files"), "sha256": snapshot.get("sha256"),
                   "name": Path(str(snapshot.get("source") or "")).name or snapshot.get("source")},
        "started_at": rec.get("started_at"), "retrieved_at": rec.get("finished_at"),
        "domains": domains, "functions": functions, "capabilities": capabilities, "requirements": requirements, "rules": rules, "questions": questions,
        "data_model": "", "sections": [{"title": "How this was reconciled", "open": True, "html": _how_one(rec, written, sme) if alone else _how(rec, written, sme)}],
        "classification": [], "unclassified": [], "issues": [], "decisions": [], "links": {"pages": []},
        "reconcile": {"rules": dict(decided), "units": dict(units), "defect_calls": dict(Counter(d.get("defect_call") or "uncalled"
                      for d in (folder.load("reconcile/decisions.json", {}) or {}).values() if str(d.get("defect") or "").strip())), "confidence": dict(Counter(r["confidence"] for r in rules)), "kinds": dict(Counter(r["kind"] or "unclassed" for r in rules)),
                      "examples": sum(len(r["examples"]) for r in rules), "examples_removed": sum(r.get("examples_removed", 0) for r in made.get("rules") or []), "defects": rec.get("defects", 0), "round": rec.get("round"),
                      "rounds": dict(Counter(str(r["round"]) for r in rules)), "sme": sme.get("counts") or {}, "originals": sme.get("originals", 0),
                      "dropped": written.get("dropped", 0), "tables": written.get("tables", 0), "risk": written.get("risk") or {}},
        "evidence": {k: v for k, v in evidence.items() if v}, "sme": sme_list, "signoffs": _signoffs(rec.get("signoffs") or [], aws_data),
        "nav": [["Claude's review", "../claude/report/index.html"]] if alone else
               [["AWS Transform's review", "../report/index.html"], ["Claude's review", "../claude/report/index.html"],
                ["AWS Transform and Claude compared", "../comparison/index.html"]],
    }


def _signoffs(read: list[dict[str, Any]], aws_data: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Sign-offs read from the context folder, by the reconciled review's function id: one made on the reconciled review
    is on rec/<function>; one made on AWS Transform's review is on the same AWS function, so it shows here too. Claude's
    review has its own functions; those sign-offs show in reframe status only."""
    aws_ids = {f["id"] for f in aws_data.get("functions") or []}
    found: dict[str, list[dict[str, Any]]] = {}
    for x in read:
        fid = x["function"] if x["function"].startswith("rec/") else ("rec/" + x["function"]) if x["function"] in aws_ids else None
        if fid:
            found.setdefault(fid, []).append({"reviewer": x["reviewer"], "at": x["at"], "comment": x["comment"], "page": x["page"]})
    return found


def _how_one(rec: dict[str, Any], written: dict[str, Any], sme: dict[str, Any]) -> str:
    """The method on a Claude-only run (docs/release-1.md, section 2)."""
    i = rec.get("inputs") or {}
    return ("<p>This run used Claude's assessment only. Every rule Claude's plugin found was checked by a headless Claude step that read the "
            "source code: kept where the code supports it, rejected where it does not, and sent to a subject-matter expert where the code cannot "
            "settle it. Reframe checked every decision: the cited lines exist in the snapshot, and every input rule is covered. Requirements were "
            "then written from the recommended rules in Claude's frame of domains and functions; "
            f"{written.get('dropped', 0)} that cited no rule were dropped.</p><p>Inputs: {i.get('rules', 0)} rules, "
            f"{i.get('questions', 0)} open questions; context: {i.get('documents', 0)} documents, {i.get('marks', 0)} review marks, "
            f"{i.get('answers', 0)} answered questions. The SME list holds {sme.get('originals', 0)} original questions. Round {html.escape(str(rec.get('round', '')))}.</p>")


def _how(rec: dict[str, Any], written: dict[str, Any], sme: dict[str, Any]) -> str:
    i = rec.get("inputs") or {}
    return ("<p>Rules both tools describe the same way were agreed without an agent. Every other rule was decided by a headless Claude step that "
            "read the source code: overlapping and conflicting rules made into the rules the code supports, rules only one tool found kept or rejected, "
            "and what the code cannot settle sent to a subject-matter expert. Reframe checked every decision: the cited lines exist in the snapshot, and "
            "every input rule is covered. Requirements were then written from the recommended rules in AWS Transform's frame of domains and functions; "
            f"{written.get('dropped', 0)} that cited no rule were dropped.</p><p>Inputs: {i.get('rules', 0)} rules, {i.get('pairs', 0)} pairs, "
            f"{i.get('questions', 0)} open questions; context: {i.get('documents', 0)} documents, {i.get('marks', 0)} review marks, "
            f"{i.get('answers', 0)} answered questions. The SME list holds {sme.get('originals', 0)} original questions. Round {html.escape(str(rec.get('round', '')))}.</p>")


def build_reconciled(folder: RunFolder) -> Path:
    from reframe.report.build import TEMPLATE
    data = collect_reconciled(folder)
    target = folder.path(PAGE)
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    payload = json.dumps(data, default=str).replace("</", "<\\/")
    target.write_text(TEMPLATE.replace("/*DATA*/", payload).replace("{{title}}", html.escape(f"Reconciled review: {data['project'] or 'run'}")))
    target.chmod(0o600)
    folder.event("reconcile_page_built", rules=len(data["rules"]), requirements=len(data["requirements"]), questions=len(data["sme"]))
    return target
