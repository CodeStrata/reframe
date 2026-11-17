"""Reimagine (Neptune) connector for AWS requirements generation (#206).

AWS generates requirements only in the "Assess and reimagine" and "Reimagine" job plans, and those plans
use the mainframe reimagine connector: an S3 bucket plus an Amazon Neptune Serverless knowledge graph in a
VPC. The assessment's S3 connector cannot serve them.

Every value below is observed, not guessed:

* `CONNECTOR_TYPE` and `CONFIGURATION_KEYS` are what AWS accepted in CreateConnector for this account on
  2026-11-15, and what its own validation error lists as the valid properties of this type.
* `STACK_OUTPUTS` are the outputs of AWS's `neptune-kg-setup.yaml` template, which the user guide recommends.
* `role_documents` mirrors the trust and permissions the AWS console generated for an activated reimagine
  connector, scoped to one stack's bucket, cluster, account, and region.

The command is read-only unless `--create` is passed. Each AWS mutation saves its intent before the call and
its receipt after it; an intent without a receipt stops for reconciliation and is never retried. Nothing here
changes the project stage, the assessment's connector, or the Neptune stack, and nothing is deleted.
"""
import json
import re
import time
from pathlib import Path

from pilot import require

CONNECTOR_TYPE = 'mainframe_modernization|reimagine|1'
CONFIGURATION_KEYS = ('s3BucketArn', 'neptuneClusterArn', 'neptuneClusterResourceId', 'neptuneBulkUploadRoleArn',
                      'vpcSubnetIds', 'vpcSecurityGroupId')
OPTIONAL_KEYS = ('s3BucketKmsKeyArn',)
# CloudFormation output of neptune-kg-setup.yaml -> connector configuration key.
STACK_OUTPUTS = {'NeptuneClusterArn': 'neptuneClusterArn', 'NeptuneClusterResourceId': 'neptuneClusterResourceId',
                 'NeptuneS3BulkLoaderRoleArn': 'neptuneBulkUploadRoleArn', 'AppSubnetIds': 'vpcSubnetIds',
                 'AppSecurityGroupId': 'vpcSecurityGroupId'}
STACK_READY = {'CREATE_COMPLETE', 'UPDATE_COMPLETE'}
MINIMUM_ENGINE = (1, 4, 5, 1)
ROLE_PATH = '/service-role/'
TRANSFORM_TAG = 'ManagedByAWSTransform'


def folder(work):
    """Where the connector plan, intents, and receipts are saved."""
    return Path(work) / 'requirements' / 'connector'


def _save(path, value):
    """Write one owner-only JSON record atomically."""
    import reframe_requirements as requirements
    requirements._save(path, value)


def _load(path):
    """A saved JSON record, or None when it was never written."""
    return json.loads(Path(path).read_text()) if Path(path).is_file() else None


def _engine(version):
    """Neptune engine version as a comparable tuple, or None when it is not numeric."""
    parts = str(version or '').split('.')
    return tuple(int(part) for part in parts) if parts and all(part.isdigit() for part in parts) else None


