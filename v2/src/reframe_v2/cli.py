"""Command-line entry point for Reframe v2.

The commands in specification section 13 are added by the stories that
implement them; the command contract itself is P0-07. Available so far:
bootstrap (P2-04).
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from reframe_v2 import __version__
from reframe_v2.commands import Exit

DESCRIPTION = (
    "Reframe v2 (in development). It is built from docs/v2/specification.md "
    "on the v2 branch; commands arrive as their stories land. The v1 CLI, `reframe`, "
    "is frozen."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reframe-v2", description=DESCRIPTION)
    parser.add_argument("--version", action="version", version=f"reframe-v2 {__version__}")
    commands = parser.add_subparsers(dest="command")
    bootstrap = commands.add_parser("bootstrap", help="Print the bootstrap policy; write the Terraform. No AWS change.")
    bootstrap.add_argument("--print", dest="print_policy", action="store_true", required=True,
                           help="print the policy an administrator grants the engineer once")
    bootstrap.add_argument("--terraform", type=Path, metavar="DIR",
                           help="also write the Terraform module, the state-bucket definition and a resources-file template")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "bootstrap":
        from reframe_v2.bootstrap import BootstrapError, print_text, write_terraform

        sys.stdout.write(print_text())
        if args.terraform is not None:
            try:
                written = write_terraform(args.terraform)
            except BootstrapError as error:
                sys.stderr.write(f"{error}\n")
                return int(Exit.REFUSED)
            sys.stdout.write(f"Wrote {len(written)} files to {args.terraform}. No AWS change was made.\n")
        return int(Exit.OK)
    parser.print_help()
    return int(Exit.OK)
