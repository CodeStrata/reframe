"""Command-line entry point for Reframe v2.

The commands in specification section 13 are added by the stories that
implement them; the command contract itself is P0-07. Until then the CLI
only reports its version and where the specification lives.
"""

from __future__ import annotations

import argparse
from collections.abc import Sequence

from reframe_v2 import __version__

DESCRIPTION = (
    "Reframe v2 (in development). It is built from docs/v2/specification.md "
    "on the v2 branch; no commands are available yet. The v1 CLI, `reframe`, "
    "is frozen."
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="reframe-v2", description=DESCRIPTION)
    parser.add_argument("--version", action="version", version=f"reframe-v2 {__version__}")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    parser.parse_args(argv)
    parser.print_help()
    return 0
