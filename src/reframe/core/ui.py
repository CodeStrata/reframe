"""The look of Reframe's console (specification section 3), after the first console (v1).

A REFRAME header panel naming the steps, coloured status lines, simple tables and numbered choices. Output goes through
rich, which prints plain text when stdout is not a terminal. Questions need a terminal; without one they raise EOFError,
so a caller can say what flag to pass instead.
"""

from __future__ import annotations

import sys
from typing import Iterable, Sequence

from rich import box
from rich.console import Console
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console(highlight=False)
errors = Console(highlight=False, stderr=True)
STEPS = "Prerequisites  →  Sign in  →  Source  →  AWS Transform and Claude  →  Reconcile  →  Review"


def header(subtitle: str = "AWS Transform · Claude · Reconciliation") -> None:
    content = Text("REFRAME\n", style="bold bright_cyan")
    content.append("From mainframe source to requirements and business rules your business can review\n", style="bold white")
    content.append(STEPS, style="dim")
    console.print(Panel(content, border_style="cyan", padding=(1, 2), subtitle=subtitle))


def section(title: str) -> None:
    console.print()
    console.print(Text(title, style="bold bright_cyan"))


def say(text: str = "", style: str | None = None) -> None:
    console.print(Text(text, style=style) if style else Text(text))


def ok(text: str) -> None:
    console.print(Text("✓ ", style="bold green") + Text(text))


def warn(text: str) -> None:
    console.print(Text("! ", style="bold yellow") + Text(text, style="yellow"))


def fail(text: str) -> None:
    console.print(Text("✗ ", style="bold red") + Text(text, style="red"))


def error(text: str) -> None:
    errors.print(Text("✗ ", style="bold red") + Text(text, style="red"))


def hint(text: str) -> None:
    console.print(Text(text, style="dim"))


def state(label: str, value: str, style: str = "bold yellow") -> None:
    console.print(Text(label + "  ", style="bold") + Text(value, style=style))


def command(text: str) -> None:
    console.print(Text("  " + text, style="bright_cyan"))


def table(columns: Sequence[str], rows: Iterable[Sequence[str]], styles: Sequence[str | None] = ()) -> None:
    grid = Table(box=box.SIMPLE, expand=True, show_edge=False, show_header=any(columns))
    for i, name in enumerate(columns):
        grid.add_column(name, style=styles[i] if i < len(styles) else None, overflow="fold")
    for row in rows:
        grid.add_row(*row)
    console.print(grid)


def panel(body: str, title: str, style: str = "blue") -> None:
    console.print(Panel(Text(body), title=escape(title), border_style=style, padding=(0, 2)))


# ---- questions ------------------------------------------------------------------------------------


def interactive() -> bool:
    return sys.stdin.isatty() and sys.stdout.isatty()


def _read(prompt: Text) -> str:
    if not sys.stdin.isatty():
        raise EOFError
    console.print(prompt, end="")
    line = sys.stdin.readline()
    if line == "":
        raise EOFError
    return line.strip()


def ask(label: str, default: str | None = None, check=None) -> str:
    """One value. `check` returns an error message for a bad value, or None; the question is asked again."""
    while True:
        prompt = Text(label, style="bold") + (Text(f" [{default}]", style="dim") if default else Text("")) + Text(": ")
        value = _read(prompt) or (default or "")
        if "\n" in value or value.startswith(("{", "[")):
            fail("Enter one value, not pasted JSON or several lines.")
            continue
        problem = check(value) if check else None
        if problem:
            fail(problem)
            continue
        return value


def yes(label: str, default: bool = True) -> bool:
    while True:
        value = _read(Text(label, style="bold") + Text(" [Y/n]: " if default else " [y/N]: ", style="dim")).lower()
        if not value:
            return default
        if value in ("y", "yes", "n", "no"):
            return value.startswith("y")
        fail("Answer y or n.")


def choose(label: str, options: Sequence[tuple[str, str]], default: int = 1) -> int:
    """Numbered choices: (title, detail) pairs. Returns the 1-based choice."""
    section(label)
    for number, (title, detail) in enumerate(options, 1):
        console.print(Text(f"  {number}  ", style="bold bright_cyan") + Text(title, style="bold") + (Text("  " + detail, style="dim") if detail else Text("")))
    while True:
        value = _read(Text("Choose", style="bold") + Text(f" [{default}]: ", style="dim")) or str(default)
        if value.isdigit() and 1 <= int(value) <= len(options):
            return int(value)
        fail(f"Choose a number from 1 to {len(options)}.")
