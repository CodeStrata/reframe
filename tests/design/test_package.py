"""P4-08: the AI-DLC package, written by Reframe from the final specifications in three forms, with no model."""
import json
import tempfile
import unittest
from pathlib import Path

from reframe.design import package, specs
from tests.design.test_specs import MENU, SpecsTest, written


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(PackageTest(name) for name in vars(PackageTest) if name.startswith("test_"))


class PackageTest(SpecsTest):
    def setUp(self):
        super().setUp()
        specs.run(self.folder, self.writer(written))
        proto = self.folder.path("outputs/design/prototype/index.html")
        proto.parent.mkdir(parents=True, exist_ok=True)
        proto.write_text("<!doctype html><title>Prototype</title>")

    def test_three_forms_with_every_id_traced(self):
        value = package.run(self.folder)
        self.assertEqual((value["version"], value["new"], value["problems"]), (1, True, []))
        root = Path(value["path"])
        for path in ("kiro/.kiro/steering/product.md", "kiro/.kiro/steering/tech.md", "kiro/.kiro/steering/structure.md",
                     "kiro/.kiro/specs/sig-01-sign-on/requirements.md", "kiro/.kiro/specs/sig-01-sign-on/design.md", "kiro/.kiro/specs/sig-01-sign-on/tasks.md",
                     "claude-code/CLAUDE.md", "claude-code/tasks.md", "claude-code/specs/va-01-view-an-account.md", "claude-code/ui-reference/index.html",
                     "spec-kit/.specify/memory/constitution.md", "spec-kit/specs/002-va-01-view-an-account/spec.md",
                     "spec-kit/specs/002-va-01-view-an-account/plan.md", "spec-kit/.claude/agents/test-generation.md", "CHANGES.md", "manifest.json"):
            self.assertTrue((root / path).is_file(), path)
        self.assertEqual(len(list((root / "spec-kit/.claude/agents").glob("*.md"))), 6)
        kiro = (root / "kiro/.kiro/specs/sig-01-sign-on/requirements.md").read_text()
        self.assertIn("**Status: FINAL**, signed off by Pat, 2026-11-25.", kiro)
        self.assertIn("GIVEN USERID: ADMIN001; PASSWD: WRONG WHEN the password does not match THEN it shows 'Wrong Password. Try again ...' (SIG-C01-AC-01; SIG-BR-001)", kiro)
        self.assertIn("**Status: DRAFT**", (root / "kiro/.kiro/specs/va-01-view-an-account/design.md").read_text())
        design = (root / "kiro/.kiro/specs/va-01-view-an-account/design.md").read_text()
        self.assertIn("Record `ACCOUNT-RECORD`", design)
        self.assertIn("| All zeros | **Gap:** No rule says whether all zeros is accepted. | |", design)
        # tasks: each for a role, citing IDs; the technical requirement goes to the service task with its design note
        tasks = (root / "kiro/.kiro/specs/sig-01-sign-on/tasks.md").read_text()
        self.assertIn("SIG-C01-T3 [api] Build the services behind the screens", tasks)
        self.assertIn("SIG-BR-002: A keyed lookup of the user by ID.", tasks)
        self.assertIn("_Requirements: SIG-REQ-F-002_", tasks)
        self.assertIn("- [ ] VA-C01-T", (root / "spec-kit/specs/002-va-01-view-an-account/tasks.md").read_text())
        self.assertIn("[ui-modernization] Build the screen", (root / "claude-code/tasks.md").read_text())
        trace = (root / "claude-code/traceability.md").read_text()
        self.assertIn("| VA-REQ-F-001 | VA-C01 | `rec/Accounts/View/REQ-F-001` | VA-BR-001 | VA-C01-AC-01, VA-C01-AC-02 |", trace)
        self.assertIn(f"| SIG-BR-002 | MENU00C | `{MENU}` |", trace)
        self.assertIn("**Not given yet.**", (root / "claude-code/CLAUDE.md").read_text())
        self.assertEqual((root / "CHANGES.md").read_text(), "# Changes in v1\n\nThe first version: 2 capabilities.\n")
        # unchanged: the same version; a sign-off and a stack: a new one that says what changed
        self.assertEqual((package.run(self.folder)["version"], package.run(self.folder)["new"]), (1, False))
        path = self.folder.path("design/specs/Accounts-View-1.json")
        spec = json.loads(path.read_text())
        spec["status"], spec["signed_off"] = "final", [{"reviewer": "Sam", "at": "2026-11-26T09:00:00Z", "comment": ""}]
        spec["requirements"][0]["text"] = "When the account number is blank, the system shall show 'Enter an account number'."
        path.write_text(json.dumps(spec))
        specs.stack_of(self.folder, "React; Java 21; PostgreSQL")
        again = package.run(self.folder)
        self.assertEqual((again["version"], again["new"]), (2, True))
        changes = (Path(again["path"]) / "CHANGES.md").read_text()
        self.assertIn("- The target stack: not given → React; Java 21; PostgreSQL.", changes)
        self.assertIn("- VA-C01 View an account: now final (was draft); requirements changed: VA-REQ-F-001.", changes)
        self.assertIn("Java 21", (Path(again["path"]) / "kiro/.kiro/steering/tech.md").read_text())
        self.assertTrue(self.folder.path("outputs/design/package/v1/manifest.json").is_file())  # earlier versions are kept

    def test_ids_stay_from_version_to_version(self):
        given = [{"function": "F/One", "function_name": "Card Account Update", "rules": [{"key": "b"}, {"key": "a"}]},
                 {"function": "F/Two", "function_name": "Customer Account Update", "rules": [{"key": "c"}]}]
        first = package.ids(given, {})
        self.assertEqual(first["functions"], {"F/One": "CAU", "F/Two": "CAU2"})
        self.assertEqual(first["rules"], {"b": "CAU-BR-001", "a": "CAU-BR-002", "c": "CAU2-BR-001"})
        given[0]["rules"].insert(0, {"key": "new"})
        self.assertEqual(package.ids(given, first)["rules"], {**first["rules"], "new": "CAU-BR-003"})

    def test_a_missing_id_is_found_and_the_copy_is_cleaned(self):
        value = package.run(self.folder)
        root = Path(value["path"])
        raw = [package.label(s, package.ids(package.load_specs(self.folder), {})) for s in package.load_specs(self.folder)]
        ts = {s["id"]: package.tasks(s) for s in raw}
        (root / "spec-kit/specs/001-sig-01-sign-on/tasks.md").unlink()
        found = package.check(root, raw, ts)
        self.assertEqual(found, ["spec-kit: SIG-C01 is missing " + ", ".join(t["id"] for t in ts["SIG-C01"])])  # only there: the other forms still have them
        with tempfile.TemporaryDirectory() as out:
            done = package.copy_out(self.folder, Path(out), "kiro")
            self.assertEqual(done["left"], [])
            self.assertTrue((Path(out) / "kiro/.kiro/steering/product.md").is_file())
            self.assertFalse((Path(out) / "claude-code").exists())
            self.assertNotIn(str(Path.home()), (Path(out) / "kiro/traceability.md").read_text())


if __name__ == "__main__":
    unittest.main()
