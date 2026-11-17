"""Human-guided orchestration of existing CLI operations; never bypass their gates."""
import json
from datetime import datetime
from pathlib import Path
from pilot import Blocked, require


def record_framework_update(ui, project):
    """Record a controller commit before approval. Findings stay on the saved run."""
    recorded = project.get('framework_commit')
    if not recorded:
        return True
    from reframe import FRAMEWORK, git
    if recorded == git(FRAMEWORK, 'rev-parse', 'HEAD'):
        return True
    ui.say('Reframe was updated after this run was saved. Record that update before approval. The findings stay unchanged.')
    note = ui.ask('Note for this Reframe update')
    if ui.invoke(['upgrade-framework', '--note', note, '--by', approver(ui, 'records this Reframe update')]) != 0:
        report = getattr(ui, 'last_report', None) or {}
        ui.say(str(report.get('hint') or report.get('reason') or 'The update was not recorded. /flow retries it before approval, skip, or review.'))
        return False
    return True


def workspace_path():
    """Return the active assessment folder, or nothing when no run is selected."""
    from pilot import Blocked
    from reframe_setup import workspace
    try:
        return workspace()
    except Blocked:
        return None


def say_review(ui, heading, rows):
    """Print each review file with its format and location."""
    ui.say(heading)
    for what, kind, location in rows:
        ui.say(what + ' — ' + kind + ' — ' + location)


def assessment_rows(project):
    """The assessment review page, the sealed findings, and the report index."""
    label = project.get('active_assessment') or project.get('selected')
    record = (project.get('assessments') or {}).get(label or '', {})
    directory = Path(record['directory']) if record.get('directory') else None
    if directory:
        work = directory.parent.parent if directory.parent.name == 'runs' else directory.parent
        return [
            ('Assessment review page', 'HTML', str(directory / 'assessment-review.html')),
            ('Sealed findings', 'ZIP, CSV, JSON, and PDF', str(directory / 'assessment')),
            ('Report index', 'HTML', str(work / 'reports' / 'index.html')),
        ]
    return [
        ('Assessment review page', 'HTML', 'runs/<run>/assessment-review.html'),
        ('Sealed findings', 'ZIP, CSV, JSON, and PDF', 'runs/<run>/assessment'),
        ('Report index', 'HTML', 'reports/index.html'),
    ]


def validation_rows(project):
    """The preparation review and the executor and reviewer JSON."""
    work = workspace_path()
    prefix = str(work) + '/' if work else ''
    spec = project.get('specification') or {}
    candidate = spec.get('path') or 'preparation/candidate-*.json'
    review = spec.get('review_path') or 'preparation/review-*.json'
    return [
        ('SME and architect review', 'HTML', prefix + 'preparation/review.html'),
        ('Executor candidate', 'JSON', prefix + candidate),
        ('Independent reviewer report', 'JSON', prefix + review),
    ]


def specification_rows(project):
    """The business wireframes and the screen and API JSON."""
    work = workspace_path()
    site = (project.get('site') or {}).get('directory')
    if work and site:
        directory = work / site
        return [
            ('Business review wireframes', 'HTML', str(directory / 'index.html')),
            ('Screen content', 'JSON', str(directory / 'screens.json')),
            ('API reference', 'HTML', str(directory / 'api.html')),
            ('OpenAPI document', 'JSON', str(directory / 'openapi.json')),
            ('API contracts', 'JSON', str(directory / 'api-contracts.json')),
            ('Token spend', 'HTML', str(directory / 'usage.html')),
        ]
    return [
        ('Business review wireframes', 'HTML', 'previews/business-*/index.html'),
        ('Screen content', 'JSON', 'previews/business-*/screens.json'),
        ('API reference', 'HTML', 'previews/business-*/api.html'),
        ('OpenAPI document', 'JSON', 'previews/business-*/openapi.json'),
        ('API contracts', 'JSON', 'previews/business-*/api-contracts.json'),
        ('Token spend', 'HTML', 'previews/business-*/usage.html'),
    ]


def draft_rows(name):
    """The skip wireframes, the handoff records, and the draft ZIP."""
    work = workspace_path()
    if not work:
        return [
            ('Wireframes', 'HTML', 'previews/' + name + '/handoff/index.html'),
            ('Imported rules', 'HTML', 'previews/' + name + '/handoff/rules.html'),
            ('Handoff records', 'JSON and Markdown', 'previews/' + name + '/handoff'),
            ('AI-DLC draft package', 'ZIP', 'packages/' + name + '/ai-dlc-draft.zip'),
        ]
    from reframe_workspace import preview_directory
    handoff = preview_directory(work, name) / 'handoff'
    archive = work / 'packages' / name / 'ai-dlc-draft.zip'
    return [
        ('Wireframes', 'HTML', str(handoff / 'index.html')),
        ('Imported rules', 'HTML', str(handoff / 'rules.html')),
        ('Handoff records', 'JSON and Markdown', str(handoff)),
        ('AI-DLC draft package', 'ZIP', str(archive)),
    ]


def package_rows(project):
    """The package ZIP, its status, and the folder of HTML, JSON, and Markdown it was built from."""
    work = workspace_path()
    package = project.get('package') or {}
    label = 'AI-DLC package (' + str(package.get('status') or 'awaiting acceptance').replace('_', ' ').lower() + ')'
    if package.get('route') == 'skip':
        label = 'Unverified skip-route AI-DLC package (' + str(package.get('status') or '').replace('_', ' ').lower() + ')'
    recorded = package.get('path')
    if work and recorded:
        archive = work / recorded
        folder = archive.with_suffix('')
        return [
            (label, 'ZIP', str(archive)),
            ('Package files', 'HTML, JSON, and Markdown', str(folder)),
        ]
    return [
        (label, 'ZIP', 'packages/package-<version>.zip'),
        ('Package files', 'HTML, JSON, and Markdown', 'packages/package-<version>'),
    ]


def open_question_ids(project):
    """Question ids with no recorded decision. An absent specification file means none yet."""
    record = project.get('specification') or {}
    work = workspace_path()
    if not work or not record.get('path'):
        return []
    path = work / record['path']
    if not path.is_file():
        return []
    from reframe import read, spec_path
    spec = read(spec_path(work, project))
    decided = project.get('decisions') or {}
    return [q['id'] for q in spec.get('questions') or [] if isinstance(q, dict) and q.get('id') not in decided]


def defer_open_questions(ui, project):
    """Record one confirmed deferral batch for every open SME question."""
    pending = open_question_ids(project)
    if not pending:
        return True
    ui.say(str(len(pending)) + ' SME questions are still open. A deferral is not an answer. Affected implementation remains blocked.')
    ui.say('Scope: ' + str(len(pending)) + ' open questions. Saved decisions stay unchanged.')
    if not ui.yes('Defer the ' + str(len(pending)) + ' open SME questions in one batch so the package can be written for review?'):
        ui.say('Paused. Record each SME answer with reframe decide, then return with /flow. No approval was recorded.')
        return False
    owner = ui.ask('Accountable owner for these deferred questions')
    note = ui.ask('Reason for deferring the open questions')
    if ui.invoke(['decide', '--open', '--by', owner, '--answer', note, '--disposition', 'deferred', '--confirm']) != 0:
        ui.say('A deferral was not recorded. /flow retries the open questions in one batch. No approval was recorded.')
        return False
    report = getattr(ui, 'last_report', None) or {}
    ui.say('Recorded ' + str(report.get('recorded', len(pending))) + '. Remaining ' + str(report.get('remaining', 0))
           + '. Skipped ' + str(report.get('skipped', 0)) + '.')
    return True


