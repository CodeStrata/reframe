import json
import tempfile
import unittest

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import Changes, new_run
from reframe.transform import answers
from reframe.transform.driver import Driver, is_done

from tests.transform.fake_transform import FakeApi, FakeClient

MENU = ("Welcome.\n\n1. Assess only: analyze the code\n2. Assess and reimagine: analyze and generate requirements\n\n"
        "How would you like to proceed?")
CATALOG = ("## Business function catalog\n\n| # | Business Domain | Business Function | Data Paths |\n|---|---|---|---|\n"
           "| 1 | Payments | Card Payments | 4 |\n| 2 | Payments | Refunds | 2 |\n| 3 | Accounts | Account Profile | 3 |\n\n"
           "### Unassigned Programs\nYou can ask to reimagine them on their own or together with business functions.")
SELECT = [{"actionType": "SELECT", "data": {"selectInteractionData": {"options": [
    {"label": 'Reimagine business domain "Payments"', "value": 'Reimagine business domain "Payments"'},
    {"label": 'Reimagine business function "Refunds"', "value": 'Reimagine business function "Refunds"'},
    {"label": "Reimagine unassigned programs", "value": "Reimagine unassigned programs"}]}}}]
LOCATION_SCHEMA = {"type": "object", "required": ["assetLocation"], "properties": {"assetLocation": {"type": "string"},
                                                                                  "optInChatBox": {"type": "boolean"}}}


def system(message_id, text, at, interactions=None):
    return {"messageId": message_id, "messageOrigin": "SYSTEM", "text": text, "createdAt": at,
            "processingInfo": {"messageType": "FINAL_RESPONSE"}, **({"interactions": interactions} if interactions else {})}


def snapshot(status, steps, tasks=()):
    return {"job": {"job": {"statusDetails": {"status": status}}}, "plan": {"steps": [{"stepName": n, "status": s} for n, s in steps]},
            "tasks": {"hitlTasks": list(tasks)}}


class DriverTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.folder = new_run("demo", {"REFRAME_HOME": self.tmp.name})
        self.client, self.api = FakeClient(), FakeApi()
        self.clock = [1000.0]

    def tearDown(self):
        self.tmp.cleanup()

    def driver(self, mode="autonomous"):
        return Driver(self.client, self.api, self.folder, Changes(self.folder, "t"), workspace_id="ws-1", job_name="reframe-demo-abc123",
                      source_uri="s3://reframe-demo-abc123-src/source/x.zip", mode=mode, clock=lambda: self.clock[0],
                      sleep=lambda s: self.clock.__setitem__(0, self.clock[0] + s))

    def step(self, driver, snap, *messages):
        self.client.snapshots = [snap]
        self.api._messages.extend(messages)
        self.clock[0] += 61
        return driver.poll_once()

    def test_spike_one_sequence_autonomous(self):
        d = self.driver()
        d._ensure_job()
        self.step(d, snapshot("EXECUTING", []), system("m1", MENU, "2026-11-21T18:01:55"))
        self.assertIn("2. Assess and reimagine.", self.api.sent[0]["text"])
        self.client.tasks["t1"] = {"title": "Specify the source location", "uxComponentId": "SpecifyAssetsLocation", "_outputSchema": LOCATION_SCHEMA}
        self.step(d, snapshot("EXECUTING", [("Kickoff", "IN_PROGRESS")], [{"taskId": "t1", "status": "AWAITING_HUMAN_INPUT"}]))
        completed = self.client.changed("complete_task")[0]
        self.assertEqual(json.loads(completed["content"]), {"assetLocation": "s3://reframe-demo-abc123-src/source/x.zip"})
        self.client.tasks["t2"] = {"title": "Review business functions discovery results", "uxComponentId": answers.CATALOG_COMPONENT,
                                   "_outputSchema": {"type": "object", "required": ["x"]}}
        self.client.tasks["t3"] = {"title": "Add collaborators", "uxComponentId": "InviteCollaboratorsContent", "_outputSchema": {}}
        tasks = [{"taskId": "t2", "status": "AWAITING_HUMAN_INPUT"}, {"taskId": "t3", "status": "AWAITING_HUMAN_INPUT", "blockingType": "NON_BLOCKING"}]
        self.step(d, snapshot("AWAITING_HUMAN_INPUT", [("Discover business functions", "PENDING_HUMAN_INPUT")], tasks),
                  system("m2", CATALOG, "2026-11-21T18:20:41", SELECT))
        selection = self.api.sent[1]
        self.assertEqual(selection["origin"], "m2")
        self.assertEqual(selection["text"], 'Reimagine business domain "Payments", business domain "Accounts", and unassigned programs')
        self.assertEqual(len(self.client.changed("complete_task")), 1)  # neither the catalog form nor the collaborators form
        self.step(d, snapshot("AWAITING_HUMAN_INPUT", [("Discover business functions", "PENDING_HUMAN_INPUT")], tasks),
                  system("m3", "This will finalize discovery.\n\n**Do you want to proceed?**", "2026-11-21T18:22:31"))
        self.assertEqual(self.api.sent[2]["text"], "Yes, proceed.")
        done = self.step(d, snapshot("EXECUTING", [("Reimagine", "SUCCEEDED"), ("Generate requirements", "SUCCEEDED")], tasks[1:]))
        self.assertTrue(done["done"])
        decisions = self.folder.load("decisions.json")
        self.assertEqual(len(decisions), 4)
        self.assertEqual(len(self.api.sent), 3)

    def test_open_offer_left_alone_while_running(self):
        d = self.driver()
        d._ensure_job()
        self.step(d, snapshot("EXECUTING", [("Kickoff", "SUCCEEDED"), ("Analyze code", "SUCCEEDED")]),
                  system("m1", "Is there anything you'd like to know while the plan executes?", "2026-11-21T18:03:10"))
        self.assertEqual(self.api.sent, [])
        self.assertFalse(self.folder.exists("question.json"))

    def test_interactive_waits_for_answer(self):
        d = self.driver("interactive")
        d._ensure_job()
        summary = self.step(d, snapshot("EXECUTING", []), system("m1", MENU, "2026-11-21T18:01:55"))
        self.assertEqual(summary["waiting"]["kind"], "plan")
        question = self.folder.load("question.json")
        self.assertEqual(question["options"], ["Assess only", "Assess and reimagine"])
        answer = answers.interactive(answers.Question(**{k: (tuple(v) if isinstance(v, list) else v) for k, v in question.items()
                                                         if k in ("id", "kind", "text", "options", "replies", "interaction_origin_id")}),
                                     [1], None)
        self.folder.save("answer.json", {"id": question["id"], "text": answer.text, "reason": answer.reason})
        self.step(d, snapshot("EXECUTING", []))
        self.assertIn("1. Assess only.", self.api.sent[0]["text"])
        self.assertFalse(self.folder.exists("question.json"))
        self.assertIsNone(self.folder.load("decisions.json"))

    def test_failed_step_stops(self):
        d = self.driver()
        self.client.snapshots = [snapshot("EXECUTING", [("Analyze code", "FAILED")])]
        with self.assertRaises(Stop) as stop:
            d.run()
        self.assertEqual(stop.exception.outcome, Outcome.FAILED)

    def test_done_needs_generate_requirements(self):
        self.assertFalse(is_done([{"name": "Kickoff", "status": "SUCCEEDED"}]))
        self.assertTrue(is_done([{"name": "Kickoff", "status": "SUCCEEDED"}, {"name": "Generate requirements", "status": "SUCCEEDED"}]))


class AnswersTest(unittest.TestCase):
    def test_catalog_domains_and_everything(self):
        self.assertEqual(answers.catalog_domains(CATALOG), ["Payments", "Accounts"])
        question = answers.chat_question(system("m", CATALOG, "t", SELECT))
        self.assertEqual(question.kind, "catalog")
        self.assertEqual(question.options[0], answers.EVERYTHING)
        combined = answers.interactive(question, [2, 4], None)
        self.assertEqual(combined.text, 'Reimagine business domain "Payments" and unassigned programs')
        self.assertEqual(combined.interaction_origin_id, "m")

    def test_reply_yes_confirmation_answered(self):
        text = ("Please confirm to proceed with reimagining:\n- Daily Transaction Processing domain\n- Unassigned programs\n\n"
                "Once confirmed, this will finalize business function discovery and begin generating modernization requirements.\n\n"
                'Reply "yes" to confirm or "no" to cancel.')
        question = answers.chat_question(system("m", text, "t"))
        self.assertEqual(question.kind, "confirm")
        self.assertEqual(answers.autonomous(question).text, "yes")

    def test_bold_confirmation_recognised(self):
        self.assertEqual(answers.chat_question(system("m", "x\n**Do you want to proceed?**", "t")).kind, "confirm")

    def test_unknown_form_asks(self):
        self.assertEqual(answers.form_decision("Other", {"type": "object", "required": ["a"]}, None, "s3://x").action, "ask")
        self.assertEqual(answers.form_decision("Other", {"type": "object"}, None, "s3://x").action, "approve")


if __name__ == "__main__":
    unittest.main()
