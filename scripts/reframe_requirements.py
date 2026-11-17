"""AWS business requirements: capability record, generation job, import, and normalized records.

Nothing here invents an AWS operation, enum value, connector, or schema.

* Documented facts come from the AWS Transform user guide and are labeled as
  documentation, which proves what AWS describes, not what this account allows.
* Tool names are the ones this adapter already calls for assessments. A tool is
  used only when the live MCP server lists it, and its arguments are checked
  against the schema that server returns.
* Business-function choices come from the enum in the selection task's own
  response schema. Requirement files are found by the documented names.
* An offline fixture can exercise this code. Its results are labeled
  offline-fixture and never count as verified generation.
"""
import json
import os
import re
import time
import uuid
from hashlib import sha256
from pathlib import Path

from pilot import Blocked, actor_provenance, require

DOCUMENTATION = {
    'read_on': '2026-11-15',
    'sources': [
        'https://docs.aws.amazon.com/transform/latest/userguide/transform-app-mainframe-workflow.html',
        'https://docs.aws.amazon.com/transform/latest/userguide/transform-app-mainframe-reimagine-supported.html',
        'https://docs.aws.amazon.com/transform/latest/userguide/developer-tools.html',
    ],
}
DOCUMENTED = {
    'service_plan': 'Generate requirements appears in the "Assess and reimagine" and "Reimagine" job plans. It is not listed as a custom-plan capability.',
    'identity': 'AWS Transform refuses operations the signed-in user lacks permission for; only an administrator can cancel or delete a job.',
    'function_catalog': 'Assess identifies business functions; the chat prompts the user to select one or more business functions to reimagine.',
    'operations': 'The MCP server offers 19 tools for workspace, job, HITL task, artifact, connector, chat, and resource operations. The guide does not name the tools used for requirements generation.',
    'connector': 'The mainframe reimagine connector uses an S3 bucket and an Amazon Neptune cluster with VPC networking (two subnets in separate Availability Zones, an S3 gateway endpoint) and a bulk-loader IAM role. The custom-plan S3 connector does not mention Neptune.',
    'reuse': 'Within one job, AWS sends the selected boundaries and assessment outputs to the reimagine flow; selecting another set restarts reimagine for those functions. Reuse across jobs is not documented.',
    'mutations': 'Not documented beyond job creation, human input requests, and the worklog.',
    'formats': 'One requirements.md per selected business function (title, global preconditions, workflow sections with EARS requirements and unique identifiers) and a traceability.yaml mapping business rules to requirements. Coverage files and the S3 layout are not documented.',
    'costs': 'Not documented on these pages. Neptune, VPC, and storage incur separate AWS charges.',
}
ITEMS = tuple(DOCUMENTED)
GENERATE_STEP = 'generate requirements'
FUNCTION_TERM = 'business function'
# Task component the official AWS Transform MCP server names for choosing a job's connector.
CONNECTOR_TASK = 'CreateOrSelectConnectors'
REQUIREMENTS_FILE = 'requirements.md'
TRACEABILITY_FILES = ('traceability.yaml', 'traceability.yml')
# Tools this adapter already calls on AWS Transform for assessments.
ADAPTER_TOOLS = {
    'create_job': 'create_job', 'job_state': 'load_instructions', 'job_status': 'get_job_status',
    'send_message': 'send_message', 'complete_task': 'complete_task',
    'list_resources': 'list_resources', 'get_resource': 'get_resource',
}
STATES = ('NOT_REQUESTED', 'REQUIREMENTS_GENERATION_UNAVAILABLE', 'AUTHORIZED', 'CREATING', 'NEEDS_RECONCILIATION',
          'PLAN_PENDING', 'WAITING_FOR_HUMAN', 'GENERATING', 'STEPS_COMPLETE', 'RETRIEVED', 'IMPORTED', 'FAILED')


def _sha(data):
    """SHA-256 of bytes or text."""
    return sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def _digest(value):
    """SHA-256 of the canonical JSON form of a value."""
    return _sha(json.dumps(value, sort_keys=True, separators=(',', ':')))


def _save(path, value):
    """Write JSON atomically with owner-only permissions."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True))
    temporary.chmod(0o600)
    os.replace(temporary, path)


def _store_bytes(path, data):
    """Write an original artifact once, unchanged. A different existing file is an integrity failure."""
    path = Path(path)
    if path.exists():
        require(path.read_bytes() == data, 'Stored requirement artifact ' + path.name + ' differs from the new copy')
        return
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.write_bytes(data)
    path.chmod(0o600)


def root(work):
    """The folder that holds requirements records for this workspace."""
    return Path(work) / 'requirements'


# Capability record (#169)

def blank_capability():
    """Every item starts documented-only: no fixture coverage, no account observation, no verified generation."""
    return {'schema_version': 1, 'documentation': DOCUMENTATION,
            'items': {item: {'documented': DOCUMENTED[item], 'offline_fixture': False, 'account_verified': False,
                             'observed': None} for item in ITEMS},
            'generation_verified': False, 'discoveries': []}


def capability(work):
    """The saved capability record, or the documented-only default."""
    path = root(work) / 'capability.json'
    return json.loads(path.read_text()) if path.is_file() else blank_capability()


def _observe(record, item, observed, fixture):
    """Record what was observed for one capability item, and whether it came from an offline fixture or this account."""
    entry = record['items'][item]
    entry['observed'] = observed
    if fixture:
        entry['offline_fixture'] = True
    else:
        entry['account_verified'] = True


def _tool_catalog(client):
    """Read-only list of the MCP server's tools and input schemas."""
    tools = client.tools()
    require(isinstance(tools, list), 'MCP tool listing is not a list')
    return {tool['name']: tool.get('inputSchema') or {} for tool in tools if isinstance(tool, dict) and tool.get('name')}


