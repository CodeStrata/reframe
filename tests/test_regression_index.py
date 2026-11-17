"""The CardDemo regression index names only tests that exist, and covers all 21 items (spec §10). L1."""
import ast
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / 'docs' / 'validation' / 'carddemo-regressions.md'


def defined_tests(path):
    """Every test method name in one test module."""
    tree = ast.parse(path.read_text())
    return {node.name for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}


class RegressionIndexTests(unittest.TestCase):
    def test_every_item_has_a_test_and_every_named_test_exists(self):
        rows = re.findall(r'^\| (\d+) \| [^|]+ \| (.+) \|$', INDEX.read_text(), re.M)
        self.assertEqual([int(number) for number, _ in rows], list(range(1, 22)))
        cache = {}
        for number, cell in rows:
            names = re.findall(r'`(test_[a-z0-9_]+\.py)::(test_[a-z0-9_]+)`', cell)
            self.assertTrue(names, 'item ' + number + ' names no test')
            synthetic = False
            for module, test in names:
                if module not in cache:
                    cache[module] = defined_tests(ROOT / 'tests' / module)
                self.assertIn(test, cache[module], module + '::' + test + ' (item ' + number + ')')
                marked = re.search(re.escape(test) + r'`\s*\(\*saved\*\)', cell)
                synthetic = synthetic or not marked
            self.assertTrue(synthetic, 'item ' + number + ' depends only on the saved workspace')


if __name__ == '__main__':
    unittest.main()
