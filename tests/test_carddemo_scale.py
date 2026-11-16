"""Saved-size and near-threshold wireframe requests (NR-03; AC-20; spec §10 items 12 and 18). L1.

Uses the sanitized generated fixture in carddemo_scale.py, so the checks run on any machine.
"""
import json
import unittest
from unittest.mock import patch

import carddemo_scale as scale
import test_reframe as fixtures
import reframe as app

LIMIT = 180000
PROTOCOL = 'Wireframe protocol fixture.'


def _ids(stages, kind):
    return [ident for stage in stages for ident in stage[kind]]


def _message(spec, stage, count, extra=None):
    return json.dumps({**app.wireframe_message(spec, stage, count, PROTOCOL), **(extra or {})})


class SavedSizeStagingTests(unittest.TestCase):
    def setUp(self):
        self.spec = scale.specification()
        self.decisions = scale.decisions()

    def test_the_fixture_is_at_saved_carddemo_scale(self):
        legacy = json.dumps({'protocol': PROTOCOL, 'specification': self.spec, 'decisions': self.decisions})
        self.assertGreater(len(legacy.encode()), 600000)
        self.assertEqual(len(self.spec['questions']), 452)
        self.assertEqual(len(self.decisions), 54)

    def test_a_saved_size_request_is_staged_complete_and_untruncated(self):
        stages = app.wireframe_stages(self.spec, self.decisions, LIMIT, PROTOCOL)
        self.assertGreater(len(stages), 2)
        for stage in stages:
            message = _message(self.spec, stage, len(stages))
            self.assertLessEqual(len(message.encode()), LIMIT - 8192, 'room is kept for the owned-id list')
            payload = json.loads(message)
            self.assertEqual(len(payload['decisions']), 452, 'every stage sees every decision state')
            self.assertEqual(sum(1 for item in payload['decisions'] if item['disposition'] == 'deferred'), 54)
        for kind, records in (('rules', self.spec['rules']), ('questions', self.spec['questions']),
                              ('evidence', self.spec['assessment_evidence']), ('coverage', self.spec['coverage'])):
            placed = _ids(stages, kind)
            self.assertEqual(sorted(placed), sorted(item['id'] for item in records), kind)
            self.assertEqual(len(placed), len(set(placed)), kind + ' are placed once')
        self.assertEqual(sorted(_ids(stages, 'sections')), sorted(scale.SECTIONS))
        sent = {}
        for stage in stages:
            for rule in json.loads(_message(self.spec, stage, len(stages)))['specification']['rules']:
                sent[rule['id']] = rule['statement']
                self.assertTrue(rule['source_path'] and rule['source_anchor'], 'evidence links travel with each rule')
        self.assertEqual(sent, {rule['id']: rule['statement'] for rule in self.spec['rules']},
                         'every statement reaches a provider request byte for byte')

    def test_the_design_context_is_counted_when_packing(self):
        extra = {'design_plan': {'mode': 'reimagine', 'constraints': [scale.text(9, 2000)]}}
        stages = app.wireframe_stages(self.spec, self.decisions, LIMIT, PROTOCOL, extra)
        for stage in stages:
            self.assertLessEqual(len(_message(self.spec, stage, len(stages), extra).encode()), LIMIT - 8192)
        self.assertGreater(len(stages), len(app.wireframe_stages(self.spec, self.decisions, LIMIT, PROTOCOL)) - 1)


class NearThresholdTests(unittest.TestCase):
    """One record sized to the exact byte budget fits; one byte more is refused, not truncated."""
    limit = 50000

    def spec(self, length):
        return {'sections': {}, 'rules': [{'id': 'R1', 'statement': 'x' * length}], 'questions': [],
                'assessment_evidence': [], 'coverage': []}

    def size(self, length):
        spec = self.spec(length)
        stage = {'index': 0, 'sections': [], 'rules': ['R1'], 'questions': [], 'evidence': [], 'coverage': [],
                 'catalog': app.wireframe_catalog(spec, {})}
        return len(_message(spec, stage, 99).encode())

    def exact(self):
        budget = self.limit - 8192
        length = 1000 + budget - self.size(1000)
        self.assertEqual(self.size(length), budget)
        return length

    def test_a_record_at_the_exact_budget_fits_in_one_stage(self):
        length = self.exact()
        stages = app.wireframe_stages(self.spec(length), {}, self.limit, PROTOCOL)
        self.assertEqual(len(stages), 1)
        self.assertEqual(stages[0]['rules'], ['R1'])

    def test_one_byte_over_is_refused_with_both_sizes(self):
        length = self.exact() + 1
        with self.assertRaises(app.Blocked) as raised:
            app.wireframe_stages(self.spec(length), {}, self.limit, PROTOCOL)
        message = str(raised.exception)
        self.assertIn('It was not truncated', message)
        self.assertIn(str(self.limit) + ' bytes', message)
        self.assertIn('R1', message)

    def test_two_records_that_each_fit_are_split_not_dropped(self):
        half = (self.exact() - 200) // 2
        spec = self.spec(half)
        spec['rules'].append({'id': 'R2', 'statement': 'y' * (half + 400)})
        stages = app.wireframe_stages(spec, {}, self.limit, PROTOCOL)
        self.assertEqual([stage['rules'] for stage in stages], [['R1'], ['R2']])


class PreDispatchCounterTests(unittest.TestCase):
    """An oversized request stops before the call counter, output folder, or provider (spec §10 item 18)."""

    def setUp(self):
        self.inner = fixtures.PreparationTests('test_missing_sme_decision_blocks_validation_approval')
        self.inner.setUp()
        self.addCleanup(self.inner.doCleanups)

    def test_one_byte_over_through_the_cli_spends_nothing(self):
        inner = self.inner
        inner.validated()
        path = inner.work / inner.project['specification']['path']
        spec = app.read(path)
        spec['rules'][0]['statement'] = 'x' * (app.wireframe_limit(inner.project) + 1)
        app.write(path, spec)
        inner.project['specification']['sha256'] = app.sha(path)
        app.preparation_report(inner.work, inner.project)
        app.persist(inner.work, inner.project)
        inner.approve('validation')
        before = app.read(inner.work / 'project.json')
        results = []
        with patch.object(app, 'model_call', side_effect=AssertionError('provider called')):
            code = app.main(['--workspace', str(inner.work), 'review-site'], reporter=results.append)
        self.assertNotEqual(code, 0)
        self.assertIn('not truncated', json.dumps(results))
        after = app.read(inner.work / 'project.json')
        self.assertEqual(after.get('ui_calls') or 0, before.get('ui_calls') or 0)
        self.assertEqual(after['pipeline']['calls'], before['pipeline']['calls'])
        self.assertFalse(any((inner.work / 'previews').glob('business-*')))


if __name__ == '__main__':
    unittest.main()
