"""The exception table (specification section 4): park the work, keep going.

Each exception parks only the work that depends on it, says whether it waits
on a person or on something outside Reframe, and says how it may be cleared.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass


class Waiting(enum.Enum):
    HUMAN = "HUMAN"
    EXTERNAL = "EXTERNAL"


class Resume(enum.Enum):
    CHECK = "CHECK"
    """Cleared when a read-only check shows the cause is gone (credentials valid, permission granted, sign-in done)."""
    RESET_TIME = "RESET_TIME"
    """Cleared at a reset time the provider reported, otherwise by a bounded check schedule."""
    PERSON = "PERSON"
    """Cleared only by a named person's recorded action."""
    REBUILD = "REBUILD"
    """Cleared by rebuilding or regenerating from verified upstream records."""


class Parks(enum.Enum):
    AWS_CALLS = "every AWS call"
    PERMISSION_CALLS = "the calls that need the denied permission"
    MODEL_CALLS = "model calls"
    JOB = "that job and the functions waiting on it"
    STEP_AND_DEPENDENTS = "the affected step and its dependents"
    PAID_WORK = "all further paid work"
    ARTIFACT_AND_DEPENDENTS = "the artifact and everything that depends on it"
    RESOURCE_STEPS = "steps that need that resource"
    DELETION = "the deletion and the steps that need the recreated resource"


class Kind(enum.Enum):
    AWS_SIGN_IN_EXPIRED = "AWS_SIGN_IN_EXPIRED"
    AWS_PERMISSION_DENIED = "AWS_PERMISSION_DENIED"
    CLAUDE_CLI_SIGN_IN_EXPIRED = "CLAUDE_CLI_SIGN_IN_EXPIRED"
    CLAUDE_PLAN_LIMIT = "CLAUDE_PLAN_LIMIT"
    AWS_REVIEW_TASK = "AWS_REVIEW_TASK"
    UNKNOWN_AWS_TASK = "UNKNOWN_AWS_TASK"
    UNCERTAIN_DISPATCH = "UNCERTAIN_DISPATCH"
    BUDGET_REACHED = "BUDGET_REACHED"
    INTEGRITY_DERIVED = "INTEGRITY_DERIVED"
    INTEGRITY_CANONICAL = "INTEGRITY_CANONICAL"
    INTEGRITY_SOURCE = "INTEGRITY_SOURCE"
    CLIENT_RESOURCE_UNSUITABLE = "CLIENT_RESOURCE_UNSUITABLE"
    DESTRUCTIVE_CONFIRMATION = "DESTRUCTIVE_CONFIRMATION"


@dataclass(frozen=True)
class Rule:
    parks: Parks
    waiting: Waiting | None
    """Who the project waits on while this is unresolved. None when Reframe clears it itself by rebuilding."""
    resume: Resume
    note: str


RULES: dict[Kind, Rule] = {
    Kind.AWS_SIGN_IN_EXPIRED: Rule(Parks.AWS_CALLS, Waiting.EXTERNAL, Resume.CHECK,
                                   "The engineer signs in; the worker detects valid credentials and resumes. Local work on fetched evidence continues."),
    Kind.AWS_PERMISSION_DENIED: Rule(Parks.PERMISSION_CALLS, Waiting.EXTERNAL, Resume.CHECK,
                                     "An administrator changes access; retried only after a read-only permission check passes, never a sign-in loop."),
    Kind.CLAUDE_CLI_SIGN_IN_EXPIRED: Rule(Parks.MODEL_CALLS, Waiting.EXTERNAL, Resume.CHECK,
                                          "The engineer signs in to Claude Code; AWS work continues."),
    Kind.CLAUDE_PLAN_LIMIT: Rule(Parks.MODEL_CALLS, Waiting.EXTERNAL, Resume.RESET_TIME,
                                 "Resumes after the reported reset time; without one, a bounded check schedule, never an open-ended retry loop."),
    Kind.AWS_REVIEW_TASK: Rule(Parks.JOB, Waiting.HUMAN, Resume.PERSON,
                               "A review task Reframe may not answer by its class waits for a person; Reframe never invents an answer."),
    Kind.UNKNOWN_AWS_TASK: Rule(Parks.JOB, Waiting.HUMAN, Resume.PERSON,
                                "Nothing is submitted until Reframe is updated for the task or a person answers it."),
    Kind.UNCERTAIN_DISPATCH: Rule(Parks.STEP_AND_DEPENDENTS, Waiting.HUMAN, Resume.PERSON,
                                  "Settled automatically only from authoritative service state, a durable receipt or an idempotency key; otherwise reframe resolve."),
    Kind.BUDGET_REACHED: Rule(Parks.PAID_WORK, Waiting.HUMAN, Resume.PERSON,
                              "A person raises the allowance with reframe budget, recorded with who and why; never raised automatically."),
    Kind.INTEGRITY_DERIVED: Rule(Parks.ARTIFACT_AND_DEPENDENTS, None, Resume.REBUILD,
                                 "A derived view is rebuilt from verified canonical records; the damaged copy is kept."),
    Kind.INTEGRITY_CANONICAL: Rule(Parks.ARTIFACT_AND_DEPENDENTS, None, Resume.REBUILD,
                                   "Regenerated as a new version from verified upstream evidence; approvals of the old version lapse."),
    Kind.INTEGRITY_SOURCE: Rule(Parks.ARTIFACT_AND_DEPENDENTS, Waiting.HUMAN, Resume.PERSON,
                                "A damaged source snapshot, AWS original or receipt needs a verified restore or an independently checked refetch."),
    Kind.CLIENT_RESOURCE_UNSUITABLE: Rule(Parks.RESOURCE_STEPS, Waiting.EXTERNAL, Resume.CHECK,
                                          "The client fixes the resource or the resources file; checked before any job using it starts."),
    Kind.DESTRUCTIVE_CONFIRMATION: Rule(Parks.DELETION, Waiting.HUMAN, Resume.PERSON,
                                        "A person confirms the listed manifest-owned items and cost; nothing is deleted meanwhile."),
}

PAID_KINDS = frozenset({Kind.BUDGET_REACHED})
