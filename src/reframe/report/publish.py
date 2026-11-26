"""`reframe publish`: a cleaned copy of a run's reports, for people who don't run Reframe (docs/sharing.md, S-01).

The copy holds AWS Transform's review (aws/), Claude's review (claude/), the comparison (comparison/), the plugin's own
report and map (claude/plugin/) and an index page. The three Reframe pages are rendered again from their data with
links that work inside the copy. Every file is then cleaned of the run's identifiers, and the whole copy is checked
for each kind; if any is left, nothing is written and the file is named.
"""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import RunFolder, iso

UUID = re.compile(r"(?<![0-9a-f])[0-9a-f]{8}[-_][0-9a-f]{4}[-_][0-9a-f]{4}[-_][0-9a-f]{4}[-_][0-9a-f]{12}(?![0-9a-f])", re.I)
ARN = re.compile(r"\barn:aws[a-z-]*:[a-z0-9-]*:[a-z0-9-]*:\d{0,12}:[^\s\"'<>\\]+", re.I)
S3_URI = re.compile(r"\bs3://[a-z0-9][a-z0-9.\-]{1,62}", re.I)
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
ACCOUNT = re.compile(r"(?<![\d.])\d{12}(?![\d.])")


class Cleaner:
    """The run's own identifiers, and the generic kinds, replaced by placeholders."""

    def __init__(self, folder: RunFolder) -> None:
        state = folder.state
        self.exact: list[tuple[str, str]] = []
        account = str(state.get("account") or "")
        if re.fullmatch(r"\d{12}", account):
            self.exact.append((account, "<account>"))
        home = str(Path.home())
        self.exact.append((home, "~"))
        user = os.environ.get("USER", "")
        if len(user) >= 4:
            self.exact.append((f"/Users/{user}", "~"))
        profile = str(state.get("profile") or "")
        self.profile = re.compile(rf"(?<![\w-]){re.escape(profile)}(?![\w-])") if len(profile) >= 3 else None
        project, run = state.get("project", ""), folder.root.name
        self.resources = re.compile(rf"\breframe-{re.escape(project)}-{run}[a-z0-9-]*", re.I) if project else None

    def clean(self, text: str) -> str:
        text = ARN.sub("<arn>", text)  # first: an ARN holds the account ID, which would no longer match once replaced
        for old, new in self.exact:
            text = text.replace(old, new)
        text = S3_URI.sub("s3://<bucket>", text)
        if self.resources is not None:
            text = self.resources.sub("<run resource>", text)
        # each distinct ID gets a stable stand-in, so keys and links that use it stay unique
        text = UUID.sub(lambda m: "id-" + hashlib.sha256(m.group(0).lower().replace("_", "-").encode()).hexdigest()[:10], text)
        text = EMAIL.sub("<email>", text)
        if self.profile is not None:
            text = self.profile.sub("<profile>", text)
        return text

    def left(self, text: str) -> list[str]:
        found = []
        for name, pattern in (("an ARN", ARN), ("an S3 location", re.compile(r"s3://(?!<bucket>)[a-z0-9]", re.I)), ("an ID", UUID), ("an e-mail address", EMAIL)):
            if pattern.search(text):
                found.append(name)
        for old, _ in self.exact:
            if old in text:
                found.append("an account ID" if old.isdigit() else "a local path")
        if self.profile is not None and self.profile.search(text):
            found.append("the AWS profile name")
        if self.resources is not None and self.resources.search(text):
            found.append("a run resource name")
        return found


def run_keys(folder: RunFolder, keys: Iterable[str]) -> dict[str, str]:
    """Each key as a published copy names it (cleaned: an AWS Transform ID becomes a stand-in) -> the key the run uses,
    for every key that cleaning changes. A review downloaded from a published copy names items by the cleaned keys."""
    cleaner = Cleaner(folder)
    return {cleaned: key for key in keys if (cleaned := cleaner.clean(key)) != key}


def _render(template: str, data: dict[str, Any], title: str) -> str:
    payload = json.dumps(data, default=str).replace("</", "<\\/")
    return template.replace("/*DATA*/", payload).replace("{{title}}", html.escape(title))


def _retarget(value: Any, moves: dict[str, str]) -> Any:
    text = json.dumps(value, default=str)
    for old, new in moves.items():
        text = text.replace(old, new)
    return json.loads(text)


