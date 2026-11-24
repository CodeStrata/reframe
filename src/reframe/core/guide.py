"""The guided `reframe run` and `reframe setup` (specification section 3, "The guided run").

Each step asks in the terminal and checks the answer before going on: prerequisites (installed only on a yes), the AWS
sign-in (the person signs in in their browser; Reframe never sees credentials), the source, the choices, a summary,
then one yes to start. The answers become the next run's defaults.
"""

from __future__ import annotations

import re
import shlex
import subprocess
import zipfile
from pathlib import Path
from typing import Any

from reframe.core import setup, ui
from reframe.core.shell import base_environment

REGION = re.compile(r"^[a-z]{2}(-[a-z]+)+-\d$")


# ---- 1. prerequisites ------------------------------------------------------------------------------


def _show(tools: list[setup.Tool]) -> None:
    rows = []
    for t in tools:
        status = "[green]✓ ready[/]" if t.ready else "[dim]optional[/]" if t.optional else "[red]✗ missing[/]"
        found = t.found or "—"
        rows.append((t.name, t.needed, found + (f"  [dim]{t.note}[/]" if t.note else ""), status))
    from rich.table import Table
    from rich import box
    grid = Table(box=box.SIMPLE, expand=True, show_edge=False)
    for name in ("Tool", "Needs", "Found", ""):
        grid.add_column(name, overflow="fold")
    for row in rows:
        grid.add_row(*row)
    ui.console.print(grid)


def _install(tool: setup.Tool, m: setup.Machine) -> None:
    if tool.install == "reframe-plugin":
        from reframe.claude import plugin
        ui.say(f"Reframe fetches Claude's code-modernization plugin {plugin.VERSION} from Anthropic's plugin repository at one pinned commit "
               "into ~/.reframe/tools, and loads it only for its own Claude runs. Nothing is installed into your Claude Code settings.")
        if not ui.yes(f"Fetch it now? ({tool.note})", default=True):
            return
        try:
            with ui.console.status("Fetching the plugin…"):
                plugin.fetch()
            ui.ok(f"code-modernization plugin {plugin.VERSION} ready")
        except Exception as error:  # noqa: BLE001 - shown to the person; nothing was changed
            ui.fail(f"The plugin was not fetched: {error}")
        return
    if tool.install == "reframe":
        ui.say(f"Reframe can install Terraform {setup.TERRAFORM_VERSION} for {m.name} from HashiCorp, check it against "
               "HashiCorp's SHA-256 sums, and keep it in ~/.reframe/tools. Your PATH and shell files are not changed.")
        if not ui.yes(f"Install Terraform {setup.TERRAFORM_VERSION} now?"):
            return
        try:
            with ui.console.status("Downloading and checking Terraform…"):
                path = setup.install_terraform(m)
            ui.ok(f"Terraform {setup.TERRAFORM_VERSION} installed at {path}")
        except (RuntimeError, OSError, subprocess.SubprocessError) as error:
            ui.fail(f"Terraform was not installed: {error}")
        return
    ui.say(f"To install {tool.name} on {m.name}, Reframe would run:")
    ui.command(tool.install or "")
    if tool.optional:
        prompt, default = f"Install {tool.name} now? ({tool.note})", False
    else:
        prompt, default = f"Run it now?", True
    if ui.yes(prompt, default):
        if setup.run_in_terminal(tool.install or ""):
            ui.ok(f"{tool.name}: the install command finished")
        else:
            ui.fail(f"{tool.name}: the install command did not finish; see its output above")
        setup.use_saved_paths()


