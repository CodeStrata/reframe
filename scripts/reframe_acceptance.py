"""Final package review, explicit acceptance, and implementation readiness (FR-10, FR-11).

Building a package never accepts it. A person reviews the exact archive and
accepts its SHA-256. The acceptance is written to a ledger outside the archive,
so the accepted ZIP is never modified and no hash refers to itself. Readiness
is computed from every known blocker and is separate from acceptance.
"""
import json
import os
import time
import zipfile
from hashlib import sha256
from pathlib import Path

from pilot import require, sha

AWAITING = 'AWAITING_PACKAGE_ACCEPTANCE'
ACCEPTED = 'PACKAGE_ACCEPTED'
LEGACY_BUILT = 'PACKAGED'
LEDGER = Path('acceptance') / 'ledger.jsonl'


def built_stage(stage):
    """True for a built package that still waits for acceptance, including the legacy PACKAGED name."""
    return stage in {AWAITING, LEGACY_BUILT}


def _questions(work, project, app):
    """Every SME question with its decision state."""
    try:
        spec = app.read(app.spec_path(work, project)) if project.get('specification') else {}
    except Exception:
        spec = {}
    decisions = project.get('decisions') or {}
    rows = []
    for question in spec.get('questions') or []:
        if not isinstance(question, dict) or not question.get('id'):
            continue
        decision = decisions.get(question['id'])
        state = 'unrecorded' if not isinstance(decision, dict) else decision.get('disposition') or 'unrecorded'
        rows.append({'id': question['id'], 'state': state, 'blocks': question.get('blocks'), 'owner': question.get('owner')})
    return spec, rows


def readiness(work, project, app):
    """Implementation readiness from every blocker. Empty decisions or blanket deferral never mean ready."""
    spec, questions = _questions(work, project, app)
    blockers = []
    for row in questions:
        if row['state'] in {'unrecorded', 'deferred'}:
            blockers.append({'kind': 'decision', 'id': row['id'], 'state': row['state'], 'blocks': row['blocks']})
    if project.get('specification') and not questions and not spec:
        blockers.append({'kind': 'specification', 'id': 'specification', 'state': 'unreadable'})
    if not project.get('specification') and not project.get('verification_skip'):
        blockers.append({'kind': 'specification', 'id': 'specification', 'state': 'not produced'})
    try:
        import reframe_optional as optional
        scope = app.spec_scope_ids(work, project)
        for conflict in optional.conflicts_affecting(work, scope):
            blockers.append({'kind': 'conflict', 'id': conflict['id'], 'state': 'open'})
    except Exception as error:
        blockers.append({'kind': 'conflict', 'id': 'context', 'state': 'unreadable: ' + str(error)[:80]})
    for row in spec.get('coverage') or []:
        if isinstance(row, dict) and row.get('gaps') and row.get('disposition') != 'excluded':
            blockers.append({'kind': 'coverage', 'id': row.get('id'), 'state': 'gap', 'gaps': row['gaps']})
    for row in spec.get('requirement_coverage') or []:
        if isinstance(row, dict) and row.get('disposition') == 'gap':
            blockers.append({'kind': 'coverage', 'id': row.get('id'), 'state': 'gap', 'gaps': row.get('gaps')})
    for row in spec.get('test_templates') or []:
        if isinstance(row, dict) and row.get('state') == 'PLACEHOLDER':
            blockers.append({'kind': 'test_template', 'id': row.get('id'), 'state': 'PLACEHOLDER', 'missing': row.get('missing')})
    for row in (project.get('design_coverage') or {}).get('rows') or []:
        if row.get('state') == 'gap':
            blockers.append({'kind': 'coverage', 'id': row.get('id'), 'state': 'gap'})
    for item in pending_deltas(work, project):
        blockers.append({'kind': 'delta', 'id': item['id'], 'state': item['status']})
    if project.get('verification_skip'):
        blockers.append({'kind': 'verification', 'id': 'independent-validation', 'state': 'skipped by owner'})
    for phase in required_approvals(project):
        if phase not in (project.get('approvals') or {}):
            blockers.append({'kind': 'approval', 'id': phase, 'state': 'missing'})
    decisions = [b for b in blockers if b['kind'] == 'decision']
    if decisions:
        state = 'BLOCKED_BY_UNRESOLVED_DECISIONS'
    elif blockers:
        state = 'PARTIALLY_READY'
    else:
        state = 'NO_KNOWN_BLOCKERS'
    return {'state': state, 'blockers': blockers, 'blocker_count': len(blockers),
            'note': 'Readiness is computed from recorded blockers. It is not deployment approval or evidence that tests ran.'}


