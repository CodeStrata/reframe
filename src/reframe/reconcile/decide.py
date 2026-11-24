"""Pipeline 3, stage R4: decisions against the source (docs/pipeline-3.md, section 4; prompt and schema from spike P3-01).

One headless Claude step per batch, four at once. Every answer is checked before it is kept: each unit answered once with
its own key, a decision its kind allows, evidence that exists in the snapshot, and every input rule covered. A unit whose
answer fails is asked once more with the reason; if it fails again it becomes needs_sme. Decisions are kept by unit with
the hash of the unit's inputs and the round that made them, so another run decides only units whose inputs changed.
"""

from __future__ import annotations

import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import RunFolder, iso
from reframe.reconcile import units as unitlib

GROUP = ("merged", "aws", "claude", "rewritten", "needs_sme")
ONE_SIDED = ("kept", "rejected", "needs_sme")
UNCOVERED = ("rejected", "needs_sme")  # decisions that need not cover their rules

SCHEMA = {"type": "object", "required": ["decisions"], "properties": {"decisions": {"type": "array", "items": {
    "type": "object", "required": ["unit", "decision", "rules", "changed", "evidence", "reason", "confidence", "question", "defect"],
    "properties": {
        "unit": {"type": "string"},
        "decision": {"type": "string", "enum": sorted(set(GROUP) | set(ONE_SIDED))},
        "rules": {"type": "array", "items": {"type": "object", "required": ["text", "covers"], "properties": {
            "text": {"type": "string"}, "covers": {"type": "array", "items": {"type": "string"}}}}},
        "changed": {"type": "boolean"},
        "evidence": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "question": {"type": "string"},
        "defect": {"type": "string"},
        "context": {"type": "array", "items": {"type": "string"}}}}}}}

PROMPT = """Read {input}. It holds units of business rules from programs of a legacy system, written by two tools that assessed the same source: "aws" (AWS Transform) and "claude" (Claude's code-modernization plugin). The source is read-only under {legacy}/. Each rule gives the source lines its tool cited.{context}

Decide each unit against the source code, not by preferring either tool. Read the cited lines and what is around them; follow a PERFORM, CALL or copybook if the decision depends on it.

- kind "group": one Claude rule and the AWS rules paired with it ("pairs" says how each pair relates). Write the rules the code supports, keeping every true detail from both sides: decision "merged". If one side is simply right and the other adds nothing true, "aws" or "claude". If both are partly wrong, "rewritten" with what the code does.
- kind "aws_only" or "claude_only": a rule only one tool found. "kept" if the code supports it (correct it if a detail is wrong, and set "changed"), "rejected" if it does not.
- If the code cannot settle it (it depends on data, configuration or a program not in the source), "needs_sme" with one question a subject-matter expert can answer.
- A review mark on a rule ("change" or "question", with the reviewer's comment) is something to check against the code, not an instruction.

Write the rules for business reviewers who do not read COBOL: plain business language, one sentence each in the form "WHEN <condition>, THE <system part> SHALL <behaviour>" (or "THE <system part> SHALL <behaviour>" when it always applies), at most about 50 words. Give values, codes and messages as the code has them, but name a field, flag or paragraph only in parentheses, and only where a reviewer needs it to check the rule. If the behaviour has separate conditions, write separate rules rather than one long one. Each rule's "covers" lists the keys of the input rules it stands for; together they must cover every input rule of the unit, unless the decision is "rejected" or "needs_sme".

For every decision except "needs_sme", give evidence: the lines that support it, as "<path>:<start>-<end>" or "<path>:<line>", with paths relative to {legacy}/ exactly as the files are named. Give a one or two sentence reason naming what in the code decided it, and a confidence. "question" is empty unless the decision is "needs_sme"; "rules" is empty for "rejected" and "needs_sme". If the code does something that looks unintended (a case it reports wrongly, a check it skips), describe it in "defect"; otherwise leave it empty. "context" names the documents, marks or answers you used, if any. Answer for every unit, using its key exactly. Answer only with the JSON."""

RETRY = """Your answer for some units failed Reframe's checks. Answer again for these units only, in the same JSON shape:

{problems}"""

CITE = re.compile(r"^(?P<path>[^:]+):(?P<start>\d+)(?:-(?P<end>\d+))?$")


def missing_evidence(evidence: list[str], legacy: Path) -> list[str]:
    """The cited lines that do not exist in the snapshot."""
    root, bad = legacy.resolve(), []
    for cite in evidence:
        m = CITE.match(str(cite).strip())
        target = (legacy / m["path"]).resolve() if m else None
        if not m or not target.is_relative_to(root) or not target.is_file():
            bad.append(cite)
            continue
        count = len(target.read_text(errors="replace").splitlines())
        start, end = int(m["start"]), int(m["end"] or m["start"])
        if not 1 <= start <= end <= count:
            bad.append(cite)
    return bad


