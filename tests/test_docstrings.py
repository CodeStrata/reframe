"""Every module-level function and class method in scripts/ says what it does (#115). Nested helpers are exempt. L1."""
import ast
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'


class DocstringTests(unittest.TestCase):
    def test_module_functions_and_methods_have_docstrings(self):
        missing = []
        for path in sorted(SCRIPTS.glob('*.py')):
            tree = ast.parse(path.read_text())
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not ast.get_docstring(node):
                    missing.append(path.name + ':' + node.name)
                if isinstance(node, ast.ClassDef):
                    for item in node.body:
                        if (isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith('__')
                                and not ast.get_docstring(item)):
                            missing.append(path.name + ':' + node.name + '.' + item.name)
        self.assertEqual(missing, [])


if __name__ == '__main__':
    unittest.main()
