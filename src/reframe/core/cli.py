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
    "claude": "reframe.core.commands:claude",
    "reconcile": "reframe.core.commands:reconcile",
    "review": "reframe.core.commands:review",
    "export": "reframe.core.commands:export",
    "design": "reframe.core.commands:design",
    "compare": "reframe.core.commands:compare",
    "publish": "reframe.core.commands:publish",
    "reports": "reframe.core.commands:reports",
    "worker": "reframe.core.commands:worker",
}


def _run_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--run", metavar="RUN", help="the run to act on (default: the latest run)")


def parser() -> argparse.ArgumentParser:
    from reframe.core.helptext import Parser
    top = Parser(prog="reframe", description="Run an AWS Transform mainframe assessment end to end and bring back its requirements.")
    top.add_argument("--version", action="version", version=f"reframe {__version__}")
    commands = top.add_subparsers(dest="command", metavar="<command>")

    def command(name: str, help: str) -> argparse.ArgumentParser:
        return commands.add_parser(name, help=help, description=help)

    run = command("run", "Assess mainframe source with AWS Transform and Claude, or with Claude only (--tools claude, no AWS): with no "
                              "options, a guided run that checks and sets up everything first; the AWS resources stay until reframe teardown")
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
    run.add_argument("--terraform", help="the Terraform binary to use (default: REFRAME_TERRAFORM, then the one Reframe installed, then terraform on PATH)")
    run.add_argument("--foreground", action="store_true", help="run in this terminal instead of a background worker")
    run.add_argument("--tools", choices=("both", "claude"), default="both",
                     help="both: AWS Transform and Claude (needs an AWS account); claude: Claude only, with no AWS at all")
    run.add_argument("--max-agents", type=int, help="with --tools claude: the agent limit for Claude's rule extraction (default 600)")

    setup = command("setup", "Check and set up the prerequisites and the AWS sign-in, without starting a run")
    setup.add_argument("--tools", choices=("both", "claude"), default="both",
                       help="both: everything, with the AWS sign-in; claude: only Git, Claude Code and the plugin, with no AWS")

    status = command("status", "The run's stage, the job's plan steps, any waiting question and the next step")
    _run_option(status)

    events = command("events", "The run's event log")
    _run_option(events)
    events.add_argument("--follow", action="store_true", help="keep printing new events")

    answer = command("answer", "Show AWS's waiting question, or answer it")
    _run_option(answer)
    answer.add_argument("choices", nargs="*", help="option numbers as listed by reframe answer")
    answer.add_argument("--text", help="a free-text answer, for a question without options")

    resume = command("resume", "Continue a run that stopped; nothing with a receipt is repeated")
    _run_option(resume)
    resume.add_argument("--foreground", action="store_true", help="run in this terminal instead of a background worker")

    report = command("report", "Build the HTML report from the run's downloads again")
    _run_option(report)
    report.add_argument("--open", action="store_true", help="open the report in the browser")

    claude = command("claude", "The Claude assessment: assess the same snapshot with Claude's code-modernization plugin, show it in the same "
                     "business review, load its graph into the run's Neptune cluster, and compare it with AWS Transform's results")
    _run_option(claude)
    claude.add_argument("--auth", choices=("subscription", "bedrock"), default=None,
                        help="how Claude signs in: your Claude subscription (default) or Amazon Bedrock with the run's AWS profile")
    claude.add_argument("--max-agents", type=int, default=None, help="the agent limit for rule extraction (default: 600)")
    claude.add_argument("--mode", choices=("autonomous", "interactive"), default=None, help="default: the run's mode")
    claude.add_argument("--graph-load", choices=("yes", "no"), default=None,
                        help="load Claude's graph into the cluster (default: yes on a graph the run created, no on an existing cluster)")
    claude.add_argument("--foreground", action="store_true", help="run in this terminal instead of a background worker")

    reconcile = command("reconcile", "The reconciliation: decide every rule the two assessments do not agree on against the source code, with "
                        "evidence Reframe checks, then write recommended requirements, one SME list and the reconciliation page; needs both "
                        "assessments done, and no AWS resources")
    _run_option(reconcile)
    reconcile.add_argument("--context", help="a folder of context: documents (Markdown, text, PDF, Word), review exports and answered questions")
    reconcile.add_argument("--auth", choices=("subscription", "bedrock"), default=None,
                           help="how Claude signs in (default: as for the Claude assessment)")
    reconcile.add_argument("--max-batches", type=int, default=None, help="the limit for the decisions; Reframe stops and asks above it (default: 120)")
    reconcile.add_argument("--foreground", action="store_true", help="run in this terminal instead of a background worker")
    reconcile.add_argument("--open", action="store_true", help="open the reconciliation page instead of running")

    review = command("review", "Read the review downloads in a folder and show each reviewer's coverage, sign-offs and where reviewers disagree; "
                     "runs nothing, and the next reframe reconcile --context with the same folder combines them")
    _run_option(review)
    review.add_argument("--context", required=True, help="the folder holding the review downloads (JSON or CSV)")

    export = command("export", "Write a run's reconciled results as one Excel workbook: domains, functions, capabilities, requirements, business "
                     "rules, decision tables, open questions and the SME list, with the reviewers' marks; runs nothing")
    _run_option(export)
    export.add_argument("--to", required=True, choices=("xlsx",), help="the format: xlsx, an Excel workbook")
    export.add_argument("--out", help="the file or folder to write it to (default: outputs/reconcile/<project>-<run>-requirements.xlsx in the run folder)")
    export.add_argument("--context", help="a folder of review downloads whose marks to add (default: the reconciliation's context folder)")
    export.add_argument("--open", action="store_true", help="open the workbook when written")

    design = command("design", "The design (pipeline 4): legacy and modern screens, journeys, the clickable prototype, final specifications "
                              "and the AI-DLC package, from the reconciled results; a round redoes only what new context touches")
    _run_option(design)
    design.add_argument("--context", help="the design context folder (default: the one given before, then the run's inputs/design/)")
    design.add_argument("--stack", help='the target stack, "<front end>; <back end>; <data>"; never chosen for you')
    design.add_argument("--plan", action="store_true", help="say what a round would redo, and why, without a Claude step")
    design.add_argument("--package", metavar="FOLDER", help="copy the latest package, cleaned, into an empty folder; runs nothing")
    design.add_argument("--form", choices=("kiro", "claude-code", "spec-kit", "all"), default="all", help="with --package: which form (default: all)")
    design.add_argument("--check", metavar="COPY", help="list the placeholders left in a copy of the package; runs nothing")
    design.add_argument("--open", action="store_true", help="open the design page when done")
    design.add_argument("--auth", choices=("subscription", "bedrock"), default="subscription", help="how Claude signs in (default: your subscription)")

    compare = command("compare", "Build the page comparing AWS Transform's and Claude's results again")
    _run_option(compare)
    compare.add_argument("--open", action="store_true", help="open the page in the browser")

    publish = command("publish", "Optional: copy a run's reports, cleaned of the AWS account's identifiers, into a folder others can open, upload the run's "
                                 "source, results and reports to your account's private bucket, or publish the copy to a GitHub Pages site")
    _run_option(publish)
    publish.add_argument("--to", required=True, help="a folder to write the copy into (for example reports/carddemo); aws to upload it to "
                         "the private Reframe bucket in your AWS account, with the run's source and results; or pages to publish it to a GitHub "
                         "Pages site, which is public, after you type yes")
    publish.add_argument("--repo", help="for --to pages: the GitHub repository, <owner>/<name>; the copy goes on its gh-pages branch")
    publish.add_argument("--profile", help="for --to aws: the AWS profile (default: the one saved by reframe setup)")
    publish.add_argument("--region", help="for --to aws: the AWS region (default: the saved one, then us-east-1)")

    reports = command("reports", "The reports published to your AWS account: list them, open one with your AWS sign-in, or remove the bucket")
    reports.add_argument("action", nargs="?", choices=("list", "open", "download", "teardown"), default="list",
                         help="list (the default): what is published; open: download one and open it; download: save one in a folder; "
                              "teardown: remove the bucket")
    reports.add_argument("path", nargs="?", help="for open and download: a project (its latest run) or <project>/<run>, as reframe reports lists them")
    reports.add_argument("--run", metavar="RUN", help="for open and download: an older run of the project")
    reports.add_argument("--to", help="for download: the folder to save the report in")
    reports.add_argument("--profile", help="the AWS profile (default: the one saved by reframe setup)")
    reports.add_argument("--region", help="the AWS region (default: the saved one, then us-east-1)")

    teardown = command("teardown", "List every AWS resource the run created, ask for consent, record it, then remove them")
    _run_option(teardown)

    worker = commands.add_parser("worker")  # internal: the background worker started by run, resume and teardown
    worker.add_argument("folder")
    worker.add_argument("--task", choices=("run", "teardown", "claude", "reconcile"), default="run")
    return top


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if not args.command:
        from reframe.core import ui
        if ui.interactive():
            from reframe.core.home import main as home
            return home()
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
