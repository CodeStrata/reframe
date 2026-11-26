"""The command handlers behind reframe's CLI (specification section 3)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from reframe.core.errors import EXIT_CODES, NotSent, Outcome, ReframeError, Stop
from reframe.core.runfolder import RunFolder, claude_only, find_run, iso, new_run, project_name

def say(text: str) -> None:
    sys.stdout.write(text)  # the current stdout, so output can be redirected


def _fail(stop: Stop) -> int:
    from reframe.core import ui
    ui.error(f"{stop.outcome.value}: {stop.message}")
    return EXIT_CODES[stop.outcome]


def _prompt(text: str) -> str:
    if not sys.stdin.isatty():
        raise EOFError
    return input(text)


def _start_worker(folder: RunFolder, task: str = "run") -> int:
    log = folder.path("worker.log").open("a")
    process = subprocess.Popen([sys.executable, "-m", "reframe", "worker", str(folder.root), "--task", task], stdin=subprocess.DEVNULL,
                               stdout=log, stderr=log, start_new_session=True, cwd=str(folder.root))
    return process.pid


# ---- run, resume, worker -------------------------------------------------------------------------


def run(args) -> int:
    """With --source, start at once and ask nothing; without it, the guided run (reframe.core.guide)."""
    if not args.source:
        from reframe.core import guide
        return guide.run(args)
    auth = getattr(args, "auth", None) or "subscription"
    if getattr(args, "tools", "both") == "claude":
        return start_claude_only(source=args.source, ref=args.ref, mode=args.mode, project=args.project, foreground=args.foreground,
                                 max_agents=getattr(args, "max_agents", None), auth=auth,
                                 profile=args.profile if auth == "bedrock" else None, region=args.region if auth == "bedrock" else None)
    from reframe.core.setup import load_config
    saved = load_config()
    profile = args.profile or saved.get("profile")
    if not profile:
        return _fail(Stop(Outcome.REFUSED, "no AWS profile: pass --profile, or run reframe setup once to choose and save one"))
    both = getattr(args, "tools", "both") == "both"  # the Claude assessment alongside, as the guided run offers by default
    return start(source=args.source, profile=profile, ref=args.ref, mode=args.mode, region=args.region or saved.get("region") or "us-east-1",
                 project=args.project, graph=args.graph, terraform=args.terraform, foreground=args.foreground,
                 claude={"auth": auth, "max_agents": getattr(args, "max_agents", None)} if both else None)


def start(*, source: str, profile: str, ref: str | None, mode: str, region: str, project: str | None, graph: str | None,
          terraform: str | None, foreground: bool, claude: dict[str, Any] | None = None) -> int:
    """Stage 0 and the Neptune choice here, then stages 1 to 8 in a background worker (or this terminal)."""
    from reframe.core import pipeline, ui
    from reframe.source.snapshot import kind
    try:
        kind(source)
        source = source if kind(source) == "git-url" else str(Path(source).expanduser().resolve())
        project = project or project_name(source.rstrip("/").removesuffix(".zip"))
        folder = new_run(project)
    except (Stop, ReframeError) as error:
        return _fail(error if isinstance(error, Stop) else Stop(Outcome.REFUSED, str(error)))
    folder.update(project=project, source=source, ref=ref, mode=mode, graph_arg=graph, profile=profile,
                  region=region, terraform=pipeline.terraform_binary(terraform), started_at=iso(), stage="preflight", status="RUNNING")
    ui.section(f"Run {folder.root.name}")
    ui.hint(f"{project} · {mode} mode · run folder {folder.root}")
    ctx = pipeline.Context.load(folder)
    if claude:
        from reframe.claude import pipeline as claude_pipeline
        claude_pipeline.request(ctx, auth=claude.get("auth", "subscription"), max_agents=claude.get("max_agents"), mode=mode)
        folder.update(claude_after=True)
    try:
        ui.hint("Checking everything the run needs (preflight)…")
        pipeline.prepare(ctx, _prompt, say)
    except Stop as stop:
        pipeline.record_stop(ctx, stop)
        return _fail(stop)
    graph_state = ctx.state["graph"]
    ui.ok("Preflight passed")
    ui.ok("Neptune: " + ("existing cluster " + graph_state["name"] if graph_state["kind"] == "existing" else "a new graph for this run"))
    if foreground:
        return worker(type("Args", (), {"folder": str(folder.root), "task": "run"})())
    pid = _start_worker(folder)
    ui.console.print()
    ui.panel(f"The run continues in the background (process {pid}); it takes about an hour"
             + ("; the Claude assessment runs alongside it from when the Neptune graph exists, about two hours" if claude else "") + ".\n"
             "Follow it:        reframe status   ·   reframe events --follow\n"
             + ("Answer AWS:       reframe answer\n" if mode == "interactive" else "")
             + "When it is done:  reframe report --open   ·   reframe teardown", "Started", "green")
    return 0


def start_claude_only(*, source: str, ref: str | None, mode: str, project: str | None, foreground: bool,
                      max_agents: int | None = None, auth: str = "subscription", profile: str | None = None, region: str | None = None) -> int:
    """A Claude-only run (docs/release-1.md, section 2): the snapshot and the Claude assessment, in one worker, with no AWS resources.
    With Amazon Bedrock, the AWS profile (or a Bedrock API key) is used to sign Claude in, and for nothing else."""
    from reframe.claude import pipeline as claude_pipeline
    from reframe.core import pipeline, ui
    from reframe.source.snapshot import kind
    try:
        kind(source)
        source = source if kind(source) == "git-url" else str(Path(source).expanduser().resolve())
        project = project or project_name(source.rstrip("/").removesuffix(".zip"))
        folder = new_run(project)
    except (Stop, ReframeError) as error:
        return _fail(error if isinstance(error, Stop) else Stop(Outcome.REFUSED, str(error)))
    folder.update(tools="claude", project=project, source=source, ref=ref, mode=mode, started_at=iso(), stage="snapshot", status="RUNNING",
                  **({"profile": profile, "region": region or "us-east-1"} if profile else {}))
    claude_pipeline.request(pipeline.Context.load(folder), auth=auth, max_agents=max_agents, mode=mode)
    ui.section(f"Run {folder.root.name} · Claude only")
    signin = {"subscription": "your Claude subscription", "api-key": "your Anthropic API key",
              "bedrock": f"Amazon Bedrock{' with profile ' + profile if profile else ''}"}[auth]
    ui.hint(f"{project} · {mode} mode · Claude signs in with {signin} · no AWS resources · run folder {folder.root}")
    if foreground:
        return worker(type("Args", (), {"folder": str(folder.root), "task": "claude"})())
    pid = _start_worker(folder, "claude")
    folder.event("claude_worker_started", pid=pid)
    ui.console.print()
    ui.panel(f"The Claude assessment runs in the background (process {pid}); on CardDemo it takes about two hours. It uses no AWS, so "
             "there is nothing to tear down.\n"
             "Follow it:        reframe status   ·   reframe events --follow\n"
             + ("Answer Claude:    reframe answer\n" if mode == "interactive" else "")
             + "When it is done:  reframe report --open   ·   then reframe reconcile", "Started", "green")
    return 0


def _claude_wanted(folder: RunFolder) -> bool:
    claude_state = folder.state.get("claude") or {}
    return bool(claude_state.get("requested_at")) and claude_state.get("status") != Outcome.DONE.value


def start_claude_if_ready(folder: RunFolder) -> int | None:
    """Pipeline 2 runs alongside pipeline 1 (docs/pipeline-2.md): its worker starts once the run's snapshot and AWS
    resources exist, if pipeline 2 is wanted and its worker is not already running. Returns the new worker's process."""
    from reframe.claude import pipeline as claude_pipeline
    from reframe.core import pipeline
    if not _claude_wanted(folder) or folder.worker_pid("claude") or folder.state.get("torn_down"):
        return None
    if not claude_pipeline.ready(pipeline.Context.load(folder)):
        return None
    pid = _start_worker(folder, "claude")
    folder.event("claude_worker_started", pid=pid)
    return pid


