"""P4-04: user journeys, one Claude step per domain, every answer checked by Reframe."""
import os
import tempfile
import unittest
from unittest import mock

from reframe.core.errors import Stop
from reframe.core.runfolder import new_run
from reframe.design import flow, inventory, journeypage, journeys
from tests.design.test_flow import ACCOUNT, CSD, MENU, MENU_TABLE, SIGNON, bms
from tests.reconcile.test_decide import FakeClaude

REQUIREMENTS = {
    "complete": True,
    "domains": [{"key": "access", "name": "Access", "functions": ["Access/SignOn"]}, {"key": "accounts", "name": "Accounts", "functions": ["Accounts/View"]}],
    "names": {"Access/SignOn": {"name": "Sign on"}, "Accounts/View": {"name": "View accounts"}},
    "functions": {
        "Access/SignOn": {"capabilities": [{"number": 1, "title": "Sign on", "story": "As a user, I want to sign on",
                                            "requirements": [{"code": "REQ-F-001", "text": "The system shall check the password."}]}]},
        "Accounts/View": {"capabilities": [{"number": 1, "title": "View an account", "story": "As a clerk, I want to see an account",
                                            "requirements": [{"code": "REQ-F-001", "text": "The system shall show the balance."}]}]}},
}
RULES = [{"program": "SIGN00C", "function": "Access/SignOn"}, {"program": "MENU00C", "function": "Access/SignOn"},
         {"program": "ACCTV00C", "function": "Accounts/View"}]


def good(data):
    """A journey per domain over every screen of it, starting at sign-on and following the flow."""
    if data["domain"]["name"] == "Access":
        return {"journeys": [{"name": "Sign in", "role": "user", "goal": "Get to the menu",
                              "steps": [{"screen": "SIGN0A", "action": "Type the user ID and password"}, {"screen": "MENU0A", "action": "See the options"}],
                              "capabilities": ["rec/Access/SignOn#1"], "requirements": ["rec/Access/SignOn/REQ-F-001"]}], "unused": []}
    return {"journeys": [{"name": "View an account", "role": "clerk", "goal": "See a balance",
                          "steps": [{"screen": "SIGN0A", "action": "Sign in"}, {"screen": "MENU0A", "action": "Choose 1"},
                                    {"screen": "ACCTV0A", "action": "Read the balance"}, {"screen": "MENU0A", "action": "Press F3"}],
                          "capabilities": ["rec/Accounts/View#1"], "requirements": ["rec/Accounts/View/REQ-F-001"]}], "unused": []}


class JourneysTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        env.start()
        self.addCleanup(env.stop)
        self.folder = new_run("demo")
        self.folder.update(project="demo")
        legacy = self.folder.root / "claude" / "legacy" / "demo"
        files = {"app/bms/SIGN00.bms": bms("SIGN00", "SIGN0A", "ENTER=Sign-on  F3=Exit"), "app/bms/MENU00.bms": bms("MENU00", "MENU0A", "ENTER=Go  F3=Exit"),
                 "app/bms/ACCTV00.bms": bms("ACCTV00", "ACCTV0A", "F3=Back  F7=Up"), "app/cpy/MENU02Y.cpy": MENU_TABLE,
                 "app/cbl/SIGN00C.cbl": SIGNON, "app/cbl/MENU00C.cbl": MENU, "app/cbl/ACCTV00C.cbl": ACCOUNT, "app/csd/DEMO.csd": CSD}
        for name, text in files.items():
            (legacy / name).parent.mkdir(parents=True, exist_ok=True)
            (legacy / name).write_text(text)
        screens = inventory.inventory(legacy)
        self.folder.save("design/screens.json", screens)
        self.folder.save("design/flow.json", flow.flow(legacy, screens))
        self.folder.save("outputs/reconcile/requirements.json", REQUIREMENTS)
        self.folder.save("outputs/reconcile/rules.json", {"rules": RULES})

    def fake(self, answer):
        claude = FakeClaude(journeys=answer)
        claude.root = self.folder.root / "claude"
        return claude

    def test_journeys_per_domain_checked_and_kept(self):
        claude = self.fake(good)
        value = journeys.run(self.folder, claude)
        self.assertEqual([(j["id"], j["name"], j["domain"]) for j in value["journeys"]],
                         [("J01", "Sign in", "access"), ("J02", "View an account", "accounts")])
        self.assertEqual(value["problems"], [])
        self.assertEqual(len(claude.other_calls), 2)
        given = {c[1]["domain"]["name"]: c[1] for c in claude.other_calls}
        self.assertEqual([s["screen"] for s in given["Accounts"]["screens"]], ["ACCTV0A"])
        self.assertIn({"from": "MENU0A", "to": "ACCTV0A", "by": "option 1 Account View"}, given["Accounts"]["flow"])
        self.assertEqual(given["Accounts"]["capabilities"][0]["requirements"][0]["key"], "rec/Accounts/View/REQ-F-001")
        self.assertIn("follow only links listed", claude.other_calls[0][2])
        journeys.run(self.folder, claude)
        self.assertEqual(len(claude.other_calls), 2)  # nothing changed: kept
        page = journeypage.draw(self.folder, value).read_text()
        self.assertIn("View an account", page)
        self.assertIn('href="legacy/ACCTV0A.html"', page)

    def test_a_failed_answer_is_asked_again_with_the_reasons(self):
        answers = iter([lambda data: {"journeys": [{"name": "Jump", "role": "clerk", "goal": "g",
                                                    "steps": [{"screen": "SIGN0A", "action": "a"}, {"screen": "ACCTV0A", "action": "b"},
                                                              {"screen": "NOPE", "action": "c"}],
                                                    "capabilities": ["rec/Accounts/View#9"], "requirements": ["rec/Access/SignOn/REQ-F-001"]}],
                                       "unused": []}])

        def first_bad(data):
            if data["domain"]["name"] == "Accounts":
                bad = next(answers, None)
                if bad:
                    return bad(data)
            return good(data)
        claude = self.fake(first_bad)
        value = journeys.run(self.folder, claude)
        retry = [c for c in claude.other_calls if c[0].endswith("-retry")]
        self.assertEqual(len(retry), 1)
        for expected in ('"NOPE" is not a screen', "no link in the flow goes from SIGN0A to ACCTV0A", 'capability "rec/Accounts/View#9" is not listed',
                         "requirement \"rec/Access/SignOn/REQ-F-001\" is not one of the journey's capabilities' requirements"):
            self.assertIn(expected, retry[0][2])
        self.assertEqual(value["problems"], [])
        self.assertEqual(value["domains"]["accounts"]["attempts"], 2)

    def test_a_screen_in_no_journey_must_be_listed_as_unused(self):
        data = {"screens": [{"screen": "A"}, {"screen": "B"}], "other_screens": [], "flow": [], "capabilities": [{"key": "c", "requirements": []}]}
        answer = {"journeys": [{"name": "j", "steps": [{"screen": "A", "action": ""}], "capabilities": ["c"], "requirements": []}], "unused": []}
        self.assertEqual(journeys.problems(answer, data), ["screen B is in no journey and not listed as unused"])
        answer["unused"] = [{"screen": "B", "reason": "no link reaches it"}]
        self.assertEqual(journeys.problems(answer, data), [])

    def test_the_usage_limit_stops_and_keeps_what_is_done(self):
        claude = self.fake(lambda data: "limit" if data["domain"]["name"] == "Accounts" else good(data))
        with self.assertRaises(Stop):
            journeys.run(self.folder, claude)
        self.assertEqual(list(self.folder.load(journeys.FILE)["domains"]), ["access"])
        value = journeys.run(self.folder, self.fake(good))  # run again: only what is left
        self.assertEqual(len(value["journeys"]), 2)


if __name__ == "__main__":
    unittest.main()
