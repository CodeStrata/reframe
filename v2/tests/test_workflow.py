"""P0-04 (#219): run states, scheduled gates and the exception table (section 4, NFR-13). L1.

Section 14 scenarios covered here at contract level: all three gates left
unanswered (no approval appears anywhere); the only job parked, with status
showing a waiting state.
"""

import unittest
from datetime import datetime, timedelta, timezone

from reframe_v2.model.records import Ref
from reframe_v2.workflow import (
    GATES,
    RULES,
    Clearance,
    ConcurrentGateChange,
    GateError,
    GateState,
    Kind,
    LateInputOutcome,
    Project,
    ProjectState,
    StepState,
    Waiting,
    WorkflowError,
    answer,
    evaluate_deadline,
    extend,
    open_gate,
)

T0 = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)
SNAPSHOT = Ref("design:billing", 1, "sha256:" + "a" * 64)
INPUT = Ref("context:1", 1, "sha256:" + "b" * 64)


class GateTests(unittest.TestCase):
    def gate(self, days=7):
        return open_gate("gate1", SNAPSHOT, T0, ["sme"], deadline_days=days)

    def test_default_deadline_is_seven_days_elapsed_utc(self):
        self.assertEqual(self.gate().deadline, T0 + timedelta(days=7))

    def test_naive_times_are_refused(self):
        with self.assertRaises(GateError):
            open_gate("gate1", SNAPSHOT, datetime(2026, 11, 18, 12, 0), ["sme"])

    def test_other_time_zones_are_converted_to_utc(self):
        ist = timezone(timedelta(hours=5, minutes=30))
        gate = open_gate("gate1", SNAPSHOT, T0.astimezone(ist), ["sme"])
        self.assertEqual(gate.opened_at, T0)
        self.assertEqual(gate.opened_at.tzinfo, timezone.utc)

    def test_an_answer_before_the_deadline_closes_it_as_answered(self):
        gate, outcome = answer(self.gate(), INPUT, T0 + timedelta(days=1), expected_version=1)
        self.assertEqual(outcome, LateInputOutcome.RECORDED)
        self.assertEqual(gate.state, GateState.ANSWERED)
        self.assertEqual(gate.answers, (INPUT,))

    def test_no_answer_times_out_once(self):
        gate = evaluate_deadline(self.gate(), T0 + timedelta(days=7))
        self.assertEqual(gate.state, GateState.TIMED_OUT_NO_RESPONSE)
        again = evaluate_deadline(gate, T0 + timedelta(days=30))
        self.assertIs(again, gate)
        self.assertEqual(sum("TIMED_OUT" in event for event in gate.events), 1)

    def test_before_the_deadline_nothing_changes(self):
        gate = self.gate()
        self.assertIs(evaluate_deadline(gate, T0 + timedelta(days=6, hours=23)), gate)

    def test_an_answer_after_the_deadline_goes_to_the_next_revision(self):
        gate, outcome = answer(self.gate(), INPUT, T0 + timedelta(days=8), expected_version=1)
        self.assertEqual(outcome, LateInputOutcome.NEXT_REVISION)
        self.assertEqual(gate.state, GateState.TIMED_OUT_NO_RESPONSE)
        self.assertEqual(gate.answers, ())

    def test_input_after_an_answer_goes_to_the_next_revision(self):
        gate, _ = answer(self.gate(), INPUT, T0 + timedelta(days=1), expected_version=1)
        later, outcome = answer(gate, Ref("context:2", 1, INPUT.content_hash), T0 + timedelta(days=2), expected_version=gate.version)
        self.assertEqual(outcome, LateInputOutcome.NEXT_REVISION)
        self.assertEqual(later.answers, (INPUT,))

    def test_no_gate_state_is_an_approval(self):
        open_ = self.gate()
        answered, _ = answer(open_, INPUT, T0 + timedelta(days=1), expected_version=1)
        timed_out = evaluate_deadline(open_, T0 + timedelta(days=8))
        self.assertFalse(any(gate.is_approval for gate in (open_, answered, timed_out)))

    def test_all_three_gates_unanswered_time_out_with_no_approval(self):
        gates = [evaluate_deadline(open_gate(name, SNAPSHOT, T0, ["sme"]), T0 + timedelta(days=7)) for name in GATES]
        self.assertEqual({gate.state for gate in gates}, {GateState.TIMED_OUT_NO_RESPONSE})
        self.assertFalse(any(gate.is_approval for gate in gates))

    def test_extend_moves_an_open_deadline_later(self):
        gate = extend(self.gate(), T0 + timedelta(days=10), T0 + timedelta(days=3), expected_version=1)
        self.assertEqual(gate.deadline, T0 + timedelta(days=10))
        self.assertEqual(evaluate_deadline(gate, T0 + timedelta(days=8)).state, GateState.OPEN)

    def test_extend_cannot_shorten_or_reopen(self):
        with self.assertRaises(GateError):
            extend(self.gate(), T0 + timedelta(days=5), T0, expected_version=1)
        with self.assertRaises(GateError):
            extend(self.gate(), T0 + timedelta(days=20), T0 + timedelta(days=8), expected_version=1)

    def test_close_and_extend_are_atomic(self):
        gate = self.gate()
        answered, _ = answer(gate, INPUT, T0 + timedelta(days=1), expected_version=1)
        with self.assertRaises(ConcurrentGateChange):
            extend(answered, T0 + timedelta(days=10), T0 + timedelta(days=1), expected_version=1)
        with self.assertRaises(ConcurrentGateChange):
            answer(answered, INPUT, T0 + timedelta(days=1), expected_version=1)

    def test_unknown_gate_is_refused(self):
        with self.assertRaises(GateError):
            open_gate("gate4", SNAPSHOT, T0, [])