def _enum_values(schema, name):
    """Enum values of one property in a tool input schema, or an empty list.

    Follows local `#/$defs/...` references and `anyOf`/`oneOf` branches, the form the live AWS Transform server uses."""
    defs = schema.get('$defs') or schema.get('definitions') or {}

    def values(node, seen):
        if not isinstance(node, dict):
            return []
        ref = node.get('$ref')
        if isinstance(ref, str) and ref.startswith('#/') and ref not in seen:
            target = defs.get(ref.rsplit('/', 1)[-1]) if ref.split('/')[1] in ('$defs', 'definitions') else None
            return values(target, seen | {ref})
        found = [str(value) for value in node.get('enum') or []]
        for branch in (node.get('anyOf') or []) + (node.get('oneOf') or []):
            found += [value for value in values(branch, seen) if value not in found]
        return found

    return values((schema.get('properties') or {}).get(name) or {}, frozenset())


def discover(work, project, client, by, note):
    """Read-only discovery. Records which tools and connectors the server actually reports; changes nothing in AWS."""
    require(str(by).strip() and str(note).strip(), 'Read-only discovery needs the authorizing owner and a note')
    fixture = bool(getattr(client, 'fixture', False))
    record = capability(work)
    catalog = _tool_catalog(client)
    present = {role: name for role, name in ADAPTER_TOOLS.items() if name in catalog}
    missing = sorted(set(ADAPTER_TOOLS) - set(present))
    observed_ops = {'tools_listed': sorted(catalog), 'adapter_tools_present': present, 'adapter_tools_missing': missing,
                    'schemas': {name: catalog[name] for name in present.values()}}
    if not missing:
        _observe(record, 'operations', observed_ops, fixture)
    else:
        record['items']['operations']['observed'] = observed_ops
    aws = project.get('aws') or {}
    if aws.get('profile') and aws.get('region'):
        _observe(record, 'identity', {'profile': aws['profile'], 'region': aws['region']}, fixture)
    resources = _enum_values(catalog.get('list_resources') or {}, 'resource')
    connector_kind = next((value for value in resources if value.casefold() in {'connector', 'connectors'}), None)
    workspace = ((project.get('settings') or {}).get('transform') or {}).get('workspace_id')
    if connector_kind and workspace:
        listing = client.calls([('list_resources', {'workspaceId': workspace, 'resource': connector_kind})])[-1]
        connectors = listing.get('connectors') or listing.get('items') or []
        summary = [{'id': item.get('connectorId') or item.get('id'), 'type': item.get('connectorType') or item.get('type'),
                    'status': item.get('status') or ((item.get('accountConnection') or {}).get('awsAccountConnection') or {})
                    .get('status')} for item in connectors if isinstance(item, dict)]
        # Only the observed reimagine type counts, and only once AWS has activated it.
        from reframe_reimagine import CONNECTOR_TYPE
        for item in summary:
            # The live listing carries no status; AWS reports it only on the connector record (read-only).
            if item.get('type') == CONNECTOR_TYPE and item.get('status') is None and item.get('id'):
                detail = client.calls([('get_resource', {'resource': 'connector', 'workspaceId': workspace,
                                                         'connectorId': item['id']})])[0]
                item['status'] = ((detail.get('accountConnection') or {}).get('awsAccountConnection') or {}).get('status')
        reimagine = [item for item in summary if item.get('type') == CONNECTOR_TYPE and item.get('status') == 'ACTIVE']
        observed = {'resource_kind': connector_kind, 'connectors': summary, 'reimagine_connectors': reimagine}
        if reimagine:
            _observe(record, 'connector', observed, fixture)
        else:
            record['items']['connector']['observed'] = observed
    elif 'list_resources' in catalog:
        reason = ('No Transform workspace is recorded for this project' if connector_kind
                  else 'list_resources declares no connector resource kind')
        record['items']['connector']['observed'] = {'resource_kind': connector_kind, 'connectors_listed': False, 'reason': reason}
    record['discoveries'].append({'at': time.time(), 'by': by, 'note': note, 'evidence': 'offline-fixture' if fixture else 'live',
                                  'read_only': True})
    _save(root(work) / 'capability.json', record)
    project['requirements_capability'] = {'path': 'requirements/capability.json', 'status': generation_status(record)['status']}
    return record


def generation_status(record):
    """Say whether integrated generation may be requested, and exactly which evidence is missing."""
    items = record['items']
    def ready(item):
        return items[item]['account_verified'] or items[item]['offline_fixture']
    missing = [item for item in ('operations', 'connector', 'identity') if not ready(item)]
    level = 'live' if all(items[i]['account_verified'] for i in ('operations', 'connector', 'identity')) else (
        'offline-fixture' if not missing else None)
    if missing:
        return {'status': 'REQUIREMENTS_GENERATION_UNAVAILABLE', 'missing': missing, 'evidence_level': None,
                'generation_verified': record.get('generation_verified', False),
                'reason': 'Integrated AWS requirements generation is not verified for this account: '
                          + ', '.join(missing) + ' not observed. Documentation alone is not verification.'}
    return {'status': 'GENERATION_REQUESTABLE', 'missing': [], 'evidence_level': level,
            'generation_verified': record.get('generation_verified', False)}


def require_requestable(work):
    """Stop with REQUIREMENTS_GENERATION_UNAVAILABLE when generation cannot be requested (#170)."""
    status = generation_status(capability(work))
    if status['status'] != 'GENERATION_REQUESTABLE':
        from reframe_states import stop
        stop(status['reason'], 'REQUIREMENTS_GENERATION_UNAVAILABLE',
             hint='Record read-only discovery with an owner authorization, or import externally generated requirements '
                  'with reframe --workspace WORKSPACE requirements import. An import is labeled imported, not generated.')
    return status


