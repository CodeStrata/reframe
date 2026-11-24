"""`reframe --help` and each command's help, in the look of the first console (specification section 3).

The header panel, then a table of commands or options with what each does, then common examples. Errors in the
arguments keep argparse's short usage message on standard error.
"""

from __future__ import annotations

import argparse

from reframe.core import ui

EXAMPLES = {
    "reframe": [
        ("reframe", "the home screen: your runs, the next step and a menu"),
        ("reframe run", "a guided run: checks the prerequisites, the AWS sign-in and the source, then starts"),
        ("reframe run --source <folder | file.zip | github-url>", "start straight away, with no questions"),
        ("reframe status", "where the latest run is, and what to do next"),
        ("reframe answer", "AWS's waiting question, in interactive mode"),
        ("reframe report --open", "open the business review in the browser"),
        ("reframe claude", "pipeline 2: assess the same snapshot with Claude as well"),
        ("reframe compare --open", "open the page comparing AWS Transform and Claude"),
        ("reframe publish --to aws", "upload a cleaned copy of the reports to your account's private bucket"),
        ("reframe reports", "list the published reports; reframe reports open <project> opens the latest"),
        ("reframe teardown", "remove the AWS resources the run created"),
    ],
    "run": [
        ("reframe run", "guided: asks for everything it needs"),
        ("reframe run --source https://github.com/<owner>/<repo>", "a GitHub repository, latest commit"),
        ("reframe run --source ~/code/app --ref release-1", "a local Git checkout, at a branch, tag or commit"),
        ("reframe run --source app.zip --mode interactive", "a ZIP file; you answer AWS's questions with reframe answer"),
    ],
    "answer": [
        ("reframe answer", "show the waiting question and its numbered options"),
        ("reframe answer 1 3", "choose options 1 and 3"),
        ('reframe answer --text "Yes, proceed"', "answer a question that has no options"),
    ],
    "status": [("reframe status", "the latest run"), ("reframe status --run <id>", "another run, by the ID the home screen shows")],
    "events": [("reframe events --follow", "keep printing new events until Ctrl+C")],
    "report": [("reframe report --open", "build the report again and open it")],
    "claude": [("reframe claude", "start pipeline 2 on the latest run, now or as soon as its AWS resources exist"),
               ("reframe claude --max-agents 650", "a higher agent limit, so a larger estimate does not stop to ask")],
    "compare": [("reframe compare --open", "build the comparison page again and open it")],
    "publish": [("reframe publish --to aws", "upload to the private reports bucket in your AWS account"),
                ("reframe publish --to reports/my-system", "write the copy into a folder")],
    "reports": [("reframe reports", "list the published reports"),
                ("reframe reports open <project>", "download the project's latest report with your AWS sign-in and open it"),
                ("reframe reports open <project> --run <run>", "an older run of the project"),
                ("reframe reports download <project> --to <folder>", "save the latest report in a folder, to keep or send on"),
                ("reframe reports teardown", "remove the bucket and every report in it, after your consent")],
    "resume": [("reframe resume", "continue the latest run, and pipeline 2 if it stopped too")],
    "teardown": [("reframe teardown", "list the latest run's AWS resources, then remove them after you type yes")],
}


def _commands(parser: argparse.ArgumentParser) -> list[tuple[str, str]]:
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return [(choice.dest, choice.help or "") for choice in action._choices_actions]
    return []


def _option(action: argparse.Action) -> str:
    if not action.option_strings:
        return f"<{action.dest}>" + (" ..." if action.nargs in ("*", "+") else "")
    names = ", ".join(action.option_strings)
    if action.nargs == 0:
        return names
    if action.choices:
        return f"{names} {'|'.join(map(str, action.choices))}"
    return f"{names} <{(action.metavar or action.dest).lower()}>"


def _options(parser: argparse.ArgumentParser) -> list[tuple[str, str]]:
    rows = []
    for action in parser._actions:
        if isinstance(action, (argparse._HelpAction, argparse._SubParsersAction)) or action.help == argparse.SUPPRESS:
            continue
        rows.append((_option(action), action.help or ""))
    return rows


def _examples(name: str) -> None:
    examples = EXAMPLES.get(name)
    if examples:
        ui.section("Examples")
        ui.table(("", ""), examples, ("bright_cyan", "dim"))


def show(parser: argparse.ArgumentParser) -> None:
    name = parser.prog.split()[-1]
    if name == "reframe":
        ui.header()
        ui.section("Commands")
        ui.table(("Command", "What it does"), [("reframe " + c, h) for c, h in _commands(parser)], ("bold bright_cyan", None))
        _examples(name)
        ui.section("Options")
        ui.table(("", ""), _options(parser) + [("-h, --help", "this help")], ("bright_cyan", None))
        ui.hint("reframe <command> --help shows a command's options.")
        return
    ui.section(parser.prog)
    if parser.description:
        ui.say(parser.description)
    rows = _options(parser)
    if rows:
        ui.section("Options")
        ui.table(("Option", "What it does"), rows, ("bright_cyan", None))
    _examples(name)


class Parser(argparse.ArgumentParser):
    """An argument parser whose --help is drawn in Reframe's console look."""

    def print_help(self, file=None) -> None:  # noqa: ARG002 - help goes to Reframe's console
        show(self)
