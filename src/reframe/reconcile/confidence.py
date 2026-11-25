"""Pipeline 3, part 2: confidence that means something (docs/pipeline-3.md, section 8.5).

Reframe sets each recommended rule's confidence from facts it has checked, not from the model's word: who decided the
rule against the code, whether the code runs (with the lines that show how it is reached, which Reframe checked exist),
and whether anything outside the source decides it. The model's own rating is kept beside it as model_confidence.

In the accuracy audit (P3-11) every rule an agent decided with both tools' rules in front of it was correct, and every
error was a rule agreed without an agent or kept from one tool; the two wrong rules described code that never runs.
"""

from __future__ import annotations

from typing import Any

BOTH_TOOLS = ("merged", "aws", "claude", "rewritten")
LEVELS = ("high", "medium", "low")


def rate(decision: str, reachable: str | None, entry: list[str] | None, depends: str | None) -> tuple[str, str]:
    """(confidence, why) for a recommended rule. `decision` is "agreed" for a rule both tools describe the same way."""
    depends = str(depends or "").strip()
    if decision == "agreed" and reachable == "no":
        return "low", "Both tools describe it the same way, but the code it describes never runs."
    if decision == "needs_sme":
        return "low", "The code could not settle it: it waits for a subject-matter expert."
    reasons = []
    if decision == "agreed":
        reasons.append("both tools describe it the same way, but no agent decided it against the code")
    elif decision == "kept":
        reasons.append("only one tool found it")
    elif decision not in BOTH_TOOLS:
        reasons.append(f"it was decided as {decision}")
    if reachable != "yes" or not entry:
        reasons.append("the source does not show that the code runs" if reachable == "unknown" else "how the code is reached is not shown")
    if depends:
        reasons.append(f"it depends on something outside the source ({depends})")
    if reasons:
        return "medium", (reasons[0][0].upper() + reasons[0][1:] + ("; " + "; ".join(reasons[1:]) if reasons[1:] else "") + ".")
    return "high", "Decided against the code with both tools' rules in front of it, and the code is reached from the lines shown."


def facts(rule: dict[str, Any], record: dict[str, Any]) -> dict[str, Any]:
    """The fields a recommended rule carries for its confidence, from its unit's decision or its description."""
    confidence, why = rate(rule["decision"], record.get("reachable"), record.get("entry"), record.get("depends"))
    return {"confidence": confidence, "confidence_why": why, "model_confidence": rule.get("model_confidence", record.get("confidence", "")),
            "reachable": record.get("reachable") or "", "entry": list(record.get("entry") or []), "depends": record.get("depends") or ""}
