"""Pipeline 4, stage D1: each legacy screen drawn as a faithful 3270 copy (docs/pipeline-4.md, section 4, P4-02).

A 24 × 80 grid in the screen's own colours: labels and initial values as the map has them, input fields underlined,
dark (hidden) fields shown as hidden, bright fields bright, and fields the program fills shown as dots with their name
on hover. Under the screen: its function keys (shown on the screen, handled by its programs, and where the two
differ), its fields and what the inventory's checks found. One page per map, and an index, in outputs/design/legacy/.
Nothing is loaded from outside the page.
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

COLORS = {"BLUE": "#6aa8ff", "RED": "#ff5c5c", "PINK": "#ff86d6", "GREEN": "#4cf06a", "TURQUOISE": "#3fe0d0", "YELLOW": "#ffe74c",
          "NEUTRAL": "#f2f2f2", "DEFAULT": "#4cf06a"}
FOLDER = "outputs/design/legacy"

STYLE = """
:root{--bg:#f6f7f9;--fg:#1d232b;--muted:#5b6673;--line:#d9dee5;--card:#fff;--accent:#1f5fbf;--warn:#a5531a}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#14181d;--fg:#e6e9ed;--muted:#9aa5b1;--line:#2c333b;--card:#1b2026;--accent:#7fb0ff;--warn:#f0a36b}}
:root[data-theme="dark"]{--bg:#14181d;--fg:#e6e9ed;--muted:#9aa5b1;--line:#2c333b;--card:#1b2026;--accent:#7fb0ff;--warn:#f0a36b}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}
main{max-width:1080px;margin:0 auto;padding:24px 16px 48px}h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 8px}
.muted{color:var(--muted)}a{color:var(--accent)}code{font:13px ui-monospace,SFMono-Regular,Menlo,monospace}
.screen{background:#000;border-radius:8px;padding:14px 16px;overflow-x:auto;box-shadow:0 2px 10px rgba(0,0,0,.25);margin-top:12px}
.screen pre{margin:0;font:15px/1.35 ui-monospace,"IBM Plex Mono",Menlo,Consolas,monospace;color:#4cf06a;white-space:pre}
.f{cursor:default}.in{text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}.br{font-weight:700;filter:brightness(1.25)}
.dk{opacity:.35}.ph{opacity:.45}.rev{background:currentColor}.rev>span{color:#000}.ul{text-decoration:underline}
table{border-collapse:collapse;width:100%;background:var(--card);border:1px solid var(--line);border-radius:6px;overflow:hidden;font-size:13.5px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--muted);font-weight:600}
.tag{display:inline-block;border:1px solid var(--line);border-radius:10px;padding:0 7px;font-size:12px;margin-right:4px}
.warn{color:var(--warn)}.wrap{overflow-x:auto}
"""


def _color(f: dict[str, Any]) -> str:
    if f["color"]:
        return COLORS.get(f["color"], COLORS["DEFAULT"])
    bright = "BRT" in f["attributes"]
    if f["kind"] == "input":  # base 3270 colours when the map gives none
        return COLORS["RED"] if bright else COLORS["GREEN"]
    return COLORS["NEUTRAL"] if bright else COLORS["BLUE"]


def grid(screen: dict[str, Any]) -> str:
    """The screen as <pre> text, a span per run of cells of one field."""
    lines, columns = screen["size"]
    chars = [[" "] * columns for _ in range(lines)]
    owner: list[list[int | None]] = [[None] * columns for _ in range(lines)]
    fields = screen["fields"]
    for i, f in enumerate(fields):
        text = f["initial"]
        if not text and f["kind"] == "input":
            text = "" if "DRK" in f["attributes"] else "_" * f["length"]
        elif not text and f["kind"] == "output":
            text = "·" * f["length"]
        start = (f["line"] - 1) * columns + f["column"] - 1
        for occurrence in range(max(1, f["occurs"])):
            first = start + occurrence * (f["length"] + 1)
            for k in range(f["length"]):
                at = first + k
                if 0 <= at < lines * columns:
                    line, column = divmod(at, columns)
                    chars[line][column] = text[k] if k < len(text) else " "
                    owner[line][column] = i
    out = []
    for line in range(lines):
        row, column = [], 0
        while column < columns:
            who = owner[line][column]
            end = column
            while end < columns and owner[line][end] == who:
                end += 1
            text = html.escape("".join(chars[line][column:end]))
            if who is None:
                row.append(text)
            else:
                f = fields[who]
                classes = ["f"] + (["in"] if f["kind"] == "input" else []) + (["br"] if "BRT" in f["attributes"] else []) \
                    + (["dk"] if "DRK" in f["attributes"] else []) + (["ph"] if not f["initial"] and f["kind"] == "output" else []) \
                    + (["ul"] if f["highlight"] == "UNDERLINE" else [])
                tip = f"{f['name'] or f['kind']}: line {f['line']}, column {f['column']}, length {f['length']}; {', '.join(f['attributes']) or 'no attributes'}"
                row.append(f'<span class="{" ".join(classes)}" style="color:{_color(f)}" title="{html.escape(tip)}">{text}</span>')
            column = end
        out.append("".join(row))
    return "<pre>" + "\n".join(out) + "</pre>"


def _keys(screen: dict[str, Any]) -> str:
    keys = screen["keys"]
    shown = {k["key"]: k for k in keys["shown"]}
    handled: dict[str, list[dict[str, Any]]] = {}
    for k in keys["handled"]:
        handled.setdefault(k["key"], []).append(k)
    from reframe.design.inventory import _key_order
    rows = []
    for key in sorted(set(shown) | set(handled), key=_key_order):
        s, h = shown.get(key), handled.get(key, [])
        status = ("" if s and h else '<span class="warn">shown, handling not found</span>' if s
                  else '<span class="warn">handled, not shown on the screen</span>')
        where = "<br>".join(f"<code>{html.escape(x['program'])}</code> line {x['line']}: <code>{html.escape(x['action'][:70])}</code>" for x in h[:4])
        rows.append(f"<tr><td><b>{html.escape(key)}</b></td><td>{html.escape(s['says']) if s else '–'}</td><td>{where or '–'}</td><td>{status}</td></tr>")
    if not rows:
        return '<p class="muted">No function keys are shown or handled.</p>'
    return ('<div class="wrap"><table><tr><th>Key</th><th>The screen says</th><th>Handled in the program</th><th></th></tr>'
            + "".join(rows) + "</table></div>")


def _fields(screen: dict[str, Any]) -> str:
    rows = [f"<tr><td><code>{html.escape(f['name'] or '–')}</code></td><td>{f['kind']}</td><td>{f['line']}, {f['column']}</td><td>{f['length']}</td>"
            f"<td>{html.escape(', '.join(f['attributes']))}</td><td>{html.escape(f['color'] or '')}</td><td>{html.escape(f['initial'])}</td>"
            f"<td>{f['source_line']}</td></tr>" for f in screen["fields"] if f["kind"] != "stopper"]
    return ('<div class="wrap"><table><tr><th>Field</th><th>Kind</th><th>Line, column</th><th>Length</th><th>Attributes</th><th>Colour</th>'
            "<th>Initial text</th><th>BMS line</th></tr>" + "".join(rows) + "</table></div>")


def page(screen: dict[str, Any], project: str) -> str:
    title = screen["title"] or screen["map"]
    c = screen["counts"]
    programs = ", ".join(f"<code>{html.escape(p['name'])}</code>" for p in screen["programs"]) or '<span class="warn">none found</span>'
    problems = ("".join(f'<li class="warn">{html.escape(p)}</li>' for p in screen["problems"]) or '<li class="muted">None.</li>')
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(screen['map'])} legacy screen</title><style>{STYLE}</style></head><body><main>
<p class="muted"><a href="index.html">All legacy screens</a> · {html.escape(project)}</p>
<h1>{html.escape(title)}</h1>
<p class="muted">Map <code>{html.escape(screen['map'])}</code> in mapset <code>{html.escape(screen['mapset'])}</code>, <code>{html.escape(screen['file'])}</code> line {screen['source_line']} ·
{screen['size'][0]} × {screen['size'][1]} · {c['input']} input, {c['output']} output, {c['label']} label fields · used by {programs}</p>
<div class="screen">{grid(screen)}</div>
<p class="muted">Drawn by Reframe from the BMS source, with no model. Underlined: input fields. Dots: fields the program fills. Hover a field for its name and attributes.</p>
<h2>Function keys</h2>{_keys(screen)}
<h2>Checks</h2><ul>{problems}</ul>
<h2>Fields</h2>{_fields(screen)}
</main></body></html>"""


def index(found: dict[str, Any], project: str) -> str:
    rows = []
    for s in found["screens"]:
        keys = s["keys"]
        gaps = ", ".join([f"{k} shown, not handled" for k in keys["shown_not_handled"]] + [f"{k} handled, not shown" for k in keys["handled_not_shown"]])
        rows.append(f"<tr><td><a href=\"{html.escape(s['map'])}.html\"><b>{html.escape(s['title'] or s['map'])}</b></a></td><td><code>{html.escape(s['map'])}</code></td>"
                    f"<td>{', '.join(p['name'] for p in s['programs']) or '–'}</td><td>{s['counts']['input']}</td><td>{s['counts']['output']}</td>"
                    f"<td>{html.escape(gaps) or '–'}</td><td>{len(s['problems']) or '–'}</td></tr>")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Legacy screens</title><style>{STYLE}</style></head><body><main>
<h1>Legacy screens</h1>
<p class="muted">{html.escape(project)} · {found['maps']} maps in {found['mapsets']} mapsets, {found['fields']} fields, read from the BMS source with no model.
{found['problems']} check problem(s).</p>
<div class="wrap"><table><tr><th>Screen</th><th>Map</th><th>Programs</th><th>Inputs</th><th>Outputs</th><th>Keys that differ</th><th>Problems</th></tr>
{''.join(rows)}</table></div></main></body></html>"""


def draw_all(folder, found: dict[str, Any]) -> Path:
    project = folder.state.get("project") or ""
    target = folder.path(FOLDER)
    target.mkdir(parents=True, exist_ok=True)
    for s in found["screens"]:
        (target / f"{s['map']}.html").write_text(page(s, project))
    (target / "index.html").write_text(index(found, project))
    return target / "index.html"
