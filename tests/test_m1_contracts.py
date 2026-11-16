"""M1 contracts: typed stops, version manifests, approval supersession, and the operation ledger (L1)."""
import argparse
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import test_reframe_checkpoints as checkpoint_fixtures
import reframe as app
import reframe_operations as ops
import reframe_states as states
import reframe_versions as versions
from pilot import Blocked


class StopCauseTests(unittest.TestCase):
    def test_messages_map_to_causes_and_recovery_classes(self):
        cases = {
            'Wireframe call 3 was dispatched and has no provider receipt. The counter stays.': ('UNCERTAIN_DISPATCH', 'reconciliation'),
            'Review site changed; approval invalid': ('INTEGRITY_FAILURE', 'integrity'),
            'Model call would exceed the dollar cap': ('DOLLAR_CAP', 'authorization'),
            'Run claude auth login, then resume': ('PROVIDER_UNAVAILABLE', 'provider'),
            'Record SME decisions first: Q1': ('HUMAN_DECISION_REQUIRED', 'human_decision'),
            'Validation blocked: in-scope finding has no source file and line: R1': ('EVIDENCE_MISSING', 'evidence_repair'),
            'Open context conflicts block specification approval': ('CONTEXT_CONFLICT', 'human_decision'),
            'Choose functional-parity or reimagine': ('PRECONDITION', 'input'),
        }
        for message, expected in cases.items():
            with self.subTest(message=message):
                detail = states.describe(Blocked(message))
                self.assertEqual((detail['cause'], detail['recovery']), expected)

    def test_explicit_cause_wins_and_unknown_causes_are_rejected(self):
        with self.assertRaises(Blocked) as raised:
            states.stop('Generation cannot be invoked', 'REQUIREMENTS_GENERATION_UNAVAILABLE')
        self.assertEqual(states.describe(raised.exception), {'cause': 'REQUIREMENTS_GENERATION_UNAVAILABLE', 'recovery': 'capability'})
        with self.assertRaises(ValueError):
            states.stop('x', 'MADE_UP')

    def test_only_automatic_recovery_continues_without_a_person(self):
        self.assertTrue(states.may_continue_automatically({'recovery': 'automatic'}))
        for recovery in ('authorization', 'human_decision', 'integrity', 'reconciliation', 'capability'):
            self.assertFalse(states.may_continue_automatically({'recovery': recovery}))


