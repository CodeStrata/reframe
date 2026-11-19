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
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass, field
from typing import Any

from reframe_v2.model.hashing import content_hash

SOURCE_LOCATION_COMPONENT = "SpecifyAssetsLocation"
"""Recorded in v1's live runs (docs/validation/acceptance-defects.md)."""

PROCEED_QUESTIONS = ("proceed with this plan?",)
"""Reframe's maintained list of chat questions that only ask to proceed. Matched exactly after normalizing case and spaces."""

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
        exact = (schema.get("required") == ["assetLocation"] and set(properties) == {"assetLocation"}
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
    text = _normalize(question.text)
    schema_hash = content_hash({"text": text, "options": list(question.options)})
    if text in PROCEED_QUESTIONS:
        if _approvals_parked(intake):
            return Decision(Class.PARK, "the project asks a person for every approval (aws_reviews: ask or audit mode)")
        response = {"proceed": True}
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
        response = {"selected": selected}
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
