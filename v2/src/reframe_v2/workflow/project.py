"""Project state: RUNNING while any runnable work remains, otherwise a waiting state (specification section 4).

Steps carry tags that say what they use (AWS calls, model calls, paid work, a
job, a resource, an artifact). An exception parks the steps whose tags match
its scope, and their dependents wait behind them; everything else keeps
running. A parked step is never shown as running. When no runnable work is
left the project is WAITING_HUMAN or WAITING_EXTERNAL and status lists each
parked item and what it waits on.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field

from reframe_v2.workflow.exceptions import RULES, Kind, Parks, Resume, Waiting


class StepState(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    PARKED = "PARKED"
    DONE = "DONE"


class ProjectState(enum.Enum):
    RUNNING = "RUNNING"
    WAITING_HUMAN = "WAITING_HUMAN"
    WAITING_EXTERNAL = "WAITING_EXTERNAL"
    COMPLETE = "COMPLETE"
    """Every step is done and nothing is parked. Gates may still be open beside it."""


class WorkflowError(Exception):
    """A step or exception change was refused."""


# Which tag prefix an exception's scope must use, by what the table says it parks.
SCOPE_PREFIX = {
    Parks.AWS_CALLS: "aws",
    Parks.PERMISSION_CALLS: "aws_permission:",
    Parks.MODEL_CALLS: "model",
    Parks.JOB: "aws_job:",
    Parks.STEP_AND_DEPENDENTS: "step:",
    Parks.PAID_WORK: "paid",
    Parks.ARTIFACT_AND_DEPENDENTS: "artifact:",
    Parks.RESOURCE_STEPS: "resource:",
    Parks.DELETION: "deletion:",
}


@dataclass
class Step:
    id: str
    needs: tuple[str, ...] = ()
    tags: frozenset[str] = frozenset()
    state: StepState = StepState.PENDING


@dataclass(frozen=True)
class Clearance:
    """Evidence that an exception's cause is gone. Which field counts depends on the exception's resume rule."""

    check_passed: bool = False
    reset_reached: bool = False
    person: str | None = None
    reason: str | None = None


@dataclass
class ActiveException:
    id: str
    kind: Kind
    scope: str
    detail: str
    rebuild_step: str | None = None


@dataclass
class StatusItem:
    exception: str
    kind: str
    waiting_on: str
    parks: str
    steps: tuple[str, ...]
    how_to_resume: str


@dataclass
class Project:
    steps: dict[str, Step] = field(default_factory=dict)
    active: dict[str, ActiveException] = field(default_factory=dict)
    history: list[str] = field(default_factory=list)

    # Steps -------------------------------------------------------------------

    def add_step(self, step_id: str, needs: tuple[str, ...] | list[str] = (), tags: frozenset[str] | set[str] = frozenset()) -> Step:
        if step_id in self.steps:
            raise WorkflowError(f"step {step_id} already exists")
        missing = [need for need in needs if need not in self.steps]
        if missing:
            raise WorkflowError(f"step {step_id} needs unknown steps {missing}")
        tags = frozenset(tags) | {f"step:{step_id}"}
        step = Step(step_id, tuple(needs), tags)
        self.steps[step_id] = step
        if self._parking(step):
            step.state = StepState.PARKED
        return step

    def runnable(self) -> list[str]:
        return sorted(step.id for step in self.steps.values() if self._is_runnable(step))

    def start(self, step_id: str) -> None:
        step = self.steps[step_id]
        if not self._is_runnable(step):
            raise WorkflowError(f"step {step_id} is not runnable: {self._why_not(step)}")
        step.state = StepState.RUNNING
        self.history.append(f"start {step_id}")

    def finish(self, step_id: str) -> None:
        step = self.steps[step_id]
        if step.state is not StepState.RUNNING:
            raise WorkflowError(f"step {step_id} is {step.state.value}, not RUNNING")
        step.state = StepState.DONE
        self.history.append(f"done {step_id}")
        for exception in list(self.active.values()):
            if exception.rebuild_step == step_id:
                self._close(exception, "rebuilt from verified records")

    # Exceptions --------------------------------------------------------------

    def raise_exception(self, exception_id: str, kind: Kind, scope: str, detail: str) -> ActiveException:
        if exception_id in self.active:
            raise WorkflowError(f"exception {exception_id} is already active")
        rule = RULES[kind]
        prefix = SCOPE_PREFIX[rule.parks]
        if not (scope == prefix if not prefix.endswith(":") else scope.startswith(prefix) and len(scope) > len(prefix)):
            raise WorkflowError(f"{kind.value} parks {rule.parks.value}; its scope must be {prefix!r}{'<name>' if prefix.endswith(':') else ''}, not {scope!r}")
        exception = ActiveException(exception_id, kind, scope, detail)
        self.active[exception_id] = exception
        if rule.resume is Resume.REBUILD:
            exception.rebuild_step = f"rebuild:{exception_id}"
            self.steps[exception.rebuild_step] = Step(exception.rebuild_step, (), frozenset({f"step:{exception.rebuild_step}", "model", "paid"}))
        for step in self.steps.values():
            if step.state in (StepState.PENDING, StepState.RUNNING) and scope in step.tags:
                step.state = StepState.PARKED
        self.history.append(f"park {exception_id} {kind.value} {scope}")
        return exception

    def clear(self, exception_id: str, clearance: Clearance) -> None:
        exception = self.active.get(exception_id)
        if exception is None:
            raise WorkflowError(f"no active exception {exception_id}")
        rule = RULES[exception.kind]
        if rule.resume is Resume.CHECK and not clearance.check_passed:
            raise WorkflowError(f"{exception.kind.value} clears only after a read-only check passes")
        if rule.resume is Resume.RESET_TIME and not (clearance.reset_reached or clearance.check_passed):
            raise WorkflowError(f"{exception.kind.value} clears at the reported reset time or after a bounded check passes")
        if rule.resume is Resume.PERSON:
            if not clearance.person:
                raise WorkflowError(f"{exception.kind.value} is cleared only by a named person")
            if exception.kind is Kind.BUDGET_REACHED and not clearance.reason:
                raise WorkflowError("raising an allowance records who and why")
        if rule.resume is Resume.REBUILD:
            raise WorkflowError(f"{exception.kind.value} clears when its rebuild step {exception.rebuild_step} is done")
        self._close(exception, clearance.person or "check passed")

    # State -------------------------------------------------------------------

    def state(self) -> ProjectState:
        if any(step.state is StepState.RUNNING for step in self.steps.values()) or self.runnable():
            return ProjectState.RUNNING
        if all(step.state is StepState.DONE for step in self.steps.values()) and not self.active:
            return ProjectState.COMPLETE
        waiting = {RULES[exception.kind].waiting for exception in self.active.values()}
        if Waiting.HUMAN in waiting:
            return ProjectState.WAITING_HUMAN
        if Waiting.EXTERNAL in waiting:
            return ProjectState.WAITING_EXTERNAL
        raise WorkflowError("no runnable work and nothing parked, but not every step is done; the step graph is inconsistent")

    def status(self) -> list[StatusItem]:
        items = []
        for exception in sorted(self.active.values(), key=lambda e: e.id):
            rule = RULES[exception.kind]
            steps = tuple(sorted(step.id for step in self.steps.values() if exception.scope in step.tags and step.state is StepState.PARKED))
            waiting = rule.waiting.value if rule.waiting else "REFRAME (rebuilding)"
            items.append(StatusItem(exception.id, exception.kind.value, waiting, rule.parks.value, steps, rule.note))
        return items

    # Internals ---------------------------------------------------------------

    def _parking(self, step: Step) -> list[ActiveException]:
        return [exception for exception in self.active.values() if exception.scope in step.tags]

    def _is_runnable(self, step: Step) -> bool:
        return step.state is StepState.PENDING and not self._parking(step) and all(
            self.steps[need].state is StepState.DONE for need in step.needs
        )

    def _why_not(self, step: Step) -> str:
        if step.state is not StepState.PENDING:
            return step.state.value
        parking = self._parking(step)
        if parking:
            return "parked by " + ", ".join(exception.id for exception in parking)
        return "waiting for " + ", ".join(need for need in step.needs if self.steps[need].state is not StepState.DONE)

    def _close(self, exception: ActiveException, by: str) -> None:
        del self.active[exception.id]
        for step in self.steps.values():
            if step.state is StepState.PARKED and not self._parking(step):
                step.state = StepState.PENDING
        self.history.append(f"clear {exception.id} by {by}")
