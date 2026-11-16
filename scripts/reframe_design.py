"""Design plan, design inventory, shared-definition reconciliation, and API completeness (FR-07, FR-08).

The mode and target constraints are captured before any wireframe call and shape
every request. The inventory is saved before the first detail call and records,
before each later call, which stage owns each shared screen, journey, or API.
Conflicting definitions stop until a person records which one stands; nothing is
renamed, overwritten, or dropped.
"""
import json
import shutil
import time
from hashlib import sha256
from pathlib import Path

from pilot import Blocked, require

MODES = ('functional-parity', 'reimagine')
KINDS = ('journeys', 'screens', 'apis')
WRITE_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}


def _digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True))
    temporary.chmod(0o600)
    temporary.replace(path)


# Design plan (#182)

def plan_fields(plan):
    """The parts of the plan that shape generation."""
    plan = plan or {}
    return {key: plan.get(key) for key in ('mode', 'version', 'target', 'constraints')}


def capture(work, project, mode, version, language, runtime, platform, constraints, by, revise=False):
    """Record the mode and target constraints before detailed design. A change after design starts is a new version."""
    require(mode in MODES, 'Choose functional-parity or reimagine')
    require(str(by).strip(), 'Name the person recording the design plan')
    require(version and str(version).strip(), 'Name the design version')
    plan = {'mode': mode, 'version': str(version).strip(),
            'target': {'language': (language or 'unspecified').strip(), 'runtime': (runtime or 'unspecified').strip(),
                       'platform': (platform or 'unspecified').strip()},
            'constraints': [item.strip() for item in (constraints or []) if item and item.strip()],
            'by': str(by).strip(), 'at': time.time()}
    previous = project.get('design_plan')
    if previous and plan_fields(previous) == plan_fields(plan):
        return {'status': 'DESIGN_PLAN_UNCHANGED', 'plan': previous}
    started = bool(project.get('site') or project.get('wireframe_plan') or project.get('skip_design'))
    if previous and started:
        require(revise, 'Design work already exists for the current plan. Recording a different mode or target creates a '
                        'new design version; pass --revise to do that. The earlier design and its receipts are kept.')
        retire_design(work, project, 'design_plan_change')
    if previous:
        project.setdefault('design_plan_history', []).append(previous)
    project['design_plan'] = plan
    return {'status': 'DESIGN_PLAN_RECORDED', 'plan': plan, 'revised': bool(previous and started)}


def retire_design(work, project, reason):
    """Keep the earlier design for audit, supersede what rested on it, and clear it from the active state."""
    import reframe_versions as versions
    import reframe_acceptance as acceptance
    stamp = time.time()
    archived = archive_stage_receipts(work, (project.get('wireframe_plan') or {}).get('fingerprint') or 'unplanned')
    project.setdefault('design_history', []).append({
        'reason': reason, 'at': stamp, 'plan': project.get('design_plan'), 'site': project.get('site'),
        'wireframe_plan': project.get('wireframe_plan'), 'stage_receipts': archived,
        'inventory': project.get('design_inventory')})
    versions.supersede(project, ('specifications', 'design', 'package'), reason, stamp)
    acceptance.withdraw(work, project, reason)
    for key in ('site', 'wireframe_plan', 'design_inventory', 'package'):
        project.pop(key, None)


def archive_stage_receipts(work, fingerprint):
    """Move saved stage receipts aside so a new plan can never read them as its own. Nothing is deleted."""
    source = Path(work) / 'previews' / 'wireframe-stages'
    if not source.is_dir() or not any(source.iterdir()):
        return None
    target = Path(work) / 'previews' / 'wireframe-stages-archive' / (str(fingerprint)[:16] + '-' + str(int(time.time() * 1000)))
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    shutil.move(str(source), str(target))
    return str(target.relative_to(work))


def require_plan(project):
    """Detailed design needs a recorded plan first."""
    from reframe_states import stop
    if not project.get('design_plan'):
        stop('Record the design mode and target constraints before detailed design: reframe design-plan.', 'HUMAN_DECISION_REQUIRED')
    return project['design_plan']


# Design inventory (#183)

def inventory_path(work, fingerprint):
    return Path(work) / 'previews' / ('design-inventory-' + str(fingerprint)[:16] + '.json')