INDEX = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>:root{{--bg:#f6f6f3;--panel:#fff;--ink:#1d1d1b;--muted:#5f5f5a;--line:#e1e0da;--accent:#2f5d8a}}
@media (prefers-color-scheme:dark){{:root{{--bg:#151514;--panel:#1e1e1c;--ink:#ecebe6;--muted:#a5a49e;--line:#33332f;--accent:#8db6df}}}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}}
main{{max-width:900px;margin:0 auto;padding:32px 24px}}a{{color:var(--accent)}}.muted{{color:var(--muted)}}
.card{{display:block;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:12px;text-decoration:none;color:var(--ink)}}
.card:hover{{border-color:var(--accent)}}.card h2{{margin:0 0 4px;font-size:18px}}.card p{{margin:0;color:var(--muted)}}
table{{border-collapse:collapse;font-size:14px;margin-top:18px}}td{{padding:4px 14px 4px 0;vertical-align:top}}td:first-child{{color:var(--muted)}}</style></head>
<body><main>
<h1>{heading}</h1>
<p class="muted">{lead}</p>
{cards}
<table>{rows}</table>
<p class="muted" style="margin-top:24px">Both assessments are model output: two runs of either tool can differ. Claude's business functions, capabilities and
requirements were generated by Reframe from the plugin's results. Review marks you make stay in your browser; download them from each review.
Published by Reframe {published}; identifiers of the AWS account that ran it are removed.</p>
</main></body></html>
"""


# macOS keeps these folders private: a browser that has not been given access to one can open the page you open there,
# but not the pages it links to, so every link in a copy published there fails (found 24 November 2026).
PROTECTED = ("Desktop", "Documents", "Downloads")


def protected_folder(target: Path, platform: str = sys.platform, home: Path | None = None) -> str | None:
    """The macOS privacy-protected folder that holds `target`, if any."""
    if platform != "darwin":
        return None
    home = (home or Path.home()).resolve()
    for name in PROTECTED:
        if target.resolve().is_relative_to(home / name):
            return name
    return None


def protected_warning(target: Path) -> str | None:
    """What to tell someone who writes a report into a macOS-protected folder, if they did."""
    name = protected_folder(target)
    if not name:
        return None
    return (f"{target} is inside your {name} folder, which macOS keeps private: unless your browser has access to that folder, index.html "
            "opens but its links do not. Use a folder outside Desktop, Documents and Downloads (for example "
            f"~/reframe-reports/{target.name}), or give the browser access in System Settings > Privacy & Security > Files and Folders.")


def _design_pages(folder: RunFolder) -> dict[str, str]:
    """Pipeline 4's pages as they are in outputs/design/ (the design page, the legacy screens, the flow, the journeys,
    the modern screens and the prototype) and the latest version of the package, all under design/."""
    base = folder.root / "outputs" / "design"
    if not (base / "index.html").is_file():
        return {}
    versions = sorted((int(p.name[1:]), p) for p in (base / "package").glob("v*") if p.is_dir() and p.name[1:].isdigit())
    latest = versions[-1][1] if versions else None
    found = {}
    for p in sorted(base.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in (".html", ".md", ".json"):
            continue
        rel = p.relative_to(base)
        if rel.parts[0] == "package":
            if latest is None or latest not in p.parents:
                continue
            rel = Path("package") / p.relative_to(latest)
        found[f"design/{rel.as_posix()}"] = p.read_text(errors="replace")
    return found


def publish(folder: RunFolder, target: Path) -> dict[str, Any]:
    from reframe.claude.workspace import paths
    from reframe.report import build, compare
    state = folder.state
    if not folder.exists("outputs/requirements"):
        raise Stop(Outcome.REFUSED, "this run has no AWS Transform results to publish yet")
    claude = folder.exists("outputs/claude/model.json") and folder.exists("outputs/claude/requirements.json")
    both = claude and (state.get("claude") or {}).get("status") == "DONE"
    reconciled = both and folder.exists("outputs/reconcile/rules.json") and (state.get("reconcile") or {}).get("status") == "DONE"
    to_reconciled = [["Reconciled review", "../reconciled/index.html"]] if reconciled else []
    cleaner = Cleaner(folder)
    pages: dict[str, str] = {}
    aws = build.collect(folder)
    aws["nav"] = ([["Claude's review", "../claude/index.html"], ["AWS Transform and Claude compared", "../comparison/index.html"]] if both else []) + to_reconciled
    aws["links"] = {}  # AWS's own pages are not part of the copy
    pages["aws/index.html"] = _render(build.TEMPLATE, aws, f"Business review: {aws['project']}")
    if claude:
        data = build.collect_claude(folder)
        data["nav"] = [["AWS Transform's review", "../aws/index.html"]] + ([["AWS Transform and Claude compared", "../comparison/index.html"]] if both else []) + to_reconciled
        data["links"] = {"pages": [["The plugin's own report", "plugin/REPORT.html", "REPORT.html"], ["The plugin's interactive map", "plugin/TOPOLOGY.html", "TOPOLOGY.html"]]}
        pages["claude/index.html"] = _render(build.TEMPLATE, data, f"Business review (Claude): {data['project']}")
        analysis = paths(folder)["analysis"]
        for name in ("REPORT.html", "TOPOLOGY.html"):
            if (analysis / name).exists():
                pages[f"claude/plugin/{name}"] = (analysis / name).read_text(errors="replace")
    if both:
        data = _retarget(compare.model(folder), {"../claude/report/index.html": "../claude/index.html", "../report/index.html": "../aws/index.html"})
        data["links"]["reconciled"] = "../reconciled/index.html" if reconciled else None
        page = _render(compare.TEMPLATE, data, f"AWS Transform and Claude compared: {data['project']}")
        pages["comparison/index.html"] = page.replace('href="../claude/report/index.html"', 'href="../claude/index.html"').replace('href="../report/index.html"', 'href="../aws/index.html"')
    if reconciled:
        from reframe.report import reconciled as reconciled_page
        data = _retarget(reconciled_page.collect_reconciled(folder), {"../claude/report/index.html": "../claude/index.html", "../report/index.html": "../aws/index.html"})
        pages["reconciled/index.html"] = _render(build.TEMPLATE, data, f"Reconciled review: {data['project']}")
    designed = _design_pages(folder)
    pages.update(designed)
    snapshot = folder.load("snapshot.json") or {}
    plugin = (state.get("claude") or {}).get("plugin") or {}
    cards = [("aws/index.html", "AWS Transform's business review", "Business domains, functions, capabilities, requirements and business rules, from overview down to each requirement.")]
    if claude:
        cards.append(("claude/index.html", "Claude's business review", "The code-modernization plugin's rule cards, with requirements generated by Reframe from them, in the same layout."))
    if both:
        cards.append(("comparison/index.html", "AWS Transform and Claude compared", "The numbers side by side, domains aligned by shared programs, rules by program, AI-paired rules, and what only one tool found."))
    if reconciled:
        cards.append(("reconciled/index.html", "Reconciled review", "Both assessments reconciled against the source code: recommended rules with their evidence, recommended requirements, and one SME list."))
    if designed:
        cards.append(("design/index.html", "The design", "The modernized application: legacy and modern screens, journeys, the clickable prototype, a final "
                      "specification for every capability, and the AI-DLC package in Kiro, Claude Code and Spec Kit form."))
    rows = [("Source", snapshot.get("source") if str(snapshot.get("source", "")).startswith("http") else Path(str(snapshot.get("source") or "")).name),
            ("Commit", snapshot.get("commit") or "–"), ("Snapshot SHA-256", snapshot.get("sha256")), ("Files", snapshot.get("files")),
            ("AWS Transform results", state.get("retrieved_at")), ("Claude assessment", (state.get("claude") or {}).get("finished_at") or "–"),
            ("Code-modernization plugin", f"{plugin.get('version')} at {str(plugin.get('commit', ''))[:12]}" if plugin else "–")]
    pages["index.html"] = INDEX.format(
        title=html.escape(f"Reframe: {state.get('project')}"), heading=html.escape(f"Assessment of {rows[0][1]}"),
        lead="The same source snapshot assessed by AWS Transform" + (" and by Claude's code-modernization plugin" if claude else "") + ", for review in a browser.",
        cards="".join(f'<a class="card" href="{href}"><h2>{html.escape(t)}</h2><p>{html.escape(d)}</p></a>' for href, t, d in cards),
        rows="".join(f"<tr><td>{html.escape(k)}</td><td>{html.escape(str(v))}</td></tr>" for k, v in rows), published=iso()[:10])
    cleaned = {name: cleaner.clean(text) for name, text in pages.items()}
    problems = [f"{name}: {', '.join(found)}" for name, text in cleaned.items() if (found := cleaner.left(text))]
    if problems:
        raise Stop(Outcome.REFUSED, "the cleaned copy still holds identifiers, so nothing was written: " + "; ".join(problems))
    target.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=target.parent) as scratch:
        staged = Path(scratch) / "copy"
        for name, text in cleaned.items():
            path = staged / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        manifest = {"published_at": iso(), "run": folder.root.name, "project": state.get("project"), "source_sha256": snapshot.get("sha256"),
                    "commit": snapshot.get("commit"), "files": sorted(cleaned)}
        (staged / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
        for old in ("aws", "claude", "comparison", "reconciled", "design", "index.html", "manifest.json"):
            existing = target / old
            if existing.is_dir():
                shutil.rmtree(existing)
            elif existing.exists():
                existing.unlink()
        for item in staged.iterdir():
            shutil.move(str(item), target / item.name)
    folder.event("published", files=len(cleaned), target=str(target))
    return manifest