# Generation job (#173)

def job_path(work, label):
    """Where one requirements job record is saved."""
    return root(work) / 'jobs' / label / 'job.json'


def authorize_job(work, project, functions, by, note):
    """Record an explicit, scoped authorization for one new requirements job. Nothing is sent to AWS here."""
    status = require_requestable(work)
    require(str(by).strip() and str(note).strip(), 'A new requirements job needs a named owner and a note')
    require(project.get('selected'), 'Approve the assessment baseline first')
    label = 'requirements-' + str(len(list((root(work) / 'jobs').glob('*'))) + 1) if (root(work) / 'jobs').is_dir() else 'requirements-1'
    run = _baseline_run(project)
    job = {'label': label, 'state': 'AUTHORIZED', 'evidence_level': status['evidence_level'],
           'authorization': {'by': by, 'note': note, 'at': time.time(), 'functions_requested': list(functions or [])},
           'baseline': {'assessment_label': project['selected'], 'assessment_sha256': project['assessments'][project['selected']]['sha256'],
                        'source_commit': (project.get('source') or {}).get('commit'),
                        'uploaded_source': run.get('uploaded_source')},
           'run_id': new_run_id(), 'job_id': None, 'create_pending': False, 'selected_functions': [], 'catalog': [], 'events': []}
    _save(job_path(work, label), job)
    project.setdefault('requirements', {}).update(state='AUTHORIZED', active_job=label)
    return job


def new_run_id():
    """A job identity in the form assessment runs use: RUN- and 16 hex characters."""
    return 'RUN-' + uuid.uuid4().hex[:16]


def _baseline_run(project):
    """The selected assessment's run record."""
    from reframe import read
    record = project['assessments'][project['selected']]
    return read(Path(record['directory']) / 'run.json')


def _identity(project, job):
    """The Transform workspace and job ids for one requirements job."""
    workspace = ((project.get('settings') or {}).get('transform') or {}).get('workspace_id')
    require(workspace, 'The Transform workspace is not configured')
    return {'workspaceId': workspace, 'jobId': job['job_id']}


def _check_schema(record, tool, arguments):
    """Arguments must satisfy the schema the server reported during discovery."""
    schema = ((record['items']['operations'].get('observed') or {}).get('schemas') or {}).get(tool)
    require(isinstance(schema, dict), 'No observed schema for ' + tool + '; run read-only discovery first')
    required = schema.get('required') or []
    allowed = set((schema.get('properties') or {}))
    require(all(key in arguments for key in required), 'Arguments for ' + tool + ' miss required fields ' + str(required))
    require(not set(arguments) - allowed, 'Unrecognized arguments for ' + tool + '; nothing is guessed')