def stack_plan(project, stack, identity):
    """Read one Neptune knowledge-graph stack and its cluster, and return the connector configuration. Read-only."""
    import reframe as app
    require(re.fullmatch(r'[A-Za-z][A-Za-z0-9-]{0,127}', stack or ''), 'Enter the CloudFormation stack name only.')
    stacks = app.aws(project, 'cloudformation', 'describe-stacks', '--stack-name', stack, '--output', 'json').get('Stacks') or []
    require(len(stacks) == 1, 'CloudFormation stack ' + stack + ' was not found in this profile and region')
    found = stacks[0]
    require(found.get('StackStatus') in STACK_READY,
            'Stack ' + stack + ' is ' + str(found.get('StackStatus')) + '; it must be CREATE_COMPLETE or UPDATE_COMPLETE')
    parameters = {item.get('ParameterKey'): item.get('ParameterValue') for item in found.get('Parameters') or []}
    outputs = {item.get('OutputKey'): item.get('OutputValue') for item in found.get('Outputs') or []}
    missing = sorted(name for name in STACK_OUTPUTS if not str(outputs.get(name) or '').strip())
    require(not missing, 'Stack ' + stack + ' lacks the Neptune connector outputs: ' + ', '.join(missing)
            + '. Deploy AWS\'s neptune-kg-setup.yaml template.')
    bucket = str(parameters.get('BucketName') or '').strip()
    require(re.fullmatch(r'[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]', bucket), 'Stack ' + stack + ' has no BucketName parameter')
    cluster_arn = outputs['NeptuneClusterArn']
    arn = cluster_arn.split(':')
    require(len(arn) >= 7 and arn[2] == 'rds' and arn[5] == 'cluster', 'NeptuneClusterArn is not a cluster ARN')
    partition, region, account, cluster = arn[1], arn[3], arn[4], arn[6]
    require(account == identity.get('Account'), 'The Neptune cluster belongs to another AWS account than this profile')
    require(region == project['aws'].get('region'), 'The Neptune cluster is in ' + region + ', not the project region')
    subnets = [item.strip() for item in outputs['AppSubnetIds'].split(',') if item.strip()]
    require(len(set(subnets)) >= 2, 'The stack must output at least two application subnets in separate Availability Zones')
    clusters = app.aws(project, 'neptune', 'describe-db-clusters', '--db-cluster-identifier', cluster,
                       '--output', 'json').get('DBClusters') or []
    require(len(clusters) == 1, 'Neptune cluster ' + cluster + ' was not found')
    detail = clusters[0]
    require(detail.get('Engine') == 'neptune', 'Cluster ' + cluster + ' is not a Neptune cluster')
    require(detail.get('Status') == 'available', 'Neptune cluster ' + cluster + ' is ' + str(detail.get('Status')))
    version = _engine(detail.get('EngineVersion'))
    require(version and version >= MINIMUM_ENGINE, 'AWS requires Neptune engine 1.4.5.1 or later; the cluster runs '
            + str(detail.get('EngineVersion')))
    require(detail.get('IAMDatabaseAuthenticationEnabled') is True, 'AWS requires IAM authentication on the Neptune cluster')
    require(detail.get('StorageEncrypted') is True, 'AWS requires storage encryption on the Neptune cluster')
    scaling = detail.get('ServerlessV2ScalingConfiguration') or {}
    require(scaling, 'AWS requires Neptune Serverless; the cluster has no serverless scaling configuration')
    configuration = {'s3BucketArn': 'arn:' + partition + ':s3:::' + bucket}
    for output, key in STACK_OUTPUTS.items():
        configuration[key] = ','.join(subnets) if key == 'vpcSubnetIds' else outputs[output].strip()
    kms = str(parameters.get('KmsKeyId') or '').strip()
    if kms:
        require(kms.startswith('arn:'), 'The stack KmsKeyId is not a key ARN; the connector needs s3BucketKmsKeyArn as an ARN')
        configuration['s3BucketKmsKeyArn'] = kms
    members = detail.get('DBClusterMembers') or []
    return {'stack': stack, 'stack_status': found['StackStatus'], 'bucket': bucket, 'partition': partition,
            'region': region, 'account': account, 'cluster': cluster, 'configuration': configuration,
            'neptune': {'engine_version': detail.get('EngineVersion'), 'instances': len(members),
                        'min_ncu': scaling.get('MinCapacity'), 'max_ncu': scaling.get('MaxCapacity'),
                        'billing': 'Neptune Serverless bills per NCU-hour for every instance while the cluster runs, '
                                   'including when no job uses it.'}}


def project_name(project):
    """The one name Reframe gives a project's resources: its bucket, Transform workspace, and S3 connector."""
    name = str((project.get('aws') or {}).get('bucket') or '').strip()
    require(name, 'The project has no recorded resource name (its S3 bucket); run setup first')
    return name


def connector_name(project):
    """The reimagine connector's name: the project name and its purpose."""
    return project_name(project) + '-reimagine'


def role_name(project):
    """The reimagine connector role's name: the project name and a short suffix that fits IAM's 64 characters."""
    name = project_name(project) + '-rmg'
    require(len(name) <= 64, 'The project name leaves no room for the connector role name within IAM\'s 64 characters')
    return name


