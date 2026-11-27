"""Pipeline 4, stage D5: the clickable prototype (docs/pipeline-4.md, section 4, P4-06).

Reframe draws one static HTML app from the modern screens (stage D4), with no model and nothing loaded from outside:

- a route per modern screen (#/S-ACCOUNT-VIEW), the shared screens' header and navigation around them, and every
  button and link that opens a screen working; a link to a screen that replaces nothing (the shell) goes Home;
- sample data shaped by each field: its legacy length and attributes and what the component says it shows (a date, an
  amount, an 11-digit number), filled from a fixed seed so every build shows the same data, and taken from the rules'
  worked examples where they give a value for the field;
- validations and messages in the rules' own words: an action on a screen with an empty field whose check says it is
  required shows that check's message;
- on each screen, "Show the legacy screen" opens the 3270 copies it replaces, with the mapping of their fields;
- a journeys page that walks each journey through the modern screens;
- marks, as on the review pages: Agree, Needs change or Question with a comment on each screen and component, and
  sign-off by journey, kept in the browser and downloaded as JSON or CSV in the reframe-review/1 format with the tool
  "Reframe's design".

    python -m reframe.design.prototype [--run <run>]

writes outputs/design/prototype/index.html.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PAGE = "outputs/design/prototype/index.html"
TOOL = "Reframe's design"
INPUTS = {"text", "number", "money", "date", "select", "checkbox", "radio", "password", "search"}
FIRST = ["Maria", "James", "Aiko", "Omar", "Grace", "Luis", "Priya", "Tom", "Elena", "Kwame"]
LAST = ["Garcia", "Smith", "Tanaka", "Haddad", "Okafor", "Silva", "Patel", "Brown", "Novak", "Mensah"]
STREETS = ["Maple Street", "Harbor Road", "Oak Avenue", "Station Lane", "Hill Drive"]
CITIES = [("Springfield", "IL", "62704"), ("Portland", "OR", "97205"), ("Austin", "TX", "78701"), ("Albany", "NY", "12207")]


def _seed(*parts: str) -> int:
    return int(hashlib.sha256("|".join(parts).encode()).hexdigest()[:12], 16)


def sample(label: str, shows: str, length: int, seed: int) -> str:
    """A believable value for a field, from its label, what it shows and its legacy length; the same seed gives the same
    value."""
    text = f"{label} {shows}".lower()
    digits = re.search(r"(\d+)[- ]digit", text)
    r = seed
    pick = lambda items: items[r % len(items)]  # noqa: E731
    if "ssn" in text or "social security" in text:
        return f"***-**-{r % 9000 + 1000}"
    if "phone" in text:
        return f"({r % 800 + 200}) {r % 900 + 100}-{r % 9000 + 1000}"
    if "zip" in text or "postal" in text:
        return pick(CITIES)[2]
    if re.search(r"\bstate\b", text):
        return pick(CITIES)[1]
    if "city" in text:
        return pick(CITIES)[0]
    if "country" in text:
        return "USA"
    if "address" in text or "street" in text:
        return f"{r % 900 + 100} {pick(STREETS)}"
    if "first name" in text:
        return pick(FIRST)
    if "last name" in text:
        return pick(LAST)
    if "middle" in text:
        return pick(FIRST)[0] + "."
    if "name" in text and "user" not in text and "program" not in text:
        return f"{pick(FIRST)} {LAST[(r // 7) % len(LAST)]}"
    if "fico" in text or "score" in text:
        return str(580 + r % 270)
    if "date" in text or "expir" in text or "opened" in text or "reissu" in text or "birth" in text:
        y, m, d = 2020 + r % 7, r % 12 + 1, r % 28 + 1
        return f"{m:02d}/{d:02d}/{y % 100:02d}" if "mm/dd/yy" in text else f"{y}-{m:02d}-{d:02d}"
    if "time" in text:
        return f"{r % 24:02d}:{r % 60:02d}:{(r // 60) % 60:02d}"
    if any(w in text for w in ("amount", "balance", "limit", "credit", "debit", "payment", "money", "fee", "interest")):
        return f"${(r % 900000) / 100 + 10:,.2f}"
    if "status" in text or "active" in text or "y/n" in text:
        return pick(["Active", "Active", "Inactive"])
    if "type" in text and ("user" in text or "admin" in text):
        return pick(["Regular user", "Administrator"])
    if "user id" in text or "userid" in text:
        return f"USER{r % 9000 + 1000:04d}"[:8]
    if digits or "number" in text or re.search(r"\bid\b", text) or "account" in text or "card" in text:
        n = int(digits.group(1)) if digits else max(4, min(length or 11, 16))
        return "".join(str((r >> i) % 10) for i in range(n)).replace("0", "4", 1)
    if "description" in text or "desc" in text:
        return pick(["Grocery store purchase", "Online subscription", "Fuel", "Restaurant", "Cash withdrawal"])
    return pick(["Sample value", "Example", "Demo data"])


def quoted(text: str) -> list[str]:
    return [a or b for a, b in re.findall(r"'([^']{3,})'|\"([^\"]{3,})\"", text or "")]


def build(screens: dict[str, Any], modern: dict[str, Any], journeys: dict[str, Any], rules: list[dict[str, Any]], project: str) -> dict[str, Any]:
    """The prototype's data: screens with components and sample values, the shell, routes, journeys and legacy copies."""
    from reframe.design.legacy import grid
    examples = {r["key"]: r.get("examples") or [] for r in rules}
    legacy = {s["map"]: s for s in screens["screens"]}
    all_screens = modern["screens"]
    rendered = [s for s in all_screens if s.get("replaces")]
    shells = [s for s in all_screens if not s.get("replaces")]
    ids = {s["id"] for s in rendered}
    outgoing = Counter(s["id"] for s in rendered for c in s.get("components") or [] if c.get("goes_to") in ids)
    home = max(outgoing, key=lambda k: (outgoing[k], k)) if outgoing else (rendered[0]["id"] if rendered else "")
    entry_map = next((r["screen"] for r in (screens.get("reach") or [])), None)
    start = next((s["id"] for s in rendered if any("SGN" in m or "SIGN" in m for m in s["replaces"])), None) or home

    def route(target: str) -> str:
        return target if target in ids else home if target else ""

    mapping_by_legacy = defaultdict(list)
    for d in modern["domains"].values():
        for m in d["mapping"]:
            mapping_by_legacy[m["legacy_screen"]].append({k: m.get(k, "") for k in ("legacy", "kind", "how", "becomes", "why")})

    def value_for(sid: str, c: dict[str, Any]) -> str:
        words = set(re.findall(r"[a-z]{3,}", (c.get("label") or "").lower()))
        for key in c.get("rules") or []:
            for ex in examples.get(key, []):
                for g in ex.get("given") or []:
                    if words & set(re.findall(r"[a-z]{3,}", str(g.get("field", "")).lower())):
                        v = str(g.get("value", "")).strip().strip("'\"")
                        if v and len(v) <= 40:
                            return v
        return sample(c.get("label", ""), c.get("shows", ""), 0, _seed(project, sid, c.get("id", "")))

    out = []
    for s in rendered:
        comps = []
        for c in s.get("components") or []:
            kind = str(c.get("type", "")).lower()
            item = {k: c.get(k, "") for k in ("id", "label", "section", "shows", "validation", "keyboard")}
            item.update({"type": kind, "goes_to": route(c.get("goes_to", "")), "rules": len(c.get("rules") or []),
                         "messages": quoted(c.get("validation", "")) + (quoted(c.get("shows", "")) if kind == "message" else [])})
            if kind == "display":
                item["value"] = value_for(s["id"], c)
            elif kind in INPUTS:
                item["sample"] = value_for(s["id"], c)
                item["required"] = bool(re.search(r"required|blank|no input|must (be|enter)|cannot be empty|empty", c.get("validation", ""), re.I))
            elif kind == "table":
                head = re.split(r"[;.]", c.get("shows", ""))[0]
                cols = [x.strip(" ,") for x in re.split(r",| and ", head) if x.strip(" ,")][:7] or ["Item", "Detail"]
                item["columns"] = cols
                item["rows"] = [[sample(col, col, 0, _seed(project, s["id"], c.get("id", ""), str(n), col)) for col in cols] for n in range(6)]
            comps.append(item)
        success = ""
        for c in s.get("components") or []:
            if str(c.get("type", "")).lower() != "message":
                continue
            m = re.search(r"success\w*\W[^']*'([^']+)'", c.get("shows", ""), re.I)
            if m:
                success = m.group(1)
                break
            if re.search(r"success|saved|added|updated|deleted|submitted|confirm", c.get("label", ""), re.I) and \
                    not re.search(r"error|invalid|fail|problem", c.get("label", "") + c.get("shows", ""), re.I) and quoted(c.get("shows", "")):
                success = quoted(c.get("shows", ""))[0]
                break
        row_target = next((c["goes_to"] for c in comps if c["type"] in ("link", "button") and c["goes_to"] and c["goes_to"] != s["id"]
                           and re.search(r"view|detail|edit|open|select|update", c["label"], re.I)), "")
        out.append({"id": s["id"], "title": s["title"], "purpose": s.get("purpose", ""), "domain": s.get("domain", ""), "journeys": s.get("journeys") or [],
                    "replaces": s["replaces"], "components": comps, "row_target": row_target, "success": success})
    nav, seen = [], set()
    for sh in shells:
        for c in sh.get("components") or []:
            target = c.get("goes_to")
            if c.get("type") == "link" and target in ids and target not in seen:
                seen.add(target)
                nav.append({"label": c.get("label", target), "to": target, "group": c.get("section", "")})
    app = next((c.get("label") for sh in shells for c in sh.get("components") or [] if c.get("type") == "header" and c.get("label")), project)
    by_legacy = defaultdict(list)
    for s in rendered:
        for m in s["replaces"]:
            by_legacy[m].append(s["id"])
    walk = []
    for j in journeys.get("journeys") or []:
        steps, last = [], None
        for st in j["steps"]:
            target = (by_legacy.get(st["screen"]) or [None])[0]
            if target and target != last:
                steps.append({"screen": target, "legacy": st["screen"], "action": st["action"]})
                last = target
            elif target:
                steps[-1]["action"] += "; " + st["action"]
        walk.append({"id": j["id"], "name": j["name"], "role": j["role"], "goal": j["goal"], "domain": j.get("domain_name", ""), "steps": steps})
    return {"project": project, "app": app, "home": home, "start": start, "screens": out, "nav": nav, "journeys": walk,
            "legacy": {m: {"title": legacy[m]["title"] or m, "grid": grid(legacy[m]), "mapping": mapping_by_legacy.get(m, [])} for m in by_legacy if m in legacy},
            "source": {"sha256": ""}, "tool": TOOL, "entry": entry_map}