def resume(args) -> int:
    try:
        folder = find_run(args.run)
    except Stop as stop:
        return _fail(stop)
    state = folder.state
    started = []
    if state.get("status") != Outcome.DONE.value and not claude_only(state):
        pid = folder.worker_pid("run")
        if pid:
            say(f"Run {folder.root.name}: the AWS Transform assessment is already running (process {pid}).\n")
        else:
            if state.get("graph") is None:
                from reframe.core import pipeline
                ctx = pipeline.Context.load(folder)
                try:
                    pipeline.prepare(ctx, _prompt, say)
                except Stop as stop:
                    pipeline.record_stop(ctx, stop)
                    return _fail(stop)
            if args.foreground:
                return worker(type("Args", (), {"folder": str(folder.root), "task": "run"})())
            started.append(f"the AWS Transform assessment (process {_start_worker(folder)})")
    if _claude_wanted(folder):
        pid = folder.worker_pid("claude")
        if pid:
            say(f"Run {folder.root.name}: the Claude assessment is already running (process {pid}).\n")
        elif args.foreground and (state.get("status") == Outcome.DONE.value or claude_only(state)):
            return worker(type("Args", (), {"folder": str(folder.root), "task": "claude"})())
        else:
            new = start_claude_if_ready(folder)
            if new:
                started.append(f"the Claude assessment (process {new})")
    reconciling = state.get("reconcile") or {}
    if reconciling.get("status") not in (None, Outcome.DONE.value):
        pid = folder.worker_pid("reconcile")
        if pid:
            say(f"Run {folder.root.name}: the reconciliation is already running (process {pid}).\n")
        elif args.foreground:
            return worker(type("Args", (), {"folder": str(folder.root), "task": "reconcile"})())
        else:
            started.append(f"the reconciliation (process {_start_worker(folder, 'reconcile')})")
    if started:
        say(f"Run {folder.root.name} resumed in the background: {' and '.join(started)}. Follow it with reframe status.\n")
    elif (state.get("status") == Outcome.DONE.value or claude_only(state)) and not _claude_wanted(folder):
        say(f"Run {folder.root.name} is done. {state.get('message', '')}\n")
    return 0


def reconcile(args) -> int:
    """Pipeline 3 on a run where both pipelines are done: record the request, then the worker runs stages R0 to R7."""
    from reframe.core import ui
    from reframe.reconcile import pipeline as reconcile_pipeline
    try:
        folder = find_run(args.run)
        if getattr(args, "open", False):
            from reframe.report.reconciled import PAGE
            if not folder.exists(PAGE):
                raise Stop(Outcome.REFUSED, f"run {folder.root.name} has no reconciliation page yet; reframe reconcile makes it")
            say(f"Reconciliation: {folder.path(PAGE)}\n")
            subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(folder.path(PAGE))], check=False)
            return 0
        context = str(Path(args.context).expanduser().resolve()) if args.context else None
        if context and not Path(context).is_dir():
            raise Stop(Outcome.REFUSED, f"the context folder {args.context} does not exist")
    except Stop as stop:
        return _fail(stop)
    pid = folder.worker_pid("reconcile")
    if pid:
        ui.ok(f"Run {folder.root.name}: the reconciliation is already running (process {pid}).")
        return 0
    settings = reconcile_pipeline.request(folder, context=context, auth=args.auth, max_batches=args.max_batches)
    ui.section(f"Run {folder.root.name} · reconciliation, round {settings['round']}")
    kept = settings.get("context")  # a context folder given before is kept when this request names none
    ui.hint(f"sign-in: {settings['auth']} · batch limit {settings['max_batches']}" + (f" · context: {kept}" if kept else " · no context folder"))
    if args.foreground:
        return worker(type("Args", (), {"folder": str(folder.root), "task": "reconcile"})())
    pid = _start_worker(folder, "reconcile")
    ui.panel(f"The reconciliation runs in the background (process {pid}). It needs no AWS resources.\n"
             "Follow it:  reframe status   ·   reframe events --follow", "Started", "green")
    return 0


