"""The command handlers behind reframe's CLI (specification section 3)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from reframe.core.errors import EXIT_CODES, Outcome, ReframeError, Stop
from reframe.core.runfolder import RunFolder, find_run, iso, new_run, project_name

say = sys.stdout.write


def _fail(stop: Stop) -> int:
    sys.stderr.write(f"{stop.outcome.value}: {stop.message}\n")
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
    from reframe.core import pipeline
    from reframe.source.snapshot import kind
    try:
        kind(args.source)
        source = args.source if kind(args.source) == "git-url" else str(Path(args.source).expanduser().resolve())
        project = args.project or project_name(args.source.rstrip("/").removesuffix(".zip"))
        folder = new_run(project)
    except (Stop, ReframeError) as error:
        return _fail(error if isinstance(error, Stop) else Stop(Outcome.REFUSED, str(error)))
    folder.update(project=project, source=source, ref=args.ref, mode=args.mode, graph_arg=args.graph, profile=args.profile,
                  region=args.region, terraform=pipeline.terraform_binary(args.terraform), started_at=iso(), stage="preflight", status="RUNNING")
    say(f"Run {folder.root.name} for {project} ({args.mode} mode)\nRun folder: {folder.root}\n")
    ctx = pipeline.Context.load(folder)
    try:
        pipeline.prepare(ctx, _prompt, say)
    except Stop as stop:
        pipeline.record_stop(ctx, stop)
        return _fail(stop)
    graph = ctx.state["graph"]
    say(f"Neptune graph: {'existing cluster ' + graph['name'] if graph['kind'] == 'existing' else 'a new graph for this run'}\n")
    if args.foreground:
        return worker(type("Args", (), {"folder": str(folder.root), "task": "run"})())
    pid = _start_worker(folder)
    say(f"Started in the background (process {pid}). Follow it with:\n  reframe status\n  reframe events --follow\n")
    return 0


def resume(args) -> int:
    try:
        folder = find_run(args.run)
    except Stop as stop:
        return _fail(stop)
    pid = folder.worker_pid()
    if pid:
        say(f"Run {folder.root.name} is already running (process {pid}).\n")
        return 0
    state = folder.state
    if state.get("status") == Outcome.DONE.value:
        say(f"Run {folder.root.name} is done. {state.get('message', '')}\n")
        return 0
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
    pid = _start_worker(folder)
    say(f"Run {folder.root.name} resumed in the background (process {pid}). Follow it with reframe status.\n")
    return 0


def worker(args) -> int:
    from reframe.core import pipeline
    folder = RunFolder(Path(args.folder))
    ctx = pipeline.Context.load(folder)
    try:
        folder.lock()
    except Stop as stop:
        return _fail(stop)
    try:
        folder.event("worker_started", pid=os.getpid())
        outcome = pipeline.work(ctx)
        say(f"{outcome.value}: {folder.state.get('message', '')}\n")
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
        folder.unlock()


# ---- reading the run -----------------------------------------------------------------------------


NEXT = {Outcome.WAITING_SIGNIN.value: "sign in with aws sso login --profile {profile}, then run reframe resume",
        Outcome.WAITING_HUMAN.value: "answer with reframe answer, or fix what the message says, then reframe resume",
        Outcome.REFUSED.value: "fix what the message says, then reframe resume",
        Outcome.UNCERTAIN.value: "run reframe resume; it settles the change from AWS's state",
        Outcome.FAILED.value: "read the message and worker.log; reframe resume tries again, reframe teardown removes the resources"}


def status(args) -> int:
    try:
        folder = find_run(args.run)
    except Stop as stop:
        return _fail(stop)
    state, pid = folder.state, folder.worker_pid()
    say(f"Run {folder.root.name}: {state.get('project')} from {state.get('source')} ({state.get('mode')} mode)\n")
    say(f"Stage: {state.get('stage')} | status: {state.get('status')}" + (f" | worker running (process {pid})" if pid else "") + "\n")
    if state.get("graph"):
        graph = state["graph"]
        say(f"Neptune: {'existing cluster ' + graph['name'] if graph['kind'] == 'existing' else 'new graph'}\n")
    job = state.get("job")
    if job:
        say(f"AWS Transform job: {job['status']} (poll {job['poll']} at {job['at']})\n")
        for step in job.get("steps") or []:
            say(f"  - {step['name']}: {step['status']}\n")
    question = folder.load("question.json")
    if question:
        say(f"\nAWS is waiting for an answer ({question['kind']}). See it with: reframe answer\n")
    if state.get("message"):
        say(f"\n{state['message']}\n")
    if state.get("report"):
        say(f"Report: {folder.path(state['report'])}\n")
    if state.get("torn_down"):
        say(f"Torn down at {state['torn_down']}.\n")
    hint = NEXT.get(str(state.get("status")))
    if hint and not pid:
        say("Next: " + hint.format(profile=state.get("profile")) + "\n")
    elif state.get("status") == Outcome.DONE.value and not state.get("torn_down"):
        say("Next: open the report with reframe report --open; remove the AWS resources with reframe teardown\n")
    return 0


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
        say("AWS is not waiting for an answer.\n")
        return 0
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


# ---- report and teardown -------------------------------------------------------------------------


def report(args) -> int:
    from reframe.report import build
    try:
        folder = find_run(args.run)
        if not folder.exists("outputs/requirements"):
            raise Stop(Outcome.REFUSED, "this run has no downloaded results yet")
    except Stop as stop:
        return _fail(stop)
    path = build.build(folder)
    say(f"Report: {path}\n")
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
    pid = folder.worker_pid()
    if pid:
        return _fail(Stop(Outcome.REFUSED, f"the run's worker is still running (process {pid}); wait for it to stop, or stop it, first"))
    if not sys.stdin.isatty():
        return _fail(Stop(Outcome.REFUSED, "reframe teardown asks for consent, so it needs a terminal"))
    ctx = pipeline.Context.load(folder)
    try:
        folder.lock()
        consented = stage.ask(ctx, _prompt, say)
        if consented is None:
            return 0
        say("\nDeleting, in order. This takes about 15 minutes with a new Neptune graph.\n")
        result = stage.delete(ctx, consented, say)
    except Stop as stop:
        return _fail(stop)
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