def offer_review_budget(ui, project):
    """Say when the paired review does not fit the saved cap. A larger cap is recorded only after a yes."""
    state = project.get('pipeline') or {}
    if state.get('reason') != 'Insufficient call budget for remaining checkpoint plan':
        ui.say('Verification paused. Inspect status and any budget or evidence blocker before continuing.')
        return None
    needed = state.get('minimum_additional_calls')
    spent = state.get('calls', 0) or 0
    ui.say('The review plan needs at least ' + str(needed) + ' more model calls. The saved allowance leaves '
           + str(state.get('remaining_calls')) + '. ' + str(spent) + ' model calls were already used.')
    cap = spent + needed if isinstance(needed, int) else None
    if not isinstance(cap, int) or not spent < cap:
        ui.say('The remaining plan has no usable call count. No model call was made.')
        return None
    if not ui.yes('Raise the model-call cap to ' + str(cap) + ' and start the review?'):
        if ui.yes('Remove the saved call cap and keep the completed work?'):
            owner = ui.ask('Accountable owner for this call budget')
            note = ui.ask('Reason for this call budget')
            if ui.invoke(['model-budget', '--clear-call-cap', '--by', owner, '--note', note]) != 0:
                return None
            if ui.invoke(['validate']) != 0:
                return ui.project()
            return ui.project()
        ui.say('Review stayed within the saved cap. No model call was made.')
        return None
    owner = ui.ask('Accountable owner for this call budget')
    note = ui.ask('Reason for this call budget')
    if ui.invoke(['model-budget', '--max-calls', str(cap), '--by', owner, '--note', note]) != 0:
        return None
    if ui.invoke(['validate']) != 0:
        return ui.project()
    return ui.project()


def offer_dollar_budget(ui, project):
    """Ask before raising the model dollar cap. The provider account remains the spend limit."""
    state = project.get('pipeline') or {}
    if state.get('reason') != 'Model call would exceed the dollar cap':
        return None
    settings = project.get('settings') or {}
    spent = settings.get('model_dollars_spent', 0)
    cap = settings.get('max_model_dollars', 0)
    price = state.get('next_call_price') or 0
    ui.say('Model dollars spent ' + str(spent) + ' of cap ' + str(cap) + '. The next billed call needs ' + str(price) + '.')
    if not ui.yes('Raise the model dollar cap so this call can run?'):
        ui.say('The review stayed within the saved dollar cap. No model call was made.')
        return None
    owner = ui.ask('Accountable owner for this dollar budget')
    note = ui.ask('Reason for this dollar budget')
    amount = ui.ask('Model dollar cap', str(round(max(cap, spent) + price, 2)))
    try:
        value = float(amount)
    except ValueError:
        ui.say('The dollar cap was not a number. No model call was made.')
        return None
    if ui.invoke(['model-budget', '--max-dollars', str(value), '--by', owner, '--note', note]) != 0:
        return None
    return ui.project()


def _choose_match(ui, matches):
    """Ask only when more than one saved workspace matches the repository."""
    if len(matches) == 1:
        return matches[0]
    for index, folder in enumerate(matches, start=1):
        ui.say(str(index) + ' ' + str(folder))
    picked = ui.ask('Saved workspace number', '1')
    require(picked.isdigit() and 1 <= int(picked) <= len(matches), 'Choose one of the saved workspaces')
    return matches[int(picked) - 1]


def offer_known_repository(ui, repository=None):
    """Recognize a repository before setup. A failed reuse check does not provision a replacement."""
    repository = repository or ui.ask('Repository URL to recognize')
    from reframe_projects import load_project, matching_workspaces, pin_requested_revision, verify_saved_infrastructure
    matches = matching_workspaces(repository)
    if not matches:
        ui.say('No saved project matches this repository. A new project is separate from every saved sandbox.')
        if not ui.yes('Create a new project?'):
            ui.say('No project was created.')
            return False
        return repository
    folder = _choose_match(ui, matches)
    saved = load_project(folder)
    ui.say('Saved project recognized at ' + str(folder) + '.')
    choice = ui.ask('Choose resume, reuse-baseline, assess-new-revision, or new-project', 'resume')
    require(choice in {'resume', 'reuse-baseline', 'assess-new-revision', 'new-project'},
            'Choose resume, reuse-baseline, assess-new-revision, or new-project')
    if choice == 'new-project':
        ui.say('A new project does not reuse this sandbox.')
        if not ui.yes('Create a new project?'):
            ui.say('No project was created.')
            return False
        return repository
    try:
        verify_saved_infrastructure(saved)
    except Blocked as error:
        ui.say(str(error))
        ui.say('Reuse is paused. No new resources were created.')
        return False
    from reframe_optional import resource_plan
    from reframe_setup import select_workspace
    import reframe
    intent = {'resume': 'resume', 'reuse-baseline': 'reuse-baseline', 'assess-new-revision': 'new-assessment'}[choice]
    plan = resource_plan(saved, intent)
    ui.say('Infrastructure verified. AWS jobs created: ' + str(plan['aws_jobs_created']) + '.')
    select_workspace(folder)
    if choice == 'reuse-baseline':
        ui.say('The saved baseline stays in place. No assessment job was created.')
        return True
    if choice == 'resume':
        ui.say('Resuming the saved job. No new assessment job was created.')
        return True
    if (saved.get('source') or {}).get('root'):
        ref = ui.ask('Source revision to assess', saved['source'].get('commit') or 'HEAD')
        try:
            pinned = pin_requested_revision(folder, saved, ref)
        except Blocked as error:
            ui.say(str(error))
            ui.say('Reuse is paused. No new resources were created.')
            return False
        reframe.persist(folder, saved)
        ui.say('Pinned revision ' + pinned['commit'] + '. The saved baseline and its approvals stay in place.')
    if not ui.yes('Authorize one new assessment of this revision on the verified infrastructure?'):
        # A declined assessment ends this /flow; it does not walk on into the saved project's gates.
        ui.say('No assessment job was created. The pinned revision is saved; /flow continues the saved project.')
        return False
    command = ['assess', '--wait', '--allow-new-assessment']
    pending = saved.get('pending_revision') or {}
    if pending.get('commit'):
        command += ['--label', 'revision-' + pending['commit'][:8]]
    if ui.invoke(command) != 0:
        ui.say('The assessment was not started. No replacement sandbox was created.')
        return False
    return True