def export(args) -> int:
    """`reframe export --to xlsx` (docs/sharing.md, section 7): the reconciled results as one workbook; runs nothing."""
    from reframe.core import ui
    from reframe.report import export as exporter
    try:
        folder = find_run(args.run)
        given = args.context or (folder.state.get("reconcile") or {}).get("context")
        context = Path(given).expanduser().resolve() if given else None
        if context and not context.is_dir():
            raise Stop(Outcome.REFUSED, f"the context folder {given} does not exist")
        target = Path(args.out).expanduser().resolve() if args.out else None
        value = exporter.export(folder, target, context)
    except Stop as stop:
        return _fail(stop)
    ui.section(f"Run {folder.root.name} · export to Excel")
    ui.table(["Sheet", "Rows"], [[k, str(v)] for k, v in value["counts"].items()])
    if context:
        ui.hint(f"review downloads read from {context}: {len(value['read'])}, with marks on {value['marks']} item(s)")
        for i in value["ignored"]:
            ui.hint(f"ignored {i['file']}: {i['why']}")
    else:
        ui.hint("no context folder: the workbook has no reviewers' marks")
    ui.ok(f"Workbook: {value['path']}")
    if args.open:
        subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(value["path"])], check=False)
    return 0


def design(args) -> int:
    """`reframe design` (docs/pipeline-4.md): a design round, its plan, the package copied out, or a copy's readiness."""
    from reframe.core import ui
    from reframe.design import handover, package, pipeline
    if args.check:
        found = handover.readiness(Path(args.check).expanduser())
        ui.section(f"Package copy {args.check}")
        ui.table(["File", "Placeholders left"], [[k, str(len(v))] for k, v in found["files"].items()] or [["–", "0"]])
        if found["drafts"]:
            ui.hint(f"{len(found['drafts'])} draft capabilities: confirm them with the owner before building them")
        (ui.ok if found["ready"] else ui.hint)("ready for forward engineering" if found["ready"] else f"{found['placeholders']} placeholders to fill in; START-HERE.md says how")
        return 0 if found["ready"] else 1
    try:
        folder = find_run(args.run)
        if args.package:
            done = package.copy_out(folder, Path(args.package).expanduser().resolve(), args.form)
            if done["left"]:
                raise Stop(Outcome.REFUSED, "; ".join(done["left"][:5]))
            ui.ok(f"Package v{done['version']} copied to {done['path']}: {done['written']} files. Open START-HERE.md there.")
            return 0
        context = Path(args.context).expanduser().resolve() if args.context else None
        claude = None
        if not args.plan:
            from reframe.claude import preflight
            from reframe.reconcile.pipeline import claude_code
            report = preflight.check(args.auth, aws_identity=preflight.run_identity(folder) if args.auth == "bedrock" else None)
            if not report.ok:
                raise Stop(Outcome.REFUSED, report.problems())
            claude = claude_code(folder, args.auth)
        value = pipeline.run(folder, claude, context, args.stack, args.plan)
    except (Stop, ValueError) as stop:
        return _fail(stop if isinstance(stop, Stop) else Stop(Outcome.REFUSED, str(stop)))
    ui.section(f"Run {folder.root.name} · the design" + (" · plan" if args.plan else f" · round {value['round']}"))
    ui.table(["Stage", "Redone", "Kept"], [[k, ", ".join(x["name"] or "No domain" for x in v["redone"]) or "–", str(len(v["kept"]))]
                                            for k, v in value["stages"].items()])
    if args.plan:
        ui.hint(value["note"])
        return 0
    ui.ok(f"What changed: {value['changes']}")
    ui.ok(f"Package v{value['package']['version']}" + (" (new)" if value["package"]["new"] else " (unchanged)") + f": {value['package']['path']}")
    page = folder.path("outputs/design/index.html")
    ui.ok(f"The design page: {page}")
    if value.get("problems"):
        ui.hint(f"{len(value['problems'])} problems the checks still found; they are on the design page")
    if args.open:
        subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(page)], check=False)
    return 0


def review(args) -> int:
    """Several reviewers' files (docs/pipeline-3.md, section 8.11): coverage, sign-offs and disagreements; runs nothing."""
    from reframe.core import ui
    from reframe.reconcile import reviews
    try:
        folder = find_run(args.run)
        context = Path(args.context).expanduser().resolve()
        if not context.is_dir():
            raise Stop(Outcome.REFUSED, f"the context folder {args.context} does not exist")
    except Stop as stop:
        return _fail(stop)
    value = reviews.summary(folder, context)
    ui.section(f"Run {folder.root.name} · reviews in {context}")
    if not value["reviewers"]:
        ui.warn("No review download of this run's snapshot in the folder. Download your marks from a review page (Your review) into it.")
    else:
        short = {"aws": "AWS Transform", "claude": "Claude", "reconciled": "Reconciled"}
        ui.table(["Reviewer", "Page and file", "Agree / change / question", "Coverage", "Signed off"],
                 [[r["reviewer"] or "(no name)", f"{short[r['page']]}: {r['file']}",
                   f"{r['marks'].get('agree', 0)} / {r['marks'].get('change', 0)} / {r['marks'].get('question', 0)}",
                   f"{r['marked']} of {r['items']} ({round(100 * r['coverage'])}%)", ", ".join(x["name"] or x["function"] for x in r["signoffs"]) or "–"]
                  for r in value["reviewers"]])
    if value["disagreements"]:
        ui.state("Disagreements", f"{len(value['disagreements'])} item(s) marked differently; the next round takes Needs change or Question over Agree", "bold yellow")
        names = {"agree": "Agree", "change": "Needs change", "question": "Question"}
        ui.table(["Item", "Marks", "Next round"],
                 [[d["key"], "; ".join(f"{m['reviewer'] or 'a reviewer'}: {names.get(m['status'], m['status'])}" + (f" ({m['comment']})" if m["comment"] else "")
                                      for m in d["marks"]), names.get(d["combined"], d["combined"])] for d in value["disagreements"]])
    elif value["reviewers"]:
        ui.ok("No two reviewers marked an item differently.")
    for i in value["ignored"]:
        ui.hint(f"ignored {i['file']}: {i['why']}")
    ui.state("Next", f"reframe reconcile --context {context} combines these marks in the next round", "bright_cyan")
    return 0


