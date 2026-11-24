"""Pipeline 3, stage by stage (docs/pipeline-3.md, section 4). Its status lives under "reconcile" in run.json, beside the
other two pipelines', and every stage can be run again: what is done is kept.

R0 preflight · R1 inputs · R2 identical pairs agreed · R3 estimate (behind the batch limit) · R4 decisions against the source ·
R5 the SME list · R6 the recommended requirements · R7 the reconciliation page
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import RunFolder, iso

DEFAULT_MAX_BATCHES = 120


def state(folder: RunFolder) -> dict[str, Any]:
    return dict(folder.state.get("reconcile") or {})


def update(folder: RunFolder, **values: Any) -> dict[str, Any]:
    return folder.merge("reconcile", **values)


def stage(folder: RunFolder, name: str) -> None:
    update(folder, stage=name, status="RUNNING", message=None, updated_at=iso())
    folder.event("reconcile_stage", stage=name)


def record_stop(folder: RunFolder, stop: Stop) -> None:
    update(folder, status=stop.outcome.value, message=stop.message, updated_at=iso())
    folder.event("reconcile_stopped", outcome=stop.outcome.value, message=stop.message[:500])


def request(folder: RunFolder, *, context: str | None = None, auth: str | None = None, max_batches: int | None = None) -> dict[str, Any]:
    """Record what pipeline 3 should do on this run; the worker reads it. A new request starts a new round of decisions."""
    current = state(folder)
    return update(folder, requested_at=iso(), context=context if context is not None else current.get("context"),
                  auth=auth or current.get("auth") or (folder.state.get("claude") or {}).get("auth") or "subscription",
                  max_batches=_limit(max_batches if max_batches is not None else current.get("max_batches")),
                  round=_next_round(current),
                  status="REQUESTED", message=None)


def _limit(value: Any) -> int:
    """The batch limit as given, 0 included; the default only when none was given."""
    return DEFAULT_MAX_BATCHES if value is None else int(value)


def _next_round(current: dict[str, Any]) -> int:
    """A new round after a finished one; the same round when a stopped or requested one is asked for again."""
    previous = int(current.get("round") or 0)
    return previous + 1 if previous == 0 or current.get("status") == Outcome.DONE.value else previous


def claude_code(folder: RunFolder, auth: str):
    from reframe.claude import plugin
    from reframe.claude.runner import ClaudeCode, environment
    from reframe.claude.workspace import paths
    places = paths(folder)
    aws_credentials = None
    if auth == "bedrock":
        from reframe.core.pipeline import Context
        aws_credentials = Context.load(folder).aws.credentials_environment
    env = environment(auth, aws_credentials=aws_credentials, region=folder.state.get("region"))
    return ClaudeCode(places["root"], places["policy"], plugin.plugin_dir(), places["logs"], env)


def page(folder: RunFolder) -> None:
    """R7: the reconciliation page, and the other three pages built again so that they link to it."""
    from reframe.report import build, compare, reconciled
    reconciled.build_reconciled(folder)
    build.build(folder)
    build.build_claude(folder)
    compare.build(folder)
    update(folder, page=reconciled.PAGE)


def work(folder: RunFolder, claude=None, claude_check=None) -> Outcome:
    from reframe.reconcile import decide, inputs, questions, requirements, units
    settings = state(folder)
    auth = settings.get("auth") or "subscription"
    context = Path(settings["context"]).expanduser() if settings.get("context") else None
    round_ = int(settings.get("round") or 1)
    update(folder, started_at=settings.get("started_at") or iso(), round=round_)

    stage(folder, "preflight")
    inputs.preflight(folder, context, auth, claude_check)

    stage(folder, "inputs")
    gathered = inputs.gather(folder, context)
    update(folder, inputs={"rules": len(gathered["rules"]), "pairs": len(gathered["pairs"]), "questions": len(gathered["questions"]),
                           "documents": len(gathered["context"]["documents"]), "marks": len(gathered["context"]["marks"]),
                           "answers": len(gathered["context"]["answers"]), "ignored": gathered["context"]["ignored"]})

    stage(folder, "agreed")
    agreed = units.agreed(gathered)
    folder.save("reconcile/agreed.json", agreed)

    stage(folder, "estimate")
    found = units.units(gathered)
    pending = [u for u in found if not decide.Decisions(folder).current(u)]
    batched = units.batches(pending)
    size = units.estimate(pending, batched, agreed)
    limit = _limit(state(folder).get("max_batches"))
    update(folder, estimate=size)
    if size["batches"] > limit:
        raise Stop(Outcome.WAITING_HUMAN, f"stage R4 needs {size['batches']} batches, above the limit of {limit}: about {size['minutes_low']} to "
                                          f"{size['minutes_high']} minutes four at a time, and ${size['usd_low']} to ${size['usd_high']} at API "
                                          f"prices on your Claude account. To go ahead: reframe reconcile --max-batches {size['batches']}")
    folder.decide("reconcile-estimate", f"run {size['batches']} batches", f"within the batch limit ({limit})", step="pipeline 3 decisions")

    stage(folder, "decide")
    claude = claude or claude_code(folder, auth)
    result = decide.decide(folder, claude, found, gathered["context"], round_,
                           progress=lambda done, total: update(folder, progress={"batches_done": done, "batches": total}))
    kept = decide.Decisions(folder).saved
    counts: dict[str, int] = {"agreed": len(agreed)}
    for u in found:
        d = kept[u["key"]]["decision"]
        counts[d] = counts.get(d, 0) + 1
    defects = sum(1 for u in found if str(kept[u["key"]].get("defect") or "").strip())
    update(folder, decisions=counts, defects=defects, last=result)

    stage(folder, "questions")
    listed = questions.build(folder, claude, gathered, found, kept)
    update(folder, questions=listed["counts"], originals=listed["originals"])

    stage(folder, "requirements")
    written = requirements.build(folder, claude, gathered, found, kept, agreed, listed)
    update(folder, requirements={k: written[k] for k in ("requirements", "dropped", "rules_cited", "rules_total")})

    stage(folder, "page")
    page(folder)

    c = listed["counts"]
    update(folder, stage="done", status=Outcome.DONE.value, finished_at=iso(),
           message=f"Round {round_}: {result['decided']} units decided against the source, {result['kept_from_before']} kept from before; "
                   f"{len(agreed)} rules agreed by both tools. SME list: {c['questions']} questions from {listed['originals']} originals "
                   f"({c.get('answered', 0)} answered, {c.get('settled', 0)} settled by your context), and {c['defects']} possible defects. "
                   f"{written['requirements']} recommended requirements citing {written['rules_cited']} of {written['rules_total']} recommended rules"
                   + (f" ({written['dropped']} dropped for citing no rule)." if written["dropped"] else "."))
    folder.event("reconcile_done", round=round_, **result)
    return Outcome.DONE
