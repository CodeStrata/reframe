"""Acceptance harness: operate the real no-argument `reframe` console as a labeled simulated person (#194).

The harness starts `reframe.main([])` in a background process for one isolated run and lets an
acceptance agent answer one prompt at a time. Setup, routing, validation, rendering, packaging,
review gates, and acceptance are the candidate's real code. Only these boundaries are replaced:

- AWS: the AWS CLI wrapper, the Transform MCP client, sandbox provisioning checks, and the
  assessment download, which seals a fixed findings file. Every call is logged to aws-calls.jsonl.
- Models: provider replies come from the offline fixture model in tests/. Every call is logged to
  model-calls.jsonl. `fail-next-model` makes the next call fail before any reply.

Every record a person makes in this run is marked simulated (REFRAME_SIMULATED_ACTOR=1). It is a
test record, never genuine sign-off, and it never touches a saved workspace outside the run folder.

Commands (RUN is a new or existing run folder):
  start RUN          create the isolated run, check the candidate is clean, launch the console
  say RUN TEXT       answer the waiting prompt (`<default>` takes the default), print new output
  ctrl-c RUN         press Ctrl-C at the waiting prompt
  restart RUN        launch the no-argument console again in the same run, after it exited
  fail-next-model RUN  the next model call fails before a reply
  screen RUN         print the whole transcript
  status RUN         the waiting prompt, exit code, call counts, and candidate fingerprint
  stop RUN           end the console process
"""
import json
import os
import signal
import subprocess
import sys
import time
from hashlib import sha256
from pathlib import Path

CANDIDATE = Path(__file__).resolve().parents[1]
WAIT_SECONDS = 120


def _read(path, default=None):
    """Read JSON, or return the default when the file is missing."""
    path = Path(path)
    return json.loads(path.read_text()) if path.is_file() else default


def _write(path, value):
    """Write JSON through a temporary file."""
    path = Path(path)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True))
    temporary.replace(path)


def _log(path, entry):
    """Append one JSON line."""
    with Path(path).open('a') as handle:
        handle.write(json.dumps(entry, sort_keys=True) + '\n')


def fingerprint():
    """The candidate commit and tree. A dirty candidate is refused."""
    def git(*args):
        return subprocess.check_output(['git', '-C', str(CANDIDATE), *args], text=True).strip()
    dirty = git('status', '--porcelain')
    if dirty and os.environ.get('REFRAME_HARNESS_SMOKE') != '1':
        raise SystemExit('The candidate checkout has uncommitted changes. Acceptance needs a frozen candidate:\n' + dirty)
    return {'path': str(CANDIDATE), 'commit': git('rev-parse', 'HEAD'), 'tree': git('rev-parse', 'HEAD^{tree}'),
            'dirty': bool(dirty), 'note': 'A dirty candidate is a harness smoke run, never an acceptance report.' if dirty else ''}


def _source_fixture(root):
    """A small committed source repository: one rule, one copybook, one batch job."""
    source = root / 'source'
    source.mkdir()
    (source / 'rule.cbl').write_text('IF AMOUNT = ZERO\n MOVE 1 TO ERROR-FLAG\nEND-IF\n')
    (source / 'cpy').mkdir()
    (source / 'cpy' / 'AMOUNT.cpy').write_text('05 AMOUNT PIC 9(7)V99.\n')
    (source / 'jcl').mkdir()
    (source / 'jcl' / 'NIGHTLY.jcl').write_text("//NIGHTLY JOB (ACCT),'NIGHTLY'\n//STEP1 EXEC PGM=RULE\n")
    env = {**os.environ, 'GIT_AUTHOR_NAME': 'Acceptance Fixture', 'GIT_AUTHOR_EMAIL': 'fixture@example.test',
           'GIT_COMMITTER_NAME': 'Acceptance Fixture', 'GIT_COMMITTER_EMAIL': 'fixture@example.test'}
    for command in (['init', '-q'], ['add', '.'], ['commit', '-q', '-m', 'baseline'],
                    ['remote', 'add', 'origin', 'https://example.test/demo.git']):
        subprocess.check_call(['git', *command], cwd=source, env=env)
    return source


