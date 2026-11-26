"""P4-05: modern screens and the mapping of every legacy screen, field and key, one Claude step per domain."""
import unittest

from reframe.design import journeys, modernpage, screens
from reframe.design.flow import CALLER
from tests.design.test_journeys import JourneysTest, good as good_journeys
from tests.reconcile.test_decide import FakeClaude

RULES = [{"key": "rec/u:sign/1", "program": "SIGN00C", "function": "Access/SignOn", "kind": "validation", "text": "WHEN the password is wrong, SHOW 'Wrong Password'"},
         {"key": "rec/u:menu/1", "program": "MENU00C", "function": "Access/SignOn", "kind": "technical", "text": "Opens a file"},
         {"key": "rec/u:acct/1", "program": "ACCTV00C", "function": "Accounts/View", "kind": "validation", "text": "WHEN the account is blank, SHOW 'Enter an account'"}]


def design(data):
    """A modern screen per legacy screen: a component per field and per key, every item mapped once, every validation shown."""
    found, mapping = [], []
    menu_target = {"Access": "S-MENU0A", "Accounts": "S-MENU0A"}
    for s in data["legacy_screens"]:
        sid = f"S-{s['screen']}"
        parts = [{"id": f"f-{f['field']}", "type": "text", "label": f["label"] or f["field"]} for f in s["fields"]]
        parts += [{"id": f"k-{k['key']}", "type": "button", "label": k["says"] or k["key"], "goes_to": menu_target[data["domain"]] if k["key"] == "F3" else ""}
                  for k in s["keys"]]
        parts[0]["rules"] = [r["key"] for r in data["rules"] if r["kind"] == "validation" and r["program"] in s["programs"]]
        found.append({"id": sid, "title": s["title"] or s["screen"], "purpose": "p", "journeys": [j["id"] for j in data["journeys"]][:1],
                      "replaces": [s["screen"]], "components": parts})
        mapping.append({"legacy_screen": s["screen"], "legacy": s["screen"], "kind": "screen", "how": "kept", "becomes": sid, "why": "w"})
        mapping += [{"legacy_screen": s["screen"], "legacy": f["field"], "kind": "field", "how": "kept", "becomes": f"{sid}/f-{f['field']}", "why": "w"}
                    for f in s["fields"]]
        mapping += [{"legacy_screen": s["screen"], "legacy": k["key"], "kind": "key", "how": "kept", "becomes": f"{sid}/k-{k['key']}", "why": "w"} for k in s["keys"]]
    return {"screens": found, "mapping": mapping}


