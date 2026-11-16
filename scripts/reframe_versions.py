"""One logical version manifest for every artifact, and approval supersession.

A version names every input a consumer may read: the source pin, the sealed
assessment, the requirements evidence (or its explicit absence), the human
context, the specification and decisions, the design plan, the wireframes and
API contracts, and the package. The version id is the hash of those references,
so equal inputs give the same id and any change gives a new one. Version files
are written once and never rewritten.
"""
import copy
import hashlib
import json
import os
import time
from pathlib import Path

from pilot import Blocked, require, sha

SCHEMA_VERSION = 1
VERSION_DIR = 'versions'


def _digest(value):
    """Stable hash of a JSON value."""
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _file_ref(work, relative, kind, producer):
    """Reference one file by relative path and content hash."""
    path = Path(work) / relative
    require(path.is_file() and not path.is_symlink(), kind + ' artifact is missing: ' + str(relative))
    return {'type': kind, 'path': str(relative), 'sha256': sha(path), 'schema': SCHEMA_VERSION, 'producer': producer}


def references(work, project):
    """Every artifact the current project state points at. Absent work is an explicit state, not a gap."""
    work = Path(work)
    source = project.get('source') or {}
    refs = {'source': {'type': 'source', 'repository': source.get('repository'), 'commit': source.get('commit'),
                       'archive_sha256': source.get('archive_sha256') or source.get('sha256')}}
    label = project.get('selected')
    assessment = (project.get('assessments') or {}).get(label) if label else None
    refs['assessment'] = ({'type': 'assessment', 'label': label, 'sha256': assessment.get('sha256'), 'producer': 'assessment'}
                          if assessment else {'type': 'assessment', 'state': 'NOT_APPROVED'})
    requirements = project.get('requirements') or {}
    if requirements.get('manifest'):
        refs['requirements'] = _file_ref(work, requirements['manifest'], 'requirements', requirements.get('origin') or 'requirements')
    else:
        refs['requirements'] = {'type': 'requirements', 'state': requirements.get('state') or 'NOT_REQUESTED'}
    try:
        import reframe_optional as optional
        refs['context'] = {'type': 'context', 'sha256': optional._context_fingerprint(work),
                           'status': optional.context_status(work).get('status')}
    except (OSError, ValueError):
        refs['context'] = {'type': 'context', 'state': 'UNREADABLE'}
    specification = project.get('specification') or {}
    refs['specification'] = (_file_ref(work, specification['path'], 'specification', 'validation')
                             if specification.get('path') else {'type': 'specification', 'state': 'NOT_PRODUCED'})
    refs['decisions'] = {'type': 'decisions', 'sha256': _digest(project.get('decisions') or {}),
                         'count': len(project.get('decisions') or {})}
    plan = project.get('design_plan') or {}
    refs['design_plan'] = ({'type': 'design_plan', 'sha256': _digest(plan), 'mode': plan.get('mode'),
                            'target': plan.get('target')} if plan else {'type': 'design_plan', 'state': 'NOT_CAPTURED'})
    inventory = (project.get('design_inventory') or {}).get('path')
    refs['design_inventory'] = (_file_ref(work, inventory, 'design_inventory', 'design-plan')
                                if inventory else {'type': 'design_inventory', 'state': 'NOT_PERSISTED'})
    site = project.get('site') or {}
    if site.get('directory'):
        files = {name: _file_ref(work, str(Path(site['directory']) / name), 'wireframes', 'review-site')['sha256']
                 for name in sorted((site.get('files') or {}))}
        refs['wireframes'] = {'type': 'wireframes', 'directory': site['directory'], 'files': files}
        if 'api-contracts.json' in files:
            refs['api_contracts'] = {'type': 'api_contracts', 'path': str(Path(site['directory']) / 'api-contracts.json'),
                                     'sha256': files['api-contracts.json']}
    else:
        refs['wireframes'] = {'type': 'wireframes', 'state': 'NOT_GENERATED'}
    package = project.get('package') or {}
    refs['package'] = (_file_ref(work, package['path'], 'package', package.get('route') or 'package')
                       if package.get('path') else {'type': 'package', 'state': 'NOT_BUILT'})
    return refs