def step(work, project, client, selected=None, plan=None, reply=None, by=None):
    """Advance the active requirements job by one saved step. A finished job is not rerun."""
    label = (project.get('requirements') or {}).get('active_job')
    require(label, 'No requirements job is authorized')
    job = json.loads(job_path(work, label).read_text())
    record = capability(work)
    if job['state'] in {'RETRIEVED', 'FAILED'}:
        return job
    directory = job_path(work, label).parent
    if not job['job_id']:
        receipt = directory / 'create-job-receipt.json'
        if receipt.is_file():
            response = json.loads(receipt.read_text())
            import kiro_workflow as kw
            found = kw.recorded_job_id(response)
            if found:
                job.update(job_id=found, create_pending=False, state='PLAN_PENDING')
            else:
                job.update(state='NEEDS_RECONCILIATION', reason='Requirements job creation has no successful receipt. '
                                                                'Attach the existing job; another is never created.')
                _save(job_path(work, label), job)
                return job
        elif job['create_pending']:
            job.update(state='NEEDS_RECONCILIATION', reason='Requirements job creation outcome uncertain.')
            _save(job_path(work, label), job)
            return job
        else:
            # AWS job names follow the assessment runs: RUN- and 16 hex characters.
            job.setdefault('run_id', new_run_id())
            source = (job['baseline'].get('uploaded_source') or {}).get('uri')
            require(source, 'The assessment baseline has no recorded source upload to reuse')
            from reframe_reimagine import job_source
            source = job_source(project, source)
            arguments = {'workspaceId': _identity(project, {'job_id': None})['workspaceId'], 'jobName': job['run_id'],
                         'objective': ('Assess and reimagine the source archive at ' + source + ' for the business functions '
                                       'selected in this job, and generate requirements with traceability. '
                                       'Source commit ' + str(job['baseline']['source_commit']) + '.'),
                         'intent': 'Generate business requirements for selected business functions; preserve human selection tasks.'}
            # The live service rejects a job without an orchestrator although the schema marks it optional.
            # Reuse the one the baseline assessment recorded, else the one mainframe orchestrator AWS lists.
            import kiro_workflow as kw
            baseline = ((_baseline_run(project).get('settings') or {}).get('transform') or {}).get('orchestrator_agent')
            arguments['orchestratorAgent'] = kw.select_orchestrator(
                {'settings': {'transform': {'orchestrator_agent': baseline} if baseline else {}}, 'events': job['events']}, client)
            job['orchestrator_agent'] = arguments['orchestratorAgent']
            _check_schema(record, ADAPTER_TOOLS['create_job'], arguments)
            job.update(state='CREATING', create_pending=True)
            _save(job_path(work, label), job)
            _save(receipt, {'accepted': False, 'label': label})
            response = client.calls([(ADAPTER_TOOLS['create_job'], arguments)])[0]
            _save(receipt, response)
            import kiro_workflow as kw
            job.update(job_id=kw.nested_job(response)['jobId'], create_pending=False, state='PLAN_PENDING')
            _save(job_path(work, label), job)
    identity = _identity(project, job)
    snapshot = client.calls([(ADAPTER_TOOLS['job_state'], identity),
                             (ADAPTER_TOOLS['job_status'], {**identity, 'detailed': True})])[-1]
    _save(directory / 'job-status.json', snapshot)
    import kiro_workflow as kw
    detail = kw.nested_job(snapshot)
    # The live job reports its status under statusDetails, as the assessment path already reads it.
    details = detail.get('statusDetails') or {}
    status = str(detail.get('status') or (details.get('status') if isinstance(details, dict) else details) or 'UNKNOWN').upper()
    steps = [item for item in (snapshot.get('plan') or {}).get('steps') or [] if isinstance(item, dict)]
    names = [str(item.get('stepName') or '') for item in steps]
    job['service_status'] = status
    job['plan_steps'] = [{'name': item.get('stepName'), 'status': item.get('status')} for item in steps]
    if steps and not any(name.casefold() == GENERATE_STEP for name in names):
        job.update(state='FAILED', reason='The job plan has no "Generate requirements" step. Observed steps: ' + ', '.join(names))
        _save(job_path(work, label), job)
        from reframe_states import stop
        stop(job['reason'] + '. Integrated generation is not available through this plan.', 'CAPABILITY_UNVERIFIED')
    if steps and job['evidence_level'] == 'live':
        _observe(record, 'service_plan', {'plan_steps': names}, False)
        _save(root(work) / 'capability.json', record)
    if not steps and _answer_chat(work, record, client, job, identity, snapshot, plan, reply, by):
        _save(job_path(work, label), job)
        return job
    container = snapshot.get('tasks') or {}
    tasks = container.get('hitlTasks', []) if isinstance(container, dict) else container if isinstance(container, list) else []
    waiting = [task for task in tasks if isinstance(task, dict) and task.get('status') in
               {'AWAITING_HUMAN_INPUT', 'PENDING_HUMAN_INPUT', 'AWAITING_APPROVAL'}]
    for task in waiting:
        if _answer_connector(work, project, client, job, task, identity):
            continue
        if not _answer_selection(work, project, client, job, task, identity, selected):
            job.update(state='WAITING_FOR_HUMAN', reason='AWS presents a human task this adapter does not answer: '
                       + str(task.get('title') or task.get('uxComponentId') or task.get('taskId')))
            _save(job_path(work, label), job)
            return job
    generate = next((item for item in steps if str(item.get('stepName')).casefold() == GENERATE_STEP), None)
    steps_done = bool(steps) and all(str(item.get('status')).upper() in {'COMPLETED', 'SUCCEEDED'} for item in steps)
    terminal = status in {'COMPLETED', 'SUCCEEDED'}
    job['completion'] = {'authorized_steps_complete': steps_done, 'job_terminal': terminal, 'service_job_status': status}
    if status in {'FAILED', 'STOPPED', 'CANCELLED'}:
        job.update(state='FAILED', reason='AWS stopped the requirements job: ' + status)
    elif generate and str(generate.get('status')).upper() in {'COMPLETED', 'SUCCEEDED'}:
        job['state'] = 'STEPS_COMPLETE'
        _save(job_path(work, label), job)
        return retrieve(work, project, client, job)
    elif job['state'] not in {'WAITING_FOR_HUMAN'}:
        job['state'] = 'GENERATING'
    _save(job_path(work, label), job)
    return job


PLAN_OPTION = re.compile(r'^\s*(\d+)\.\s+([^:\n]+?)\s*(?::|$)', re.M)
CHAT_LIMIT = 7000  # send_message: "max 7000 chars"


def _open_question(snapshot):
    """AWS's latest chat message when it asks a question no one has answered: (message, numbered options) or None."""
    messages = [m for m in ((snapshot.get('messages') or {}).get('messages') or []) if isinstance(m, dict)]
    system = [m for m in messages if m.get('messageOrigin') == 'SYSTEM'
              and (m.get('processingInfo') or {}).get('messageType') == 'FINAL_RESPONSE']
    if not system:
        return None
    latest = max(system, key=lambda m: str(m.get('createdAt', '')))
    text = str(latest.get('text') or '').strip()
    answered = any(m.get('messageOrigin') != 'SYSTEM' and str(m.get('createdAt', '')) > str(latest.get('createdAt', ''))
                   for m in messages)
    if answered or not text.endswith('?'):
        return None
    options = [(number, label.strip()) for number, label in PLAN_OPTION.findall(text)]
    return latest, options if len(options) >= 2 else []