def _launch(run):
    """Start the console process for this run in the background."""
    meta = _read(run / 'meta.json')
    env = {**os.environ, 'REFRAME_CONFIG_HOME': str(run / 'config'), 'REFRAME_SIMULATED_ACTOR': '1',
           'COLUMNS': '110', 'NO_COLOR': '1', 'PYTHONPATH': os.pathsep.join([str(CANDIDATE / 'scripts'), str(CANDIDATE / 'tests')])}
    _write(run / 'state.json', {'seq': _read(run / 'state.json', {}).get('seq', 0), 'waiting': False, 'exited': None,
                                'launch': meta['launches'] + 1})
    meta['launches'] += 1
    _write(run / 'meta.json', meta)
    with (run / 'transcript.txt').open('a') as handle:
        handle.write('\n=== console launch ' + str(meta['launches']) + ' (reframe with no arguments) ===\n')
    log = (run / 'serve.log').open('a')
    process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), 'serve', str(run)], cwd=str(run),
                               env=env, stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True)
    (run / 'pid').write_text(str(process.pid))


def _wait(run, seq, cursor):
    """Wait for the next prompt or for the console to exit, then print what it showed."""
    deadline = time.time() + WAIT_SECONDS
    while time.time() < deadline:
        state = _read(run / 'state.json', {})
        if (state.get('waiting') and state.get('seq', 0) > seq) or state.get('exited') is not None:
            break
        time.sleep(0.1)
    text = (run / 'transcript.txt').read_text()
    print(text[cursor:].rstrip())
    state = _read(run / 'state.json', {})
    if state.get('exited') is not None:
        print('\n[console exited with code ' + str(state['exited']) + ']')
    elif not state.get('waiting'):
        print('\n[still working after ' + str(WAIT_SECONDS) + ' seconds; run status or say again]')
    (run / 'cursor').write_text(str(len(text)))


def start(run):
    """Create an isolated run folder and launch the console."""
    run = Path(run).resolve()
    if run.exists():
        raise SystemExit('Run folder already exists; use restart')
    run.mkdir(parents=True)
    for name in ('config', 'engineer', 'inbox'):
        (run / name).mkdir()
    source = _source_fixture(run)
    _write(run / 'meta.json', {'candidate': fingerprint(), 'created_at': time.time(), 'launches': 0,
                               'source_fixture': str(source), 'workspace_parent': str(run / 'engineer'),
                               'simulated': True,
                               'note': 'All human records in this run are simulated test records, not genuine sign-off.'})
    (run / 'transcript.txt').write_text('')
    print('Run ' + str(run) + '\nCandidate ' + json.dumps(_read(run / 'meta.json')['candidate']))
    print('Source fixture to type at the source prompt: ' + str(source))
    print('Parent directory for the new run: ' + str(run / 'engineer'))
    _launch(run)
    _wait(run, 0, 0)


def say(run, text):
    """Answer the waiting prompt."""
    run = Path(run).resolve()
    state = _read(run / 'state.json', {})
    if not state.get('waiting'):
        raise SystemExit('The console is not waiting for an answer. Use status or restart.')
    (run / 'inbox' / ('%05d.txt' % state['seq'])).write_text(text)
    _wait(run, state['seq'], int((run / 'cursor').read_text() or 0))


def ctrl_c(run):
    """Press Ctrl-C at the waiting prompt."""
    run = Path(run).resolve()
    state = _read(run / 'state.json', {})
    os.kill(int((run / 'pid').read_text()), signal.SIGINT)
    _wait(run, state.get('seq', 0), int((run / 'cursor').read_text() or 0))


def restart(run):
    """Launch the console again in the same run."""
    run = Path(run).resolve()
    if _read(run / 'state.json', {}).get('exited') is None and _alive(run):
        raise SystemExit('The console is still running. Use ctrl-c or stop first.')
    cursor = len((run / 'transcript.txt').read_text())
    _launch(run)
    _wait(run, _read(run / 'state.json', {}).get('seq', 0), cursor)


def _alive(run):
    """True while the console process exists."""
    try:
        os.kill(int((run / 'pid').read_text()), 0)
        return True
    except (OSError, ValueError):
        return False


