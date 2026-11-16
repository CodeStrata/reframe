"""Menu 1 journeys through every review gate to explicit package acceptance (AC-01, AC-02, AC-27, AC-28, AC-29).

AWS transport and model replies are mocked. Setup, routing, validation, rendering, packaging, and acceptance are not.
Every person in these journeys is a labeled simulated actor; no record here is genuine sign-off.
"""
import json
import os
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import test_docs_consistency as docs
import test_release_acceptance as release
import test_reframe_checkpoints as checkpoint_fixtures
import reframe
import reframe_acceptance as acceptance

FINDINGS = {'program_name': 'PAY', 'all_rules': [{
    'Rule_Id': 'R1', 'Rule_Name': 'Reject zero', 'Rule_Description': 'Reject a zero amount',
    'Acceptance_Criteria': ['Zero is rejected']}]}


class MenuJourneyTests(unittest.TestCase):
    def setUp(self):
        release.ReleaseAcceptanceTests.setUp(self)
        simulated = patch.dict(os.environ, {'REFRAME_SIMULATED_ACTOR': '1'})
        simulated.start()
        self.addCleanup(simulated.stop)

    def model(self):
        helper = checkpoint_fixtures.CheckpointTests('test_default_workflow_reviews_units_then_integrates_and_preserves_human_gate')
        helper.seen = []
        self.state = {'calls': [], 'pause': False}
        return release.review_model(helper, self.state)

    def drive(self, answers):
        code, prompts, console = release.drive(answers, self.model_fn, release.refuse_aws)
        text = '\n'.join(prompts) + '\n' + console
        self.assertEqual(code, 0, text)
        return text

    def test_skip_route_reaches_design_review_package_review_and_explicit_acceptance(self):
        journey = release.MenuJourney(FINDINGS)
        self.model_fn = self.model()
        text = self.drive([
            '1', 'continue',
            'none', 'Ari', 'none',                                   # requirements none, reviewer, baseline context none
            'skip',
            'functional-parity', 'v1', 'java', 'none',              # design plan before the draft
            'guided-draft', 'Ari', 'Trust the sealed findings for this draft', 'codex', 'y',
            'none', 'approve', 'Reviewed the draft screens',         # design review: no context, approve
            'none', 'accept', 'Blake', 'Second reviewer accepts the unverified draft',
            'Accept this draft handoff for stakeholder review',
            '0'])
        project = journey.reload()
        self.assertEqual(project['stage'], 'PACKAGE_ACCEPTED', text)
        self.assertEqual(project['package']['route'], 'skip')
        self.assertEqual(project['package']['verification'], 'SKIPPED_BY_OWNER')
        self.assertEqual(project['design_plan']['mode'], 'functional-parity')
        self.assertEqual(project['design_plan']['target']['language'], 'java')
        self.assertTrue(project['approvals']['design']['simulated'])
        self.assertEqual(project['approvals']['verification-skip']['by'], 'Blake')
        self.assertNotIn('validation', project['approvals'])
        accepted = project['package_acceptance']
        self.assertTrue(accepted['simulated'])
        archive = journey.work / project['package']['path']
        self.assertEqual(accepted['package_sha256'], reframe.sha(archive))
        self.assertTrue(acceptance.verify_ledger(journey.work))
        with zipfile.ZipFile(archive) as bundle:
            names = set(bundle.namelist())
            manifest = json.loads(bundle.read('package-manifest.json'))
            record = json.loads(bundle.read('ai-dlc.json'))
            evidence = json.loads(bundle.read('requirements-evidence.json'))
            context = json.loads(bundle.read('human-context.json'))
            history = json.loads(bundle.read('approval-history.json'))
            plan = json.loads(bundle.read('design-plan.json'))
        self.assertEqual(record['verification'], 'SKIPPED_BY_OWNER')
        self.assertEqual(record['workflow_status'], 'AWAITING_PACKAGE_ACCEPTANCE')
        self.assertNotEqual(record['implementation_readiness'], 'NO_KNOWN_BLOCKERS', 'a skipped validation stays a blocker')
        self.assertNotIn('ledger.jsonl', names)
        self.assertEqual(docs.undocumented(names), [], 'the README package table lists every file')
        self.assertEqual(manifest['route'], 'skip')
        self.assertEqual(manifest['absent'], [], 'every FR-10 item is carried or explained')
        notes = {row['item']: row['note'] for row in manifest['items']}
        self.assertIn('Not independently reviewed', notes['Reviewed business specification and requirement/rule coverage'])
        self.assertEqual(evidence['state'], 'NOT_PROVIDED')
        self.assertTrue(evidence['provenance'])
        self.assertEqual(sorted(context['gates']), ['baseline', 'design'])
        self.assertEqual(sorted(history['current']), ['assessment', 'design'],
                         'the second-person skip acceptance is given at the package gate, after the build')
        entry = json.loads((journey.work / 'acceptance' / 'ledger.jsonl').read_text().splitlines()[-1])
        self.assertEqual(entry['skip_acceptance']['by'], 'Blake')
        self.assertTrue(entry['skip_acceptance']['simulated'])
        self.assertEqual(plan['mode'], 'functional-parity')
        draft = journey.work / project['package']['draft_archive']
        self.assertNotEqual(draft, archive)
        self.assertEqual(reframe.sha(draft), project['package']['draft_sha256'], 'the reviewed draft ZIP is unchanged')
        self.assertIn('Building it did not accept it', text)
        self.assertIn('Implementation readiness', text)
        self.assertEqual(self.state['calls'], ['wireframes'])
        gates = json.loads((journey.work / 'human-review-context' / 'gates.json').read_text())
        self.assertEqual({gate: [e['provided'] for e in entries] for gate, entries in gates.items()},
                         {'baseline': [False], 'design': [False], 'package': [False]})
        self.assertEqual(project['requirements']['state'], 'NOT_PROVIDED')
        (Path(__file__).resolve().parents[1] / 'acceptance-skip-route-transcript.txt').write_text(text + '\n')

    def test_review_route_with_context_feedback_loops_and_exact_acceptance(self):
        import test_requirements as req_fixtures
        journey = release.MenuJourney({'rules': ['reject zero amount']})
        self.model_fn = self.model()
        (journey.root / 'requirements.md').write_text(req_fixtures.REQUIREMENTS_MD)
        (journey.root / 'traceability.yaml').write_text(req_fixtures.TRACEABILITY_YAML)
        baseline_note = journey.root / 'baseline.md'
        baseline_note.write_text('# Zero amounts\nOperations confirms a zero amount is always rejected.\n')
        package_note = journey.root / 'package.md'
        package_note.write_text('# Package review\nShow the rejection reason on the payment screen.\n')
        text = self.drive([
            '1', 'continue',
            'import', str(journey.root / 'requirements.md'), str(journey.root / 'traceability.yaml'), 'F1',
            'Exported from the AWS console by the analyst', 'Ari',
            str(baseline_note), 'clarification', 'R1', 'operations SME', 'accepted',
            'review', 'y',
            'none',                                                   # specification review context
            'y', 'Ari', 'Deferred until the business owner replies',  # defer open questions
            'y', 'Ari', 'Reviewed the specification and decisions',   # approve validation
            'reimagine', 'v1', 'java', 'Keep the nightly batch window',
            'none', 'none', 'design-change', 'Show the rejection reason on the payment screen',
            'none', 'none', 'approve', 'The revised screens show the rejection reason',
            str(package_note), 'review-feedback', 's1', 'business owner', 'accepted',
            'design-change', 'Label the amount field in the currency of the account',
            'none', 'none', 'approve', 'The amount label is correct',
            'none', 'accept', 'Accept this conditional handoff; deferred questions stay blocking',
            '0'])
        project = journey.reload()
        self.assertEqual(project['stage'], 'PACKAGE_ACCEPTED', text)
        self.assertEqual(project['package']['route'], 'review')
        archive = journey.work / project['package']['path']
        self.assertEqual(project['package_acceptance']['package_sha256'], reframe.sha(archive))
        self.assertEqual(project['package_acceptance']['readiness'], 'BLOCKED_BY_UNRESOLVED_DECISIONS')
        self.assertEqual(len(project['design_history']), 2, 'two design feedback loops kept their earlier designs')
        self.assertEqual(project['design_plan']['version'], 'v3')
        self.assertEqual([plan['version'] for plan in project['design_plan_history']], ['v1', 'v2'])
        superseded = [item['phase'] for item in project['approval_history'] if item.get('status') == 'superseded']
        self.assertEqual(superseded.count('specifications'), 1)
        self.assertIn('validation', project['approvals'], 'design feedback keeps the specification approval')
        packages = sorted((journey.work / 'packages').glob('package-*.zip'))
        self.assertEqual(len(packages), 2, 'the first package stays on disk and was never accepted')
        events = [json.loads(line) for line in (journey.work / 'acceptance' / 'ledger.jsonl').read_text().splitlines()]
        self.assertEqual([e['event'] for e in events], ['package_accepted'])
        self.assertEqual(events[0]['package_sha256'], reframe.sha(archive))
        spec = reframe.read(reframe.spec_path(journey.work, project))
        admitted = spec['admitted_inputs']
        self.assertEqual([item['supplied_by'] for item in admitted['human_context']], ['Ari'])
        self.assertEqual(len(admitted['requirement_ids']), 3)
        with zipfile.ZipFile(archive) as bundle:
            names = set(bundle.namelist())
            evidence = json.loads(bundle.read('requirements-evidence.json'))
            context = json.loads(bundle.read('human-context.json'))
            ai = json.loads(bundle.read('ai-dlc.json'))
            deltas = json.loads(bundle.read('deltas.json'))
            manifest = json.loads(bundle.read('package-manifest.json'))
        self.assertEqual(evidence['manifest']['origin'], 'imported')
        self.assertIn('Reframe did not generate them', evidence['provenance'])
        self.assertIn('requirements-F1-requirements.md', names)
        self.assertEqual(sorted(context['gates']), ['baseline', 'design', 'package', 'specification'])
        self.assertTrue(any(item['category'] == 'review-feedback' for item in context['submissions']))
        self.assertEqual(ai['workflow_status'], 'AWAITING_PACKAGE_ACCEPTANCE')
        self.assertEqual(deltas['proposals'], [], 'no future-state expectation was supplied, so nothing is proposed')
        self.assertTrue(deltas['gaps'])
        self.assertTrue({'design-plan.json', 'design-inventory.json', 'api-completeness.json', 'future-state.html'} <= names)
        self.assertEqual(manifest['absent'], [])
        self.assertNotIn('ledger.jsonl', names)
        self.assertEqual(docs.undocumented(names), [], 'the README package table lists every file')
        self.assertTrue((journey.work / 'previews' / 'wireframe-stages-archive').is_dir())
        (Path(__file__).resolve().parents[1] / 'acceptance-review-route-transcript.txt').write_text(text + '\n')


if __name__ == '__main__':
    unittest.main()