def finish_guided_design(ui, project):
    """Ask for mode, version, stack, and optional context, then write the draft package."""
    from reframe import budget_summary
    work = workspace_path()
    summary = budget_summary(project or {}, work)

    def cap_text(value):
        """Name the cap and say it applies to this role only."""
        return 'no call cap' if value is None else 'a per-role cap of ' + str(value)

    ui.say('Preparation model calls used ' + str(summary['preparation_calls']) + ' with ' + cap_text(summary['preparation_cap'])
           + '. Completed units ' + str(summary.get('completed_units', 0)) + '. Remaining units ' + str(summary.get('remaining_units', 0)) + '.')
    ui.say('Wireframe model calls used ' + str(summary['wireframe_calls']) + ' with ' + cap_text(summary['wireframe_cap']) + '.')
    ui.say('Skip-draft model calls used ' + str(summary['skip_draft_calls'])
           + '. Failed attempts ' + str(summary.get('skip_failures', 0)) + ' of limit ' + str(summary.get('skip_failure_limit', 3)) + '.')
    from reframe import spend_text
    ui.say('Total model calls across roles ' + str(summary.get('total_calls', 0)) + '. ' + summary.get('call_cap_note', ''))
    ui.say(spend_text(summary))
    if summary.get('next_call_estimate') is not None:
        ui.say('Estimated next billed call ' + str(summary['next_call_estimate']) + '. This estimate is not measured spend.')
    mode = ui.ask('Design mode (functional-parity/reimagine)', 'functional-parity')
    require(mode in {'functional-parity', 'reimagine'}, 'Choose functional-parity or reimagine')
    version = ui.ask('Design version', 'v1')
    stack = ui.ask('Target stack', 'unspecified')
    context = ui.ask('Human context file, or none', 'none')
    if context not in {'', 'none'}:
        author = ui.ask('Context author')
        role = ui.ask('Context role', 'architect')
        category = ui.ask('Context category (current-state/future-state/clarification)', 'clarification')
        require(category in {'current-state', 'future-state', 'clarification'}, 'Choose a context category')
        affected = ui.ask('Affected ids, comma separated', '')
        if ui.invoke(['context', 'import', '--file', context, '--by', author, '--role', role,
                      '--category', category, '--affected', affected]) != 0:
            ui.say('The context file was not imported. The design was not written.')
            return
        from reframe_optional import context_status
        pending = [item for item in context_status(work).get('submissions') or [] if item.get('disposition') == 'proposed']
        disposition = ui.ask('Disposition for the imported context (accepted/rejected)', 'rejected')
        require(disposition in {'accepted', 'rejected'}, 'Choose accepted or rejected')
        if pending and ui.invoke(['context', 'decide', '--id', pending[-1]['id'], '--disposition', disposition,
                                  '--by', author, '--note', 'Recorded in the guided flow']) != 0:
            ui.say('The context disposition was not recorded. The design was not written.')
            return
        if category == 'future-state' and disposition == 'accepted':
            ui.say('Accepting this note records input only. It does not authorize a behavior change.')
    if not offer_open_conflicts(ui, work):
        return
    if ui.invoke(['design-export', '--version', version, '--mode', mode, '--stack', stack]) != 0:
        say_design_recovery(ui)
        return
    report = getattr(ui, 'last_report', None) or {}
    if report.get('resumed'):
        ui.say('Incomplete generation was resumed from the saved selection. No new model call was required.')
        ui.say('Review the completed version before packaging.')
    if category_was_future(context, locals()) and ui.yes('Approve one future-state delta as an implementation requirement?'):
        proposal = ask_proposal_id(ui, proposal_ids(version), 'Proposal id to approve', None)
        if proposal:
            owner = ui.ask('Delta approver')
            note = ui.ask('Delta approval note')
            if ui.invoke(['context', 'approve-delta', '--version', version, '--id', proposal, '--by', owner, '--note', note]) != 0:
                ui.say('The delta was not approved. The proposal stays proposed_unapproved.')
    if ui.invoke(['package-export', '--version', version, '--mode', mode]) != 0:
        ui.say('The draft ZIP was not written. /flow retries packaging. No final handoff was created.')
        return
    ui.say('Draft ' + mode + ' package written for ' + version + '. It stays DRAFT and is not the authorized implementation handoff.')


def simulated_flags():
    """Approvals made by a labeled test actor carry --simulated; they are never genuine sign-off."""
    import os
    return ['--simulated'] if os.environ.get('REFRAME_SIMULATED_ACTOR') == '1' else []


NOT_A_NAME = {'y', 'n', 'yes', 'no', 'none', 'ok', 'true', 'false'}


def _person(value):
    """A typed person name. A yes/no answer or a blank is not a name."""
    name = str(value or '').strip()
    require(name and name.casefold() not in NOT_A_NAME, 'Enter a person\'s name, not "' + name + '"')
    return name


def ask_person(ui, prompt, default=None):
    """Ask for a person's name. A yes/no answer or a blank is refused and asked again, up to three times."""
    for _attempt in range(2):
        value = ui.ask(prompt, default) if default is not None else ui.ask(prompt)
        if str(value or '').strip() and str(value).strip().casefold() not in NOT_A_NAME:
            return value.strip()
        ui.say('Enter a person\'s name, not "' + str(value or '').strip() + '". Nothing was recorded.')
    return _person(ui.ask(prompt, default) if default is not None else ui.ask(prompt))


def reviewer(ui):
    """The person recording review decisions in this session, asked once."""
    name = getattr(ui, 'reviewer_name', None)
    if not name:
        ui.reviewer_name = ask_person(ui, 'Your name for these review records')
    return ui.reviewer_name


def approver(ui, what):
    """Ask who makes this approval at this gate. The session name is offered, never assumed."""
    return ask_person(ui, 'Who ' + what + '? Their name is recorded on it', reviewer(ui))


def known_ids(work):
    """Rule, question, journey, screen, and API ids a context note can name, from the current specification and design."""
    if not work:
        return []
    import reframe
    ids = []
    try:
        project = json.loads((Path(work) / 'project.json').read_text())
        ids += sorted(reframe.spec_scope_ids(work, project))
    except (OSError, ValueError, KeyError, Exception):
        return ids
    return list(dict.fromkeys(str(item) for item in ids if item))


def ask_existing_file(ui, label, allow_none=False):
    """Ask for a file path and check it at once. Three missing paths stop with nothing recorded."""
    for _attempt in range(3):
        value = ui.ask(label, 'none' if allow_none else None).strip()
        if allow_none and value in {'', 'none'}:
            return 'none'
        if Path(value).expanduser().is_file():
            return value
        ui.say('No file was found at that path. Nothing was recorded. Enter the path again' + (', or none.' if allow_none else '.'))
    ui.say('Stopped after three paths that were not found. Nothing was recorded.')
    return None


