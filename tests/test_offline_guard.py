"""The offline guard fails closed on provider processes and network access; local Git still works.

Each refused command runs with PATH set to a directory of fake provider programs
that record a marker if they ever start. A guard regression therefore cannot
reach a real provider, and the marker proves no process was started.
"""
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import pilot  # noqa: F401  Importing pilot under unittest installs the guard, as in the suite.
import reframe_offline
import reframe_models
from kiro_workflow import RuntimeUnavailable

PROVIDERS = ('aws', 'claude', 'codex', 'tofu', 'terraform', 'uvx', 'kiro', 'kiro-cli')
API_KEY_NAMES = ('ANTHROPIC_API_KEY', 'CLAUDE_API_KEY', 'ANTHROPIC_AUTH_TOKEN', 'OPENAI_API_KEY')


class OfflineGuardTests(unittest.TestCase):
    def setUp(self):
        reframe_offline.install()
        self.root = Path(tempfile.mkdtemp(prefix='reframe-offline-guard-'))
        self.addCleanup(shutil.rmtree, self.root, True)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.marker = self.root / 'started.log'
        for name in PROVIDERS + ('curl',):
            program = self.bin / name
            program.write_text('#!/bin/sh\necho "%s $*" >> "%s"\nexit 97\n' % (name, self.marker))
            program.chmod(0o700)

    def fake_path(self):
        """Only fake programs resolve; nothing real can start even if the guard regresses."""
        return mock.patch.dict(os.environ, {'PATH': str(self.bin)})

    def assertNothingStarted(self):
        self.assertFalse(self.marker.exists(), self.marker.read_text() if self.marker.exists() else '')

    def test_guard_replaces_process_and_socket_entry_points(self):
        self.assertTrue(reframe_offline.install.active)
        self.assertEqual(subprocess.Popen.__name__, 'GuardedPopen')
        for replaced in (subprocess.run, socket.create_connection, socket.socket.connect, socket.socket.connect_ex):
            with self.subTest(entry=replaced.__name__):
                self.assertEqual(replaced.__module__, 'reframe_offline')

    def test_provider_programs_are_refused_through_run_and_popen(self):
        with self.fake_path():
            for name in PROVIDERS:
                for argv in ([name, '--version'], [str(self.bin / name), '--version']):
                    with self.subTest(entry='run', argv=argv):
                        with self.assertRaisesRegex(AssertionError, 'unmocked provider process: ' + name):
                            subprocess.run(argv, capture_output=True)
                    with self.subTest(entry='Popen', argv=argv):
                        with self.assertRaisesRegex(AssertionError, 'unmocked provider process: ' + name):
                            subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for helper in (subprocess.call, subprocess.check_call, subprocess.check_output):
                with self.subTest(entry=helper.__name__):
                    with self.assertRaisesRegex(AssertionError, 'unmocked provider process: claude'):
                        helper(['claude', '-p', 'hello'])
        self.assertNothingStarted()

    def test_named_specific_commands_fail_closed(self):
        with self.fake_path():
            cases = {
                'claude': ['claude', '-p', '--output-format', 'json'],
                'aws': ['aws', 'sts', 'get-caller-identity'],
                'codex': ['codex', 'exec', '-'],
                'tofu': ['tofu', 'apply', '-auto-approve'],
            }
            for name, argv in cases.items():
                with self.subTest(name=name):
                    with self.assertRaisesRegex(AssertionError, 'unmocked provider process: ' + name):
                        subprocess.run(argv, capture_output=True, text=True)
        self.assertNothingStarted()

    def test_provider_host_on_any_command_line_is_refused(self):
        with self.fake_path():
            for host in reframe_offline.BLOCKED_HOSTS:
                with self.subTest(host=host):
                    with self.assertRaisesRegex(AssertionError, 'unmocked provider network request: ' + host):
                        subprocess.run(['curl', '--silent', 'https://service.' + host + '/'], capture_output=True)
            with self.assertRaisesRegex(AssertionError, 'amazonaws.com'):
                subprocess.run(['curl', 'https://bedrock-runtime.us-east-1.amazonaws.com/model'], capture_output=True)
        self.assertNothingStarted()

    def test_shell_and_wrapper_commands_cannot_hide_a_provider(self):
        with self.fake_path():
            cases = [
                ('aws sts get-caller-identity', {'shell': True}),
                ('cd /tmp && codex exec -', {'shell': True}),
                (['/bin/sh', '-c', 'echo start; claude -p hello'], {}),
                (['/bin/sh', '-ec', 'tofu plan'], {}),
                ('echo "$(aws sts get-caller-identity)"', {'shell': True}),
                (['env', 'AWS_REGION=us-east-1', 'aws', 's3', 'ls'], {}),
                (['nohup', str(self.bin / 'terraform'), 'apply'], {}),
            ]
            for command, options in cases:
                with self.subTest(command=command):
                    with self.assertRaisesRegex(AssertionError, 'unmocked provider process'):
                        subprocess.run(command, capture_output=True, **options)
        self.assertNothingStarted()

    def test_network_connections_are_refused(self):
        with self.assertRaisesRegex(AssertionError, 'unmocked network request'):
            socket.create_connection(('example.com', 443), timeout=1)
        with self.assertRaisesRegex(AssertionError, 'unmocked network request'):
            socket.create_connection(('93.184.215.14', 443), timeout=1)
        for family, address in ((socket.AF_INET, ('example.com', 443)), (socket.AF_INET, ('93.184.215.14', 80))):
            with self.subTest(address=address):
                connection = socket.socket(family, socket.SOCK_STREAM)
                self.addCleanup(connection.close)
                with self.assertRaisesRegex(AssertionError, 'unmocked network request'):
                    connection.connect(address)
                with self.assertRaisesRegex(AssertionError, 'unmocked network request'):
                    connection.connect_ex(address)
        default = socket.socket()
        self.addCleanup(default.close)
        with self.assertRaisesRegex(AssertionError, 'unmocked network request'):
            default.connect(('example.com', 443))

    def test_local_git_still_works(self):
        version = subprocess.run(['git', '--version'], capture_output=True, text=True, check=False)
        self.assertEqual(version.returncode, 0, version.stderr)
        self.assertTrue(version.stdout.startswith('git version'), version.stdout)
        repository = self.root / 'repository'
        repository.mkdir()
        identity = ['-c', 'user.name=Offline Test', '-c', 'user.email=offline@example.invalid']
        subprocess.run(['git', 'init', '-q', str(repository)], check=True)
        (repository / 'note.txt').write_text('local only\n')
        subprocess.run(['git', '-C', str(repository), 'add', 'note.txt'], check=True)
        subprocess.run(['git', '-C', str(repository), *identity, 'commit', '-q', '-m', 'local'], check=True)
        head = subprocess.Popen(['git', '-C', str(repository), 'rev-parse', 'HEAD'], stdout=subprocess.PIPE, text=True)
        output, _ = head.communicate(timeout=30)
        self.assertEqual(head.returncode, 0)
        self.assertRegex(output.strip(), r'^[0-9a-f]{40}$')
        status = subprocess.check_output(['git', '-C', str(repository), 'status', '--porcelain'], text=True)
        self.assertEqual(status, '')


