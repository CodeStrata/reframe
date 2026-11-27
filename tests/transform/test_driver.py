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
# The readiness menu after the selection, as AWS worded it on 23 November 2026.
READINESS = ("**Readiness Summary for Your Reimagine Selection:**\n\nYou have selected 2 business domains (Payments, Accounts) plus "
             "unassigned programs. Here's what's ready:\n\n- **3 business functions** across the 2 domains\n- **4 unassigned programs** "
             "to include\n- \u26a0\ufe0f 1 missing file (in Payments)\n\n**What would you like to do?**\n\n"
             "1. **Proceed** with reimagining all 3 business functions and 4 unassigned programs\n"
             "2. **Switch selection** to different business domains or functions\n"
             "3. **Drop unassigned programs** and reimagine only the 3 business functions in the named domains\n\n"
             "Please reply with your choice.")
# A name that is both a business domain and a business function, in the three wordings AWS used on a test run on 25 November 2026.
CLASH_BARE = ('I need you to decide between these two options for "Web Service Interface Generation":\n\n'
              "1. **domain Web Service Interface Generation** \u2014 reimagine all business functions in that domain\n"
              "2. **function Web Service Interface Generation** \u2014 reimagine only that one business function\n\n"
              'Please reply with either "domain" or "function" to clarify, and I\'ll proceed with your full selection.')
CLASH_INTEND = ('I need you to clarify the ambiguity for "Web Service Interface Generation" before I can proceed.\n\n'
                '**"Web Service Interface Generation"** exists as both a business domain AND a business function with the same name.\n\n'
                "Please reply with one of these:\n\n"
                "- **domain Web Service Interface Generation** \u2014 to reimagine all business functions in that domain\n"
                "- **function Web Service Interface Generation** \u2014 to reimagine only that one business function\n\n"
                "Which did you intend?")
CLASH_PREFER = ('The tool found an ambiguity: **"Web Service Interface Generation"** exists as both a business domain and a business '
                "function with the same name.\n\nPlease clarify which you meant:\n\n"
                "- **Domain Web Service Interface Generation** \u2014 to reimagine all business functions in that domain\n"
                "- **Function Web Service Interface Generation** \u2014 to reimagine only that one business function\n\n"
                "Which would you prefer?")
