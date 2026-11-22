"""Stage 8: one self-contained HTML report of the run's results (specification section 4, stage 8).

outputs/report/index.html, with its data inline and no network needed to view it. It is written for business users and
functional subject-matter experts first: an overview, then each business domain, each business function, each
capability, and each requirement with the business rules behind it. Every requirement, rule and open question can be
marked Agree, Needs change or Question, and a reviewer downloads their marks. Technical detail has its own section.
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

from reframe.core.runfolder import RunFolder, iso
from reframe.transform import documents
from reframe.transform.traceability import load as load_traceability

UNASSIGNED = {"key": "unassigned", "name": "Programs not in a business function", "kind": "unassigned",
              "description": "Programs AWS Transform assessed that it did not place in any business function."}


# ---- reading AWS's files -------------------------------------------------------------------------


def _yaml(path: Path) -> Any:
    try:
        return yaml.safe_load(path.read_text(errors="replace")) if path.exists() else None
    except yaml.YAMLError:
        return None


def _json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(errors="replace")) if path.exists() else None
    except ValueError:
        return None


def _rules(trace: dict[str, Any], fid: str) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    """The function's rules, and for each requirement code the keys of the rules that back it."""
    rules, backing = [], {}
    for item in trace.get("requirements") or []:
        if isinstance(item, dict) and item.get("req_id"):
            backing.setdefault(str(item["req_id"]), []).extend(f"{fid}/{r}" for r in item.get("rule_ids") or [])
    for rule in trace.get("rules") or []:
        if not isinstance(rule, dict) or not rule.get("rule_id"):
            continue
        key = f"{fid}/{rule['rule_id']}"
        req_ids = rule.get("req_ids") or []
        if isinstance(req_ids, str):
            req_ids = re.findall(r"REQ-[A-Z]+-\d+", req_ids)
        for code in req_ids:
            if key not in backing.setdefault(str(code), []):
                backing[str(code)].append(key)
        rules.append({"key": key, "function": fid, "id": str(rule["rule_id"]), "name": str(rule.get("rule_name") or ""),
                      "text": str(rule.get("rule_text") or ""), "program": str(rule.get("program") or ""),
                      "disposition": str(rule.get("disposition") or ""), "reason": str(rule.get("reason") or ""),
                      "requirements": [str(c) for c in req_ids]})
    return rules, backing


