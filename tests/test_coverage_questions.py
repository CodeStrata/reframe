"""Structured coverage, placeholder test templates, and SME question views (FR-06; AC-19; #179, #180). L1."""
import io
import json
import unittest
from contextlib import redirect_stdout

import test_m1_contracts as m1
import test_requirements as req_fixtures
import reframe as app
import reframe_acceptance as acceptance
import reframe_coverage as coverage
import reframe_requirements as requirements


SPEC = {
    'sections': {'ui': {'rule_ids': ['R1'], 'requirement_ids': ['aws-req:F1:PAY-001'],
                        'specification': 'PAY-002 is handled here too, in prose only.'}},
    'work_items': [{'id': 'W1', 'rule_ids': ['R1'], 'requirement_ids': ['aws-req:F1:PAY-001']}],
    'tests': [{'id': 'T1', 'rule_id': 'R1', 'requirement_ids': ['aws-req:F1:PAY-001'], 'preconditions': 'Account open',
               'inputs': 'Amount 0', 'expected': 'Rejected', 'oracle': 'Legacy screen message', 'status': 'NOT RUN'},
              {'id': 'T2', 'rule_id': 'R1', 'status': 'NOT RUN', 'description': 'Check zero'}],
    'excluded_requirements': {'aws-req:F1:PAY-003': 'Audit logging is out of the selected scope'},
    'questions': [
        {'id': 'Q1', 'question': 'Is zero ever valid?', 'owner': 'SME', 'impact': 'Amount', 'blocks': 'Payment API', 'rule_ids': ['R1']},
        {'id': 'Q2', 'question': 'Can zero be retried?', 'owner': 'SME', 'impact': 'Retry', 'blocks': 'payment api', 'rule_ids': ['R1']},
        {'id': 'Q3', 'question': 'Who closes accounts?', 'owner': 'Ops', 'impact': 'Closure', 'blocks': 'Batch', 'rule_ids': []}],
}


class CoverageTests(unittest.TestCase):
    def test_prose_never_maps_and_exclusions_need_a_reason(self):
        rows = {row['id']: row for row in coverage.requirement_coverage(
            SPEC, ['aws-req:F1:PAY-001', 'aws-req:F1:PAY-002', 'aws-req:F1:PAY-003'])}
        self.assertEqual(rows['aws-req:F1:PAY-001']['disposition'], 'mapped')
        self.assertEqual(rows['aws-req:F1:PAY-002']['disposition'], 'gap', 'prose naming PAY-002 is not a mapping')
        self.assertEqual(rows['aws-req:F1:PAY-002']['gaps'], ['sections', 'work_items', 'tests'])
        self.assertEqual(rows['aws-req:F1:PAY-003']['disposition'], 'excluded')
        self.assertIn('out of the selected scope', rows['aws-req:F1:PAY-003']['reason'])

    def test_tests_stay_placeholders_until_concrete(self):
        rows = {row['id']: row for row in coverage.test_templates(SPEC)}
        self.assertEqual(rows['T1']['state'], 'CONCRETE')
        self.assertEqual(rows['T2']['state'], 'PLACEHOLDER')
        self.assertEqual(rows['T2']['missing'], ['preconditions', 'inputs', 'expected', 'oracle'])
        self.assertTrue(all(row['execution'] == 'NOT RUN' for row in rows.values()))

    def test_question_filters_use_recorded_fields_and_groups_never_merge(self):
        rows = coverage.question_rows(SPEC, {'Q3': {'disposition': 'deferred'}})
        self.assertEqual([r['id'] for r in coverage.filter_questions(rows, owner='SME')], ['Q1', 'Q2'])
        self.assertEqual([r['id'] for r in coverage.filter_questions(rows, state='deferred')], ['Q3'])
        self.assertEqual([r['id'] for r in coverage.filter_questions(rows, rule='R1')], ['Q1', 'Q2'])
        self.assertEqual(coverage.filter_questions(rows, severity='high'), [], 'severity is not recorded, so nothing matches')
        groups = coverage.suggested_groups(rows)
        self.assertEqual(groups, [{'owner': 'SME', 'blocks': 'payment api', 'rule_ids': ['R1'], 'question_ids': ['Q1', 'Q2'],
                                   'basis': 'same owner, blocked work, and rule ids; questions stay separate'}])
        self.assertEqual(len(rows), 3, 'grouping keeps every question')
        self.assertEqual(coverage.summary(rows)['by_state'], {'open': 2, 'deferred': 1})


class CoverageInWorkflowTests(m1.WorkspaceFixture):
    def test_validation_records_requirement_coverage_and_readiness_counts_its_gaps(self):
        folder = self.root / 'external'
        folder.mkdir()
        (folder / 'requirements.md').write_text(req_fixtures.REQUIREMENTS_MD)
        requirements.import_files(self.work, self.project, folder / 'requirements.md', None, 'F1', 'Analyst', 'Console export')
        result = app.pipeline(self.work, self.project, self.args('validate'), self.runtime)
        self.assertEqual(result['status'], 'AWAITING_VALIDATION_APPROVAL')
        spec = app.read(app.spec_path(self.work, self.project))
        self.assertEqual([row['id'] for row in spec['requirement_coverage']],
                         ['aws-req:F1:PAY-001', 'aws-req:F1:PAY-002', 'aws-req:F1:PAY-003'])
        self.assertTrue(all(row['disposition'] == 'gap' for row in spec['requirement_coverage']),
                        'the fixture specification maps no requirement, and nothing pretends it does')
        self.assertTrue(spec['test_templates'])
        blockers = acceptance.readiness(self.work, self.project, app)['blockers']
        self.assertTrue(any(b['kind'] == 'coverage' and b['id'] == 'aws-req:F1:PAY-002' for b in blockers))

    def test_the_questions_command_lists_filters_and_suggests_groups(self):
        app.pipeline(self.work, self.project, self.args('validate'), self.runtime)
        app.persist(self.work, self.project)
        out = io.StringIO()
        with redirect_stdout(out):
            code = app.main(['--workspace', str(self.work), 'questions', '--state', 'open', '--groups'])
        self.assertEqual(code, 0)
        result = json.loads(out.getvalue())
        self.assertEqual(result['summary']['total'], result['selected'])
        self.assertIn('suggested_groups', result)


if __name__ == '__main__':
    unittest.main()