def worker(args) -> int:
    from reframe.core import pipeline
    folder = RunFolder(Path(args.folder))
    ctx = pipeline.Context.load(folder)
    task = getattr(args, "task", "run")
    if task == "reconcile":  # needs no AWS: the run's profile is not loaded
        return _reconcile_work(folder)
    lock = "claude" if task == "claude" else "run"
    try:
        folder.lock(lock)
    except Stop as stop:
        return _fail(stop)
    try:
        folder.event("worker_started", pid=os.getpid(), task=task)
        if task == "claude":
            return _claude_work(ctx)
        if task == "run" and claude_only(folder.state):
            raise Stop(Outcome.REFUSED, "this run is Claude-only: it has no AWS Transform assessment; reframe resume continues the Claude assessment")
        if task == "run" and folder.state.get("status") != Outcome.DONE.value:
            outcome = pipeline.work(ctx, on_resources=lambda: start_claude_if_ready(folder))
            say(f"{outcome.value}: {folder.state.get('message', '')}\n")
        # pipeline 2 asked for after pipeline 1's resources existed, and not running: start it now
        start_claude_if_ready(folder)
        return 0
    except Stop as stop:
        pipeline.record_stop(ctx, stop)
        return _fail(stop)
    except Exception as error:  # noqa: BLE001 - recorded so status can show it; the traceback is in worker.log
        stop = Stop(Outcome.FAILED, f"{type(error).__name__}: {str(error)[:400]}")
        pipeline.record_stop(ctx, stop)
        import traceback
        traceback.print_exc()
        return _fail(stop)
    finally:
        folder.unlock(lock)


def _reconcile_work(folder: RunFolder) -> int:
    from reframe.reconcile import pipeline as reconcile_pipeline
    try:
        folder.lock("reconcile")
    except Stop as stop:
        return _fail(stop)
    try:
        folder.event("worker_started", pid=os.getpid(), task="reconcile")
        outcome = reconcile_pipeline.work(folder)
        say(f"reconciliation {outcome.value}: {(folder.state.get('reconcile') or {}).get('message', '')}\n")
        return 0
    except Stop as stop:
        reconcile_pipeline.record_stop(folder, stop)
        return _fail(stop)
    except Exception as error:  # noqa: BLE001 - recorded so status can show it; the traceback is in worker.log
        stop = Stop(Outcome.FAILED, f"{type(error).__name__}: {str(error)[:400]}")
        reconcile_pipeline.record_stop(folder, stop)
        import traceback
        traceback.print_exc()
        return _fail(stop)
    finally:
        folder.unlock("reconcile")


def _claude_work(ctx) -> int:
    from reframe.claude import pipeline as claude_pipeline
    try:
        outcome = claude_pipeline.work(ctx)
        say(f"Claude assessment {outcome.value}: {(ctx.state.get('claude') or {}).get('message', '')}\n")
        return 0
    except Stop as stop:
        claude_pipeline.record_stop(ctx, stop)
        return _fail(stop)
    except NotSent as error:  # an expired AWS sign-in (graph stage) waits for the person, like pipeline 1; a Claude-only run makes no AWS call
        stop = Stop(Outcome.WAITING_SIGNIN, f"{error}. Sign in with aws sso login --profile {ctx.state.get('profile')}, then run reframe resume")
        claude_pipeline.record_stop(ctx, stop)
        return _fail(stop)
    except Exception as error:  # noqa: BLE001 - recorded so status can show it; the traceback is in worker.log
        stop = Stop(Outcome.FAILED, f"{type(error).__name__}: {str(error)[:400]}")
        claude_pipeline.record_stop(ctx, stop)
        import traceback
        traceback.print_exc()
        return _fail(stop)


def claude(args) -> int:
    """Pipeline 2 on a run whose pipeline 1 is done: record the request, then the worker runs stages C0 to C8."""
    from reframe.claude import pipeline as claude_pipeline
    from reframe.core import pipeline, ui
    try:
        folder = find_run(args.run)
    except Stop as stop:
        return _fail(stop)
    state = folder.state
    if state.get("torn_down"):
        return _fail(Stop(Outcome.REFUSED, f"run {folder.root.name} is torn down; the Claude assessment needs a run whose resources are still there"))
    ctx = pipeline.Context.load(folder)
    settings = claude_pipeline.request(ctx, auth=args.auth, max_agents=args.max_agents, mode=args.mode, graph_load=args.graph_load)
    if (folder.state.get("claude") or {}).get("status") == Outcome.DONE.value:
        ui.ok(f"The Claude assessment is already done for run {folder.root.name}. reframe compare --open shows the comparison.")
        return 0
    pid = folder.worker_pid("claude")
    if pid:
        ui.ok(f"Run {folder.root.name}: the Claude assessment is already running (process {pid}).")
        return 0
    if not claude_pipeline.ready(ctx):
        if folder.worker_pid("run"):
            ui.ok(f"Recorded. Run {folder.root.name}'s AWS Transform assessment starts the Claude assessment as soon as its AWS resources exist.")
            return 0
        return _fail(Stop(Outcome.REFUSED, f"run {folder.root.name} has no AWS resources yet and the AWS Transform assessment is not running; the Claude assessment is "
                                           "recorded and starts when reframe resume has made them"))
    ui.section(f"Run {folder.root.name} · Claude assessment")
    ui.hint(f"{settings['mode']} mode · sign-in: {settings['auth']} · agent limit {settings['max_agents']}")
    if args.foreground:
        return worker(type("Args", (), {"folder": str(folder.root), "task": "claude"})())
    pid = _start_worker(folder, "claude")
    ui.panel(f"The Claude assessment runs in the background (process {pid}), alongside the AWS Transform assessment if it is still running; on CardDemo it "
             "takes about two hours.\n"
             "Follow it:        reframe status   ·   reframe events --follow\n"
             "When it is done:  reframe compare --open   ·   reframe teardown", "Started", "green")
    return 0


