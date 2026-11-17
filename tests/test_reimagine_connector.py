"""Reimagine (Neptune) connector for requirements generation (#206). Offline: AWS CLI and Transform are fixtures.

The stack outputs, cluster fields, and connector record have the shapes AWS returned for this account; every
identifier here is synthetic.
"""
import json
import unittest
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

import test_requirements as base
import reframe as app
import reframe_reimagine as reimagine
import reframe_states as states
from pilot import Blocked

ACCOUNT = '000000000000'
CLUSTER_ARN = 'arn:aws:rds:us-east-1:' + ACCOUNT + ':cluster:fixture-kg-cluster'
LOADER_ARN = 'arn:aws:iam::' + ACCOUNT + ':role/fixture-NeptuneS3Role-us-east-1'


def stack(bucket='fixture-bucket', status='CREATE_COMPLETE', subnets='subnet-a,subnet-b', drop=None, kms=''):
    outputs = {'VPCId': 'vpc-fixture', 'NeptuneClusterArn': CLUSTER_ARN, 'NeptuneClusterResourceId': 'cluster-FIXTURE',
               'AppSubnetIds': subnets, 'AppSecurityGroupId': 'sg-fixture', 'NeptuneS3BulkLoaderRoleArn': LOADER_ARN}
    outputs.pop(drop, None)
    return {'Stacks': [{'StackName': 'fixture-kg', 'StackStatus': status,
                        'Parameters': [{'ParameterKey': 'BucketName', 'ParameterValue': bucket},
                                       {'ParameterKey': 'KmsKeyId', 'ParameterValue': kms}],
                        'Outputs': [{'OutputKey': key, 'OutputValue': value} for key, value in outputs.items()]}]}


def cluster(**changes):
    detail = {'DBClusterIdentifier': 'fixture-kg-cluster', 'Engine': 'neptune', 'EngineVersion': '1.4.5.1', 'Status': 'available',
              'IAMDatabaseAuthenticationEnabled': True, 'StorageEncrypted': True,
              'ServerlessV2ScalingConfiguration': {'MinCapacity': 1.0, 'MaxCapacity': 32.0},
              'DBClusterMembers': [{'DBInstanceIdentifier': 'primary'}, {'DBInstanceIdentifier': 'replica'}]}
    detail.update(changes)
    return {'DBClusters': [detail]}


class FakeAws:
    """AWS CLI fixture. Records every command; answers only the read and create calls this feature makes."""

    def __init__(self, stack_reply=None, cluster_reply=None, account=ACCOUNT):
        self.seen = []
        self.stack_reply = stack_reply or stack()
        self.cluster_reply = cluster_reply or cluster()
        self.account = account

    def __call__(self, project, *args):
        self.seen.append(args)
        if args[:2] == ('sts', 'get-caller-identity'):
            return {'Account': self.account, 'Arn': 'arn:aws:sts::' + self.account + ':assumed-role/fixture/owner@example.com'}
        if args[:2] == ('cloudformation', 'describe-stacks'):
            return self.stack_reply
        if args[:2] == ('neptune', 'describe-db-clusters'):
            return self.cluster_reply
        if args[:2] == ('iam', 'create-role'):
            name = args[args.index('--role-name') + 1]
            return {'Role': {'RoleName': name, 'Arn': 'arn:aws:iam::' + ACCOUNT + ':role/service-role/' + name}}
        if args[:2] in {('iam', 'put-role-policy'), ('s3', 'cp')}:
            return {}
        raise AssertionError('Unexpected AWS command ' + ' '.join(args[:2]))

    def mutations(self):
        return [args[:2] for args in self.seen if args[:2] in {('iam', 'create-role'), ('iam', 'put-role-policy'), ('s3', 'cp')}]


class FakeConnectors:
    """Transform fixture: creates one connector, echoes its record, and activates it on accept."""

    def __init__(self, reported_type=None, activates=True, refuse=None):
        self.seen = []
        self.refuse = refuse
        self.created = None
        self.role = None
        self.reported_type = reported_type
        self.activates = activates

    def calls(self, requests):
        results = []
        for name, arguments in requests:
            self.seen.append((name, arguments))
            if name == 'create_connector' and self.refuse:
                raise Blocked(self.refuse)
            if name == 'create_connector':
                self.created = arguments
                results.append({'connectorId': 'fixture-reimagine', 'verificationLink': 'https://example.invalid/verify'})
            elif name == 'accept_connector':
                self.role = arguments['roleArn'] if self.activates else None
                results.append({'connectorId': arguments['connectorId']})
            elif name == 'get_resource':
                created = self.created or {}
                connection = {'status': 'ACTIVE', 'accountId': ACCOUNT, 'roleArn': self.role} if self.role else {'status': 'PENDING'}
                results.append({'connectorId': arguments['connectorId'], 'connectorName': created.get('connectorName'),
                                'connectorType': self.reported_type or created.get('connectorType'),
                                'connectorConfiguration': created.get('configuration'),
                                'accountConnection': {'awsAccountConnection': connection}})
            else:
                raise AssertionError('Unexpected Transform call ' + name)
        return results

    def names(self):
        return [name for name, _ in self.seen]


