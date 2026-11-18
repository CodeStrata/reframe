"""P0-01 (#216): v1 and v2 do not import each other. L1.

v1 is the set of modules listed in the root pyproject.toml (`py-modules`,
under scripts/). A v1 module reaches v2 only by being ported into reframe_v2
with its tests (specification section 15, P0-02), never by import.
"""

import ast
import tomllib
import unittest
from pathlib import Path

V2_ROOT = Path(__file__).resolve().parents[1]
REPO = V2_ROOT.parent
V2_SOURCES = sorted((V2_ROOT / "src").rglob("*.py")) + sorted((V2_ROOT / "tests").rglob("*.py"))


def v1_modules() -> set[str]:
    config = tomllib.loads((REPO / "pyproject.toml").read_text())
    return set(config["tool"]["setuptools"]["py-modules"])


def v1_sources() -> list[Path]:
    package_dir = tomllib.loads((REPO / "pyproject.toml").read_text())["tool"]["setuptools"]["package-dir"][""]
    return sorted((REPO / package_dir).rglob("*.py")) + sorted((REPO / "tests").rglob("*.py"))


def imported_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            roots.add(node.module.split(".")[0])
    return roots


class BoundaryTests(unittest.TestCase):
    def test_v1_module_list_is_found(self):
        self.assertIn("reframe", v1_modules())

    def test_v2_imports_nothing_from_v1(self):
        v1 = v1_modules()
        offenders = {
            str(path.relative_to(REPO)): sorted(imported_roots(path) & v1)
            for path in V2_SOURCES
            if imported_roots(path) & v1
        }
        self.assertEqual(offenders, {}, "port the module into reframe_v2 instead (P0-02)")

    def test_v1_imports_nothing_from_v2(self):
        offenders = [str(path.relative_to(REPO)) for path in v1_sources() if "reframe_v2" in imported_roots(path)]
        self.assertEqual(offenders, [])

    def test_v2_license_matches_the_repository_license(self):
        self.assertEqual((V2_ROOT / "LICENSE").read_text(), (REPO / "LICENSE").read_text())


if __name__ == "__main__":
    unittest.main()
