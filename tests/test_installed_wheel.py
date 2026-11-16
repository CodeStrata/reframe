"""Installed wheel outside the source checkout (AC-34), plus the packaged-license fallback.

InstalledWheelTests is opt-in (REFRAME_WHEEL_CHECK=1). It copies the tracked files
to a temporary directory, builds a wheel there, installs it into a disposable
virtual environment outside the checkout, and never touches a shared installation.
It needs uv (on PATH or named by REFRAME_UV) or pip, and access to a package index for the build backend and the
runtime dependencies. It never starts an AWS or model provider.

PackageFallbackTests always runs: it proves framework_notice() reads the packaged
LICENSE when no checkout LICENSE sits beside the module.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

SOURCE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOURCE / 'scripts'))
import reframe_handoff as handoff

# Every checkout-relative file the CLI reads at run time, by the module whose
# FRAMEWORK (or __file__) anchors the lookup. Keep in step with grep for
# "FRAMEWORK /" and "Path(__file__)" in scripts/.
RESOURCES = {
    'reframe': ['prompts/pipeline/executor.md', 'prompts/pipeline/reviewer.md',
                'prompts/pipeline/wireframes.md', 'prompts/pipeline/comparison.md',
                'prompts/pipeline/transform-preview.md',
                'prompts/checkpoints/executor.md', 'prompts/checkpoints/reviewer.md',
                'docs/engineer-setup.md', 'docs/cli-guide.md', 'docs/assessment-comparison.md',
                'infrastructure/main.tf', 'infrastructure/deny-check.sh'],
    'kiro_workflow': ['prompts/automated/executor.md', 'prompts/automated/reviewer.md'],
    'reframe_contracts': ['contracts/task-contract.yaml', 'contracts/review-record.yaml',
                          'contracts/approval-record.yaml'],
}

PROBE = textwrap.dedent('''
    import importlib, json, sys, tomllib
    from pathlib import Path
    source, prefix = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    resources = json.loads(sys.argv[3])
    report = {'modules': {}, 'resources': {}, 'calls': {}, 'framework_pin': None,
              'unittest_loaded_by_cli': None}

    def outside(path):
        path = Path(path).resolve()
        return path.is_relative_to(prefix) and not path.is_relative_to(source)

    def attempt(label, function):
        try:
            report['calls'][label] = {'ok': True, 'detail': str(function())[:120]}
        except BaseException as error:
            report['calls'][label] = {'ok': False, 'detail': type(error).__name__ + ': ' + str(error)[:300]}

    modules = tomllib.loads((source / 'pyproject.toml').read_text())['tool']['setuptools']['py-modules']
    for name in modules:
        try:
            module = importlib.import_module(name)
            report['modules'][name] = {'ok': outside(module.__file__), 'detail': str(Path(module.__file__).resolve())}
        except BaseException as error:
            report['modules'][name] = {'ok': False, 'detail': type(error).__name__ + ': ' + str(error)}
    report['unittest_loaded_by_cli'] = 'unittest' in sys.modules

    for owner, relatives in resources.items():
        try:
            framework = Path(importlib.import_module(owner).FRAMEWORK)
        except BaseException as error:
            for relative in relatives:
                report['resources'][relative] = {'ok': False, 'detail': repr(error)}
            continue
        for relative in relatives:
            located = framework / relative
            if not located.is_file():
                report['resources'][relative] = {'ok': False, 'detail': 'missing at ' + str(located)}
            elif not outside(located):
                report['resources'][relative] = {'ok': False, 'detail': 'resolved inside the checkout: ' + str(located)}
            elif located.read_bytes() != (source / relative).read_bytes():
                report['resources'][relative] = {'ok': False, 'detail': 'differs from the checkout copy: ' + str(located)}
            else:
                report['resources'][relative] = {'ok': True, 'detail': str(located)}

    import reframe, reframe_models, reframe_contracts, reframe_handoff
    attempt('reframe.wireframe_prompt_hash', reframe.wireframe_prompt_hash)
    attempt('reframe_models.preparation_protocol_hash', reframe_models.preparation_protocol_hash)
    for kind in ('task', 'review', 'approval'):
        attempt('reframe_contracts.requirements(%s)' % kind, lambda kind=kind: reframe_contracts.requirements(kind))
    attempt('reframe_handoff.framework_notice', reframe_handoff.framework_notice)
    notice_path = Path(reframe_handoff.__file__).resolve().parents[1] / 'LICENSE'
    report['calls']['notice uses packaged LICENSE'] = {
        'ok': not notice_path.is_file(), 'detail': 'checkout-style LICENSE beside module: ' + str(notice_path.is_file())}
    try:
        commit = reframe.git(reframe.FRAMEWORK, 'rev-parse', 'HEAD')
        top = reframe.git(reframe.FRAMEWORK, 'rev-parse', '--show-toplevel')
        report['framework_pin'] = {'ok': outside(top), 'detail': 'commit %s from %s' % (commit, top)}
    except BaseException as error:
        report['framework_pin'] = {'ok': False, 'detail': type(error).__name__ + ': ' + str(error)[:300]}
    print(json.dumps(report))
''')


def run(command, **options):
    """Run one local build or install step with a readable failure."""
    options.setdefault('timeout', 900)
    completed = subprocess.run([str(part) for part in command], capture_output=True, text=True, check=False, **options)
    if completed.returncode:
        raise AssertionError('%s failed (%s)\n%s\n%s' % (
            ' '.join(map(str, command)), completed.returncode, completed.stdout[-4000:], completed.stderr[-4000:]))
    return completed


@unittest.skipUnless(os.environ.get('REFRAME_WHEEL_CHECK') == '1',
                     'Set REFRAME_WHEEL_CHECK=1 to build the wheel and check it from a disposable '
                     'virtual environment outside the checkout (slow; needs uv or pip and a package index)')
class InstalledWheelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(tempfile.mkdtemp(prefix='reframe-wheel-check-')).resolve()
        if cls.root.is_relative_to(SOURCE):
            raise AssertionError('Temporary directory is inside the checkout: ' + str(cls.root))
        try:
            cls._prepare()
        except BaseException:
            shutil.rmtree(cls.root, ignore_errors=True)
            raise

    @classmethod
    def _prepare(cls):
        root = cls.root
        cls.env = {key: value for key, value in os.environ.items()
                   if key not in {'PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV', 'PYTHONSTARTUP'}}
        # Git must not find an enclosing repository above the temporary directory.
        cls.env['GIT_CEILING_DIRECTORIES'] = str(root)
        # Build from a copy of the tracked files so the checkout stays clean.
        build = root / 'src'
        listed = run(['git', '-C', SOURCE, 'ls-files', '-z'], env=cls.env).stdout.split('\0')
        for relative in filter(None, listed):
            origin = SOURCE / relative
            if origin.is_file():
                target = build / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(origin, target)
        dist, cls.venv, cls.work = root / 'dist', root / 'venv', root / 'work'
        cls.work.mkdir()
        # REFRAME_UV names uv when an isolated PATH leaves it out; otherwise pip is used.
        uv = os.environ.get('REFRAME_UV') or shutil.which('uv')
        if uv:
            run([uv, 'build', '--wheel', '--out-dir', dist, build], cwd=cls.work, env=cls.env)
        else:
            run([sys.executable, '-m', 'pip', '--version'], cwd=cls.work, env=cls.env)
            run([sys.executable, '-m', 'pip', 'wheel', build, '--no-deps', '-w', dist], cwd=cls.work, env=cls.env)
        wheels = sorted(dist.glob('reframe-*.whl'))
        if len(wheels) != 1:
            raise AssertionError('Expected one wheel, found %s' % wheels)
        cls.wheel = wheels[0]
        if uv:
            run([uv, 'venv', '--python', sys.executable, cls.venv], cwd=cls.work, env=cls.env)
            cls.python = cls.venv / 'bin' / 'python'
            run([uv, 'pip', 'install', '--python', cls.python, cls.wheel], cwd=cls.work, env=cls.env)
        else:
            run([sys.executable, '-m', 'venv', cls.venv], cwd=cls.work, env=cls.env)
            cls.python = cls.venv / 'bin' / 'python'
            run([cls.python, '-m', 'pip', 'install', cls.wheel], cwd=cls.work, env=cls.env)
        shutil.rmtree(build)
        purelib = run([cls.python, '-c', 'import sysconfig; print(sysconfig.get_paths()["purelib"])'],
                      cwd=cls.work, env=cls.env).stdout.strip()
        cls.purelib = Path(purelib).resolve()
        completed = subprocess.run(
            [str(cls.python), '-c', PROBE, str(SOURCE), str(cls.venv.resolve()), json.dumps(RESOURCES)],
            cwd=cls.work, env=cls.env, capture_output=True, text=True, timeout=300, check=False)
        if completed.returncode:
            raise AssertionError('Installed-package probe crashed\n' + completed.stdout + completed.stderr)
        cls.report = json.loads(completed.stdout.strip().splitlines()[-1])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.root, ignore_errors=True)

    def test_wheel_contains_every_module_and_the_license(self):
        import tomllib
        import zipfile
        modules = tomllib.loads((SOURCE / 'pyproject.toml').read_text())['tool']['setuptools']['py-modules']
        with zipfile.ZipFile(self.wheel) as archive:
            names = set(archive.namelist())
        self.assertEqual([m for m in modules if m + '.py' not in names], [])
        self.assertTrue(any(name.endswith('/LICENSE') for name in names), sorted(names))

    def test_installed_command_runs_outside_the_checkout(self):
        command = self.venv / 'bin' / 'reframe'
        self.assertTrue(command.is_file())
        completed = subprocess.run([str(command), '--help'], cwd=self.work, env=self.env,
                                   capture_output=True, text=True, timeout=120, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn('usage', completed.stdout.lower())

    def test_every_declared_module_imports_from_the_installed_package(self):
        for name, result in self.report['modules'].items():
            with self.subTest(module=name):
                self.assertTrue(result['ok'], result['detail'])
                self.assertTrue(Path(result['detail']).is_relative_to(self.purelib), result['detail'])

    def test_cli_import_does_not_load_unittest(self):
        # pilot imports the unpackaged reframe_offline guard whenever unittest is loaded.
        self.assertFalse(self.report['unittest_loaded_by_cli'])

    def test_installed_modules_import_under_a_unittest_runner(self):
        # pilot imports reframe_offline whenever unittest is loaded; the wheel must provide it.
        completed = subprocess.run([str(self.python), '-c', 'import unittest, pilot, reframe; print("imported")'],
                                   cwd=self.work, env=self.env, capture_output=True, text=True, timeout=120, check=False)
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr[-2000:])

    def test_prompts_contracts_and_guides_resolve_from_the_installed_package(self):
        for relative, result in sorted(self.report['resources'].items()):
            with self.subTest(resource=relative):
                self.assertTrue(result['ok'], result['detail'])

    def test_resource_reading_functions_work_from_the_installed_package(self):
        for label, result in sorted(self.report['calls'].items()):
            with self.subTest(call=label):
                self.assertTrue(result['ok'], result['detail'])

    def test_framework_pin_does_not_need_a_source_checkout(self):
        result = self.report['framework_pin']
        self.assertTrue(result['ok'], result['detail'])

    def test_installed_license_check_passes_against_the_wheel(self):
        copy = self.work / 'test_installed_license.py'
        shutil.copy2(SOURCE / 'tests' / 'test_installed_license.py', copy)
        env = dict(self.env, REFRAME_INSTALLED_LICENSE='1', REFRAME_LICENSE_SOURCE=str(SOURCE))
        completed = subprocess.run([str(self.python), '-m', 'unittest', '-v', 'test_installed_license'],
                                   cwd=self.work, env=env, capture_output=True, text=True, timeout=300, check=False)
        output = completed.stdout + completed.stderr
        self.assertEqual(completed.returncode, 0, output)
        self.assertIn('test_installed_export_uses_packaged_mit_text', output)
        self.assertNotIn('skipped', output)


class PackageFallbackTests(unittest.TestCase):
    """framework_notice() uses the packaged LICENSE when no checkout LICENSE is beside the module."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix='reframe-license-fallback-'))
        self.addCleanup(shutil.rmtree, self.root, True)
        self.site = self.root / 'lib' / 'site-packages'
        self.site.mkdir(parents=True)
        self.packaged = self.root / 'reframe-0.0.0.dist-info' / 'licenses' / 'LICENSE'
        self.packaged.parent.mkdir(parents=True)
        self.packaged.write_text('MIT License\n\nPackaged fixture text\n')

    def distribution(self, files):
        class Entry:
            def __init__(self, path):
                self.name, self._path = Path(path).name, Path(path)

            def locate(self):
                return self._path

        fake = mock.Mock()
        fake.files = [Entry(path) for path in files]
        return mock.patch('importlib.metadata.distribution', return_value=fake)

    def test_checkout_license_is_used_when_present(self):
        notice = handoff.framework_notice()
        self.assertTrue(notice.endswith((SOURCE / 'LICENSE').read_text()))

    def test_packaged_license_is_used_without_a_checkout(self):
        with mock.patch.object(handoff, '__file__', str(self.site / 'reframe_handoff.py')), \
                self.distribution([self.site / 'reframe_handoff.py', self.packaged]) as distribution:
            notice = handoff.framework_notice()
        distribution.assert_called_once_with('reframe')
        self.assertTrue(notice.endswith('MIT License\n\nPackaged fixture text\n'))
        self.assertIn('does not claim ownership of the source code, AWS findings', notice)
        self.assertNotIn((SOURCE / 'LICENSE').read_text(), notice)

    def test_checkout_license_beside_the_module_wins_over_the_package(self):
        (self.site.parent / 'LICENSE').write_text('Checkout text\n')
        with mock.patch.object(handoff, '__file__', str(self.site / 'reframe_handoff.py')), \
                self.distribution([self.packaged]) as distribution:
            notice = handoff.framework_notice()
        distribution.assert_not_called()
        self.assertTrue(notice.endswith('Checkout text\n'))


if __name__ == '__main__':
    unittest.main()