def _answer_chat(work, record, client, job, identity, snapshot, plan, reply, by):
    """Answer AWS's open chat question once, with a named person's choice or words. True when this step ends here.

    A numbered menu takes only an option it lists (--plan), sent as AWS numbered and worded it. Any other question
    takes the person's own reply (--reply). Nothing is answered without a person, and no question is answered twice.
    """
    question = _open_question(snapshot)
    if not question:
        return False
    message, options = question
    message_id = message.get('messageId')
    require(message_id, 'The AWS question has no message identity; inspect the job chat privately')
    labels = [label for _, label in options]
    directory = job_path(work, job['label']).parent
    intent, receipt = directory / ('chat-intent-' + message_id + '.json'), directory / ('chat-receipt-' + message_id + '.json')
    legacy = directory / 'plan-receipt.json'
    if receipt.is_file() or (legacy.is_file() and json.loads(legacy.read_text()).get('reply_to') == message_id):
        return False
    if intent.is_file():
        job.update(state='NEEDS_RECONCILIATION', reason='The reply to AWS is uncertain. Check the job chat; '
                                                        'Reframe never sends it again.')
        return True
    job['question'] = {'message_id': message_id, 'text': str(message.get('text') or '')[-2000:], 'options': labels}
    if options:
        if not plan:
            job.update(state='WAITING_FOR_HUMAN', plan_options=labels,
                       reason='AWS asks which plan to run. Choose one with requirements resume --plan NAME --by NAME: '
                              + ', '.join(labels))
            return True
        require(not reply, 'AWS offers a numbered menu; choose with --plan, not --reply')
        chosen = next(((number, label) for number, label in options if label.casefold() == plan.strip().casefold()), None)
        require(chosen, 'AWS does not offer that plan. Options: ' + ', '.join(labels))
        text = chosen[0] + '. ' + chosen[1]
    else:
        require(not plan, 'AWS is not offering a plan menu; answer its question with --reply')
        if not str(reply or '').strip():
            job.update(state='WAITING_FOR_HUMAN', reason='AWS asks: "' + job['question']['text'][-400:]
                       + '" Answer with requirements resume --reply TEXT --by NAME')
            return True
        text = reply.strip()
        require(len(text) <= CHAT_LIMIT, 'The reply exceeds the AWS job chat limit')
    require(str(by or '').strip(), 'A reply to AWS needs a named person: add --by')
    arguments = {**identity, 'text': text, 'skipPolling': True}
    _check_schema(record, ADAPTER_TOOLS['send_message'], arguments)
    _save(intent, {'reply_to': message_id, 'text': text, 'by': by, 'at': time.time()})
    response = client.calls([(ADAPTER_TOOLS['job_state'], identity), (ADAPTER_TOOLS['send_message'], arguments)])[-1]
    _save(receipt, {'reply_to': message_id, 'text': text, 'response': response})
    entry = {'reply_to': message_id, 'text': text, 'by': by, 'at': time.time(), **actor_provenance()}
    job.setdefault('chat_replies', []).append(entry)
    if options:
        job['plan_choice'] = {'option': chosen[1], 'by': by, 'at': entry['at'], **actor_provenance()}
    job['events'].append({'event': 'aws_question_answered', 'at': entry['at'], 'by': by,
                          **({'option': chosen[1]} if options else {})})
    job.pop('question', None)
    job.update(state='PLAN_PENDING', reason='Reply sent to AWS; resume to follow the job.')
    return True


def _selection_options(task):
    """Enum options from a task's own response schema, and the property that holds them."""
    schema = task.get('_outputSchema') or {}
    for name, prop in (schema.get('properties') or {}).items():
        if not isinstance(prop, dict):
            continue
        if prop.get('type') == 'array' and isinstance((prop.get('items') or {}).get('enum'), list):
            return name, [str(v) for v in prop['items']['enum']], True
        if isinstance(prop.get('enum'), list):
            return name, [str(v) for v in prop['enum']], False
    return None, [], False


def _answer_connector(work, project, client, job, task, identity):
    """Answer a connector task with the recorded, active reimagine connector, and only when its schema asks for that."""
    entry = project.get('requirements_connector') or {}
    if task.get('uxComponentId') != CONNECTOR_TASK or entry.get('status') != 'ACTIVE':
        return False
    task_id = task.get('taskId')
    directory = job_path(work, job['label']).parent
    receipt = directory / ('connector-receipt-' + str(task_id) + '.json')
    if receipt.is_file():
        return True
    record = client.calls([(ADAPTER_TOOLS['job_state'], identity),
                           (ADAPTER_TOOLS['get_resource'], {**identity, 'resource': 'task', 'taskId': task_id})])[-1]
    detail = record.get('task') or {}
    schema = detail.get('_outputSchema') or {}
    content = {'connectorId': entry['connector_id'], 'connectorType': entry['connector_type']}
    if not set(schema.get('required') or []) <= set(content) or not set(content) <= set(schema.get('properties') or content):
        return False
    _save(directory / ('connector-task-' + str(task_id) + '.json'), record)
    _save(directory / ('connector-intent-' + str(task_id) + '.json'), {'task_id': task_id, 'content': content})
    response = client.calls([(ADAPTER_TOOLS['job_state'], identity), (ADAPTER_TOOLS['complete_task'], {
        **identity, 'taskId': task_id, 'content': json.dumps(content), 'action': 'APPROVE'})])[-1]
    _save(receipt, response)
    job['events'].append({'event': 'connector_selected', 'at': time.time(), 'connector_type': entry['connector_type']})
    return True


def _answer_selection(work, project, client, job, task, identity, selected):
    """Answer only a business-function selection task, only with values its schema offers."""
    task_id = task.get('taskId')
    record = client.calls([(ADAPTER_TOOLS['job_state'], identity),
                           (ADAPTER_TOOLS['get_resource'], {**identity, 'resource': 'task', 'taskId': task_id})])[-1]
    detail = record.get('task') or {}
    text = ' '.join(str(detail.get(key) or '') for key in ('title', 'description', 'uxComponentId')).casefold()
    if FUNCTION_TERM not in text:
        return False
    field, options, multiple = _selection_options(detail)
    if not options:
        return False
    job['catalog'] = options
    directory = job_path(work, job['label']).parent
    _save(directory / ('selection-task-' + str(task_id) + '.json'), record)
    chosen = list(selected or job['authorization']['functions_requested'] or [])
    if not chosen:
        job.update(state='WAITING_FOR_HUMAN', reason='Choose business functions from the catalog: ' + ', '.join(options))
        _save(job_path(work, job['label']), job)
        return True
    unknown = [item for item in chosen if item not in options]
    require(not unknown, 'Selected functions are not in the task schema: ' + ', '.join(unknown))
    require(multiple or len(chosen) == 1, 'This selection task accepts one function')
    content = {field: chosen if multiple else chosen[0]}
    receipt = directory / ('selection-receipt-' + str(task_id) + '.json')
    if receipt.is_file():
        return True
    _save(directory / ('selection-intent-' + str(task_id) + '.json'), {'task_id': task_id, 'content': content})
    response = client.calls([(ADAPTER_TOOLS['job_state'], identity), (ADAPTER_TOOLS['complete_task'], {
        **identity, 'taskId': task_id, 'content': json.dumps(content), 'action': 'APPROVE'})])[-1]
    _save(receipt, response)
    job['selected_functions'] = chosen
    job['events'].append({'event': 'functions_selected', 'at': time.time(), 'functions': chosen})
    return True


