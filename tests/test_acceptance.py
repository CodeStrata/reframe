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

    def test_a_copied_recovery_hint_is_refused_as_a_name_or_rationale(self):
        self.validated()
        for by, note in (('NAME', 'Reviewed the report'), ('Owner', 'WHY'), ('Owner', ' RATIONALE ')):
            with self.assertRaisesRegex(Blocked, 'instructional placeholder'):
                app.approve(self.work, self.project, self.args('approve', 'validation', '--by', by, '--note', note))
        self.assertNotIn('validation', self.project['approvals'])
        self.assertIsNone(app.instructional_placeholder('Why the NAME field is optional was reviewed'))

    def test_a_copied_recovery_hint_cannot_accept_a_package(self):
        result = self.built()
        for by, note in (('NAME', 'Reviewed the inventory'), ('Owner', 'WHY')):
            with self.assertRaisesRegex(Blocked, 'instructional placeholder'):
                acceptance.accept(self.work, self.project, app, result['sha256'], by, note)
        self.assertNotIn('package_acceptance', self.project)
        self.assertIn('--by NAME --note WHY', result['next_step'])

    def test_context_admitted_after_the_build_needs_a_rebuild_before_acceptance(self):
        import reframe_optional as optional
        first = self.built()
        note = self.work / 'package-note.md'
        note.write_text('# Package review\nShow the rejection reason on the amount screen.\n')
        record = optional.import_context(self.work, note, 'Owner', 'business owner', 'review-feedback', ['s1'], 'package')
        optional.decide_context(self.work, record['id'], 'accepted', 'Owner', 'Admitted at the package gate')
        with self.assertRaisesRegex(Blocked, 'changed after this package was built'):
            acceptance.accept(self.work, self.project, app, first['sha256'], 'Owner', 'Reviewed the inventory')
        self.assertNotIn('package_acceptance', self.project)
        second = app.package(self.work, self.project)
        self.assertNotEqual(second['archive'], first['archive'])
        self.assertTrue(Path(first['archive']).is_file(), 'the earlier package stays on disk')
        import zipfile
        with zipfile.ZipFile(second['archive']) as bundle:
            submissions = json.loads(bundle.read('human-context.json'))['submissions']
        self.assertIn(record['id'], [item['id'] for item in submissions])
        entry = acceptance.accept(self.work, self.project, app, second['sha256'], 'Owner', 'Reviewed the rebuilt package')
        self.assertEqual(entry['package_sha256'], second['sha256'])

    def test_status_after_acceptance_is_consistent(self):
        result = self.built()
        acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the inventory and gaps')
        app.persist(self.work, self.project)
        reports = []
        self.assertEqual(app.main(['--workspace', str(self.work), 'status'], reporter=reports.append), 0)
        status = reports[-1]
        self.assertEqual(status['last_local_action'], 'package_accepted')
        self.assertEqual(status['summary']['implementation_blockers_total'], status['readiness']['blocker_count'])
        self.assertEqual(status['summary']['package'], 'PACKAGE_ACCEPTED')
        import zipfile
        with zipfile.ZipFile(result['archive']) as bundle:
            coverage = json.loads(bundle.read('rule-coverage.json'))
        self.assertEqual(sum(coverage['dispositions'].values()), coverage['rule_count'])
        self.assertIn('Dispositions are counted separately', coverage['status_meaning'])

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

    def test_an_api_contract_gap_alone_keeps_the_package_from_no_known_blockers(self):
        result = self.built()
        import zipfile
        with zipfile.ZipFile(result['archive']) as archive:
            record = json.loads(archive.read('ai-dlc.json'))
        report = app.read(self.work / self.project['site']['directory'] / 'api-completeness.json')
        gaps = [(row['id'], row['gaps']) for row in report['rows'] if row['state'] == 'gap']
        self.assertTrue(gaps, 'the fixture design has a named API gap')
        self.assertEqual([(b['id'], b['gaps']) for b in record['implementation_blockers'] if b['kind'] == 'api_contract'], gaps,
                         'the package names each API gap as an implementation blocker')
        self.assertTrue(any(b['kind'] == 'api_contract' for b in acceptance.review(self.work, self.project, app)['readiness']['blockers']))
        # Every other blocker cleared: the API gap alone keeps the package from NO_KNOWN_BLOCKERS.
        spec_file = app.spec_path(self.work, self.project)
        spec = app.read(spec_file)
        for key in ('coverage', 'requirement_coverage', 'test_templates'):
            spec.pop(key, None)
        self.project['decisions'] = {q['id']: {'disposition': 'resolved'} for q in spec.get('questions') or []}
        self.save_spec(spec_file, spec)
        state = acceptance.readiness(self.work, self.project, app)
        self.assertEqual(state['state'], 'PARTIALLY_READY')
        self.assertEqual({b['kind'] for b in state['blockers']}, {'api_contract'})

    def import_pay_999(self):
        import reframe_requirements as requirements
        folder = self.root / 'requirements-change'
        folder.mkdir(exist_ok=True)
        (folder / 'requirements.md').write_text('# Payments\n- PAY-999: The system SHALL require a second approver.\n')
        return requirements.import_files(self.work, self.project, folder / 'requirements.md', None, 'F1', 'Analyst',
                                         'New rule from the business owner')

    def test_a_requirements_import_after_the_build_retires_the_package_and_refuses_its_acceptance(self):
        result = self.built()
        self.import_pay_999()
        self.assertEqual(self.project['stage'], 'REVISION_PENDING', 'validation runs again against the new requirements')
        self.assertNotIn('package', self.project)
        retired = self.project['package_history'][-1]
        self.assertEqual((retired['sha256'], retired['status']), (result['sha256'], 'SUPERSEDED'))
        self.assertTrue(Path(result['archive']).is_file(), 'the earlier package stays on disk')
        with self.assertRaises(Blocked):
            acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the package')
        self.assertNotIn('package_acceptance', self.project)

    def test_a_requirements_import_after_acceptance_withdraws_it_and_keeps_the_ledger(self):
        result = self.built()
        acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the package')
        self.import_pay_999()
        self.assertNotIn('package_acceptance', self.project)
        self.assertEqual(self.project['acceptance_history'][-1]['reason'], 'requirements_imported')
        events = [entry['event'] for entry in acceptance._ledger_entries(self.work)]
        self.assertEqual(events, ['package_accepted', 'acceptance_superseded'])
        self.assertTrue(acceptance.verify_ledger(self.work))
        self.assertEqual(self.project['stage'], 'REVISION_PENDING')

    def test_a_package_whose_approval_basis_was_superseded_cannot_be_accepted(self):
        result = self.built()
        # The state the audited develop left after an import: approvals superseded, the old package still current.
        import reframe_versions as versions
        versions.supersede(self.project, ('validation', 'specifications'), 'requirements_imported')
        with self.assertRaisesRegex(Blocked, 'missing approval: specifications'):
            acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the package')
        self.assertNotIn('package_acceptance', self.project)

    def test_a_package_records_its_inputs_and_a_changed_input_blocks_acceptance(self):
        result = self.built()
        inputs = self.project['package']['inputs']
        self.assertEqual(inputs['specification_sha256'], self.project['specification']['sha256'])
        self.assertEqual(set(inputs['approvals']), {'assessment', 'validation', 'specifications'})
        self.project['requirements'] = {'set_id': 'later-set'}
        with self.assertRaisesRegex(Blocked, 'changed: requirements_set'):
            acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the package')

    def test_a_skipped_route_needs_the_documented_second_acceptance(self):
        result = self.built()
        self.project['verification_skip'] = {'owner': 'Fixture owner', 'reason': 'r', 'assessment_sha256': 'x'}
        with self.assertRaisesRegex(Blocked, 'second acceptance'):
            acceptance.accept(self.work, self.project, app, result['sha256'], 'Owner', 'Reviewed the package')


if __name__ == '__main__':
    unittest.main()