def role_documents(plan):
    """Trust and permissions for the connector role, mirroring what the AWS console generates for this connector."""
    p, region, account = plan['partition'], plan['region'], plan['account']
    bucket = 'arn:' + p + ':s3:::' + plan['bucket']
    in_account = {'StringEquals': {'aws:ResourceAccount': account}}
    interface = 'arn:' + p + ':ec2:' + region + ':' + account + ':network-interface/*'
    trust = {'Version': '2012-10-17', 'Statement': [{
        'Effect': 'Allow', 'Principal': {'Service': 'transform.amazonaws.com'}, 'Action': ['sts:AssumeRole', 'sts:SetContext'],
        'Condition': {'StringEquals': {'aws:SourceAccount': account},
                      'ArnEquals': {'aws:SourceArn': 'arn:' + p + ':transform:' + region + ':' + account + ':connector/*'}}}]}
    permissions = {'Version': '2012-10-17', 'Statement': [
        {'Effect': 'Allow', 'Action': ['s3:GetBucketLocation', 's3:ListBucket', 's3:GetObject', 's3:ListMultipartUploadParts',
                                       's3:ListBucketMultipartUploads', 's3:GetBucketPublicAccessBlock'],
         'Resource': [bucket + '/*', bucket], 'Condition': in_account},
        {'Effect': 'Allow', 'Action': ['s3:GetAccountPublicAccessBlock'], 'Resource': ['*'], 'Condition': in_account},
        {'Effect': 'Allow', 'Action': ['s3:PutObject', 's3:AbortMultipartUpload'],
         'Resource': [bucket + '/transform-output/*'], 'Condition': in_account},
        {'Sid': 'AllowS3Deletes', 'Effect': 'Allow', 'Action': ['s3:DeleteObject'],
         'Resource': [bucket + '/transform-output/neptune-quads/*'], 'Condition': in_account},
        {'Effect': 'Allow', 'Action': ['ec2:DescribeDhcpOptions', 'ec2:DescribeNetworkInterfaces', 'ec2:DescribeSubnets',
                                       'ec2:DescribeSecurityGroups', 'ec2:DescribeVpcs'], 'Resource': ['*']},
        {'Effect': 'Allow', 'Action': ['ec2:CreateNetworkInterfacePermission'], 'Resource': [interface]},
        {'Effect': 'Allow', 'Action': ['ec2:CreateTags'], 'Resource': [interface],
         'Condition': {'StringEquals': {'aws:RequestTag/' + TRANSFORM_TAG: '', 'ec2:CreateAction': 'CreateNetworkInterface'}}},
        {'Effect': 'Allow', 'Action': ['ec2:DeleteNetworkInterface'], 'Resource': ['*'],
         'Condition': {'StringEquals': {'aws:ResourceTag/' + TRANSFORM_TAG: ''}}},
        {'Effect': 'Allow', 'Action': ['ec2:CreateNetworkInterface'],
         'Resource': ['arn:' + p + ':ec2:' + region + ':' + account + ':subnet/*',
                      'arn:' + p + ':ec2:' + region + ':' + account + ':security-group/*']},
        {'Effect': 'Allow', 'Action': ['ec2:CreateNetworkInterface'], 'Resource': [interface],
         'Condition': {'ForAnyValue:StringEquals': {'aws:TagKeys': [TRANSFORM_TAG]}}},
        {'Effect': 'Allow', 'Action': ['ec2:ModifyNetworkInterfaceAttribute'], 'Resource': [interface],
         'Condition': {'Null': {'aws:ResourceTag/' + TRANSFORM_TAG: 'false'}}},
        {'Effect': 'Allow', 'Action': ['ec2:ModifyNetworkInterfaceAttribute'],
         'Resource': ['arn:' + p + ':ec2:' + region + ':*:instance/*']},
        {'Sid': 'AllowNeptuneDBAccess', 'Effect': 'Allow',
         'Action': ['neptune-db:ReadDataViaQuery', 'neptune-db:DeleteDataViaQuery', 'neptune-db:StartLoaderJob',
                    'neptune-db:GetLoaderJobStatus', 'neptune-db:CancelLoaderJob', 'neptune-db:ListLoaderJobs',
                    'neptune-db:GetQueryStatus'],
         'Resource': ['arn:' + p + ':neptune-db:' + region + ':' + account + ':'
                      + plan['configuration']['neptuneClusterResourceId'] + '/*']},
        {'Sid': 'AllowNeptuneDescribe', 'Effect': 'Allow', 'Action': 'rds:DescribeDBClusters',
         'Resource': [plan['configuration']['neptuneClusterArn']]}]}
    return trust, permissions


def _once(work, name, call):
    """Run one AWS mutation at most once: intent saved first, receipt after. An intent alone stops."""
    intent, receipt = folder(work) / (name + '-intent.json'), folder(work) / (name + '-receipt.json')
    saved = _load(receipt)
    if saved is not None:
        return saved
    if intent.is_file():
        from reframe_states import stop
        stop('The ' + name.replace('-', ' ') + ' request was sent but no receipt was saved. Its outcome is uncertain.',
             'UNCERTAIN_DISPATCH', hint='Check AWS for it, then rerun with --role-arn or --attach-connector to record '
                                          'what exists. Reframe never sends it again.')
    _save(intent, {'at': time.time()})
    result = call()
    _save(receipt, result if isinstance(result, dict) else {'result': result})
    return _load(receipt)


