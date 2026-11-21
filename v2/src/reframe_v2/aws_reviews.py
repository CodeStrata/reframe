"""AWS review-task classifier (specification section 4, AWS review tasks; FR-03).

AWS Transform pauses a job for a person through forms with a response schema,
display-only forms, and questions in the job's chat. Each is sorted into one
class:

- ANSWER_FROM_INTAKE: answered once from the recorded intake, after checking it.
- DISPLAY_ONLY: recorded as seen; AWS submits it itself.
- APPROVE_ONLY: approved so the job continues, recorded as approved by
  Reframe and not reviewed by a person; its content is kept as NOT_CHECKED
  evidence for gate 1.
- PARK: anything else waits for a person, whose answer must fit the task's
  own schema.

The policy setting aws_reviews: ask, and audit mode by default, park every
approval. Only shapes recorded from live runs are recognized; nothing here
infers an operation, component or schema from a console label.

AWS's setup chat (P2-10, #263): a new job asks, in chat and one at a time, which
plan to run, whether the restated objective matches and which output languages,
then whether to proceed with the generated plan (live, 20 November 2026). Intake
records every answer; the plan menu is answered with one message carrying all of
them, so AWS has nothing left to ask before it builds the plan. A chat question is
recognized by its closing line, because AWS puts it at the end of a longer message.
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass, field
from typing import Any

from reframe_v2.model.hashing import content_hash

SOURCE_LOCATION_COMPONENT = "SpecifyAssetsLocation"
"""Recorded in v1's live runs (docs/validation/acceptance-defects.md)."""

SOURCE_LOCATION_OPTIONAL = frozenset({"enableFeatures", "isDownloadButtonClicked", "optInChatBox"})
"""Optional fields AWS's source-location form also declares, recorded live on 20 November 2026 (P1 stage D).
Reframe sends only assetLocation; a form with any other field parks."""

PROCEED_QUESTIONS = ("proceed with this plan?",)
"""Reframe's maintained list of chat questions that only ask to proceed. Matched against the message's closing line,
after normalizing case and spaces."""

PLAN_MENU_QUESTIONS = ("how would you like to proceed?",)
"""Closing line of AWS's opening plan menu (live, 20 November 2026)."""

OBJECTIVE_QUESTIONS = ("does this objective match your goals?",)
"""Closing line of AWS's objective confirmation, which restates the chosen plan (live, 20 November 2026)."""

OUTPUT_LANGUAGE_QUESTIONS = ("would you like your output translated into any of these languages, or would you prefer english only?",)
"""Closing line of AWS's output-language question (live, 20 November 2026)."""

MENU_OPTION = re.compile(r"^\s*(\d+)\.\s+([^:\n]+?)\s*(?::|$)", re.M)
"""A numbered option in AWS's chat, read as v1 did: its number and its label up to the colon."""

FUNCTION_SELECTION_QUESTIONS = ("please select the business function(s) to re-imagine before continuing.",
                                "please select the business function(s) to re-imagine")
"""Chat prompts recorded from live runs that ask for the business functions to carry forward."""


class Class(enum.Enum):
    ANSWER_FROM_INTAKE = "ANSWER_FROM_INTAKE"
    DISPLAY_ONLY = "DISPLAY_ONLY"
    APPROVE_ONLY = "APPROVE_ONLY"
    PARK = "PARK"


@dataclass(frozen=True)
class Intake:
    source_uri: str | None
    source_checksum_verified: bool
    scope_mode: str
    """'all' or 'list'."""
    scope_functions: tuple[str, ...] = ()
    aws_reviews: str = "by_class"
    audit_mode: bool = False
    plan: str = "Assess and reimagine"
    """The plan AWS's opening menu is answered with, by AWS's own label."""
    output_languages: tuple[str, ...] = ()
    """Languages besides English; English output is always produced."""
    collaborators: tuple[str, ...] = ()


@dataclass(frozen=True)
class Form:
    task_id: str
    title: str
    component: str | None
    schema: dict[str, Any]


@dataclass(frozen=True)
class ChatQuestion:
    message_id: str
    text: str
    options: tuple[str, ...] = ()
    """Numbered options, in AWS's order and wording, when the question is a menu."""


