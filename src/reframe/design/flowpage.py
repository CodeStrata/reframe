"""Pipeline 4, stage D2: the screen flow as a page (docs/pipeline-4.md, section 4, P4-03).

outputs/design/flow.html: each screen with how it is reached and where it goes (by key, menu option or transfer), each
link with the lines that show it, linked to the 3270 copies; the transactions; and what the source left unresolved.
Nothing is loaded from outside the page.
"""

from __future__ import annotations

import html
from collections import defaultdict
from pathlib import Path
from typing import Any

from reframe.design.legacy import STYLE

PAGE = "outputs/design/flow.html"
KINDS = {"key": "key", "xctl": "transfer (XCTL)", "link": "call (LINK)", "return": "next transaction", "transaction": "transaction"}


def _cites(lines: list[str]) -> str:
    return "<br>".join(f"<code>{html.escape(c)}</code>" for c in lines)


def _target(program: str, screens_of: dict[str, list[str]], titles: dict[str, str]) -> str:
    from reframe.design.flow import CALLER
    if program == CALLER:
        return "<i>the screen it came from</i>, as the program records it before transferring"
    maps = screens_of.get(program) or []
    if not maps:
        return f"<code>{html.escape(program)}</code> <span class=\"muted\">(no screen)</span>"
    return ", ".join(f'<a href="legacy/{html.escape(m)}.html">{html.escape(titles.get(m) or m)}</a>' for m in maps) + f" <code>{html.escape(program)}</code>"


BACK = ("F3", "F12")


def forward(found: dict[str, Any]) -> dict[str, set[str]]:
    """Screen-to-screen links that go forward: transfers and keys, leaving out F3, F12 and returns to the caller."""
    from reframe.design.flow import CALLER
    screen_of = found["screens_of_programs"]
    back = {(l["from"], l["to"]) for l in found["links"] if l["kind"] == "key" and l.get("key") in BACK}
    edges: dict[str, set[str]] = defaultdict(set)
    for l in found["links"]:
        if l["kind"] not in ("xctl", "key", "link") or l["to"] == CALLER or (l["kind"] == "key" and l.get("key") in BACK) or (l["from"], l["to"]) in back:
            continue
        for a in screen_of.get(l["from"], []):
            for b in screen_of.get(l["to"], []):
                if a != b:
                    edges[a].add(b)
    entry = entry_screen(edges)
    if entry:  # transfers to the entry screen (sign-on when a program starts without a session) are not forward
        for a in list(edges):
            edges[a].discard(entry)
    return edges


