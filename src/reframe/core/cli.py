"""The reframe command line (specification section 3).

Each command's handler lives in its own module and is imported only when the command runs,
so `reframe --help` works without AWS, Terraform or the MCP server installed.
"""

from __future__ import annotations

import argparse
import importlib
import sys

from reframe import __version__

HANDLERS = {
    "run": "reframe.core.commands:run",
    "setup": "reframe.core.guide:setup_only",
    "status": "reframe.core.commands:status",
    "events": "reframe.core.commands:events",
    "answer": "reframe.core.commands:answer",
    "resume": "reframe.core.commands:resume",
    "report": "reframe.core.commands:report",
    "teardown": "reframe.core.commands:teardown",
    "worker": "reframe.core.commands:worker",
}


def _run_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--run", metavar="RUN", help="the run to act on (default: the latest run)")


def parser() -> argparse.ArgumentParser:
    top = argparse.ArgumentParser(prog="reframe", description="Run an AWS Transform mainframe assessment end to end and bring back its requirements.")
    top.add_argument("--version", action="version", version=f"reframe {__version__}")
    commands = top.add_subparsers(dest="command", metavar="<command>")

    run = commands.add_parser("run", help="Assess mainframe source with AWS Transform: with no options, a guided run that checks and sets up "
                              "everything first; the AWS resources stay until reframe teardown")
    run.add_argument("--source", help="the mainframe source: a local folder, a local .zip file, or a GitHub URL; given, nothing is asked "
                     "and the prerequisites are assumed to be set up")
    run.add_argument("--profile", help="the AWS CLI profile to sign in with (default: the one saved by the guided setup)")
    run.add_argument("--ref", help="for a Git checkout or URL: the branch, tag or commit to assess (default: HEAD)")
    run.add_argument("--mode", choices=("autonomous", "interactive"), default="autonomous",
                     help="autonomous: Reframe answers AWS and records why; interactive: answer each question with reframe answer")
    run.add_argument("--region", help="AWS region (default: the one saved by the guided setup, then us-east-1)")
    run.add_argument("--project", help="project name used in resource names (default: from the source's name)")
    run.add_argument("--graph", default=None, help="new, existing (choose from a list) or the name of an existing Neptune cluster "
                     "(default: interactive mode asks; autonomous mode creates a new graph)")
    run.add_argument("--terraform", help="the Terraform binary to use (default: REFRAME_TERRAFORM, then terraform on PATH)")
    run.add_argument("--foreground", action="store_true", help="run in this terminal instead of a background worker")

    commands.add_parser("setup", help="Check and set up the prerequisites and the AWS sign-in, without starting a run")

    status = commands.add_parser("status", help="The run's stage, the job's plan steps, any waiting question and the next step")
    _run_option(status)

    events = commands.add_parser("events", help="The run's event log")
    _run_option(events)
    events.add_argument("--follow", action="store_true", help="keep printing new events")

    answer = commands.add_parser("answer", help="Show AWS's waiting question, or answer it")
    _run_option(answer)
    answer.add_argument("choices", nargs="*", help="option numbers as listed by reframe answer")
    answer.add_argument("--text", help="a free-text answer, for a question without options")

    resume = commands.add_parser("resume", help="Continue a run that stopped; nothing with a receipt is repeated")
    _run_option(resume)
    resume.add_argument("--foreground", action="store_true", help="run in this terminal instead of a background worker")

    report = commands.add_parser("report", help="Build the HTML report from the run's downloads again")
    _run_option(report)
    report.add_argument("--open", action="store_true", help="open the report in the browser")

    teardown = commands.add_parser("teardown", help="List every AWS resource the run created, ask for consent, record it, then remove them")
    _run_option(teardown)

    worker = commands.add_parser("worker")  # internal: the background worker started by run, resume and teardown
    worker.add_argument("folder")
    worker.add_argument("--task", choices=("run", "teardown"), default="run")
    return top


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if not args.command:
        parser().print_help()
        return 2
    from reframe.core.setup import use_saved_paths
    use_saved_paths()
    module, _, name = HANDLERS[args.command].partition(":")
    try:
        handler = getattr(importlib.import_module(module), name)
    except (ImportError, AttributeError):
        sys.stderr.write(f"reframe {args.command} is not built yet.\n")
        return 2
    return int(handler(args) or 0)


if __name__ == "__main__":
    raise SystemExit(main())
