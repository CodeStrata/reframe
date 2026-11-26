"""Pipeline 4, stage D4: the modern screens and the mapping as a page (docs/pipeline-4.md, section 4, P4-05).

outputs/design/modern.html: each modern screen drawn as a plain wireframe from its components, grouped by section, with
the journeys it serves and the legacy screens it replaces (linked to their 3270 copies); then, per legacy screen, the
mapping of its fields and keys (kept, merged, split, dropped, new) with the reasons. The clickable prototype is P4-06.
Nothing is loaded from outside the page.
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from reframe.design.legacy import STYLE

PAGE = "outputs/design/modern.html"
EXTRA = """
.screenbox{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin:14px 0}
.screenbox h3{margin:0;font-size:17px}.frame{border:1px solid var(--line);border-radius:8px;padding:10px 12px;margin-top:10px;background:var(--bg)}
.sec{margin:8px 0}.sec>b{display:block;font-size:13px;color:var(--muted);margin-bottom:4px}.comp{display:flex;gap:8px;align-items:baseline;margin:3px 0;font-size:14px}
.ctype{font:11.5px ui-monospace,Menlo,monospace;color:var(--muted);min-width:64px}.input{border:1px solid var(--line);border-radius:5px;padding:1px 8px;min-width:140px;color:var(--muted);background:var(--card)}
.btn{border:1px solid var(--accent);color:var(--accent);border-radius:5px;padding:0 10px}.how{font-size:12px;border-radius:9px;padding:0 7px;border:1px solid var(--line)}
.dropped{color:var(--warn)}
"""
INPUTS = {"text", "number", "money", "date", "select", "checkbox", "radio", "password", "search"}


def _component(c: dict[str, Any], ids: dict[str, str]) -> str:
    kind = str(c.get("type", "")).lower()
    label = html.escape(c.get("label", ""))
    if kind in INPUTS:
        body = f"{label} <span class=\"input\">{html.escape(c.get('shows', '') or kind)}</span>"
    elif kind in ("button", "link"):
        target = c.get("goes_to")
        body = f"<span class=\"btn\">{label}</span>" + (f" → <a href=\"#{html.escape(target)}\">{html.escape(ids.get(target, target))}</a>" if target else "")
    else:
        body = f"<b>{label}</b>" + (f" <span class=\"muted\">{html.escape(c.get('shows', ''))}</span>" if c.get("shows") else "")
    extra = []
    if c.get("validation"):
        extra.append(f"checks: {html.escape(c['validation'])}")
    if c.get("keyboard"):
        extra.append(f"key {html.escape(c['keyboard'])}")
    if c.get("rules"):
        extra.append(f"{len(c['rules'])} rule(s)")
    tail = f' <span class="muted" style="font-size:12.5px">{"; ".join(extra)}</span>' if extra else ""
    return f'<div class="comp"><span class="ctype">{html.escape(kind)}</span><span>{body}{tail}</span></div>'


def draw(folder, value: dict[str, Any]) -> Path:
    legacy = {s["map"]: s for s in (folder.load("design/screens.json") or {}).get("screens") or []}
    ids = {s["id"]: s["title"] for s in value["screens"]}
    parts = []
    for s in value["screens"]:
        sections: dict[str, list[str]] = {}
        for c in s.get("components") or []:
            sections.setdefault(c.get("section") or "", []).append(_component(c, ids))
        frame = "".join(f'<div class="sec">{"<b>" + html.escape(k) + "</b>" if k else ""}{"".join(v)}</div>' for k, v in sections.items())
        replaces = ", ".join(f'<a href="legacy/{html.escape(m)}.html">{html.escape((legacy.get(m) or {}).get("title") or m)}</a>' for m in s.get("replaces") or [])
        parts.append(f'<div class="screenbox" id="{html.escape(s["id"])}"><h3>{html.escape(s["title"])} <code>{html.escape(s["id"])}</code></h3>'
                     f'<p class="muted">{html.escape(s.get("purpose", ""))}<br>{html.escape(s["domain"])} · journeys {", ".join(s.get("journeys") or []) or "–"}'
                     f' · replaces {replaces or "nothing (new)"}</p><div class="frame">{frame}</div></div>')
    rows = []
    for d in value["domains"].values():
        for m in sorted(d["mapping"], key=lambda m: (m.get("legacy_screen", ""), {"screen": 0, "key": 2}.get(m.get("kind"), 1), m.get("legacy", ""))):
            becomes = m.get("becomes", "")
            target = becomes.split("/")[0]
            link = f'<a href="#{html.escape(target)}">{html.escape(becomes)}</a>' if becomes else "–"
            rows.append(f'<tr><td><a href="legacy/{html.escape(m["legacy_screen"])}.html">{html.escape(m["legacy_screen"])}</a></td><td>{html.escape(m.get("kind", ""))}</td>'
                        f'<td><code>{html.escape(m.get("legacy", ""))}</code></td><td><span class="how {"dropped" if m.get("how") == "dropped" else ""}">{html.escape(m.get("how", ""))}</span></td>'
                        f'<td>{link}</td><td>{html.escape(m.get("why", ""))}</td></tr>')
    c = value["counts"]
    problems = "".join(f'<li class="warn">{html.escape(p)}</li>' for p in value["problems"]) or '<li class="muted">None.</li>'
    how = ", ".join(f"{n} {h}" for h, n in c["how"].items() if n)
    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Modern screens</title><style>{STYLE}{EXTRA}</style></head><body><main>
<p class="muted"><a href="legacy/index.html">Legacy screens</a> · <a href="flow.html">Screen flow</a> · <a href="journeys.html">Journeys</a> · {html.escape(folder.state.get('project') or '')}</p>
<h1>Modern screens</h1>
<p class="muted">{c['screens']} modern screens designed by a Claude step per domain from Reframe's design system, and {c['mapped']} legacy screens, fields and keys
mapped ({html.escape(how)}). Reframe checked that every legacy field and key is mapped once and every validation rule is shown. Model output, for review.</p>
{''.join(parts)}
<h2>Mapping</h2><div class="wrap"><table><tr><th>Legacy screen</th><th>Kind</th><th>Item</th><th>How</th><th>Becomes</th><th>Why</th></tr>{''.join(rows)}</table></div>
<h2>What the checks still found</h2><ul>{problems}</ul>
</main></body></html>"""
    target = folder.path(PAGE)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body)
    return target