def required_approvals(project):
    """Approvals a package on this route rests on."""
    if project.get('verification_skip'):
        return ['assessment', 'design']
    return ['assessment', 'validation', 'specifications']


def pending_deltas(work, project):
    """Reimagine proposals that are not approved."""
    version = (project.get('design_plan') or {}).get('version')
    found = []
    for path in sorted(Path(work).glob('previews/*/future-state/deltas.json')):
        if version and path.parents[1].name != version:
            continue
        try:
            for item in json.loads(path.read_text()).get('proposals') or []:
                if item.get('status') not in {'implementation_requirement', 'rejected'}:
                    found.append({'id': item.get('id'), 'status': item.get('status')})
        except (OSError, ValueError, AttributeError):
            continue
    return found


def inventory(archive):
    """Name, size, and SHA-256 of every member of the archive."""
    with zipfile.ZipFile(archive) as bundle:
        return [{'name': info.filename, 'bytes': info.file_size,
                 'sha256': sha256(bundle.read(info.filename)).hexdigest()} for info in bundle.infolist()]


def review(work, project, app):
    """What a person reviews before accepting: inventory, exact hash, approval basis, gaps, unresolved work."""
    package = project.get('package') or {}
    require(package.get('path'), 'Build a package first')
    archive = Path(work) / package['path']
    require(archive.is_file(), 'The package archive is missing')
    current = sha(archive)
    require(current == package.get('sha256'), 'The package changed after it was built. It was not accepted.')
    approvals = [{'phase': phase, 'by': item.get('by'), 'version_id': item.get('version_id'),
                  'simulated': bool(item.get('simulated'))} for phase, item in sorted((project.get('approvals') or {}).items())]
    return {'status': project.get('stage'), 'package': package['path'], 'sha256': current, 'route': package.get('route'),
            'version_id': package.get('version_id'), 'verification': package.get('verification'),
            'inventory': inventory(archive), 'approval_basis': approvals,
            'readiness': readiness(work, project, app),
            'acceptance': (project.get('package_acceptance') or {}).get('package_sha256') == current}


def _ledger_entries(work):
    path = Path(work) / LEDGER
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _append(work, entry):
    """Append one hash-chained ledger entry outside the archive."""
    path = Path(work) / LEDGER
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    entries = _ledger_entries(work)
    entry['previous_entry_sha256'] = entries[-1]['entry_sha256'] if entries else None
    body = json.dumps({k: v for k, v in entry.items() if k != 'entry_sha256'}, sort_keys=True)
    entry['entry_sha256'] = sha256(body.encode()).hexdigest()
    with path.open('a') as handle:
        handle.write(json.dumps(entry, sort_keys=True) + '\n')
    path.chmod(0o600)
    return entry


def verify_ledger(work):
    """Every entry hash and chain link must hold."""
    previous = None
    for entry in _ledger_entries(work):
        body = json.dumps({k: v for k, v in entry.items() if k != 'entry_sha256'}, sort_keys=True)
        require(sha256(body.encode()).hexdigest() == entry['entry_sha256'], 'Acceptance ledger entry changed')
        require(entry.get('previous_entry_sha256') == previous, 'Acceptance ledger chain is broken')
        previous = entry['entry_sha256']
    return True