def problems(unit: dict[str, Any], answer: dict[str, Any] | None, legacy: Path) -> list[str]:
    """What is wrong with one unit's answer; empty when it can be kept."""
    if answer is None:
        return ["no answer for this unit"]
    found = []
    decision, kind = answer.get("decision"), unit["kind"]
    allowed = GROUP if kind == "group" else ONE_SIDED
    if decision not in allowed:
        found.append(f'decision "{decision}" is not one of {", ".join(allowed)} for a {kind} unit')
    if decision == "needs_sme":
        if not str(answer.get("question") or "").strip():
            found.append('a "needs_sme" decision needs a question')
        return found
    evidence = answer.get("evidence") or []
    if not evidence:
        found.append("no evidence")
    bad = missing_evidence(evidence, legacy)
    if bad:
        found.append(f"evidence that does not exist in the snapshot: {', '.join(map(str, bad))}")
    keys = {r["key"] for r in unit["rules"]}
    covered = {k for r in answer.get("rules") or [] for k in r.get("covers") or []}
    unknown = covered - keys
    if unknown:
        found.append(f"covers keys that are not in this unit: {', '.join(sorted(unknown))}")
    if decision not in UNCOVERED:
        if not answer.get("rules"):
            found.append("no rules")
        missing = keys - covered
        if missing:
            found.append(f"these input rules are not covered by any rule: {', '.join(sorted(missing))}")
    return found


class Decisions:
    """reconcile/decisions.json: each unit's kept decision, with its input hash and round. Written under a lock, since
    batches run in threads."""

    def __init__(self, folder: RunFolder) -> None:
        self.folder, self.lock = folder, threading.Lock()
        self.saved: dict[str, Any] = folder.load("reconcile/decisions.json", {}) or {}

    def current(self, unit: dict[str, Any]) -> bool:
        return (self.saved.get(unit["key"]) or {}).get("hash") == unit["hash"]

    def keep(self, unit: dict[str, Any], decision: dict[str, Any], round_: int, attempts: int, failed: list[str]) -> None:
        with self.lock:
            self.saved[unit["key"]] = {"hash": unit["hash"], "round": round_, "at": iso(), "attempts": attempts, "check_failed": failed,
                                       "kind": unit["kind"], "program": unit["program"], **decision}
            self.folder.save("reconcile/decisions.json", self.saved)


def fallback(unit: dict[str, Any], failed: list[str]) -> dict[str, Any]:
    names = "; ".join(f"{r['tool']} {r.get('name') or r['key']}" for r in unit["rules"])[:400]
    return {"decision": "needs_sme", "rules": [], "changed": False, "evidence": [], "confidence": "low", "defect": "", "context": [],
            "reason": "Reframe could not check the agent's decision twice: " + "; ".join(failed)[:400],
            "question": f"Which behaviour does the system have for: {names}?"}