def version_record(work, project, reason):
    """Build the version record for the current state. Its id is the hash of the references."""
    refs = references(work, project)
    verification = 'skipped' if project.get('verification_skip') else (
        'independently-reviewed' if project.get('specification') else 'not-yet-validated')
    source = project.get('source') or {}
    identity = project.get('project_id') or ('project-' + _digest(str(source.get('repository') or ''))[:12])
    run_id = project.get('run_id') or ('run-' + _digest([source.get('repository'), source.get('commit'),
                                                         project.get('created_at')])[:12])
    body = {'schema_version': SCHEMA_VERSION, 'project_id': identity, 'run_id': run_id,
            'references': refs, 'verification_status': verification}
    version_id = _digest(body)[:24]
    return {**body, 'version_id': version_id, 'input_fingerprint': _digest(refs),
            'workflow_status': project.get('stage'), 'reason': reason, 'recorded_at': time.time()}


def _write_once(path, record):
    """Write a version file once. An existing file must hold the same version."""
    if path.exists():
        saved = json.loads(path.read_text())
        require(saved.get('version_id') == record['version_id'] and saved.get('references') == record['references'],
                'Version file ' + path.name + ' changed after it was recorded')
        return False
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(record, indent=2, sort_keys=True))
    temporary.chmod(0o600)
    os.replace(temporary, path)
    return True


def record(work, project, reason):
    """Record the current inputs as a version and make it active. Equal inputs reuse the same id."""
    entry = version_record(work, project, reason)
    created = _write_once(Path(work) / VERSION_DIR / (entry['version_id'] + '.json'), entry)
    history = project.setdefault('versions', [])
    if created or not any(item.get('id') == entry['version_id'] for item in history):
        history.append({'id': entry['version_id'], 'reason': reason, 'at': entry['recorded_at'],
                        'workflow_status': entry['workflow_status']})
    project['active_version'] = entry['version_id']
    return entry['version_id']


def load(work, version_id):
    """Read one saved version."""
    path = Path(work) / VERSION_DIR / (str(version_id) + '.json')
    require(path.is_file(), 'Version ' + str(version_id) + ' is not recorded')
    return json.loads(path.read_text())


def _changed(saved, current):
    """Names of references whose recorded content no longer matches."""
    return sorted(name for name in set(saved) | set(current) if saved.get(name) != current.get(name))


def verify(work, project, names=None):
    """Stop when an artifact named by the active version changed. Nothing is rewritten."""
    version_id = project.get('active_version')
    require(version_id, 'No version is recorded for this project yet')
    saved = load(work, version_id)
    current = references(work, project)
    keys = names or list(saved['references'])
    changed = _changed({k: saved['references'].get(k) for k in keys}, {k: current.get(k) for k in keys})
    if changed:
        from reframe_states import stop
        stop('Integrity failure: ' + ', '.join(changed) + ' changed after version ' + version_id
             + ' was recorded. Nothing was overwritten and no approval was transferred.', 'INTEGRITY_FAILURE')
    return saved


def require_named(work, project, consumer, names):
    """A consumer may read only the inputs the active version names, unchanged."""
    saved = verify(work, project, names)
    missing = [name for name in names if name not in saved['references']]
    require(not missing, consumer + ' needs inputs the active version does not name: ' + ', '.join(missing))
    return saved


def bind_approval(project, phase):
    """Tie the current approval for a phase to the active version."""
    approval = (project.get('approvals') or {}).get(phase)
    if isinstance(approval, dict) and project.get('active_version'):
        approval['version_id'] = project['active_version']
    return approval


def supersede(project, phases, reason, at=None):
    """Move current approvals into history as superseded. Nothing is deleted from history."""
    stamp = at or time.time()
    moved = []
    for phase in phases:
        approval = (project.get('approvals') or {}).get(phase)
        if isinstance(approval, dict):
            project.setdefault('approval_history', []).append({
                'phase': phase, 'at': stamp, 'reason': reason, 'status': 'superseded',
                'approval': copy.deepcopy(approval)})
            moved.append(phase)
        project.get('approvals', {}).pop(phase, None)
    return moved


def superseded(project, phase):
    """Every earlier approval for a phase, newest last."""
    return [item for item in project.get('approval_history') or [] if item.get('phase') == phase]
