"""Pipeline 3, stage R2b: the rules both tools describe the same way, described without being decided
(docs/pipeline-3.md, section 8.4).

Identical pairs are agreed without an agent deciding them (stage R2, the owner's decision). They still need what every
other recommended rule has, so a headless step reads each agreed rule's cited lines and says whether the code runs, how
it is reached and what it depends on outside the source. It does not change the wording or the decision. Answers are
checked like stage R4's, asked once more if they fail, and kept by rule with a hash of the rule, so a later round
describes only rules that changed.

Written to reconcile/described.json.
"""

from __future__ import annotations

import hashlib
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from reframe.core.runfolder import RunFolder, iso
from reframe.reconcile import units as unitlib
from reframe.reconcile.decide import REACHABLE, missing_evidence

FILE = "reconcile/described.json"

SCHEMA = {"type": "object", "required": ["rules"], "properties": {"rules": {"type": "array", "items": {
    "type": "object", "required": ["rule", "reachable", "entry", "depends"],
    "properties": {
        "rule": {"type": "string"},
        "reachable": {"type": "string", "enum": list(REACHABLE)},
        "entry": {"type": "array", "items": {"type": "string"}},
        "depends": {"type": "string"}}}}}}

PROMPT = """Read {input}. It holds business rules about a legacy system that two tools ("AWS Transform" and "Claude's plugin") described the same way. The source is read-only under {legacy}/. Each rule gives the source lines it was found in. Do not change or judge the rules' wording: describe each rule.

- Check that the code the rule describes can run: a paragraph must be reached from the program's entry, and a program from a menu entry, a transaction, an XCTL, LINK or CALL, or a job step that runs (not in a job whose job card has TYPRUN=SCAN, and not commented out). Say so in "reachable": "yes" with the lines that show how it is reached in "entry", "no" if it can never run, or "unknown" if the source cannot show it.
- In "depends", say what the behaviour depends on outside the source (data, configuration, a program not in the source), or leave it empty.

Give "entry" lines as "<path>:<start>-<end>" or "<path>:<line>", with paths relative to {legacy}/ exactly as the files are named. Answer for every rule, using its key exactly. Answer only with the JSON."""

RETRY = """Your answer for some rules failed Reframe's checks. Answer again for these rules only, in the same JSON shape:

{problems}"""

FIELDS = ("reachable", "entry", "depends")


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()[:16]


def items(agreed: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Each agreed rule as an item to describe, with the hash of what the step is given."""
    found = []
    for r in agreed:
        content = {"text": r["text"], "name": r.get("name", ""), "program": r["program"], "cites": r["evidence"], "method": unitlib.METHOD}
        found.append({"key": r["key"], "program": r["program"], "rules": [r], **content, "hash": _hash(content)})
    return found


def problems(answer: dict[str, Any] | None, legacy: Path) -> list[str]:
    if answer is None:
        return ["no answer for this rule"]
    found = []
    reachable = answer.get("reachable")
    if reachable not in REACHABLE:
        found.append(f'reachable must be one of {", ".join(REACHABLE)}')
    if reachable == "yes":
        entry = answer.get("entry") or []
        if not entry:
            found.append('reachable "yes" needs the lines that show how the code is reached, in "entry"')
        bad = missing_evidence(entry, legacy)
        if bad:
            found.append(f"entry lines that do not exist in the snapshot: {', '.join(map(str, bad))}")
    return found


def fallback(failed: list[str]) -> dict[str, Any]:
    return {"reachable": "unknown", "entry": [], "depends": "", "check_failed": failed}


def describe(folder: RunFolder, claude, agreed: list[dict[str, Any]]) -> dict[str, Any]:
    """R2b for every agreed rule whose text or citations changed since it was described. Stops, after the batches already
    running, on Claude's usage limit or a sign-in problem: reframe resume continues with what is left."""
    from reframe.claude.steps import stop_for
    from reframe.claude.workspace import paths
    places = paths(folder)
    project = folder.state["project"]
    saved: dict[str, Any] = folder.load(FILE, {}) or {}
    found = items(agreed)
    pending = [i for i in found if (saved.get(i["key"]) or {}).get("hash") != i["hash"]]
    by_key = {i["key"]: i for i in pending}
    batched = unitlib.batches(pending)
    lock, stop_now, stopped = threading.Lock(), threading.Event(), []
    log = folder.load("reconcile/describe-steps.json", []) or []
    folder_in = places["analysis"] / "reframe" / "reconcile"
    folder_in.mkdir(parents=True, exist_ok=True)

    def keep(item: dict[str, Any], value: dict[str, Any], attempts: int) -> None:
        with lock:
            saved[item["key"]] = {"hash": item["hash"], "at": iso(), "attempts": attempts, **value}
            folder.save(FILE, saved)

    def one(b: dict[str, Any]) -> None:
        if stop_now.is_set():
            return
        name = f"describe-b{b['number']}"
        todo = {k: by_key[k] for k in b["units"]}
        failed: dict[str, list[str]] = {}
        for attempt in (1, 2):
            if not todo or stop_now.is_set():
                break
            path = folder_in / f"{name}{'-retry' if attempt == 2 else ''}.json"
            path.write_text(json.dumps({"rules": [{"key": i["key"], "program": i["program"], "name": i["name"], "text": i["text"], "cites": i["cites"]}
                                                  for i in todo.values()]}, indent=1))
            prompt = PROMPT.format(input=f"analysis/{project}/{path.relative_to(places['analysis']).as_posix()}", legacy=f"legacy/{project}")
            if attempt == 2:
                prompt += "\n\n" + RETRY.format(problems="\n".join(f"- {k}: {'; '.join(v)}" for k, v in failed.items()))
            step = claude.run(f"{name}{'-retry' if attempt == 2 else ''}", prompt, timeout=3600, schema=SCHEMA)
            with lock:
                log.append({"batch": b["number"], "attempt": attempt, **{k: v for k, v in step.as_json().items()
                                                                          if k in ("ok", "seconds", "tokens", "cost_usd", "problem")}})
                folder.save("reconcile/describe-steps.json", log)
            if not step.ok:
                if step.problem in ("limit", "signin"):
                    stopped.append(step)
                    stop_now.set()
                    return
                failed = {k: [f"the step did not finish ({step.problem})"] for k in todo}
                continue
            answers = {a["rule"]: a for a in (claude.structured(step) or {}).get("rules") or [] if isinstance(a, dict) and a.get("rule") in todo}
            failed = {}
            for key, item in list(todo.items()):
                wrong = problems(answers.get(key), places["legacy"])
                if wrong:
                    failed[key] = wrong
                    continue
                keep(item, {k: answers[key].get(k) for k in FIELDS}, attempt)
                del todo[key]
        if stop_now.is_set():
            return
        for key, item in todo.items():  # failed twice: described as unknown, with the reason
            keep(item, fallback(failed.get(key, ["no answer"])), 2)

    with ThreadPoolExecutor(max_workers=unitlib.PARALLEL) as pool:
        list(pool.map(one, batched))
    if stopped:
        raise stop_for(stopped[0], "the description of the rules both tools agree on")
    return {"described": len(pending), "kept_from_before": len(found) - len(pending), "batches": len(batched)}
