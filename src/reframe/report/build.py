"""Stage 8: one self-contained HTML report of the run's results (specification section 4, stage 8).

outputs/report/index.html, with its data inline and no network needed to view it:
overview, business domains and functions, every requirement in one searchable table, the business rules
from each function's traceability file, AWS's open questions, the data model, the assessment, links to
AWS's own coverage report and catalog, and Reframe's decisions.
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
from reframe.transform.traceability import load as load_traceability

REQUIREMENT_LINE = re.compile(r"^(REQ-([A-Z]+)-\d+):\s*(?:\[([^\]]+)\]\s*)?(.*)$")
SECTION = re.compile(r"^##\s+(?:\d+\.\s+)?(.+?)\s*$")


# ---- reading AWS's files -------------------------------------------------------------------------


def parse_requirements(text: str) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Requirements (id, type, pattern, text, capability) and open questions (capability, text) from one requirements.md."""
    requirements, questions = [], []
    capability, sub = "", ""
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("## "):
            match = SECTION.match(line)
            capability, sub = (match.group(1) if match else line[3:]), ""
            continue
        if line.startswith("### "):
            sub = line[4:].strip()
            continue
        match = REQUIREMENT_LINE.match(line)
        if match:
            requirements.append({"id": match.group(1), "type": match.group(2), "pattern": match.group(3) or "",
                                 "text": match.group(4), "capability": capability})
        elif sub.casefold() == "open questions" and line.startswith(("-", "*")) or (sub.casefold() == "open questions" and re.match(r"^\d+\.", line)):
            questions.append({"capability": capability, "text": re.sub(r"^([-*]|\d+\.)\s*", "", line)})
    return requirements, questions


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


def collect(folder: RunFolder) -> dict[str, Any]:
    outputs = folder.path("outputs")
    spec = outputs / "requirements" / "spec"
    if not spec.is_dir():
        spec = outputs / "requirements"
    functions, requirements, rules, questions = [], [], [], []
    for document in sorted(spec.rglob("requirements.md")):
        parts = document.parent.relative_to(spec).parts
        domain = parts[0] if len(parts) > 1 else "(none)"
        function = parts[-1] if parts else document.parent.name
        reqs, opens = parse_requirements(document.read_text(errors="replace"))
        trace = load_traceability(document.parent / "traceability.yaml")
        discovery = document.parent / "discovery"
        programs = (_yaml(discovery / "programs.yaml") or {}).get("programs") or []
        jobs = (_yaml(discovery / "batch-jobs.yaml") or {}).get("jobs") or {}
        screens = (_yaml(discovery / "screens.yaml") or {}).get("screens") or []
        stores = (_yaml(discovery / "data-stores.yaml") or {}).get("data_stores") or []
        backing: dict[str, list[str]] = {}
        for item in trace.get("requirements") or []:
            if isinstance(item, dict):
                backing[str(item.get("req_id"))] = [str(r) for r in item.get("rule_ids") or []]
        rule_programs = {}
        for rule in trace.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            rule_programs[str(rule.get("rule_id"))] = str(rule.get("program") or "")
            req_ids = rule.get("req_ids")
            if isinstance(req_ids, str):
                req_ids = re.findall(r"REQ-[A-Z]+-\d+", req_ids)
            rules.append({"domain": domain, "function": function, "id": str(rule.get("rule_id") or ""), "program": str(rule.get("program") or ""),
                          "name": str(rule.get("rule_name") or ""), "text": str(rule.get("rule_text") or rule.get("reason") or ""),
                          "disposition": str(rule.get("disposition") or ""), "requirements": list(req_ids or [])})
        for req in reqs:
            req.update(domain=domain, function=function,
                       programs=sorted({rule_programs.get(r, "") for r in backing.get(req["id"], [])} - {""}))
        requirements += reqs
        questions += [{**q, "domain": domain, "function": function} for q in opens]
        job_list = [j for group in (jobs.values() if isinstance(jobs, dict) else [jobs]) for j in (group or []) if isinstance(j, dict)]
        functions.append({"domain": domain, "function": function, "summary": trace.get("summary") or {},
                          "requirements": len(reqs), "open_questions": len(opens),
                          "programs": [{"name": p.get("name"), "type": p.get("type"), "execution": p.get("execution")} for p in programs if isinstance(p, dict)],
                          "jobs": [j.get("name") for j in job_list], "screens": [s.get("name") for s in screens if isinstance(s, dict)],
                          "data_stores": [s.get("name") for s in stores if isinstance(s, dict)],
                          "markdown": render_markdown(document.read_text(errors="replace"))})
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
        "functions": functions, "requirements": requirements, "rules": rules, "questions": questions,
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
    page = TEMPLATE.replace("/*DATA*/", payload).replace("{{title}}", html.escape(f"Reframe report: {data['project'] or 'run'} {data['run']}"))
    target.write_text(page)
    target.chmod(0o600)
    folder.update(report="outputs/report/index.html")
    folder.event("report_built", functions=len(data["functions"]), requirements=len(data["requirements"]), rules=len(data["rules"]))
    return target


TEMPLATE = (Path(__file__).with_name("template.html")).read_text() if (Path(__file__).with_name("template.html")).exists() else ""