def entry_screen(edges: dict[str, set[str]]) -> str | None:
    """The screen most other screens transfer to: on CardDemo the sign-on, where every program goes when it starts
    without a session."""
    incoming: dict[str, int] = defaultdict(int)
    for a, targets in edges.items():
        for b in targets:
            incoming[b] += 1
    if not incoming:
        return None
    best = max(incoming, key=lambda m: (incoming[m], m))
    return best if incoming[best] >= max(3, len(edges) // 3) else None


def layers(maps: list[str], edges: dict[str, set[str]]) -> list[list[str]]:
    """Screens in columns by their distance from the screens nothing leads forward to (sign-on, on CardDemo)."""
    incoming = {m: 0 for m in maps}
    for a, targets in edges.items():
        for b in targets:
            incoming[b] = incoming.get(b, 0) + 1
    roots = [m for m in maps if not incoming.get(m)] or maps[:1]
    depth = {m: 0 for m in roots}
    queue = list(roots)
    while queue:
        a = queue.pop(0)
        for b in sorted(edges.get(a, ())):
            if b not in depth:
                depth[b] = depth[a] + 1
                queue.append(b)
    top = max(depth.values(), default=0)
    for m in maps:
        depth.setdefault(m, top + 1)  # reached only by going back
    return [sorted(m for m in maps if depth[m] == d) for d in range(max(depth.values(), default=0) + 1)]


def diagram(screens: dict[str, Any], found: dict[str, Any]) -> str:
    """An SVG map: columns by distance from sign-on, a box per screen linked to its 3270 copy, forward links as curves."""
    titles = {s["map"]: s["title"] or s["map"] for s in screens["screens"]}
    edges = forward(found)
    columns = layers([s["map"] for s in screens["screens"]], edges)
    w, h, gap_x, gap_y = 168, 40, 70, 14
    pos = {}
    for c, col in enumerate(columns):
        for r, m in enumerate(col):
            pos[m] = (16 + c * (w + gap_x), 16 + r * (h + gap_y))
    width = 32 + len(columns) * (w + gap_x) - gap_x
    height = 32 + max((len(col) for col in columns), default=1) * (h + gap_y) - gap_y
    paths = []
    for a, targets in sorted(edges.items()):
        for b in sorted(targets):
            (x1, y1), (x2, y2) = pos[a], pos[b]
            sx, sy, ex, ey = x1 + w, y1 + h / 2, x2, y2 + h / 2
            if ex <= sx:  # a link to an earlier column or within one is listed under its screen, not drawn
                continue
            else:
                mid = (sx + ex) / 2
                paths.append(f'<path d="M{sx},{sy} C{mid},{sy} {mid},{ey} {ex},{ey}" class="edge" marker-end="url(#arrow)"/>')
    boxes = []
    for m, (x, y) in pos.items():
        label = html.escape(titles[m] if len(titles[m]) <= 24 else titles[m][:23] + "…")
        boxes.append(f'<a href="#{html.escape(m)}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" class="box"/>'
                     f'<text x="{x + 10}" y="{y + 17}" class="t1">{label}</text><text x="{x + 10}" y="{y + 32}" class="t2">{html.escape(m)}</text></a>')
    return (f'<div class="wrap"><svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" role="img" aria-label="Map of the screens">'
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" class="head"/></marker></defs>' + "".join(paths) + "".join(boxes) + "</svg></div>")


MAP_STYLE = """
.box{fill:var(--card);stroke:var(--line)}a:hover .box{stroke:var(--accent)}.t1{font:600 12.5px system-ui,sans-serif;fill:var(--fg)}
.t2{font:11px ui-monospace,Menlo,monospace;fill:var(--muted)}.edge{fill:none;stroke:var(--muted);stroke-width:1.2;opacity:.75}
.edge.back{stroke-dasharray:3 3;opacity:.5}.head{fill:var(--muted)}
"""


def draw(folder, screens: dict[str, Any], found: dict[str, Any]) -> Path:
    titles = {s["map"]: s["title"] or s["map"] for s in screens["screens"]}
    screens_of = found["screens_of_programs"]
    out_of: dict[str, list[dict[str, Any]]] = defaultdict(list)
    into: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for link in found["links"]:
        if link["kind"] != "transaction":
            out_of[link["from"]].append(link)
            into[link["to"]].append(link)
    sections = []
    reach = {r["screen"]: r for r in found["reach"]}
    for s in screens["screens"]:
        progs = [p["name"] for p in s["programs"]]
        r = reach.get(s["map"], {})
        rows = []
        for p in progs:
            by_key = {l["to"] for l in out_of.get(p, []) if l["kind"] == "key"}
            for link in sorted(out_of.get(p, []), key=lambda l: (l["kind"] != "key", l.get("key", ""), l["to"])):
                if link["kind"] != "key" and link["to"] in by_key and not link.get("option"):
                    continue  # the key row already shows this transfer
                via = (f"<b>{html.escape(link['key'])}</b>" if link["kind"] == "key" else
                       f"option {html.escape(' '.join(str(v) for v in (link.get('option') or {}).values()))}" if link.get("option") else KINDS[link["kind"]])
                rows.append(f"<tr><td>{via}</td><td>{_target(link['to'], screens_of, titles)}</td><td>{_cites(link['lines'])}</td></tr>")
        comes = sorted({l["from"] for p in progs for l in into.get(p, [])})
        sections.append(
            f"<h2 id=\"{html.escape(s['map'])}\"><a href=\"legacy/{html.escape(s['map'])}.html\">{html.escape(titles[s['map']])}</a> "
            f"<span class=\"muted\"><code>{html.escape(s['map'])}</code> · {', '.join(progs)}</span></h2>"
            f"<p class=\"muted\">Reached: {html.escape(r.get('reached', ''))}"
            + (f" · transaction {', '.join(r.get('transactions') or [])}" if r.get("transactions") else "")
            + (f" · from {', '.join(_target(c, screens_of, titles) for c in comes)}" if comes else "") + "</p>"
            + ('<div class="wrap"><table><tr><th>By</th><th>Goes to</th><th>Lines</th></tr>' + "".join(rows) + "</table></div>" if rows
               else '<p class="muted">No transfer found from this screen.</p>'))
    unresolved = "".join(f"<li><code>{html.escape(u['program'])}</code> {html.escape(u['kind'])} <code>{html.escape(u['expression'])}</code> at "
                         f"{_cites(u['lines'])}</li>" for u in found["unresolved"]) or '<li class="muted">None.</li>'
    c = found["counts"]
    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Screen flow</title><style>{STYLE}{MAP_STYLE}</style></head><body><main>
<p class="muted"><a href="legacy/index.html">Legacy screens</a> · {html.escape(folder.state.get('project') or '')}</p>
<h1>How the screens connect</h1>
<p class="muted">Read from the source with no model: {c['transaction']} transactions, {c['xctl']} transfers, {c['link']} calls, {c['return']} returns to another
transaction and {c['key']} key links, each with the lines that show it. {len(found['unresolved'])} transfer(s) the source leaves open.</p>
<h2>Map</h2><p class="muted">Columns by distance from the screens nothing leads to. Arrows: transfers, menu options and keys that move forward.
F3, F12, returns to the screen a user came from, links to an earlier column and transfers to the sign-on are left out; each screen below lists them.</p>
{diagram(screens, found)}
{''.join(sections)}
<h2>Left open by the source</h2><ul>{unresolved}</ul>
</main></body></html>"""
    target = folder.path(PAGE)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body)
    return target
