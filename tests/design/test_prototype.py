"""P4-06: the clickable prototype, drawn by Reframe from the modern screens with no model."""
import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

from reframe.design import prototype, screens
from tests.design.test_screens import ScreensTest, design

NODE = shutil.which("node")
RENDER = Path(__file__).with_name("render_prototype.js")


def with_actions(data):
    """The fake design, with a required field and a success message on the account screen, and a link to the shell."""
    answer = design(data)
    for s in answer["screens"]:
        if s["id"] == "S-ACCTV0A":
            s["components"][0].update({"validation": "Required: 'Enter an account' when blank"})
            s["components"].append({"id": "save", "type": "button", "label": "Save"})
            s["components"].append({"id": "result", "type": "message", "label": "Result", "shows": "Success: 'Account saved' and the form clears"})
            s["components"].append({"id": "back", "type": "link", "label": "Back", "goes_to": "S-SHELL"})
    answer["screens"].append({"id": "S-SHELL", "title": "Shell", "purpose": "", "journeys": [], "replaces": [],
                              "components": [{"id": "h", "type": "header", "label": "Demo App"},
                                             {"id": "n1", "type": "link", "label": "Accounts", "goes_to": "S-ACCTV0A", "section": "Main navigation"}]})
    return answer


def load_tests(loader, tests, pattern):
    return unittest.TestSuite(PrototypeTest(name) for name in vars(PrototypeTest) if name.startswith("test_"))


class PrototypeTest(ScreensTest):
    def build(self):
        screens.run(self.folder, self.designer(with_actions))
        load = self.folder.load
        return prototype.build(load("design/screens.json"), load("design/modern.json"), load("design/journeys.json"), [], "demo")

    def test_screens_routes_sample_data_and_legacy_copies(self):
        data = self.build()
        ids = {s["id"] for s in data["screens"]}
        self.assertEqual(ids, {"S-SIGN0A", "S-MENU0A", "S-ACCTV0A"})  # the shell is around the screens, not a screen
        self.assertEqual((data["start"], data["app"]), ("S-SIGN0A", "Demo App"))
        account = next(s for s in data["screens"] if s["id"] == "S-ACCTV0A")
        back = next(c for c in account["components"] if c["id"] == "back")
        self.assertEqual(back["goes_to"], data["home"])  # a link to the shell goes Home
        first = account["components"][0]
        self.assertTrue(first["required"])
        self.assertEqual(first["messages"], ["Enter an account"])
        self.assertEqual(account["success"], "Account saved")
        self.assertEqual([n["to"] for n in data["nav"]], ["S-ACCTV0A"])
        self.assertIn("<pre>", data["legacy"]["ACCTV0A"]["grid"])
        self.assertTrue(all(st["screen"] in ids for j in data["journeys"] for st in j["steps"]))
        load = self.folder.load
        again = prototype.build(load("design/screens.json"), load("design/modern.json"), load("design/journeys.json"), [], "demo")
        self.assertEqual(json.dumps(again, sort_keys=True), json.dumps(data, sort_keys=True))  # the same data every build

    def test_sample_values(self):
        self.assertRegex(prototype.sample("Account number", "11-digit account number", 0, 7), r"^\d{11}$")
        self.assertRegex(prototype.sample("Current balance", "", 0, 7), r"^\$[\d,]+\.\d\d$")
        self.assertRegex(prototype.sample("Opened", "Open date (MM/DD/YY)", 0, 7), r"^\d\d/\d\d/\d\d$")
        self.assertEqual(prototype.sample("SSN", "", 0, 7)[:7], "***-**-")
        self.assertEqual(prototype.sample("x", "y", 0, 7), prototype.sample("x", "y", 0, 7))

    @unittest.skipUnless(NODE, "Node is not installed")
    def test_every_route_renders_and_acts_without_a_script_error(self):
        page = prototype.draw(self.folder, self.build())
        done = subprocess.run([NODE, str(RENDER), str(page)], capture_output=True, text=True, timeout=60)
        views = [json.loads(line) for line in done.stdout.splitlines() if line.strip()]
        self.assertEqual([v["route"] for v in views if not v["ok"]], [], done.stdout[-2000:])
        account = next(v for v in views if v["route"] == "#/S-ACCTV0A")
        self.assertIn("Account saved", account["banner"])
        self.assertIn("class=\"legacy\"", account["legacy"])
        self.assertIn("design/S-ACCTV0A", account["review"])
        known = {"journeys"} | {v["route"][2:] for v in views if v["route"].startswith("#/S-")}
        for v in views:
            self.assertTrue(set(re.findall(r'href="#/([^"]+)"', v.get("html", ""))) <= known, v["route"])
        self.assertNotIn("http", page.read_text().replace("http-equiv", ""))  # nothing loaded from outside


if __name__ == "__main__":
    unittest.main()