class ProviderDispatchTests(unittest.TestCase):
    """reframe_models.call stops before any provider process starts."""

    def setUp(self):
        reframe_offline.install()
        self.root = Path(tempfile.mkdtemp(prefix='reframe-offline-dispatch-'))
        self.addCleanup(shutil.rmtree, self.root, True)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.marker = self.root / 'started.log'
        for name in ('claude', 'codex'):
            program = self.bin / name
            program.write_text('#!/bin/sh\necho "%s $*" >> "%s"\nexit 97\n' % (name, self.marker))
            program.chmod(0o700)
        self.directory = self.root / 'run'
        self.directory.mkdir()
        self.run_record = {'model_calls': 0, 'settings': {'executor_model': None, 'call_timeout_seconds': 5}}

    def environment(self, path, **extra):
        values = {'PATH': str(path), **extra}
        patcher = mock.patch.dict(os.environ, values)
        patcher.start()
        self.addCleanup(patcher.stop)
        for name in API_KEY_NAMES:
            if name not in extra:
                os.environ.pop(name, None)

    def assertNoProviderStarted(self):
        self.assertFalse(self.marker.exists(), self.marker.read_text() if self.marker.exists() else '')
        self.assertEqual(sorted(path.name for path in self.directory.glob('provider-[0-9]*.json')), [])

    def test_claude_login_check_is_refused_by_the_guard(self):
        self.environment(self.bin)
        with self.assertRaisesRegex(AssertionError, 'unmocked provider process: claude'):
            reframe_models.call('claude', self.run_record, self.directory, 'executor', '{"task":"offline"}')
        self.assertNoProviderStarted()
        self.assertFalse((self.directory / 'provider-request-0.json').exists())

    def test_claude_dispatch_with_api_key_is_refused_before_the_process_starts(self):
        self.environment(self.bin, ANTHROPIC_API_KEY='offline-placeholder-not-a-key')
        with self.assertRaisesRegex(AssertionError, 'unmocked provider process: claude'):
            reframe_models.call('claude', self.run_record, self.directory, 'executor', '{"task":"offline"}')
        self.assertNoProviderStarted()

    def test_codex_dispatch_is_refused_before_the_process_starts(self):
        self.environment(self.bin)
        with self.assertRaisesRegex(AssertionError, 'unmocked provider process: codex'):
            reframe_models.call('codex', self.run_record, self.directory, 'executor', '{"task":"offline"}')
        self.assertNoProviderStarted()

    def test_missing_provider_is_a_pre_dispatch_runtime_stop(self):
        empty = self.root / 'empty-bin'
        empty.mkdir()
        self.environment(empty)
        for provider in ('claude', 'codex'):
            with self.subTest(provider=provider):
                with self.assertRaises(RuntimeUnavailable) as raised:
                    reframe_models.call(provider, self.run_record, self.directory, 'executor', '{}')
                self.assertTrue(raised.exception.pre_dispatch)
        self.assertNoProviderStarted()
        self.assertFalse((self.directory / 'runtime').exists())


if __name__ == '__main__':
    unittest.main()