def offer_context(ui, gate):
    """Optional Markdown at one review gate. None is valid and is recorded; nothing is inferred from a missing file."""
    work = workspace_path()
    if work and not offer_open_conflicts(ui, work):
        return False
    import reframe_optional
    for _attempt in range(3):
        path = ask_existing_file(ui, 'Markdown context for the ' + gate + ' review, or none', allow_none=True)
        if path is None:
            return False
        if path in {'', 'none'}:
            return ui.invoke(['context', 'none', '--gate', gate, '--by', reviewer(ui)]) == 0
        # A file that would be refused is refused before the category, ids, and role are asked.
        problem = reframe_optional.context_file_problem(work, path) if work else None
        if not problem:
            break
        ui.say(problem + ' Enter another path, or none.')
    else:
        ui.say('Stopped after three refused files. Nothing was recorded.')
        return False
    category = ui.ask('Context category (clarification/correction/constraint/current-state/future-state/review-feedback)',
                      'clarification')
    known = known_ids(work)
    if known:
        ui.say('Ids you can name: ' + ', '.join(known[:40]) + (' and ' + str(len(known) - 40) + ' more' if len(known) > 40 else '')
               + '. A future-state note can name a journey, a screen, or an API.')
    affected = ui.ask('Affected ids, comma separated, or blank', '')
    role = ui.ask('Your role for this context', 'reviewer')
    if ui.invoke(['context', 'import', '--file', path, '--by', reviewer(ui), '--role', role, '--category', category,
                  '--affected', affected, '--gate', gate]) != 0:
        ui.say('The context file was not imported. Nothing else changed.')
        return False
    imported = (getattr(ui, 'last_report', None) or {}).get('id')
    disposition = ui.ask('Admit this context as input (accepted) or keep it out (rejected)', 'accepted')
    require(disposition in {'accepted', 'rejected'}, 'Choose accepted or rejected')
    if imported and ui.invoke(['context', 'decide', '--id', imported, '--disposition', disposition, '--by', reviewer(ui),
                               '--note', 'Recorded at the ' + gate + ' review']) != 0:
        ui.say('The disposition was not recorded. The submission stays proposed.')
        return False
    if category == 'future-state' and disposition == 'accepted':
        ui.say('Accepting this note records input only. It does not authorize a behavior change.')
    if work and disposition == 'accepted':
        from reframe_optional import open_conflicts
        if any(item.get('submission_id') == imported for item in open_conflicts(work)):
            ui.say('This context contradicts recorded evidence. The conflict is shown now; it blocks the approvals it affects.')
            return offer_open_conflicts(ui, work)
    return True


def baseline_inputs(ui, project):
    """After the assessment baseline: requirements (generated, imported, or none) and optional context."""
    from reframe_optional import gate_records
    requirements = project.get('requirements') or {}
    if requirements.get('state') in {None, 'NOT_REQUESTED'}:
        ui.invoke(['requirements', 'status'])
        report = getattr(ui, 'last_report', None) or {}
        requestable = report.get('status') == 'GENERATION_REQUESTABLE'
        if not requestable:
            ui.say('Integrated AWS requirements generation is not available: ' + str(report.get('reason') or 'capability not verified')
                   + ' You can import externally generated requirements, labeled imported, or continue without them.')
        options = 'generate/import/none' if requestable else 'import/none'
        choice = ui.ask('Business requirements (' + options + ')', 'generate' if requestable else 'none')
        require(choice in set(options.split('/')), 'Choose ' + options)
        if choice == 'generate' and not generate_requirements(ui):
            return False
        if choice == 'import':
            path = ask_existing_file(ui, 'Path to requirements.md')
            if path is None:
                return False
            trace = ask_existing_file(ui, 'Path to traceability.yaml, or none', allow_none=True)
            if trace is None:
                return False
            function = ui.ask('Business function id for these files')
            note = ui.ask('Where these files came from')
            command = ['requirements', 'import', '--requirements', path, '--function', function, '--by', reviewer(ui), '--note', note]
            if trace.strip() not in {'', 'none'}:
                command += ['--traceability', trace]
            if ui.invoke(command) != 0:
                ui.say('The requirements were not imported. Nothing else changed.')
                return False
            report = getattr(ui, 'last_report', None) or {}
            ui.say('Imported ' + str(report.get('count', 0)) + ' requirement records, labeled imported. '
                   + str(report.get('unrecognized_lines', 0)) + ' lines named an id in an unrecognized shape.')
            for warning in report.get('warnings') or []:
                ui.say('Warning: ' + warning)
        if choice == 'none' and ui.invoke(['requirements', 'none', '--by', reviewer(ui)]) != 0:
            return False
    work = workspace_path()
    if not work or 'baseline' not in gate_records(work):
        if not offer_context(ui, 'baseline'):
            return False
    return True


def generate_requirements(ui):
    """Authorize one requirements job, then advance it until retrieval or a person is needed."""
    functions = ui.ask('Business functions to generate, comma separated (blank to choose from the catalog)', '')
    note = ui.ask('Reason for this new AWS requirements job')
    if not ui.yes('Authorize one new AWS requirements job? AWS charges and resources may apply.'):
        return False
    if ui.invoke(['requirements', 'authorize-job', '--functions', functions, '--by', reviewer(ui), '--note', note]) != 0:
        return False
    for _ in range(20):
        code = ui.invoke(['requirements', 'resume'])
        report = getattr(ui, 'last_report', None) or {}
        status = report.get('status')
        if code != 0 or status in {'REQUIREMENTS_FAILED', 'REQUIREMENTS_NEEDS_RECONCILIATION'}:
            ui.say('Requirements generation stopped: ' + str(report.get('reason') or status))
            return False
        if status == 'REQUIREMENTS_RETRIEVED':
            return True
        if status == 'REQUIREMENTS_WAITING_FOR_HUMAN':
            catalog = report.get('catalog') or []
            if not catalog:
                ui.say(str(report.get('reason')))
                return False
            selection = ui.ask('Select business functions from ' + ', '.join(catalog))
            if ui.invoke(['requirements', 'resume', '--select', selection]) != 0:
                return False
    ui.say('The requirements job is still running. /flow continues the same job.')
    return False


def ensure_design_plan(ui, project):
    """Capture mode and target constraints before any detailed design call."""
    if project.get('design_plan'):
        return True
    mode = ui.ask('Design mode (functional-parity/reimagine)', 'functional-parity')
    require(mode in {'functional-parity', 'reimagine'}, 'Choose functional-parity or reimagine')
    version = ui.ask('Design version', 'v1')
    language = ui.ask('Target language or stack', 'unspecified')
    constraints = ui.ask('Architecture constraints separated by semicolons, or none', 'none')
    command = ['design-plan', '--mode', mode, '--version', version, '--language', language, '--by', reviewer(ui)]
    for item in constraints.split(';'):
        if item.strip() and item.strip() != 'none':
            command += ['--constraint', item.strip()]
    return ui.invoke(command) == 0


def proposal_ids(version):
    """The Reimagine proposal ids recorded for one design version."""
    work = workspace_path()
    path = work / 'previews' / str(version) / 'future-state' / 'deltas.json' if work else None
    deltas = json.loads(path.read_text()) if path and path.is_file() else {}
    return [str(item.get('id')) for item in deltas.get('proposals') or []]