class ScreensTest(JourneysTest):
    def setUp(self):
        super().setUp()
        self.folder.save("outputs/reconcile/rules.json", {"rules": RULES})
        journeys.run(self.folder, self.fake(good_journeys))

    def designer(self, answer):
        claude = FakeClaude(screens=answer)
        claude.root = self.folder.root / "claude"
        return claude

    def test_every_legacy_item_mapped_and_every_validation_shown(self):
        claude = self.designer(design)
        value = screens.run(self.folder, claude)
        self.assertEqual(value["problems"], [])
        self.assertEqual(sorted(s["id"] for s in value["screens"]), ["S-ACCTV0A", "S-MENU0A", "S-SIGN0A"])
        given = {c[1]["domain"]: c[1] for c in claude.other_calls}
        self.assertEqual([j["id"] for j in given["Access"]["journeys"]], ["J01"])  # only the domain's own journeys
        self.assertEqual([r["key"] for r in given["Accounts"]["rules"]], ["rec/u:acct/1"])
        self.assertIn("OPTION", [f["field"] for f in given["Accounts"]["legacy_screens"][0]["fields"]])
        self.assertIn({"key": "F3", "says": "Back", "leads_to": [CALLER, "MENU00C"]},
                      given["Accounts"]["legacy_screens"][0]["keys"])
        self.assertEqual(value["counts"]["how"]["kept"], value["counts"]["mapped"])
        screens.run(self.folder, claude)
        self.assertEqual(len(claude.other_calls), 2)  # unchanged: kept
        page = modernpage.draw(self.folder, value).read_text()
        self.assertIn('id="S-ACCTV0A"', page)
        self.assertIn('href="legacy/ACCTV0A.html"', page)

    def test_a_missing_field_an_unshown_validation_and_a_bad_type_are_asked_again(self):
        def first(data):
            answer = design(data)
            if data["domain"] == "Accounts" and not getattr(first, "done", False):
                first.done = True
                answer["mapping"] = [m for m in answer["mapping"] if m["legacy"] != "OPTION"]
                answer["screens"][0]["components"][0]["rules"] = []
                answer["screens"][0]["components"][0]["type"] = "spinner"
            return answer
        claude = self.designer(first)
        value = screens.run(self.folder, claude)
        retry = [c for c in claude.other_calls if c[0].endswith("-retry")]
        self.assertEqual(len(retry), 1)
        for expected in ("mapping: field OPTION on ACCTV0A is not mapped", "validation rule rec/u:acct/1 of ACCTV0A is shown by no component",
                         'type "spinner" is not a component of the design system'):
            self.assertIn(expected, retry[0][2])
        self.assertEqual(value["problems"], [])

    def test_a_link_to_a_screen_no_domain_designed_is_listed(self):
        def wrong_target(data):
            answer = design(data)
            answer["screens"][0]["components"].append({"id": "x", "type": "link", "label": "Elsewhere", "goes_to": "S-NOWHERE"})
            return answer
        value = screens.run(self.folder, self.designer(wrong_target))
        self.assertTrue(any('goes to "S-NOWHERE", which is no screen' in p for p in value["problems"]))

    def test_the_links_pass_gives_a_domain_the_other_domains_screens(self):
        def guess(data):
            answer = design(data)
            if data["domain"] == "Access":
                target = "S-ACCTV0A" if data.get("other_domains_screens") else "S-ACCOUNT-VIEW"  # a guess, until it sees the others
                answer["screens"][0]["components"].append({"id": "to-account", "type": "link", "label": "Accounts", "goes_to": target})
            answer["screens"].append({"id": "S-SHELL", "title": "Shell", "purpose": "", "journeys": [], "replaces": [],
                                      "components": [{"id": f"nav-{data['domain'].lower()}", "type": "nav", "label": data["domain"]}]})
            return answer
        claude = self.designer(guess)
        value = screens.run(self.folder, claude)
        links = [c for c in claude.other_calls if c[0].endswith("-links")]
        self.assertEqual(len(links), 1)
        self.assertIn('goes to "S-ACCOUNT-VIEW", which is no screen', links[0][2])
        self.assertIn("S-ACCTV0A", [x["id"] for x in links[0][1]["other_domains_screens"]])
        self.assertEqual(value["problems"], [])
        shell = [x for x in value["screens"] if x["id"] == "S-SHELL"]
        self.assertEqual(len(shell), 1)  # two domains' shells are one shared screen, with both domains' components
        self.assertEqual((shell[0]["domain"], [c["id"] for c in shell[0]["components"]]), ("Shared", ["nav-access", "nav-accounts"]))
        screens.run(self.folder, claude)
        self.assertEqual(len([c for c in claude.other_calls if c[0].endswith("-links")]), 1)  # not asked again

    def test_mapped_twice_and_unknown_items(self):
        data = {"components": screens.COMPONENTS, "rules": [], "requirements": [], "journeys": [],
                "legacy_screens": [{"screen": "A", "programs": ["P"], "fields": [{"field": "F1"}], "keys": []}]}
        answer = {"screens": [{"id": "S-A", "title": "A", "journeys": [], "replaces": ["A"], "components": [{"id": "c", "type": "text", "label": "F1"}]}],
                  "mapping": [{"legacy_screen": "A", "legacy": "A", "kind": "screen", "how": "kept", "becomes": "S-A", "why": ""},
                              {"legacy_screen": "A", "legacy": "F1", "kind": "field", "how": "kept", "becomes": "S-A/c", "why": ""},
                              {"legacy_screen": "A", "legacy": "F1", "kind": "field", "how": "dropped", "becomes": "", "why": ""},
                              {"legacy_screen": "A", "legacy": "F9", "kind": "field", "how": "kept", "becomes": "S-A/c", "why": ""}]}
        found = screens.problems(answer, data)
        self.assertIn("mapping: field F1 on A is mapped 2 times", found)
        self.assertIn('mapping: field "F9" on A is not a legacy field listed', found)


def load_tests(loader, tests, pattern):
    """Only this module's own tests: ScreensTest borrows JourneysTest's setup, not its tests."""
    return unittest.TestSuite(ScreensTest(name) for name in vars(ScreensTest) if name.startswith("test_"))


if __name__ == "__main__":
    unittest.main()