def prerequisites(m: setup.Machine) -> bool:
    ui.section("1  Prerequisites")
    ui.hint(f"What a run needs, checked on {m.name}.")
    offered: set[str] = set()
    while True:
        with ui.console.status("Checking…"):
            tools = setup.check(m)
        _show(tools)
        required = [t for t in tools if not t.ready and not t.optional]
        optional = [t for t in tools if not t.ready and t.optional and t.install and t.key not in offered]
        if not required and not optional:
            ui.ok("Everything a run needs is ready.")
            return True
        uv_missing = not next(t for t in tools if t.key == "uv").ready
        claude_missing = not next(t for t in tools if t.key == "claude").ready
        todo = [t for t in required + optional if t.key not in offered and not (t.key == "mcp" and uv_missing)
                and not (t.key == "plugin" and claude_missing)]
        if not todo:
            break  # every missing tool was offered once; what is left was declined, did not install, or waits for uv
        for tool in todo:
            offered.add(tool.key)
            ui.console.print()
            if not tool.install:
                ui.warn(f"{tool.name}: Reframe has no install command for {m.name}. Install it, then run reframe run again.")
                continue
            _install(tool, m)
        setup.use_saved_paths()
    missing = [t for t in setup.check(m) if not t.ready and not t.optional]
    if not missing:
        ui.ok("Everything a run needs is ready.")
        return True
    ui.console.print()
    ui.fail("Still missing: " + ", ".join(t.name for t in missing) + ".")
    for t in missing:
        if t.install == "reframe":
            ui.say(f"{t.name}: run reframe run again and answer yes to let Reframe install it, or point Reframe at your own "
                   f"{t.needed} build with REFRAME_TERRAFORM=/path/to/terraform.")
        elif t.install:
            ui.say(f"{t.name}:")
            ui.command(t.install)
    ui.hint("Then run reframe run again.")
    return False


# ---- 2. sign-in -------------------------------------------------------------------------------------


def sign_in() -> setup.SignIn | None:
    ui.section("2  AWS sign-in")
    config = setup.load_config()
    names = setup.profiles()
    if not names:
        ui.warn("The AWS CLI has no profiles yet.")
        ui.say("Reframe can start the AWS CLI's own set-up for IAM Identity Center (SSO), which asks for your start URL and region:")
        ui.command("aws configure sso")
        if not ui.yes("Run it now?"):
            return None
        setup.run_in_terminal("aws configure sso")
        names = setup.profiles()
        if not names:
            ui.fail("Still no AWS profile. Set one up, then run reframe run again.")
            return None
    saved = config.get("profile")
    default = names.index(saved) + 1 if saved in names else 1
    profile = names[ui.choose("Which AWS profile should Reframe use?", [(n, "last used" if n == saved else "") for n in names], default) - 1]
    region = ui.ask("AWS region", config.get("region") or "us-east-1",
                    check=lambda v: None if REGION.match(v) else "Enter a region such as us-east-1")
    for _ in range(3):
        with ui.console.status(f"Checking the sign-in for {profile}…"):
            state = setup.signed_in(profile, region)
        if state.account:
            ui.ok(f"Signed in with {profile} to account …{state.account[-4:]} in {region}")
            setup.save_config(profile=profile, region=region)
            return state
        if state.expired or state.sso:
            ui.warn(f"{profile} is not signed in.")
            ui.say("Reframe can run the sign-in for you. Your browser opens, and you sign in there; Reframe never sees your credentials:")
            ui.command(f"aws sso login --profile {shlex.quote(profile)}")
            if not ui.yes("Sign in now?"):
                return None
            setup.run_in_terminal(f"aws sso login --profile {shlex.quote(profile)}")
            continue
        ui.fail(f"{profile} could not be used: {state.problem}")
        ui.hint(f"Check the profile with aws configure list --profile {profile}, then run reframe run again.")
        return None
    ui.fail("The sign-in did not complete. Run reframe run again when you are signed in.")
    return None


# ---- 3. source ---------------------------------------------------------------------------------------


def _reachable(url: str) -> str | None:
    try:
        result = subprocess.run(["git", "ls-remote", "--heads", url], capture_output=True, text=True, timeout=120,
                                env={**base_environment(), "GIT_TERMINAL_PROMPT": "0"})
    except (OSError, subprocess.TimeoutExpired):
        return "Git could not reach it; check the URL and your network"
    return None if result.returncode == 0 else "Git cannot read that repository; check the URL and that you have access"


