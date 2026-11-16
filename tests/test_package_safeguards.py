"""Credential and customer-identifier checks on every package route (SA-2). L1.

The review-route package is covered by test_reframe.PreparationTests.test_package_refuses_secret_and_writes_no_zip.
"""
import json
import unittest
from pathlib import Path

import test_reframe_optional as optional_fixtures
import test_reframe_preview as preview_fixtures
import reframe as app
import reframe_optional as optional
import reframe_preview as preview
from pilot import Blocked

FAKES = (('AKIAIOSFODNN7EXAMPLE', 'cloud access key'), ('123-45-6789', 'customer identifier'))


class SkipDraftSafeguardTests(unittest.TestCase):
    args, assess, approve = preview_fixtures.PreviewTests.args, preview_fixtures.PreviewTests.assess, preview_fixtures.PreviewTests.approve
    spec, screens, runtime = preview_fixtures.PreviewTests.spec, preview_fixtures.PreviewTests.screens, preview_fixtures.PreviewTests.runtime
    setUp = preview_fixtures.PreviewTests.setUp

    def test_a_fake_secret_in_the_draft_is_refused_and_no_zip_is_written(self):
        for value, kind in FAKES:
            def runtime(provider, run, directory, role, message, value=value):
                reply = self.runtime(provider, run, directory, role, message)
                reply['sections']['ui']['implementation_prompt'] += '\n' + value + '\n'
                return reply

            name = 'secret-' + kind.replace(' ', '-')
            arguments = self.args('preview', '--skip-validation', '--by', 'Fixture owner', '--note', 'Preview AWS findings',
                                  '--name', name)
            with self.assertRaises(Blocked) as raised:
                preview.run(self.work, self.project, arguments, app, runtime)
            message = str(raised.exception)
            self.assertIn('ui-prompt.md', message)
            self.assertIn(kind, message)
            self.assertNotIn(value, message)
            self.assertFalse(list(self.work.glob('**/' + name + '/ai-dlc-draft.zip')))
            self.assertFalse(list(self.work.glob('packages/**/*.zip')))


class ModeExportSafeguardTests(unittest.TestCase):
    setUp = optional_fixtures.OptionalModeTests.setUp

    def test_a_fake_secret_in_a_mode_export_is_refused_and_no_zip_is_written(self):
        for index, (value, kind) in enumerate(FAKES):
            screens = json.loads(json.dumps(optional_fixtures.SCREENS))
            screens['screens'][0]['purpose'] = 'Check the amount for ' + value + '.'
            (self.site / 'screens.json').write_text(json.dumps(screens))
            version = 'v' + str(index + 1)
            optional.design_export(self.root, self.project, version, 'functional-parity', 'unspecified')
            with self.assertRaises(Blocked) as raised:
                optional.package_export(self.root, self.project, version, 'functional-parity')
            message = str(raised.exception)
            self.assertIn(kind, message)
            self.assertNotIn(value, message)
            self.assertFalse((Path(self.root) / 'packages' / version / 'functional-parity' / 'ai-dlc-package.zip').exists())

    def test_a_clean_mode_export_still_packages(self):
        optional.design_export(self.root, self.project, 'v1', 'functional-parity', 'unspecified')
        result = optional.package_export(self.root, self.project, 'v1', 'functional-parity')
        self.assertTrue((Path(self.root) / result['archive']).is_file())


if __name__ == '__main__':
    unittest.main()