@dataclass(frozen=True)
class Decision:
    cls: Class
    reason: str
    response: dict[str, Any] | None = None
    """For forms: the content to send. For chat: {'selected': [...]} or {'proceed': True}. None when nothing is sent."""
    evidence_status: str | None = None
    audit: dict[str, Any] = field(default_factory=dict)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().casefold())


def closing_line(text: str) -> str:
    """The last non-empty line of a chat message, normalized: where AWS puts its question."""
    lines = [line for line in text.strip().splitlines() if line.strip()]
    return _normalize(lines[-1]) if lines else ""


def needs_answer(text: str) -> bool:
    """False for status notices: a message that asks to wait, or one with no question in it. AWS's function
    selection prompt asks without a question mark (v1, live 17 November 2026), so it is a question too."""
    if "please wait" in _normalize(text):
        return False
    return "?" in text or closing_line(text) in FUNCTION_SELECTION_QUESTIONS


def menu_options(text: str) -> tuple[tuple[str, str], ...]:
    """AWS's numbered options in the order and wording it used; empty unless there are at least two."""
    options = tuple((number, label.strip()) for number, label in MENU_OPTION.findall(text))
    return options if len(options) >= 2 else ()


def setup_message(choice: str, intake: Intake) -> str:
    """One reply that carries every setup answer, so AWS has nothing left to ask before it builds the plan.

    It names no workspace, job, connector or archive: AWS refuses identifiers in its chat (v1, live).
    """
    languages = (", ".join(intake.output_languages) + " as well as English") if intake.output_languages else "English only, no translations"
    collaborators = "No collaborators are needed." if not intake.collaborators else "Collaborators are added separately."
    parts = [f"{choice}.", f"Output: {languages}.", collaborators,
             "The Amazon Neptune cluster is already configured in this account, and this workspace already has an active reimagine connector to it.",
             "The source code archive is already uploaded; its location is given in the resource-location task."]
    parts.append("These are all my choices: please generate the job plan now."
                 if _approvals_parked(intake) else "These are all my choices: please generate the job plan now and proceed with it.")
    return " ".join(parts)


def _schema_hash(schema: dict[str, Any]) -> str:
    return content_hash(schema)


def _approvals_parked(intake: Intake) -> bool:
    return intake.aws_reviews == "ask" or intake.audit_mode


def _audit(task_id: str, schema_hash: str, response: Any, policy: str) -> dict[str, Any]:
    return {"task": task_id, "schema_hash": schema_hash, "response": response, "policy": policy}


def classify_form(form: Form, intake: Intake) -> Decision:
    schema = form.schema or {}
    schema_hash = _schema_hash(schema)
    if schema.get("displayOnly") is True:
        return Decision(Class.DISPLAY_ONLY, "display-only form; AWS submits it itself", audit=_audit(form.task_id, schema_hash, None, "display_only"))
    if form.component == SOURCE_LOCATION_COMPONENT:
        properties = schema.get("properties") or {}
        exact = (schema.get("required") == ["assetLocation"] and "assetLocation" in properties
                 and set(properties) - {"assetLocation"} <= SOURCE_LOCATION_OPTIONAL
                 and (properties["assetLocation"] or {}).get("type") == "string")
        if not exact:
            return Decision(Class.PARK, "source location form with an unexpected schema; a person checks it")
        if not intake.source_uri or not intake.source_checksum_verified:
            return Decision(Class.PARK, "the recorded source is missing or its checksum is not verified")
        response = {"assetLocation": intake.source_uri}
        return Decision(Class.ANSWER_FROM_INTAKE, "source location answered from the recorded, checksum-verified source",
                        response, audit=_audit(form.task_id, schema_hash, response, "answer_from_intake"))
    required = schema.get("required") or []
    if schema.get("type") == "object" and not required and schema.get("additionalProperties") is not True:
        if _approvals_parked(intake):
            return Decision(Class.PARK, "the project asks a person for every approval (aws_reviews: ask or audit mode)")
        return Decision(Class.APPROVE_ONLY, "approve-only review: approved by Reframe, not reviewed by a person", {},
                        evidence_status="NOT_CHECKED", audit=_audit(form.task_id, schema_hash, {}, "approve_only"))
    return Decision(Class.PARK, "a form Reframe cannot answer from intake; a person answers within its schema")