def compare(args) -> int:
    from reframe.report import build as builder
    from reframe.report import compare as comparison
    try:
        folder = find_run(args.run)
        if claude_only(folder.state):
            raise Stop(Outcome.REFUSED, "this run is Claude-only, so there is nothing to compare; reframe report --open shows Claude's review")
        if not folder.exists("outputs/claude/model.json"):
            raise Stop(Outcome.REFUSED, "this run has no Claude results yet; run reframe claude first")
    except Stop as stop:
        return _fail(stop)
    builder.build_claude(folder)
    path = comparison.build(folder)
    say(f"Comparison: {path}\n")
    if args.open:
        subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(path)], check=False)
    return 0


def publish(args) -> int:
    from reframe.report.publish import publish as make
    try:
        folder = find_run(args.run)
        if args.to == "pages":
            return _publish_pages(folder, getattr(args, "repo", None))
        if args.to != "aws":
            manifest = make(folder, Path(args.to).expanduser().resolve())
            target = Path(args.to).expanduser()
            say(f"Published {len(manifest['files'])} pages to {target}; open index.html there.\n")
            from reframe.core import ui
            from reframe.report.publish import protected_warning
            if warning := protected_warning(target):
                ui.warn(warning)
            return 0
        import tempfile
        from reframe.report.store import Store, signed_in
        store = Store(signed_in(getattr(args, "profile", None), getattr(args, "region", None)))
        with tempfile.TemporaryDirectory() as scratch:
            copy = Path(scratch) / "copy"
            manifest = make(folder, copy)
            prefix = store.upload(copy, str(manifest["project"]), str(manifest["run"]), folder)
    except Stop as stop:
        return _fail(stop)
    except NotSent as error:
        return _fail(Stop(Outcome.WAITING_SIGNIN, f"{error}. Sign in with aws sso login, then run it again"))
    what = {"source/": "the snapshot both tools read", "results/": "what AWS Transform and Claude's plugin wrote",
            "reports/": f"{len(manifest['files'])} pages, cleaned, with report.zip"}
    say(f"Published the run to the private Reframe bucket in your AWS account, under {prefix}:\n"
        + "".join(f"  {prefix}{key:<10} {what[key]}\n" for key in ("source/", "results/", "reports/") if key in store.sent)
        + f"Anyone who can sign in to the account and read the bucket can now:\n"
        f"  open the project's latest report:  reframe reports open {manifest['project']}\n"
        f"  save this one in a folder:         reframe reports download {prefix.rstrip('/')} --to <folder>\n"
        f"  without Reframe:                   download {prefix}reports/report.zip from the bucket in the S3 console\n")
    return 0


def _publish_pages(folder: RunFolder, repo: str | None) -> int:
    """S-16 (docs/release-1.md, section 3): the cleaned copy on the repository's gh-pages branch, after a typed yes."""
    import tempfile
    from reframe.report.pages import Pages
    from reframe.report.publish import publish as make
    if not repo:
        raise Stop(Outcome.REFUSED, "say which repository: reframe publish --to pages --repo <owner>/<name>")
    if not sys.stdin.isatty():
        raise Stop(Outcome.REFUSED, "publishing to GitHub Pages makes a public site, so it asks you first and needs a terminal")
    pages = Pages(repo)
    pages.signed_in()
    with tempfile.TemporaryDirectory() as scratch:
        copy = Path(scratch) / "copy"
        manifest = make(folder, copy)
        project, run = str(manifest["project"]), str(manifest["run"])
        say(pages.warning(project, run))
        if _prompt("Type yes to publish this public site, or anything else to stop: ").strip() != "yes":
            say("Nothing was published.\n")
            return 0
        address = pages.push(copy, project, run)
    folder.merge("pages", repo=repo, address=address, published_at=iso())
    folder.event("published_pages", repo=repo, address=address, files=len(manifest["files"]))
    say(f"Published {len(manifest['files'])} pages to the gh-pages branch of {repo}. It is public at:\n  {address}\n"
        "GitHub can take a minute or two to build the site the first time.\n")
    return 0



def reports(args) -> int:
    from reframe.core import ui
    from reframe.report.store import Store, open_in_browser, signed_in
    try:
        store = Store(signed_in(args.profile, args.region))
        if args.action in ("open", "download"):
            if not args.path:
                raise Stop(Outcome.REFUSED, f"name the report: reframe reports {args.action} <project>, for its latest run, or "
                                            "<project>/<run>; reframe reports lists them")
            if args.action == "download" and not args.to:
                raise Stop(Outcome.REFUSED, "say where to save it: reframe reports download <project> --to <folder>")
            path = store.resolve(args.path, args.run)
            if args.action == "open":
                page = store.download(path)
                say(f"Downloaded {path} with your AWS sign-in to {page.parent}\n")
                open_in_browser(page)
                return 0
            from reframe.report.publish import protected_warning
            target = Path(args.to).expanduser()
            page = store.download(path, target.resolve())
            say(f"Downloaded {path} with your AWS sign-in to {target}; open index.html there.\n")
            if warning := protected_warning(target):
                ui.warn(warning)
            return 0
        if args.action == "teardown":
            if not sys.stdin.isatty():
                raise Stop(Outcome.REFUSED, "reframe reports teardown asks for consent, so it needs a terminal")
            store.teardown(_prompt, say)
            return 0
        found = store.reports()
    except Stop as stop:
        return _fail(stop)
    except NotSent as error:
        return _fail(Stop(Outcome.WAITING_SIGNIN, f"{error}. Sign in with aws sso login, then run it again"))
    if not found:
        say("No reports are published to AWS yet. Publish one with: reframe publish --run <id> --to aws\n")
        return 0
    ui.section(f"Reports in {store.reading_bucket()}")
    ui.table(("Report", "Project", "Commit", "Published"), [(r["path"], str(r["project"]), str(r["commit"] or "")[:12], str(r["published_at"])[:16])
                                                           for r in found], ("bold", None, "dim", "dim"))
    ui.hint("Open one with: reframe reports open <project> (its latest run) or <project>/<run>   ·   save one: reframe reports download <project> --to <folder>")
    return 0


