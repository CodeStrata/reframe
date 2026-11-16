"""Recursive local link and fragment validation for reports, sites and packages."""
import json
import shutil
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / 'scripts'))
import test_reframe as fixtures
import test_reframe_optional
import test_reframe_preview
import reframe as app
import reframe_artifacts as artifacts
import reframe_links as links
import reframe_optional as optional
import reframe_preview as preview
from pilot import Blocked


def page(body, title='Fixture'):
    """Return a minimal HTML page around a body."""
    return '<!doctype html><html><head><title>' + title + '</title></head><body>' + body + '</body></html>'


class LinkTreeTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.base = Path(temp.name)
        self.root = self.base / 'site'
        self.root.mkdir()

    def write(self, name, body):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page(body))
        return path

    def zip_of(self, members):
        archive = self.base / 'package.zip'
        with zipfile.ZipFile(archive, 'w') as bundle:
            for name, data in members.items():
                bundle.writestr(name, data)
        return archive

    def test_valid_tree_passes_recursively(self):
        self.write('index.html', '<a href="#top">Top</a><h1 id="top">Index</h1>'
                                 '<a href="docs/guide.html#step-2">Guide</a><img src="img/logo.svg">'
                                 '<a href="data.json">Data</a><a href="docs/">Docs</a><a href="#">Self</a>')
        self.write('docs/guide.html', '<a name="step-2"></a><a href="../index.html#top">Back</a>'
                                      '<a href="guide.html?view=1#step-2">Again</a>')
        self.write('docs/index.html', '<a href="../index.html">Home</a>')
        (self.root / 'img').mkdir()
        (self.root / 'img' / 'logo.svg').write_text('<svg/>')
        (self.root / 'data.json').write_text('{}')
        self.assertEqual(links.check_html_tree(self.root), [])
        links.require_valid(self.root, 'Fixture site')

    def test_missing_target_file_is_reported(self):
        self.write('index.html', '<a href="api.html">API</a>')
        self.assertEqual(links.check_html_tree(self.root),
                         [{'file': 'index.html', 'link': 'api.html', 'problem': 'target file does not exist'}])

    def test_missing_fragment_in_another_page_is_reported(self):
        self.write('index.html', '<a href="api.html#op-missing">Op</a>')
        self.write('api.html', '<section id="op-present"></section>')
        problems = links.check_html_tree(self.root)
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0]['file'], 'index.html')
        self.assertIn('#op-missing', problems[0]['problem'])
        self.assertIn('api.html', problems[0]['problem'])

    def test_missing_same_page_fragment_is_reported(self):
        self.write('index.html', '<a href="#flow">Flow</a><div id="other"></div>')
        problems = links.check_html_tree(self.root)
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0]['link'], '#flow')
        self.assertIn('this page', problems[0]['problem'])

    def test_nested_page_is_checked(self):
        self.write('index.html', '<a href="deep/a.html">A</a>')
        self.write('deep/a.html', '<a href="missing.html">Missing</a>')
        self.assertEqual(links.check_html_tree(self.root),
                         [{'file': 'deep/a.html', 'link': 'missing.html', 'problem': 'target file does not exist'}])

    def test_link_escaping_the_root_is_refused(self):
        (self.base / 'outside.html').write_text(page('<p id="x">outside</p>'))
        self.write('index.html', '<a href="../outside.html#x">Out</a><a href="/etc/hosts">Abs</a>')
        problems = links.check_html_tree(self.root)
        self.assertEqual([item['link'] for item in problems], ['../outside.html#x', '/etc/hosts'])
        self.assertIn('outside the checked root', problems[0]['problem'])
        self.assertIn('absolute', problems[1]['problem'])

    def test_symlink_escaping_the_root_is_refused(self):
        (self.base / 'outside.html').write_text(page('<p>outside</p>'))
        (self.root / 'linked.html').symlink_to(self.base / 'outside.html')
        self.write('index.html', '<a href="linked.html">Linked</a>')
        problems = links.check_html_tree(self.root)
        self.assertTrue(problems)
        self.assertTrue(all('outside the checked root' in item['problem'] for item in problems))

    def test_external_links_are_ignored(self):
        self.write('index.html', '<a href="https://example.invalid/x#y">A</a><a href="http://example.invalid">B</a>'
                                 '<a href="mailto:owner@example.invalid">C</a><img src="data:image/png;base64,AA==">'
                                 '<a href="javascript:void(0)">D</a><script src="//cdn.example.invalid/x.js"></script>')
        self.assertEqual(links.check_html_tree(self.root), [])

    def test_require_valid_lists_at_most_ten_problems(self):
        self.write('index.html', ''.join('<a href="missing-' + str(n) + '.html">x</a>' for n in range(12)))
        with self.assertRaisesRegex(Blocked, 'link') as raised:
            links.require_valid(self.root, 'Fixture site')
        message = str(raised.exception)
        self.assertIn('12 broken local links', message)
        self.assertIn('missing-9.html', message)
        self.assertNotIn('missing-10.html', message)
        self.assertIn('2 more', message)

    def test_require_valid_blocks_a_missing_path(self):
        with self.assertRaisesRegex(Blocked, 'link'):
            links.require_valid(self.base / 'absent', 'Fixture site')

    def test_zip_with_a_broken_link_is_reported(self):
        archive = self.zip_of({'index.html': page('<a href="nested/a.html#x">A</a>'),
                               'nested/a.html': page('<p id="y"></p>')})
        problems = links.check_zip(archive)
        self.assertEqual(len(problems), 1)
        self.assertEqual(problems[0]['file'], 'index.html')
        self.assertIn('#x', problems[0]['problem'])
        with self.assertRaisesRegex(Blocked, 'link'):
            links.require_valid(archive, 'Fixture package')

    def test_valid_zip_passes(self):
        archive = self.zip_of({'index.html': page('<a href="nested/a.html#y">A</a>'),
                               'nested/a.html': page('<p id="y"></p><a href="../index.html">Back</a>')})
        self.assertEqual(links.check_zip(archive), [])
        links.require_valid(archive, 'Fixture package')

    def test_zip_with_a_parent_member_is_refused(self):
        archive = self.zip_of({'index.html': page(''), '../escape.html': page('')})
        with self.assertRaisesRegex(Blocked, r'\.\.'):
            links.check_zip(archive)
        self.assertFalse((self.base / 'escape.html').exists())

    def test_zip_with_an_absolute_member_is_refused(self):
        archive = self.zip_of({'/tmp/escape.html': page('')})
        with self.assertRaisesRegex(Blocked, 'absolute'):
            links.check_zip(archive)

    def test_zip_with_a_symlink_member_is_refused(self):
        archive = self.base / 'package.zip'
        with zipfile.ZipFile(archive, 'w') as bundle:
            info = zipfile.ZipInfo('index.html')
            info.external_attr = (stat.S_IFLNK | 0o777) << 16
            bundle.writestr(info, '/etc/hosts')
        with self.assertRaisesRegex(Blocked, 'symbolic link'):
            links.check_zip(archive)