def ask_proposal_id(ui, known, prompt, default):
    """A proposal id from the recorded list, checked before the approver is asked. Three unknown ids record nothing."""
    for _attempt in range(3):
        value = (ui.ask(prompt, default) if default is not None else ui.ask(prompt)).strip()
        if value in {'', 'none'} or value in known:
            return value
        ui.say('No proposal ' + value + ' is recorded for this version. Proposals: ' + (', '.join(known) or 'none') + '.')
    ui.say('Stopped after three unknown proposal ids. No delta was approved.')
    return None


def masked(text):
    """Text with credential- or identifier-shaped values replaced, for printing on the console."""
    import reframe
    data = text.encode()
    for _kind, pattern in reframe.SECRET_PATTERNS:
        data = pattern.sub(b'[hidden value]', data)
    return data.decode(errors='replace')


def design_review(ui, project, skip_route):
    """Design review: context, Reimagine proposals, then approve or route feedback to design or specification."""
    plan = project.get('design_plan') or {}
    if not offer_context(ui, 'design'):
        return 'stop'
    # Both routes show the Reimagine proposals here; the package carries this same completed version.
    if plan.get('mode') == 'reimagine':
        exported = ui.invoke(['design-export', '--version', plan['version'], '--mode', 'reimagine', '--stack',
                              (plan.get('target') or {}).get('language') or 'unspecified']) == 0
        if not exported and 'immutable' in str((getattr(ui, 'last_report', None) or {}).get('reason') or ''):
            ui.say('Design version ' + str(plan['version']) + ' is complete and cannot change. New context reaches the design '
                   'through design-change, which starts the next version and keeps this one.')
        if exported:
            ui.say('Future-state proposals stay proposed_unapproved until a person approves a named delta.')
            work = workspace_path()
            deltas_path = work / 'previews' / str(plan['version']) / 'future-state' / 'deltas.json' if work else None
            deltas = json.loads(deltas_path.read_text()) if deltas_path and deltas_path.is_file() else {}
            for item in deltas.get('proposals') or []:
                ui.say('Proposal ' + str(item.get('id')) + ' (' + str(item.get('status')) + '): ' + masked(str(item.get('after') or ''))[:160])
            if not deltas.get('proposals'):
                ui.say('No proposal was made. ' + '; '.join(str(gap.get('reason')) for gap in (deltas.get('gaps') or [])[:3]))
            proposal = ask_proposal_id(ui, [str(item.get('id')) for item in deltas.get('proposals') or []],
                                       'Approve one future-state delta by id, or none', 'none') or 'none'
            if proposal.strip() not in {'', 'none'}:
                by = approver(ui, 'approves this delta')
                note = ui.ask('Rationale for approving this delta')
                ui.invoke(['context', 'approve-delta', '--version', plan['version'], '--id', proposal, '--by', by, '--note', note])
    decision = ui.ask('Design decision (approve/design-change/behavior-change/pause)', 'pause')
    require(decision in {'approve', 'design-change', 'behavior-change', 'pause'}, 'Choose approve, design-change, behavior-change, or pause')
    if decision == 'pause':
        ui.say('Paused for human review. No approval was recorded. Return with /flow.')
        return 'stop'
    if decision == 'approve':
        by = approver(ui, 'approves this design')
        note = ui.ask('Your rationale for approving this design')
        phase = 'design' if skip_route else 'specifications'
        return 'continue' if ui.invoke(['approve', phase, '--by', by, '--note', note] + simulated_flags()) == 0 else 'stop'
    note = ui.ask('Describe the change you need')
    scope = 'design' if decision == 'design-change' else 'specification'
    return 'continue' if ui.invoke(['feedback', '--scope', scope, '--by', reviewer(ui), '--note', note]) == 0 else 'stop'


def package_review(ui, project):
    """Final package review: inventory, exact hash, gaps; then accept that hash or route changes."""
    say_review(ui, 'Review this package before you decide. It is not accepted until you accept its exact SHA-256.',
               package_rows(project))
    if ui.invoke(['package-review']) != 0:
        return 'stop'
    report = getattr(ui, 'last_report', None) or {}
    readiness = report.get('readiness') or {}
    ui.say('Package ' + str(report.get('package')) + ' SHA-256 ' + str(report.get('sha256')) + ' with '
           + str(len(report.get('inventory') or [])) + ' files. Verification ' + str(report.get('verification')) + '.')
    ui.say('Implementation readiness ' + str(readiness.get('state')) + ' with ' + str(readiness.get('blocker_count', 0))
           + ' recorded blockers. Accepting the package does not make blocked work ready.')
    if not offer_context(ui, 'package'):
        return 'stop'
    import reframe_acceptance
    work = workspace_path()
    current = ui.project() or project
    if work and reframe_acceptance.context_changed(work, current):
        ui.say('Context or a conflict changed after this package was built. Rebuilding so the package carries it. '
               'The earlier package stays on disk and was not accepted.')
        if ui.invoke(['package']) == 0:
            return 'continue'
        offer_withdraw_flagged_context(ui)
        return 'stop'
    decision = ui.ask('Package decision (accept/design-change/behavior-change/pause)', 'pause')
    require(decision in {'accept', 'design-change', 'behavior-change', 'pause'}, 'Choose accept, design-change, behavior-change, or pause')
    if decision == 'pause':
        ui.say('Paused. The package awaits acceptance. Nothing was accepted.')
        return 'stop'
    if decision == 'accept':
        current = ui.project() or project
        if current.get('verification_skip') and not (current.get('approvals') or {}).get('verification-skip'):
            ui.say('This package skipped independent verification. The documented policy needs a second person to accept that skip.')
            second = ui.ask('Second person accepting the verification skip')
            skip_note = ui.ask('Their rationale for accepting the skip')
            if ui.invoke(['approve', 'verification-skip', '--by', second, '--note', skip_note] + simulated_flags()) != 0:
                return 'stop'
        by = approver(ui, 'accepts this exact package')
        note = ui.ask('Your rationale for accepting this exact package')
        if ui.invoke(['accept-package', '--sha256', str(report.get('sha256')), '--by', by, '--note', note]
                     + simulated_flags()) != 0:
            return 'stop'
        accepted = getattr(ui, 'last_report', None) or {}
        ui.say('Accepted package ' + str(report.get('sha256')) + '. Implementation readiness stays '
               + str(accepted.get('implementation_readiness')) + '.')
        return 'done'
    note = ui.ask('Describe the change you need')
    scope = 'design' if decision == 'design-change' else 'specification'
    return 'continue' if ui.invoke(['feedback', '--scope', scope, '--by', reviewer(ui), '--note', note]) == 0 else 'stop'


