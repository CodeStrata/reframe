"""`reframe` on its own: the home screen, in the look of the first console (specification section 3).

The header, the runs with their status, the suggested next step and a numbered menu. Each menu entry runs the same
command a person could type, through reframe's own command line, so the home screen adds no behaviour of its own.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from rich import box
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from reframe.core import ui
from reframe.core.runfolder import RunFolder, home

SHOWN = 8
MENU = [  # (title, needs a run, the command line)
    ("Start a guided run", False, ["run"]),
    ("Run status", True, ["status"]),
    ("Answer a waiting question", True, ["answer"]),
    ("Resume a run", True, ["resume"]),
    ("Open the business review", True, ["report", "--open"]),
    ("Assess with Claude (pipeline 2)", True, ["claude"]),
    ("Open the comparison", True, ["compare", "--open"]),
    ("Publish a run's reports to AWS", True, ["publish", "--to", "aws"]),
    ("Published reports", False, ["reports"]),
    ("Event log", True, ["events"]),
    ("Tear down a run", True, ["teardown"]),
    ("Set up prerequisites and sign-in", False, ["setup"]),
    ("Help", False, ["--help"]),
]


@dataclass
class Run:
    folder: RunFolder
    state: dict[str, Any]
    working: bool

    @property
    def id(self) -> str:
        return self.folder.root.name

    @property
    def resources(self) -> str:
        if self.state.get("torn_down"):
            return "removed"
        changes = self.folder.root / "changes"
        return "in place" if changes.is_dir() and any(changes.glob("*.receipt.json")) else "none"


def runs() -> list[Run]:
    found = []
    for path in (home() / "projects").glob("*/runs/*/run.json"):
        try:
            state = json.loads(path.read_text())
        except (OSError, ValueError):
            continue
        folder = RunFolder(path.parent)
        found.append(Run(folder, state, bool(folder.worker_pid("run") or folder.worker_pid("claude"))))
    return sorted(found, key=lambda r: str(r.state.get("started_at") or ""), reverse=True)


def _when(value: Any) -> str:
    text = str(value or "")
    return text[:16].replace("T", " ") + " UTC" if text.endswith("Z") else text


def number(command: str) -> int:
    """The menu number of a command, so the suggested next step stays right when the menu changes."""
    return next(n for n, (_, _, argv) in enumerate(MENU, 1) if argv[0] == command)


def next_step(latest: Run | None) -> str:
    from reframe.core.commands import NEXT
    if latest is None:
        return f"choose {number('run')} to start a guided run"
    status = str(latest.state.get("status"))
    if latest.working:
        return f"run {latest.id} is working; choose {number('status')} to see where it is"
    if latest.state.get("torn_down"):
        return f"choose {number('run')} to start another run"
    claude = latest.state.get("claude") or {}
    if status == "DONE" and claude.get("status") == "DONE":
        return f"choose {number('compare')} to open the comparison of run {latest.id}; choose {number('teardown')} to remove its AWS resources"
    if status == "DONE" and claude.get("status") in ("RUNNING", "REQUESTED"):
        return f"run {latest.id} is done with AWS Transform; the Claude assessment follows (choose {number('status')} to see where it is)"
    if status == "DONE" and claude.get("status"):
        return f"pipeline 2 stopped ({claude.get('status')}): choose {number('status')} for the reason; choose {number('resume')} to resume"
    if status == "DONE":
        return (f"choose {number('report')} to open the business review of run {latest.id}; choose {number('claude')} to assess the same snapshot "
                f"with Claude; choose {number('teardown')} to remove its AWS resources")
    hint = NEXT.get(status)
    return hint.format(profile=latest.state.get("profile")) if hint else f"choose {number('status')} to see where the latest run is"


def dashboard(all_runs: list[Run]) -> None:
    from reframe.core.commands import STATUS_STYLE
    ui.header()
    ui.console.print()
    if not all_runs:
        ui.console.print(Panel("Choose 1 to start a guided run. Reframe checks what this computer needs, signs you in to AWS, takes the "
                               "source and asks each choice before anything is created.", title="Welcome", border_style="blue"))
    else:
        grid = Table(box=box.SIMPLE, expand=True, show_edge=False)
        for name, style in (("Run", "bold"), ("Project", None), ("Status", None), ("Stage", None), ("Claude", None), ("Started", "dim"), ("AWS resources", None)):
            grid.add_column(name, style=style, overflow="fold")
        for run in all_runs[:SHOWN]:
            status = str(run.state.get("status") or "")
            grid.add_row(run.id, str(run.state.get("project") or ""),
                         Text(status + (" ●" if run.working else ""), style=STATUS_STYLE.get(status, "bold yellow")),
                         str(run.state.get("stage") or ""),
                         Text(str((run.state.get("claude") or {}).get("status") or "–").replace("REQUESTED", "after AWS"),
                              style=STATUS_STYLE.get(str((run.state.get("claude") or {}).get("status")), "dim")),
                         _when(run.state.get("started_at")),
                         Text(run.resources, style={"in place": "yellow", "removed": "dim"}.get(run.resources, "dim")))
        ui.console.print(grid)
        if len(all_runs) > SHOWN:
            ui.hint(f"{len(all_runs) - SHOWN} older runs are not shown; reframe status --run <id> reads any run.")
    ui.console.print()
    ui.state("Suggested next step", next_step(all_runs[0] if all_runs else None), "bright_cyan")
    menu()


def menu() -> None:
    grid = Table.grid(expand=True, padding=(0, 2))
    grid.add_column()
    grid.add_column()
    entries = [f"{n:>2}  {title}" for n, (title, _, _) in enumerate(MENU, 1)] + [" 0  Exit"]
    half = (len(entries) + 1) // 2
    for left, right in zip(entries[:half], entries[half:] + [""]):
        grid.add_row(Text(left), Text(right))
    ui.console.print(Panel(grid, title="Menu", border_style="blue"))
    ui.hint("reframe <command> --help  a command's options   ·   reframe run --source …  run with no questions   ·   Ctrl+C  back to the menu")


def pick(all_runs: list[Run]) -> Run | None:
    if not all_runs:
        ui.warn(f"There is no run yet; choose {number('run')} to start one.")
        return None
    if len(all_runs) == 1:
        return all_runs[0]
    shown = all_runs[:SHOWN]
    chosen = ui.choose("Which run?", [(f"{r.id}  {r.state.get('project')}", f"{r.state.get('status')} · {r.state.get('stage')}") for r in shown])
    return shown[chosen - 1]


def main() -> int:
    from reframe.core.cli import main as command_line
    from reframe.core.cli import parser
    from reframe.core.helptext import show
    while True:
        all_runs = runs()
        try:
            dashboard(all_runs)
            value = ui.ask("Choose", "1" if not all_runs else None, check=lambda v: None if v.isdigit() and 0 <= int(v) <= len(MENU)
                           else f"Choose a number from 0 to {len(MENU)}.")
            if value == "0":
                return 0
            title, needs_run, argv = MENU[int(value) - 1]
            if argv == ["--help"]:
                show(parser())
            else:
                run = pick(all_runs) if needs_run else None
                if not needs_run or run:
                    ui.section(title)
                    command_line(argv + (["--run", run.id] if run else []))
            ui.console.print()
            ui.ask("Press Enter for the menu")
        except KeyboardInterrupt:
            ui.console.print()
            ui.hint("Cancelled; back to the menu.")
        except EOFError:
            ui.console.print()
            return 0
