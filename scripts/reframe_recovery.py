"""Read-only recovery plan for a saved workspace (spec §11).

The plan checks every recorded hash and receipt, says which saved outputs can
be reused and which cannot, names approvals that need renewal, and lists the
actions that need an owner's authorization. It writes nothing.
"""
from pathlib import Path

from pilot import Blocked

# The checks each approval rests on. A failed check means that approval needs renewal.
DEPENDS = {
    'assessment': ('source pin', 'sealed assessment'),
    'validation': ('source pin', 'sealed assessment', 'specification hash', 'preparation report',
                   'validation approval binding'),
    'specifications': ('source pin', 'sealed assessment', 'specification hash', 'preparation report',
                       'validation approval binding', 'review site'),
}
TEST_ONLY_WORDS = ('test only', 'test-only', 'workflow testing', 'for testing', 'simulated', 'fixture')


def _check(label, fn):
    """Run one read-only verification and report it."""
    try:
        detail = fn()
        return {'check': label, 'status': 'ok', **({'detail': detail} if detail else {})}
    except (Blocked, OSError, ValueError, KeyError, TypeError) as error:
        return {'check': label, 'status': 'failed', 'reason': str(error)[:300]}


def _test_only(approval):
    """True when an approval is marked simulated or its note says it was for testing."""
    note = str((approval or {}).get('note') or '').casefold()
    return bool((approval or {}).get('simulated')) or any(word in note for word in TEST_ONLY_WORDS)


def _stage_outputs(work, project, app):
    """Classify saved wireframe stage responses: reusable, incompatible, or missing."""
    plan = project.get('wireframe_plan') or {}
    stages = plan.get('stages') or []
    result = {'stages': [], 'conflicts': []}
    parts = []
    for stage in stages:
        response, failure = app.wireframe_stage_files(work, stage.get('index'))
        entry = {'index': stage.get('index'), 'call': stage.get('call'), 'status': stage.get('status')}
        if response.is_file():
            entry['receipt'] = 'present'
            try:
                parts.append((stage, app.read(response)))
            except (OSError, ValueError) as error:
                entry['receipt'] = 'unreadable: ' + str(error)[:120]
        elif failure.is_file():
            entry['receipt'] = 'failure-recorded'
        else:
            entry['receipt'] = 'absent'
        result['stages'].append(entry)
    seen = {}
    for stage, part in parts:
        for kind in ('screens', 'apis', 'journeys'):
            for item in part.get(kind) or []:
                if not isinstance(item, dict) or not item.get('id'):
                    continue
                key = (kind, item['id'])
                if key in seen and app.digest(seen[key][1]) != app.digest(item):
                    result['conflicts'].append({'kind': kind, 'id': item['id'],
                                                'first_stage': seen[key][0], 'second_stage': stage.get('index')})
                else:
                    seen.setdefault(key, (stage.get('index'), item))
    conflicted = {c['second_stage'] for c in result['conflicts']} | {c['first_stage'] for c in result['conflicts']}
    for entry in result['stages']:
        if entry['receipt'] != 'present':
            entry['classification'] = 'missing' if entry['receipt'] == 'absent' else 'not-reusable'
        elif entry['index'] in conflicted:
            entry['classification'] = 'incompatible-shared-definition'
        else:
            entry['classification'] = 'reusable'
    return result


def plan(work, project, app):
    """Build the recovery plan. Every check reads; nothing is written."""
    import reframe_operations as ops
    import reframe_versions as versions
    work = Path(work)
    checks = [
        _check('source pin', lambda: app.verify_source(project)),
        _check('framework migration', lambda: app.migration_state(project)),
    ]
    if project.get('selected'):
        checks.append(_check('sealed assessment',
                             lambda: app.approved(project, 'assessment', project['assessments'][project['selected']]['sha256'])))
    if project.get('specification'):
        checks.append(_check('specification hash', lambda: app.spec_path(work, project) and None))
        checks.append(_check('preparation report', lambda: app.verified_preparation_report(work, project) and None))
    if (project.get('approvals') or {}).get('validation'):
        checks.append(_check('validation approval binding', lambda: app.approved(
            project, 'validation', app.digest({'specification': project['specification']['sha256'],
                                               'decisions': project['decisions']}))))
    if project.get('site'):
        checks.append(_check('review site', lambda: app.site_fingerprint(work, project)))
    if project.get('active_version'):
        checks.append(_check('active version', lambda: versions.verify(work, project) and None))
    receipts = sorted((work / 'preparation').glob('reply-*.json')) if (work / 'preparation').is_dir() else []
    calls = (project.get('pipeline') or {}).get('calls') or 0
    usage = {'preparation_calls': calls, 'preparation_receipts': len(receipts),
             'wireframe_calls': project.get('ui_calls') or 0,
             'dollars_spent': (project.get('settings') or {}).get('model_dollars_spent', 0),
             'operations': ops.counts(project), 'preserved': True}
    stages = _stage_outputs(work, project, app)
    approvals = []
    for phase, approval in sorted((project.get('approvals') or {}).items()):
        relies_on = DEPENDS.get(phase, tuple(c['check'] for c in checks))
        failed = [c for c in checks if c['status'] == 'failed' and c['check'] in relies_on]
        approvals.append({'phase': phase, 'by': approval.get('by'), 'test_only': _test_only(approval),
                          'needs_renewal': bool(failed) or _test_only(approval),
                          'reason': ('test-only approval; not genuine sign-off' if _test_only(approval)
                                     else (failed[0]['reason'] if failed else None))})
    try:
        questions = app.question_counts(work, project) if project.get('specification') else {}
    except (Blocked, OSError, ValueError, KeyError) as error:
        questions = {'unavailable': str(error)[:200]}
    authorization = []
    if stages['conflicts']:
        authorization.append('Record a reconciliation for each conflicting shared definition, or start a new design '
                             'version. The saved stage outputs stay unchanged.')
    if any(entry['classification'] in {'missing', 'not-reusable'} for entry in stages['stages']):
        authorization.append('Generate the missing wireframe stages; each new provider call needs authorization and stays counted.')
    if app.failed_wireframe_stages(work, project):
        authorization.append('A wireframe call failed or returned invalid output and stays counted. '
                             'reframe retry-wireframes --by NAME --note WHY authorizes one new counted attempt.')
    if any(item['needs_renewal'] for item in approvals):
        authorization.append('Renew the listed approvals with a genuine reviewer; test-only approvals are not sign-off.')
    if questions.get('deferred'):
        authorization.append(str(questions['deferred']) + ' SME questions are deferred. Deferral is not an answer; '
                             'affected implementation stays blocked.')
    return {
        'status': 'RECOVERY_PLAN', 'writes': 'none', 'phase': project.get('stage'),
        'checks': checks, 'usage': usage, 'wireframe_stages': stages, 'approvals': approvals,
        'questions': questions,
        'controller_migration': {'prompts_changed': app.prompts_differ(project),
                                 'wireframe_prompt_changed': app.wireframe_prompt_changed(project)},
        'requires_authorization': authorization,
        'never': ['delete the workspace', 'reset counters', 'erase receipts', 'rename conflicting screens',
                  'reopen passed units', 'change deferrals', 'rerun the assessment to escape a blocker'],
    }