def offer_open_conflicts(ui, work):
    """Show conflicts that already exist, including when this turn imports no context."""
    from reframe_optional import open_conflicts
    conflicts = open_conflicts(work) if work else []
    if not conflicts:
        return True
    ui.say(str(len(conflicts)) + ' unresolved context conflicts are visible. Final approval and authorized handoff stay blocked until they are resolved.')
    for conflict in conflicts:
        ui.say('Conflict ' + str(conflict.get('id')) + ' contradicts ' + str(conflict.get('contradicts') or 'recorded evidence') + '.')
    if ui.yes('Resolve the open context conflict now?'):
        conflict = conflicts[0]
        resolution = ui.ask('Conflict resolution (keep-evidence/keep-human-statement/needs-more-evidence)', 'keep-evidence')
        owner = ui.ask('Conflict resolver')
        note = ui.ask('Conflict resolution note')
        if ui.invoke(['context', 'resolve', '--id', conflict['id'], '--resolution', resolution,
                      '--by', owner, '--note', note]) != 0:
            ui.say('The conflict remains open. The draft can still be written. Final approval stays blocked.')
        return True
    if ui.yes('Defer the open conflict and continue? It stays open and keeps blocking the approvals it affects.'):
        conflict = conflicts[0]
        owner = ui.ask('Who is deferring this conflict')
        note = ui.ask('Why it is deferred and what evidence is needed')
        if ui.invoke(['context', 'resolve', '--id', conflict['id'], '--resolution', 'needs-more-evidence',
                      '--by', owner, '--note', note]) != 0:
            ui.say('The deferral was not recorded. The conflict stays open.')
        ui.say('The conflict stays open and keeps blocking the approvals it affects. Other work can continue.')
        return True
    ui.say('Paused. Resolve the conflict or defer it before the design is written.')
    return False


def flagged_design_outputs(work, project):
    """Folders of the current design version or skip draft whose files look like a credential, by folder name only."""
    import reframe
    folders = []
    plan = project.get('design_plan') or {}
    if plan.get('version'):
        folders.append(Path(work) / 'previews' / str(plan['version']))
    if project.get('skip_bundle'):
        folders.append(Path(work) / project['skip_bundle'])
    flagged = []
    for folder in folders:
        if folder.is_dir() and any(path.is_file() and any(pattern.search(path.read_bytes()) for _kind, pattern in reframe.SECRET_PATTERNS)
                                   for path in folder.rglob('*')):
            flagged.append(folder.name)
    return flagged


def offer_withdraw_flagged_context(ui):
    """After a package refusal, offer to reject accepted context whose stored text looks like a credential.

    The value itself is never printed. Rejecting keeps the submission on record; it only stops it reaching new outputs.
    A completed design version that already carries the value cannot change, so a design change starts the next one.
    """
    reason = str((getattr(ui, 'last_report', None) or {}).get('reason') or '')
    work = workspace_path()
    if not work or not reason.startswith('Refusing package'):
        return
    import reframe
    import reframe_optional as optional
    flagged = []
    for item in optional.context_status(work).get('submissions') or []:
        stored = optional.context_dir(work) / 'extracted' / (str(item.get('id')) + '.txt')
        if item.get('disposition') == 'accepted' and stored.is_file() and any(
                pattern.search(stored.read_bytes()) for _kind, pattern in reframe.SECRET_PATTERNS):
            flagged.append(item['id'])
    if flagged:
        ui.say('Accepted context ' + ', '.join(flagged) + ' contains text that looks like a credential or identifier, '
               'so it cannot be packaged. Rejecting it keeps the record and leaves it out of new design versions.')
    for submission in flagged:
        if not ui.yes('Reject context ' + submission + ' now?'):
            ui.say('Nothing was changed. The package stays blocked until that context is rejected or superseded.')
            return
        by = approver(ui, 'rejects this context')
        note = ui.ask('Why it is rejected', 'Contains a credential-shaped value')
        if ui.invoke(['context', 'decide', '--id', submission, '--disposition', 'rejected', '--by', by, '--note', note]) != 0:
            return
    outputs = flagged_design_outputs(work, ui.project() or {})
    if not outputs:
        if flagged:
            ui.say('Rejected. /flow builds the package again.')
        return
    ui.say('The design outputs ' + ', '.join(outputs) + ' already carry that text and cannot change; a completed version '
           'is immutable. A design change starts the next version from accepted context only. It needs a new counted '
           'model call, and the design is reviewed again before the package is built.')
    if not ui.yes('Start a design change now?'):
        ui.say('Nothing was changed. The package stays blocked; /flow offers the design change again.')
        return
    by = approver(ui, 'requests this design change')
    note = ui.ask('Why the design changes', 'Leave out rejected context that looks like a credential')
    if ui.invoke(['feedback', '--scope', 'design', '--by', by, '--note', note]) == 0:
        ui.say('Design change recorded. /flow generates the next version and returns to the design gate.')


def offer_wireframe_retry(ui):
    """After a failed or invalid wireframe call: authorize one new counted attempt, or stop. The failed call stays counted."""
    import reframe
    work = workspace_path()
    current = ui.project() or {}
    if not work or not reframe.failed_wireframe_stages(work, current):
        return False
    ui.say('The wireframe call failed or returned invalid output. It stays counted, and its receipt is kept. '
           'A new attempt makes another counted provider call.')
    if not ui.yes('Authorize one new wireframe attempt now?'):
        ui.say('Paused. Nothing was changed. /flow offers the new attempt again.')
        return False
    owner = approver(ui, 'authorizes the new attempt')
    note = ui.ask('Why a new attempt is acceptable')
    if ui.invoke(['retry-wireframes', '--by', owner, '--note', note]) != 0:
        return False
    ui.say('The new attempt is authorized. Generating the review site now.')
    return ui.invoke(['review-site']) == 0 or offer_wireframe_retry(ui)


def say_design_recovery(ui):
    """Tell the operator which recovery applies without repeating hidden paths."""
    from reframe_terminal import recovery_notice
    report = getattr(ui, 'last_report', None) or {}
    notice = recovery_notice(report.get('reason'), report)
    if notice:
        ui.say(notice['summary'])
        ui.say(notice['next_step'])
        return
    ui.say('The design was not written. /flow resumes the same version when its completion record is missing.')


def category_was_future(context, names):
    """True when this turn imported a future-state note."""
    return context not in {'', 'none'} and names.get('category') == 'future-state' and names.get('disposition') == 'accepted'


FLOW_STEPS = 40


