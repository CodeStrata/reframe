"""Package review, explicit acceptance, ledger integrity, and readiness (AC-28, AC-29, AC-30; #187, #188, #190). L1."""
import json
import unittest
from pathlib import Path

import test_reframe as fixtures
import reframe as app
import reframe_acceptance as acceptance
import pilot
from pilot import Blocked


HELPERS = {name: value for name, value in vars(fixtures.PreparationTests).items()
           if callable(value) and not name.startswith('test')}


class AcceptanceTests(unittest.TestCase):
    locals().update(HELPERS)

    def built(self):
        self.site()
        self.approve('specifications')
        return app.package(self.work, self.project)

    def test_generation_awaits_acceptance_and_never_claims_it(self):
        result = self.built()
        self.assertEqual(result['status'], 'AWAITING_PACKAGE_ACCEPTANCE')
        self.assertNotIn('package_acceptance', self.project)
        self.assertEqual(self.project['package']['status'], 'AWAITING_PACKAGE_ACCEPTANCE')
        self.assertTrue(self.project['package']['version_id'])
        import zipfile
        with zipfile.ZipFile(result['archive']) as archive:
            record = json.loads(archive.read('ai-dlc.json'))
        self.assertEqual(record['workflow_status'], 'AWAITING_PACKAGE_ACCEPTANCE')
        self.assertNotIn('PACKAGE_ACCEPTED', json.dumps(record))

    def test_review_lists_inventory_hash_basis_and_readiness(self):
        result = self.built()
        detail = acceptance.review(self.work, self.project, app)
        self.assertEqual(detail['sha256'], result['sha256'])
        names = {item['name'] for item in detail['inventory']}
        self.assertTrue({'ai-dlc.json', 'specification.json', 'checksums.json'} <= names)
        self.assertEqual({item['phase'] for item in detail['approval_basis']}, {'assessment', 'validation', 'specifications'})
        self.assertIn(detail['readiness']['state'], {'BLOCKED_BY_UNRESOLVED_DECISIONS', 'PARTIALLY_READY', 'NO_KNOWN_BLOCKERS'})
        self.assertFalse(detail['acceptance'])

    def test_acceptance_names_the_exact_hash_and_leaves_the_archive_unchanged(self):
        result = self.built()
        archive = Path(result['archive'])
        before = archive.read_bytes()
        with self.assertRaisesRegex(Blocked, 'does not match'):
            acceptance.accept(self.work, self.project, app, 'f' * 64, 'Owner', 'Reviewed')
        with self.assertRaisesRegex(Blocked, 'Acceptance note'):
            acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'YOUR_REASON')
        entry = acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the inventory and gaps')
        self.assertEqual(self.project['stage'], 'PACKAGE_ACCEPTED')
        self.assertEqual(entry['package_sha256'], result['sha256'])
        self.assertEqual(archive.read_bytes(), before)
        self.assertNotIn('acceptance', ' '.join(n for n in __import__('zipfile').ZipFile(archive).namelist()))
        self.assertTrue(acceptance.verify_ledger(self.work))

    def test_a_changed_archive_cannot_be_reviewed_or_accepted(self):
        result = self.built()
        Path(result['archive']).write_bytes(Path(result['archive']).read_bytes() + b' ')
        with self.assertRaisesRegex(Blocked, 'changed after it was built'):
            acceptance.review(self.work, self.project, app)

    def test_a_tampered_ledger_is_detected(self):
        result = self.built()
        acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the package')
        ledger = self.work / 'acceptance' / 'ledger.jsonl'
        entry = json.loads(ledger.read_text().splitlines()[0])
        entry['by'] = 'Someone else'
        ledger.write_text(json.dumps(entry) + '\n')
        with self.assertRaisesRegex(Blocked, 'ledger'):
            acceptance.verify_ledger(self.work)

    def test_withdrawal_keeps_the_ledger_and_moves_acceptance_to_history(self):
        result = self.built()
        acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the package')
        acceptance.withdraw(self.work, self.project, 'package_feedback')
        self.assertNotIn('package_acceptance', self.project)
        self.assertEqual(self.project['acceptance_history'][-1]['reason'], 'package_feedback')
        events = [json.loads(line)['event'] for line in (self.work / 'acceptance' / 'ledger.jsonl').read_text().splitlines()]
        self.assertEqual(events, ['package_accepted', 'acceptance_superseded'])
        self.assertTrue(acceptance.verify_ledger(self.work))

    def save_spec(self, spec_file, spec):
        app.write(spec_file, spec)
        self.project['specification']['sha256'] = pilot.sha(spec_file)

    def test_readiness_never_follows_from_empty_decisions(self):
        self.built()
        spec_file = app.spec_path(self.work, self.project)
        spec = app.read(spec_file)
        state = acceptance.readiness(self.work, self.project, app)
        if spec.get('questions'):
            self.assertEqual(state['state'], 'BLOCKED_BY_UNRESOLVED_DECISIONS')
        self.project['decisions'] = {}
        spec['questions'] = [{'id': 'QX', 'question': 'Open', 'impact': 'i', 'owner': 'o', 'blocks': 'b'}]
        self.save_spec(spec_file, spec)
        state = acceptance.readiness(self.work, self.project, app)
        self.assertEqual(state['state'], 'BLOCKED_BY_UNRESOLVED_DECISIONS')
        self.assertIn({'kind': 'decision', 'id': 'QX', 'state': 'unrecorded', 'blocks': 'b'}, state['blockers'])
        self.project['decisions'] = {'QX': {'disposition': 'deferred'}}
        self.assertEqual(acceptance.readiness(self.work, self.project, app)['state'], 'BLOCKED_BY_UNRESOLVED_DECISIONS')
        self.project['decisions'] = {'QX': {'disposition': 'resolved'}}
        spec['coverage'] = [{'id': 'R1', 'kind': 'rule', 'disposition': 'mapped', 'gaps': ['test']}]
        self.save_spec(spec_file, spec)
        state = acceptance.readiness(self.work, self.project, app)
        self.assertEqual(state['state'], 'PARTIALLY_READY')
        self.assertTrue(any(b['kind'] == 'coverage' for b in state['blockers']))

    def test_a_skipped_route_needs_the_documented_second_acceptance(self):
        result = self.built()
        self.project['verification_skip'] = {'owner': 'Fixture owner', 'reason': 'r', 'assessment_sha256': 'x'}
        with self.assertRaisesRegex(Blocked, 'second acceptance'):
            acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the package')


if __name__ == '__main__':
    unittest.main()