# ---- reading the run -----------------------------------------------------------------------------


NEXT = {Outcome.WAITING_SIGNIN.value: "sign in with aws sso login --profile {profile}, then run reframe resume",
        Outcome.WAITING_HUMAN.value: "answer with reframe answer, or fix what the message says, then reframe resume",
        Outcome.REFUSED.value: "fix what the message says, then reframe resume",
        Outcome.UNCERTAIN.value: "run reframe resume; it settles the change from AWS's state",
        Outcome.FAILED.value: "read the message and worker.log; reframe resume tries again, reframe teardown removes the resources"}


STATUS_STYLE = {"DONE": "bold green", "RUNNING": "bold bright_cyan", "WAITING_HUMAN": "bold yellow", "WAITING_SIGNIN": "bold yellow",
                "UNCERTAIN": "bold yellow", "REFUSED": "bold red", "FAILED": "bold red"}
STEP_STYLE = {"SUCCEEDED": "[green]✓ succeeded[/]", "IN_PROGRESS": "[bright_cyan]● in progress[/]", "PENDING_HUMAN_INPUT": "[yellow]? waiting for input[/]",
              "FAILED": "[red]✗ failed[/]", "NOT_STARTED": "[dim]not started[/]"}


def status(args) -> int:
    from reframe.core import ui
    try:
        folder = find_run(args.run)
    except Stop as stop:
        return _fail(stop)
    state, pid = folder.state, folder.worker_pid()
    ui.section(f"Run {folder.root.name} · {state.get('project')}")
    alone = claude_only(state)
    ui.hint(f"{state.get('source')} · {state.get('mode')} mode" + (" · Claude only, no AWS" if alone else "")
            + (f" · worker running (process {pid})" if pid else ""))
    ui.state("Status", f"{state.get('status')} · stage {state.get('stage')}", STATUS_STYLE.get(str(state.get("status")), "bold yellow"))
    if state.get("graph"):
        graph = state["graph"]
        ui.state("Neptune", "existing cluster " + graph["name"] if graph["kind"] == "existing" else "a new graph", "")
    job = state.get("job")
    if job:
        ui.state("AWS Transform job", f"{job['status']} (poll {job['poll']} at {job['at']})", "")
        steps = job.get("steps") or []
        if steps:
            ui.table(("Plan step", ""), [(step["name"], STEP_STYLE.get(step["status"], step["status"])) for step in steps])
    question = folder.load("question.json")
    if question:
        ui.warn(f"AWS is waiting for an answer ({question['kind']}). See it with: reframe answer")
    if state.get("message") and not state.get("torn_down"):  # the run's last message predates the teardown
        ui.say(state["message"])
    if state.get("report"):
        ui.state("Report", str(folder.path(state["report"])), "bright_cyan")
    hint = NEXT.get(str(state.get("status")))
    claude_state = state.get("claude") or {}
    if hint and not pid and not alone:  # a Claude-only run's next step is the Claude assessment's, below
        ui.state("Next", hint.format(profile=state.get("profile")), "bright_cyan")
    elif state.get("status") == Outcome.DONE.value and not state.get("torn_down") and not claude_state and not alone:
        ui.state("Next", "open the report with reframe report --open; assess the same snapshot with Claude: reframe claude; "
                         "remove the AWS resources with reframe teardown", "bright_cyan")
    _claude_status(folder, state)
    _reconcile_status(folder, state)
    if state.get("torn_down"):
        ui.ok(f"Torn down at {state['torn_down']}.")
    return 0


CLAUDE_NEXT = {Outcome.WAITING_SIGNIN.value: "sign in (claude auth login, or the AWS sign-in for Bedrock), then reframe resume",
               Outcome.WAITING_HUMAN.value: "answer with reframe answer, or after Claude's usage limit resets run reframe resume",
               Outcome.REFUSED.value: "fix what the message says, then reframe claude",
               Outcome.FAILED.value: "read the message and worker.log, then reframe resume",
               Outcome.UNCERTAIN.value: "run reframe resume; it settles the change from AWS's state"}


def _reconcile_status(folder: RunFolder, state: dict[str, Any]) -> None:
    from reframe.core import ui
    rec = state.get("reconcile") or {}
    if not rec:
        return
    ui.section("Reconciliation")
    status = str(rec.get("status"))
    pid = folder.worker_pid("reconcile")
    ui.state("Status", f"{status} · stage {rec.get('stage', 'not started')} · round {rec.get('round')}", STATUS_STYLE.get(status, "bold yellow"))
    ui.hint(f"sign-in {rec.get('auth')} · batch limit {rec.get('max_batches')}" + (f" · context {rec['context']}" if rec.get("context") else "")
            + (f" · worker running (process {pid})" if pid else ""))
    if rec.get("estimate"):
        e = rec["estimate"]
        ui.state("Estimate", f"{e['batches']} batches for {sum(e['units'].values())} units; about {e['minutes_low']} to {e['minutes_high']} "
                             f"minutes, ${e['usd_low']} to ${e['usd_high']} at API prices", "")
    if rec.get("progress") and status == "RUNNING":
        ui.state("Progress", f"{rec['progress']['batches_done']} of {rec['progress']['batches']} batches", "")
    if rec.get("decisions"):
        ui.state("Decisions", ", ".join(f"{k} {v}" for k, v in rec["decisions"].items()) + f"; possible defects {rec.get('defects', 0)}", "")
    if rec.get("questions"):
        q = rec["questions"]
        ui.state("SME list", f"{q.get('questions', 0)} questions ({q.get('answered', 0)} answered, {q.get('settled', 0)} settled), {q.get('defects', 0)} possible defects", "")
    if rec.get("requirements"):
        r = rec["requirements"]
        ui.state("Requirements", f"{r['requirements']} recommended, citing {r['rules_cited']} of {r['rules_total']} rules; {r['dropped']} dropped", "")
    if rec.get("signoffs"):
        ui.state("Signed off", f"{len({(x['page'], x['function']) for x in rec['signoffs']})} function(s) in the review downloads read", "")
        for x in rec["signoffs"]:
            ui.hint(f"{x['page'] or 'a review'}: {x['name'] or x['function']}, by {x['reviewer'] or 'an unnamed reviewer'}"
                    + (f" on {str(x['at'])[:10]}" if x.get("at") else ""))
    if rec.get("message"):
        ui.say(rec["message"])
    if status == "DONE" and rec.get("page"):
        ui.state("Next", "reframe reconcile --open shows the reconciliation page; reframe export --to xlsx writes it as a workbook; answer the "
                         "SME list (reconcile/questions.csv) and run reframe reconcile --context <folder> again; reframe publish includes it", "bright_cyan")
    if status not in ("DONE", "RUNNING", "REQUESTED") and not pid:
        ui.state("Next", "fix what the message says, then reframe resume (or reframe reconcile with what it asks for)", "bright_cyan")