class ExceptionTableTests(unittest.TestCase):
    def test_every_exception_has_a_rule(self):
        self.assertEqual(set(RULES), set(Kind))

    def test_waiting_categories_follow_section_4(self):
        human = {Kind.AWS_REVIEW_TASK, Kind.UNKNOWN_AWS_TASK, Kind.UNCERTAIN_DISPATCH, Kind.BUDGET_REACHED,
                 Kind.INTEGRITY_SOURCE, Kind.DESTRUCTIVE_CONFIRMATION}
        external = {Kind.AWS_SIGN_IN_EXPIRED, Kind.AWS_PERMISSION_DENIED, Kind.CLAUDE_CLI_SIGN_IN_EXPIRED,
                    Kind.CLAUDE_PLAN_LIMIT, Kind.CLIENT_RESOURCE_UNSUITABLE}
        self.assertEqual({k for k, r in RULES.items() if r.waiting is Waiting.HUMAN}, human)
        self.assertEqual({k for k, r in RULES.items() if r.waiting is Waiting.EXTERNAL}, external)
        self.assertEqual({k for k, r in RULES.items() if r.waiting is None}, {Kind.INTEGRITY_DERIVED, Kind.INTEGRITY_CANONICAL})


def pipeline():
    """Two functions, each: AWS extract, then a model step; plus a local render step."""
    project = Project()
    project.add_step("extract:A", tags={"aws", "aws_job:job-A", "paid"})
    project.add_step("extract:B", tags={"aws", "aws_job:job-B", "paid"})
    project.add_step("model:A", needs=["extract:A"], tags={"model", "paid", "artifact:rules-A"})
    project.add_step("model:B", needs=["extract:B"], tags={"model", "paid", "artifact:rules-B"})
    project.add_step("render", needs=["model:A"], tags={"artifact:site"})
    return project


def run_all(project):
    progressed = True
    while progressed:
        progressed = False
        for step in project.runnable():
            project.start(step)
            project.finish(step)
            progressed = True


