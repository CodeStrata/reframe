"""Pipeline 4, stage D8: the design page (docs/pipeline-4.md, section 4, P4-07).

outputs/design/index.html, in the review layout: the overview first (legacy and modern screens, journeys, the mapping's
counts, final and draft capabilities, the target stack), links to the flow map, the journeys, the modern screens and the
prototype; then each capability's specification, by domain and function, filtered by status, domain or words; then the
data contracts, each copybook once. Nothing is loaded from outside the page.
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from reframe.design.legacy import STYLE

PAGE = "outputs/design/index.html"
EXTRA = """
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin:14px 0}
.tile{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:10px 12px}.tile b{display:block;font-size:22px}
.tile span{color:var(--muted);font-size:13px}
.filters{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0;position:sticky;top:0;background:var(--bg);padding:8px 0;z-index:2}
.filters input,.filters select{font:inherit;padding:4px 8px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg)}
.filters input{flex:1;min-width:180px}
details.cap{background:var(--card);border:1px solid var(--line);border-radius:8px;margin:8px 0;padding:0 14px}
details.cap>summary{cursor:pointer;padding:10px 0;list-style:none}details.cap>summary::-webkit-details-marker{display:none}
details.cap[open]>summary{border-bottom:1px solid var(--line);margin-bottom:8px}
.st{font-size:12px;border-radius:10px;padding:0 8px;border:1px solid var(--line);margin-left:6px}
.final{color:#1c7c3a;border-color:#1c7c3a}.draft{color:var(--warn);border-color:var(--warn)}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]) .final{color:#6fd08f;border-color:#6fd08f}}
:root[data-theme="dark"] .final{color:#6fd08f;border-color:#6fd08f}
h3{font-size:15px;margin:16px 0 6px}h4{font-size:14px;margin:12px 0 4px}.cap p{margin:6px 0}
.gwt b{color:var(--muted);font-weight:600}.small{font-size:12.5px}.ev{font-size:12px;color:var(--muted)}
td.code{white-space:nowrap}
"""
SCRIPT = """
(function(){
  var q=document.getElementById('q'),st=document.getElementById('status'),dm=document.getElementById('domain'),n=document.getElementById('shown');
  function apply(){
    var words=q.value.toLowerCase().trim(),s=st.value,d=dm.value,count=0;
    document.querySelectorAll('details.cap').forEach(function(el){
      var ok=(!s||el.dataset.status===s)&&(!d||el.dataset.domain===d)&&(!words||el.textContent.toLowerCase().indexOf(words)>=0);
      el.hidden=!ok;if(ok)count++;
    });
    document.querySelectorAll('section.fn').forEach(function(el){el.hidden=!el.querySelector('details.cap:not([hidden])');});
    document.querySelectorAll('section.dom').forEach(function(el){el.hidden=!el.querySelector('section.fn:not([hidden])');});
    n.textContent=count+' shown';
  }
  [q,st,dm].forEach(function(el){el.addEventListener('input',apply);});
  if(location.hash){var t=document.getElementById(location.hash.slice(1));if(t&&t.tagName==='DETAILS'){t.open=true;}}
  apply();
})();
"""


def e(value: Any) -> str:
    return html.escape(str(value if value is not None else ""))


def anchor(key: str) -> str:
    return "cap-" + "".join(c if c.isalnum() else "-" for c in key).strip("-")


def _n(count: int, one: str, many: str = "") -> str:
    return f"{count} {one if count == 1 else many or one + 's'}"


def _table(rows: list[str], head: list[str]) -> str:
    if not rows:
        return '<p class="muted small">None.</p>'
    return f'<div class="wrap"><table><tr>{"".join(f"<th>{e(h)}</th>" for h in head)}</tr>{"".join(rows)}</table></div>'


def capability(s: dict[str, Any], rule_names: dict[str, str]) -> str:
    reqs = [f'<tr><td class="code"><code>{e(q["code"])}</code></td><td>{e(q["class"])}</td><td>{e(q["text"])}</td>'
            f'<td class="small">{e(", ".join(q["criteria"]) or "–")}</td></tr>' for q in s["requirements"]]
    rules = []
    for r in s["rules"]:
        examples = "".join(f'<li>{e("; ".join(str(g.get("field", "")) + ": " + str(g.get("value", "")) for g in x.get("given") or []) or "–")} → {e(x.get("then", ""))}</li>'
                           for x in r["examples"])
        rules.append(f'<tr><td><b>{e(r["name"])}</b><br><span class="ev">{e(r["key"])}</span></td><td>{e(r["class"])}<br><span class="ev">{e(r["kind"])}, {e(r["confidence"])}</span></td>'
                     f'<td>{e(r["text"])}{f"<ul class=small>{examples}</ul>" if examples else ""}<div class="ev">{e(", ".join(r["evidence"][:6]))}</div></td></tr>')
    criteria = [f'<tr><td class="code">{e(x["id"])}</td><td class="gwt"><b>Given</b> {e(x["given"])}<br><b>When</b> {e(x["when"])}<br><b>Then</b> {e(x["then"])}</td>'
                f'<td class="small">{e(", ".join(x["requirements"]))}<br><span class="ev">{e(", ".join(rule_names.get(k, k) for k in x["rules"]))}</span><br>'
                f'<span class="ev">{e(x["from"])}</span></td></tr>' for x in s["acceptance"]]
    screens = []
    for x in s["screens"]:
        parts = "".join(f'<li><code>{e(c.get("type", ""))}</code> {e(c.get("label", ""))}' + (f' <span class="ev">checks: {e(c["validation"])}</span>' if c.get("validation") else "") + "</li>"
                        for c in x["components"])
        how = ", ".join(f"{n} {h}" for h, n in x["mapping"].items())
        screens.append(f'<li><a href="{e(x["prototype"])}">{e(x["title"])}</a> <code>{e(x["id"])}</code> · <a href="modern.html#{e(x["id"])}">design</a>'
                       + (f' · replaces {", ".join(f"<a href=legacy/{e(m)}.html>{e(m)}</a>" for m in x["replaces"])}' if x["replaces"] else "")
                       + (f' <span class="ev">({e(how)})</span>' if how else "") + (f"<ul class=small>{parts}</ul>" if parts else "") + "</li>")
    contracts = ", ".join(f'<a href="#contract-{e(b["copybook"])}">{e(b["copybook"])}</a> <span class="ev">({e(b["role"])}; {e(", ".join(b["programs"]))})</span>'
                          for b in s["contracts"])
    tables = []
    for t in s["tables"]:
        rows = [f'<tr>{"".join(f"<td>{e(v)}</td>" for v in r.get("values") or [])}<td>{e(r.get("outcome", ""))}</td><td class="ev">{e(r.get("rule", ""))}</td></tr>'
                for r in t.get("rows") or []]
        gaps = [f'<tr class="warn">{"".join(f"<td>{e(v)}</td>" for v in g.get("values") or [])}<td colspan="2">Gap: {e(g.get("note", ""))}</td></tr>'
                for g in t.get("gaps") or []]
        tables.append(f'<h4>{e(t.get("title", ""))}</h4>' + _table(rows + gaps, list(t.get("conditions") or []) + [t.get("outcome") or "Outcome", "Rule"]))
    questions = "".join(f'<li>{e(q["id"])} {e(q["question"])}' + (f' <span class="ev">({e(q["owner"])})</span>' if q["owner"] else "") + "</li>" for q in s["questions"])
    notes = "".join(f'<li>{e(n["note"])} <span class="ev">{e(rule_names.get(n["rule"], n["rule"]))}</span></li>' for n in s["design_notes"])
    signed = "; ".join(f'{e(x["reviewer"] or "A reviewer")}, {e(str(x["at"])[:10])}' for x in s["signed_off"])
    extra = (f" · {_n(len(s['screens']), 'screen')}" if s["screens"] else "") + (f" · {_n(s['gaps'], 'gap')}" if s["gaps"] else "")
    head = (f'<summary><b>{e(s["number"])}. {e(s["title"])}</b><span class="st {e(s["status"])}">{e(s["status"])}</span>'
            f'<span class="muted small"> · {e(s["runs_as"])} · {len(s["requirements"])} requirements · {len(s["rules"])} rules · {_n(len(s["acceptance"]), "criterion", "criteria")}'
            f'{extra}</span></summary>')
    return (f'<details class="cap" id="{anchor(s["key"])}" data-status="{e(s["status"])}" data-domain="{e(s["domain"])}">{head}'
            f'<p>{e(s["summary"]) or "<span class=muted>No summary written.</span>"}</p><p class="muted small">{e(s["story"])}</p>'
            f'<p class="small">{"Final: signed off by " + signed if s["status"] == "final" else "Draft: the function is not signed off yet."}'
            f' Risk {e(s["risk"] or "–")}{"; touches " + e(", ".join(s["touches"])) if s["touches"] else ""}. <code>{e(s["key"])}</code></p>'
            f'<h3>Requirements</h3>{_table(reqs, ["Code", "Class", "Requirement", "Criteria"])}'
            f'<h3>Business rules</h3>{_table(rules, ["Rule", "Class", "Text, worked examples and evidence"])}'
            f'<h3>Acceptance criteria</h3>{_table(criteria, ["ID", "Criterion", "Checks"])}'
            f'<h3>Screens</h3>{"<ul>" + "".join(screens) + "</ul>" if screens else "<p class=muted small>None: " + e(s["runs_as"]) + ".</p>"}'
            f'<h3>Data contracts</h3><p class="small">{contracts or "<span class=muted>None found in the source.</span>"}</p>'
            f'<h3>Decision tables</h3>{"".join(tables) or "<p class=muted small>None.</p>"}'
            f'<h3>Open questions</h3>{"<ul class=small>" + questions + "</ul>" if questions else "<p class=muted small>None.</p>"}'
            f'<h3>Design notes</h3>{"<ul class=small>" + notes + "</ul>" if notes else "<p class=muted small>None.</p>"}</details>')


def _group(f: dict[str, Any]) -> str:
    return f'<br><span class="ev">in {e(f["group"])}</span>' if f["group"] else ""


def contract_block(c: dict[str, Any]) -> str:
    parts = []
    for r in c["records"]:
        rows = [f'<tr><td><code>{e(f["name"])}</code>{_group(f)}</td>'
                f'<td><code>{e(f["pic"])}</code> <span class="ev">{e(f["usage"])}</span></td><td>{e(f["says"])}'
                + (f'<br><span class="ev">occurs {e(f["occurs"])}</span>' if f.get("occurs") else "") + (f'<br><span class="ev">redefines {e(f["redefines"])}</span>' if f.get("redefines") else "")
                + (f'<br><span class="ev">{e(", ".join(x["name"] + " = " + str(x["value"]) for x in f["conditions"]))}</span>' if f.get("conditions") else "")
                + f'</td><td>{e((f.get("stack") or {}).get("code", ""))}</td><td>{e((f.get("stack") or {}).get("column", ""))}</td><td class="ev">{e(c["file"])}:{e(f["line"])}</td></tr>'
                for f in r["fields"]]
        parts.append(f'<h4>{e(r["name"])}</h4>' + _table(rows, ["Field", "PIC", "Type", "Code type", "Column type", "Source"]))
    return f'<details class="cap" id="contract-{e(c["copybook"])}"><summary><b>{e(c["copybook"])}</b> <span class="muted small">{e(c["file"])} · ' \
           f'{len(c["records"])} record(s), {sum(len(r["fields"]) for r in c["records"])} fields</span></summary>{"".join(parts)}</details>'


def draw(folder, value: dict[str, Any]) -> Path:
    specs = value["full"]
    inventory = folder.load("design/screens.json") or {}
    modern = folder.load("design/modern.json") or {}
    journeys = (folder.load("design/journeys.json") or {}).get("journeys") or []
    rule_names = {r["key"]: r["name"] or r["key"] for s in specs for r in s["rules"]}
    c, m = value["counts"], (modern.get("counts") or {})
    how = ", ".join(f"{n} {h}" for h, n in (m.get("how") or {}).items() if n)
    stack = value.get("stack") or {}
    tiles = [(len(inventory.get("screens") or []), "legacy screens"), (len(modern.get("screens") or []), "modern screens"), (len(journeys), "journeys"),
             (m.get("mapped", 0), "legacy items mapped"), (c["capabilities"], "capabilities"), (c["final"], "final"), (c["draft"], "draft"),
             (c["requirements"], "requirements"), (c["criteria"], "acceptance criteria"), (c["contracts"], "data contracts"), (c["gaps"], "decision table gaps"),
             (c["questions"], "open SME questions")]
    domains: dict[str, dict[str, list[dict[str, Any]]]] = {}
    for s in specs:
        domains.setdefault(s["domain"], {}).setdefault(s["function_name"], []).append(s)
    body_parts = []
    for d, fns in domains.items():
        inner = "".join(f'<section class="fn"><h3>{e(fn)}</h3>{"".join(capability(s, rule_names) for s in caps)}</section>' for fn, caps in fns.items())
        body_parts.append(f'<section class="dom"><h2>{e(d)}</h2>{inner}</section>')
    options = "".join(f'<option value="{e(d)}">{e(d)}</option>' for d in domains)
    problems = "".join(f'<li class="warn">{e(p)}</li>' for p in value["problems"][:400]) or '<li class="muted">None.</li>'
    more = f'<li class="muted">and {len(value["problems"]) - 400} more, in design/specs.json</li>' if len(value["problems"]) > 400 else ""
    classes = ", ".join(f"{n} {k}" for k, n in c["classes"].items() if n)
    stack_line = (f'Target stack, given by {e(stack.get("given_by", "the engineer"))} on {e(str(stack.get("at", ""))[:10])}: <b>{e(stack.get("stack", ""))}</b>.'
                  if stack else "Target stack: not given yet, so the data contracts show neutral types.")
    notes = " ".join(e(n) for n in value.get("stack_notes") or [] if stack)
    contracts = "".join(contract_block(x) for x in value["contracts"].values())
    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The design</title><style>{STYLE}{EXTRA}</style></head><body><main>
<p class="muted"><a href="legacy/index.html">Legacy screens</a> · <a href="flow.html">Screen flow</a> · <a href="journeys.html">Journeys</a> ·
<a href="modern.html">Modern screens</a> · <a href="prototype/index.html">Prototype</a> · {e(folder.state.get('project') or '')}</p>
<h1>The design</h1>
<p class="muted">The modernized application's design, from the reconciled requirements and rules: the screens, the journeys, and a final specification
for every capability. A capability in a signed-off function is final; every other one is draft. Reframe assembled each specification and checked
every requirement, rule, screen and copybook it cites; a Claude step per function wrote the summaries, {c['written']} acceptance criteria for requirements
no worked example covers, and {c['design_notes']} design notes. Model output, for review.</p>
<div class="tiles">{''.join(f'<div class="tile"><b>{e(n)}</b><span>{e(t)}</span></div>' for n, t in tiles)}</div>
<p class="small">{stack_line} {notes}</p>
<p class="small muted">Mapping: {e(how or '–')}. Rules by class: {e(classes)}. Criteria: {c['from_examples']} from worked examples, {c['written']} written from the rules.</p>
<div class="filters"><input id="q" type="search" placeholder="Find words in the specifications" aria-label="Find">
<select id="status" aria-label="Status"><option value="">Final and draft</option><option value="final">Final</option><option value="draft">Draft</option></select>
<select id="domain" aria-label="Domain"><option value="">Every domain</option>{options}</select><span class="muted small" id="shown"></span></div>
{''.join(body_parts)}
<h2>Data contracts</h2><p class="muted small">The copybooks the capabilities' programs copy, as typed records, read from the source with no model.</p>{contracts}
<h2>What the checks still found</h2><ul>{problems}{more}</ul>
</main><script>{SCRIPT}</script></body></html>"""
    target = folder.path(PAGE)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body)
    return target