def retrieve(work, project, client, job):
    """Download the generated files by their documented names and seal them as one requirements set."""
    import kiro_workflow as kw
    directory = job_path(work, job['label']).parent
    identity = _identity(project, job)
    listing = kw.list_assessment_exports(directory, client, identity)
    wanted = [item for item in listing['assets'] if Path(item['assetKey']).name.casefold() in
              {REQUIREMENTS_FILE, *TRACEABILITY_FILES}]
    require(wanted, 'The finished job lists no requirements.md or traceability.yaml. Nothing was imported.')
    target = directory / 'downloads'
    target.mkdir(parents=True, exist_ok=True, mode=0o700)
    originals = []
    for index, item in enumerate(wanted):
        filename = str(index) + '-' + Path(item['assetKey']).name
        path = target / filename
        if path.exists():
            path.unlink()  # Never mistake an earlier failed download for this one.
        client.calls([(ADAPTER_TOOLS['job_state'], identity), (ADAPTER_TOOLS['get_resource'], {
            **identity, 'resource': 'asset', 'assetKey': item['assetKey'], 'connectorId': item['connectorId'],
            'savePath': str(target), 'fileName': filename})])
        require(path.is_file() and not path.is_symlink(), 'Requirements download did not produce ' + item['assetKey'])
        function_id = _function_from_key(item['assetKey'], job['selected_functions'])
        originals.append({'function_id': function_id, 'original_path': item['assetKey'], 'data': path.read_bytes()})
    set_id = record_set(work, project, originals, origin='aws-generated', evidence_level=job['evidence_level'],
                        producing_job_id=job['job_id'], functions=job['selected_functions'],
                        service_status=job.get('completion'))
    job.update(state='RETRIEVED', requirements_set=set_id)
    _save(job_path(work, job['label']), job)
    if job['evidence_level'] == 'live':
        record = capability(work)
        record['generation_verified'] = True
        _observe(record, 'formats', {'files': [o['original_path'] for o in originals]}, False)
        _save(root(work) / 'capability.json', record)
    return job


def _function_from_key(key, functions):
    """The selected function whose id appears as a folder in the asset key, else unassigned."""
    parts = Path(key).parts
    for function in functions:
        if function in parts:
            return function
    return 'unassigned' if len(functions) != 1 else functions[0]


# Import and requirement sets (#171, #172)

def record_set(work, project, originals, origin, evidence_level, producing_job_id=None, functions=None,
               service_status=None, by=None, note=None):
    """Seal original files unchanged, normalize them, and make the set the project's requirements evidence."""
    require(originals, 'A requirements set needs at least one file')
    source = project.get('source') or {}
    files = []
    for item in originals:
        data = item['data']
        name = Path(item['original_path']).name
        require(name.casefold() in {REQUIREMENTS_FILE, *TRACEABILITY_FILES}, 'Unsupported requirements file name: ' + name)
        files.append({'function_id': item['function_id'], 'kind': 'traceability' if name.casefold() in TRACEABILITY_FILES else 'requirements',
                      'original_path': item['original_path'], 'sha256': _sha(data), 'bytes': len(data)})
    set_id = _digest({'files': files, 'origin': origin, 'job': producing_job_id})[:16]
    folder = root(work) / 'sets' / set_id
    for item, entry in zip(originals, files):
        stored = folder / 'originals' / entry['function_id'] / Path(entry['original_path']).name
        _store_bytes(stored, item['data'])
        entry['stored_path'] = str(stored.relative_to(work))
    normalized = normalize(work, project, files)
    _save(folder / 'normalized.json', normalized)
    manifest = {'set_id': set_id, 'origin': origin, 'evidence_level': evidence_level,
                'generated_by_reframe': origin == 'aws-generated',
                'source': {'repository': source.get('repository'), 'commit': source.get('commit')},
                'assessment_sha256': project['assessments'][project['selected']]['sha256'] if project.get('selected') else None,
                'producing_job_id': producing_job_id, 'function_ids': sorted({f['function_id'] for f in files}),
                'service_status': service_status, 'files': files, 'recorded_at': time.time(),
                'normalized': {'path': str((folder / 'normalized.json').relative_to(work)),
                               'sha256': _sha((folder / 'normalized.json').read_bytes())}}
    if by:
        manifest['imported_by'] = {'by': by, 'note': note, **actor_provenance()}
    _save(folder / 'manifest.json', manifest)
    previous = (project.get('requirements') or {}).get('manifest')
    history = (project.get('requirements') or {}).get('history') or []
    if previous and previous != str((folder / 'manifest.json').relative_to(work)):
        history = history + [previous]
    project['requirements'] = {**(project.get('requirements') or {}), 'state': 'RETRIEVED' if origin == 'aws-generated' else 'IMPORTED',
                               'manifest': str((folder / 'manifest.json').relative_to(work)), 'set_id': set_id,
                               'origin': origin, 'evidence_level': evidence_level, 'history': history}
    if project.get('specification'):
        import reframe_versions as versions
        moved = versions.supersede(project, ('validation', 'specifications', 'design', 'package'), 'requirements_' + origin)
        project['requirements']['requires_revalidation'] = True
        project['requirements']['superseded_approvals'] = moved
    return set_id


