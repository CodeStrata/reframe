"""Typed stop causes, recovery classes, and the one-screen status summary.

A stop says why work paused and what kind of action resumes it. The cause is
attached where the stop is raised when the code knows it, and otherwise is
classified from the message so older stops still carry a cause.
"""
import json
import os
import re
import time
from pathlib import Path

from pilot import Blocked

# Recovery classes. Only "automatic" may continue without a person.
AUTOMATIC = 'automatic'
AUTHORIZATION = 'authorization'
EVIDENCE_REPAIR = 'evidence_repair'
HUMAN_DECISION = 'human_decision'
PROVIDER = 'provider'
INTEGRITY = 'integrity'
RECONCILIATION = 'reconciliation'
CAPABILITY = 'capability'
INPUT = 'input'

CAUSES = {
    'HUMAN_DECISION_REQUIRED': HUMAN_DECISION,
    'CONTEXT_CONFLICT': HUMAN_DECISION,
    'NO_PROGRESS': HUMAN_DECISION,
    'AUTHORIZATION_REQUIRED': AUTHORIZATION,
    'ALLOWANCE_EXHAUSTED': AUTHORIZATION,
    'DOLLAR_CAP': AUTHORIZATION,
    'EVIDENCE_MISSING': EVIDENCE_REPAIR,
    'CONTEXT_LIMIT': EVIDENCE_REPAIR,
    'INTEGRITY_FAILURE': INTEGRITY,
    'PROVIDER_UNAVAILABLE': PROVIDER,
    'PROVIDER_FAILURE': PROVIDER,
    'PROVIDER_REFUSAL': PROVIDER,
    'UNCERTAIN_DISPATCH': RECONCILIATION,
    'UNCERTAIN_JOB_CREATION': RECONCILIATION,
    'CAPABILITY_UNVERIFIED': CAPABILITY,
    'REQUIREMENTS_GENERATION_UNAVAILABLE': CAPABILITY,
    'INVALID_INPUT': INPUT,
    'PRECONDITION': INPUT,
    'RECOVERABLE_RETRY': AUTOMATIC,
}

# Ordered: the first matching pattern names the cause of an untyped stop.
PATTERNS = (
    ('REQUIREMENTS_GENERATION_UNAVAILABLE', r'REQUIREMENTS_GENERATION_UNAVAILABLE|requirements generation (is )?unavailable'),
    ('CAPABILITY_UNVERIFIED', r'CAPABILITY_UNVERIFIED|capability (is )?unverified|unsupported (operation|schema)'),
    ('UNCERTAIN_JOB_CREATION', r'uncertain (job )?creation|Reconcile uncertain'),
    ('UNCERTAIN_DISPATCH', r'no provider receipt|uncertain dispatch|dispatched and has no|no longer a pre-dispatch'),
    ('INTEGRITY_FAILURE', r'changed after|changed or is missing|does not match|integrity|tamper|stale|approval invalid|Hash mismatch|was modified'),
    ('DOLLAR_CAP', r'dollar cap'),
    ('ALLOWANCE_EXHAUSTED', r'exhausted|revision limit|retry allowance|Insufficient call budget|call cap|allowance'),
    ('PROVIDER_REFUSAL', r'provider refusal|refused by the provider|reasoning_extraction'),
    ('PROVIDER_UNAVAILABLE', r'auth login|Install and authenticate|not logged in|RuntimeUnavailable|runtime unavailable'),
    ('PROVIDER_FAILURE', r'failed and stays counted|returned invalid output|provider (call|process) failed'),
    ('CONTEXT_CONFLICT', r'context conflict'),
    ('CONTEXT_LIMIT', r'context budget|exceeds budget|too large|does not fit|bytes and the limit|allowance is'),
    ('EVIDENCE_MISSING', r'source file and line|Evidence missing|missing evidence|citation|must inspect'),
    ('HUMAN_DECISION_REQUIRED', r'Record SME decisions|approval first|Approve |approve |review site first|Generate the review site'),
    ('AUTHORIZATION_REQUIRED', r'authoriz|--allow-new-assessment|--confirm'),
)

SUMMARY_LIMIT = 8


def stop(message, cause, hint=None):
    """Raise a stop with an explicit typed cause."""
    require_cause(cause)
    error = Blocked(message)
    error.cause = cause
    if hint:
        error.hint = hint
    raise error


def require_cause(cause):
    """Reject a cause that is not in the published table."""
    if cause not in CAUSES:
        raise ValueError('Unknown stop cause: ' + str(cause))