def build_inventory(work, project, spec, stages, fingerprint):
    """Save the inventory before any detail call: plan, capabilities, requirements, stage assignments, gaps."""
    import reframe_handoff as handoff
    import reframe_requirements as requirements
    rules = [rule for rule in spec.get('rules') or [] if isinstance(rule, dict)]
    try:
        records = requirements.active_set(work, project)['requirements']
    except Blocked:
        records = []
    decisions = project.get('decisions') or {}
    inventory = {
        'schema_version': 1, 'fingerprint': fingerprint, 'design_plan': plan_fields(project.get('design_plan')),
        'capabilities': [{'id': item['id'], 'programs': item.get('programs'), 'rule_ids': item.get('rule_ids'),
                          'disposition': item.get('disposition')} for item in handoff.capabilities(rules)],
        'requirement_ids': [item['id'] for item in records],
        'stage_assignments': [{'stage': stage['index'] + 1, 'rules': stage.get('rules', []),
                               'questions': stage.get('questions', []), 'sections': stage.get('sections', [])}
                              for stage in stages],
        'owners': {kind: {} for kind in KINDS},
        'gaps': [{'question': q.get('id'), 'disposition': (decisions.get(q.get('id')) or {}).get('disposition', 'undecided')}
                 for q in spec.get('questions') or [] if isinstance(q, dict)
                 if (decisions.get(q.get('id')) or {}).get('disposition') != 'resolved'],
        'reconciliations': [],
        'saved_before_detail': True, 'created_at': time.time(),
        'ownership_rule': 'The first stage that defines an id owns it. Ownership is saved before the next stage is requested.',
    }
    path = inventory_path(work, fingerprint)
    if path.is_file():
        saved = json.loads(path.read_text())
        inventory['owners'] = saved.get('owners') or inventory['owners']
        inventory['reconciliations'] = saved.get('reconciliations') or []
        inventory['created_at'] = saved.get('created_at', inventory['created_at'])
    _save(path, inventory)
    project['design_inventory'] = {'path': str(path.relative_to(work)), 'fingerprint': fingerprint}
    return inventory


def load_inventory(work, project):
    record = project.get('design_inventory') or {}
    require(record.get('path'), 'No design inventory is saved')
    return json.loads((Path(work) / record['path']).read_text())


def record_owners(work, project, stage_index, payload):
    """After a stage receipt and before the next request, save which ids that stage defined."""
    inventory = load_inventory(work, project)
    for kind in KINDS:
        for item in (payload or {}).get(kind) or []:
            if isinstance(item, dict) and isinstance(item.get('id'), str) and not item.get('ref'):
                inventory['owners'][kind].setdefault(item['id'], stage_index + 1)
    _save(Path(work) / project['design_inventory']['path'], inventory)
    return inventory


def message_view(work, project):
    """What each stage request carries from the plan and inventory."""
    plan = plan_fields(project.get('design_plan'))
    view = {'design_plan': plan,
            'design_instruction': ('Design for mode ' + str(plan.get('mode')) + ' and target ' + json.dumps(plan.get('target'))
                                   + '. Functional parity keeps confirmed behavior only. Reimagine proposals stay '
                                   'separate from current state. Each API states request and response schemas, error '
                                   'cases, an auth assumption, an idempotency or transaction note for writes, and the '
                                   'rule or requirement ids it rests on; name a gap instead of inventing one.')}
    feedback = [item.get('note') for item in project.get('design_feedback') or [] if item.get('note')]
    if feedback:
        view['reviewer_feedback'] = feedback
    # Owners already reach each stage in the request's owned list; the saved inventory stays local.
    return view


# Reconciliation and global references (#184)

def reconcile(work, project, kind, ident, keep_stage, by, note):
    """A person records which stage's definition of a shared id stands. The other definition is kept as superseded."""
    require(kind in KINDS, 'Kind must be journeys, screens, or apis')
    require(str(by).strip() and str(note).strip(), 'A reconciliation needs a named person and a note')
    inventory = load_inventory(work, project)
    inventory['reconciliations'] = [item for item in inventory['reconciliations']
                                    if not (item['kind'] == kind and item['id'] == ident)]
    inventory['reconciliations'].append({'kind': kind, 'id': ident, 'keep_stage': int(keep_stage), 'by': str(by).strip(),
                                         'note': str(note).strip(), 'at': time.time()})
    _save(Path(work) / project['design_inventory']['path'], inventory)
    return inventory['reconciliations'][-1]


def merge(staged, reconciliations=None):
    """Merge (stage index, response) pairs. Identical definitions collapse; a conflict needs a recorded reconciliation."""
    chosen = {(item['kind'], item['id']): item['keep_stage'] for item in reconciliations or []}
    merged = {key: [] for key in KINDS}
    definitions = {key: {} for key in KINDS}
    references = {key: set() for key in KINDS}
    superseded = []
    conflicts = []
    for index, part in staged:
        require(isinstance(part, dict), 'Wireframe stage returned an unexpected response')
        for key in KINDS:
            value = part.get(key) or []
            require(isinstance(value, list), 'Wireframe stage returned an unexpected ' + key)
            for item in value:
                require(isinstance(item, dict) and isinstance(item.get('id'), str), 'Wireframe stage item needs an id')
                if item.get('ref') is True and set(item) <= {'id', 'ref'}:
                    references[key].add(item['id'])
                    continue
                canonical = json.dumps(item, sort_keys=True)
                previous = definitions[key].get(item['id'])
                if previous is None:
                    definitions[key][item['id']] = (canonical, item, index)
                    continue
                if previous[0] == canonical:
                    continue
                keep = chosen.get((key, item['id']))
                if keep is None:
                    conflicts.append({'kind': key, 'id': item['id'], 'stages': [previous[2] + 1, index + 1]})
                    continue
                if keep == index + 1:
                    superseded.append({'kind': key, 'id': item['id'], 'stage': previous[2] + 1, 'definition': previous[1]})
                    definitions[key][item['id']] = (canonical, item, index)
                else:
                    superseded.append({'kind': key, 'id': item['id'], 'stage': index + 1, 'definition': item})
    if conflicts:
        from reframe_states import stop
        first = conflicts[0]
        listed = ('conflicting ' + first['kind'] + ' definitions for ' + first['id'] + '. All conflicts: '
                  + '; '.join(c['kind'] + ' ' + c['id'] + ' (stages ' + ', '.join(map(str, c['stages'])) + ')' for c in conflicts))
        error_hint = ('Record which definition stands: reframe --workspace WORKSPACE reconcile-design --kind KIND --id ID '
                      '--keep-stage N --by NAME --note REASON. The other definition is kept as superseded.')
        stop('Wireframe stages gave ' + listed + '. Reconciliation is required. '
             'Nothing was renamed or overwritten.', 'HUMAN_DECISION_REQUIRED', hint=error_hint)
    for key in KINDS:
        for _canonical, item, _index in definitions[key].values():
            merged[key].append(item)
        missing = sorted(references[key] - set(definitions[key]))
        require(not missing, 'Wireframe stage referenced ' + key + ' without a definition: ' + ', '.join(missing))
    merged['superseded_definitions'] = superseded
    return merged