NO_ACTION = ("Your reimagine workflow for those business domains and unassigned programs is already in progress. The system has "
             "started generating modernization requirements for:\n\n- Payments\n- Accounts\n- Unassigned programs\n\n"
             "No further action is needed at this time. The workflow will continue processing, and you can check on results as "
             "they become available.")
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

    def stalled_after_catalog(self, mode="autonomous"):
        d = self.driver(mode)
        d._ensure_job()
        template = {"isBPDEnabled": True, "s3Uri": "s3://reframe-demo-abc123-src/transform-output/job-1/business-functions/delivery.zip"}
        self.client.tasks["t2"] = {"title": "Review business functions discovery results", "uxComponentId": answers.CATALOG_COMPONENT,
                                   "blockingType": "BLOCKING", "_outputSchema": {}, "_responseTemplate": template}
        tasks = [{"taskId": "t2", "status": "AWAITING_HUMAN_INPUT", "blockingType": "BLOCKING"}]
        waiting = snapshot("AWAITING_HUMAN_INPUT", [("Discover business functions", "PENDING_HUMAN_INPUT")], tasks)
        self.step(d, waiting, system("m2", CATALOG, "2026-11-21T18:20:41", SELECT))
        self.step(d, waiting, system("m3", "This will finalize discovery.\n\nDo you want to proceed?", "2026-11-21T18:22:31"))
        self.step(d, waiting, system("m4", "It appears the finalization workflow has already processed your request.\n\n"
                                           "What would you like to do next?", "2026-11-21T18:23:00"))
        return d, waiting, template

    def test_stalled_catalog_form_gets_aws_template(self):
        d, waiting, template = self.stalled_after_catalog()
        self.assertFalse(self.folder.exists("question.json"))  # the open offer is not a question
        for _ in range(3):  # the open-offer poll was the first quiet one
            self.step(d, waiting)
        self.assertEqual(self.client.changed("complete_task"), [])
        self.step(d, waiting)
        completed = self.client.changed("complete_task")
        self.assertEqual(len(completed), 1)
        self.assertEqual(json.loads(completed[0]["content"]), template)
        self.step(d, waiting)
        self.assertEqual(len(self.client.changed("complete_task")), 1)
        self.step(d, waiting, system("m5", "Please select the business function(s) to Re-Imagine before continuing.", "2026-11-21T18:40:00"))
        self.assertEqual(self.api.sent[-1], self.api.sent[0])  # the same selection, structured against the catalog message
        self.assertEqual(self.api.sent[-1]["origin"], "m2")

    def test_a_selection_refused_as_already_running_is_recovered_once(self):
        # The second test codebase, 26 November 2026: after the form, AWS asked for the selection again, refused the same selection as a second
        # request ("already in progress"), reopened the form, and so on for hours, with no reimagine steps in its plan. Asked in
        # plain words what was running, it showed its readiness menu again, and Proceed started the plan.
        from reframe.transform.driver import RECOVERY
        d, waiting, template = self.stalled_after_catalog()
        for _ in range(4):
            self.step(d, waiting)
        self.assertEqual(len(self.client.changed("complete_task")), 1)
        self.step(d, waiting, system("m5", "Please select the business function(s) to Re-Imagine before continuing.", "2026-11-21T18:40:00"))
        self.step(d, waiting, system("m6", "I cannot initiate a new reimagine request. A reimagine workflow is already in progress for "
                                           "those exact business domains and unassigned programs.", "2026-11-21T18:40:05"))
        self.assertEqual(self.api.sent[-1]["text"], RECOVERY)  # asked once, in plain words
        self.client.tasks["t3"] = dict(self.client.tasks["t2"])  # AWS reopens the review form
        again = snapshot("AWAITING_HUMAN_INPUT", [("Discover business functions", "PENDING_HUMAN_INPUT")],
                         [{"taskId": "t3", "status": "AWAITING_HUMAN_INPUT", "blockingType": "BLOCKING"}])
        for _ in range(6):
            self.step(d, again)
        self.assertEqual(len(self.client.changed("complete_task")), 1)  # the reopened form is not submitted again
        self.step(d, again, system("m7", READINESS, "2026-11-21T18:41:00"))
        self.assertTrue(self.api.sent[-1]["text"].startswith("1") or "Proceed" in self.api.sent[-1]["text"])  # its Proceed
        sent = len(self.api.sent)
        self.step(d, again, system("m8", "I cannot initiate a new reimagine request. A reimagine workflow is already in progress.", "2026-11-21T18:42:00"))
        self.assertEqual(len(self.api.sent), sent)  # a second refusal is not answered by Reframe
        question = self.folder.load("question.json")
        self.assertEqual(question["id"], "m8")
        self.assertIn("AWS Transform console", question["text"])

    def readiness_after_catalog(self, mode="autonomous", menu=READINESS):
        d = self.driver(mode)
        d._ensure_job()
        template = {"isBPDEnabled": True, "s3Uri": "s3://reframe-demo-abc123-src/transform-output/job-1/business-functions/delivery.zip"}
        self.client.tasks["t2"] = {"title": "Review business functions discovery results", "uxComponentId": answers.CATALOG_COMPONENT,
                                   "blockingType": "BLOCKING", "_outputSchema": {}, "_responseTemplate": template}
        tasks = [{"taskId": "t2", "status": "AWAITING_HUMAN_INPUT", "blockingType": "BLOCKING"}]
        waiting = snapshot("AWAITING_HUMAN_INPUT", [("Discover business functions", "PENDING_HUMAN_INPUT")], tasks)
        self.step(d, waiting, system("m2", CATALOG, "2026-11-23T03:38:19", SELECT))
        self.step(d, waiting, system("m3", "A confirmation is required before proceeding. **Proceed with reimagining the selected business "
                                           "domains?**\n\nPlease reply **yes** to confirm or **no** to cancel.", "2026-11-23T03:39:16"))
        self.step(d, waiting, system("m4", menu, "2026-11-23T03:40:18"))
        return d, waiting

    def test_readiness_menu_answered_with_its_proceed_choice(self):
        d, waiting = self.readiness_after_catalog()
        self.assertEqual([m["text"] for m in self.api.sent][1:],
                         ["yes", "1. Proceed with reimagining all 3 business functions and 4 unassigned programs"])
        self.assertFalse(self.folder.exists("question.json"))
        self.step(d, waiting, system("m5", NO_ACTION, "2026-11-23T03:41:00"))
        self.assertFalse(self.folder.exists("question.json"))  # a notice, not a question
        self.assertEqual(len(self.api.sent), 3)

    def test_review_form_never_submitted_over_a_question_with_choices(self):
        # A menu Reframe does not recognise waits as a chat question. Before 23 November 2026 the stall rule counted those
        # polls as quiet and submitted the review form over it, and AWS asked for the selection again.
        menu = READINESS.replace("Please reply with your choice.", "Let me know which option you prefer.")
        d, waiting = self.readiness_after_catalog(menu=menu)
        self.assertEqual(self.folder.load("question.json")["kind"], "chat")
        for _ in range(8):
            self.step(d, waiting)
        self.assertEqual(self.client.changed("complete_task"), [])
        self.assertEqual(self.folder.load("question.json")["id"], "m4")

    def test_name_clash_answered_with_the_domain(self):
        # A test run, 25 November 2026: the selection named business domain "Web Service Interface Generation", which is also a
        # business function's name. AWS asked which was meant; Reframe left it waiting, the stall rule submitted the review
        # form over it, and the run looped (selection, the same question) until the owner answered "domain".
        d, waiting = self.readiness_after_catalog(menu=CLASH_PREFER)
        self.assertEqual(self.api.sent[-1]["text"], "domain Web Service Interface Generation")
        self.assertFalse(self.folder.exists("question.json"))
        self.assertIn("names business domains only", self.folder.load("decisions.json")[-1]["reason"])
        self.step(d, waiting, system("m5", CLASH_BARE, "2026-11-25T17:11:59"))
        self.assertEqual(self.api.sent[-1]["text"], "domain")
        self.assertFalse(self.folder.exists("question.json"))  # nothing waits for the person

    def test_name_clash_waits_in_interactive_mode(self):
        d, waiting = self.readiness_after_catalog(mode="interactive", menu=CLASH_INTEND)
        question = self.folder.load("question.json")
        self.assertEqual((question["kind"], question["replies"]),
                         ("clash", ["domain Web Service Interface Generation", "function Web Service Interface Generation"]))
        for _ in range(8):
            self.step(d, waiting)
        self.assertEqual(self.client.changed("complete_task"), [])

    def test_stalled_catalog_form_with_foreign_bucket_asks(self):
        d, waiting, template = self.stalled_after_catalog()
        self.client.tasks["t2"]["_responseTemplate"] = {**template, "s3Uri": "s3://someone-else/transform-output/x/business-functions/delivery.zip"}
        self.folder.remove("tasks/t2.json")
        for _ in range(5):
            self.step(d, waiting)
        self.assertEqual(self.client.changed("complete_task"), [])
        self.assertEqual(self.folder.load("question.json")["kind"], "form")

    def test_question_for_an_older_message_is_cleared(self):
        d = self.driver("interactive")
        d._ensure_job()
        awaiting = snapshot("AWAITING_HUMAN_INPUT", [("Discover business functions", "PENDING_HUMAN_INPUT")])
        self.step(d, awaiting, system("m1", "Which output format would you like?", "2026-11-21T18:30:00"))
        self.assertEqual(self.folder.load("question.json")["id"], "m1")
        self.step(d, snapshot("EXECUTING", [("Reimagine", "IN_PROGRESS")]), system("m2", "Adding steps to your plan...", "2026-11-21T18:31:00"))
        self.assertFalse(self.folder.exists("question.json"))

    def test_saved_question_shows_the_newer_reading(self):
        d = self.driver("interactive")
        d._ensure_job()
        self.folder.save("question.json", {"id": "m1", "kind": "chat", "text": "x", "options": [], "asked_at": "earlier"})
        text = "Please confirm to proceed with the reimagine workflow for the domain."
        self.step(d, snapshot("AWAITING_HUMAN_INPUT", [("Discover business functions", "PENDING_HUMAN_INPUT")]),
                  system("m1", text, "2026-11-21T18:30:00"))
        saved = self.folder.load("question.json")
        self.assertEqual((saved["kind"], saved["options"][0], saved["asked_at"]), ("confirm", "Yes, proceed", "earlier"))

    def test_interactive_reselect_offers_the_same_selection(self):
        d = self.driver("interactive")
        d._ensure_job()
        waiting = snapshot("AWAITING_HUMAN_INPUT", [("Discover business functions", "PENDING_HUMAN_INPUT")])
        self.step(d, waiting, system("m2", CATALOG, "2026-11-21T18:20:41", SELECT))
        self.folder.save("answer.json", {"id": "m2", "text": 'Reimagine business domain "Payments"', "reason": "the person"})
        self.step(d, waiting)
        self.assertEqual(self.api.sent[-1]["origin"], "m2")
        self.step(d, waiting, system("m5", "Please select the business function(s) to Re-Imagine before continuing.", "2026-11-21T18:40:00"))
        question = self.folder.load("question.json")
        self.assertEqual((question["kind"], question["interaction_origin_id"]), ("reselect", "m2"))
        self.assertIn('business domain "Payments"', question["options"][0])
        self.folder.save("answer.json", {"id": "m5", "text": question["replies"][0], "reason": "the person"})
        self.step(d, waiting)
        self.assertEqual(self.api.sent[-1], {"text": 'Reimagine business domain "Payments"', "origin": "m2"})

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

    def test_reply_yes_to_proceed_answered(self):
        text = ("Your reimagine selection is ready.\n\n**Total: 14 business functions + 25 unassigned programs**\n\n"
                'Reply "yes" to proceed with the reimagine workflow or "no" to cancel.')
        question = answers.chat_question(system("m", text, "t"))
        self.assertEqual(question.kind, "confirm")
        self.assertEqual(answers.autonomous(question).text, "yes")

    def test_yes_no_confirmation_recognised(self):
        text = ("Your selection includes:\n- Technical domain\n\n"
                "**Please confirm: Proceed with the reimagine for these selections?** (yes/no)")
        question = answers.chat_question(system("m", text, "t"))
        self.assertEqual((question.kind, answers.autonomous(question).text), ("confirm", "yes"))

    def test_spelled_out_reply_sent_as_given(self):
        text = ("The system is asking for explicit confirmation to proceed despite the missing files.\n\n"
                "To move forward, please reply: **Yes, proceed**")
        self.assertEqual(answers.autonomous(answers.chat_question(system("m", text, "t"), awaiting=True)).text, "Yes, proceed")

    def test_either_or_proceed_question_gets_an_explicit_proceed(self):
        text = ("Would you like to proceed with generating the modernization requirements for the 2 business functions, "
                "or would you prefer to view the missing/unsupported file details first?")
        self.assertEqual(answers.autonomous(answers.chat_question(system("m", text, "t"))).text, "Yes, proceed.")

    def test_statement_confirmation_recognised(self):
        text = ('Please confirm to proceed with the reimagine workflow for the "Card Authorization Management" domain and '
                "unassigned programs. This will finalize business function discovery and initiate spec generation for modernization.")
        question = answers.chat_question(system("m", text, "t"), awaiting=True)
        self.assertEqual((question.kind, question.options[0], answers.autonomous(question).text), ("confirm", "Yes, proceed", "Yes, proceed."))

    def test_open_offer_is_not_a_question_even_when_awaiting(self):
        text = "The reimagine workflow has been initiated.\n\nYou can now:\n- Ask questions\n\nWhat would you like to do next?"
        self.assertIsNone(answers.chat_question(system("m", text, "t"), awaiting=True))
        started = ("**Reimagine workflow initiated successfully!**\n\nThe specification will be ready shortly. "
                   "Feel free to ask questions or check on job progress while the analysis runs.")
        self.assertIsNone(answers.chat_question(system("m", started, "t"), awaiting=True))
        executing = ("Your job is now executing.\n\nThe Amazon Neptune cluster in your account is storing the artifacts. "
                     "You can monitor progress or ask me for status updates as the workflow runs.")
        self.assertIsNone(answers.chat_question(system("m", executing, "t"), awaiting=True))
        notified = ("Reimagine workflow started. Specification generation is now running.\n\nYou'll be notified when the "
                    "specifications are ready. Feel free to query results or check status at any time.")
        self.assertIsNone(answers.chat_question(system("m", notified, "t"), awaiting=True))

    def test_name_clash(self):
        for text, reply in ((CLASH_BARE, "domain"), (CLASH_INTEND, "domain Web Service Interface Generation"),
                            (CLASH_PREFER, "domain Web Service Interface Generation")):
            question = answers.chat_question(system("m", text, "t"))
            self.assertEqual((question.kind, answers.autonomous(question).text), ("clash", reply))
            self.assertEqual(answers.interactive(question, [2], None).text, reply.replace("domain", "function"))
        two = ("Both names are ambiguous:\n\n- domain Payments: every function\n- function Payments: that one\n"
               "- domain Accounts: every function\n- function Accounts: that one\n\nWhich did you mean?")
        self.assertEqual(answers.autonomous(answers.chat_question(system("m", two, "t"))).text, "domain Payments, domain Accounts")
        # The readiness menu and the catalog name domains and functions, but never one name both ways.
        self.assertEqual(answers.chat_question(system("m", READINESS, "t")).kind, "choice")
        self.assertEqual(answers.name_clashes(CATALOG), [])

    def test_readiness_menu(self):
        question = answers.chat_question(system("m", READINESS, "t"), awaiting=True)
        self.assertEqual(question.kind, "choice")
        self.assertEqual(question.options[1], "Switch selection to different business domains or functions")
        self.assertEqual(answers.autonomous(question).text, "1. Proceed with reimagining all 3 business functions and 4 unassigned programs")
        self.assertEqual(answers.interactive(question, [3], None).text,
                         "3. Drop unassigned programs and reimagine only the 3 business functions in the named domains")
        two = READINESS.replace("2. **Switch selection**", "2. **Proceed** only")
        self.assertIsNone(answers.autonomous(answers.chat_question(system("m", two, "t"), awaiting=True)))
        self.assertTrue(answers.offers_choices(READINESS))
        self.assertFalse(answers.offers_choices(NO_ACTION))

    def test_no_further_action_is_a_notice(self):
        self.assertIsNone(answers.chat_question(system("m", NO_ACTION, "t"), awaiting=True))

    def test_bold_confirmation_recognised(self):
        self.assertEqual(answers.chat_question(system("m", "x\n**Do you want to proceed?**", "t")).kind, "confirm")

    def test_unknown_form_asks(self):
        self.assertEqual(answers.form_decision("Other", {"type": "object", "required": ["a"]}, None, "s3://x").action, "ask")
        self.assertEqual(answers.form_decision("Other", {"type": "object"}, None, "s3://x").action, "approve")


if __name__ == "__main__":
    unittest.main()
