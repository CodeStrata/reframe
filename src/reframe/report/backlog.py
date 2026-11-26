"""`reframe export --to jira | azure-devops`: the design's capabilities as a backlog to import (docs/sharing.md, section 8, S-13).

Built from the final specifications (pipeline 4), with the AI-DLC package's IDs, so a story, its requirements, rules and
acceptance criteria carry the same IDs as the package and the golden datasets. Each tool's own CSV import file:

- **Jira:** an Epic per business function and a Story per capability, linked by Issue ID and Parent.
- **Azure DevOps:** an Epic per domain, a Feature per business function and a User Story per capability, linked by the
  import's Title 1, Title 2 and Title 3 columns.

No credentials are needed: a person imports the file in the tool. Every cell is cleaned as `reframe publish` cleans its
copy, and if anything is left, nothing is written. It runs nothing and uses neither AWS nor Claude.
"""

from __future__ import annotations

import csv
import html
import io
from collections import defaultdict
from pathlib import Path
from typing import Any

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import RunFolder

TOOLS = {"jira": "Jira", "azure-devops": "Azure DevOps"}
JIRA_PRIORITY = {"high": "High", "medium": "Medium", "low": "Low"}
ADO_PRIORITY = {"high": "1", "medium": "2", "low": "3"}
STATUS = {"final": "Final: signed off; build to it as written.", "draft": "Draft: its function is not signed off; confirm it with the owner before building it."}


def default_path(folder: RunFolder, tool: str) -> Path:
    return folder.path(f"outputs/design/{folder.state.get('project') or 'run'}-{folder.root.name}-{tool}.csv")


def stories(folder: RunFolder) -> list[dict[str, Any]]:
    """The labelled specifications, with the package's IDs kept in design/package-ids.json, and each one's golden cases."""
    from reframe.design import golden, package
    raw = package.load_specs(folder)
    if not raw:
        raise Stop(Outcome.REFUSED, "this run has no final specifications yet; reframe design writes them, and the backlog is built from them")
    registry = package.ids(raw, folder.load(package.IDS, {}) or {})
    folder.save(package.IDS, registry)  # the same IDs the package uses, now and in later versions
    labelled = [package.label(s, registry) for s in raw]
    return [{**s, "golden": golden.dataset(s)["counts"]["cases"]} for s in labelled]


def _safe(text: Any) -> str:
    """A cell a spreadsheet will not run: a value starting =, +, - or @ gets a leading space."""
    value = str(text if text is not None else "")
    return " " + value if value[:1] in ("=", "+", "-", "@") else value


def _label(text: str) -> str:
    return "-".join("".join(c if c.isalnum() else " " for c in text.lower()).split())[:40]


def _criteria(s: dict[str, Any]) -> list[str]:
    rid = s["rule_ids"]
    return [f"{s['ac_ids'][x['id']]}: Given {x['given']} When {x['when']} Then {x['then']}"
            + (f" ({', '.join(rid.get(k, k) for k in x.get('rules') or [])})" if x.get("rules") else "") for x in s["acceptance"]]


def _parts(s: dict[str, Any]) -> dict[str, list[str]]:
    rid = s["rule_ids"]
    return {
        "Requirements": [f"{s['req_ids'][q['code']]}: {q['text']}" for q in s["requirements"]],
        "Business rules": [f"{rid[r['key']]} ({r['class']}): {r['text']}" for r in s["rules"]],
        "Open questions": [f"{q.get('id') or 'Question'}: {q['question']}" + (f" (owner: {q['owner']})" if q.get("owner") else "") for q in s["questions"]],
        "Traceability": [f"Capability {s['id']} in the AI-DLC package ({s['folder']}); run key {s['key']}.",
                         f"Runs as: {s['runs_as']}. Risk: {s.get('risk') or 'not set'}" + (f"; touches {', '.join(s['touches'])}" if s.get("touches") else "") + ".",
                         (f"Golden dataset: golden/{s['id']}.json, {s['golden']} cases." if s["golden"] else "No golden cases: its rules are design notes.")],
    }


def _jira_text(s: dict[str, Any]) -> str:
    out = [s.get("story") or s.get("summary") or s["title"], "", STATUS.get(s["status"], s["status"])]
    for title, lines in {**_parts(s), "Acceptance criteria": _criteria(s)}.items():
        if lines:
            out += ["", f"h3. {title}"] + [f"* {line}" for line in lines]
    return "\n".join(out)


def _ado_html(s: dict[str, Any]) -> str:
    out = [f"<p>{html.escape(s.get('story') or s.get('summary') or s['title'])}</p>", f"<p><b>{html.escape(STATUS.get(s['status'], s['status']))}</b></p>"]
    for title, lines in _parts(s).items():
        if lines:
            out.append(f"<h3>{html.escape(title)}</h3><ul>" + "".join(f"<li>{html.escape(line)}</li>" for line in lines) + "</ul>")
    return "".join(out)