def classify_chat(question: ChatQuestion, intake: Intake) -> Decision:
    """Sort one chat question. A response carries "text": the exact reply to send, once."""
    text = _normalize(question.text)
    closing = closing_line(question.text)
    options = question.options or tuple(label for _, label in menu_options(question.text))
    schema_hash = content_hash({"text": text, "options": list(options)})
    if closing in PLAN_MENU_QUESTIONS:
        numbered = menu_options(question.text)
        chosen = [f"{number}. {label}" for number, label in numbered if _normalize(label) == _normalize(intake.plan)]
        if len(chosen) != 1:
            return Decision(Class.PARK, f"AWS's plan menu does not list the recorded plan {intake.plan!r} exactly once; a person decides")
        response = {"plan": chosen[0], "text": setup_message(chosen[0], intake)}
        return Decision(Class.ANSWER_FROM_INTAKE, "plan menu answered with the recorded plan and every setup answer", response,
                        audit=_audit(question.message_id, schema_hash, response, "answer_from_intake"))
    if closing in OBJECTIVE_QUESTIONS:
        restated = re.search(r"you selected option \d+, ([^.\n]+)\.", text)
        if not restated or restated.group(1).strip() != _normalize(intake.plan):
            return Decision(Class.PARK, "AWS restates an objective that is not the recorded plan; a person decides")
        response = {"confirm": True, "text": "Yes, this objective matches my goals."}
        return Decision(Class.ANSWER_FROM_INTAKE, "objective confirmation: AWS restates the recorded plan", response,
                        audit=_audit(question.message_id, schema_hash, response, "answer_from_intake"))
    if closing in OUTPUT_LANGUAGE_QUESTIONS:
        reply = ("English only, no translations." if not intake.output_languages
                 else "Please also produce output in: " + ", ".join(intake.output_languages) + ".")
        response = {"languages": list(intake.output_languages), "text": reply}
        return Decision(Class.ANSWER_FROM_INTAKE, "output language answered from intake", response,
                        audit=_audit(question.message_id, schema_hash, response, "answer_from_intake"))
    if closing in PROCEED_QUESTIONS:
        if _approvals_parked(intake):
            return Decision(Class.PARK, "the project asks a person for every approval (aws_reviews: ask or audit mode)")
        response = {"proceed": True, "text": "Yes, proceed with this plan."}
        return Decision(Class.APPROVE_ONLY, "proceed question: approved by Reframe, not reviewed by a person", response,
                        evidence_status="NOT_CHECKED", audit=_audit(question.message_id, schema_hash, response, "approve_only"))
    if text in FUNCTION_SELECTION_QUESTIONS:
        if not question.options:
            return Decision(Class.PARK, "function selection without a listed menu; a person answers")
        if intake.scope_mode == "all":
            selected = list(question.options)
        else:
            if not intake.scope_functions:
                return Decision(Class.PARK, "the scope names no functions; a person decides")
            missing = sorted(set(intake.scope_functions) - set(question.options))
            if missing:
                return Decision(Class.PARK, f"AWS's list does not exactly match the scope file: {', '.join(missing)} not listed; a person decides")
            selected = [option for option in question.options if option in intake.scope_functions]
        response = {"selected": selected, "text": ", ".join(selected)}
        return Decision(Class.ANSWER_FROM_INTAKE, "function selection answered from the recorded scope", response,
                        audit=_audit(question.message_id, schema_hash, response, "answer_from_intake"))
    return Decision(Class.PARK, "a chat question Reframe does not recognize; a person answers")


def fits_schema(schema: dict[str, Any], value: Any) -> bool:
    """A person's answer must fit the task's own schema: type, enum, required and allowed fields."""
    types = {"string": str, "boolean": bool, "array": list, "object": dict, "integer": int, "number": (int, float)}
    if not isinstance(schema, dict):
        return True
    if "enum" in schema and value not in schema["enum"]:
        return False
    kind = schema.get("type")
    if isinstance(kind, str) and kind in types:
        if kind in ("integer", "number") and isinstance(value, bool):
            return False
        if not isinstance(value, types[kind]):
            return False
    if isinstance(value, dict):
        properties = schema.get("properties") or {}
        if not set(schema.get("required") or []) <= set(value):
            return False
        if properties and schema.get("additionalProperties") is not True and not set(value) <= set(properties):
            return False
        return all(fits_schema(properties.get(key), item) for key, item in value.items())
    if isinstance(value, list):
        return all(fits_schema(schema.get("items"), item) for item in value)
    return True