def status(run):
    """Print the waiting prompt, exit state, call counts, and fingerprint."""
    run = Path(run).resolve()
    count = lambda name: len((run / name).read_text().splitlines()) if (run / name).is_file() else 0
    print(json.dumps({'state': _read(run / 'state.json', {}), 'alive': _alive(run), 'meta': _read(run / 'meta.json'),
                      'model_calls': count('model-calls.jsonl'), 'aws_calls_mocked': count('aws-calls.jsonl')}, indent=2))


def stop(run):
    """End the console process."""
    run = Path(run).resolve()
    if _alive(run):
        os.kill(int((run / 'pid').read_text()), signal.SIGTERM)
    print('stopped')


def serve(run):
    """Run reframe.main([]) with the AWS and model boundaries replaced. Runs in the background process."""
    run = Path(run).resolve()
    sys.path[:0] = [str(CANDIDATE / 'scripts'), str(CANDIDATE / 'tests')]
    from contextlib import ExitStack
    from unittest.mock import patch
    import kiro_workflow as kw
    import reframe
    import reframe_setup as setup
    import test_reframe_checkpoints as checkpoint_fixtures
    import test_release_acceptance as release

    transcript = (run / 'transcript.txt').open('a', buffering=1)

    class Screen:
        """The console's stdout, written to the transcript."""
        encoding = 'utf-8'

        def write(self, text):
            transcript.write(text)
            return len(text)

        def flush(self):
            transcript.flush()

        def isatty(self):
            return True

        def fileno(self):
            raise OSError('transcript')

    def answer_for(seq):
        while True:
            path = run / 'inbox' / ('%05d.txt' % seq)
            if path.is_file():
                return path.read_text()
            time.sleep(0.1)

    class Session:
        """Stands in for the terminal prompt. The acceptance agent types each answer."""
        def __init__(self, *args, **kwargs):
            pass

        def prompt(self, message, **kwargs):
            text = message if isinstance(message, str) else ''.join(
                part[1] if isinstance(part, tuple) else str(part) for part in message)
            default = kwargs.get('default') or ''
            state = _read(run / 'state.json', {})
            seq = state.get('seq', 0) + 1
            transcript.write('\n> ' + text.strip() + (' [default: ' + default + ']' if default else '') + '\n')
            _write(run / 'state.json', {**state, 'seq': seq, 'waiting': True, 'prompt': text.strip(), 'default': default})
            try:
                answer = answer_for(seq)
            finally:
                _write(run / 'state.json', {**_read(run / 'state.json', {}), 'waiting': False})
            transcript.write('< ' + answer + '\n')
            return default if answer == '<default>' else answer

    role = 'arn:aws:iam::111111111111:role/fixture-role'
    user = '11111111-1111-1111-1111-111111111111'

    class FakeTransform:
        """The Transform MCP client. Answers the setup and status calls the console makes."""
        def __init__(self, config=None, directory=None):
            pass

        def tools(self):
            _log(run / 'aws-calls.jsonl', {'transform': 'tools', 'at': time.time()})
            return []

        def calls(self, requests):
            results = []
            for name, _payload in requests:
                _log(run / 'aws-calls.jsonl', {'transform': name, 'at': time.time()})
                results.append({
                    'get_status': {'connection': {'configured': True}},
                    'create_workspace': {'workspaceId': 'workspace'},
                    'create_connector': {'connectorId': 'connector'},
                    'accept_connector': {'status': 'ACTIVE'},
                    'get_resource': {'accountConnection': {'awsAccountConnection': {
                        'status': 'ACTIVE', 'accountId': '111111111111', 'roleArn': role}}},
                    'list_resources': {'users': [{'email': 'acceptance', 'userId': user}]},
                }.get(name, {}))
            return results

    def aws(project, *args):
        joined = ' '.join(args)
        _log(run / 'aws-calls.jsonl', {'aws': joined[:200], 'at': time.time()})
        if 'get-caller-identity' in joined:
            return {'Account': '111111111111', 'Arn': 'arn:aws:sts::111111111111:assumed-role/fixture-role/acceptance'}
        if 'get-public-access-block' in joined:
            return {'PublicAccessBlockConfiguration': {'BlockPublicAcls': True, 'IgnorePublicAcls': True,
                                                       'BlockPublicPolicy': True, 'RestrictPublicBuckets': True}}
        return {}

    def seal(record, directory, client):
        folder = directory / 'assessment'
        folder.mkdir(exist_ok=True)
        target = folder / 'rules.json'
        target.write_text(json.dumps({'rules': ['reject zero amount']}))
        record['assessment_index'] = [{'path': 'rules.json', 'bytes': target.stat().st_size,
                                       'sha256': sha256(target.read_bytes()).hexdigest()}]
        record['assessment_ready'] = True
        _log(run / 'aws-calls.jsonl', {'transform': 'assessment download (fixture findings)', 'at': time.time()})

    helper = checkpoint_fixtures.CheckpointTests()
    helper.seen = []
    fixture_model = release.review_model(helper, {'calls': [], 'pause': False})

    def model(provider, record, directory, role_name, message):
        flag = run / 'fail-next-model'
        entry = {'provider': provider, 'role': role_name, 'request_bytes': len(message.encode()), 'at': time.time()}
        if flag.is_file():
            flag.unlink()
            _log(run / 'model-calls.jsonl', {**entry, 'outcome': 'injected failure before reply'})
            raise kw.RuntimeUnavailable('Provider unavailable (failure injected by the acceptance harness)')
        reply = fixture_model(provider, record, directory, role_name, message)
        _log(run / 'model-calls.jsonl', {**entry, 'outcome': 'fixture reply'})
        return reply

    real_pipeline, real_review, real_semantic = reframe.pipeline, reframe.review_site, reframe.semantic_compare
    code = None
    try:
        with ExitStack() as stack:
            stack.enter_context(patch.object(sys, 'stdout', Screen()))
            stack.enter_context(patch.object(sys.stdin, 'isatty', return_value=True))
            stack.enter_context(patch('reframe_terminal.PromptSession', Session))
            stack.enter_context(patch.object(reframe, 'model_call', model))
            stack.enter_context(patch.object(reframe, 'pipeline', lambda w, p, a, runtime=None: real_pipeline(w, p, a, model)))
            stack.enter_context(patch.object(reframe, 'review_site', lambda w, p, a, runtime=None: real_review(w, p, a, model)))
            stack.enter_context(patch.object(reframe, 'semantic_compare', lambda w, p, a, runtime=None: real_semantic(w, p, a, model)))
            stack.enter_context(patch.object(reframe, 'aws', aws))
            stack.enter_context(patch.object(setup, 'ensure_aws_login', lambda project: None))
            stack.enter_context(patch.object(setup, 'checks', lambda project, work=None: None))
            stack.enter_context(patch.object(setup, 'sandbox_outputs', lambda *a, **k: ('fixture-bucket', 'reframe/', 'fixture-role', role)))
            stack.enter_context(patch.object(setup, 'confirm_production_deny', lambda *a, **k: None))
            stack.enter_context(patch.object(setup, 'connect_transform', lambda *a, **k: FakeTransform()))
            stack.enter_context(patch.object(kw, 'Transform', FakeTransform))
            stack.enter_context(patch.object(kw, 'assessment_step', seal))
            stack.enter_context(patch('reframe_models.claude_uses_api_key', return_value=False))
            code = reframe.main([])
    except BaseException as error:  # the transcript records how the console ended
        transcript.write('\n[console ended: ' + type(error).__name__ + ': ' + str(error)[:300] + ']\n')
        code = 'exception'
    finally:
        transcript.flush()
        _write(run / 'state.json', {**_read(run / 'state.json', {}), 'waiting': False, 'exited': code})


def main(argv):
    """Dispatch one harness command."""
    if len(argv) < 2:
        raise SystemExit(__doc__)
    command, run = argv[0], argv[1]
    if command == 'say':
        return say(run, ' '.join(argv[2:]))
    if command == 'fail-next-model':
        (Path(run).resolve() / 'fail-next-model').write_text('1')
        return print('The next model call will fail before a reply.')
    actions = {'start': start, 'ctrl-c': ctrl_c, 'restart': restart, 'screen': lambda r: print((Path(r) / 'transcript.txt').read_text()),
               'status': status, 'stop': stop, 'serve': serve}
    if command not in actions:
        raise SystemExit(__doc__)
    return actions[command](run)


if __name__ == '__main__':
    main(sys.argv[1:])
