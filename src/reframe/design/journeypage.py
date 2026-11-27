"""Pipeline 4, stage D3: the journeys as a page (docs/pipeline-4.md, section 4, P4-04).

outputs/design/journeys.html: by domain, each journey with its role and goal, its steps linked to the 3270 copies, and
the capabilities and requirements it serves; the screens in no journey with the reason; and what Reframe's checks still
found. Nothing is loaded from outside the page.
"""

from __future__ import annotations

import html
from pathlib import Path
from typing import Any

from reframe.design.legacy import STYLE

PAGE = "outputs/design/journeys.html"
EXTRA = """
.journey{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px 16px;margin:12px 0}
.journey h3{margin:0 0 2px;font-size:16px}.steps{margin:8px 0 6px;padding-left:22px}.steps li{margin:2px 0}
details{margin-top:6px}summary{cursor:pointer;color:var(--muted);font-size:13.5px}
"""


def draw(folder, value: dict[str, Any]) -> Path:
    screens = {s["map"]: s for s in (folder.load("design/screens.json") or {}).get("screens") or []}
    requirements = folder.load("outputs/reconcile/requirements.json") or {}
    cap_title, req_text = {}, {}
    for fid, body in (requirements.get("functions") or {}).items():
        page = "rec/" + (fid or "unassigned")
        for cap in body.get("capabilities") or []:
            cap_title[f"{page}#{cap['number']}"] = cap["title"]
            for r in cap.get("requirements") or []:
                req_text[f"{page}/{r['code']}"] = (r["code"], r["text"])

    def screen(m: str) -> str:
        s = screens.get(m)
        return f'<a href="legacy/{html.escape(m)}.html">{html.escape((s or {}).get("title") or m)}</a> <code>{html.escape(m)}</code>'

    parts: list[str] = []
    by_domain: dict[str, Any] = {}
    for j in value["journeys"]:
        by_domain.setdefault(j["domain_name"], []).append(j)
    for name, journeys in by_domain.items():
        parts.append(f"<h2>{html.escape(name)}</h2>")
        for j in journeys:
            steps = "".join(f"<li>{screen(s['screen'])}: {html.escape(s['action'])}</li>" for s in j["steps"])
            caps = "".join(f"<li>{html.escape(cap_title.get(k, k))} <code>{html.escape(k)}</code></li>" for k in j["capabilities"])
            reqs = "".join(f"<li><code>{html.escape(req_text.get(k, (k, ''))[0])}</code> {html.escape(req_text.get(k, ('', ''))[1])}</li>" for k in j["requirements"])
            parts.append(f'<div class="journey"><h3>{html.escape(j["id"])} {html.escape(j["name"])}</h3>'
                         f'<p class="muted">{html.escape(j["role"])} · {html.escape(j["goal"])}</p><ol class="steps">{steps}</ol>'
                         f"<details><summary>{len(j['capabilities'])} capabilities, {len(j['requirements'])} requirements</summary>"
                         f"<ul>{caps}</ul><ul>{reqs}</ul></details></div>")
    unused = "".join(f"<li>{screen(u['screen'])}: {html.escape(u['reason'])}</li>" for u in value["unused"]) or '<li class="muted">None.</li>'
    problems = "".join(f'<li class="warn">{html.escape(p)}</li>' for p in value["problems"]) or '<li class="muted">None.</li>'
    in_journeys = {s["screen"] for j in value["journeys"] for s in j["steps"]}
    body = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>User journeys</title><style>{STYLE}{EXTRA}</style></head><body><main>
<p class="muted"><a href="legacy/index.html">Legacy screens</a> · <a href="flow.html">Screen flow</a> · {html.escape(folder.state.get('project') or '')}</p>
<h1>User journeys</h1>
<p class="muted">{len(value['journeys'])} journeys over {len(in_journeys)} of {len(screens)} screens, grouped by a Claude step per domain and checked by Reframe:
every step follows a link in the screen flow, and every capability and requirement cited exists. Model output, for review.</p>
{''.join(parts)}
<h2>Screens in no journey</h2><ul>{unused}</ul>
<h2>What the checks still found</h2><ul>{problems}</ul>
</main></body></html>"""
    target = folder.path(PAGE)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body)
    return target
