"""The command contract (specification section 13): what each command takes, changes and refuses, and its exit codes.

The CLI implements these as their stories land; tests keep this table in step
with specification section 13, so a command cannot appear or disappear
without a specification change.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass


class Exit(enum.IntEnum):
    OK = 0
    """Done, or the background run started or resumed."""
    UNEXPECTED = 1
    """A defect in Reframe; the message says where the details are."""
    USAGE = 2
    """Arguments are missing or invalid; nothing changed."""
    REFUSED = 3
    """A rule refused the request (policy, budget, version, confirmation, deletion); nothing changed."""
    WAITING = 4
    """No runnable work is left: WAITING_HUMAN or WAITING_EXTERNAL; status lists what it waits on."""
    INTEGRITY = 5
    """Stored content does not match its hash; the damaged copy is kept."""
    UNCERTAIN = 6
    """A call may or may not have happened; settle it with reframe resolve before anything depends on it."""


@dataclass(frozen=True)
class Command:
    name: str
    changes: str
    refuses: tuple[str, ...]
    exits: tuple[Exit, ...]
    story: str


COMMANDS: tuple[Command, ...] = (
    Command("bootstrap", "Nothing in AWS; prints the bootstrap policy, or writes the Terraform module, a state-bucket definition and a resources-file template",
            ("an existing output directory with other files",), (Exit.OK, Exit.USAGE, Exit.REFUSED), "F2-01"),
    Command("run", "Creates the first assessment or resumes the current one, in the background unless --foreground",
            ("a second assessment without --new-assessment", "a changed snapshot or scope without --new-assessment",
             "an uncertain assessment creation before it is settled", "a destination outside the data policy",
             "--clean-start without --provision", "a live lease held by another machine"),
            (Exit.OK, Exit.USAGE, Exit.REFUSED, Exit.WAITING, Exit.INTEGRITY, Exit.UNCERTAIN), "P1-02, P1-05, F3-01"),
    Command("status", "Nothing; reports stage, open gates and deadlines, parked work and why, reruns, cost, readiness and running resources",
            (), (Exit.OK, Exit.WAITING, Exit.INTEGRITY), "P0-04"),
    Command("stop", "Stops the worker after its current step; past --timeout the step is left UNCERTAIN",
            (), (Exit.OK, Exit.UNCERTAIN), "P0-07"),
    Command("events", "Nothing; shows the event log, following it with --follow", (), (Exit.OK,), "P0-07"),
    Command("resolve", "Records a person's settlement of an UNCERTAIN operation, or authorizes one more counted attempt",
            ("an operation that is not UNCERTAIN", "no --by"), (Exit.OK, Exit.USAGE, Exit.REFUSED), "P0-05"),
    Command("budget", "Raises an allowance, recorded with who and why",
            ("no --by or --reason", "a value below the current allowance"), (Exit.OK, Exit.USAGE, Exit.REFUSED), "P0-05"),
    Command("context add", "Adds context, decisions or local feedback; --for is a hint, not a limit",
            ("a file that is not valid context",), (Exit.OK, Exit.USAGE, Exit.REFUSED), "F2-05, F3-02"),
    Command("continue", "Records context and feedback for an open gate with who gave it; reruns what it affects",
            ("no --by", "a closed gate (the input goes to the next revision)", "--stack or --tool before gate 3"),
            (Exit.OK, Exit.USAGE, Exit.REFUSED), "F2-05"),
    Command("accept", "Records a named person's acceptance of an exact version, including after a timeout",
            ("a version that does not exist or is stale", "gate 3 accepted by anyone but the design owner"),
            (Exit.OK, Exit.USAGE, Exit.REFUSED), "P0-04, F2-05"),
    Command("design owner", "Names the gate 3 design owner and sets or extends the deadline",
            ("a deadline earlier than the current one",), (Exit.OK, Exit.USAGE, Exit.REFUSED), "F2-05"),
    Command("design export", "Writes design.json, the HTML pages and the base hash", (), (Exit.OK, Exit.USAGE), "F3-03"),
    Command("design import", "Imports an edited design under section 9's rules",
            ("a stale base", "a conflicting import", "behavioural HTML changes without the same design.json change",
             "removing a verified rule without a decision", "unknown interactions", "disallowed HTML"),
            (Exit.OK, Exit.USAGE, Exit.REFUSED), "F3-03"),
    Command("resources adopt", "Records an existing stack in the manifest as Reframe-owned and tags it, after checks and confirmation",
            ("a client-owned, shared, busy or unknown stack", "no confirmation"), (Exit.OK, Exit.USAGE, Exit.REFUSED), "P0-13, F3-07"),
    Command("teardown", "Deletes manifest-owned resources after confirmation and checks; keeps project data unless --include-data",
            ("anything not eligible under the deletion rules", "--include-data without a verified export"),
            (Exit.OK, Exit.USAGE, Exit.REFUSED), "P0-13, F3-07"),
    Command("export", "Writes a verified archive of the project's data, canonical model, ledger and package",
            ("an output directory with other files",), (Exit.OK, Exit.USAGE, Exit.REFUSED, Exit.INTEGRITY), "F3-07"),
    Command("import-v1", "Copies AWS evidence and receipts from a v1 workspace into a new v2 project",
            ("creating jobs, spending model calls, resetting counters or transferring approvals",),
            (Exit.OK, Exit.USAGE, Exit.REFUSED, Exit.INTEGRITY), "F3-08"),
)


def command(name: str) -> Command:
    for entry in COMMANDS:
        if entry.name == name:
            return entry
    raise KeyError(name)
