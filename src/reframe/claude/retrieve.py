"""Stage C5: read what the code-modernization plugin wrote, as it wrote it (docs/pipeline-2.md, section 4).

The plugin's files stay in claude/analysis/<project>/. This module reads them into one model (outputs/claude/model.json):
the preflight answers, the assessment's sections, the map (domains, modules, jobs, screens, data stores, edges, entry
points, flows), the rule cards and the data objects. Rule cards are read from BUSINESS_RULES.md, whose headings the
plugin fixes as `### RULE-NNN: <name>`, with fields `**Category:**`, `**Priority:**`, `**Source:**` and so on.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from reframe.core.runfolder import RunFolder, iso

RULE = re.compile(r"^###\s+(RULE-\d+):\s*(.+?)\s*$", re.M)
FIELD = re.compile(r"^\*\*([^*:]+):\*\*\s*(.*)$")
SOURCE = re.compile(r"`?([^`\s:]+(?:\.[A-Za-z0-9]+)?|[^`\s:]+):(\d+)(?:-(\d+))?`?")
SME_LINE = re.compile(r"^\s*[-*]\s*\*{0,2}(RULE-\d+)\*{0,2}\s*(?:\(([^)]*)\))?\s*[:\u2014-]\s*(.+)$")
GWT = re.compile(r"^\s*(Given|When|Then|And)\b\s*(.*)$", re.I)


def sections(markdown: str, level: int = 2) -> list[dict[str, str]]:
    """Split Markdown at headings of one level: [{"title", "markdown"}], the text before the first heading under ""."""
    marker = re.compile(rf"^{'#' * level}\s+(.+?)\s*$", re.M)
    out, last, title = [], 0, ""
    for match in marker.finditer(markdown):
        body = markdown[last:match.start()].strip()
        if body or title:
            out.append({"title": title, "markdown": body})
        title, last = match.group(1).strip(), match.end()
    body = markdown[last:].strip()
    if body or title:
        out.append({"title": title, "markdown": body})
    return out


def program_of(path: str) -> str:
    """The program name a source path stands for: the file's stem, upper-cased (COBOL member names)."""
    stem = Path(path).name.split(".")[0]
    return stem.upper()


def parse_rules(markdown: str) -> list[dict[str, Any]]:
    cards = []
    matches = list(RULE.finditer(markdown))
    for i, match in enumerate(matches):
        body = markdown[match.end(): matches[i + 1].start() if i + 1 < len(matches) else len(markdown)]
        body = re.split(r"^#{1,2}\s", body, maxsplit=1, flags=re.M)[0]  # stop at the next section (## …)
        fields: dict[str, str] = {}
        current = None
        spec: list[tuple[str, str]] = []
        for raw in body.splitlines():
            line = raw.rstrip()
            found = FIELD.match(line.strip())
            if found:
                current = found.group(1).strip().casefold()
                fields[current] = found.group(2).strip()
                continue
            clause = GWT.match(line)
            if current == "specification" and clause:
                spec.append((clause.group(1).capitalize(), clause.group(2).strip()))
                continue
            if current and line.strip() and not line.strip().startswith("---"):
                fields[current] = (fields[current] + " " + line.strip()).strip()
        source = fields.get("source", "")
        where = SOURCE.search(source)
        path = where.group(1) if where else source.strip("` ")
        confidence = fields.get("confidence", "")
        level = confidence.split("—")[0].split("-")[0].split(" ")[0].strip() if confidence else ""
        cards.append({
            "id": match.group(1), "name": match.group(2).strip(), "category": fields.get("category", ""),
            "priority": fields.get("priority", "").split(" ")[0], "source": source.strip("` "), "path": path,
            "line": int(where.group(2)) if where else None, "line_end": int(where.group(3)) if where and where.group(3) else None,
            "program": program_of(path) if path else "", "plain": fields.get("plain english", ""),
            "spec": [{"clause": c, "text": t} for c, t in spec], "parameters": fields.get("parameters", ""),
            "edge_cases": fields.get("edge cases handled", ""), "defect": fields.get("suspected defect", ""),
            "confidence": level, "confidence_note": confidence[len(level):].strip(" —-") if confidence else ""})
    return cards