class WorkspaceContracts(unittest.TestCase):
    args = checkpoint_fixtures.CheckpointTests.args
    assess = checkpoint_fixtures.CheckpointTests.assess
    approve = checkpoint_fixtures.CheckpointTests.approve
    baseline = checkpoint_fixtures.CheckpointTests.baseline
    spec = checkpoint_fixtures.CheckpointTests.spec
    checkpoint = checkpoint_fixtures.CheckpointTests.checkpoint
    runtime = checkpoint_fixtures.CheckpointTests.runtime

    def setUp(self):
        checkpoint_fixtures.CheckpointTests.setUp(self)

    def cli(self, *values):
        out = io.StringIO()
        with redirect_stdout(out):
            code = app.main(['--workspace', str(self.work), *values])
        return code, json.loads(out.getvalue())

    def test_a_refused_command_reports_a_cause_and_leaves_project_state_unchanged(self):
        before = (self.work / 'project.json').read_bytes()
        code, result = self.cli('approve', 'validation', '--by', 'Ari', '--note', 'Reviewed')
        self.assertEqual(code, 2)
        self.assertEqual(result['status'], 'BLOCKED')
        self.assertIn(result['recovery'], states.CAUSES.values())
        self.assertEqual((self.work / 'project.json').read_bytes(), before)
        saved = states.last_stop(self.work)
        self.assertEqual(saved['command'], 'approve')
        code, status = self.cli('status')
        self.assertEqual(status['last_stop']['cause'], saved['cause'])
        self.assertNotIn('reason', status['last_stop'])
        self.assertEqual(status['summary']['phase'], self.project['stage'])
        self.assertEqual(status['summary']['package'], 'NOT_BUILT')

    def test_cancellation_is_an_event_and_the_phase_stays(self):
        stage = app.read(self.work / 'project.json')['stage']
        with patch.object(app, 'pipeline', side_effect=KeyboardInterrupt):
            code, result = self.cli('validate')
        self.assertEqual(code, 130)
        self.assertEqual(result['status'], 'CANCELLED')
        saved = app.read(self.work / 'project.json')
        self.assertEqual(saved['stage'], stage)
        self.assertEqual(saved['last_cancellation']['command'], 'validate')
        self.assertEqual(saved['last_cancellation']['phase'], stage)

    def test_versions_are_content_addressed_and_written_once(self):
        first = versions.record(self.work, self.project, 'baseline')
        again = versions.record(self.work, self.project, 'baseline again')
        self.assertEqual(first, again)
        saved = versions.load(self.work, first)
        self.assertEqual(saved['references']['requirements'], {'type': 'requirements', 'state': 'NOT_REQUESTED'})
        self.assertEqual(saved['references']['package'], {'type': 'package', 'state': 'NOT_BUILT'})
        self.project['decisions'] = {'Q1': {'disposition': 'deferred'}}
        changed = versions.record(self.work, self.project, 'decision')
        self.assertNotEqual(first, changed)
        self.assertEqual([item['id'] for item in self.project['versions']], [first, changed])
        tampered = self.work / versions.VERSION_DIR / (first + '.json')
        record = json.loads(tampered.read_text())
        record['references']['decisions']['count'] = 99
        tampered.write_text(json.dumps(record))
        self.project['decisions'] = {}
        with self.assertRaises(Blocked):
            versions.record(self.work, self.project, 'rewrite attempt')

    def test_a_changed_artifact_is_an_integrity_failure_without_overwrite(self):
        result = app.pipeline(self.work, self.project, self.args('validate'), self.runtime)
        self.assertEqual(result['status'], 'AWAITING_VALIDATION_APPROVAL')
        versions.record(self.work, self.project, 'validated')
        path = self.work / self.project['specification']['path']
        path.write_text(path.read_text().replace('"', '"', 1) + ' ')
        before = path.read_bytes()
        with self.assertRaises(Blocked) as raised:
            versions.verify(self.work, self.project)
        self.assertEqual(states.describe(raised.exception)['cause'], 'INTEGRITY_FAILURE')
        self.assertIn('specification', str(raised.exception))
        self.assertEqual(path.read_bytes(), before)

    def test_supersede_moves_approvals_into_history(self):
        self.project['approvals']['validation'] = {'by': 'Ari', 'note': 'ok', 'sha256': 'x'}
        moved = versions.supersede(self.project, ('validation', 'specifications'), 'feedback')
        self.assertEqual(moved, ['validation'])
        self.assertNotIn('validation', self.project['approvals'])
        history = versions.superseded(self.project, 'validation')
        self.assertEqual(history[-1]['status'], 'superseded')
        self.assertEqual(history[-1]['approval']['by'], 'Ari')

    def test_approval_is_bound_to_the_active_version(self):
        approval = self.project['approvals']['assessment']
        self.assertIn('version_id', approval)
        self.assertEqual(approval['version_id'], self.project['active_version'])
        self.assertTrue((self.work / versions.VERSION_DIR / (approval['version_id'] + '.json')).is_file())

    def test_an_interrupted_dispatch_is_uncertain_and_is_not_redispatched(self):
        calls = {'n': 0}

        def interrupted(provider, run, directory, role, message):
            calls['n'] += 1
            if calls['n'] == 2:
                raise KeyboardInterrupt
            return self.runtime(provider, run, directory, role, message)

        with self.assertRaises(KeyboardInterrupt):
            app.pipeline(self.work, self.project, self.args('validate'), interrupted)
        app.persist(self.work, self.project)
        counted = self.project['pipeline']['calls']
        self.assertEqual(counted, 2)
        self.assertEqual(self.project['operations']['preparation:2']['state'], 'dispatched')
        with self.assertRaises(Blocked) as raised:
            app.pipeline(self.work, self.project, self.args('resume'), self.runtime)
        self.assertEqual(states.describe(raised.exception)['cause'], 'UNCERTAIN_DISPATCH')
        self.assertEqual(calls['n'], 2)
        self.assertEqual(self.project['pipeline']['calls'], counted)
        self.assertEqual(self.project['operations']['preparation:2']['state'], 'uncertain')
        with self.assertRaises(Blocked):
            ops.reconcile(self.project, 'preparation:2', 'failed', 'Ari', '')
        ops.reconcile(self.project, 'preparation:2', 'failed', 'Ari', 'Provider console shows no completed request')
        result = app.pipeline(self.work, self.project, self.args('resume'), self.runtime)
        self.assertEqual(result['status'], 'AWAITING_VALIDATION_APPROVAL')
        self.assertGreater(self.project['pipeline']['calls'], counted)
        self.assertEqual(self.project['operations']['preparation:2']['state'], 'reconciled_failed')
        tally = ops.counts(self.project, 'preparation')
        self.assertEqual(tally['uncertain'], 0)
        self.assertEqual(tally['failed'], 1)

    def test_a_saved_receipt_recovers_a_dispatched_call_and_completed_calls_never_replay(self):
        ops.begin(self.project, 'preparation:7', 'preparation', 'm', call=7)
        (self.work / 'preparation').mkdir(exist_ok=True)
        (self.work / 'preparation' / 'reply-7.json').write_text('{}')
        self.assertEqual(ops.recover(self.project, 'preparation', lambda r: app.preparation_receipt(self.work, r).is_file()), [])
        self.assertEqual(self.project['operations']['preparation:7']['state'], 'received')
        with self.assertRaises(Blocked):
            ops.begin(self.project, 'preparation:7', 'preparation', 'm', call=7)

    def test_a_pre_start_runtime_failure_is_not_dispatched_but_stays_counted(self):
        import kiro_workflow as kw

        def missing(provider, run, directory, role, message):
            raise kw.not_started('Install and authenticate claude, then resume')

        with self.assertRaises(kw.RuntimeUnavailable):
            app.pipeline(self.work, self.project, self.args('validate'), missing)
        record = self.project['operations']['preparation:1']
        self.assertEqual(record['state'], 'not_dispatched')
        self.assertEqual(self.project['pipeline']['calls'], 1)
        self.assertTrue(any(e.get('event') == 'operation_not_dispatched' for e in self.project['events']))


if __name__ == '__main__':
    unittest.main()