TOKENS = ("bg", "fg", "muted", "line", "card", "accent", "accent-fg", "warn", "ok", "soft")


def token_style(tokens: dict[str, Any] | None) -> str:
    """The design system's tokens (design-system/tokens.json in the context folder) as the prototype's colours and font:
    {"accent": "#0b5", ...}, or the same under "colors", and "font" for the font family. Other names are left out."""
    if not isinstance(tokens, dict):
        return ""
    colors = {**{k: v for k, v in tokens.items() if k in TOKENS}, **{k: v for k, v in (tokens.get("colors") or {}).items() if k in TOKENS}}
    safe = lambda v: re.fullmatch(r"[#\w\s,.%()'\"-]{1,80}", str(v)) is not None  # noqa: E731
    rules = "".join(f"--{k}:{v};" for k, v in colors.items() if safe(v))
    font = str(tokens.get("font") or "")
    css = (f":root,:root[data-theme]{{{rules}}}" if rules else "") + (f"body{{font-family:{font}}}" if font and safe(font) else "")
    return f"<style>{css}</style>" if css else ""


def draw(folder, data: dict[str, Any], tokens: dict[str, Any] | None = None) -> Path:
    data = {**data, "source": {"sha256": (folder.load("snapshot.json") or {}).get("sha256", "")}, "run": folder.root.name}
    template = (Path(__file__).with_name("prototype.html")).read_text()
    page = template.replace("/*DATA*/", json.dumps(data, default=str).replace("</", "<\\/")).replace("{{title}}", html.escape(f"{data['app']} prototype"))
    page = page.replace("</head>", token_style(tokens) + "</head>", 1)
    target = folder.path(PAGE)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page)
    return target


def main(argv: list[str] | None = None) -> int:
    import argparse
    from reframe.core.runfolder import find_run
    parser = argparse.ArgumentParser(prog="python -m reframe.design.prototype", description="The clickable prototype (P4-06)")
    parser.add_argument("--run", help="the run (default: the latest run)")
    args = parser.parse_args(argv)
    folder = find_run(args.run)
    screens, modern, journeys = folder.load("design/screens.json"), folder.load("design/modern.json"), folder.load("design/journeys.json")
    if not screens or not modern or not journeys:
        print("Run the screen inventory, the flow, the journeys and the modern screens first.")
        return 2
    rules = (folder.load("outputs/reconcile/rules.json") or {}).get("rules") or []
    data = build(screens, modern, journeys, rules, folder.state.get("project") or "")
    page = draw(folder, data)
    print(json.dumps({"screens": len(data["screens"]), "journeys": len(data["journeys"]), "legacy": len(data["legacy"]), "start": data["start"],
                      "home": data["home"], "size_kb": round(page.stat().st_size / 1024), "page": str(page)}, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