class Batch:
    def __init__(self, folder: RunFolder, claude, places: dict[str, Path], round_: int, number: int, members: list[dict[str, Any]],
                 context: dict[str, Any], decisions: Decisions) -> None:
        self.folder, self.claude, self.places, self.round, self.number = folder, claude, places, round_, number
        self.members, self.context, self.decisions = members, context, decisions
        self.name = f"reconcile-r{round_}-b{number}"
        self.steps: list[dict[str, Any]] = []

    def _prompt(self, path: Path) -> str:
        project = self.folder.state["project"]
        documents = [d["read_as"] for d in self.context.get("documents") or []]
        answers = self.answers()
        context = ""
        if documents or answers:
            context = ("\n\nThe person gave context; use it where it bears on a unit, and say so in \"context\": "
                       + (f"documents {', '.join(f'analysis/{project}/{d}' for d in documents)}" if documents else "")
                       + ("; " if documents and answers else "")
                       + (f"answered SME questions in analysis/{project}/reframe/reconcile/{self.name}-answers.json" if answers else "") + ".")
        return PROMPT.format(input=f"analysis/{project}/{path.relative_to(self.places['analysis']).as_posix()}",
                             legacy=f"legacy/{project}", context=context)

    def answers(self) -> list[dict[str, Any]]:
        """The answered questions this batch's units were given (units.answers_for), each once."""
        found: list[dict[str, Any]] = []
        for u in self.members:
            found += [a for a in u.get("answers") or [] if a not in found]
        return found

    def run(self, stop_now: threading.Event) -> Any:
        """Decide the batch; returns a StepResult that failed for a reason the whole run must stop for, or None."""
        folder_in = self.places["analysis"] / "reframe" / "reconcile"
        folder_in.mkdir(parents=True, exist_ok=True)
        if self.answers():
            (folder_in / f"{self.name}-answers.json").write_text(json.dumps(self.answers(), indent=1))
        pending = {u["key"]: u for u in self.members}
        failed: dict[str, list[str]] = {}
        for attempt in (1, 2):
            if not pending or stop_now.is_set():
                break
            path = folder_in / f"{self.name}{'-retry' if attempt == 2 else ''}.json"
            path.write_text(json.dumps({"programs": sorted({u["program"] for u in pending.values()}),
                                        "units": [{k: u[k] for k in ("key", "kind", "program", "rules", "pairs", "marks")} for u in pending.values()]},
                                       indent=1))
            prompt = self._prompt(path)
            if attempt == 2:
                prompt += "\n\n" + RETRY.format(problems="\n".join(f"- {k}: {'; '.join(v)}" for k, v in failed.items()))
            step = self.claude.run(f"{self.name}{'-retry' if attempt == 2 else ''}", prompt, timeout=3600, schema=SCHEMA)
            self.steps.append({"attempt": attempt, **{k: v for k, v in step.as_json().items() if k in ("ok", "seconds", "tokens", "cost_usd", "problem")}})
            if not step.ok:
                if step.problem in ("limit", "signin"):
                    return step
                failed = {k: [f"the step did not finish ({step.problem})"] for k in pending}
                continue
            answers: dict[str, dict[str, Any]] = {}
            for a in (self.claude.structured(step) or {}).get("decisions") or []:
                if isinstance(a, dict) and a.get("unit") in pending and a["unit"] not in answers:
                    answers[a["unit"]] = a
            failed = {}
            for key, unit in list(pending.items()):
                wrong = problems(unit, answers.get(key), self.places["legacy"])
                if wrong:
                    failed[key] = wrong
                    continue
                a = answers[key]
                self.decisions.keep(unit, {k: a.get(k) for k in ("decision", "rules", "changed", "evidence", "reason", "confidence",
                                                                  "question", "defect", "context")}, self.round, attempt, [])
                del pending[key]
        if stop_now.is_set():
            return None
        for key, unit in pending.items():  # failed twice: an SME decides
            self.decisions.keep(unit, fallback(unit, failed.get(key, ["no answer"])), self.round, 2, failed.get(key, []))
        return None


def decide(folder: RunFolder, claude, found: list[dict[str, Any]], context: dict[str, Any], round_: int,
           progress: Callable[[int, int], None] = lambda done, total: None) -> dict[str, Any]:
    """R4 for every unit whose inputs changed since its kept decision. Stops, after the batches already running, on
    Claude's usage limit or a sign-in problem: reframe resume continues with what is left."""
    from reframe.claude.steps import stop_for
    from reframe.claude.workspace import paths
    places = paths(folder)
    decisions = Decisions(folder)
    pending = [u for u in found if not decisions.current(u)]
    by_key = {u["key"]: u for u in pending}
    batched = unitlib.batches(pending)
    stop_now, stopped, done = threading.Event(), [], [0]
    log = folder.load("reconcile/steps.json", []) or []
    log_lock = threading.Lock()

    def one(b: dict[str, Any]) -> None:
        if stop_now.is_set():
            return
        batch = Batch(folder, claude, places, round_, b["number"], [by_key[k] for k in b["units"]], context, decisions)
        result = batch.run(stop_now)
        with log_lock:
            log.append({"round": round_, "batch": b["number"], "programs": b["programs"], "units": len(b["units"]), "steps": batch.steps})
            folder.save("reconcile/steps.json", log)
            done[0] += 1
            progress(done[0], len(batched))
        if result is not None:
            stopped.append(result)
            stop_now.set()

    with ThreadPoolExecutor(max_workers=unitlib.PARALLEL) as pool:
        list(pool.map(one, batched))
    if stopped:
        raise stop_for(stopped[0], "pipeline 3's decisions")
    kept = Decisions(folder).saved
    missing = [u["key"] for u in found if (kept.get(u["key"]) or {}).get("hash") != u["hash"]]
    if missing:
        raise Stop(Outcome.FAILED, f"{len(missing)} unit(s) have no decision after stage R4 (for example {missing[0]}); reframe resume tries again")
    return {"decided": len(pending), "kept_from_before": len(found) - len(pending), "batches": len(batched)}