class ReimagineConnectorTests(unittest.TestCase):
    args = base.RequirementsTests.args
    assess = base.RequirementsTests.assess
    approve = base.RequirementsTests.approve
    baseline = base.RequirementsTests.baseline
    spec = base.RequirementsTests.spec
    command = base.RequirementsTests.command
    discover = base.RequirementsTests.discover

    def setUp(self):
        base.RequirementsTests.setUp(self)
        self.project['aws']['bucket'] = 'fixture-bucket'
        self.project['stage'] = 'VALIDATION_APPROVED'
        self.project['setup']['connector_id'] = 'assessment-s3'
        app.persist(self.work, self.project)

    def connector(self, *values, aws=None, client=None):
        aws = aws or FakeAws()
        with patch.object(app, 'aws', side_effect=aws):
            result = self.command('connector', '--neptune-stack', 'fixture-kg', '--by', 'Owner', '--note', 'Pilot connector',
                                  *values, client=client)
        return result, aws

    def test_without_create_it_only_reads_and_plans(self):
        result, aws = self.connector()
        self.assertEqual(result['status'], 'REIMAGINE_CONNECTOR_PLANNED')
        self.assertEqual(aws.mutations(), [])
        self.assertEqual(result['connector_type'], 'mainframe_modernization|reimagine|1')
        self.assertTrue(result['same_bucket_as_project'])
        self.assertEqual(result['neptune']['instances'], 2)
        self.assertIn('bills', result['neptune']['billing'])
        self.assertNotIn('requirements_connector', self.project)
        plan = json.loads((reimagine.folder(self.work) / 'plan.json').read_text())
        self.assertEqual(plan['configuration']['vpcSubnetIds'], 'subnet-a,subnet-b')

    def test_create_makes_one_role_and_one_connector_and_keeps_the_assessment_state(self):
        client = FakeConnectors()
        first, aws = self.connector('--create', client=client)
        again, aws_again = self.connector('--create', client=client)
        self.assertEqual(first['status'], 'REIMAGINE_CONNECTOR_ACTIVE')
        self.assertEqual(again['status'], 'REIMAGINE_CONNECTOR_ACTIVE')
        self.assertEqual(aws.mutations(), [('iam', 'create-role'), ('iam', 'put-role-policy')])
        self.assertEqual(aws_again.mutations(), [])
        self.assertEqual(client.names().count('create_connector'), 1)
        self.assertEqual(client.names().count('accept_connector'), 1)
        created = client.created
        self.assertEqual(created['connectorType'], 'mainframe_modernization|reimagine|1')
        self.assertEqual(created['configuration'], {
            's3BucketArn': 'arn:aws:s3:::fixture-bucket', 'neptuneClusterArn': CLUSTER_ARN,
            'neptuneClusterResourceId': 'cluster-FIXTURE', 'neptuneBulkUploadRoleArn': LOADER_ARN,
            'vpcSubnetIds': 'subnet-a,subnet-b', 'vpcSecurityGroupId': 'sg-fixture'})
        self.assertEqual(created['awsAccountId'], ACCOUNT)
        entry = self.project['requirements_connector']
        self.assertEqual(entry['status'], 'ACTIVE')
        self.assertTrue(entry['role_created_by_reframe'])
        self.assertEqual(self.project['stage'], 'VALIDATION_APPROVED')
        self.assertEqual(self.project['setup']['connector_id'], 'assessment-s3')
        self.assertEqual(self.project['events'][-1]['event'], 'reimagine_connector_recorded')

    def test_the_role_is_scoped_to_the_stack_and_trusts_only_this_accounts_connectors(self):
        aws = FakeAws()
        self.connector('--create', aws=aws, client=FakeConnectors())
        create = next(args for args in aws.seen if args[:2] == ('iam', 'create-role'))
        self.assertEqual(create[create.index('--path') + 1], '/service-role/')
        trust = json.loads(create[create.index('--assume-role-policy-document') + 1])['Statement'][0]
        self.assertEqual(trust['Principal'], {'Service': 'transform.amazonaws.com'})
        self.assertEqual(trust['Action'], ['sts:AssumeRole', 'sts:SetContext'])
        self.assertEqual(trust['Condition']['StringEquals'], {'aws:SourceAccount': ACCOUNT})
        self.assertEqual(trust['Condition']['ArnEquals'], {'aws:SourceArn': 'arn:aws:transform:us-east-1:' + ACCOUNT + ':connector/*'})
        put = next(args for args in aws.seen if args[:2] == ('iam', 'put-role-policy'))
        policy = json.loads(put[put.index('--policy-document') + 1])
        resources = [item for statement in policy['Statement'] for item in statement['Resource']]
        buckets = {item.split(':::')[1].split('/')[0] for item in resources if item.startswith('arn:aws:s3:::')}
        self.assertEqual(buckets, {'fixture-bucket'})
        self.assertIn('arn:aws:neptune-db:us-east-1:' + ACCOUNT + ':cluster-FIXTURE/*', resources)
        self.assertIn(CLUSTER_ARN, resources)
        writes = [statement for statement in policy['Statement'] if 's3:PutObject' in statement['Action']]
        self.assertEqual(writes[0]['Resource'], ['arn:aws:s3:::fixture-bucket/transform-output/*'])

    def test_an_existing_role_is_used_and_no_role_is_created(self):
        role = 'arn:aws:iam::' + ACCOUNT + ':role/service-role/owner-made'
        client = FakeConnectors()
        result, aws = self.connector('--create', '--role-arn', role, client=client)
        self.assertEqual(aws.mutations(), [])
        self.assertEqual(next(args for name, args in client.seen if name == 'accept_connector')['roleArn'], role)
        self.assertFalse(self.project['requirements_connector']['role_created_by_reframe'])
        self.assertEqual(result['status'], 'REIMAGINE_CONNECTOR_ACTIVE')
        with self.assertRaisesRegex(Blocked, 'another AWS account'):
            self.connector('--create', '--role-arn', 'arn:aws:iam::111111111111:role/other', client=client)

    def test_a_connector_aws_records_differently_is_refused_and_not_activated(self):
        client = FakeConnectors(reported_type='mainframe_modernization|s3|2')
        with self.assertRaisesRegex(Blocked, 'connector type mainframe_modernization\\|s3\\|2'):
            self.connector('--create', client=client)
        self.assertNotIn('accept_connector', client.names())
        self.assertNotEqual((self.project.get('requirements_connector') or {}).get('status'), 'ACTIVE')

    def test_an_inactive_connector_is_recorded_pending_and_the_rerun_creates_nothing(self):
        client = FakeConnectors(activates=False)
        pending, _ = self.connector('--create', client=client)
        self.assertEqual(pending['status'], 'REIMAGINE_CONNECTOR_ACTIVATION_PENDING')
        self.assertIn('Rerun the same command', pending['next_step'])
        client.activates = True
        active, aws = self.connector('--create', client=client)
        self.assertEqual(active['status'], 'REIMAGINE_CONNECTOR_ACTIVE')
        self.assertEqual(client.names().count('create_connector'), 1)
        self.assertEqual(aws.mutations(), [])

    def test_an_uncertain_connector_creation_is_never_sent_again(self):
        folder = reimagine.folder(self.work)
        folder.mkdir(parents=True, exist_ok=True)
        (folder / 'connector-fixture-bucket-reimagine-intent.json').write_text('{}')
        client = FakeConnectors()
        with self.assertRaises(Blocked) as raised:
            self.connector('--create', client=client)
        self.assertEqual(states.describe(raised.exception)['cause'], 'UNCERTAIN_DISPATCH')
        self.assertNotIn('create_connector', client.names())
        plan = json.loads((folder / 'plan.json').read_text())
        client.created = {'connectorType': reimagine.CONNECTOR_TYPE, 'configuration': plan['configuration']}  # It exists in AWS.
        attached, _ = self.connector('--create', '--attach-connector', 'fixture-reimagine', client=client)
        self.assertEqual(attached['status'], 'REIMAGINE_CONNECTOR_ACTIVE')
        self.assertNotIn('create_connector', client.names())
        self.assertEqual(self.project['requirements_connector']['connector_id'], 'fixture-reimagine')

    def test_a_stack_that_does_not_meet_aws_requirements_is_refused_before_any_change(self):
        cases = {
            'lacks the Neptune connector outputs: NeptuneClusterResourceId': FakeAws(stack(drop='NeptuneClusterResourceId')),
            'at least two application subnets': FakeAws(stack(subnets='subnet-a')),
            'must be CREATE_COMPLETE': FakeAws(stack(status='ROLLBACK_COMPLETE')),
            'another AWS account': FakeAws(account='111111111111'),
            'engine 1.4.5.1 or later': FakeAws(cluster_reply=cluster(EngineVersion='1.3.2.1')),
            'IAM authentication': FakeAws(cluster_reply=cluster(IAMDatabaseAuthenticationEnabled=False)),
            'Neptune Serverless': FakeAws(cluster_reply=cluster(ServerlessV2ScalingConfiguration=None)),
            'not a key ARN': FakeAws(stack(kms='fixture-key-id')),
        }
        for message, aws in cases.items():
            with self.subTest(message=message):
                client = FakeConnectors()
                with self.assertRaisesRegex(Blocked, message):
                    self.connector('--create', aws=aws, client=client)
                self.assertEqual(aws.mutations(), [])
                self.assertEqual(client.seen, [])

    def test_a_kms_key_arn_is_passed_as_the_bucket_key(self):
        key = 'arn:aws:kms:us-east-1:' + ACCOUNT + ':key/fixture'
        result, _ = self.connector(aws=FakeAws(stack(kms=key)))
        plan = json.loads((reimagine.folder(self.work) / 'plan.json').read_text())
        self.assertEqual(plan['configuration']['s3BucketKmsKeyArn'], key)

    def source_archive(self):
        record = self.project['assessments'][self.project['selected']]
        archive = Path(record['directory']) / 'source.zip'
        archive.write_bytes(b'fixture source archive')
        run = app.read(Path(record['directory']) / 'run.json')
        run['uploaded_source']['sha256'] = sha256(archive.read_bytes()).hexdigest()
        app.write(Path(record['directory']) / 'run.json', run)
        return archive

    def test_a_separate_stack_bucket_needs_the_checked_source_copy_before_a_job(self):
        archive = self.source_archive()
        other = FakeAws(stack(bucket='fixture-kg-bucket'))
        connectors = FakeConnectors()
        result, _ = self.connector('--create', aws=other, client=connectors)
        self.assertFalse(result['same_bucket_as_project'])
        self.assertIn('--copy-source', result['next_step'])
        transform = base.FakeTransform()
        self.discover(transform)
        self.command('authorize-job', '--functions', 'F1', '--by', 'Owner', '--note', 'Bill payment', client=transform)
        with self.assertRaisesRegex(Blocked, 'source was not copied there'):
            self.command('resume', client=transform)
        self.assertNotIn('create_job', [name for name, _ in transform.calls_seen])
        archive.write_bytes(b'changed after upload')
        with self.assertRaisesRegex(Blocked, 'differs from the one the assessment uploaded'):
            self.connector('--create', '--copy-source', aws=FakeAws(stack(bucket='fixture-kg-bucket')),
                           client=connectors)
        self.source_archive()
        copied, aws = self.connector('--create', '--copy-source',
                                     aws=FakeAws(stack(bucket='fixture-kg-bucket')), client=connectors)
        copy = next(args for args in aws.seen if args[:2] == ('s3', 'cp'))
        self.assertTrue(copy[3].startswith('s3://fixture-kg-bucket/reframe/'))
        self.assertEqual(copied['source']['uri'], copy[3])
        self.command('resume', client=transform)
        objective = next(arguments for name, arguments in transform.calls_seen if name == 'create_job')['objective']
        self.assertIn(copy[3], objective)

    def test_the_jobs_connector_task_is_answered_only_with_the_active_reimagine_connector(self):
        task = {'taskId': 'C1', 'status': 'AWAITING_HUMAN_INPUT', 'title': 'Choose a connector',
                'uxComponentId': 'CreateOrSelectConnectors',
                '_outputSchema': {'type': 'object', 'required': ['connectorId', 'connectorType'],
                                  'properties': {'connectorId': {'type': 'string'}, 'connectorType': {'type': 'string'}}}}
        transform = base.FakeTransform(task=task)
        self.discover(transform)
        self.command('authorize-job', '--functions', 'F1', '--by', 'Owner', '--note', 'Bill payment', client=transform)
        waiting = self.command('resume', client=transform)
        self.assertEqual(waiting['status'], 'REQUIREMENTS_WAITING_FOR_HUMAN')
        self.assertNotIn('complete_task', [name for name, _ in transform.calls_seen])
        self.connector('--create', client=FakeConnectors())
        self.command('resume', client=transform)
        answer = next(arguments for name, arguments in transform.calls_seen if name == 'complete_task')
        self.assertEqual(json.loads(answer['content']),
                         {'connectorId': 'fixture-reimagine', 'connectorType': 'mainframe_modernization|reimagine|1'})

    def test_discovery_counts_only_an_active_connector_of_the_observed_type(self):
        for connector_type, status, expected in (('mainframe_modernization|reimagine|1', 'ACTIVE', []),
                                                 ('mainframe_modernization|reimagine|1', 'PENDING', ['connector']),
                                                 ('NEPTUNE_REIMAGINE', 'ACTIVE', ['connector'])):
            with self.subTest(connector_type=connector_type, status=status):
                transform = base.FakeTransform(connector=connector_type)
                transform.connector_status = status
                (self.work / 'requirements' / 'capability.json').unlink(missing_ok=True)
                self.discover(transform)
                self.assertEqual(self.command('status').get('missing') or [], expected)

    def test_the_transform_client_uses_the_saved_aws_profile_like_the_aws_cli_calls(self):
        with patch.dict('os.environ', {'AWS_PROFILE': 'shell-profile'}):
            client = app.transform_client(self.project, self.work)
        self.assertEqual({key: client.config['env'][key] for key in ('AWS_PROFILE', 'AWS_REGION')},
                         {'AWS_PROFILE': 'fixture-profile', 'AWS_REGION': 'us-east-1'})
        self.assertNotIn('env', self.project['settings']['transform'])


    def test_names_follow_the_project_name_and_the_role_is_tagged_with_it(self):
        client = FakeConnectors()
        result, aws = self.connector('--create', client=client)
        self.assertEqual(client.created['connectorName'], 'fixture-bucket-reimagine')
        create = next(args for args in aws.seen if args[:2] == ('iam', 'create-role'))
        self.assertEqual(create[create.index('--role-name') + 1], 'fixture-bucket-rmg')
        self.assertIn('Key=ReframeProject,Value=fixture-bucket', create)
        self.assertIn('Key=Purpose,Value=reimagine-connector', create)
        self.assertEqual(self.project['requirements_connector']['connector_name'], 'fixture-bucket-reimagine')

    def test_a_connector_named_otherwise_is_replaced_only_on_request_and_kept_on_record(self):
        old = {'connector_id': 'old-reimagine', 'connector_name': 'carddemo-reimagine', 'connector_type': reimagine.CONNECTOR_TYPE,
               'stack': 'fixture-kg', 'bucket': 'fixture-bucket', 'status': 'ACTIVE', 'source': None,
               'role_arn': 'arn:aws:iam::' + ACCOUNT + ':role/service-role/reframe-reimagine-fixture-kg', 'role_created_by_reframe': True}
        self.project['requirements_connector'] = dict(old)
        app.persist(self.work, self.project)
        with self.assertRaises(Blocked):
            self.connector('--create', client=FakeConnectors())
        preview, aws = self.connector('--replace')
        self.assertEqual((preview['status'], preview['connector_name'], aws.mutations()),
                         ('REIMAGINE_CONNECTOR_PLANNED', 'fixture-bucket-reimagine', []))
        with self.assertRaises(Blocked):
            self.connector('--create', '--replace', client=FakeConnectors(refuse='quota of 1 connector for this type'))
        self.assertEqual((self.project['requirements_connector'], self.project.get('requirements_connector_history')), (old, None))
        (reimagine.folder(self.work) / 'connector-fixture-bucket-reimagine-intent.json').unlink()
        client = FakeConnectors()
        replaced, aws = self.connector('--create', '--replace', client=client)
        self.assertEqual(replaced['status'], 'REIMAGINE_CONNECTOR_ACTIVE')
        self.assertEqual(aws.mutations(), [])
        self.assertEqual(client.names().count('create_connector'), 1)
        self.assertEqual(self.project['requirements_connector']['connector_name'], 'fixture-bucket-reimagine')
        history = self.project['requirements_connector_history']
        self.assertEqual([(entry['connector_id'], entry['replaced_by']) for entry in history], [('old-reimagine', 'Owner')])
        with self.assertRaises(Blocked):
            self.connector('--create', '--replace', client=client)
        again, aws_again = self.connector('--create', client=client)
        self.assertEqual((again['status'], aws_again.mutations(), client.names().count('create_connector')),
                         ('REIMAGINE_CONNECTOR_ACTIVE', [], 1))

if __name__ == '__main__':
    unittest.main()