def _role(work, project, plan, args):
    """The connector role ARN: the one given, or one created for this stack."""
    import reframe as app
    if args.role_arn:
        require(re.fullmatch(r'arn:[a-z-]+:iam::\d{12}:role/[\w+=,.@/-]+', args.role_arn), 'Enter an IAM role ARN')
        require(args.role_arn.split(':')[4] == plan['account'], 'The connector role is in another AWS account')
        return args.role_arn, False
    name = role_name(project)
    trust, permissions = role_documents(plan)
    created = _once(work, 'role-' + name, lambda: app.aws(
        project, 'iam', 'create-role', '--role-name', name, '--path', ROLE_PATH,
        '--assume-role-policy-document', json.dumps(trust),
        '--description', 'AWS Transform reimagine connector for stack ' + plan['stack'] + ' (created by Reframe)',
        '--tags', 'Key=ManagedBy,Value=reframe', 'Key=ReframeProject,Value=' + project_name(project),
        'Key=Purpose,Value=reimagine-connector', 'Key=NeptuneStack,Value=' + plan['stack'], '--output', 'json'))
    arn = (created.get('Role') or {}).get('Arn')
    require(arn, 'The role receipt has no ARN; reconcile in IAM and rerun with --role-arn')
    _once(work, 'role-policy-' + name, lambda: app.aws(
        project, 'iam', 'put-role-policy', '--role-name', name, '--policy-name', 'reframe-reimagine-connector',
        '--policy-document', json.dumps(permissions)) or {'put': name})
    return arn, True


def _readiness(client, workspace, connector_id, plan, role_arn):
    """AWS's own record of the connector must match what was requested, exactly."""
    record = client.calls([('get_resource', {'resource': 'connector', 'workspaceId': workspace,
                                             'connectorId': connector_id})])[0]
    require(record.get('connectorType') == CONNECTOR_TYPE,
            'AWS reports connector type ' + str(record.get('connectorType')) + ', not ' + CONNECTOR_TYPE)
    require((record.get('connectorConfiguration') or {}) == plan['configuration'],
            'AWS reports a different connector configuration than the stack outputs that were requested')
    connection = (record.get('accountConnection') or {}).get('awsAccountConnection') or {}
    return record, connection.get('status') == 'ACTIVE' and connection.get('accountId') == plan['account'] \
        and connection.get('roleArn') == role_arn