class RendererLinkTests(unittest.TestCase):
    """Real renderer output must pass the validator without weakening it."""

    def test_review_site_pages_written_side_by_side(self):
        spec = fixtures.PreparationTests.spec(None)
        screens = fixtures.PreparationTests.screens(None)
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / 'screens.json').write_text(json.dumps(screens))
            (directory / 'api-contracts.json').write_text(json.dumps(screens['apis']))
            (directory / 'openapi.json').write_text(json.dumps(artifacts.openapi_document(screens['apis'])))
            (directory / 'api.html').write_text(artifacts.render_api_page(
                screens['apis'], screens=screens['screens'], journeys=screens.get('journeys')))
            (directory / 'index.html').write_text(artifacts.render_site(spec, screens, {}))
            (directory / 'usage.html').write_text(artifacts.render_usage_page(
                artifacts.provider_usage([directory]), {}))
            self.assertEqual(links.check_html_tree(directory), [])

    def test_preparation_report_alone_links_only_what_exists(self):
        spec = fixtures.PreparationTests.spec(None)
        with tempfile.TemporaryDirectory() as temp:
            directory = Path(temp)
            (directory / 'review.html').write_text(artifacts.render_site(
                spec, {'screens': []}, {}, title='SME and architect review', companions=False))
            self.assertEqual(links.check_html_tree(directory), [])


class WorkflowLinkTests(unittest.TestCase):
    """Reports and packages produced by the offline workflow fixtures."""

    def setUp(self):
        self.inner = fixtures.PreparationTests('test_four_phase_acceptance_no_cloud_or_application_build')
        self.inner.setUp()
        self.addCleanup(self.inner.doCleanups)

    def test_preparation_report_review_site_and_approved_package(self):
        inner = self.inner
        inner.validated()
        report = Path(app.preparation_report(inner.work, inner.project))
        self.assertEqual(links.check_html_tree(report.parent), [])
        links.require_valid(report.parent, 'Preparation report')
        inner.approve('validation')
        result = app.review_site(inner.work, inner.project, inner.args('review-site'), inner.runtime([inner.screens()]))
        site = Path(result['html']).parent
        self.assertEqual(links.check_html_tree(site), [])
        inner.approve('specifications')
        packaged = app.package(inner.work, inner.project)
        self.assertEqual(links.check_zip(packaged['archive']), [])
        links.require_valid(packaged['archive'], 'Approved package')


class DraftPackageLinkTests(unittest.TestCase):
    def setUp(self):
        self.inner = test_reframe_preview.PreviewTests('test_preview_skips_agents_preserves_gate_state_and_exports_draft')
        self.inner.setUp()
        self.addCleanup(self.inner.doCleanups)

    def test_draft_package_links_resolve(self):
        inner = self.inner
        result = preview.run(inner.work, inner.project, inner.arguments, app, inner.runtime)
        self.assertEqual(result['status'], 'DRAFT_READY')
        self.assertEqual(links.check_html_tree(Path(result['html']).parent), [])
        self.assertEqual(links.check_zip(result['archive']), [])


class ModePackageLinkTests(unittest.TestCase):
    def setUp(self):
        self.inner = test_reframe_optional.OptionalModeTests('test_missing_context_still_exports_parity_and_leaves_the_review_site')
        self.inner.setUp()
        self.addCleanup(shutil.rmtree, self.inner.root, True)

    def test_mode_packages_and_design_pages_link_resolve(self):
        inner = self.inner
        for version, mode in (('v1', 'functional-parity'), ('v2', 'reimagine')):
            optional.design_export(inner.root, inner.project, version, mode, 'unspecified')
            packaged = optional.package_export(inner.root, inner.project, version, mode)
            with self.subTest(mode=mode, artifact='design pages'):
                self.assertEqual(links.check_html_tree(inner.root / 'previews' / version), [])
            with self.subTest(mode=mode, artifact='package'):
                self.assertEqual(links.check_zip(inner.root / packaged['archive']), [])


if __name__ == '__main__':
    unittest.main()
