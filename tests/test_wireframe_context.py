"""Wireframe context stages, placeholder rationales, and the pre-dispatch call counter."""
import json
import unittest
from pathlib import Path
from unittest.mock import patch

import test_reframe as fixtures
import reframe as app
from pilot import sha


class WireframeContextTests(unittest.TestCase):
    def setUp(self):
        self.inner = fixtures.PreparationTests('test_missing_sme_decision_blocks_validation_approval')
        self.inner.setUp()
        self.addCleanup(self.inner.doCleanups)

    def approved_project(self):
        inner = self.inner
        inner.validated()
        inner.approve('validation')
        return inner

    def test_saved_request_is_staged_inside_the_context_budget(self):
        live = Path('/Users/satish_byndr/Documents/workspace-intraedge/aws-mainframe-modernization-carddemo_assessment')
        if not (live / 'project.json').is_file():
            self.skipTest('saved CardDemo workspace is not on this machine')
        project = json.loads((live / 'project.json').read_text())
        spec = json.loads((live / project['specification']['path']).read_text())
        protocol = (app.FRAMEWORK / 'prompts/pipeline/wireframes.md').read_text()
        legacy = json.dumps({'protocol': protocol, 'specification': spec, 'decisions': project['decisions']})
        limit = project['settings']['max_context_bytes']
        self.assertGreater(len(legacy.encode()), 600000)
        self.assertGreater(len(legacy.encode()), limit)
        stages = app.wireframe_stages(spec, project['decisions'], limit, protocol)
        self.assertGreater(len(stages), 1)
        covered = {'rules': set(), 'questions': set(), 'evidence': set(), 'coverage': set()}
        for stage in stages:
            stage['catalog'] = app.wireframe_catalog(spec, project['decisions'])
            message = json.dumps(app.wireframe_message(spec, stage, len(stages), protocol))
            self.assertLessEqual(len(message.encode()), limit)
            payload = json.loads(message)
            body = payload['specification']
            self.assertNotIn('tests', body)
            self.assertNotIn('work_items', body)
            self.assertNotIn('implementation_prompt', json.dumps(body['sections']))
            self.assertTrue(all(set(item) == {'id', 'disposition'} for item in payload['decisions']))
            self.assertEqual(len(payload['decisions']), len(spec['questions']))
            covered['rules'].update(item['id'] for item in body['rules'])
            covered['questions'].update(item['id'] for item in body['questions'])
            covered['evidence'].update(item['id'] for item in body['assessment_evidence'])
            covered['coverage'].update(item['id'] for item in body['coverage'])
        self.assertEqual(covered['rules'], {rule['id'] for rule in spec['rules']})
        self.assertEqual(covered['questions'], {question['id'] for question in spec['questions']})
        self.assertTrue(all(item['disposition'] for item in json.loads(json.dumps(app.wireframe_message(
            spec, {**stages[0], 'catalog': app.wireframe_catalog(spec, project['decisions'])}, len(stages), protocol)))['decisions']))

    def test_an_oversized_record_is_refused_without_truncation_or_a_call(self):
        inner = self.approved_project()
        spec = app.read(inner.work / inner.project['specification']['path'])
        spec['rules'][0]['statement'] = 'x' * 200000
        with self.assertRaisesRegex(app.Blocked, 'not truncated'):
            app.wireframe_stages(spec, {}, inner.project['settings']['max_context_bytes'])
        self.assertEqual(inner.project.get('ui_calls') or 0, 0)
        self.assertFalse(any((inner.work / 'previews').glob('business-*')))

    def test_review_site_counts_a_call_only_after_the_request_fits(self):
        inner = self.approved_project()
        calls = []

        def provider(provider_name, run, directory, role, message):
            calls.append(role)
            self.assertLessEqual(len(message.encode()), inner.project['settings']['max_context_bytes'])
            self.assertNotIn('implementation_prompt', message)
            return inner.screens()

        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')), \
             patch.object(app, 'pipeline', side_effect=AssertionError('checkpoint')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
        self.assertEqual(code, 0)
        self.assertEqual(calls, ['wireframes', 'wireframes'], 'the design plan call, then one detail call')
        saved = app.read(inner.work / 'project.json')
        self.assertEqual(saved['ui_calls'], 2)
        self.assertEqual(saved['stage'], 'AWAITING_SPECIFICATIONS_APPROVAL')
        self.assertEqual(saved['pipeline']['calls'], inner.project['pipeline']['calls'])

    def test_placeholders_are_rejected_and_amended_without_losing_history(self):
        inner = self.approved_project()
        path = inner.work / inner.project['specification']['path']
        spec = app.read(path)
        spec['questions'] = [{'id': f'Q{index:04d}', 'question': 'fixture', 'impact': 'fixture',
                              'owner': 'SME', 'blocks': 'Implementation'} for index in range(6)]
        app.write(path, spec)
        inner.project['specification']['sha256'] = sha(path)
        for index in range(4):
            inner.project['decisions'][f'Q{index:04d}'] = {
                'by': 'saved', 'answer': 'YOUR_REASON', 'disposition': 'deferred',
                'specification_sha256': inner.project['specification']['sha256'], 'at': 1}
        inner.project['decisions']['Q0004'] = {
            'by': 'saved', 'answer': 'None', 'disposition': 'deferred',
            'specification_sha256': inner.project['specification']['sha256'], 'at': 1}
        inner.project['decisions']['Q0005'] = {
            'by': 'saved', 'answer': 'Keep the existing oracle', 'disposition': 'resolved',
            'specification_sha256': inner.project['specification']['sha256'], 'at': 1}
        app.preparation_report(inner.work, inner.project)
        inner.project['approvals']['validation'] = {
            'sha256': app.digest({'specification': inner.project['specification']['sha256'],
                                  'decisions': inner.project['decisions']}),
            'by': 'Owner', 'note': 'YOUR_APPROVAL_RATIONALE', 'at': 1,
            'report_sha256': inner.project['preparation_report']['sha256']}
        inner.project['stage'] = 'VALIDATION_APPROVED'
        inner.project['ui_calls'] = 1
        (inner.work / 'previews' / 'business-1').mkdir(parents=True)
        app.persist(inner.work, inner.project)
        reports = []
        with patch.object(app, 'model_call', side_effect=AssertionError('provider')), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            refused = app.main(['--workspace', str(inner.work), 'review-site'], reporter=reports.append)
        self.assertEqual(refused, 2)
        self.assertIn('YOUR_REASON', reports[-1]['reason'])
        self.assertEqual(app.read(inner.work / 'project.json')['ui_calls'], 1)
        preview = []
        code = app.main(['--workspace', str(inner.work), 'decide', '--placeholders', '--amend',
                         '--by', 'Owner', '--answer', 'Deferred until the oracle is located',
                         '--disposition', 'deferred'], reporter=preview.append)
        self.assertEqual(code, 0)
        self.assertEqual(preview[-1]['status'], 'DECISION_CONFIRMATION')
        self.assertEqual(preview[-1]['pending'], 4)
        self.assertNotIn('decision_history', app.read(inner.work / 'project.json'))
        code = app.main(['--workspace', str(inner.work), 'decide', '--placeholders', '--amend', '--confirm',
                         '--by', 'Owner', '--answer', 'Deferred until the oracle is located',
                         '--disposition', 'deferred'], reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(reports[-1]['recorded'], 4)
        saved = app.read(inner.work / 'project.json')
        self.assertEqual(saved['stage'], 'AWAITING_VALIDATION_APPROVAL')
        self.assertNotIn('validation', saved['approvals'])
        self.assertEqual(saved['approval_history'][0]['approval']['note'], 'YOUR_APPROVAL_RATIONALE')
        self.assertEqual(saved['decision_history'][0]['previous']['Q0000']['answer'], 'YOUR_REASON')
        self.assertEqual(len(saved['decision_batches']), 1)
        self.assertEqual(saved['decisions']['Q0004']['answer'], 'None')
        self.assertEqual(saved['decisions']['Q0005']['answer'], 'Keep the existing oracle')
        self.assertEqual(saved['pipeline']['calls'], inner.project['pipeline']['calls'])
        with self.assertRaisesRegex(app.Blocked, 'YOUR_APPROVAL_RATIONALE'):
            app.approve(inner.work, saved, inner.args('approve', 'validation', '--by', 'Owner', '--note', 'YOUR_APPROVAL_RATIONALE'))
        saved['framework_commit'] = 'b' * 40
        saved['pins']['framework_commit'] = 'b' * 40
        directory = Path(saved['assessments']['a']['directory'])
        run = app.read(directory / 'run.json')
        run['framework_commit'] = 'b' * 40
        app.write(directory / 'run.json', run)
        app.persist(inner.work, saved)
        upgraded = []
        code = app.main(['--workspace', str(inner.work), 'upgrade-framework', '--note', 'Record the controller update'],
                        reporter=upgraded.append)
        self.assertEqual(code, 0)
        self.assertEqual(upgraded[-1]['preserved'], 'reviewed_specification')
        current = app.read(inner.work / 'project.json')
        self.assertEqual(current['framework_commit'], 'a' * 40)
        self.assertEqual(current['specification']['sha256'], saved['specification']['sha256'])
        self.assertEqual(current['pipeline']['calls'], saved['pipeline']['calls'])
        self.assertNotIn('validation', current['approvals'])
        self.assertEqual(current['decisions']['Q0004']['answer'], 'None')

    def test_pre_dispatch_context_failure_does_not_reserve_a_call(self):
        inner = self.approved_project()
        inner.project['settings']['max_context_bytes'] = 1
        app.persist(inner.work, inner.project)
        spent = inner.project['settings']['model_dollars_spent']
        reports = []
        with patch.object(app, 'model_call', side_effect=AssertionError('provider')), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=reports.append)
        self.assertEqual(code, 2)
        self.assertIn('not truncated', reports[-1]['reason'])
        saved = app.read(inner.work / 'project.json')
        self.assertEqual(saved.get('ui_calls') or 0, 0)
        self.assertNotIn('wireframe_plan', saved)
        self.assertEqual(saved['settings']['model_dollars_spent'], spent)
        self.assertFalse(any((inner.work / 'previews').glob('business-*')))

    def test_reservation_recovery_keeps_receipts_spend_and_history(self):
        inner = self.approved_project()
        inner.project.setdefault('events', []).append({'event': 'older', 'at': 1})
        app.persist(inner.work, inner.project)
        spent = inner.project['settings']['model_dollars_spent']
        with patch.object(app, 'require_dollar_cap', side_effect=app.Blocked('dollar check stopped before dispatch')), \
             patch.object(app, 'model_call', side_effect=AssertionError('provider')), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
        self.assertEqual(code, 2)
        reserved = app.read(inner.work / 'project.json')
        self.assertEqual(reserved['ui_calls'], 1)
        self.assertEqual(reserved['wireframe_plan']['planner']['status'], 'reserved')
        self.assertFalse(reserved['wireframe_plan']['planner']['provider_invoked'])
        self.assertEqual(reserved['settings']['model_dollars_spent'], spent)
        released = []
        code = app.main(['--workspace', str(inner.work), 'recover-ui-call', '--confirm',
                         '--note', 'Release the pre-dispatch reservation'], reporter=released.append)
        self.assertEqual(code, 0, released[-1] if released else '')
        recovered = app.read(inner.work / 'project.json')
        self.assertEqual(recovered['ui_calls'], 0)
        self.assertEqual(recovered['wireframe_plan']['planner']['status'], 'pending')
        self.assertNotIn('call', recovered['wireframe_plan']['planner'])
        self.assertEqual(recovered['settings']['model_dollars_spent'], spent)
        self.assertEqual(recovered['events'][0]['event'], 'older')
        self.assertEqual(recovered['events'][-1]['event'], 'wireframe_counter_recovered')
        self.assertEqual(recovered['events'][-1]['from'], 1)
        self.assertEqual(recovered['events'][-1]['to'], 0)

    def test_provider_failure_and_invalid_output_stay_counted_without_screens(self):
        inner = self.approved_project()
        calls = {'count': 0}

        def fail(*_args):
            calls['count'] += 1
            raise RuntimeError('provider failed before a screen file')

        with patch.object(app, 'model_call', side_effect=fail), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            with self.assertRaises(RuntimeError):
                app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
            failed = app.read(inner.work / 'project.json')
            self.assertEqual(failed['ui_calls'], 1)
            self.assertEqual(failed['wireframe_plan']['planner']['status'], 'failed')
            self.assertTrue(failed['wireframe_plan']['planner']['provider_invoked'])
            self.assertFalse((inner.work / 'previews' / 'business-1' / 'screens.json').exists())
            self.assertTrue((inner.work / 'previews' / 'wireframe-stages' / 'stage-planner-failure.json').is_file())
            spent = failed['settings']['model_dollars_spent']
            held = []
            code = app.main(['--workspace', str(inner.work), 'recover-ui-call', '--confirm',
                             '--note', 'Do not erase the failed call'], reporter=held.append)
            self.assertEqual(code, 2)
            self.assertIn('not changed', held[-1]['reason'])
            code = app.main(['--workspace', str(inner.work), 'resume'], reporter=held.append)
        self.assertEqual(code, 2)
        self.assertEqual(calls['count'], 1)
        self.assertIn('stays counted', held[-1]['reason'])
        kept = app.read(inner.work / 'project.json')
        self.assertEqual(kept['ui_calls'], 1)
        self.assertEqual(kept['settings']['model_dollars_spent'], spent)

        other = fixtures.PreparationTests('test_missing_sme_decision_blocks_validation_approval')
        other.setUp()
        self.addCleanup(other.doCleanups)
        other.validated()
        other.approve('validation')

        def invalid(*_args):
            calls['count'] += 1
            return 'not a screen model'

        with patch.object(app, 'model_call', side_effect=invalid), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            code = app.main(['--workspace', str(other.work), 'review-site'], reporter=lambda _result: None)
            self.assertEqual(code, 2)
            saved = app.read(other.work / 'project.json')
            self.assertEqual(saved['ui_calls'], 1)
            self.assertEqual(saved['wireframe_plan']['planner']['status'], 'invalid')
            self.assertFalse((other.work / 'previews' / 'business-1' / 'screens.json').exists())
            self.assertTrue((other.work / 'previews' / 'wireframe-stages' / 'stage-planner.json').is_file())
            code = app.main(['--workspace', str(other.work), 'resume'], reporter=lambda _result: None)
        self.assertEqual(code, 2)
        self.assertEqual(calls['count'], 2)
        self.assertEqual(app.read(other.work / 'project.json')['ui_calls'], 1)

    def test_an_authorized_new_attempt_follows_a_failed_wireframe_call(self):
        inner = self.approved_project()

        def fail(*_args):
            raise RuntimeError('provider failed before a screen file')

        with patch.object(app, 'model_call', side_effect=fail), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            with self.assertRaises(RuntimeError):
                app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
            stopped = []
            self.assertEqual(app.main(['--workspace', str(inner.work), 'review-site'], reporter=stopped.append), 2)
        self.assertEqual(stopped[-1]['cause'], 'PROVIDER_FAILURE')
        self.assertIn('retry-wireframes', stopped[-1]['hint'])
        status = []
        app.main(['--workspace', str(inner.work), 'status'], reporter=status.append)
        self.assertIn('retry-wireframes', status[-1]['next_step'])
        plan = []
        app.main(['--workspace', str(inner.work), 'recovery-plan'], reporter=plan.append)
        self.assertTrue(any('retry-wireframes' in item for item in plan[-1]['requires_authorization']))
        refused = []
        self.assertEqual(app.main(['--workspace', str(inner.work), 'retry-wireframes', '--by', 'NAME', '--note', 'WHY'],
                                  reporter=refused.append), 2)
        authorized = []
        self.assertEqual(app.main(['--workspace', str(inner.work), 'retry-wireframes', '--by', 'Architect',
                                   '--note', 'The provider outage is over'], reporter=authorized.append), 0)
        saved = app.read(inner.work / 'project.json')
        self.assertEqual(saved['ui_calls'], 1, 'the failed call stays counted')
        stage = saved['wireframe_plan']['planner']
        self.assertEqual(stage['status'], 'pending')
        self.assertEqual(stage['attempt_history'][0]['status'], 'failed')
        self.assertTrue(all((inner.work / path).is_file() for path in stage['attempt_history'][0]['receipts']))
        self.assertFalse((inner.work / 'previews' / 'wireframe-stages' / 'stage-planner-failure.json').exists())
        with patch.object(app, 'model_call', side_effect=lambda *a: inner.screens()), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            self.assertEqual(app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _r: None), 0)
        done = app.read(inner.work / 'project.json')
        self.assertEqual(done['ui_calls'], 3, 'the new plan attempt and the detail call are counted after the failed one')
        self.assertEqual(done['stage'], 'AWAITING_SPECIFICATIONS_APPROVAL')

    def test_only_an_unspent_undispatched_reservation_is_released(self):
        inner = self.approved_project()
        with patch.object(app, 'require_dollar_cap', side_effect=app.Blocked('dollar check stopped before dispatch')), \
             patch.object(app, 'model_call', side_effect=AssertionError('provider')):
            app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
        reserved = app.read(inner.work / 'project.json')
        self.assertEqual(reserved['wireframe_plan']['planner']['status'], 'reserved')
        for change in ({'status': 'dispatched'}, {'provider_invoked': True},
                       {'spent_before': reserved['settings']['model_dollars_spent'] + 1}):
            tampered = json.loads(json.dumps(reserved))
            tampered['wireframe_plan']['planner'].update(change)
            app.write(inner.work / 'project.json', tampered)
            results = []
            code = app.main(['--workspace', str(inner.work), 'recover-ui-call', '--confirm', '--note', 'Release it'],
                            reporter=results.append)
            self.assertEqual(code, 2, change)
            self.assertIn('The counter was not changed', results[-1]['reason'])
            self.assertEqual(app.read(inner.work / 'project.json')['ui_calls'], 1, change)

    def test_a_contract_failure_reserves_nothing(self):
        inner = self.approved_project()
        with patch.object(app, 'require_stage_contract', side_effect=app.Blocked('stage contract changed')), \
             patch.object(app, 'model_call', side_effect=AssertionError('provider')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
        self.assertEqual(code, 2)
        saved = app.read(inner.work / 'project.json')
        self.assertEqual(saved.get('ui_calls') or 0, 0)
        self.assertFalse(any(stage.get('status') == 'reserved' for stage in (saved.get('wireframe_plan') or {}).get('stages') or []))
        self.assertFalse(any((inner.work / 'previews').glob('business-*')))

    def test_restart_after_provider_completion_does_not_recall_or_reduce_the_counter(self):
        inner = self.approved_project()
        calls = {'count': 0}
        real_write = app.write

        def provider(*_args):
            calls['count'] += 1
            return inner.screens()

        def crash(path, value):
            if str(path).endswith('screens.json'):
                raise RuntimeError('crash before screen persistence')
            real_write(path, value)

        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'write', side_effect=crash), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            with self.assertRaises(RuntimeError):
                app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
        interrupted = app.read(inner.work / 'project.json')
        self.assertEqual(interrupted['ui_calls'], 2, 'the design plan call and the detail call')
        self.assertEqual(interrupted['wireframe_plan']['stages'][0]['status'], 'received')
        self.assertTrue((inner.work / 'previews' / 'wireframe-stages' / 'stage-0.json').is_file())
        self.assertFalse((inner.work / 'previews' / 'business-2' / 'screens.json').exists())
        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            code = app.main(['--workspace', str(inner.work), 'resume'], reporter=lambda _result: None)
        self.assertEqual(code, 0)
        self.assertEqual(calls['count'], 2, 'resume made no new call')
        resumed = app.read(inner.work / 'project.json')
        self.assertEqual(resumed['ui_calls'], 2)
        self.assertEqual(resumed['wireframe_plan']['stages'][0]['status'], 'validated')
        self.assertTrue((inner.work / 'previews' / 'business-2' / 'screens.json').is_file())

    def test_ambiguous_legacy_counter_is_not_recovered(self):
        inner = self.approved_project()
        inner.project['ui_calls'] = 1
        inner.project['settings']['model_dollars_spent'] = 1.25
        inner.project['events'] = [{'event': 'older', 'at': 1}]
        (inner.work / 'previews' / 'business-1').mkdir(parents=True)
        app.persist(inner.work, inner.project)
        reports = []
        code = app.main(['--workspace', str(inner.work), 'recover-ui-call', '--confirm',
                         '--note', 'Empty directory is not proof'], reporter=reports.append)
        self.assertEqual(code, 2)
        self.assertIn('Missing screens.json', reports[-1]['reason'])
        saved = app.read(inner.work / 'project.json')
        self.assertEqual(saved['ui_calls'], 1)
        self.assertEqual(saved['settings']['model_dollars_spent'], 1.25)
        self.assertEqual(saved['events'], [{'event': 'older', 'at': 1}])
        with patch.object(app, 'model_call', return_value=inner.screens()), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=reports.append)
        self.assertEqual(code, 0)
        continued = app.read(inner.work / 'project.json')
        self.assertEqual(continued['ui_calls'], 3, 'the legacy count stays; the plan call and one detail call follow')
        self.assertFalse(any((inner.work / 'previews' / 'business-1').iterdir()))
        self.assertTrue((inner.work / 'previews' / 'business-3' / 'screens.json').is_file())
        self.assertEqual(round(continued['settings']['model_dollars_spent'], 2), 1.29)

    def two_stage_project(self):
        inner = self.approved_project()
        spec = app.read(inner.work / inner.project['specification']['path'])
        protocol = (app.FRAMEWORK / 'prompts/pipeline/wireframes.md').read_text()
        import reframe_design
        whole = app.wireframe_stages(spec, inner.project['decisions'], 600000, protocol)
        whole[0]['catalog'] = app.wireframe_catalog(spec, inner.project['decisions'])
        size = len(json.dumps({**app.wireframe_message(spec, whole[0], 1, protocol),
                               **reframe_design.message_view(inner.work, inner.project)}).encode())
        inner.project['settings']['max_context_bytes'] = size + size // 16
        app.persist(inner.work, inner.project)
        return inner

    PLAN = {'journeys': [{'id': 'amount', 'title': 'Amount', 'stage': 1, 'screen_ids': ['s1']},
                         {'id': 'audit', 'title': 'Audit', 'stage': 2, 'screen_ids': ['s2']}],
            'screens': [{'id': 's1', 'title': 'Amount', 'stage': 1, 'rule_ids': ['R1'], 'api_ids': ['validate-amount'],
                         'actions': [{'label': 'Continue', 'screen_id': 's2'}]},
                        {'id': 's2', 'title': 'Audit', 'stage': 2, 'rule_ids': ['R1']}],
            'apis': [{'id': 'validate-amount', 'title': 'Validate', 'stage': 1, 'rule_ids': ['R1']}],
            'shared_components': [], 'gaps': [{'id': 'g1', 'question_id': 'Q1', 'note': 'Amount owner undecided'}]}

    def test_the_plan_is_saved_and_hashed_and_the_first_detail_request_carries_it(self):
        inner = self.two_stage_project()
        sent = []

        def provider(_provider, _run, _directory, _role, message):
            request = json.loads(message)
            sent.append(request)
            if request['stage'].get('planner'):
                return json.loads(json.dumps(self.PLAN))
            raise RuntimeError('stop before any detail reply exists')

        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            with self.assertRaises(RuntimeError):
                app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
        saved = app.read(inner.work / 'project.json')
        import reframe_design
        inventory = app.read(inner.work / saved['design_inventory']['path'])
        self.assertEqual([request['stage'].get('planner') for request in sent], [True, None], 'the plan call came first')
        self.assertEqual(inventory['planned_sha256'], reframe_design._digest(inventory['planned']))
        self.assertEqual(inventory['owners'], {'journeys': {'amount': 1, 'audit': 2}, 'screens': {'s1': 1, 's2': 2},
                                               'apis': {'validate-amount': 1}})
        self.assertEqual(inventory['planner']['call'], 1)
        self.assertTrue((inner.work / inventory['planner']['receipt']).is_file())
        self.assertEqual({link['id'] for link in next(item for item in inventory['planned']['screens'] if item['id'] == 's1')['depends_on']},
                         {'validate-amount', 's2'})
        self.assertEqual(inventory['planned']['gaps'], [{'id': 'g1', 'question_id': 'Q1', 'note': 'Amount owner undecided'}])
        self.assertTrue(len(inventory['stage_assignments']) >= 2)
        first = sent[1]
        self.assertEqual(first['stage']['index'], 1)
        self.assertEqual({(item['kind'], item['id']) for item in first['define']},
                         {('journeys', 'amount'), ('screens', 's1'), ('apis', 'validate-amount')})
        self.assertEqual({(item['kind'], item['id'], item['owner_stage']) for item in first['owned']},
                         {('journeys', 'audit', 2), ('screens', 's2', 2)})
        self.assertFalse((inner.work / 'previews' / 'wireframe-stages' / 'stage-0.json').exists(), 'no detail reply exists yet')

    def test_a_detail_stage_that_adds_an_unplanned_id_stops_for_a_new_design_version(self):
        inner = self.two_stage_project()

        def provider(_provider, _run, _directory, _role, message):
            request = json.loads(message)
            if request['stage'].get('planner'):
                return json.loads(json.dumps(self.PLAN))
            model = inner.screens()
            model['screens'].append({'id': 'surprise', 'title': 'Unplanned', 'purpose': 'Not in the plan', 'rule_ids': ['R1'],
                                     'fields': ['x'], 'actions': ['Close'], 'states': ['Shown'], 'api_ids': [],
                                     'uncertainties': 'Unproven'})
            return model

        reports = []
        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=reports.append)
        self.assertEqual(code, 2)
        self.assertEqual(reports[-1]['cause'], 'HUMAN_DECISION_REQUIRED')
        self.assertIn('unplanned screens surprise', reports[-1]['reason'])
        self.assertIn('design-plan --revise', reports[-1]['hint'])
        saved = app.read(inner.work / 'project.json')
        self.assertEqual(saved['ui_calls'], 2, 'the plan call and the detail call stay counted')
        self.assertTrue((inner.work / 'previews' / 'wireframe-stages' / 'stage-0.json').is_file(), 'the reply is kept')
        self.assertNotIn('site', saved)
        with patch.object(app, 'model_call', side_effect=AssertionError('provider')), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            self.assertEqual(app.main(['--workspace', str(inner.work), 'review-site'], reporter=reports.append), 2)
        self.assertIn('unplanned screens surprise', reports[-1]['reason'], 'resume does not merge it or call again')
        self.assertEqual(app.main(['--workspace', str(inner.work), 'design-plan', '--mode', 'functional-parity',
                                   '--version', 'v2', '--by', 'Owner', '--revise'], reporter=reports.append), 0)
        revised = app.read(inner.work / 'project.json')
        self.assertTrue(revised['design_history'][-1]['stage_receipts'], 'the earlier receipts are kept')
        self.assertNotIn('wireframe_plan', revised)
        sent = []

        def planned_only(_provider, _run, _directory, _role, message):
            request = json.loads(message)
            sent.append(request['stage'].get('planner'))
            if request['stage'].get('planner'):
                return json.loads(json.dumps(self.PLAN))
            model = inner.screens()
            model['screens'][0]['actions'] = [{'label': 'Continue', 'screen_id': 's2'}]
            if request['stage']['index'] == 2:
                return {'journeys': [{'id': 'audit', 'name': 'Audit', 'summary': 'Read the audit.', 'screen_ids': ['s2']}],
                        'screens': [{'id': 's2', 'title': 'Audit', 'purpose': 'Show the audit', 'rule_ids': ['R1'],
                                     'fields': ['Result'], 'actions': ['Close'], 'states': ['Shown'], 'api_ids': [],
                                     'uncertainties': 'Unproven'}], 'apis': []}
            return model

        with patch.object(app, 'model_call', side_effect=planned_only), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            self.assertEqual(app.main(['--workspace', str(inner.work), 'review-site'], reporter=reports.append), 0, reports[-1])
        self.assertTrue(sent[0], 'the new design version is planned again before its detail calls')

    def test_an_invalid_plan_stays_counted_and_can_be_retried(self):
        inner = self.two_stage_project()

        def provider(_provider, _run, _directory, _role, message):
            plan = json.loads(json.dumps(self.PLAN))
            plan['screens'][0]['requirement_ids'] = ['aws-req:fake:UNKNOWN-999']
            return plan

        reports = []
        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            self.assertEqual(app.main(['--workspace', str(inner.work), 'review-site'], reporter=reports.append), 2)
        self.assertIn('unknown requirement aws-req:fake:UNKNOWN-999', reports[-1]['reason'])
        saved = app.read(inner.work / 'project.json')
        self.assertEqual((saved['ui_calls'], saved['wireframe_plan']['planner']['status']), (1, 'invalid'))
        self.assertTrue(all(stage['status'] == 'pending' for stage in saved['wireframe_plan']['stages']), 'no detail call was made')
        self.assertNotIn('planned', app.read(inner.work / saved['design_inventory']['path']))
        self.assertEqual(app.main(['--workspace', str(inner.work), 'retry-wireframes', '--by', 'Architect',
                                   '--note', 'Plan again without the unknown requirement'], reporter=reports.append), 0)
        self.assertEqual(app.read(inner.work / 'project.json')['wireframe_plan']['planner']['status'], 'pending')

    def test_a_changed_saved_plan_is_refused(self):
        inner = self.two_stage_project()

        def provider(_provider, _run, _directory, _role, message):
            if json.loads(message)['stage'].get('planner'):
                return json.loads(json.dumps(self.PLAN))
            raise RuntimeError('stop after the plan')

        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            with self.assertRaises(RuntimeError):
                app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
        saved = app.read(inner.work / 'project.json')
        path = inner.work / saved['design_inventory']['path']
        inventory = app.read(path)
        inventory['planned']['screens'][0]['owner_stage'] = 2
        app.write(path, inventory)
        import reframe_design
        with self.assertRaisesRegex(app.Blocked, 'planned design inventory changed'):
            reframe_design.verified_plan(inner.work, saved)

    def test_staged_generation_keeps_cross_references_and_rejects_conflicting_ids(self):
        inner = self.approved_project()
        spec = app.read(inner.work / inner.project['specification']['path'])
        protocol = (app.FRAMEWORK / 'prompts/pipeline/wireframes.md').read_text()
        whole = app.wireframe_stages(spec, inner.project['decisions'], 600000, protocol)
        self.assertEqual(len(whole), 1)
        whole[0]['catalog'] = app.wireframe_catalog(spec, inner.project['decisions'])
        import reframe_design
        request = {**app.wireframe_message(spec, whole[0], 1, protocol), **reframe_design.message_view(inner.work, inner.project)}
        size = len(json.dumps(request).encode())
        # Packing keeps an eighth of a small budget for the planned id lists, so this budget still forces two stages.
        inner.project['settings']['max_context_bytes'] = size + size // 16
        app.persist(inner.work, inner.project)
        self.assertGreater(len(app.wireframe_stages(spec, inner.project['decisions'], size + size // 16, protocol,
                                                    reframe_design.message_view(inner.work, inner.project))), 1)
        calls = {'count': 0}

        def provider(_provider, _run, _directory, _role, message):
            calls['count'] += 1
            index = json.loads(message)['stage']['index']
            if index == 0:
                return {'journeys': [{'id': 'amount', 'title': 'Amount', 'stage': 1, 'screen_ids': ['s1']},
                                     {'id': 'audit', 'title': 'Audit', 'stage': 2, 'screen_ids': ['s2']}],
                        'screens': [{'id': 's1', 'title': 'Amount', 'stage': 1, 'rule_ids': ['R1'],
                                     'api_ids': ['validate-amount', 'audit-amount'],
                                     'actions': [{'label': 'Continue', 'screen_id': 's2'}]},
                                    {'id': 's2', 'title': 'Audit', 'stage': 2, 'rule_ids': ['R1'], 'api_ids': ['audit-amount']}],
                        'apis': [{'id': 'validate-amount', 'title': 'Validate', 'stage': 1, 'rule_ids': ['R1']},
                                 {'id': 'audit-amount', 'title': 'Audit', 'stage': 2, 'rule_ids': ['R1']}],
                        'shared_components': [{'kind': 'apis', 'id': 'audit-amount', 'used_by': ['amount', 'audit']}]}
            if index == 1:
                model = inner.screens()
                model['screens'][0]['actions'] = [{'label': 'Continue', 'screen_id': 's2'}]
                model['screens'][0]['api_ids'] = ['validate-amount', 'audit-amount']
                model['journeys'][0]['screen_ids'] = ['s1']
                return model
            if index == 2:
                return {'journeys': [{'id': 'audit', 'name': 'Audit', 'summary': 'Read the audit result.',
                                       'screen_ids': ['s2']}],
                        'screens': [{'id': 's2', 'title': 'Audit', 'purpose': 'Show the audit result',
                                     'rule_ids': ['R1'], 'fields': ['Result'], 'actions': ['Close'],
                                     'states': ['Shown'], 'api_ids': ['audit-amount'],
                                     'uncertainties': 'Runtime equivalence is unproven'}],
                        'apis': [{'id': 'audit-amount', 'method': 'GET', 'path': '/amount/audit',
                                  'purpose': 'Read the audit result', 'authentication': 'Proposed authenticated caller',
                                  'uncertainties': 'No runtime parity proof', 'request': {'amount': 'number'},
                                  'responses': {'200': 'shown'}, 'rule_ids': ['R1']}]}
            return {'journeys': [], 'screens': [], 'apis': []}

        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
        self.assertEqual(code, 0)
        self.assertGreater(calls['count'], 1)
        saved = app.read(inner.work / 'project.json')
        merged = app.read(inner.work / 'previews' / ('business-' + str(saved['ui_calls'])) / 'screens.json')
        self.assertEqual(merged['screens'][0]['actions'][0]['screen_id'], 's2')
        self.assertIn('audit-amount', merged['screens'][0]['api_ids'])
        self.assertEqual({item['id'] for item in merged['apis']}, {'validate-amount', 'audit-amount'})
        app.validate_screens(merged, spec)
        self.assertEqual(saved['wireframe_plan']['stages'][0]['status'], 'validated')
        duplicate_screen = inner.screens()
        duplicate_screen['journeys'][0]['id'] = 'amount-again'
        duplicate_screen['screens'][0]['purpose'] = 'A second sign-on definition'
        with self.assertRaisesRegex(app.Blocked, 'conflicting screens definitions for s1'):
            app.merge_wireframe_responses([inner.screens(), duplicate_screen])
        self.assertEqual(duplicate_screen['screens'][0]['id'], 's1')
        duplicate_journey = inner.screens()
        duplicate_journey['screens'][0]['id'] = 's9'
        duplicate_journey['journeys'][0]['screen_ids'] = ['s9']
        duplicate_journey['journeys'][0]['summary'] = 'A different summary'
        duplicate_journey['apis'][0]['id'] = 'other-amount'
        with self.assertRaisesRegex(app.Blocked, 'conflicting journeys definitions for amount'):
            app.merge_wireframe_responses([inner.screens(), duplicate_journey])
        self.assertEqual(duplicate_journey['journeys'][0]['id'], 'amount')
        shared = inner.screens()
        reference = {'journeys': [], 'screens': [{'id': 's1', 'ref': True}], 'apis': [{'id': 'validate-amount', 'ref': True}]}
        collapsed = app.merge_wireframe_responses([shared, reference])
        self.assertEqual([item['id'] for item in collapsed['screens']], ['s1'])
        self.assertEqual(collapsed['screens'][0]['purpose'], shared['screens'][0]['purpose'])
        conflict = dict(merged)
        conflict['screens'] = [dict(conflict['screens'][0], rule_ids=['NOT-A-RULE'])]
        with self.assertRaisesRegex(app.Blocked, 'unknown rule'):
            app.validate_screens(conflict, spec)


if __name__ == '__main__':
    unittest.main()