def classify(reason):
    """Name the cause of an untyped stop from its message. Unknown stops are input preconditions."""
    text = str(reason or '')
    for cause, pattern in PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return cause
    return 'PRECONDITION'


def describe(error_or_reason):
    """Return the cause and recovery class for an exception or a saved reason."""
    cause = getattr(error_or_reason, 'cause', None)
    if cause not in CAUSES and type(error_or_reason).__name__ == 'RuntimeUnavailable':
        cause = 'PROVIDER_UNAVAILABLE'
    if cause not in CAUSES:
        cause = classify(error_or_reason)
    return {'cause': cause, 'recovery': CAUSES[cause]}


STOP_FILE = 'last-stop.json'


def record_stop(work, error, command):
    """Save the latest stop beside project.json. A refused command leaves project.json byte-identical."""
    detail = describe(error)
    try:
        phase = json.loads((Path(work) / 'project.json').read_text()).get('stage')
    except (OSError, ValueError):
        phase = None
    record = {'cause': detail['cause'], 'recovery': detail['recovery'], 'phase': phase,
              'reason': str(error)[:500], 'command': command, 'at': time.time()}
    path = Path(work) / STOP_FILE
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(record, indent=2, sort_keys=True))
    temporary.chmod(0o600)
    os.replace(temporary, path)
    return record


def last_stop(work):
    """The latest recorded stop, or None."""
    path = Path(work) / STOP_FILE
    try:
        return json.loads(path.read_text()) if path.is_file() else None
    except (OSError, ValueError):
        return None


def record_cancellation(project, command):
    """Save a cancellation as an event. The phase stays where it was."""
    project['last_cancellation'] = {'command': command, 'at': time.time(), 'phase': project.get('stage')}
    return project['last_cancellation']


def may_continue_automatically(stop_record):
    """Only an automatic recovery class may be resumed without a person or an authorization."""
    return isinstance(stop_record, dict) and stop_record.get('recovery') == AUTOMATIC


def summary(work, project, questions, budget, readiness=None, implementation_blockers=None):
    """One compact status block: phase, questions, units, usage, blockers, package state."""
    checkpoints = (project.get('checkpoints') or {}).get('units') or {}
    by_status = {}
    for unit in checkpoints.values():
        if isinstance(unit, dict):
            by_status[unit.get('status') or 'PENDING'] = by_status.get(unit.get('status') or 'PENDING', 0) + 1
    functions = {}
    for item in (project.get('requirements') or {}).get('functions') or []:
        if isinstance(item, dict) and item.get('id'):
            functions[item['id']] = item.get('status') or 'selected'
    package = project.get('package') or {}
    acceptance = project.get('package_acceptance') or {}
    if acceptance.get('package_sha256') and acceptance.get('package_sha256') == package.get('sha256'):
        package_state = 'PACKAGE_ACCEPTED'
    elif package:
        package_state = 'AWAITING_PACKAGE_ACCEPTANCE'
    else:
        package_state = 'NOT_BUILT'
    blockers = []
    stop_record = last_stop(work)
    if isinstance(stop_record, dict) and project.get('stage') in {'BLOCKED', 'REWORK_LIMIT', 'WAITING_FOR_RUNTIME',
                                                                   'PROVIDER_REVIEW_REQUIRED', 'NEEDS_RECONCILIATION'}:
        blockers.append({'cause': stop_record.get('cause'), 'recovery': stop_record.get('recovery')})
    for operation in (project.get('operations') or {}).values():
        if isinstance(operation, dict) and operation.get('state') == 'uncertain':
            blockers.append({'cause': 'UNCERTAIN_DISPATCH', 'recovery': RECONCILIATION, 'operation': operation.get('id')})
    result = {
        'phase': project.get('stage'),
        'questions': questions,
        'units': by_status,
        'functions': functions,
        'usage': {key: budget.get(key) for key in ('preparation_calls', 'wireframe_calls', 'skip_draft_calls',
                                                   'dollars_measured', 'api_budget', 'subscription_usage_measured')},
        'workflow_blockers': blockers[:SUMMARY_LIMIT],
        'workflow_blockers_total': len(blockers),
        'package': package_state,
    }
    if readiness:
        result['implementation_readiness'] = readiness
    if implementation_blockers is not None:
        result['implementation_blockers_total'] = implementation_blockers
    result['note'] = ('Workflow blockers stop the next step. Implementation blockers are decisions, gaps, and conflicts '
                      'that keep built work from being ready; they are counted separately.')
    return result