def source() -> tuple[str, str | None] | None:
    from reframe.source.snapshot import URL
    ui.section("3  Source")
    form = ui.choose("Where is the mainframe source?", [("A GitHub or Git URL", "https://github.com/<owner>/<repo>"),
                                                        ("A local folder", "a Git checkout or a plain folder"),
                                                        ("A local ZIP file", "")], setup.load_config().get("source_form") or 1)
    if form == 1:
        def check_url(value: str) -> str | None:
            if not URL.match(value):
                return "Enter a Git URL, such as https://github.com/owner/repo"
            with ui.console.status("Checking the repository…"):
                return _reachable(value)
        url = ui.ask("Repository URL", check=check_url)
        ref = ui.ask("Branch, tag or commit (Enter for the default branch)", "") or None
        setup.save_config(source_form=1)
        return url, ref
    if form == 2:
        folder = ui.ask("Folder", check=lambda v: None if v and Path(v).expanduser().is_dir() else "That is not a folder")
        path = str(Path(folder).expanduser().resolve())
        ref = None
        if (Path(path) / ".git").exists():
            ref = ui.ask("Branch, tag or commit to assess (Enter for what is checked out)", "") or None
        setup.save_config(source_form=2)
        return path, ref
    archive = ui.ask("ZIP file", check=lambda v: None if v and Path(v).expanduser().is_file() and zipfile.is_zipfile(Path(v).expanduser())
                     else "That is not a ZIP file")
    setup.save_config(source_form=3)
    return str(Path(archive).expanduser().resolve()), None


# ---- 4 and 5. choices, summary, start ----------------------------------------------------------------


def choices(chosen_source: str) -> dict[str, Any]:
    from reframe.core.runfolder import PROJECT, project_name
    ui.section("4  Choices")
    mode = ("autonomous", "interactive")[ui.choose("How should AWS Transform's questions be answered?", [
        ("Autonomous", "Reframe answers them and records why (recommended)"),
        ("Interactive", "you answer each one with reframe answer")]) - 1]
    try:
        default = project_name(chosen_source.rstrip("/").removesuffix(".zip"))
    except Exception:  # noqa: BLE001 - a name Reframe cannot derive is simply asked for
        default = None
    project = ui.ask("Project name (lower-case letters, digits and hyphens; used in AWS resource names)", default,
                     check=lambda v: None if PROJECT.match(v) else "Use 1 to 30 lower-case letters, digits or hyphens, starting with a letter or digit")
    graph = ("new", "existing")[ui.choose("Neptune graph for AWS Transform", [
        ("A new graph for this run", "its own private network; billed until reframe teardown"),
        ("An existing Neptune cluster", "Reframe lists the clusters in the region and checks each; used as it is, never changed")]) - 1]
    picked = {"mode": mode, "project": project, "graph": graph, "claude": None}
    picked["claude"] = claude_choice()
    return picked


def claude_choice() -> dict[str, Any] | None:
    """Pipeline 2, offered with yes as the default: after AWS Transform finishes, the same snapshot is assessed with Claude."""
    from reframe.claude import plugin, preflight
    from reframe.claude.pipeline import DEFAULT_MAX_AGENTS
    from reframe.claude.runner import environment
    ui.section("Claude assessment")
    ui.say("Reframe can also assess the same snapshot with Claude's code-modernization plugin, alongside AWS Transform: it starts as "
           "soon as the run's Neptune graph exists, shows its results in the same business review, and builds a page comparing the two.")
    if not ui.yes("Assess the same snapshot with Claude as well?", default=True):
        ui.hint("Later, run: reframe claude")
        return None
    auth = ("subscription", "bedrock")[ui.choose("How should Claude sign in?", [
        ("Your Claude subscription", "Claude Code's own sign-in (claude auth login)"),
        ("Amazon Bedrock", "Claude models billed to the AWS account, with this AWS profile or AWS_BEARER_TOKEN_BEDROCK")]) - 1]
    if auth == "subscription":
        status = preflight.auth_status(environment("subscription"))
        if status.get("loggedIn"):
            ui.ok(f"Claude Code is signed in ({status.get('subscriptionType') or status.get('authMethod') or 'signed in'}).")
        else:
            ui.warn("Claude Code is not signed in.")
            if ui.yes("Run claude auth login now? You sign in in your browser.", default=True):
                setup.run_in_terminal("claude auth login")
    if not plugin.fetched():
        ui.say(f"Reframe uses the code-modernization plugin {plugin.VERSION}, fetched from Anthropic's plugin repository at a pinned commit.")
        if ui.yes("Fetch it now?", default=True):
            with ui.console.status("Fetching the plugin…"):
                plugin.fetch()
            ui.ok(f"Plugin {plugin.VERSION} ready.")
    ui.hint("Rule extraction starts many agents at once: on CardDemo about 370 to 555, up to about 9 million tokens and an hour.")
    limit = ui.ask("Agent limit for rule extraction (Reframe stops and asks if the estimate is higher)", str(DEFAULT_MAX_AGENTS),
                   check=lambda v: None if v.isdigit() and int(v) > 0 else "Enter a whole number of agents")
    return {"auth": auth, "max_agents": int(limit)}


