"""Command-line entry point for Reframe v2.

The commands in specification section 13 are added by the stories that
implement them; the command contract itself is P0-07. Available so far:
bootstrap (P2-04), graph (P2-06).
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
    graph = commands.add_parser("graph", help="Choose an existing Neptune graph by name, or a new one in the default VPC. No AWS change.")
    graph.add_argument("--profile", required=True, help="the AWS profile you signed in with")
    graph.add_argument("--region", required=True)
    graph.add_argument("--bucket", required=True, help="the bucket the reimagine connector will use")
    answer = graph.add_mutually_exclusive_group()
    answer.add_argument("--use", metavar="CLUSTER", help="use this existing cluster without being asked")
    answer.add_argument("--new", action="store_true", help="create a new graph without being asked")
    graph.add_argument("--tfvars", type=Path, metavar="FILE", help="write the Terraform variables for the choice to this new file")
    return parser


def run_graph(args, reader=None, prompt=input, interactive=None) -> int:
    from reframe_v2.neptune import (AwsCliGraphReader, GraphError, ReaderError, ask, candidates, choose,
                                    default_network, describe, terraform_variables, write_variables)

    reader = reader or AwsCliGraphReader(args.region, args.profile)
    interactive = sys.stdin.isatty() if interactive is None else interactive
    try:
        found = candidates(reader, args.bucket)
        if args.use is not None or args.new:
            sys.stdout.write(describe(found))
            chosen = choose(found, use=args.use, new=args.new)
        elif interactive:
            chosen = ask(found, prompt, sys.stdout.write)
        elif any(c.usable for c in found):
            sys.stdout.write(describe(found))
            sys.stderr.write("A usable cluster exists. Answer with --use <name> to use it, or --new to create a graph.\n")
            return int(Exit.WAITING)
        else:
            sys.stdout.write(describe(found))
            chosen = None
        variables = terraform_variables(chosen, default_network(reader) if chosen is None else None)
        if chosen is not None:
            sys.stdout.write(f"Using {chosen.name}. Reframe will not tag, change or delete it.\n")
        else:
            network = variables["graph_network"]
            endpoint = ("and an S3 gateway endpoint on " + str(len(network["s3_endpoint_route_table_ids"])) + " route table(s)"
                        if network["s3_endpoint_route_table_ids"] else "and no S3 endpoint, because one is already there")
            sys.stdout.write(f"A new graph will go in the default VPC, in 2 of its subnets, with new security groups {endpoint}. "
                             "Neptune bills from the moment it is created.\n")
        if args.tfvars is not None:
            write_variables(args.tfvars, variables)
            sys.stdout.write(f"Wrote {args.tfvars}. It names your account: keep it out of version control. No AWS change was made.\n")
        else:
            import json

            sys.stdout.write(json.dumps(variables, indent=2) + "\n")
    except ReaderError as error:
        sys.stderr.write(f"A read-only check could not be made ({error}). Sign in again if your session expired, then rerun.\n")
        return int(Exit.WAITING)
    except GraphError as error:
        sys.stderr.write(f"{error}\n")
        return int(Exit.REFUSED)
    return int(Exit.OK)


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
    if args.command == "graph":
        return run_graph(args)
    parser.print_help()
    return int(Exit.OK)