def validate_references(screens, spec, requirement_ids=()):
    """Every journey, action, API, rule, and requirement reference must resolve after the merge."""
    screen_ids = {item.get('id') for item in screens.get('screens') or []}
    api_ids = {item.get('id') for item in screens.get('apis') or []}
    rule_ids = {item.get('id') for item in spec.get('rules') or [] if isinstance(item, dict)}
    known = rule_ids | set(requirement_ids) | {item.get('id') for item in spec.get('assessment_evidence') or [] if isinstance(item, dict)}
    problems = []
    for journey in screens.get('journeys') or []:
        for ident in journey.get('screen_ids') or []:
            if ident not in screen_ids:
                problems.append('journey ' + str(journey.get('id')) + ' -> unknown screen ' + str(ident))
    for screen in screens.get('screens') or []:
        for ident in screen.get('api_ids') or []:
            if ident not in api_ids:
                problems.append('screen ' + str(screen.get('id')) + ' -> unknown API ' + str(ident))
        for action in screen.get('actions') or []:
            target = action.get('opens') if isinstance(action, dict) else None
            if target and target not in screen_ids:
                problems.append('screen ' + str(screen.get('id')) + ' action -> unknown screen ' + str(target))
        for ident in screen.get('rule_ids') or []:
            if ident not in known:
                problems.append('screen ' + str(screen.get('id')) + ' -> unknown rule or requirement ' + str(ident))
    for api in screens.get('apis') or []:
        for ident in (api.get('rule_ids') or []) + (api.get('requirement_ids') or []):
            if ident not in known:
                problems.append('API ' + str(api.get('id')) + ' -> unknown rule or requirement ' + str(ident))
    require(not problems, 'Merged design has unresolved references: ' + '; '.join(problems[:10]))
    return True


# API completeness (#185)

def api_completeness(apis):
    """Each proposed API's schemas, errors, auth, idempotency, and evidence links, or the named gaps."""
    rows = []
    for api in apis or []:
        if not isinstance(api, dict):
            continue
        method = str(api.get('method') or '').upper()
        responses = api.get('responses') if isinstance(api.get('responses'), dict) else {}
        checks = {
            'request_schema': bool(api.get('request')) or method in {'GET', 'DELETE'},
            'response_schema': any(str(code).startswith('2') for code in responses),
            'error_cases': any(str(code)[:1] in {'4', '5'} for code in responses) or bool(api.get('errors')),
            'auth_assumption': bool(api.get('auth') or api.get('authentication') or api.get('security')),
            'idempotency_note': method not in WRITE_METHODS or bool(api.get('idempotency') or api.get('transaction')),
            'evidence_links': bool(api.get('rule_ids') or api.get('requirement_ids')),
        }
        gaps = sorted(name for name, ok in checks.items() if not ok)
        rows.append({'id': api.get('id'), 'method': method, 'path': api.get('path'), 'gaps': gaps,
                     'state': 'complete' if not gaps else 'gap'})
    return {'rows': rows, 'complete': sum(1 for r in rows if r['state'] == 'complete'),
            'with_gaps': sum(1 for r in rows if r['state'] == 'gap'),
            'note': 'A gap is named, not invented. No endpoint is live.'}


def completeness_html(report):
    """A table of API gaps for the API reference page."""
    import html
    rows = ''.join('<tr><td>' + html.escape(str(r['id'])) + '</td><td>' + html.escape(r['method'] + ' ' + str(r['path']))
                   + '</td><td>' + html.escape(', '.join(r['gaps']) or 'complete') + '</td></tr>' for r in report['rows'])
    return ('<h2 id="api-completeness">Contract completeness</h2><p>' + html.escape(report['note']) + '</p>'
            '<table><thead><tr><th>API</th><th>Operation</th><th>Gaps</th></tr></thead><tbody>' + rows + '</tbody></table>')