def run(ui):
    """Walk a saved project from setup through assessment, skip or review, approvals, and the package."""
    from reframe_setup import workspace
    project = ui.project()
    if project:
        choice = ui.ask('Continue saved project, recognize a repository, or start a fresh run? (continue/recognize/fresh)', 'continue')
        require(choice in {'continue', 'recognize', 'fresh'}, 'Choose continue, recognize, or fresh')
        if choice == 'recognize':
            recognized = offer_known_repository(ui, (project.get('source') or {}).get('repository'))
            if not recognized:
                return
            if isinstance(recognized, str) and ui.invoke(['init', '--guided', '--source', recognized]) != 0:
                return
            project = ui.project()
        elif choice == 'fresh':
            source = (project.get('source') or {}).get('repository')
            require(source, 'The saved project has no repository to carry into setup')
            ui.say('The new run uses the recognized repository ' + source + '.')
            parent = ui.ask('Parent directory for the new run', str(workspace().parent / ('run-' + datetime.now().strftime('%Y%m%d-%H%M%S'))))
            from reframe_workspace import output_directory
            require(not output_directory(parent, source).exists(), 'Output directory already exists; choose another parent or continue it')
            if ui.invoke(['init', '--guided', '--source', source, '--output-parent', parent]) != 0:
                return
            project = ui.project()
        else:
            repository = (project.get('source') or {}).get('repository')
            if repository:
                from reframe_projects import matching_workspaces
                from reframe_setup import select_workspace
                matches = matching_workspaces(repository)
                if len(matches) > 1:
                    folder = _choose_match(ui, matches)
                    select_workspace(folder)
                    project = ui.project()
    if not project:
        recognized = offer_known_repository(ui)
        if not recognized:
            return
        if isinstance(recognized, str) and ui.invoke(['init', '--guided', '--source', recognized]) != 0:
            return
        project = ui.project()
    if not project or project.get('stage') in {'INITIALIZED', 'WAITING_FOR_CONNECTOR_APPROVAL'}:
        if ui.invoke(['init', '--guided']) != 0:
            return
    for _ in range(FLOW_STEPS):
        project = ui.project()
        require(project is not None, 'Setup did not save a project; use /flow to retry')
        stage = project['stage']
        import reframe
        work = workspace_path()
        if work and not project.get('site') and project.get('approvals', {}).get('validation') \
                and reframe.failed_wireframe_stages(work, project):
            # A failed wireframe call is offered again on every /flow until a person authorizes or stops.
            if not offer_wireframe_retry(ui):
                return
            continue
        approved = bool(project.get('approvals', {}).get('assessment'))
        if not record_framework_update(ui, project):
            return
        if project.get('skip_bundle') and project.get('verification_skip') and not project.get('specification') \
                and not project.get('approvals', {}).get('design') and stage not in {'DESIGN_APPROVED', 'PACKAGE_ACCEPTED'} \
                and not (project.get('package') or {}).get('path'):
            # A saved draft waiting at the design gate resumes there; nothing is regenerated or asked again.
            draft = Path(project['skip_bundle']).name
            ui.say('Resuming the design review of saved draft ' + draft + '. Nothing is regenerated.')
            say_review(ui, 'Review these draft files. They are not an approval.', draft_rows(draft))
            if design_review(ui, project, skip_route=True) != 'continue':
                return
            continue
        later = {'AWAITING_VALIDATION_APPROVAL', 'DESIGN_APPROVED', 'AWAITING_PACKAGE_ACCEPTANCE', 'PACKAGED', 'PACKAGE_ACCEPTED'}
        if approved and not project.get('approvals', {}).get('validation') and stage not in later:
            interrupted = stage in {'WAITING_FOR_RUNTIME', 'RUNNING_EXECUTOR', 'RUNNING_REVIEWER', 'PREPARATION_PLANNED', 'REWORK_LIMIT',
                                    'REVISION_PENDING'} and project.get('pipeline')
            if interrupted:
                ui.say('Resuming the saved review. Completed calls stay recorded. No new assessment job is created.')
                code = ui.invoke(['resume'])
                updated = ui.project() or {}
            else:
                if not baseline_inputs(ui, project):
                    return
                import reframe
                import reframe_preview
                available, why = reframe_preview.skip_available(project, reframe) if project.get('selected') else (True, None)
                reviewable, unanchored = True, None
                if project.get('selected') and workspace_path():
                    try:
                        # Findings without a source line would stop review before any call; say so instead of offering it.
                        reframe.require_anchored_export(workspace_path(), project)
                    except Blocked as error:
                        reviewable, unanchored = False, str(error)
                if available and reviewable:
                    ui.say('Assessment is approved. skip generates wireframes and the AI-DLC package without a second review. review runs the executor and an independent reviewer.')
                    choice = ui.ask('Next step (skip/review)', 'skip')
                    require(choice in {'skip', 'review', 'draft', 'verify'}, 'Choose skip or review')
                elif available:
                    ui.say('Review is not available: ' + unanchored.split(' No model call')[0] + ' Independent review needs '
                           'findings that cite a source file and line. Re-export the assessment with source anchors to review, '
                           'or continue with skip, which labels the findings AWS-assumed.')
                    choice = ui.ask('Next step (skip/pause)', 'skip')
                    require(choice in {'skip', 'pause'}, 'Choose skip or pause')
                    if choice == 'pause':
                        ui.say('Paused. Nothing was recorded and no model call was made.')
                        return
                elif reviewable:
                    ui.say('Skip is not available: ' + str(why) + ' review runs the executor and an independent reviewer.')
                    choice = 'review'
                else:
                    ui.say('Neither route can use this assessment. Skip: ' + str(why) + ' Review: '
                           + unanchored.split(' No model call')[0] + ' Nothing was recorded and no model call was made.')
                    return
            if not interrupted and choice in {'skip', 'draft'}:
                ui.say('Claude or Codex will generate design content. No executor/reviewer verification or approval is implied.')
                if not ensure_design_plan(ui, project):
                    return
                from reframe import name as safe_name
                retired = [Path(item).name for item in project.get('skip_history') or [] if item]
                default = 'guided-draft' if not retired else 'guided-draft-' + str(len(retired) + 1)
                name = safe_name(ui.ask('Draft name (reuse the same name to resume)', default))
                require(name not in retired, 'That draft was revised after design feedback. Choose a new draft name.')
                from reframe_workspace import preview_directory
                saved = preview_directory(workspace(), name) / 'preview-state.json'
                state = json.loads(saved.read_text()) if saved.exists() else {}
                recorded = project.get('verification_skip') or {}
                selected = (project.get('assessments') or {}).get(project.get('selected')) or {}
                if not state and recorded and recorded.get('assessment_sha256') == selected.get('sha256'):
                    # One skip decision covers every draft of this assessment; a revised draft does not re-attribute it.
                    ui.say('The recorded decision to skip verification for this assessment applies to this draft. '
                           'Its owner and reason are not asked again.')
                    state = recorded
                owner = state.get('owner') or ui.ask('Accountable owner for skipping verification')
                note = state.get('reason') or ui.ask('Reason for trusting AWS findings without independent verification')
                provider = state.get('provider') or ui.ask('Design provider (claude/codex)', project.get('providers', {}).get('wireframes', 'claude'))
                require(provider in {'claude', 'codex'}, 'Choose claude or codex')
                if not ui.yes('Generate or resume this AWS-assumed draft wireframe site and AI-DLC ZIP?'):
                    return
                if ui.invoke(['preview', '--skip-validation', '--by', owner, '--note', note,
                              '--provider', provider, '--name', name]) != 0:
                    ui.say('The draft was not written. /flow retries it. No approval was recorded.')
                    return
                say_review(ui, 'Review these draft files. They are not an approval.', draft_rows(name))
                outcome = design_review(ui, ui.project() or project, skip_route=True)
                if outcome != 'continue':
                    return
                continue
            if not interrupted:
                if not ui.yes('Run independent verification using the saved model-call budget?'):
                    return
                code = ui.invoke(['validate'])
                updated = ui.project() or {}
            recovery_used = interrupted and (updated.get('stage') == 'REWORK_LIMIT')
            for _budget in range(6):
                if updated.get('stage') == 'AWAITING_VALIDATION_APPROVAL':
                    break
                if updated.get('stage') == 'REWORK_LIMIT':
                    if recovery_used:
                        report = getattr(ui, 'last_report', None) or {}
                        if (updated.get('checkpoints') or {}).get('status') == 'READY_FOR_SYNTHESIS':
                            ui.say(str(report.get('reason') or 'Synthesis review paused.'))
                            ui.say(str(report.get('next_step') or 'reframe resume'))
                        else:
                            ui.say('Review paused on unit ' + str(report.get('unit') or 'unknown') + '.')
                            ui.say(str(report.get('next_step') or 'Authorize one targeted correction with reframe feedback --authorize-correction.'))
                        ui.say('No new assessment job is created.')
                        return
                    recovery_used = True
                    ui.say('Resuming the saved review. Completed calls stay recorded. No new assessment job is created.')
                    code = ui.invoke(['resume'])
                    updated = ui.project() or {}
                    continue
                state = updated.get('pipeline') or {}
                settings = updated.get('settings') or {}
                spent = state.get('calls') or 0
                cap = settings.get('max_model_calls') or 0
                # Spending the last call returns exhaustion. The next check restates the remaining plan.
                if state.get('reason') == 'Total model call budget exhausted' or (
                        code != 0 and cap and spent >= cap
                        and state.get('reason') != 'Insufficient call budget for remaining checkpoint plan'):
                    ui.say('The call cap was spent. Checking how many calls the remaining programs need.')
                    code = ui.invoke(['validate'])
                    updated = ui.project() or {}
                    continue
                if state.get('reason') == 'Model call would exceed the dollar cap':
                    updated = offer_dollar_budget(ui, updated)
                    if updated is None:
                        return
                    code = ui.invoke(['validate'])
                    updated = ui.project() or {}
                    continue
                # A short allowance returns a blocked status. Calls already spent still reach the question below.
                if code != 0 and state.get('correction_error'):
                    report = getattr(ui, 'last_report', None) or {}
                    for line in report.get('progress') or []:
                        ui.say(str(line))
                    ui.say(str(report.get('reason') or 'The saved correction was rejected before any edit was applied.'))
                    from reframe import correction_retries_exhausted
                    cap = settings.get('max_model_calls')
                    recoverable = (not correction_retries_exhausted(state) and (state.get('invalid_candidates') or 0) < 3
                                   and (cap is None or spent < cap))
                    if recoverable:
                        ui.say('Continuing the saved review. A retry and call budget remain.')
                        code = ui.invoke(['resume'])
                        updated = ui.project() or {}
                        continue
                    ui.say(str(report.get('next_step') or 'reframe resume'))
                    ui.say('Passed units stay sealed. No new assessment job is created.')
                    return
                if code != 0 and state.get('reason') != 'Insufficient call budget for remaining checkpoint plan':
                    return
                if updated.get('stage') == 'AWAITING_VALIDATION_APPROVAL':
                    break
                updated = offer_review_budget(ui, updated)
                if updated is None:
                    return
                code = 0 if updated.get('stage') == 'AWAITING_VALIDATION_APPROVAL' else 2
            else:
                return
            stage = updated['stage']
            project = updated
        if stage in {'AWAITING_ASSESSMENT_APPROVAL', 'AWAITING_VALIDATION_APPROVAL', 'AWAITING_SPECIFICATIONS_APPROVAL'}:
            phase = {'AWAITING_ASSESSMENT_APPROVAL':'assessment', 'AWAITING_VALIDATION_APPROVAL':'validation', 'AWAITING_SPECIFICATIONS_APPROVAL':'specifications'}[stage]
            if phase == 'assessment' and ui.invoke(['assessment-report']) != 0:
                return
            rows = {'assessment': assessment_rows, 'validation': validation_rows, 'specifications': specification_rows}[phase](project)
            say_review(ui, 'Review these ' + phase + ' files before you approve. Unresolved decisions remain enforced.', rows)
            if phase == 'specifications':
                outcome = design_review(ui, project, skip_route=False)
                if outcome != 'continue':
                    return
                continue
            if phase == 'validation' and not offer_context(ui, 'specification'):
                return
            if phase == 'validation' and not defer_open_questions(ui, project):
                return
            if not ui.yes('Have you reviewed the ' + phase + ' outputs and want to record approval now?'):
                if phase == 'validation' and ui.ask('Request a specification change now? (feedback/pause)', 'pause') == 'feedback':
                    note = ui.ask('Describe the change you need')
                    if ui.invoke(['feedback', '--scope', 'specification', '--by', reviewer(ui), '--note', note]) == 0:
                        continue
                    return
                ui.say('Paused for human review. The files listed above are unchanged. Return with /flow; no approval was recorded.')
                return
            if ui.invoke(['approve', phase] + simulated_flags()) != 0:
                return
            continue
        if stage == 'VALIDATION_APPROVED':
            if not ensure_design_plan(ui, project):
                return
            if ui.invoke(['review-site']) != 0:
                if not offer_wireframe_retry(ui):
                    return
            continue
        if stage in {'SPECIFICATIONS_APPROVED', 'DESIGN_APPROVED'}:
            if ui.invoke(['package']) != 0:
                ui.say('The package was not written. /flow retries it.')
                offer_withdraw_flagged_context(ui)
                return
            ui.say('The package is built and awaits your review. Building it did not accept it.')
            continue
        from reframe_acceptance import built_stage
        if built_stage(stage):
            outcome = package_review(ui, project)
            if outcome != 'continue':
                return
            continue
        if stage == 'PACKAGE_ACCEPTED':
            accepted = project.get('package_acceptance') or {}
            ui.say('The handoff ' + str(accepted.get('package_sha256')) + ' is accepted. Implementation readiness: '
                   + str(accepted.get('readiness')) + '. Blocked work stays blocked.')
            return
        if not approved:
            command = 'resume' if project.get('active_assessment') else 'assess'
            args = [command, '--wait']
            if command == 'assess':
                cap = ui.ask('Maximum expanded assessment evidence bytes (resource limit)', '250000000')
                require(cap.isdigit() and 0 < int(cap) <= 250000000, 'Enter a byte limit from 1 to 250000000')
                args += ['--max-assessment-bytes', cap]
            if ui.invoke(args) != 0:
                return
            if ui.project().get('stage') == 'AWAITING_ASSESSMENT_APPROVAL':
                continue
        ui.say('Work is saved. Use /flow to continue; inspect /status for any pending service task or blocker.')
        return
    ui.say('Paused after ' + str(FLOW_STEPS) + ' steps in one /flow, a safety bound. Everything is saved; /flow continues from here.')