class ParkingTests(unittest.TestCase):
    def test_a_fresh_project_is_running(self):
        project = pipeline()
        self.assertEqual(project.runnable(), ["extract:A", "extract:B"])
        self.assertEqual(project.state(), ProjectState.RUNNING)

    def test_finished_work_is_complete(self):
        project = pipeline()
        run_all(project)
        self.assertEqual(project.state(), ProjectState.COMPLETE)

    def test_aws_sign_in_parks_aws_calls_only(self):
        project = pipeline()
        project.start("extract:A")
        project.finish("extract:A")
        project.raise_exception("x1", Kind.AWS_SIGN_IN_EXPIRED, "aws", "session expired")
        self.assertEqual(project.steps["extract:B"].state, StepState.PARKED)
        self.assertEqual(project.runnable(), ["model:A"])
        run_all(project)
        self.assertEqual(project.state(), ProjectState.WAITING_EXTERNAL)
        with self.assertRaises(WorkflowError):
            project.clear("x1", Clearance(person="someone"))
        project.clear("x1", Clearance(check_passed=True))
        run_all(project)
        self.assertEqual(project.state(), ProjectState.COMPLETE)

    def test_a_running_step_that_is_parked_is_not_shown_as_running(self):
        project = pipeline()
        project.start("extract:A")
        project.raise_exception("x1", Kind.AWS_SIGN_IN_EXPIRED, "aws", "expired mid-call")
        self.assertEqual(project.steps["extract:A"].state, StepState.PARKED)
        self.assertNotIn(StepState.RUNNING, {step.state for step in project.steps.values()})

    def test_the_only_job_parked_shows_a_waiting_state_with_status(self):
        project = Project()
        project.add_step("extract:A", tags={"aws", "aws_job:job-A"})
        project.raise_exception("task-1", Kind.AWS_REVIEW_TASK, "aws_job:job-A", "free-text question")
        self.assertEqual(project.state(), ProjectState.WAITING_HUMAN)
        [item] = project.status()
        self.assertEqual((item.exception, item.waiting_on, item.steps), ("task-1", "HUMAN", ("extract:A",)))

    def test_a_review_task_parks_only_its_job(self):
        project = pipeline()
        project.raise_exception("task-1", Kind.AWS_REVIEW_TASK, "aws_job:job-A", "free-text question")
        self.assertEqual(project.runnable(), ["extract:B"])

    def test_plan_limit_parks_model_calls_and_aws_work_continues(self):
        project = pipeline()
        project.raise_exception("limit", Kind.CLAUDE_PLAN_LIMIT, "model", "usage limit")
        run_all(project)
        self.assertEqual(project.steps["extract:A"].state, StepState.DONE)
        self.assertEqual(project.steps["model:A"].state, StepState.PARKED)
        self.assertEqual(project.state(), ProjectState.WAITING_EXTERNAL)
        with self.assertRaises(WorkflowError):
            project.clear("limit", Clearance(person="someone"))
        project.clear("limit", Clearance(reset_reached=True))
        run_all(project)
        self.assertEqual(project.state(), ProjectState.COMPLETE)

    def test_budget_is_never_cleared_by_a_check_and_records_who_and_why(self):
        project = pipeline()
        project.raise_exception("budget", Kind.BUDGET_REACHED, "paid", "call allowance reached")
        self.assertEqual(project.runnable(), [])
        self.assertEqual(project.state(), ProjectState.WAITING_HUMAN)
        with self.assertRaises(WorkflowError):
            project.clear("budget", Clearance(check_passed=True))
        with self.assertRaises(WorkflowError):
            project.clear("budget", Clearance(person="Owner"))
        project.clear("budget", Clearance(person="Owner", reason="Second domain added"))
        self.assertEqual(project.runnable(), ["extract:A", "extract:B"])

    def test_unpaid_work_continues_when_the_budget_is_reached(self):
        project = pipeline()
        project.add_step("report", tags={"artifact:report"})
        project.raise_exception("budget", Kind.BUDGET_REACHED, "paid", "allowance reached")
        self.assertEqual(project.runnable(), ["report"])

    def test_uncertain_dispatch_parks_the_step_and_its_dependents(self):
        project = pipeline()
        project.start("extract:A")
        project.raise_exception("u1", Kind.UNCERTAIN_DISPATCH, "step:extract:A", "process killed after dispatch")
        run_all(project)
        states = {name: step.state for name, step in project.steps.items()}
        self.assertEqual(states["extract:A"], StepState.PARKED)
        self.assertEqual(states["model:A"], StepState.PENDING)
        self.assertEqual(states["render"], StepState.PENDING)
        self.assertEqual(states["model:B"], StepState.DONE)
        self.assertEqual(project.state(), ProjectState.WAITING_HUMAN)
        with self.assertRaises(WorkflowError):
            project.clear("u1", Clearance(check_passed=True))
        project.clear("u1", Clearance(person="Owner"))
        self.assertEqual(project.runnable(), ["extract:A"])

    def test_a_derived_integrity_failure_is_rebuilt_without_waiting_for_anyone(self):
        project = pipeline()
        run_all(project)
        project.raise_exception("i1", Kind.INTEGRITY_DERIVED, "artifact:site", "HTML hash mismatch")
        self.assertEqual(project.state(), ProjectState.RUNNING)
        self.assertEqual(project.runnable(), ["rebuild:i1"])
        with self.assertRaises(WorkflowError):
            project.clear("i1", Clearance(person="Owner"))
        run_all(project)
        self.assertEqual(project.active, {})

    def test_damaged_source_evidence_waits_for_a_person(self):
        project = pipeline()
        project.raise_exception("i2", Kind.INTEGRITY_SOURCE, "artifact:rules-A", "snapshot hash mismatch")
        run_all(project)
        self.assertEqual(project.state(), ProjectState.WAITING_HUMAN)

    def test_human_waiting_is_reported_before_external(self):
        project = pipeline()
        project.raise_exception("x1", Kind.AWS_SIGN_IN_EXPIRED, "aws", "expired")
        project.raise_exception("d1", Kind.DESTRUCTIVE_CONFIRMATION, "deletion:stack", "clean start")
        self.assertEqual(project.state(), ProjectState.WAITING_HUMAN)
        self.assertEqual([item.waiting_on for item in project.status()], ["HUMAN", "EXTERNAL"])

    def test_scope_must_match_what_the_exception_parks(self):
        project = pipeline()
        with self.assertRaises(WorkflowError):
            project.raise_exception("x1", Kind.AWS_SIGN_IN_EXPIRED, "model", "wrong scope")
        with self.assertRaises(WorkflowError):
            project.raise_exception("x2", Kind.AWS_PERMISSION_DENIED, "aws_permission:", "no name")

    def test_a_step_added_while_an_exception_is_active_starts_parked(self):
        project = pipeline()
        project.raise_exception("x1", Kind.CLAUDE_CLI_SIGN_IN_EXPIRED, "model", "expired")
        step = project.add_step("model:C", tags={"model"})
        self.assertEqual(step.state, StepState.PARKED)

    def test_a_parked_step_cannot_be_started(self):
        project = pipeline()
        project.raise_exception("x1", Kind.AWS_SIGN_IN_EXPIRED, "aws", "expired")
        with self.assertRaises(WorkflowError):
            project.start("extract:A")

    def test_open_gates_do_not_hold_any_step(self):
        project = pipeline()
        gate = open_gate("gate1", SNAPSHOT, T0, ["sme"])
        run_all(project)
        self.assertTrue(gate.is_open)
        self.assertEqual(project.state(), ProjectState.COMPLETE)


if __name__ == "__main__":
    unittest.main()
