"""The interactive design site, rendered from any canonical design (specification FR-10, section 9; P1-06).

The renderer knows nothing about any one application: every page, field,
action, rule and interaction comes from design.json and its supporting
records, and every behavioural element carries data-reframe-id. Under
preserve there is one page per 3270 map with its keys; under modernize, task
pages list the maps they replace. A design with no screens (batch-only, or a
message or file exchange) renders its interactions without inventing pages or
endpoints.

The output is plain HTML that opens without Reframe: one inline stylesheet,
no scripts, no external resources, and every value from the input escaped.
Navigation is ordinary links. Rendering is deterministic.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import quote

from reframe_v2.model.records import Ref, hash_of
from reframe_v2.model.schemas import validate

STATUS_LABELS = {
    "SUPPORTED": "Supported by source",
    "PARTIALLY_SUPPORTED": "Partly supported",
    "CONTRADICTED": "Contradicted by source",
    "NO_SOURCE_FOUND": "No source found",
    "NOT_CHECKED": "Not yet checked",
}

STYLE = """
:root{--ink:#1d2433;--muted:#5b6475;--line:#d7dbe3;--panel:#f6f7f9;--accent:#2457c5;--ok:#1f7a3d;--warn:#9a5b00;--bad:#b42318;--bg:#ffffff}
@media (prefers-color-scheme: dark){:root{--ink:#e6e9ef;--muted:#a3abba;--line:#394150;--panel:#1c212b;--accent:#8fb0ff;--ok:#6fd08f;--warn:#f2b64c;--bad:#ff8a80;--bg:#12161d}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}
main{max-width:980px;margin:0 auto;padding:24px 16px 64px}a{color:var(--accent)}
header.site{border-bottom:1px solid var(--line);padding-bottom:12px;margin-bottom:20px}
.meta{color:var(--muted);font-size:13px}.banner{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px 12px;margin:12px 0;font-size:13px}
.screen{border:1px solid var(--line);border-radius:8px;padding:16px;background:var(--panel);margin:16px 0}
.field{display:grid;grid-template-columns:minmax(120px,220px) 1fr;gap:8px;align-items:center;margin:6px 0}
.box{border:1px dashed var(--muted);border-radius:4px;padding:4px 8px;color:var(--muted);font-family:ui-monospace,Menlo,monospace;font-size:13px}
.actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.action{display:inline-block;border:1px solid var(--accent);border-radius:6px;padding:4px 10px;text-decoration:none}
.key{font-family:ui-monospace,Menlo,monospace;font-size:12px;color:var(--muted);margin-right:4px}
table{border-collapse:collapse;width:100%;margin:8px 0 16px;font-size:14px}th,td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
.wrap{overflow-x:auto}.status-SUPPORTED{color:var(--ok)}.status-PARTIALLY_SUPPORTED,.status-NOT_CHECKED{color:var(--warn)}.status-CONTRADICTED,.status-NO_SOURCE_FOUND{color:var(--bad)}
details{border:1px solid var(--line);border-radius:6px;padding:8px 12px;margin:16px 0}pre{white-space:pre-wrap;font-size:13px}
nav.crumbs{font-size:13px;margin-bottom:8px}section{margin-top:24px}
"""


class RenderError(Exception):
    """The design cannot be rendered as given: a reference does not resolve. Nothing was written."""


@dataclass(frozen=True)
class RuleInfo:
    id: str
    statement: str
    status: str
    source: str | None


@dataclass(frozen=True)
class Feedback:
    channel: str
    """'github' or 'local' (FR-18)."""
    repository: str | None = None


@dataclass(frozen=True)
class SiteInput:
    design: dict[str, Any]
    rules: dict[str, RuleInfo]
    feedback: Feedback
    version: Ref | None = None
    findings: dict[str, tuple[str, ...]] = field(default_factory=dict)
    scenarios: dict[str, tuple[str, ...]] = field(default_factory=dict)
    label: str | None = None
    """A banner such as 'Synthetic sample', shown on every page."""


def slug(identifier: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", identifier.lower()).strip("-") or "item"


def e(value: Any) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def check(site: SiteInput) -> None:
    """Validate the design against its schema and make sure every reference resolves."""
    design = site.design
    record = {"schema": "canonical_design/1", "record_type": "canonical_design", "id": "design:render-check", "revision": 1,
              "content_hash": hash_of("canonical_design", "design:render-check", (), design), "depends_on": [], "body": design}
    validate(record)
    pages = {page["id"] for page in design["pages"]}
    interactions = {item["id"] for item in design["interactions"]}
    problems = []
    seen_slugs: dict[str, str] = {}
    for kind, identifier in [("page", p) for p in pages] + [("interaction", i) for i in interactions]:
        other = seen_slugs.setdefault(slug(identifier), identifier)
        if other != identifier:
            problems.append(f"{identifier} and {other} would share a file name")
    for journey in design["journeys"]:
        problems += [f"journey {journey['id']} names unknown page {p}" for p in journey["pages"] if p not in pages]
    for page in design["pages"]:
        for action in page["actions"]:
            if action["navigates_to"] and action["navigates_to"] not in pages:
                problems.append(f"action {action['id']} navigates to unknown page {action['navigates_to']}")
            if action["interaction"] and action["interaction"] not in interactions:
                problems.append(f"action {action['id']} uses unknown interaction {action['interaction']}")
        rule_ids = list(page["rules_applied"]) + [r for f in page["fields"] for r in f["rules"]]
        problems += [f"page {page['id']} applies unknown rule {r}" for r in rule_ids if r not in site.rules]
    for item in design["interactions"]:
        problems += [f"interaction {item['id']} applies unknown rule {r}" for r in item["rules_applied"] if r not in site.rules]
        if item["type"] == "http" and not item["contract"]:
            problems.append(f"http interaction {item['id']} needs its OpenAPI contract")
    for rule in site.rules.values():
        if rule.status not in STATUS_LABELS:
            problems.append(f"rule {rule.id} has unknown evidence status {rule.status}")
    if site.feedback.channel not in ("github", "local") or (site.feedback.channel == "github" and not site.feedback.repository):
        problems.append("feedback is 'github' with a repository, or 'local'")
    if problems:
        raise RenderError("; ".join(sorted(problems)))


def render(site: SiteInput) -> dict[str, bytes]:
    """The design site as file name to bytes. Refuses a design whose references do not resolve."""
    check(site)
    design = site.design
    files = {"index.html": _index(site)}
    for page in design["pages"]:
        files[f"page-{slug(page['id'])}.html"] = _page(site, page)
    files["interactions.html"] = _interactions(site)
    return {name: text.encode("utf-8") for name, text in sorted(files.items())}


def _shell(site: SiteInput, title: str, body: str) -> str:
    design = site.design
    version = f"{site.version.id} revision {site.version.revision}" if site.version else "unversioned draft"
    banner = f'<div class="banner">{e(site.label)}</div>' if site.label else ""
    return (
        "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>{e(title)}</title><style>{STYLE}</style></head><body><main>"
        f"<header class=\"site\"><nav class=\"crumbs\"><a href=\"index.html\">Design</a> · <a href=\"interactions.html\">Interactions</a></nav>"
        f"<div class=\"meta\">Context {e(design['context'])} · goal <strong>{e(design['goal'])}</strong> · {e(version)}</div>"
        f"{banner}</header>{body}</main></body></html>\n"
    )


def _index(site: SiteInput) -> str:
    design = site.design
    pages = {page["id"]: page for page in design["pages"]}
    parts = [f"<h1>{e(design['context'])}: design</h1>"]
    if design["journeys"]:
        parts.append("<section><h2>Journeys</h2>")
        for journey in design["journeys"]:
            steps = " → ".join(f'<a href="page-{slug(p)}.html" data-reframe-id="{e(p)}">{e(pages[p]["name"])}</a>' for p in journey["pages"])
            parts.append(f'<p data-reframe-id="{e(journey["id"])}"><strong>{e(journey["name"])}</strong>: {steps}</p>')
        parts.append("</section>")
    if design["pages"]:
        parts.append("<section><h2>Pages</h2><ul>" + "".join(
            f'<li><a href="page-{slug(p["id"])}.html" data-reframe-id="{e(p["id"])}">{e(p["name"])}</a>'
            + (f' <span class="meta">replaces {e(", ".join(p["replaces_maps"]))}</span>' if p["replaces_maps"] else "") + "</li>"
            for p in design["pages"]) + "</ul></section>")
    else:
        parts.append('<section><h2>No screens</h2><p>This design has no pages. Its behaviour is in its '
                     '<a href="interactions.html">interactions</a>; no screens or endpoints are invented for it.</p></section>')
    parts.append(f'<section><h2>Interactions</h2><p>{len(design["interactions"])} interaction(s): '
                 '<a href="interactions.html">contract explorer</a>.</p></section>')
    parts.append(_feedback(site, design["context"], "the whole design"))
    return _shell(site, f"{design['context']} design", "".join(parts))


def _rule_rows(site: SiteInput, rule_ids: list[str]) -> str:
    if not rule_ids:
        return '<p class="meta">No rules applied.</p>'
    rows = []
    for rule_id in dict.fromkeys(rule_ids):
        rule = site.rules[rule_id]
        rows.append(f'<tr data-reframe-id="{e(rule.id)}"><td>{e(rule.id)}</td><td>{e(rule.statement)}</td>'
                    f'<td class="status-{e(rule.status)}">{e(STATUS_LABELS[rule.status])}</td><td>{e(rule.source or "no source line")}</td></tr>')
    return ('<div class="wrap"><table><thead><tr><th>Rule</th><th>Statement</th><th>Evidence</th><th>Source</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")


def _list(title: str, items: tuple[str, ...] | list[str], empty: str) -> str:
    if not items:
        return f'<section><h2>{e(title)}</h2><p class="meta">{e(empty)}</p></section>'
    return f'<section><h2>{e(title)}</h2><ul>' + "".join(f"<li>{e(item)}</li>" for item in items) + "</ul></section>"


def _page(site: SiteInput, page: dict[str, Any]) -> str:
    design = site.design
    preserve = design["goal"] == "preserve"
    pages = {p["id"]: p for p in design["pages"]}
    heading = f"<h1>{e(page['name'])}</h1>"
    if preserve:
        origin = f'<p class="meta">3270 map: {e(", ".join(page["replaces_maps"]) or "none recorded")}</p>'
    else:
        origin = f'<p class="meta">Task page. Replaces maps: {e(", ".join(page["replaces_maps"]) or "none")}</p>'
    fields = "".join(
        f'<div class="field" data-reframe-id="{e(f["id"])}"><label>{e(f["label"])}</label>'
        f'<span class="box">{e(f["type"])}{"(" + e(f["length"]) + ")" if f["length"] is not None else ""}</span></div>'
        for f in page["fields"])
    actions = []
    for action in page["actions"]:
        key = f'<span class="key">{e(action["key"])}</span>' if action["key"] else ""
        if action["navigates_to"]:
            href = f'page-{slug(action["navigates_to"])}.html'
        elif action["interaction"]:
            href = f'interactions.html#{slug(action["interaction"])}'
        else:
            href = f'#{slug(action["id"])}'
        target = pages[action["navigates_to"]]["name"] if action["navigates_to"] else None
        title = f' title="Goes to {e(target)}"' if target else ""
        actions.append(f'<a class="action" id="{slug(action["id"])}" data-reframe-id="{e(action["id"])}" href="{href}"{title}>{key}{e(action["label"])}</a>')
    screen = f'<div class="screen">{fields or "<p class=meta>No fields.</p>"}<div class="actions">{"".join(actions)}</div></div>'
    field_rows = "".join(
        f'<tr data-reframe-id="{e(f["id"])}"><td>{e(f["label"])}</td><td>{e(f["type"])}</td><td>{e(f["length"] if f["length"] is not None else "")}</td>'
        f'<td>{e("; ".join(f["validation"]) or "none")}</td><td>{e(", ".join(f["rules"]) or "none")}</td></tr>' for f in page["fields"])
    spec = ('<section><h2>Fields</h2><div class="wrap"><table><thead><tr><th>Field</th><th>Type</th><th>Length</th><th>Validation</th><th>Rules</th></tr></thead>'
            f"<tbody>{field_rows}</tbody></table></div></section>") if page["fields"] else ""
    interactions = [a["interaction"] for a in page["actions"] if a["interaction"]]
    used = ("<section><h2>Interactions used</h2><ul>" + "".join(
        f'<li><a href="interactions.html#{slug(i)}" data-reframe-id="{e(i)}">{e(i)}</a></li>' for i in dict.fromkeys(interactions)) + "</ul></section>") if interactions else ""
    rule_ids = list(page["rules_applied"]) + [r for f in page["fields"] for r in f["rules"]]
    findings = list(site.findings.get(page["id"], ())) + [x for f in page["fields"] for x in site.findings.get(f["id"], ())]
    body = (heading + origin + screen + spec + f"<section><h2>Rules</h2>{_rule_rows(site, rule_ids)}</section>" + used
            + _list("Open findings", findings, "No open findings recorded for this page.")
            + _list("Scenarios", site.scenarios.get(page["id"], ()), "No scenarios recorded yet.")
            + _feedback(site, page["id"], f"page {page['name']}"))
    return _shell(site, page["name"], body)


def _interactions(site: SiteInput) -> str:
    design = site.design
    parts = ["<h1>Interactions</h1>"]
    if not design["interactions"]:
        parts.append('<p class="meta">This design has no interactions.</p>')
    for item in design["interactions"]:
        contract = (f'<p>OpenAPI contract: <code>{e(item["contract"])}</code></p>' if item["type"] == "http"
                    else f'<p class="meta">Structured description ({e(item["type"])}); no HTTP endpoint is implied.</p>')
        parts.append(
            f'<section id="{slug(item["id"])}" data-reframe-id="{e(item["id"])}"><h2>{e(item["name"])}</h2>'
            f'<p class="meta">{e(item["id"])} · {e(item["type"])}</p><p>{e(item["summary"])}</p>{contract}'
            + _list("Reads", item["inputs"], "Nothing recorded.") + _list("Writes", item["outputs"], "Nothing recorded.")
            + f"<h3>Rules</h3>{_rule_rows(site, item['rules_applied'])}"
            + _list("Open findings", site.findings.get(item["id"], ()), "No open findings recorded.")
            + _list("Scenarios", site.scenarios.get(item["id"], ()), "No scenarios recorded yet.")
            + _feedback(site, item["id"], f"interaction {item['name']}") + "</section>")
    return _shell(site, "Interactions", "".join(parts))


def feedback_text(site: SiteInput, element: str, what: str) -> tuple[str, str]:
    version = f"{site.version.id} revision {site.version.revision}" if site.version else "unversioned draft"
    title = f"Design feedback: {what}"
    body = f"Element: {element}\nDesign version: {version}\nContext: {site.design['context']}\n\nFeedback:\n"
    return title, body


def _feedback(site: SiteInput, element: str, what: str) -> str:
    title, body = feedback_text(site, element, what)
    shown = f"<pre>{e(title)}\n\n{e(body)}</pre>"
    if site.feedback.channel == "github":
        url = (f"https://github.com/{quote(site.feedback.repository, safe='/')}/issues/new?title={quote(title)}&body={quote(body)}")
        how = f'<p><a href="{e(url)}" rel="noopener">Open a GitHub issue with this text</a>. Nothing is sent until you submit it there.</p>'
    else:
        how = (f"<p>Save this text, add your feedback, and record it with <code>reframe context add &lt;file&gt; --for {e(element)}</code>. "
               "Nothing leaves this page by itself.</p>")
    return f"<details><summary>Give feedback on {e(what)}</summary><p class=\"meta\">This is exactly what will be sent:</p>{shown}{how}</details>"


def load_sample(path: str, feedback: Feedback | None = None) -> SiteInput:
    """Read a sample file (v2/examples/designs) into a SiteInput."""
    import json

    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    rules = {r["id"]: RuleInfo(r["id"], r["statement"], r["status"], r["source"]) for r in data["rules"]}
    return SiteInput(
        data["design"], rules, feedback or Feedback("local"),
        findings={k: tuple(v) for k, v in data.get("findings", {}).items()},
        scenarios={k: tuple(v) for k, v in data.get("scenarios", {}).items()},
        label=data.get("label"),
    )


def main(argv: list[str] | None = None) -> int:
    import sys
    from pathlib import Path

    args = sys.argv[1:] if argv is None else argv
    if len(args) != 2:
        print("usage: python -m reframe_v2.design_site <design-sample.json> <out-dir>", file=sys.stderr)
        return 2
    out = Path(args[1])
    if out.exists() and any(out.iterdir()):
        print(f"{out} is not empty; nothing written", file=sys.stderr)
        return 3
    out.mkdir(parents=True, exist_ok=True)
    for name, data in render(load_sample(args[0])).items():
        (out / name).write_bytes(data)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