def accept(work, project, app, package_sha256, by, note, simulated=False):
    """Record that a named person accepted this exact archive. The archive is not modified."""
    require(built_stage(project.get('stage')), 'Only a built package that awaits acceptance can be accepted')
    require(str(by).strip() and str(note).strip(), 'Acceptance needs a named person and their own rationale')
    app.reject_instructional_placeholder(note, 'Acceptance note')
    detail = review(work, project, app)
    require(package_sha256 == detail['sha256'],
            'The SHA-256 you accepted does not match the package under review. Nothing was accepted.')
    if project.get('verification_skip'):
        app.require_skip_acceptance(project)
    app.require_clear_for_final(work, 'package acceptance', app.spec_scope_ids(work, project))
    verify_ledger(work)
    entry = _append(work, {'event': 'package_accepted', 'package': detail['package'], 'package_sha256': detail['sha256'],
                           'manifest_sha256': (project.get('package') or {}).get('manifest_sha256'),
                           'version_id': detail['version_id'], 'route': detail['route'], 'by': str(by).strip(),
                           'note': str(note).strip(), 'simulated': bool(simulated), 'at': time.time(),
                           'readiness': detail['readiness']['state'],
                           'scope': 'Accepts this handoff version only. Not deployment approval; blocked work stays blocked.'})
    project['package_acceptance'] = {k: entry[k] for k in ('package_sha256', 'manifest_sha256', 'version_id', 'by',
                                                          'simulated', 'at', 'entry_sha256', 'readiness')}
    project['package']['status'] = ACCEPTED
    project['stage'] = ACCEPTED
    return entry


def withdraw(work, project, reason):
    """A change after acceptance supersedes it. The ledger keeps the earlier entry."""
    accepted = project.get('package_acceptance')
    if not accepted:
        return None
    entry = _append(work, {'event': 'acceptance_superseded', 'package_sha256': accepted.get('package_sha256'),
                           'reason': reason, 'at': time.time()})
    project.setdefault('acceptance_history', []).append({**accepted, 'superseded_by': entry['entry_sha256'], 'reason': reason})
    project.pop('package_acceptance', None)
    return entry


FR10_ITEMS = (
    ('Package manifest, scope, mode, target constraints, source pin, input fingerprints', ('ai-dlc.json', 'provenance.json', 'design-plan.json')),
    ('AWS requirements and traceability, or an explicit provenance statement', ('requirements-evidence.json',)),
    ('Reviewed business specification and requirement/rule coverage', ('specification.json', 'rule-coverage.json')),
    ('Data, interface, and batch inventories with unresolved semantics', ('field-inventory.json', 'batch-inventory.json', 'api-boundary.json')),
    ('Wireframes, screen and journey model, API contracts and OpenAPI', ('review.html', 'index.html', 'screens.json', 'api-contracts.json', 'openapi.json')),
    ('Dependency-ordered backlog with structured references', ('implementation-backlog.json',)),
    ('Acceptance scenarios with execution status and oracle or gap', ('traceability.json', 'acceptance-catalog.json', 'parallel-validation.json')),
    ('Human context dispositions, conflicts, decisions, deferrals, deltas, approval history', ('human-context.json', 'decisions.json', 'decisions-needed.json', 'approval-history.json')),
    ('Implementation boundaries, agent instructions, extraction guidance, next actions', ('AGENTS.md', 'SKILL.md', 'extraction-reading.json', 'governance.json')),
    ('Content hashes and licensing notices', ('checksums.json', 'reframe-notice.md')),
)


def fr10_manifest(names, route, notes=None):
    """Which FR-10 logical contents this package carries, by file, and which are explicitly absent."""
    names = set(names) | {'checksums.json'}
    rows = []
    for item, files in FR10_ITEMS:
        present = [name for name in files if name in names]
        rows.append({'item': item, 'files': present, 'status': 'present' if present else 'absent',
                     'note': (notes or {}).get(item)})
    return {'route': route, 'items': rows, 'absent': [row['item'] for row in rows if row['status'] == 'absent'],
            'note': 'An absent item is listed, not hidden. Building a package does not accept it.'}
