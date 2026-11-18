"""P0-01 (#216): pull requests into v2 must fill in the specification-alignment section. L1."""

import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / ".github" / "scripts" / "check_spec_alignment.py"
TEMPLATE = REPO / ".github" / "pull_request_template.md"

spec = importlib.util.spec_from_file_location("check_spec_alignment", SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

GOOD = """## Specification alignment (v2)

- Specification sections: 15
- Stories: #216
- [x] The specification, plan, epics and stories already describe this change (docs/v2/README.md)
"""


class AlignmentCheckTests(unittest.TestCase):
    def test_complete_section_passes(self):
        self.assertEqual(check.problems(GOOD), [])

    def test_windows_line_endings_pass(self):
        self.assertEqual(check.problems(GOOD.replace("\n", "\r\n")), [])

    def test_unfilled_template_fails_on_every_line(self):
        self.assertEqual(len(check.problems(TEMPLATE.read_text())), 3)

    def test_missing_section_fails(self):
        self.assertEqual(len(check.problems("Fixes a typo.")), 1)

    def test_story_needs_an_issue_number(self):
        found = check.problems(GOOD.replace("#216", "P0-01"))
        self.assertEqual(len(found), 1)
        self.assertIn("Stories", found[0])

    def test_unticked_confirmation_fails(self):
        found = check.problems(GOOD.replace("- [x]", "- [ ]"))
        self.assertEqual(len(found), 1)
        self.assertIn("update them first", found[0])

    def test_empty_sections_line_fails(self):
        found = check.problems(GOOD.replace("Specification sections: 15", "Specification sections:"))
        self.assertEqual(len(found), 1)


if __name__ == "__main__":
    unittest.main()
