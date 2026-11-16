"""Recursive local link and fragment validation for every generated report.

One validator covers the preparation report, the design and review site, and
the extracted ZIP packages. A local href or src must name a file inside the
checked root, and a #fragment must name an element in the target page.
External links are not fetched or checked.
"""
import os
import re
import stat
import tempfile
import zipfile
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

from pilot import Blocked

EXTERNAL = ('http:', 'https:', 'mailto:', 'data:', 'javascript:')
SCHEME = re.compile(r'^[A-Za-z][A-Za-z0-9+.-]*:')
HTML_SUFFIXES = ('.html', '.htm')
MAX_REPORTED = 10


class _Page(HTMLParser):
    """Collect the local link targets and the fragment anchors of one HTML page."""

    def __init__(self):
        """Start with no links and no anchors."""
        super().__init__(convert_charrefs=True)
        self.links = []
        self.anchors = set()

    def handle_starttag(self, tag, attrs):
        """Record href and src values, element ids, and named anchors."""
        for name, value in attrs:
            if value is None:
                continue
            if name in ('href', 'src'):
                self.links.append(value)
            elif name == 'id':
                self.anchors.add(value)
            elif name == 'name' and tag == 'a':
                self.anchors.add(value)

    handle_startendtag = handle_starttag


def _parse(path):
    """Parse one HTML file and return its links and anchors."""
    page = _Page()
    page.feed(Path(path).read_text(encoding='utf-8', errors='replace'))
    page.close()
    return page


def _is_external(link):
    """True when the link leaves the package and is not checked."""
    lowered = link.strip().lower()
    return lowered.startswith('//') or lowered.startswith(EXTERNAL)


def check_html_tree(root):
    """Check every local link and fragment in every HTML file under a directory."""
    root = Path(root).resolve()
    if not root.is_dir():
        raise Blocked('Link check needs a directory: ' + str(root))
    cache = {}

    def page(path):
        """Return the parsed page for one HTML file, parsing it once."""
        if path not in cache:
            cache[path] = _parse(path)
        return cache[path]

    problems = []
    for source in sorted(p for p in root.rglob('*') if p.suffix.lower() in HTML_SUFFIXES and p.is_file()):
        relative = source.relative_to(root).as_posix()
        source = source.resolve()
        try:
            source.relative_to(root)
        except ValueError:
            problems.append({'file': relative, 'link': '', 'problem': 'page resolves outside the checked root'})
            continue
        for raw in page(source).links:
            link = raw.strip()
            if _is_external(link):
                continue

            def problem(text):
                """Record one problem for this link."""
                problems.append({'file': relative, 'link': raw, 'problem': text})

            if SCHEME.match(link):
                problem('unsupported link scheme')
                continue
            target_part, _hash, fragment = link.partition('#')
            target_part = target_part.split('?', 1)[0]
            fragment = unquote(fragment)
            if not target_part:
                target = source
            else:
                decoded = unquote(target_part)
                if decoded.startswith(('/', '\\')) or re.match(r'^[A-Za-z]:[\\/]', decoded):
                    problem('absolute path is not portable')
                    continue
                target = Path(os.path.normpath(source.parent / decoded))
                try:
                    target.relative_to(root)
                    target = target.resolve()
                    target.relative_to(root)
                except ValueError:
                    problem('target is outside the checked root')
                    continue
                if target.is_dir():
                    target = target / 'index.html'
                if not target.is_file():
                    problem('target file does not exist')
                    continue
            if fragment and target.suffix.lower() in HTML_SUFFIXES and fragment not in page(target).anchors:
                where = 'this page' if target == source else target.relative_to(root).as_posix()
                problem('fragment #' + fragment + ' is not an id or anchor name in ' + where)
    return problems


def _unsafe_member(info):
    """Return why a ZIP member cannot be extracted safely, or None."""
    name = info.filename
    if '\\' in name:
        return 'uses a backslash path'
    if name.startswith('/') or re.match(r'^[A-Za-z]:', name):
        return 'is an absolute path'
    if '..' in PurePosixPath(name).parts:
        return 'escapes the archive with ..'
    if stat.S_ISLNK(info.external_attr >> 16):
        return 'is a symbolic link'
    return None


def check_zip(path):
    """Extract a ZIP into a temporary directory and check its links and fragments."""
    with zipfile.ZipFile(path) as archive, tempfile.TemporaryDirectory(prefix='reframe-links-') as temp:
        destination = Path(temp).resolve()
        members = archive.infolist()
        for info in members:
            reason = _unsafe_member(info)
            if reason:
                raise Blocked('ZIP member ' + info.filename + ' ' + reason + '; refused before link check')
        for info in members:
            if info.is_dir():
                continue
            target = destination / info.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as source, open(target, 'wb') as output:
                while True:
                    chunk = source.read(1 << 20)
                    if not chunk:
                        break
                    output.write(chunk)
        return check_html_tree(destination)


def require_valid(root_or_zip, label):
    """Block when a directory or ZIP package has a broken local link or fragment."""
    path = Path(root_or_zip)
    if path.is_dir():
        problems = check_html_tree(path)
    elif path.is_file() and zipfile.is_zipfile(path):
        problems = check_zip(path)
    else:
        raise Blocked(label + ' link check found no directory or ZIP package at ' + str(path))
    if not problems:
        return
    shown = ['- ' + item['file'] + ': ' + item['link'] + ' (' + item['problem'] + ')' for item in problems[:MAX_REPORTED]]
    more = len(problems) - len(shown)
    raise Blocked(label + ' has ' + str(len(problems)) + ' broken local link'
                  + ('' if len(problems) == 1 else 's') + ':\n' + '\n'.join(shown)
                  + ('\n- and ' + str(more) + ' more' if more else ''))