def collect(folder: RunFolder) -> dict[str, Any]:
    outputs = folder.path("outputs")
    spec = outputs / "requirements" / "spec"
    if not spec.is_dir():
        spec = outputs / "requirements"
    catalog = documents.catalog(outputs)
    domains: dict[str, dict[str, Any]] = {}
    functions, capabilities, requirements, rules, questions = [], [], [], [], []
    for document in sorted(spec.rglob("requirements.md")):
        parts = document.parent.relative_to(spec).parts
        if not parts:
            continue
        fid = "/".join(parts)
        parsed = documents.parse(document.read_text(errors="replace"))
        listed = catalog["functions"].get(documents.squeeze(parts[-1]))
        if len(parts) == 1:
            domain = dict(UNASSIGNED)
        else:
            known = catalog["domains"].get(documents.squeeze(parts[0])) or (
                catalog["domains"].get(documents.squeeze(listed["domain"])) if listed else None)
            name = known["name"] if known else documents.spaced(parts[0])
            domain = {"key": documents.squeeze(name), "name": name, "description": known["description"] if known else "",
                      "kind": "technical" if documents.squeeze(name) == "technical" else "business"}
        domain = domains.setdefault(domain["key"], {**domain, "functions": []})
        domain["functions"].append(fid)

        trace_file = document.parent / "traceability.yaml"
        trace = load_traceability(trace_file) if trace_file.exists() else {}  # a function may come without one
        function_rules, backing = _rules(trace, fid)
        rules += function_rules
        rule_programs = {r["key"]: r["program"] for r in function_rules}
        used: set[str] = set()
        function = {"id": fid, "domain": domain["key"], "name": listed["name"] if listed else (parsed["title"] or documents.spaced(parts[-1])),
                    "description": listed["description"] if listed else "", "capabilities": [],
                    "notes": [{"heading": n["heading"], "html": render_markdown(n["markdown"]), "technical": n["technical"]} for n in parsed["notes"]],
                    "summary": trace.get("summary") or {}}
        for found in parsed["capabilities"]:
            cid = f"{fid}#{found['number']}"
            capability = {"id": cid, "function": fid, "number": found["number"], "title": found["title"], "story": found["story"],
                          "fields": found["fields"], "other": render_markdown(found["other"]) if found["other"] else "",
                          "requirements": [], "questions": []}
            for item in found["requirements"]:
                key = f"{fid}/{item['code']}"
                backed = backing.get(item["code"], [])
                used.update(backed)
                requirements.append({"key": key, "code": item["code"], "kind": item["kind"], "pattern": item["pattern"], "text": item["text"],
                                     "capability": cid, "function": fid, "rules": backed,
                                     "programs": sorted({rule_programs.get(r, "") for r in backed} - {""})})
                capability["requirements"].append(key)
            for item in found["questions"]:
                key = f"{fid}/{item['code']}"
                questions.append({"key": key, "code": item["code"], "text": item["text"], "owner": item["owner"],
                                  "unverified": item["unverified"], "capability": cid, "function": fid})
                capability["questions"].append(key)
            capabilities.append(capability)
            function["capabilities"].append(cid)
        function["other_rules"] = [r["key"] for r in function_rules if r["disposition"] == "captured" and r["key"] not in used]
        function["set_aside"] = [r["key"] for r in function_rules if r["disposition"] != "captured" and r["key"] not in used]
        discovery = document.parent / "discovery"
        programs = (_yaml(discovery / "programs.yaml") or {}).get("programs") or []
        jobs = (_yaml(discovery / "batch-jobs.yaml") or {}).get("jobs") or {}
        screens = (_yaml(discovery / "screens.yaml") or {}).get("screens") or []
        stores = (_yaml(discovery / "data-stores.yaml") or {}).get("data_stores") or []
        job_list = [j for group in (jobs.values() if isinstance(jobs, dict) else [jobs]) for j in (group or []) if isinstance(j, dict)]
        function["technical"] = {"programs": [{"name": p.get("name"), "type": p.get("type"), "execution": p.get("execution")}
                                              for p in programs if isinstance(p, dict)],
                                 "jobs": [j.get("name") for j in job_list], "screens": [s.get("name") for s in screens if isinstance(s, dict)],
                                 "data_stores": [s.get("name") for s in stores if isinstance(s, dict)]}
        functions.append(function)

    order = {**{key: i for i, key in enumerate(catalog["domains"])}}
    ranked = sorted(domains.values(), key=lambda d: ({"business": 0, "technical": 1, "unassigned": 2}[d["kind"]], order.get(d["key"], 99), d["name"]))
    data_model = spec / "data-model.md"
    results = outputs / "aws" / "results"
    classification = next((_json(p) for p in sorted(results.glob("classification_*.json"))), None) or []
    issues = next((_json(p) for p in sorted(results.glob("codebase_issues_*.json"))), None) or []
    state = folder.state
    snapshot = folder.load("snapshot.json") or {}
    return {
        "generated_at": iso(),
        "run": folder.root.name,
        "project": state.get("project"),
        "source": {"form": snapshot.get("form"), "commit": snapshot.get("commit"), "files": snapshot.get("files"),
                   "sha256": snapshot.get("sha256"), "name": Path(str(snapshot.get("source") or "")).name or snapshot.get("source")},
        "started_at": state.get("started_at"), "retrieved_at": state.get("retrieved_at"),
        "graph": (state.get("graph") or {}).get("kind"),
        "domains": ranked, "functions": functions, "capabilities": capabilities,
        "requirements": requirements, "rules": rules, "questions": questions,
        "data_model": render_markdown(data_model.read_text(errors="replace")) if data_model.exists() else "",
        "classification": Counter(str(item.get("fileType") or "Unknown") for item in classification if isinstance(item, dict)).most_common(),
        "unclassified": [{"path": i.get("path"), "reason": i.get("reason")} for i in classification
                         if isinstance(i, dict) and str(i.get("fileType")) == "Unknown"][:500],
        "issues": [{"severity": (i.get("item") or {}).get("severity"), "name": (i.get("item") or {}).get("name"),
                    "description": (i.get("item") or {}).get("description"), "action": (i.get("item") or {}).get("action"),
                    "count": len(i.get("occurrences") or i.get("files") or []) or None}
                   for i in issues if isinstance(i, dict)],
        "decisions": folder.load("decisions.json", []),
        "links": {"coverage": _link(outputs / "requirements" / "spec" / "coverage-summary" / "coverage-report.html", outputs),
                  "catalog": _link(outputs / "catalog" / "index.html", outputs)},
    }