def jira_rows(specs: list[dict[str, Any]]) -> list[list[str]]:
    by_function: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for s in specs:
        by_function[s["function"]].append(s)
    rows, n = [], 0
    for caps in by_function.values():
        n += 1
        epic = n
        first = caps[0]
        risks = [c.get("risk") for c in caps]
        risk = "high" if "high" in risks else "medium" if "medium" in risks else "low"
        rows.append([str(epic), "Epic", first["function_name"], first["function_name"],
                     f"{first['domain']}: {first['function_name']}. {len(caps)} capabilities, "
                     f"{sum(1 for c in caps if c['status'] == 'final')} final, from Reframe's design of the legacy system.",
                     "", "", JIRA_PRIORITY.get(risk, ""), "reframe", _label(first["domain"]), f"function-{first['code'].lower()}", ""])
        for s in caps:
            n += 1
            rows.append([str(n), "Story", f"{s['id']} {s['title']}", "", _jira_text(s), "\n".join(_criteria(s)), str(epic),
                         JIRA_PRIORITY.get(s.get("risk") or "", ""), "reframe", _label(s["domain"]), s["status"], f"risk-{s.get('risk') or 'none'}"])
    return rows


JIRA_COLUMNS = ["Issue ID", "Issue Type", "Summary", "Epic Name", "Description", "Acceptance Criteria", "Parent", "Priority", "Labels", "Labels", "Labels", "Labels"]
ADO_COLUMNS = ["ID", "Work Item Type", "Title 1", "Title 2", "Title 3", "Description", "Acceptance Criteria", "Priority", "Tags"]


def ado_rows(specs: list[dict[str, Any]]) -> list[list[str]]:
    rows: list[list[str]] = []
    domains: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for s in specs:
        domains[s["domain"]][s["function"]].append(s)
    for domain, functions in domains.items():
        rows.append(["", "Epic", domain, "", "", f"<p>{html.escape(domain)}: {len(functions)} business functions, from Reframe's design.</p>", "", "", "reframe"])
        for caps in functions.values():
            first = caps[0]
            rows.append(["", "Feature", "", first["function_name"], "", f"<p>{len(caps)} capabilities, {sum(1 for c in caps if c['status'] == 'final')} final.</p>",
                         "", "", f"reframe; function-{first['code'].lower()}"])
            for s in caps:
                criteria = "<ul>" + "".join(f"<li>{html.escape(c)}</li>" for c in _criteria(s)) + "</ul>" if s["acceptance"] else ""
                rows.append(["", "User Story", "", "", f"{s['id']} {s['title']}", _ado_html(s), criteria, ADO_PRIORITY.get(s.get("risk") or "", ""),
                             f"reframe; {s['status']}; risk-{s.get('risk') or 'none'}"])
    return rows


def export(folder: RunFolder, tool: str, target: Path | None = None) -> dict[str, Any]:
    from reframe.report.publish import Cleaner
    if tool not in TOOLS:
        raise Stop(Outcome.REFUSED, f"no backlog format {tool}; use jira or azure-devops")
    specs = stories(folder)
    columns, rows = (JIRA_COLUMNS, jira_rows(specs)) if tool == "jira" else (ADO_COLUMNS, ado_rows(specs))
    cleaner = Cleaner(folder)
    cleaned = [[_safe(cleaner.clean(cell)) for cell in row] for row in rows]
    left = sorted({what for row in cleaned for cell in row for what in cleaner.left(cell)})
    if left:
        raise Stop(Outcome.REFUSED, f"the backlog still holds {', '.join(left)} after cleaning; nothing was written")
    path = target or default_path(folder, tool)
    if path.is_dir() or path.suffix.lower() != ".csv":  # a folder, made if need be, gets the file's own name
        path = path / default_path(folder, tool).name
    path.parent.mkdir(parents=True, exist_ok=True)
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\r\n")
    writer.writerow(columns)
    writer.writerows(cleaned)
    path.write_text(out.getvalue(), encoding="utf-8")
    return {"path": path, "tool": TOOLS[tool], "counts": {
        "epics": len({s["domain"] for s in specs}) if tool == "azure-devops" else len({s["function"] for s in specs}),
        "features": len({s["function"] for s in specs}) if tool == "azure-devops" else 0,
        "stories": len(specs), "final": sum(1 for s in specs if s["status"] == "final"),
        "criteria": sum(len(s["acceptance"]) for s in specs), "requirements": sum(len(s["requirements"]) for s in specs)}}
