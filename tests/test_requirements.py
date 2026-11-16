"""AWS requirements boundary (L1/L2 offline). The transport is a labeled fixture; its schemas are synthetic.

These tests show the adapter honors whatever tool and task schemas a server reports, stops when evidence is
missing, and labels fixture output as offline-fixture. They are not evidence that AWS supports any operation.
"""
import argparse
import io
import json
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import test_reframe as fixtures
import reframe as app
import reframe_requirements as requirements
import reframe_states as states
from pilot import Blocked

REQUIREMENTS_MD = """# Payment authorization

## Global preconditions
- The account exists.

## Workflow 1: Authorize a payment
As a cardholder I want a payment authorized.
- PAY-001: WHEN the amount is zero THE system SHALL reject the payment.
- PAY-002: WHEN the account is closed THE system SHALL reject the payment.
- PAY-003: The system SHALL record every rejection.
"""
TRACEABILITY_YAML = """PAY-001:
  rules: [R1]
  source: rule.cbl
PAY-002:
  rules: [R9]
"""

SCHEMAS = {  # Synthetic fixture schemas. They are not copied from AWS.
    'create_job': {'type': 'object', 'required': ['workspaceId', 'jobName', 'objective'],
                   'properties': {'workspaceId': {}, 'jobName': {}, 'objective': {}, 'intent': {}, 'orchestratorAgent': {}}},
    'load_instructions': {'type': 'object', 'properties': {'workspaceId': {}, 'jobId': {}}},
    'get_job_status': {'type': 'object', 'properties': {'workspaceId': {}, 'jobId': {}, 'detailed': {}}},
    'send_message': {'type': 'object', 'properties': {'workspaceId': {}, 'jobId': {}, 'text': {}}},
    'complete_task': {'type': 'object', 'properties': {'workspaceId': {}, 'jobId': {}, 'taskId': {}, 'content': {}, 'action': {}}},
    'list_resources': {'type': 'object', 'properties': {'workspaceId': {}, 'jobId': {}, 'resource': {'enum': ['artifacts', 'connectors']},
                                                         'pathPrefix': {}}},
    'get_resource': {'type': 'object', 'properties': {'workspaceId': {}, 'jobId': {}, 'resource': {}, 'taskId': {},
                                                       'assetKey': {}, 'connectorId': {}, 'savePath': {}, 'fileName': {}}},
}


class FakeTransform:
    """Offline transport. fixture=True makes every observation offline-fixture evidence."""
    fixture = True

    def __init__(self, plan_steps=('Analyze code', 'Extract business logic', 'Generate requirements'), connector='NEPTUNE_REIMAGINE',
                 task=None, fail_create=False):
        self.calls_seen = []
        self.plan_steps = list(plan_steps)
        self.connector = connector
        self.task = task if task is not None else {
            'taskId': 'T1', 'status': 'AWAITING_HUMAN_INPUT', 'title': 'Select business functions to reimagine',
            '_outputSchema': {'type': 'object', 'properties': {'functions': {'type': 'array', 'items': {'enum': ['F1', 'F2']}}}}}
        self.fail_create = fail_create
        self.generated = False
        self.selected = None

    def tools(self):
        return [{'name': name, 'inputSchema': schema} for name, schema in SCHEMAS.items()]

    def calls(self, requests):
        results = []
        for name, arguments in requests:
            self.calls_seen.append((name, arguments))
            if name == 'create_job':
                if self.fail_create:
                    raise Blocked('AWS MCP transport failed; inspect the private mcp-error.json and reconcile uncertain creation')
                results.append({'job': {'jobId': 'job-req-1'}})
            elif name == 'list_resources' and arguments.get('resource') == 'connectors':
                results.append({'connectors': [{'connectorId': 'c1', 'connectorType': self.connector, 'status': 'ACTIVE'}]})
            elif name == 'get_job_status':
                status = 'SUCCEEDED' if self.selected else 'IN_PROGRESS'
                steps = [{'stepName': step, 'status': ('SUCCEEDED' if self.selected or step != 'Generate requirements' else 'PENDING')}
                         for step in self.plan_steps]
                tasks = [] if self.selected or not self.task else [self.task]
                results.append({'job': {'jobId': 'job-req-1', 'status': status}, 'plan': {'steps': steps},
                                'tasks': {'hitlTasks': tasks}})
            elif name == 'get_resource' and arguments.get('resource') == 'task':
                results.append({'task': self.task})
            elif name == 'complete_task':
                self.selected = json.loads(arguments['content'])
                results.append({'status': 'ACCEPTED'})
            elif name == 'list_resources':
                results.append({'connectorId': 'c1', 'folders': [], 'artifacts': [], 'assets': [
                    {'assetKey': 'transform-output/job-req-1/F1/requirements.md', 'sizeInBytes': 10},
                    {'assetKey': 'transform-output/job-req-1/F1/traceability.yaml', 'sizeInBytes': 10}]})
            elif name == 'get_resource' and arguments.get('resource') == 'asset':
                body = REQUIREMENTS_MD if arguments['assetKey'].endswith('.md') else TRACEABILITY_YAML
                Path(arguments['savePath'], arguments['fileName']).write_text(body)
                results.append({'saved': True})
            else:
                results.append({})
        return results