def _link(path: Path, outputs: Path) -> str | None:
    return "../" + path.relative_to(outputs).as_posix() if path.exists() else None


# ---- a small Markdown renderer for AWS's documents -------------------------------------------------


def _inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", text)
    return text


def render_markdown(text: str) -> str:
    out, paragraph, listing, table = [], [], None, []

    def flush():
        nonlocal paragraph, listing, table
        if paragraph:
            out.append("<p>" + _inline(" ".join(paragraph)) + "</p>")
            paragraph = []
        if listing:
            out.append(f"<{listing[0]}>" + "".join(f"<li>{_inline(item)}</li>" for item in listing[1]) + f"</{listing[0]}>")
            listing = None
        if table:
            rows = [r for r in table if not re.fullmatch(r"\|?[\s:|-]+\|?", r)]
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            if cells:
                head, body = cells[0], cells[1:]
                out.append("<div class='scroll'><table><thead><tr>" + "".join(f"<th>{_inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
                           + "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in row) + "</tr>" for row in body) + "</tbody></table></div>")
            table = []

    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.strip()
        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            flush()
            level = min(len(heading.group(1)) + 1, 6)
            out.append(f"<h{level}>{_inline(heading.group(2))}</h{level}>")
        elif stripped.startswith("|"):
            if paragraph or listing:
                saved = table
                table = []
                flush()
                table = saved
            table.append(stripped)
        elif re.match(r"^[-*]\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            if table or paragraph:
                flush()
            kind = "ol" if stripped[0].isdigit() else "ul"
            if listing is None or listing[0] != kind:
                flush()
                listing = (kind, [])
            listing[1].append(re.sub(r"^([-*]|\d+\.)\s+", "", stripped))
        elif not stripped:
            flush()
        else:
            if table or listing:
                flush()
            paragraph.append(stripped)
    flush()
    return "\n".join(out)


# ---- the page ------------------------------------------------------------------------------------


def build(folder: RunFolder) -> Path:
    data = collect(folder)
    target = folder.path("outputs/report/index.html")
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    payload = json.dumps(data, default=str).replace("</", "<\\/")
    page = TEMPLATE.replace("/*DATA*/", payload).replace("{{title}}", html.escape(f"Business review: {data['project'] or 'run'}"))
    target.write_text(page)
    target.chmod(0o600)
    folder.update(report="outputs/report/index.html")
    folder.event("report_built", functions=len(data["functions"]), requirements=len(data["requirements"]),
                 rules=sum(r["disposition"] == "captured" for r in data["rules"]), questions=len(data["questions"]))
    return target


TEMPLATE = (Path(__file__).with_name("template.html")).read_text() if (Path(__file__).with_name("template.html")).exists() else ""
