"""The parser, --help, README, CLI guide, and recovery messages describe the same commands (FR-12; AC-32; #116). L1."""
import argparse
import ast
import fnmatch
import re
import unittest
from pathlib import Path

import reframe as app

ROOT = Path(__file__).resolve().parents[1]
GUIDES = [ROOT / 'README.md', ROOT / 'docs' / 'cli-guide.md', ROOT / 'docs' / 'four-phase-workflow.md']
RECOVERY = ('resume', 'upgrade-framework', 'recover-ui-call', 'recover-provider', 'reconcile-operation',
            'reconcile-design', 'recovery-plan', 'feedback', 'model-budget')


def subparsers(parser):
    """The sub-command map of one parser, or an empty map."""
    found = [action for action in parser._actions if isinstance(action, argparse._SubParsersAction)]
    return found[0] if found else None


def commands():
    """Top-level command names."""
    return set(subparsers(app.parser()).choices)


def code_lines(path):
    """Shell lines inside fenced code blocks."""
    lines, inside = [], False
    for line in path.read_text().splitlines():
        if line.lstrip().startswith('```'):
            inside = not inside
            continue
        if inside:
            lines.append(line)
    return lines


def mentioned(text):
    """Command words that follow `reframe`, with or without --workspace."""
    return re.findall(r'(?<![\w/.-])reframe (?:--workspace \S+ )?([a-z][a-z-]*)\b', text)


def script_strings():
    """Every string literal in the CLI modules."""
    found = []
    for path in sorted((ROOT / 'scripts').glob('*.py')):
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                found.append((path.name, node.value))
    return found


def package_table():
    """File names and patterns listed in the README package table."""
    text = (ROOT / 'README.md').read_text()
    section = text[text.index('## What the package contains'):text.index('## Deliverables and quality gates')]
    names = set()
    for row in section.splitlines():
        if row.startswith('| `'):
            names.update(re.findall(r'`([^`]+)`', row.split('|')[1]))
    return {name.replace('<function>', '*') for name in names}


def undocumented(archive_names):
    """Archive members the README package table does not list."""
    patterns = package_table()
    return sorted(name for name in archive_names if not any(fnmatch.fnmatch(name, pattern) for pattern in patterns))


class DocsConsistencyTests(unittest.TestCase):
    def test_every_command_and_subcommand_has_help(self):
        top = subparsers(app.parser())
        described = {action.dest for action in top._choices_actions}
        self.assertEqual(described, set(top.choices), 'commands without --help text')
        for name, child in top.choices.items():
            nested = subparsers(child)
            if nested:
                self.assertEqual({action.dest for action in nested._choices_actions}, set(nested.choices), name)

    def test_the_cli_guide_documents_every_command(self):
        guide = set(mentioned((ROOT / 'docs' / 'cli-guide.md').read_text()))
        self.assertEqual(sorted(commands() - guide), [])

    def test_docs_and_recovery_messages_name_only_real_commands(self):
        known = commands() | {'demo', 'ui', 'flow'}  # handled by main() before the parser
        for path in GUIDES:
            self.assertEqual(sorted(set(mentioned(path.read_text())) - known), [], path.name)
        prose = {'command', 'command-line', 'prefix'}  # 'the reframe command', 'reframe command-line parser'
        stale = sorted({(name, word) for name, value in script_strings() for word in mentioned(value) if word not in known | prose})
        self.assertEqual(stale, [])

    def test_doc_examples_never_carry_a_storable_name_or_rationale(self):
        for path in GUIDES:
            for line in code_lines(path):
                for flag, value in re.findall(r'--(by|note|answer) ("[^"]*"|\'[^\']*\'|\S+)', line):
                    self.assertTrue(app.instructional_placeholder(value.strip('"\'')),
                                    path.name + ': --' + flag + ' ' + value + ' would be stored if copied')

    def test_recovery_examples_name_the_workspace(self):
        for path in GUIDES:
            for line in code_lines(path):
                words = mentioned(line)
                if any(word in RECOVERY for word in words) or re.search(r'reframe .*decide .*--(amend|placeholders)', line):
                    self.assertIn('--workspace', line, path.name + ': ' + line)

    def test_the_command_reference_matches_help(self):
        text = (ROOT / 'docs' / 'cli-guide.md').read_text()
        section = text[text.index('## Command reference'):]
        section = section[:section.index('\n## ')]
        rows = dict(re.findall(r'^\| `reframe --workspace "\$W" ([a-z-]+)`[^|]*\| (.+) \|$', section, re.M))
        top = subparsers(app.parser())
        self.assertEqual(rows, {action.dest: ' '.join(action.help.split()) for action in top._choices_actions})
        for name, child in top.choices.items():
            self.assertTrue(child.description, name + ' --help has no description')

    def test_the_package_table_names_real_writers(self):
        text = (ROOT / 'README.md').read_text()
        section = text[text.index('## What the package contains'):text.index('## Deliverables and quality gates')]
        modules = {path.stem: path.read_text() for path in (ROOT / 'scripts').glob('*.py')}
        for writer in set(re.findall(r'`((?:reframe_\w+\.)?\w+)\(\)`', section)):
            module, _, function = writer.rpartition('.')
            source = modules[module or 'reframe']
            self.assertRegex(source, r'(?m)^def ' + function + r'\(', writer)


if __name__ == '__main__':
    unittest.main()
