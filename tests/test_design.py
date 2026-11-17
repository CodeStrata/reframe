"""Design plan, inventory, shared definitions, references, API completeness (FR-07, FR-08; AC-11, AC-21, AC-22, AC-24). L1."""
import argparse
import json
import unittest

import test_m1_contracts as m1
import test_reframe as fixtures
import reframe as app
import reframe_design as design
import reframe_states as states
from pilot import Blocked

SIGN_ON = {'id': 'sign-on', 'title': 'Sign on', 'purpose': 'Identify the person', 'rule_ids': ['R1'],
           'fields': ['User'], 'actions': ['Submit'], 'states': ['Signed on'], 'api_ids': [], 'uncertainties': 'Unproven'}


class MergeTests(unittest.TestCase):
    def test_identical_shared_definitions_collapse_and_references_resolve(self):
        merged = design.merge([(0, {'screens': [SIGN_ON], 'journeys': [], 'apis': []}),
                               (1, {'screens': [{'id': 'sign-on', 'ref': True}, dict(SIGN_ON)], 'journeys': [], 'apis': []})])
        self.assertEqual([item['id'] for item in merged['screens']], ['sign-on'])
        self.assertEqual(merged['superseded_definitions'], [])

    def test_conflicting_definitions_stop_with_every_conflict_named(self):
        other = dict(SIGN_ON, fields=['User', 'Password'])
        with self.assertRaises(Blocked) as raised:
            design.merge([(0, {'screens': [SIGN_ON]}), (1, {'screens': [other]})])
        self.assertEqual(states.describe(raised.exception)['cause'], 'HUMAN_DECISION_REQUIRED')
        self.assertIn('conflicting screens definitions for sign-on', str(raised.exception))
        self.assertIn('Nothing was renamed or overwritten', str(raised.exception))
        self.assertIn('reconcile-design', raised.exception.hint)

    def test_a_recorded_reconciliation_keeps_the_other_definition_as_superseded(self):
        other = dict(SIGN_ON, fields=['User', 'Password'])
        merged = design.merge([(0, {'screens': [SIGN_ON]}), (1, {'screens': [other]})],
                              [{'kind': 'screens', 'id': 'sign-on', 'keep_stage': 2}])
        self.assertEqual(merged['screens'][0]['fields'], ['User', 'Password'])
        self.assertEqual(merged['superseded_definitions'][0]['stage'], 1)
        self.assertEqual(merged['superseded_definitions'][0]['definition']['fields'], ['User'])

    def test_a_reference_without_a_definition_is_refused(self):
        with self.assertRaisesRegex(Blocked, 'without a definition: sign-on'):
            design.merge([(0, {'screens': [{'id': 'sign-on', 'ref': True}]})])

    def test_global_references_must_resolve(self):
        spec = {'rules': [{'id': 'R1'}]}
        good = {'screens': [dict(SIGN_ON, api_ids=['a1'])], 'apis': [{'id': 'a1', 'rule_ids': ['R1']}],
                'journeys': [{'id': 'j', 'screen_ids': ['sign-on']}]}
        self.assertTrue(design.validate_references(good, spec))
        bad = {'screens': [dict(SIGN_ON, api_ids=['missing'], rule_ids=['R9'])], 'apis': [],
               'journeys': [{'id': 'j', 'screen_ids': ['nowhere']}]}
        with self.assertRaises(Blocked) as raised:
            design.validate_references(bad, spec)
        for text in ('unknown screen nowhere', 'unknown API missing', 'unknown rule or requirement R9'):
            self.assertIn(text, str(raised.exception))
        self.assertTrue(design.validate_references({'screens': [dict(SIGN_ON, rule_ids=['aws-req:F1:PAY-001'])], 'apis': [],
                                                    'journeys': []}, spec, ['aws-req:F1:PAY-001']))


class ApiCompletenessTests(unittest.TestCase):
    def test_each_missing_part_is_named_not_invented(self):
        report = design.api_completeness([
            {'id': 'get', 'method': 'GET', 'path': '/x', 'responses': {'200': 'ok', '404': 'missing'},
             'auth': 'caller', 'rule_ids': ['R1']},
            {'id': 'post', 'method': 'POST', 'path': '/x', 'responses': {'201': 'created'}}])
        rows = {row['id']: row for row in report['rows']}
        self.assertEqual(rows['get']['state'], 'complete')
        self.assertEqual(rows['post']['gaps'], ['auth_assumption', 'error_cases', 'evidence_links', 'idempotency_note',
                                                'request_schema'])
        self.assertEqual((report['complete'], report['with_gaps']), (1, 1))
        self.assertIn('api-completeness', design.completeness_html(report))