def claude_next(state: dict[str, Any]) -> str:
    """What to do once both assessments are done. The reconciliation needs no AWS resources, so the teardown comes first
    (found on GenApp, 25 November 2026, where status named every next step but the reconciliation)."""
    torn_down, reconciled = bool(state.get("torn_down")), bool(state.get("reconcile"))
    if claude_only(state):
        return "; ".join((["reframe reconcile checks every rule against the code"] if not reconciled else
                          ["reframe design designs the modern application", "reframe reconcile --open shows the reconciliation"])
                         + ["reframe report --open shows Claude's business review"])
    steps = []
    if not reconciled:
        steps.append("reframe reconcile reconciles the two assessments" if torn_down else
                     "reframe teardown removes the AWS resources, which the reconciliation does not need; then reframe reconcile "
                     "reconciles the two assessments")
    steps += ["reframe compare --open shows the comparison", "reframe report --open each business review"]
    if reconciled and not torn_down:
        steps.append("reframe teardown removes the AWS resources")
    return "; ".join(steps)


def _claude_status(folder: RunFolder, state: dict[str, Any]) -> None:
    from reframe.core import ui
    claude_state = state.get("claude") or {}
    if not claude_state:
        return
    ui.section("Claude assessment")
    status = str(claude_state.get("status"))
    ui.state("Status", f"{status} · stage {claude_state.get('stage', 'not started')}", STATUS_STYLE.get(status, "bold yellow"))
    claude_pid = folder.worker_pid("claude")
    ui.hint(f"sign-in {claude_state.get('auth')} · agent limit {claude_state.get('max_agents')} · {claude_state.get('mode')} mode"
            + (f" · worker running (process {claude_pid})" if claude_pid else ""))
    if folder.load("claude-question.json"):
        ui.warn("The Claude assessment is waiting for an answer. See it with: reframe answer")
    from reframe.claude.steps import receipts
    rows = []
    order = {"preflight": 0, "assess": 1, "map": 2, "extract-rules": 3}
    for name, value in sorted(receipts(folder).items(), key=lambda item: order.get(item[0], 9)):
        rows.append((name, "[green]✓ done[/]" if value.get("ok") else f"[yellow]{value.get('problem') or 'running'}[/]",
                     (f"{value.get('seconds', 0) // 60} min" if value.get("seconds") else "") + (" (from the spike)" if value.get("seeded_from") else ""),
                     f"{sum((value.get('tokens') or {}).values()) / 1e6:.1f}M tokens" if value.get("tokens") else ""))
    if rows:
        ui.table(("Plugin step", "", "", ""), rows)
    if claude_state.get("message"):
        ui.say(claude_state["message"])
    if claude_state.get("graph", {}).get("loaded_at"):
        g = claude_state["graph"]
        ui.state("Neptune", f"Claude's graph loaded: {g.get('quads')} quads; {g.get('rules_joined_to_aws_programs')} rules join AWS's programs", "")
    if status == Outcome.DONE.value:
        ui.state("Next", claude_next(state), "bright_cyan")
    elif status in CLAUDE_NEXT and not folder.worker_pid("claude"):
        ui.state("Next", CLAUDE_NEXT[status], "bright_cyan")


def events(args) -> int:
    try:
        folder = find_run(args.run)
    except Stop as stop:
        return _fail(stop)
    path, seen = folder.path("events.jsonl"), 0
    while True:
        lines = path.read_text().splitlines() if path.exists() else []
        for line in lines[seen:]:
            event = json.loads(line)
            detail = " ".join(f"{k}={v}" for k, v in event.items() if k not in ("at", "event"))
            say(f"{event['at']}  {event['event']}  {detail}\n")
        seen = len(lines)
        if not args.follow:
            return 0
        sys.stdout.flush()
        time.sleep(5)


# ---- answering AWS -------------------------------------------------------------------------------