def summary(chosen_source: str, ref: str | None, sign: setup.SignIn, picked: dict[str, Any]) -> bool:
    ui.section("5  Summary")
    rows = [("Source", chosen_source + (f" @ {ref}" if ref else "")),
            ("AWS", f"{sign.profile} · {sign.region} · account …{(sign.account or '')[-4:]}"),
            ("Mode", picked["mode"]), ("Project", picked["project"]),
            ("Neptune", "a new graph, billed until reframe teardown" if picked["graph"] == "new" else "an existing cluster, chosen next"),
            ("Alongside", (f"Claude assessment of the same snapshot, from when Neptune is ready ({picked['claude']['auth']}, up to {picked['claude']['max_agents']} agents)"
                      if picked.get("claude") else "AWS Transform only; reframe claude adds the Claude assessment later"))]
    ui.table(("", ""), rows, ("bold", None))
    ui.say("Reframe will create S3 buckets, IAM roles" + (", a private network and a Neptune Serverless graph" if picked["graph"] == "new" else "") +
           ", and an AWS Transform workspace, connector and job. A run takes about an hour. Nothing is removed until you run reframe teardown.")
    return ui.yes("Start the run?")


def run(args) -> int:
    from reframe.core import commands
    if not ui.interactive():
        ui.fail("The guided reframe run asks questions, so it needs a terminal. Without one, pass --source (and --profile).")
        return 2
    ui.header()
    m = setup.machine()
    if m.system == "windows":
        ui.fail("Reframe runs on macOS and Linux. On Windows, install WSL2 and run Reframe inside it.")
        return 2
    try:
        if not prerequisites(m):
            return 1
        sign = sign_in()
        if sign is None:
            return 1
        picked_source = source()
        if picked_source is None:
            return 1
        chosen, ref = picked_source
        picked = choices(chosen)
        if not summary(chosen, ref, sign, picked):
            ui.hint("Nothing was started or created.")
            return 0
    except (EOFError, KeyboardInterrupt):
        ui.console.print()
        ui.hint("Stopped. Nothing was started or created.")
        return 130
    return commands.start(source=chosen, profile=sign.profile, ref=ref, mode=picked["mode"], region=sign.region, project=picked["project"],
                          graph=picked["graph"], terraform=None, foreground=bool(getattr(args, "foreground", False)), claude=picked.get("claude"))


def setup_only(args) -> int:
    if not ui.interactive():
        ui.fail("reframe setup asks questions, so it needs a terminal.")
        return 2
    ui.header("SETUP · prerequisites and AWS sign-in")
    m = setup.machine()
    if m.system == "windows":
        ui.fail("Reframe runs on macOS and Linux. On Windows, install WSL2 and run Reframe inside it.")
        return 2
    try:
        if not prerequisites(m) or sign_in() is None:
            return 1
    except (EOFError, KeyboardInterrupt):
        ui.console.print()
        ui.hint("Stopped.")
        return 130
    ui.console.print()
    ui.ok("Set up. Start a run with:")
    ui.command("reframe run")
    return 0