def sme_questions(markdown: str, cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The closing "Rules requiring SME confirmation" section, one question per rule; else each card below High confidence."""
    known = {c["id"]: c for c in cards}
    section = next((s["markdown"] for s in sections(markdown, 2) if "sme" in s["title"].casefold()), "")
    questions = []
    for line in section.splitlines():
        found = re.search(r"(RULE-\d+)", line)
        if not found or found.group(1) not in known:
            continue
        bullet = SME_LINE.match(line)
        if bullet:  # - **RULE-003** (Medium): the question
            questions.append({"rule": found.group(1), "text": bullet.group(3).strip(), "confidence": (bullet.group(2) or "").strip()})
            continue
        cells = [c.strip(" *`") for c in line.strip().strip("|").split("|")]  # | RULE-003 | the question |
        text = " · ".join(c for c in cells if c and c != found.group(1))
        questions.append({"rule": found.group(1), "text": text or line.strip()})
    if not questions:
        for card in cards:
            if card["confidence"] and card["confidence"].casefold() != "high":
                questions.append({"rule": card["id"], "text": card["confidence_note"] or f"Confirm {card['name']}"})
    seen, unique = set(), []
    for q in questions:
        if q["rule"] not in seen:
            seen.add(q["rule"])
            unique.append(q)
    return unique


def data_objects(markdown: str) -> list[dict[str, str]]:
    """The core records: whichever heading level (## or ###) gives titled sections."""
    best = []
    for level in (2, 3):
        found = [s for s in sections(markdown, level) if s["title"]]
        if len(found) > len(best):
            best = found
    return best


def walk(node: dict[str, Any], domain: dict[str, Any] | None, out: dict[str, list]) -> None:
    kind = node.get("kind")
    if kind == "domain":
        domain = {"id": node.get("id"), "name": node.get("name"), "description": node.get("description", ""), "members": []}
        out["domains"].append(domain)
    elif kind in ("module", "job", "screen", "datastore") and domain is not None:
        item = {k: v for k, v in node.items() if k != "children"}
        item["domain"] = domain["id"]
        out[kind + "s"].append(item)
        domain["members"].append(node.get("id"))
    for child in node.get("children") or []:
        walk(child, domain, out)


def read(folder: RunFolder) -> dict[str, Any]:
    from reframe.claude.workspace import paths
    analysis = paths(folder)["analysis"]

    def text(name: str) -> str:
        path = analysis / name
        return path.read_text(errors="replace") if path.exists() else ""

    topology = json.loads(text("topology.json") or "{}")
    parts: dict[str, list] = {"domains": [], "modules": [], "jobs": [], "screens": [], "datastores": []}
    if topology.get("root"):
        walk(topology["root"], None, parts)
    rules_md = text("BUSINESS_RULES.md")
    cards = parse_rules(rules_md)
    module_domain = {m["name"].upper(): m["domain"] for m in parts["modules"] if m.get("name")}
    for card in cards:
        card["domain"] = module_domain.get(card["program"], "")
    result = json.loads(text("rules_result.json") or "{}") if (analysis / "rules_result.json").exists() else {}
    stats = result.get("stats") if isinstance(result, dict) else None
    return {
        "read_at": iso(),
        "files": sorted(p.name for p in analysis.iterdir() if p.is_file() and not p.name.endswith(".local.md")) if analysis.exists() else [],
        "preflight": sections(text("PREFLIGHT.md")),
        "assessment": sections(text("ASSESSMENT.md")),
        "system": topology.get("system"),
        "domains": [d for d in parts["domains"] if d["id"] != "dom:data"],
        "modules": parts["modules"], "jobs": parts["jobs"], "screens": parts["screens"], "datastores": parts["datastores"],
        "edges": topology.get("edges") or [], "entry_points": topology.get("entryPoints") or [], "dead_ends": topology.get("deadEnds") or [],
        "observations": topology.get("observations") or [], "flows": topology.get("flows") or [],
        "rules": cards, "rules_intro": sections(rules_md)[0]["markdown"] if rules_md and sections(rules_md) and not sections(rules_md)[0]["title"] else "",
        "rule_sections": [s["title"] for s in sections(rules_md, 2)],
        "sme_questions": sme_questions(rules_md, cards),
        "rule_stats": stats or {},
        "data_objects": data_objects(text("DATA_OBJECTS.md")),
        "links": {name: f"claude/analysis/{folder.state['project']}/{name}" for name in ("REPORT.html", "TOPOLOGY.html") if (analysis / name).exists()},
    }


def save(folder: RunFolder) -> dict[str, Any]:
    model = read(folder)
    folder.save("outputs/claude/model.json", model)
    folder.event("claude_retrieved", domains=len(model["domains"]), modules=len(model["modules"]), rules=len(model["rules"]),
                 questions=len(model["sme_questions"]))
    return model
