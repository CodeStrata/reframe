"""Connected workflow checks. External AWS and model calls stay mocked."""
import io
import json
import re
import unittest
from pathlib import Path
from unittest.mock import patch

from rich.console import Console

import test_reframe as fixtures
import reframe as app
from pilot import sha
from reframe_terminal import Terminal


class WorkflowJourneyTests(unittest.TestCase):
    def setUp(self):
        self.inner = fixtures.PreparationTests('test_missing_sme_decision_blocks_validation_approval')
        self.inner.setUp()
        self.addCleanup(self.inner.doCleanups)

    def test_extraction_is_not_called_requirements(self):
        notice = app.requirements_evidence_notice({'assessment_index': [{'path': 'rules.json'}]})
        self.assertIn('Requirements generation was not performed', notice)
        self.assertIn('not requirements', notice)
        sealed = app.requirements_evidence_notice({'assessment_index': [
            {'path': 'rules.json'}, {'path': 'requirements.md'}, {'path': 'traceability.yaml'}]})
        self.assertIn('requirements.md', sealed)
        self.assertIn('not renamed', sealed)
        self.assertNotIn('Requirements generation was not performed', sealed)

    def test_preparation_report_links_only_pages_that_exist_beside_it(self):
        inner = self.inner
        inner.validated()
        report = Path(app.preparation_report(inner.work, inner.project))
        page = report.read_text()
        self.assertNotIn('href="api.html"', page)
        self.assertNotIn('href="usage.html"', page)
        self.assertIn('href="#flow"', page)

    def test_bulk_deferral_is_one_result_and_many_steps_are_one_status(self):
        inner = self.inner
        inner.validated()
        path = inner.work / inner.project['specification']['path']
        spec = app.read(path)
        spec['questions'] = [{'id': f'Q{index:04d}', 'question': 'fixture', 'impact': 'fixture',
                              'owner': 'SME', 'blocks': 'Implementation'} for index in range(400)]
        app.write(path, spec)
        inner.project['specification']['sha256'] = sha(path)
        app.persist(inner.work, inner.project)
        reports = []
        code = app.main(['--workspace', str(inner.work), 'decide', '--open', '--confirm',
                         '--by', 'Owner', '--answer', 'Deferred for package review',
                         '--disposition', 'deferred'], reporter=reports.append)
        self.assertEqual(code, 0)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]['recorded'], 400)
        self.assertNotIn('questions', reports[0])
        output = io.StringIO()
        ui = Terminal(console=Console(file=output, width=100, height=40, color_system=None))
        ui.report(reports[0])
        self.assertEqual(output.getvalue().count('AWAITING VALIDATION APPROVAL'), 1)
        steps = [{'name': 'step-' + str(index), 'status': 'SUCCEEDED'} for index in range(120)]
        project = {'stage': 'AWAITING_VALIDATION_APPROVAL', 'settings': {}, 'approvals': {}, 'pipeline': {'calls': 0}}
        with patch.object(ui, 'project', return_value=project), \
             patch('reframe_setup.workspace', return_value=inner.work), \
             patch('reframe_setup.next_step', return_value='reframe approve validation'), \
             patch('reframe.saved_progress', return_value={'active_assessment': None, 'saved_status': None,
                                                           'reason': None, 'steps': steps}), \
             patch('reframe.watcher_owns', return_value=False):
            ui.show_status()
        text = output.getvalue()
        self.assertIn('Plan steps  120', text)
        self.assertNotIn('step-119', text)
        self.assertEqual(text.count('Project status'), 1)

    def test_saved_wireframe_stages_conflict_without_rewriting_them(self):
        live = Path('/Users/satish_byndr/Documents/workspace-intraedge/aws-mainframe-modernization-carddemo_assessment/previews/wireframe-stages')
        paths = [live / 'stage-0.json', live / 'stage-1.json', live / 'stage-2.json']
        if not all(path.is_file() for path in paths):
            self.skipTest('saved wireframe stages are not on this machine')
        before = [sha(path) for path in paths]
        parts = [json.loads(path.read_text()) for path in paths]
        with self.assertRaisesRegex(app.Blocked, 'conflicting screens definitions for sign-on'):
            app.merge_wireframe_responses(parts)
        self.assertEqual([sha(path) for path in paths], before)

    def test_deferred_package_awaits_acceptance_and_stays_not_implementation_ready(self):
        inner = self.inner
        inner.validated()
        path = inner.work / inner.project['specification']['path']
        spec = app.read(path)
        spec['questions'] = [{'id': 'Q1', 'question': 'Which amount is authoritative?', 'impact': 'Amount handling',
                              'owner': 'SME', 'blocks': 'Amount implementation'}]
        app.write(path, spec)
        inner.project['specification']['sha256'] = sha(path)
        app.persist(inner.work, inner.project)
        roles = []

        def provider(provider_name, run, directory, role, message):
            roles.append(role)
            payload = json.loads(message)
            self.assertIn('owned', payload)
            if payload['stage']['index'] == 1:
                model = inner.screens()
                model['screens'].append({'id': 'sign-on', 'title': 'Sign on', 'purpose': 'Identify the person',
                                         'rule_ids': ['R1'], 'fields': ['User'], 'actions': ['Submit'],
                                         'states': ['Signed on'], 'api_ids': [], 'uncertainties': 'Unproven'})
                model['journeys'][0]['screen_ids'] = ['sign-on', 's1']
                return model
            self.assertIn('sign-on', [item['id'] for item in payload['owned'] if item['kind'] == 'screens'])
            return {'journeys': [], 'screens': [{'id': 'sign-on', 'ref': True}], 'apis': []}

        with patch.object(app, 'model_call', side_effect=provider), \
             patch.object(app, 'assessment', side_effect=AssertionError('assessment')):
            code = app.main(['--workspace', str(inner.work), 'decide', '--question', 'Q1', '--by', 'Owner',
                             '--answer', 'Deferred until the amount owner replies', '--disposition', 'deferred'],
                            reporter=lambda _result: None)
            self.assertEqual(code, 0)
            code = app.main(['--workspace', str(inner.work), 'approve', 'validation', '--by', 'Owner',
                             '--note', 'Reviewed the deferred amount question'], reporter=lambda _result: None)
            self.assertEqual(code, 0)
            self.assertEqual(app.main(['--workspace', str(inner.work), 'design-plan', '--mode', 'functional-parity',
                                       '--by', 'Owner'], reporter=lambda _result: None), 0)
            inner.project = app.read(inner.work / 'project.json')
            inner.project['settings']['max_context_bytes'] = 1
            app.persist(inner.work, inner.project)
            refused = []
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=refused.append)
            self.assertEqual(code, 2)
            self.assertIn('not truncated', refused[-1]['reason'])
            self.assertEqual(app.read(inner.work / 'project.json').get('ui_calls') or 0, 0)
            saved = app.read(inner.work / 'project.json')
            current = app.read(inner.work / saved['specification']['path'])
            protocol = (app.FRAMEWORK / 'prompts/pipeline/wireframes.md').read_text()
            whole = app.wireframe_stages(current, saved['decisions'], 600000, protocol)
            whole[0]['catalog'] = app.wireframe_catalog(current, saved['decisions'])
            import reframe_design
            request = {**app.wireframe_message(current, whole[0], 1, protocol), **reframe_design.message_view(inner.work, saved)}
            fitted = len(json.dumps(request).encode())
            saved['settings']['max_context_bytes'] = fitted - 1
            app.persist(inner.work, saved)
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=lambda _result: None)
            self.assertEqual(code, 0, roles)
            code = app.main(['--workspace', str(inner.work), 'approve', 'specifications', '--by', 'Owner',
                             '--note', 'Reviewed the screens'], reporter=lambda _result: None)
            self.assertEqual(code, 0)
            code = app.main(['--workspace', str(inner.work), 'package'], reporter=lambda _result: None)
        self.assertEqual(code, 0)
        self.assertGreaterEqual(len(roles), 2)
        self.assertTrue(all(role == 'wireframes' for role in roles))
        packaged = app.read(inner.work / 'project.json')
        archive = next((inner.work / 'packages').glob('package-*/ai-dlc.json'))
        record = json.loads(archive.read_text())
        self.assertEqual(record['workflow_status'], 'AWAITING_PACKAGE_ACCEPTANCE')
        self.assertEqual(record['implementation_readiness'], 'BLOCKED_BY_UNRESOLVED_DECISIONS')
        self.assertEqual(record['unresolved_decision_count'], 1)
        self.assertEqual(record['implementation_status'], 'NOT_STARTED')
        self.assertEqual(packaged['stage'], 'AWAITING_PACKAGE_ACCEPTANCE')
        self.assertNotIn('package_acceptance', packaged)
        zip_path = inner.work / packaged['package']['path']
        before = zip_path.read_bytes()
        refused = []
        code = app.main(['--workspace', str(inner.work), 'accept-package', '--sha256', '0' * 64, '--by', 'Owner',
                         '--note', 'Wrong hash'], reporter=refused.append)
        self.assertEqual(code, 2)
        self.assertIn('does not match', refused[-1]['reason'])
        accepted = []
        code = app.main(['--workspace', str(inner.work), 'accept-package', '--sha256', packaged['package']['sha256'],
                         '--by', 'Owner', '--note', 'Accept this conditional handoff for review', '--simulated'],
                        reporter=accepted.append)
        self.assertEqual(code, 0, accepted)
        self.assertEqual(accepted[-1]['status'], 'PACKAGE_ACCEPTED')
        self.assertEqual(accepted[-1]['implementation_readiness'], 'BLOCKED_BY_UNRESOLVED_DECISIONS')
        self.assertTrue(accepted[-1]['simulated'])
        self.assertEqual(zip_path.read_bytes(), before)
        ledger = (inner.work / 'acceptance' / 'ledger.jsonl').read_text().splitlines()
        self.assertEqual(json.loads(ledger[-1])['package_sha256'], packaged['package']['sha256'])
        self.assertNotIn('assess', roles)
        for page in archive.parent.glob('*.html'):
            for href in re.findall(r'href="([^"]+)"', page.read_text()):
                if href.startswith('#') or href.startswith('http'):
                    continue
                self.assertTrue((archive.parent / href.split('#', 1)[0]).is_file(), page.name + ' -> ' + href)


if __name__ == '__main__':
    unittest.main()