def connector(work, project, args, client):
    """Plan, and with --create make and activate, one reimagine connector for a Neptune stack. Records, never deletes."""
    import reframe as app
    require(str(args.by or '').strip() and str(args.note or '').strip(), 'The reimagine connector needs a named owner and a note')
    workspace = ((project.get('settings') or {}).get('transform') or {}).get('workspace_id')
    require(workspace, 'The Transform workspace is not configured')
    identity = app.aws(project, 'sts', 'get-caller-identity', '--output', 'json')
    plan = stack_plan(project, args.neptune_stack, identity)
    recorded = project.get('requirements_connector') or {}
    name = connector_name(project)
    named = recorded.get('connector_name') == name
    if getattr(args, 'replace', False):
        require(recorded and not named, 'Nothing to replace: no recorded connector is named other than '
                + name + ' and ' + role_name(project))
    else:
        require(not args.create or not recorded or named,
                'The recorded reimagine connector does not follow the project names (' + name + ', '
                + role_name(project) + '). Rerun with --replace to create that pair; the old one is kept, never deleted.')
        require(not recorded or recorded.get('stack') == plan['stack'],
                'A reimagine connector is already recorded for stack ' + str(recorded.get('stack')) + '; nothing is replaced')
        saved = _load(folder(work) / 'plan.json')
        require(not saved or not recorded or saved['configuration'] == plan['configuration'],
                'Stack ' + plan['stack'] + ' outputs changed after its connector was created. Reconcile; nothing is replaced.')
    _save(folder(work) / 'plan.json', plan)
    same_bucket = plan['bucket'] == project['aws'].get('bucket')
    summary = {'stack': plan['stack'], 'connector_type': CONNECTOR_TYPE, 'bucket': plan['bucket'],
               'same_bucket_as_project': same_bucket, 'neptune': plan['neptune'], 'connector_name': name,
               'role': args.role_arn or role_name(project)}
    if not args.create:
        return {'status': 'REIMAGINE_CONNECTOR_PLANNED', **summary,
                'creates': ([] if args.role_arn else ['IAM role ' + role_name(project)])
                           + ['Transform connector ' + name + ' (' + CONNECTOR_TYPE + ')'],
                'next_step': 'Add --create to create and activate it. No AWS resource was created.'}
    if getattr(args, 'replace', False):
        # The old pair stays in AWS and in this history; Reframe deletes nothing.
        project.setdefault('requirements_connector_history', []).append(
            {**recorded, 'replaced_at': time.time(), 'replaced_by': args.by, 'replace_note': args.note})
        recorded = {'source': recorded.get('source') if recorded.get('bucket') == plan['bucket'] else None}
    role_arn, role_created = _role(work, project, plan, args)
    if args.attach_connector:
        connector_id = args.attach_connector
    else:
        response = _once(work, 'connector-' + name, lambda: client.calls([('create_connector', {
            'workspaceId': workspace, 'connectorName': name, 'connectorType': CONNECTOR_TYPE,
            'configuration': plan['configuration'], 'awsAccountId': plan['account'],
            'description': 'Reimagine connector for Reframe project ' + project_name(project) + ', Neptune stack '
                           + plan['stack']})])[0])
        connector_id = response.get('connectorId')
        require(connector_id, 'The connector receipt has no identity; reconcile in Transform and rerun with --attach-connector')
    entry = {'connector_id': connector_id, 'connector_name': None if args.attach_connector else name,
             'connector_type': CONNECTOR_TYPE, 'stack': plan['stack'], 'bucket': plan['bucket'], 'role_arn': role_arn, 'role_created_by_reframe': role_created, 'by': args.by, 'note': args.note,
             'at': recorded.get('at') or time.time(), 'status': recorded.get('status') or 'CREATED',
             'source': recorded.get('source')}
    project['requirements_connector'] = entry
    record, active = _readiness(client, workspace, connector_id, plan, role_arn)
    if not active:
        client.calls([('accept_connector', {'workspaceId': workspace, 'connectorId': connector_id, 'roleArn': role_arn})])
        record, active = _readiness(client, workspace, connector_id, plan, role_arn)
    _save(folder(work) / 'readiness.json', record)
    entry['connector_name'] = entry['connector_name'] or record.get('connectorName')
    entry['status'] = 'ACTIVE' if active else 'ACTIVATION_PENDING'
    if args.copy_source and not same_bucket:
        entry['source'] = copy_source(work, project, plan)
    project.setdefault('events', []).append({'event': 'reimagine_connector_recorded', 'at': time.time(), 'by': args.by,
                                             'note': args.note, 'stack': plan['stack'], 'status': entry['status']})
    result = {'status': 'REIMAGINE_CONNECTOR_' + entry['status'], **summary, 'role_created_by_reframe': role_created,
              'source': entry.get('source')}
    if not active:
        result['next_step'] = ('AWS has not activated the connector yet (a new IAM role can take a minute to propagate). '
                               'Rerun the same command; nothing is created twice.')
    elif not same_bucket and not entry.get('source'):
        result['next_step'] = 'Rerun with --copy-source so the requirements job can read the source from ' + plan['bucket'] + '.'
    else:
        result['next_step'] = 'reframe --workspace ' + str(work) + ' requirements discover --by NAME --note WHY'
    return result


def copy_source(work, project, plan):
    """Put the assessment's own source archive in the connector bucket, after checking its recorded checksum."""
    import reframe as app
    import reframe_requirements as requirements
    from hashlib import sha256
    run = requirements._baseline_run(project)
    uploaded = run.get('uploaded_source') or {}
    record = project['assessments'][project['selected']]
    archive = Path(record['directory']) / 'source.zip'
    require(uploaded.get('sha256') and archive.is_file(), 'The assessment source archive is not saved locally')
    digest = sha256(archive.read_bytes()).hexdigest()
    require(digest == uploaded['sha256'], 'The local source archive differs from the one the assessment uploaded')
    uri = 's3://' + plan['bucket'] + '/reframe/' + str(run.get('run_id') or project['selected']) + '/source.zip'
    _once(work, 'reimagine-source', lambda: app.aws(project, 's3', 'cp', str(archive), uri, '--only-show-errors') or {'uri': uri})
    return {'uri': uri, 'sha256': digest, 'from': uploaded.get('uri')}


def job_source(project, baseline_source):
    """The source URI a requirements job names: the copy in the connector bucket when the buckets differ."""
    entry = project.get('requirements_connector') or {}
    if not entry or entry.get('bucket') == project['aws'].get('bucket'):
        return baseline_source
    copied = (entry.get('source') or {}).get('uri')
    require(copied, 'The reimagine connector reads ' + str(entry.get('bucket')) + ', but the source was not copied there. '
            'Rerun requirements connector with --copy-source.')
    return copied