def answer(args) -> int:
    from reframe.transform import answers
    try:
        folder = find_run(args.run)
    except Stop as stop:
        return _fail(stop)
    pending = folder.load("question.json")
    if not pending:
        claude_pending = folder.load("claude-question.json")  # pipeline 1's question comes first
        if claude_pending:
            return _answer_claude(folder, claude_pending, args)
        say("Nothing is waiting for an answer.\n")
        return 0
    if pending.get("kind") == "claude":
        return _answer_claude(folder, pending, args)
    question = answers.Question(pending["id"], pending["kind"], pending["text"], tuple(pending.get("options") or ()),
                                tuple(pending.get("replies") or ()), pending.get("interaction_origin_id"), pending.get("schema") or {})
    if not args.choices and not args.text:
        say(f"AWS asks ({question.kind}, since {pending.get('asked_at')}):\n\n{question.text.strip()}\n\n")
        for number, label in enumerate(question.options, 1):
            say(f"  {number}. {label}\n")
        hint = ("reframe answer <number> [<number>...]" if question.kind in ("catalog", "select") else "reframe answer <number>")
        say("\nAnswer with " + (f"{hint}, or " if question.options else "") + "reframe answer --text \"...\"\n")
        return 0
    try:
        choices = [int(c) for c in args.choices]
        reply = answers.interactive(question, choices, args.text)
    except ValueError as error:
        sys.stderr.write(f"{error}\n")
        return 2
    folder.save("answer.json", {"id": question.id, "text": reply.text, "reason": reply.reason, "at": iso()})
    folder.event("answer_given", id=question.id)
    say(f"Answer recorded: {reply.text[:300]}\n")
    say("The worker sends it within a minute." if folder.worker_pid() else "Run reframe resume to send it.")
    say("\n")
    return 0


def _answer_claude(folder: RunFolder, pending: dict[str, Any], args) -> int:
    """A pipeline 2 question (the plugin's preflight answers, the rule-extraction estimate, loading an existing cluster)."""
    options = pending.get("options") or []
    if not args.choices and not args.text:
        say(f"The Claude assessment asks (since {pending.get('asked_at')}):\n\n{pending['text'].strip()}\n\n")
        for number, label in enumerate(options, 1):
            say(f"  {number}. {label}\n")
        say("\nAnswer with reframe answer <number>" + (", or reframe answer --text \"...\"" if pending["id"].startswith("claude-preflight") else "") + "\n")
        return 0
    if args.text and not pending["id"].startswith("claude-preflight"):
        sys.stderr.write("this question takes one of the numbered options\n")
        return 2
    if args.choices:
        if len(args.choices) != 1 or not args.choices[0].isdigit() or not 1 <= int(args.choices[0]) <= len(options):
            sys.stderr.write(f"choose one number from 1 to {len(options)}\n")
            return 2
        text = options[int(args.choices[0]) - 1]
        text = text.removeprefix("Reframe's answer: ")
    else:
        text = args.text.strip()
    folder.save("claude-answer.json", {"id": pending["id"], "text": text, "reason": "answered with reframe answer", "at": iso()})
    folder.event("answer_given", id=pending["id"])
    say(f"Answer recorded: {text[:300]}\n")
    say("The worker uses it within a minute.\n" if folder.worker_pid("claude") else "Run reframe resume to continue.\n")
    return 0


# ---- report and teardown -------------------------------------------------------------------------


def report(args) -> int:
    from reframe.report import build
    try:
        folder = find_run(args.run)
        alone = claude_only(folder.state)
        if alone and not folder.exists("outputs/claude/model.json"):
            raise Stop(Outcome.REFUSED, "this run has no Claude results yet; reframe status shows where the Claude assessment is")
        if not alone and not folder.exists("outputs/requirements"):
            raise Stop(Outcome.REFUSED, "this run has no downloaded results yet")
    except Stop as stop:
        return _fail(stop)
    if alone:
        path = build.build_claude(folder)
        say(f"Claude's report: {path}\n")
        if args.open:
            subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(path)], check=False)
        return 0
    path = build.build(folder)
    say(f"Report: {path}\n")
    if folder.exists("outputs/claude/model.json"):
        say(f"Claude's report: {build.build_claude(folder)}\n")
    if args.open:
        subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(path)], check=False)
    return 0


def teardown(args) -> int:
    from reframe.core import pipeline
    from reframe.core import teardown as stage
    try:
        folder = find_run(args.run)
    except Stop as stop:
        return _fail(stop)
    if claude_only(folder.state):
        say(f"Run {folder.root.name} is Claude-only: it created no AWS resources, so there is nothing to tear down.\n")
        return 0
    pid = folder.worker_pid("run") or folder.worker_pid("claude")
    if pid:
        return _fail(Stop(Outcome.REFUSED, f"a worker is still running this run (process {pid}); wait for it to stop, or stop it, first"))
    if not sys.stdin.isatty():
        return _fail(Stop(Outcome.REFUSED, "reframe teardown asks for consent, so it needs a terminal"))
    ctx = pipeline.Context.load(folder)
    try:
        folder.lock()
        consented = stage.ask(ctx, _prompt, say)
        if consented is None:
            return 0
        say("\nDeleting, in order. This takes about 15 minutes with a new Neptune graph"
            + (", and about 20 more while AWS releases the graph loader's network interfaces" if any(i["kind"].startswith("Lambda") for i in consented) else "")
            + ".\n")
        result = stage.delete(ctx, consented, say)
    except Stop as stop:
        return _fail(stop)
    except NotSent as error:
        return _fail(Stop(Outcome.WAITING_SIGNIN, f"{error}. Sign in with aws sso login --profile {folder.state.get('profile')}, "
                                                  "then run reframe teardown again; nothing more was deleted"))
    finally:
        folder.unlock()
    left = result["leftovers"]
    say("\n")
    if left["exists"]:
        say("Still in AWS after teardown:\n" + "".join(f"  - {arn}\n" for arn in left["exists"]))
    if left["stale_index"]:
        say(f"AWS's tag index still lists {len(left['stale_index'])} deleted resources; each is gone in its own service.\n")
    if left.get("unchecked"):
        say("Tagged and not checked by Reframe:\n" + "".join(f"  - {arn}\n" for arn in left["unchecked"]))
    connector = [s for s in result["steps"] if s["step"] == "connector" and s["outcome"].startswith("left over")]
    if connector:
        say(f"The connector {ctx.names()['connector']} is {connector[0]['outcome']}. Its IAM role is deleted, so it can reach nothing.\n")
    say("Teardown finished.\n" if not left["exists"] else "Teardown finished with resources still in AWS; run reframe teardown again.\n")
    return 0 if not left["exists"] else EXIT_CODES[Outcome.FAILED]
