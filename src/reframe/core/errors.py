"""How a call or a run can end, shared by every stage (specification sections 4 and 7)."""

from __future__ import annotations

import enum


class Outcome(enum.Enum):
    DONE = "DONE"
    WAITING_HUMAN = "WAITING_HUMAN"
    """A question waits for an answer (reframe answer), or the owner must decide something."""
    WAITING_SIGNIN = "WAITING_SIGNIN"
    """The AWS sign-in expired or a read failed; sign in and run reframe resume."""
    REFUSED = "REFUSED"
    """AWS or a Reframe check refused; the reason is kept."""
    UNCERTAIN = "UNCERTAIN"
    """A change may or may not have reached AWS; it is settled from AWS's state before anything else."""
    FAILED = "FAILED"
    """AWS reported a failed step, or a stage could not finish."""


EXIT_CODES = {Outcome.DONE: 0, Outcome.WAITING_HUMAN: 3, Outcome.WAITING_SIGNIN: 4, Outcome.REFUSED: 5,
              Outcome.UNCERTAIN: 6, Outcome.FAILED: 7}


class ReframeError(Exception):
    pass


class NotSent(ReframeError):
    """Refused or failed before anything reached AWS: certainly not dispatched."""


class Rejected(ReframeError):
    """AWS answered the call with a failure. Nothing changed; the reason is AWS's own."""

    def __init__(self, operation: str, reason: str) -> None:
        super().__init__(f"{operation}: AWS refused: {reason}")
        self.operation, self.reason = operation, reason


class Uncertain(ReframeError):
    """The call was sent and its outcome is unknown."""


class Stop(ReframeError):
    """Ends the current stage with an outcome; the run records it and a resume continues from here."""

    def __init__(self, outcome: Outcome, message: str) -> None:
        super().__init__(message)
        self.outcome, self.message = outcome, message