class PlanAndRegenerationTests(m1.WorkspaceFixture):
    def approved(self):
        result = app.pipeline(self.work, self.project, self.args('validate'), self.runtime)
        self.assertEqual(result['status'], 'AWAITING_VALIDATION_APPROVAL')
        spec = app.read(app.spec_path(self.work, self.project))
        ids = [q['id'] for q in spec['questions']]
        if ids:
            app.decision(self.work, self.project, argparse.Namespace(
                question=None, questions=','.join(ids), open=False, placeholders=False, by='SME',
                answer='Deferred for this fixture', disposition='deferred', amend=False, confirm=True))
        app.approve(self.work, self.project, argparse.Namespace(
            phase='validation', by='Architect', note='Reviewed', label=None, confirm_source_match=False))

    def wireframes(self, calls):
        def runtime(provider, run, directory, role, message):
            request = json.loads(message)
            calls.append(request)
            screens = fixtures.PreparationTests.screens(None)
            rule = request['specification']['rules'][0]['id']
            for item in screens['screens'] + screens['apis']:
                item['rule_ids'] = [rule]
            return screens
        return runtime

    def test_detailed_design_needs_a_recorded_plan(self):
        self.approved()
        with self.assertRaises(Blocked) as raised:
            app.review_site(self.work, self.project, argparse.Namespace(provider='claude'), self.wireframes([]))
        self.assertEqual(states.describe(raised.exception)['cause'], 'HUMAN_DECISION_REQUIRED')
        self.assertNotIn('site', self.project)

    def test_the_plan_shapes_requests_and_the_inventory_is_saved_before_detail(self):
        self.approved()
        design.capture(self.work, self.project, 'reimagine', 'v1', 'java', 'jvm', 'cloud', ['Keep batch windows'], 'Architect')
        calls = []
        app.review_site(self.work, self.project, argparse.Namespace(provider='claude'), self.wireframes(calls))
        self.assertEqual(calls[0]['design_plan']['mode'], 'reimagine')
        self.assertEqual(calls[0]['design_plan']['target'], {'language': 'java', 'runtime': 'jvm', 'platform': 'cloud'})
        self.assertIn('Keep batch windows', calls[0]['design_plan']['constraints'])
        inventory = design.load_inventory(self.work, self.project)
        self.assertTrue(inventory['saved_before_detail'])
        self.assertEqual(inventory['design_plan']['mode'], 'reimagine')
        self.assertTrue(inventory['owners']['screens'])
        self.assertEqual(self.project['site']['design_plan']['mode'], 'reimagine')
        self.assertTrue((self.work / self.project['site']['directory'] / 'api-completeness.json').is_file())

    def refused(self, kinds, message):
        self.approved()
        design.capture(self.work, self.project, 'functional-parity', 'v1', 'java', '', '', [], 'Architect')

        def runtime(provider, run, directory, role, request):
            screens = fixtures.PreparationTests.screens(None)
            rule = json.loads(request)['specification']['rules'][0]['id']
            for kind in ('screens', 'apis'):
                for item in screens[kind]:
                    item['rule_ids'] = ['R999'] if kind in kinds else [rule]
            return screens

        with self.assertRaisesRegex(Blocked, message):
            app.review_site(self.work, self.project, argparse.Namespace(provider='claude'), runtime)
        self.assertNotIn('site', self.project)

    def test_an_api_citing_an_unknown_rule_is_refused(self):
        self.refused(('apis',), 'Unknown API rule reference')

    def test_a_screen_citing_an_unknown_rule_is_refused(self):
        self.refused(('screens',), 'Screen has unknown rule reference')

    def test_design_feedback_reports_what_happened_not_an_approval(self):
        self.approved()
        design.capture(self.work, self.project, 'functional-parity', 'v1', 'java', '', '', [], 'Architect')
        app.review_site(self.work, self.project, argparse.Namespace(provider='claude'), self.wireframes([]))
        result = app.feedback(self.work, self.project, argparse.Namespace(scope='design', by='Owner', note='Label the amount',
                                                                          unit=None, authorize_correction=False))
        self.assertEqual(result['status'], 'DESIGN_FEEDBACK_RECORDED')
        self.assertEqual(result['stage'], 'VALIDATION_APPROVED')
        self.assertNotIn('APPROVED', result['status'])

    def test_skip_route_design_feedback_names_only_what_the_run_keeps(self):
        self.approved()
        self.project.pop('specification')
        self.project['verification_skip'] = {'by': 'Owner', 'reason': 'Fixture skip'}
        self.project['skip_bundle'] = 'previews/skip-fixture'
        result = app.feedback(self.work, self.project, argparse.Namespace(scope='design', by='Owner', note='Label the amount',
                                                                          unit=None, authorize_correction=False))
        self.assertEqual(result['stage'], 'ASSESSMENT_APPROVED')
        self.assertEqual(result['kept'], ['assessment approval', 'skip decision', 'decisions'])
        self.assertNotIn('specification', result['kept'], 'a skip-route run has no specification to keep')

    def test_a_changed_plan_regenerates_and_never_returns_the_stale_design(self):
        self.approved()
        design.capture(self.work, self.project, 'functional-parity', 'v1', 'java', '', '', [], 'Architect')
        calls = []
        app.review_site(self.work, self.project, argparse.Namespace(provider='claude'), self.wireframes(calls))
        first_site = self.project['site']['directory']
        with self.assertRaisesRegex(Blocked, '--revise'):
            design.capture(self.work, self.project, 'functional-parity', 'v1', 'cobol', '', '', [], 'Architect')
        result = design.capture(self.work, self.project, 'functional-parity', 'v1', 'cobol', '', '', [], 'Architect', revise=True)
        self.assertTrue(result['revised'])
        self.assertNotIn('site', self.project)
        self.assertEqual(self.project['design_history'][-1]['site']['directory'], first_site)
        self.assertTrue(self.project['design_history'][-1]['stage_receipts'])
        app.review_site(self.work, self.project, argparse.Namespace(provider='claude'), self.wireframes(calls))
        self.assertEqual(len(calls), 2, 'the new plan made a new provider call instead of reading the old receipt')
        self.assertEqual(calls[-1]['design_plan']['target']['language'], 'cobol')
        self.assertNotEqual(self.project['site']['directory'], first_site)


if __name__ == '__main__':
    unittest.main()
