"""Spike P3-01: decide three batches of a run's rules against the source, and measure (docs/spikes/p3-01-reconcile.md).

    python docs/spikes/p3-01-reconcile.py <run folder> build     # write the three batches, no Claude
    python docs/spikes/p3-01-reconcile.py <run folder> run       # decide them with Claude Code, check the evidence, measure

Not product code: pipeline 3's stories build the real thing from what this finds.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml  # a Reframe dependency, for AWS Transform's traceability files

from reframe.claude.runner import ClaudeCode, environment
from reframe.claude.workspace import paths
from reframe.core.runfolder import RunFolder
from reframe.report.build import collect, collect_claude

BATCH = 12

SCHEMA_1 = {"type": "object", "required": ["decisions"], "properties": {"decisions": {"type": "array", "items": {
    "type": "object", "required": ["item", "decision", "rule", "evidence", "reason", "confidence", "question"],
    "properties": {
        "item": {"type": "string"},
        "decision": {"type": "string", "enum": ["merged", "aws", "claude", "rewritten", "kept", "rejected", "needs_sme"]},
        "rule": {"type": "string"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "question": {"type": "string"}}}}}}

PROMPT_1 = """Read {input}. It holds business rules about the program {program} of a legacy system, written by two tools that assessed the same source: "aws" (AWS Transform) and "claude" (Claude's code-modernization plugin). The source is read-only under {legacy}/. Each rule gives the source lines its tool cited.

Decide each item against the source code, not by preferring either tool. Read the cited lines and what is around them; follow a PERFORM, CALL or copybook if the decision depends on it.

- kind "overlapping": write one rule that keeps every detail the code supports from both; decision "merged". If one side is simply right and the other adds nothing true, use "aws" or "claude".
- kind "conflicting": decide which side the code supports ("aws" or "claude"); if neither is right, "rewritten" with the rule the code supports.
- kind "aws_only" or "claude_only": "kept" if the code supports the rule (rewrite it if a detail is wrong), "rejected" if it does not.
- If the code cannot settle it (the behaviour depends on data, configuration or a program not in the source), "needs_sme" with one question a subject-matter expert can answer.

For every decision except "needs_sme", give evidence: the lines that support it, as "<path>:<start>-<end>" or "<path>:<line>", with paths relative to {legacy}/ exactly as the files are named. Write each rule as one sentence in the form "WHEN <condition>, THE <system part> SHALL <behaviour>" (or "THE <system part> SHALL <behaviour>" when it always applies), naming values and conditions as the code has them. Give a one or two sentence reason naming what in the code decided it, and a confidence. "question" is empty unless the decision is "needs_sme"; "rule" is empty for "rejected". Answer for every item, using its key exactly. Answer only with the JSON."""

# Round 2: round 1's rules were right but long (up to 178 words) and full of code names. A rule may now be split, is written
# for business reviewers, says whether a one-sided rule was corrected, and reports code behaviour that looks unintended.
SCHEMA = {"type": "object", "required": ["decisions"], "properties": {"decisions": {"type": "array", "items": {
    "type": "object", "required": ["item", "decision", "rules", "changed", "evidence", "reason", "confidence", "question", "defect"],
    "properties": {
        "item": {"type": "string"},
        "decision": {"type": "string", "enum": ["merged", "aws", "claude", "rewritten", "kept", "rejected", "needs_sme"]},
        "rules": {"type": "array", "items": {"type": "string"}, "maxItems": 3},
        "changed": {"type": "boolean"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "question": {"type": "string"},
        "defect": {"type": "string"}}}}}}

PROMPT = PROMPT_1.replace(
    'Write each rule as one sentence in the form "WHEN <condition>, THE <system part> SHALL <behaviour>" (or "THE <system part> SHALL <behaviour>" when it always applies), naming values and conditions as the code has them.',
    'Write the rules for business reviewers who do not read COBOL: plain business language, one sentence each in the form "WHEN <condition>, THE <system part> SHALL <behaviour>" (or "THE <system part> SHALL <behaviour>" when it always applies), at most about 50 words. Give values, codes and messages as the code has them, but name a field, flag or paragraph only in parentheses, and only where a reviewer needs it to check the rule. If the behaviour has separate conditions, split it into up to three rules rather than one long one. "changed" says whether your rule corrects the wording or facts of the tool\'s rule. If the code does something that looks unintended (a case it reports wrongly, a check it skips), describe it in "defect"; otherwise leave it empty.').replace(
    '"rule" is empty for "rejected"', '"rules" is empty for "rejected"')

assert PROMPT != PROMPT_1 and "rules\" is empty" in PROMPT

CITE = re.compile(r"^(?P<path>[^:]+):(?P<start>\d+)(?:-(?P<end>\d+))?$")


def source_files(legacy: Path) -> dict[str, list[str]]:
    """Program name -> source files with that stem, as paths relative to the snapshot."""
    found: dict[str, list[str]] = defaultdict(list)
    for f in legacy.rglob("*"):
        if f.is_file() and f.suffix.lower() in (".cbl", ".cob", ".jcl", ".cpy", ".bms", ".prc", ".proc", ".asm", ".pli", ".ctl"):
            found[f.stem.upper()].append(str(f.relative_to(legacy)))
    return found


def aws_lines(folder: RunFolder) -> dict[str, list[tuple[str | None, list[int]]]]:
    """AWS Transform rule ID -> its traceability_lines, from the traceability files of every business function. They come in
    two shapes: line numbers in the program's own file, or {file, lines} for another file (a JCL procedure, a copybook)."""
    found = {}
    for path in folder.path("outputs/requirements").rglob("traceability.yaml"):
        for rule in (yaml.safe_load(path.read_text()) or {}).get("rules") or []:
            own, other = [], []
            for entry in rule.get("traceability_lines") or []:
                if isinstance(entry, dict):
                    other.append((str(entry.get("file")), [int(n) for n in entry.get("lines") or []]))
                else:
                    own.append(int(entry))
            found[str(rule.get("rule_id"))] = ([(None, own)] if own else []) + other
    return found


def ranges(numbers: list[int]) -> str:
    numbers, out = sorted(set(numbers)), []
    for n in numbers:
        if out and n == out[-1][1] + 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    return ",".join(f"{a}-{b}" if a != b else str(a) for a, b in out)


def items(folder: RunFolder) -> dict[str, list[dict]]:
    """Every pipeline 3 item by program: the comparison's pairs other than "same", and the rules in no pair."""
    legacy = paths(folder)["legacy"]
    files, traced = source_files(legacy), aws_lines(folder)
    aws = {r["key"]: r for r in collect(folder)["rules"] if r["disposition"] == "captured"}
    claude = {r["key"]: r for r in collect_claude(folder)["rules"]}
    pairs = folder.load("outputs/comparison/ai-pairs.json")["pairs"]

    def side(rule: dict, tool: str) -> dict:
        if tool == "aws":
            where = files.get(str(rule["program"]).upper(), [])
            cites = []
            for file, lines in traced.get(rule["id"], []):
                for f in ([file] if file else where):
                    cites.append(f"{f}:{ranges(lines)}" if lines else f)
            cites = cites or where
        else:
            cites = [rule.get("source")] if rule.get("source") else []
        return {"key": rule["key"], "name": rule.get("name", ""), "text": rule.get("text", ""), "cites": cites}

    by_program: dict[str, list[dict]] = defaultdict(list)
    for p in pairs:
        if p["relation"] == "same" or p["aws"] not in aws or p["claude"] not in claude:
            continue
        program = str(aws[p["aws"]]["program"]).upper()
        by_program[program].append({"item": f"{p['aws']}|{p['claude']}", "kind": p["relation"], "aws": side(aws[p["aws"]], "aws"),
                                    "claude": side(claude[p["claude"]], "claude"), "comparison": p.get("reason", "")})
    paired_aws, paired_claude = {p["aws"] for p in pairs}, {p["claude"] for p in pairs}
    for k, r in aws.items():
        if k not in paired_aws:
            by_program[str(r["program"]).upper()].append({"item": k, "kind": "aws_only", "aws": side(r, "aws")})
    for k, r in claude.items():
        if k not in paired_claude:
            by_program[str(r["program"]).upper()].append({"item": k, "kind": "claude_only", "claude": side(r, "claude")})
    return by_program


def choose(by_program: dict[str, list[dict]]) -> list[tuple[str, list[dict]]]:
    """Three batches: one with a conflict, one of overlapping pairs, one of rules only one tool found."""
    def kinds(program, *wanted):
        return [i for i in by_program[program] if i["kind"] in wanted]
    conflict = next(p for p in sorted(by_program) if kinds(p, "conflicting"))
    first = sorted(by_program[conflict], key=lambda i: i["kind"] != "conflicting")[:BATCH]
    overlap = max((p for p in by_program if p != conflict), key=lambda p: len(kinds(p, "overlapping")))
    one_sided = max((p for p in by_program if p not in (conflict, overlap)),
                    key=lambda p: min(len(kinds(p, "aws_only")), len(kinds(p, "claude_only"))) * 100 + len(kinds(p, "aws_only", "claude_only")))
    third = (kinds(one_sided, "claude_only")[:BATCH // 2] + kinds(one_sided, "aws_only"))[:BATCH]
    return [(conflict, first), (overlap, kinds(overlap, "overlapping")[:BATCH]), (one_sided, third)]


def check(evidence: list[str], legacy: Path) -> list[str]:
    """The evidence that does not exist in the snapshot."""
    bad = []
    for cite in evidence:
        m = CITE.match(cite.strip())
        target = (legacy / m["path"]).resolve() if m else None
        if not m or not target.is_file() or not target.is_relative_to(legacy.resolve()):
            bad.append(cite)
            continue
        count = len(target.read_text(errors="replace").splitlines())
        start, end = int(m["start"]), int(m["end"] or m["start"])
        if not 1 <= start <= end <= count:
            bad.append(cite)
    return bad


def main() -> None:
    folder, action = RunFolder(Path(sys.argv[1]).expanduser()), sys.argv[2]
    places, project = paths(folder), folder.state["project"]
    out = places["analysis"] / "reframe"
    out.mkdir(parents=True, exist_ok=True)
    by_program = items(folder)
    counts = defaultdict(int)
    for group in by_program.values():
        for i in group:
            counts[i["kind"]] += 1
    batches = choose(by_program)
    if action == "build":
        print(json.dumps({"items": dict(counts), "programs": len(by_program),
                          "batches_of_12": sum((len(g) + BATCH - 1) // BATCH for g in by_program.values()),
                          "chosen": [{"program": p, "items": len(b), "kinds": sorted({i["kind"] for i in b})} for p, b in batches]}, indent=1))
        for n, (program, batch) in enumerate(batches, 1):
            (out / f"reconcile-spike-{n}.json").write_text(json.dumps({"program": program, "items": batch}, indent=1))
        return
    code = ClaudeCode(places["root"], places["policy"], Path(sys.argv[3]).expanduser(), places["logs"], environment("subscription"))
    results = []
    only = {int(a) for a in sys.argv[4:]}  # rerun some batches with round 2's prompt and schema
    for n, (program, batch) in enumerate(batches, 1):
        if only and n not in only:
            continue
        name = f"reconcile-spike-{n}" + ("-round2" if only else "")
        step = code.run(name, PROMPT.format(input=f"analysis/{project}/reframe/reconcile-spike-{n}.json", program=program, legacy=f"legacy/{project}"),
                        timeout=3600, schema=SCHEMA)
        answer = (code.structured(step) or {}).get("decisions") or [] if step.ok else []
        keys = {i["item"] for i in batch}
        checked = []
        for d in answer:
            d["missing_evidence"] = check(d.get("evidence") or [], places["legacy"]) if d.get("decision") != "needs_sme" else []
            checked.append(d)
        results.append({"batch": n, "program": program, "items": len(batch), "kinds": sorted({i["kind"] for i in batch}),
                        **{k: v for k, v in step.as_json().items() if k in ("ok", "seconds", "tokens", "cost_usd", "problem")},
                        "answered": len([d for d in checked if d.get("item") in keys]),
                        "unknown_keys": [d.get("item") for d in checked if d.get("item") not in keys],
                        "decisions": {k: sum(1 for d in checked if d.get("decision") == k) for k in SCHEMA["properties"]["decisions"]["items"]["properties"]["decision"]["enum"]},
                        "evidence_failed": [d["item"] for d in checked if d["missing_evidence"]],
                        "answer": checked})
        (out / f"{name}-result.json").write_text(json.dumps(results[-1], indent=1))
        print(json.dumps({k: v for k, v in results[-1].items() if k != "answer"}))
        if not step.ok:
            break


if __name__ == "__main__":
    main()