class RequirementsTests(unittest.TestCase):
    args = fixtures.PreparationTests.args
    assess = fixtures.PreparationTests.assess
    approve = fixtures.PreparationTests.approve
    baseline = fixtures.PreparationTests.baseline
    spec = fixtures.PreparationTests.spec

    def setUp(self):
        fixtures.PreparationTests.setUp(self)
        self.baseline()
        self.project['settings']['transform']['workspace_id'] = 'ws-fixture'
        self.project['aws'] = {'profile': 'fixture-profile', 'region': 'us-east-1'}
        record = self.project['assessments'][self.project['selected']]
        run = app.read(Path(record['directory']) / 'run.json')
        run['uploaded_source'] = {'uri': 's3://fixture-bucket/reframe/run-1/source.zip', 'sha256': '0' * 64}
        app.write(Path(record['directory']) / 'run.json', run)
        app.persist(self.work, self.project)

    def command(self, *values, client=None):
        args = app.parser().parse_args(['--workspace', str(self.work), 'requirements', *values])
        return app.requirements_command(self.work, self.project, args, client)

    def discover(self, client):
        return self.command('discover', '--by', 'Owner', '--note', 'Read-only fixture discovery', client=client)

    def test_without_discovery_generation_is_unavailable_and_nothing_is_generated(self):
        status = self.command('status')
        self.assertEqual(status['status'], 'REQUIREMENTS_GENERATION_UNAVAILABLE')
        self.assertEqual(status['cause'], 'REQUIREMENTS_GENERATION_UNAVAILABLE')
        self.assertEqual(set(status['missing']), {'operations', 'connector', 'identity'})
        self.assertIn('Documentation alone is not verification', status['reason'])
        self.assertTrue(all(item['documented'] for item in status['items'].values()))
        self.assertFalse(any(item['account_verified'] for item in status['items'].values()))
        with self.assertRaises(Blocked) as raised:
            self.command('authorize-job', '--functions', 'F1', '--by', 'Owner', '--note', 'Pilot')
        self.assertEqual(states.describe(raised.exception)['cause'], 'REQUIREMENTS_GENERATION_UNAVAILABLE')
        self.assertFalse((self.work / 'requirements' / 'sets').exists())
        self.assertNotIn('manifest', self.project.get('requirements') or {})
        self.assertIn('Business-rule extraction is not requirements', requirements.provenance_statement(self.work, self.project))

    def test_a_server_without_a_reimagine_connector_stays_unavailable(self):
        self.discover(FakeTransform(connector='S3'))
        status = self.command('status')
        self.assertEqual(status['status'], 'REQUIREMENTS_GENERATION_UNAVAILABLE')
        self.assertEqual(status['missing'], ['connector'])

    def test_fixture_generation_selects_from_the_schema_and_preserves_originals(self):
        client = FakeTransform()
        discovered = self.discover(client)
        self.assertEqual(discovered['evidence_level'], 'offline-fixture')
        self.command('authorize-job', '--functions', 'F1', '--by', 'Owner', '--note', 'Generate F1 for the pilot', client=client)
        first = self.command('resume', client=client)
        self.assertEqual(first['job_id'], 'job-req-1')
        create = [arguments for name, arguments in client.calls_seen if name == 'create_job']
        self.assertEqual(len(create), 1)
        self.assertIn('s3://fixture-bucket/reframe/run-1/source.zip', create[0]['objective'])
        completed = [json.loads(arguments['content']) for name, arguments in client.calls_seen if name == 'complete_task']
        self.assertEqual(completed, [{'functions': ['F1']}])
        second = self.command('resume', client=client)
        self.assertEqual(second['status'], 'REQUIREMENTS_RETRIEVED')
        self.assertEqual(second['evidence_level'], 'offline-fixture')
        self.assertTrue(second['completion']['job_terminal'])
        self.assertTrue(second['completion']['authorized_steps_complete'])
        manifest = app.read(self.work / self.project['requirements']['manifest'])
        self.assertEqual(manifest['origin'], 'aws-generated')
        self.assertEqual(manifest['evidence_level'], 'offline-fixture')
        self.assertEqual(manifest['producing_job_id'], 'job-req-1')
        self.assertEqual(manifest['function_ids'], ['F1'])
        stored = {entry['kind']: (self.work / entry['stored_path']).read_text() for entry in manifest['files']}
        self.assertEqual(stored, {'requirements': REQUIREMENTS_MD, 'traceability': TRACEABILITY_YAML})
        self.assertEqual({e['original_path'] for e in manifest['files']},
                         {'transform-output/job-req-1/F1/requirements.md', 'transform-output/job-req-1/F1/traceability.yaml'})
        records = requirements.active_set(self.work, self.project)['requirements']
        by_id = {r['original_id']: r for r in records}
        self.assertEqual(sorted(by_id), ['PAY-001', 'PAY-002', 'PAY-003'])
        self.assertEqual(by_id['PAY-001']['id'], 'aws-req:F1:PAY-001')
        self.assertEqual(by_id['PAY-001']['traceability']['state'], 'mapped')
        self.assertEqual(by_id['PAY-001']['traceability']['source_paths_in_pin'], ['rule.cbl'])
        self.assertEqual(by_id['PAY-002']['traceability']['state'], 'partial')
        self.assertEqual(by_id['PAY-003']['traceability']['state'], 'missing')
        self.assertTrue(all(r['traceability'].get('evidence_status', 'TRACEABILITY_CLAIM') != 'SOURCE_VERIFIED' for r in records))
        record = requirements.capability(self.work)
        self.assertFalse(record['generation_verified'])
        self.assertIn('offline fixture', requirements.provenance_statement(self.work, self.project))
        calls_before = len(client.calls_seen)
        again = self.command('resume', client=client)
        self.assertEqual(again['status'], 'REQUIREMENTS_RETRIEVED')
        self.assertEqual(len(client.calls_seen), calls_before)

    def test_an_uncertain_creation_is_never_retried_automatically(self):
        client = FakeTransform(fail_create=True)
        self.discover(client)
        self.command('authorize-job', '--functions', 'F1', '--by', 'Owner', '--note', 'Pilot', client=client)
        with self.assertRaises(Blocked):
            self.command('resume', client=client)
        client.fail_create = False
        result = self.command('resume', client=client)
        self.assertEqual(result['status'], 'REQUIREMENTS_NEEDS_RECONCILIATION')
        self.assertEqual(sum(1 for name, _ in client.calls_seen if name == 'create_job'), 1)

    def test_a_plan_without_generate_requirements_is_a_capability_stop(self):
        client = FakeTransform(plan_steps=('Analyze code', 'Extract business logic'))
        self.discover(client)
        self.command('authorize-job', '--functions', 'F1', '--by', 'Owner', '--note', 'Pilot', client=client)
        with self.assertRaises(Blocked) as raised:
            self.command('resume', client=client)
        self.assertEqual(states.describe(raised.exception)['cause'], 'CAPABILITY_UNVERIFIED')
        self.assertFalse(any(name == 'complete_task' for name, _ in client.calls_seen))

    def test_a_value_outside_the_task_schema_is_refused(self):
        client = FakeTransform()
        self.discover(client)
        self.command('authorize-job', '--functions', 'F9', '--by', 'Owner', '--note', 'Pilot', client=client)
        with self.assertRaises(Blocked):
            self.command('resume', client=client)
        self.assertFalse(any(name == 'complete_task' for name, _ in client.calls_seen))

    def test_an_unrecognized_human_task_waits_for_a_person(self):
        client = FakeTransform(task={'taskId': 'T7', 'status': 'AWAITING_HUMAN_INPUT', 'title': 'Approve the decomposition',
                                     '_outputSchema': {'type': 'object', 'properties': {'ok': {'enum': ['yes', 'no']}}}})
        self.discover(client)
        self.command('authorize-job', '--functions', 'F1', '--by', 'Owner', '--note', 'Pilot', client=client)
        result = self.command('resume', client=client)
        self.assertEqual(result['status'], 'REQUIREMENTS_WAITING_FOR_HUMAN')
        self.assertIn('Approve the decomposition', result['reason'])
        self.assertFalse(any(name == 'complete_task' for name, _ in client.calls_seen))

    def test_without_a_selection_the_catalog_from_the_schema_is_shown(self):
        client = FakeTransform()
        self.discover(client)
        self.command('authorize-job', '--by', 'Owner', '--note', 'Pilot', client=client)
        result = self.command('resume', client=client)
        self.assertEqual(result['status'], 'REQUIREMENTS_WAITING_FOR_HUMAN')
        self.assertEqual(result['catalog'], ['F1', 'F2'])
        chosen = self.command('resume', '--select', 'F2', client=client)
        self.assertEqual(json.loads([a for n, a in client.calls_seen if n == 'complete_task'][0]['content']), {'functions': ['F2']})

    def test_an_import_is_labeled_imported_and_never_generated(self):
        folder = self.root / 'external'
        folder.mkdir()
        (folder / 'requirements.md').write_text(REQUIREMENTS_MD)
        (folder / 'traceability.yaml').write_text(TRACEABILITY_YAML)
        result = self.command('import', '--requirements', str(folder / 'requirements.md'), '--traceability',
                              str(folder / 'traceability.yaml'), '--function', 'F1', '--by', 'Analyst',
                              '--note', 'Exported from the AWS console by the analyst')
        self.assertEqual(result['origin'], 'imported')
        manifest = app.read(self.work / self.project['requirements']['manifest'])
        self.assertFalse(manifest['generated_by_reframe'])
        self.assertEqual(manifest['evidence_level'], 'imported')
        self.assertEqual((self.work / manifest['files'][0]['stored_path']).read_text(), REQUIREMENTS_MD)
        self.assertIn('Reframe did not generate them', result['provenance'])
        self.assertEqual(self.command('status')['status'], 'REQUIREMENTS_GENERATION_UNAVAILABLE')

    def test_heading_requirements_are_read_and_nothing_is_dropped_silently(self):
        folder = self.root / 'headings'
        folder.mkdir()
        (folder / 'requirements.md').write_text(
            '# Payments\n\n## PAY-010 Reject a zero amount\nA payment of zero is refused with a message.\n\n'
            '## PAY-011 Keep a receipt\nEvery accepted payment keeps a receipt.\n\n'
            '## F1-R1 Post nightly\nThe batch posts accepted payments nightly.\n\n## Appendix\nSee also PAY-099 in the appendix.\n')
        result = self.command('import', '--requirements', str(folder / 'requirements.md'), '--function', 'F1',
                              '--by', 'Analyst', '--note', 'Exported from the AWS console by the analyst')
        self.assertEqual(result['count'], 3)
        records = {item['original_id']: item for item in requirements.active_set(self.work, self.project)['requirements']}
        self.assertEqual(sorted(records), ['F1-R1', 'PAY-010', 'PAY-011'], 'an id whose last segment has a letter prefix is read')
        self.assertIn('refused with a message', records['PAY-010']['text'])
        self.assertIn('no "shall" statement', records['PAY-010']['uncertainty'])
        self.assertEqual(result['unrecognized_lines'], 1, 'the cross-reference line is counted, not dropped silently')
        self.assertTrue(result['warnings'])
        empty = self.root / 'prose'
        empty.mkdir()
        (empty / 'requirements.md').write_text('# Notes\nPayments are checked before posting.\n')
        result = self.command('import', '--requirements', str(empty / 'requirements.md'), '--function', 'F2',
                              '--by', 'Analyst', '--note', 'Exported from the AWS console by the analyst')
        self.assertEqual(result['count'], 0)
        self.assertIn('No requirement records were recognized', ' '.join(result['warnings']))

    def test_an_import_after_a_reviewed_specification_supersedes_its_approvals(self):
        self.project['specification'] = {'path': 'preparation/candidate.json', 'sha256': 'x'}
        self.project['approvals']['validation'] = {'by': 'A', 'note': 'ok', 'sha256': 'y'}
        folder = self.root / 'external2'
        folder.mkdir()
        (folder / 'requirements.md').write_text(REQUIREMENTS_MD)
        requirements.import_files(self.work, self.project, folder / 'requirements.md', None, 'F1', 'Analyst', 'Console export')
        self.assertNotIn('validation', self.project['approvals'])
        self.assertTrue(self.project['requirements']['requires_revalidation'])
        self.assertEqual(self.project['approval_history'][-1]['reason'], 'requirements_imported')

    def test_a_changed_stored_requirement_file_is_an_integrity_failure(self):
        folder = self.root / 'external3'
        folder.mkdir()
        (folder / 'requirements.md').write_text(REQUIREMENTS_MD)
        requirements.import_files(self.work, self.project, folder / 'requirements.md', None, 'F1', 'Analyst', 'Console export')
        manifest = app.read(self.work / self.project['requirements']['manifest'])
        (self.work / manifest['files'][0]['stored_path']).write_text('edited')
        with self.assertRaises(Blocked):
            requirements.active_set(self.work, self.project)


if __name__ == '__main__':
    unittest.main()
