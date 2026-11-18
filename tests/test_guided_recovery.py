"""Continuation, bulk deferral, and status behavior. External providers stay mocked."""
import io
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import test_reframe as fixtures
import reframe as app
from pilot import Blocked, sha
from reframe_terminal import Terminal
from rich.console import Console


class BulkAndStatusTests(unittest.TestCase):
    def setUp(self):
        self.inner = fixtures.PreparationTests('test_missing_sme_decision_blocks_validation_approval')
        self.inner.setUp()
        self.addCleanup(self.inner.doCleanups)

    def install_questions(self, count=452, decided=54):
        inner = self.inner
        inner.validated()
        path = inner.work / inner.project['specification']['path']
        spec = app.read(path)
        spec['questions'] = [{'id': f'Q{index:04d}', 'question': 'fixture', 'impact': 'fixture',
                              'owner': 'SME', 'blocks': 'Implementation'} for index in range(count)]
        app.write(path, spec)
        inner.project['specification']['sha256'] = sha(path)
        for index in range(decided):
            inner.project['decisions'][f'Q{index:04d}'] = {
                'by': 'saved', 'answer': 'None', 'disposition': 'deferred',
                'specification_sha256': inner.project['specification']['sha256'], 'at': 1}
        app.persist(inner.work, inner.project)
        directory = Path(inner.project['assessments']['a']['directory'])
        run = app.read(directory / 'run.json')
        run['status'] = 'AWAITING_ASSESSMENT_APPROVAL'
        app.write(directory / 'run.json', run)
        return path

    def test_open_batch_preserves_saved_deferrals_and_writes_once(self):
        inner = self.inner
        self.install_questions()
        saved = {key: dict(value) for key, value in inner.project['decisions'].items()}
        reports = []
        generations = {'count': 0}
        original = app.preparation_report

        def once(work, project):
            generations['count'] += 1
            return original(work, project)

        with patch.object(app, 'preparation_report', side_effect=once):
            code = app.main(['--workspace', str(inner.work), 'decide', '--open', '--by', 'Owner',
                             '--answer', 'Deferred for review', '--disposition', 'deferred', '--confirm'],
                            reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(generations['count'], 1)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]['recorded'], 398)
        self.assertEqual(reports[0]['skipped'], 0)
        self.assertEqual(reports[0]['remaining'], 0)
        self.assertIn('not an answer', reports[0]['deferral'])
        self.assertNotIn('Deferred for review', json.dumps({key: value for key, value in reports[0].items() if key != 'deferral'}))
        current = app.read(inner.work / 'project.json')
        for key, value in saved.items():
            self.assertEqual(current['decisions'][key]['answer'], 'None')
            self.assertEqual(current['decisions'][key]['by'], value['by'])
        self.assertEqual(len(current['decision_batches']), 1)
        self.assertEqual(len(current['decision_batches'][0]['question_ids']), 398)
        with patch.object(app, 'preparation_report', side_effect=AssertionError('second report')):
            again = []
            code = app.main(['--workspace', str(inner.work), 'decide', '--open', '--by', 'Owner',
                             '--answer', 'Deferred for review', '--disposition', 'deferred', '--confirm'],
                            reporter=again.append)
        self.assertEqual(code, 0)
        self.assertEqual(again[0]['recorded'], 0)
        self.assertEqual(len(app.read(inner.work / 'project.json')['decision_batches']), 1)

    def test_unconfirmed_and_invalid_batches_do_not_write(self):
        inner = self.inner
        self.install_questions()
        before = app.read(inner.work / 'project.json')
        preview = []
        code = app.main(['--workspace', str(inner.work), 'decide', '--questions', 'Q0054,Q0055', '--by', 'Owner',
                         '--answer', 'Deferred for review', '--disposition', 'deferred'], reporter=preview.append)
        self.assertEqual(code, 0)
        self.assertEqual(preview[0]['status'], 'DECISION_CONFIRMATION')
        self.assertEqual(preview[0]['pending'], 2)
        self.assertEqual(app.read(inner.work / 'project.json')['decisions'], before['decisions'])
        with self.assertRaisesRegex(Blocked, 'Unknown SME question'):
            app.decision(inner.work, inner.project, inner.args(
                'decide', '--questions', 'Q0054,Q9999', '--by', 'Owner', '--answer', 'no',
                '--disposition', 'deferred', '--confirm'))
        self.assertEqual(inner.project['decisions'], before['decisions'])
        self.assertNotIn('decision_batches', inner.project)

    def test_interruption_before_persist_keeps_decisions_and_restart_is_safe(self):
        inner = self.inner
        self.install_questions(count=4, decided=1)
        before = json.loads((inner.work / 'project.json').read_text())

        def fail_persist(*_args):
            raise RuntimeError('interrupt before persist')

        with patch.object(app, 'persist', side_effect=fail_persist):
            with self.assertRaises(RuntimeError):
                app.main(['--workspace', str(inner.work), 'decide', '--open', '--by', 'Owner',
                          '--answer', 'Deferred for review', '--disposition', 'deferred', '--confirm'],
                         reporter=lambda _result: None)
        disk = json.loads((inner.work / 'project.json').read_text())
        self.assertEqual(disk['decisions'], before['decisions'])
        self.assertNotIn('decision_batches', disk)
        reports = []
        code = app.main(['--workspace', str(inner.work), 'decide', '--open', '--by', 'Owner',
                         '--answer', 'Deferred for review', '--disposition', 'deferred', '--confirm'],
                        reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(reports[0]['recorded'], 3)
        self.assertEqual(reports[0]['skipped'], 0)
        saved = app.read(inner.work / 'project.json')
        self.assertEqual(saved['decisions']['Q0000']['answer'], 'None')
        self.assertEqual(len(saved['decision_batches']), 1)

    def test_restart_repairs_the_report_without_a_second_batch(self):
        inner = self.inner
        self.install_questions(count=4, decided=1)
        before = json.loads((inner.work / 'project.json').read_text())['decisions']['Q0000']

        def fail_report(*_args):
            raise RuntimeError('interrupt during report')

        with patch.object(app, 'preparation_report', side_effect=fail_report):
            with self.assertRaises(RuntimeError):
                app.main(['--workspace', str(inner.work), 'decide', '--open', '--by', 'Owner',
                          '--answer', 'Deferred for review', '--disposition', 'deferred', '--confirm'],
                         reporter=lambda _result: None)
        interrupted = app.read(inner.work / 'project.json')
        self.assertEqual(len(interrupted['decisions']), 4)
        self.assertEqual(interrupted['decisions']['Q0000']['answer'], before['answer'])
        self.assertEqual(len(interrupted['decision_batches']), 1)
        self.assertFalse(app.preparation_report_current(inner.work, interrupted))
        generations = {'count': 0}
        original = app.preparation_report

        def once(work, project):
            generations['count'] += 1
            return original(work, project)

        reports = []
        with patch.object(app, 'preparation_report', side_effect=once):
            code = app.main(['--workspace', str(inner.work), 'decide', '--open', '--by', 'Owner',
                             '--answer', 'Deferred for review', '--disposition', 'deferred', '--confirm'],
                            reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(generations['count'], 1)
        self.assertEqual(reports[0]['recorded'], 0)
        self.assertTrue(reports[0]['repaired_report'])
        repaired = app.read(inner.work / 'project.json')
        self.assertEqual(len(repaired['decision_batches']), 1)
        self.assertEqual(repaired['decisions']['Q0000']['answer'], 'None')
        self.assertNotIn('decision_history', repaired)
        self.assertTrue(app.preparation_report_current(inner.work, repaired))

    def test_amendment_keeps_history_and_clears_validation_approval(self):
        inner = self.inner
        self.install_questions(count=2, decided=1)
        inner.project['approvals']['validation'] = {'sha256': 'stale', 'by': 'Owner', 'note': 'old', 'at': 1}
        app.persist(inner.work, inner.project)
        result = app.decision(inner.work, inner.project, inner.args(
            'decide', '--question', 'Q0000', '--by', 'Owner', '--answer', 'Reviewed replacement',
            '--disposition', 'resolved', '--amend', '--confirm'))
        self.assertEqual(result['recorded'], 1)
        self.assertEqual(inner.project['decisions']['Q0000']['answer'], 'Reviewed replacement')
        self.assertEqual(inner.project['decision_history'][0]['previous']['Q0000']['answer'], 'None')
        self.assertNotIn('validation', inner.project['approvals'])
        self.assertNotIn('site', inner.project)

    def test_status_separates_historical_service_state_from_validation(self):
        inner = self.inner
        self.install_questions()
        reports = []
        code = app.main(['--workspace', str(inner.work), 'status'], reporter=reports.append)
        self.assertEqual(code, 0)
        result = reports[0]
        self.assertEqual(result['phase'], 'AWAITING_VALIDATION_APPROVAL')
        self.assertEqual(result['service_state'], 'AWAITING_ASSESSMENT_APPROVAL')
        self.assertEqual(result['assessment_approval'], 'recorded')
        self.assertIn('not the current blocker', result['service_state_note'])
        self.assertIn('approve validation', result['required_action'])
        self.assertEqual(result['questions'], {'total': 452, 'answered': 0, 'deferred': 54, 'remaining': 398})
        self.assertNotIn('fixture', json.dumps(result['questions']))
        self.assertNotIn('None', json.dumps(result))

    def test_resume_stops_at_validation_approval(self):
        inner = self.inner
        self.install_questions(count=1, decided=1)
        reports = []
        with patch.object(app, 'assessment', side_effect=AssertionError('aws')), \
             patch.object(app, 'pipeline', side_effect=AssertionError('provider')):
            code = app.main(['--workspace', str(inner.work), 'resume'], reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(reports[-1]['status'], 'AWAITING_VALIDATION_APPROVAL')
        self.assertNotIn('validation', app.read(inner.work / 'project.json')['approvals'])

    def test_cancellation_and_artifacts_stay_separate_from_project_phase(self):
        inner = self.inner
        self.install_questions(count=1, decided=0)
        area = inner.work / 'preparation'
        (area / 'checkpoint-candidate-2.json').write_text('{"fixture":true}')
        (area / 'checkpoint-review-2.json').write_text('{"kind":"review"}')
        output = io.StringIO()
        ui = Terminal(console=Console(file=output, width=100, height=30, color_system=None))
        ui.private = False
        ui.report({'status': 'CANCELLED', 'reason': 'Cancelled by user. Saved work is retained.',
                   'last_action': 'Last action cancelled; saved progress retained'})
        self.assertIn('Last action cancelled; saved progress retained', output.getvalue())
        self.assertNotIn('CANCELLED', output.getvalue())
        with patch('reframe_setup.workspace', return_value=inner.work), patch.object(ui, 'project', return_value=inner.project):
            ui.dispatch('/privacy')
            ui.dispatch('/privacy')
            text = output.getvalue()
            self.assertIn('AWAITING VALIDATION APPROVAL', text)
            self.assertIn('Historical service record', text)
            self.assertIn('Last action cancelled; saved progress retained', text)
            self.assertNotIn('CANCELLED', text)
            ui.dispatch('/artifacts')
        listed = output.getvalue()
        self.assertIn('preparation/checkpoint-candidate-2.json', listed)
        self.assertIn('preparation/checkpoint-review-2.json', listed)
        self.assertIn('Tracked API spend', listed)
        self.assertIn('API dollar cap', listed)
        self.assertIn('unmeasured', listed)
        self.assertIn('zero-dollar', listed)
        self.assertIn('blocks the next billed API call', __import__('re').sub(r'[\s\u2502]+', ' ', listed))


class ReviewedSpecificationUpgradeTests(BulkAndStatusTests):
    def install_paused_review(self):
        inner = self.inner
        inner.validated()
        path = inner.work / inner.project['specification']['path']
        spec = app.read(path)
        spec['questions'] = [{'id': f'Q{index:04d}', 'question': 'fixture', 'impact': 'fixture',
                              'owner': 'SME', 'blocks': 'Implementation'} for index in range(58)]
        app.write(path, spec)
        inner.project['specification']['sha256'] = sha(path)
        for index in range(54):
            inner.project['decisions'][f'Q{index:04d}'] = {
                'by': 'saved', 'answer': 'None', 'disposition': 'deferred',
                'specification_sha256': inner.project['specification']['sha256'], 'at': 1}
        area = inner.work / 'preparation'
        label = inner.project['selected']
        plan = {'source_commit': inner.project['source']['commit'], 'scope': inner.project['scope'],
                'assessment': inner.project['assessments'][label]['sha256'], 'units': []}
        units = {}
        for number in range(1, 113):
            ident = f'U{number:04d}'
            plan['units'].append({'id': ident, 'focus': 'rule.cbl', 'segments': [{'id': 'segment', 'text': 'fixture'}]})
            candidate = {'kind': 'checkpoint', 'summary': 'passed', 'findings': [], 'questions': [], 'coverage': []}
            review = {'kind': 'review', 'decision': 'PASS', 'report': 'passed', 'findings': []}
            candidate_path = area / ('saved-' + ident + '-candidate.json')
            review_path = area / ('saved-' + ident + '-review.json')
            app.write(candidate_path, candidate)
            app.write(review_path, review)
            units[ident] = {'status': 'PASS', 'candidate_path': str(candidate_path.relative_to(inner.work)),
                            'candidate_sha256': sha(candidate_path),
                            'review_path': str(review_path.relative_to(inner.work)), 'review_sha256': sha(review_path)}
        plan_path = area / 'plan.json'
        app.write(plan_path, plan)
        inner.project['checkpoints'] = {'plan_path': 'preparation/plan.json', 'plan_sha256': sha(plan_path),
                                        'status': 'READY_FOR_SYNTHESIS', 'units': units}
        import reframe_checkpoints as checkpoints
        _plan, capsules = checkpoints.verified_capsules(inner.work, inner.project, app)
        inner.project['specification']['checkpoints_sha256'] = app.digest(capsules)
        inner.project['pipeline']['calls'] = 306
        inner.project['pipeline']['status'] = 'PASS'
        inner.project['stage'] = 'AWAITING_VALIDATION_APPROVAL'
        inner.project['framework_commit'] = 'b' * 40
        inner.project['pins']['framework_commit'] = 'b' * 40
        directory = Path(inner.project['assessments'][label]['directory'])
        run = app.read(directory / 'run.json')
        run['framework_commit'] = 'b' * 40
        run['status'] = 'AWAITING_ASSESSMENT_APPROVAL'
        app.write(directory / 'run.json', run)
        app.persist(inner.work, inner.project)
        return inner

    def test_changed_prompts_are_refused_without_rewriting_the_review(self):
        inner = self.install_paused_review()
        before = app.read(inner.work / 'project.json')
        reports = []
        with patch.object(app, 'preparation_protocol_hash', return_value='e' * 64):
            code = app.main(['--workspace', str(inner.work), 'upgrade-framework', '--note', 'Controller only',
                             '--adopt-prompts'], reporter=reports.append)
        self.assertEqual(code, 2)
        self.assertIn('stays bound to the saved preparation prompts', reports[-1]['reason'])
        self.assertIn('Do not pass --adopt-prompts', reports[-1]['hint'])
        self.assertEqual(app.read(inner.work / 'project.json'), before)

    def test_validation_sequence_records_the_controller_and_keeps_the_review(self):
        inner = self.install_paused_review()
        spec = dict(inner.project['specification'])
        approvals = json.loads(json.dumps(inner.project['approvals']))
        units = json.loads(json.dumps(inner.project['checkpoints']['units']))
        saved = {key: dict(value) for key, value in list(inner.project['decisions'].items())[:54]}
        refused = []
        code = app.main(['--workspace', str(inner.work), 'approve', 'validation', '--by', 'Owner', '--note', 'Reviewed'],
                        reporter=refused.append)
        self.assertEqual(code, 2)
        self.assertIn('Framework revision changed', refused[-1]['reason'])
        self.assertNotIn('validation', app.read(inner.work / 'project.json')['approvals'])
        reports = []
        code = app.main(['--workspace', str(inner.work), 'status'], reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertIn('upgrade-framework', reports[-1]['next_step'])
        self.assertIn('Do not resume', reports[-1]['next_step'])
        with patch.object(app, 'model_call', side_effect=AssertionError('provider')), \
             patch.object(app, 'assessment', side_effect=AssertionError('aws')):
            code = app.main(['--workspace', str(inner.work), 'upgrade-framework', '--note', 'Record the controller update'],
                            reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(reports[-1]['preserved'], 'reviewed_specification')
        self.assertIn('Do not resume', reports[-1]['next_step'])
        saved_project = app.read(inner.work / 'project.json')
        self.assertEqual(saved_project['framework_commit'], 'a' * 40)
        self.assertEqual(saved_project['pins']['framework_commit'], 'a' * 40)
        self.assertEqual(saved_project['pins']['prompt_hash'], inner.project['pins']['prompt_hash'])
        self.assertEqual(saved_project['specification'], spec)
        self.assertEqual(saved_project['approvals'], approvals)
        self.assertEqual(saved_project['pipeline']['calls'], 306)
        self.assertEqual(saved_project['checkpoints']['units'], units)
        self.assertEqual(sum(unit['status'] == 'PASS' for unit in units.values()), 112)
        for key, value in saved.items():
            self.assertEqual(saved_project['decisions'][key]['answer'], 'None')
            self.assertEqual(saved_project['decisions'][key], value)
        code = app.main(['--workspace', str(inner.work), 'status'], reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertIn('approve validation', reports[-1]['next_step'])
        self.assertNotIn('upgrade-framework', reports[-1]['next_step'])
        with patch.object(app, 'model_call', side_effect=AssertionError('provider')), \
             patch.object(app, 'assessment', side_effect=AssertionError('aws')), \
             patch.object(app, 'pipeline', side_effect=AssertionError('checkpoint restart')):
            code = app.main(['--workspace', str(inner.work), 'decide', '--open', '--by', 'Owner',
                             '--answer', 'Deferred for review', '--disposition', 'deferred', '--confirm'],
                            reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(reports[-1]['recorded'], 4)
        self.assertEqual(reports[-1]['skipped'], 0)
        decided = app.read(inner.work / 'project.json')
        self.assertEqual(len(decided['decision_batches']), 1)
        self.assertEqual(len(decided['decision_batches'][0]['question_ids']), 4)
        for key, value in saved.items():
            self.assertEqual(decided['decisions'][key]['answer'], 'None')
            self.assertEqual(decided['decisions'][key]['by'], value['by'])
        self.assertEqual(decided['specification'], spec)
        self.assertEqual(decided['pipeline']['calls'], 306)
        with patch.object(app, 'model_call', side_effect=AssertionError('provider')), \
             patch.object(app, 'assessment', side_effect=AssertionError('aws')):
            code = app.main(['--workspace', str(inner.work), 'approve', 'validation', '--by', 'Owner',
                             '--note', 'Questions without decisions were deferred'], reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(reports[-1]['status'], 'VALIDATION_APPROVED')
        approved = app.read(inner.work / 'project.json')
        self.assertEqual(approved['specification'], spec)
        self.assertEqual(approved['pipeline']['calls'], 306)
        self.assertEqual(approved['checkpoints']['units'], units)
        self.assertEqual(approved['approvals']['assessment'], approvals['assessment'])
        self.assertEqual(app.main(['--workspace', str(inner.work), 'design-plan', '--mode', 'functional-parity',
                                   '--by', 'Owner'], reporter=lambda _result: None), 0)
        calls = []

        def wireframes(provider, run, directory, role, message):
            calls.append(role)
            return inner.screens()

        with patch.object(app, 'model_call', side_effect=wireframes), \
             patch.object(app, 'assessment', side_effect=AssertionError('aws')), \
             patch.object(app, 'pipeline', side_effect=AssertionError('checkpoint restart')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(calls, ['wireframes', 'wireframes'], 'the design plan call, then one detail call')
        self.assertEqual(reports[-1]['status'], 'AWAITING_SPECIFICATIONS_APPROVAL')
        finished = app.read(inner.work / 'project.json')
        self.assertEqual(finished['pipeline']['calls'], 306)
        self.assertEqual(finished['specification']['sha256'], spec['sha256'])
        self.assertEqual(finished['specification']['review_sha256'], spec['review_sha256'])
        self.assertEqual(finished['checkpoints']['units'], units)
        self.assertEqual(list(finished['assessments']), list(approvals and inner.project['assessments']))
        self.assertEqual(len(finished['assessments']), 1)


if __name__ == '__main__':
    unittest.main()
