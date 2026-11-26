"""Publishing to GitHub Pages, optional (docs/release-1.md, section 3; S-16).

`reframe publish --to pages --repo <owner>/<name>` puts the cleaned copy (the same one `--to <folder>` writes) on the
repository's gh-pages branch, under <project>/<run>/, with an index of every published run, using the person's own
GitHub sign-in through git and gh. It turns Pages on for that branch if it is off. A Pages site is public, so nothing is
pushed until the person has typed yes to a warning that names the repository and the address.
"""

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Callable

from reframe.core.errors import Outcome, Stop

REPO = re.compile(r"^[A-Za-z0-9-]{1,39}/[A-Za-z0-9._-]{1,100}$")
BRANCH = "gh-pages"
Run = Callable[..., subprocess.CompletedProcess]


def _run(argv: list[str], cwd: Path | None = None, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(argv, cwd=str(cwd) if cwd else None, capture_output=True, text=True, check=check, timeout=600)


class Pages:
    def __init__(self, repo: str, run: Run = _run, remote: str | None = None) -> None:
        if not REPO.match(repo or ""):
            raise Stop(Outcome.REFUSED, "name the repository as <owner>/<name>, for example --repo my-org/reframe-reports")
        self.repo, self.run = repo, run
        self.url = remote or f"https://github.com/{repo}.git"  # a local remote only in tests

    def signed_in(self) -> None:
        if shutil.which("gh") is None:
            raise Stop(Outcome.REFUSED, "publishing to GitHub Pages uses the GitHub CLI (gh); install it, sign in with gh auth login, and run this again")
        if self.run(["gh", "auth", "status"], check=False).returncode != 0:
            raise Stop(Outcome.WAITING_SIGNIN, "the GitHub CLI is not signed in: run gh auth login, then run this again")

    def site(self) -> dict[str, Any] | None:
        found = self.run(["gh", "api", f"repos/{self.repo}/pages"], check=False)
        return json.loads(found.stdout) if found.returncode == 0 and found.stdout.strip() else None

    def address(self, site: dict[str, Any] | None) -> str:
        if site and site.get("html_url"):
            return str(site["html_url"]).rstrip("/") + "/"
        owner, name = self.repo.split("/")
        return f"https://{owner.lower()}.github.io/" + ("" if name.lower() == f"{owner.lower()}.github.io" else f"{name}/")

    def visibility(self) -> str:
        found = self.run(["gh", "repo", "view", self.repo, "--json", "visibility", "-q", ".visibility"], check=False)
        if found.returncode != 0:
            raise Stop(Outcome.REFUSED, f"GitHub has no repository {self.repo} that your sign-in can see: {found.stderr.strip()[:200]}")
        return found.stdout.strip().lower()

    def warning(self, project: str, run: str) -> str:
        site = self.site()
        where = f"{self.address(site)}{project}/{run}/"
        private = self.visibility() != "public"
        return (f"This publishes the cleaned copy of run {run} to the {BRANCH} branch of {self.repo}, at {where}\n"
                "A GitHub Pages site is public: anyone with the address can read it"
                + (", even though the repository is private (only GitHub Enterprise Cloud can limit who reads a Pages site)" if private else "")
                + ". The copy holds the project's business rules, requirements and design, cleaned of your account's identifiers.\n")

    def push(self, copy: Path, project: str, run: str) -> str:
        """The copy to <project>/<run>/ on gh-pages, the index rebuilt from what is there, and Pages on. Returns the address."""
        git = ["git", "-c", "credential.helper=", "-c", "credential.https://github.com.helper=!gh auth git-credential"]
        url = self.url
        with tempfile.TemporaryDirectory() as scratch:
            work = Path(scratch) / "site"
            cloned = self.run([*git, "clone", "--quiet", "--depth", "1", "--branch", BRANCH, url, str(work)], check=False)
            if cloned.returncode != 0:  # no gh-pages branch yet: a new one, with no history from the main branch
                work.mkdir()
                self.run([*git, "init", "--quiet"], cwd=work)
                self.run([*git, "checkout", "--quiet", "--orphan", BRANCH], cwd=work)
                self.run([*git, "remote", "add", "origin", url], cwd=work)
            target = work / project / run
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(copy, target)
            (work / ".nojekyll").write_text("")
            (work / "index.html").write_text(index(work))
            self.run([*git, "add", "--all"], cwd=work)
            if self.run([*git, "diff", "--cached", "--quiet"], cwd=work, check=False).returncode != 0:
                who = [] if self.run(["git", "config", "user.email"], cwd=work, check=False).stdout.strip() else \
                    ["-c", "user.name=Reframe", "-c", "user.email=reframe@users.noreply.github.com"]
                self.run([*git, *who, "commit", "--quiet", "-m", f"Reframe: publish {project}/{run}"], cwd=work)
                pushed = self.run([*git, "push", "--quiet", "origin", BRANCH], cwd=work, check=False)
                if pushed.returncode != 0:
                    raise Stop(Outcome.FAILED, f"git could not push to {self.repo}: {pushed.stderr.strip()[:300]}")
        site = self.site()
        if site is None:
            made = self.run(["gh", "api", "-X", "POST", f"repos/{self.repo}/pages", "-f", f"source[branch]={BRANCH}", "-f", "source[path]=/"], check=False)
            if made.returncode != 0:
                raise Stop(Outcome.FAILED, f"the copy is on {BRANCH}, but GitHub did not turn Pages on: {made.stderr.strip()[:300]}. Turn it on in the "
                                           f"repository's settings (Pages, deploy from the {BRANCH} branch)")
            site = self.site()
        return f"{self.address(site)}{project}/{run}/"


def index(site: Path) -> str:
    """The site's front page: every published run, newest first, from each copy's manifest."""
    runs = []
    for manifest in site.glob("*/*/manifest.json"):
        try:
            data = json.loads(manifest.read_text())
        except ValueError:
            continue
        runs.append((str(data.get("published_at") or ""), manifest.parent.relative_to(site).as_posix(), data))
    cards = "".join(f'<a class="card" href="{html.escape(path)}/"><h2>{html.escape(str(d.get("project") or path))}</h2>'
                    f'<p>Run {html.escape(str(d.get("run") or ""))}, published {html.escape(at[:10])}</p></a>'
                    for at, path, d in sorted(runs, reverse=True))
    return ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
            "<title>Reframe reports</title><style>:root{--bg:#f6f6f3;--panel:#fff;--ink:#1d1d1b;--muted:#5f5f5a;--line:#e1e0da;--accent:#2f5d8a}"
            "@media (prefers-color-scheme:dark){:root{--bg:#151514;--panel:#1e1e1c;--ink:#ecebe6;--muted:#a5a49e;--line:#33332f;--accent:#8db6df}}"
            "body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}"
            "main{max-width:900px;margin:0 auto;padding:32px 24px}.muted{color:var(--muted)}"
            ".card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:12px;"
            "text-decoration:none;color:var(--ink)}.card:hover{border-color:var(--accent)}.card h2{margin:0 0 4px;font-size:18px}.card p{margin:0;color:var(--muted)}"
            "</style></head><body><main><h1>Reframe reports</h1><p class=\"muted\">Mainframe assessments published by Reframe, cleaned of the "
            "identifiers of the accounts that ran them. Each is model output, for people to review.</p>" + cards + "</main></body></html>\n")