def import_files(work, project, requirements_file, traceability_file, function_id, by, origin_note, job_id=None):
    """Import externally generated requirements. They are labeled imported and never presented as generated."""
    require(str(by).strip() and str(origin_note).strip(), 'An import needs a named owner and a note on where the files came from')
    require(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,80}', str(function_id or '')), 'Name the business function id')
    originals = []
    for path in (requirements_file, traceability_file):
        if not path:
            continue
        path = Path(path).expanduser()
        require(path.is_file() and not path.is_symlink(), 'Import file not found: ' + str(path))
        require(path.stat().st_size <= 5_000_000, 'Import file is larger than 5 MB')
        originals.append({'function_id': function_id, 'original_path': path.name, 'data': path.read_bytes()})
    require(any(Path(o['original_path']).name.casefold() == REQUIREMENTS_FILE for o in originals),
            'An import needs a requirements.md file')
    return record_set(work, project, originals, origin='imported', evidence_level='imported',
                      producing_job_id=job_id, functions=[function_id], by=by, note=origin_note)


# The last segment may carry a letter prefix, so F1-R1 is read as well as REQ-1.
REQ_ID = re.compile(r'\b([A-Z][A-Z0-9]*(?:[-_.][A-Z0-9]+)*[-_.][A-Z]*\d+[A-Z0-9]*)\b')
EARS = re.compile(r'\b(shall|SHALL)\b')


def _requirements(text, function_id):
    """Requirement records with stable namespaced ids.

    Two shapes are read: a line with an id and 'shall', and a heading that names an id followed by its text.
    Other lines that name an id are counted as unrecognized, never dropped silently.
    """
    records, section, seen, unrecognized = [], None, {}, []
    lines = text.splitlines()
    current = None
    for number, line in enumerate(lines, 1):
        heading = re.match(r'^\s*#{1,6}\s+(.*)$', line)
        if heading:
            current = None
            title = heading.group(1).strip()
            match = REQ_ID.search(title)
            if match:
                original = match.group(1)
                current = {'id': 'aws-req:' + function_id + ':' + original, 'original_id': original,
                           'function_id': function_id, 'section': section, 'text': title, 'line': number,
                           'shape': 'heading', 'acceptance_criteria': [], 'uncertainty': None, 'disposition': 'unreviewed'}
                seen[original] = seen.get(original, 0) + 1
                records.append(current)
            else:
                section = title
            continue
        match = REQ_ID.search(line)
        if match and EARS.search(line):
            current = None
            original = match.group(1)
            seen[original] = seen.get(original, 0) + 1
            records.append({'id': 'aws-req:' + function_id + ':' + original, 'original_id': original, 'function_id': function_id,
                            'section': section, 'text': line.strip(), 'line': number, 'shape': 'statement',
                            'acceptance_criteria': [], 'uncertainty': None, 'disposition': 'unreviewed'})
            continue
        criterion = re.match(r'^\s*(?:[-*]\s+)?(?:acceptance(?:\s+criteri(?:on|a))?|AC)\s*:\s*(.*)$', line, re.IGNORECASE)
        if current is not None and criterion:
            # Supplied acceptance criteria are kept as criteria, not folded into the requirement text.
            current['in_acceptance'] = True
            if criterion.group(1).strip():
                current['acceptance_criteria'].append(criterion.group(1).strip())
            continue
        if current is not None and current.get('in_acceptance') and re.match(r'^\s*[-*]\s+\S', line):
            current['acceptance_criteria'].append(re.sub(r'^\s*[-*]\s+', '', line).strip())
            continue
        if current is not None and line.strip():
            current.pop('in_acceptance', None)
            current['text'] = (current['text'] + ' ' + line.strip()).strip()
            continue
        if match:
            unrecognized.append({'line': number, 'id': match.group(1)})
    for item in records:
        item.pop('in_acceptance', None)
        if seen[item['original_id']] > 1:
            item['uncertainty'] = 'duplicate identifier in the source file'
        if item.get('shape') == 'heading' and not EARS.search(item['text']):
            item['uncertainty'] = item['uncertainty'] or 'no "shall" statement; read from a heading and its text'
    return records, unrecognized


def _trace_blocks(text):
    """Split YAML text into one block per traced item without a YAML parser. Unknown shapes stay unparsed.

    A top-level key per requirement is one block. A top-level list of mappings (- id: F1-R1) is split into its
    items, so one item's rules and sources never attach to another id.
    """
    blocks = []
    for block in _top_level_blocks(text):
        blocks += _list_items(block) or [block]
    return blocks


def _list_items(block):
    """The items of a list of mappings directly under a top-level key, or [] for any other shape."""
    lines = block.splitlines()
    depth = lambda line: len(line) - len(line.lstrip())
    children = [line for line in lines[1:] if line.strip() and not line.lstrip().startswith('#')]
    if not children:
        return []
    indent = min(depth(line) for line in children)
    starts = [index for index, line in enumerate(lines)
              if index and depth(line) == indent and re.match(r'^\s*-\s+[\w.-]+\s*:', line)]
    if not starts or any(depth(line) == indent and not line.lstrip().startswith('-') for line in children):
        return []
    return ['\n'.join(lines[start:(starts[n + 1] if n + 1 < len(starts) else len(lines))]) for n, start in enumerate(starts)]


def _top_level_blocks(text):
    """Split YAML text at its top-level keys."""
    blocks, current = [], []
    for line in text.splitlines():
        if line and not line[0].isspace() and not line.startswith('#') and current:
            blocks.append('\n'.join(current))
            current = []
        if line.strip():
            current.append(line)
    if current:
        blocks.append('\n'.join(current))
    return blocks


def _rule_tokens(block):
    """Rule ids listed under a key whose name contains 'rule', inline ([R1, R2]) or as indented '- R1' items."""
    tokens, lines = [], block.splitlines()
    for index, line in enumerate(lines):
        match = re.match(r'^(\s*)[\w.-]*rule[\w.-]*\s*:\s*(.*)$', line, re.IGNORECASE)
        if not match:
            continue
        indent, rest = len(match.group(1)), match.group(2).strip()
        if rest:
            tokens += [t for t in re.split(r'[\[\],\s]+', rest) if t and t not in {'-', '[]'}]
            continue
        for item in lines[index + 1:]:
            if not item.strip():
                continue
            depth = len(item) - len(item.lstrip())
            if depth <= indent:
                break
            bullet = re.match(r'^\s*-\s*(?:id\s*:\s*)?([^\s#]+)', item)
            if bullet:
                tokens.append(bullet.group(1).strip('\'"'))
    return [t.strip('\'"') for t in tokens]


def normalize(work, project, files):
    """Namespaced requirement records with honest traceability states: mapped, partial, missing, ambiguous, unsupported."""
    rule_ids = set()
    try:
        from reframe import spec_path, read
        if project.get('specification'):
            rule_ids = {rule.get('id') for rule in read(spec_path(work, project)).get('rules') or []}
    except (Blocked, OSError, ValueError, KeyError):
        rule_ids = set()
    source_root = Path((project.get('source') or {}).get('root') or '.')
    requirements, traces, unrecognized = [], {}, []
    for entry in files:
        data = (Path(work) / entry['stored_path']).read_text(errors='replace') if entry.get('stored_path') else ''
        if entry['kind'] == 'requirements':
            found, skipped = _requirements(data, entry['function_id'])
            requirements += found
            unrecognized += [{**item, 'file': entry['stored_path']} for item in skipped]
        else:
            traces.setdefault(entry['function_id'], []).append(data)
    for item in requirements:
        blocks = [block for text in traces.get(item['function_id'], []) for block in _trace_blocks(text)
                  if re.search(r'\b' + re.escape(item['original_id']) + r'\b', block)]
        if not traces.get(item['function_id']):
            item['traceability'] = {'state': 'missing', 'reason': 'no traceability file for this function'}
            continue
        if not blocks:
            item['traceability'] = {'state': 'missing', 'reason': 'identifier not found in traceability'}
            continue
        rules = sorted({token for block in blocks for token in _rule_tokens(block)} - {item['original_id']})
        paths = sorted({m for block in blocks for m in re.findall(r'[\w./-]+\.(?:cbl|cob|cpy|jcl|bms|pli|txt)\b', block, re.IGNORECASE)})
        linked = [path for path in paths if (source_root / path).is_file()]
        state = 'ambiguous' if len(blocks) > 1 else ('mapped' if rules and paths else ('partial' if rules or paths else 'unsupported'))
        item['traceability'] = {'state': state, 'rule_ids': rules, 'known_rule_ids': sorted(set(rules) & rule_ids),
                                'source_paths': paths, 'source_paths_in_pin': linked,
                                'evidence_status': 'TRACEABILITY_CLAIM'}
    warnings = []
    if not requirements:
        warnings.append('No requirement records were recognized. The original files are kept unchanged. '
                        'Reframe reads a line with an id and "shall", or a heading that names an id.')
    if unrecognized:
        warnings.append(str(len(unrecognized)) + ' lines name an id but are not in a recognized requirement shape; '
                        'they are listed in unrecognized_lines and kept in the original file.')
    return {'schema_version': 1, 'requirements': requirements, 'unrecognized_lines': unrecognized, 'warnings': warnings,
            'counts': {'requirements': len(requirements), 'unrecognized_lines': len(unrecognized),
                       'by_traceability': {state: sum(1 for r in requirements if (r.get('traceability') or {}).get('state') == state)
                                           for state in ('mapped', 'partial', 'missing', 'ambiguous', 'unsupported')}},
            'note': 'Traceability is the producer\'s claim. It is not SOURCE_VERIFIED until independent validation checks it.'}


def active_set(work, project):
    """The manifest and normalized records of the project's current requirements set, or an explicit absence."""
    record = project.get('requirements') or {}
    if not record.get('manifest'):
        return {'state': record.get('state') or 'NOT_REQUESTED', 'requirements': [], 'manifest': None}
    manifest = json.loads((Path(work) / record['manifest']).read_text())
    normalized_path = Path(work) / manifest['normalized']['path']
    require(_sha(normalized_path.read_bytes()) == manifest['normalized']['sha256'], 'Normalized requirements changed after sealing')
    for entry in manifest['files']:
        require(_sha((Path(work) / entry['stored_path']).read_bytes()) == entry['sha256'], 'Stored requirement file changed: ' + entry['stored_path'])
    return {'state': record.get('state'), 'manifest': manifest,
            'requirements': json.loads(normalized_path.read_text())['requirements']}


def provenance_statement(work, project):
    """One sentence for reports and packages: generated, imported, unavailable, or not requested."""
    record = project.get('requirements') or {}
    status = generation_status(capability(work))
    if record.get('origin') == 'aws-generated':
        level = record.get('evidence_level')
        return ('Requirements were generated by an AWS Transform job and retrieved unchanged'
                + (' (offline fixture; not live evidence).' if level == 'offline-fixture' else '.'))
    if record.get('origin') == 'imported':
        return ('Requirements were imported from outside Reframe and stored unchanged. Reframe did not generate them. '
                'Integrated generation status: ' + status['status'] + '.')
    return ('No requirements set is recorded. Integrated generation status: ' + status['status']
            + '. Business-rule extraction is not requirements.')
