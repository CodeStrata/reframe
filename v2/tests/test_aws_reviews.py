"""P0-11 (#226): AWS review-task classifier (section 4). L1.

Form and chat shapes follow those recorded in v1's live runs
(docs/validation/acceptance-defects.md), reduced to synthetic fixtures with
no job, task or account identifiers. Section 14 scenario: unknown AWS task.
"""

import unittest

from reframe_v2.aws_reviews import ChatQuestion, Class, Form, Intake, classify_chat, classify_form, fits_schema, needs_answer

SOURCE_SCHEMA = {"type": "object", "required": ["assetLocation"], "properties": {"assetLocation": {"type": "string"}}}
INTAKE = Intake("s3://sample-bucket/source.zip", True, "all")


def form(component=None, schema=None, title="task"):
    return Form("task-1", title, component, schema if schema is not None else {})


class FormTests(unittest.TestCase):
    def test_source_location_is_answered_from_the_verified_source(self):
        decision = classify_form(form("SpecifyAssetsLocation", SOURCE_SCHEMA), INTAKE)
        self.assertEqual(decision.cls, Class.ANSWER_FROM_INTAKE)
        self.assertEqual(decision.response, {"assetLocation": "s3://sample-bucket/source.zip"})
        self.assertEqual(set(decision.audit), {"task", "schema_hash", "response", "policy"})

    def test_source_location_with_an_unverified_source_parks(self):
        intake = Intake("s3://sample-bucket/source.zip", False, "all")
        self.assertEqual(classify_form(form("SpecifyAssetsLocation", SOURCE_SCHEMA), intake).cls, Class.PARK)

    def test_source_location_with_any_other_schema_parks(self):
        schema = dict(SOURCE_SCHEMA, properties={"assetLocation": {"type": "string"}, "branch": {"type": "string"}})
        self.assertEqual(classify_form(form("SpecifyAssetsLocation", schema), INTAKE).cls, Class.PARK)

    def test_display_only_is_recorded_and_not_answered(self):
        decision = classify_form(form("MainframeBreResultComponent", {"displayOnly": True}, "Business rule extraction results"), INTAKE)
        self.assertEqual(decision.cls, Class.DISPLAY_ONLY)
        self.assertIsNone(decision.response)

    def test_approve_only_review_is_approved_and_marked_not_reviewed(self):
        decision = classify_form(form("SampleReviewComponent", {"type": "object", "properties": {}}, "Review business functions discovery results"), INTAKE)
        self.assertEqual(decision.cls, Class.APPROVE_ONLY)
        self.assertEqual(decision.evidence_status, "NOT_CHECKED")
        self.assertIn("not reviewed by a person", decision.reason)

    def test_ask_policy_and_audit_mode_park_every_approval(self):
        schema = {"type": "object", "properties": {}}
        for intake in (Intake(None, False, "all", aws_reviews="ask"), Intake(None, False, "all", audit_mode=True)):
            self.assertEqual(classify_form(form("SampleReviewComponent", schema), intake).cls, Class.PARK)

    def test_a_form_with_a_required_field_parks(self):
        schema = {"type": "object", "required": ["choice"], "properties": {"choice": {"type": "string", "enum": ["a", "b"]}}}
        self.assertEqual(classify_form(form("SampleChoiceComponent", schema), INTAKE).cls, Class.PARK)

    def test_an_unknown_form_or_schema_parks_without_submission(self):
        for schema in ({}, {"type": "object", "additionalProperties": True}, {"type": "array"}):
            with self.subTest(schema=schema):
                decision = classify_form(form("NeverSeenComponent", schema), INTAKE)
                self.assertEqual(decision.cls, Class.PARK)
                self.assertIsNone(decision.response)


class ChatTests(unittest.TestCase):
    def test_proceed_question_is_approve_only(self):
        decision = classify_chat(ChatQuestion("m1", "  Proceed with this PLAN?  "), INTAKE)
        self.assertEqual(decision.cls, Class.APPROVE_ONLY)
        self.assertEqual(decision.evidence_status, "NOT_CHECKED")

    def test_proceed_question_parks_under_ask(self):
        intake = Intake(None, False, "all", aws_reviews="ask")
        self.assertEqual(classify_chat(ChatQuestion("m1", "Proceed with this plan?"), intake).cls, Class.PARK)

    def test_scope_all_selects_every_function_aws_lists(self):
        question = ChatQuestion("m2", "Please select the business function(s) to Re-Imagine before continuing.", ("Bill Payment", "Account View"))
        decision = classify_chat(question, INTAKE)
        self.assertEqual(decision.cls, Class.ANSWER_FROM_INTAKE)
        self.assertEqual(decision.response, {"selected": ["Bill Payment", "Account View"], "text": "Bill Payment, Account View"})

    def test_a_scope_file_selects_its_functions_when_aws_lists_them_exactly(self):
        question = ChatQuestion("m2", "Please select the business function(s) to Re-Imagine", ("Bill Payment", "Account View"))
        decision = classify_chat(question, Intake(None, False, "list", ("Bill Payment",)))
        self.assertEqual(decision.response, {"selected": ["Bill Payment"], "text": "Bill Payment"})

    def test_a_scope_file_naming_a_function_aws_does_not_list_parks(self):
        question = ChatQuestion("m2", "Please select the business function(s) to Re-Imagine", ("Bill Payment",))
        self.assertEqual(classify_chat(question, Intake(None, False, "list", ("Bill payment",))).cls, Class.PARK)

    def test_an_unrecognized_question_parks(self):
        self.assertEqual(classify_chat(ChatQuestion("m3", "Which database should the target use?"), INTAKE).cls, Class.PARK)


# AWS's setup chat as recorded live on 20 November 2026 (P2-10, #263).
PLAN_MENU = """To begin, let me know what you are looking to accomplish today on your mainframe modernization project. You can write out an objective or select from options below:

1. Assess and reimagine: Identify modernization boundaries to identify business functions, and generate requirements to reimagine the business functions.

2. Reimagine: If you already have a scoped application, generate requirements and reimagine this application

3. See list of all capabilities to create a custom job plan

How would you like to proceed?"""
OBJECTIVE = """You selected option 1, assess and reimagine. This workflow will analyze code and data to discover discrete data paths and produce a catalog of business functions. You will then generate modernization requirements to reimagine your selected business functions.

These workflows use Amazon Neptune to store artifacts about your legacy systems. You will need to configure an Amazon Neptune cluster in your account.

Does this objective match your goals?"""
LANGUAGE = """Now, before we generate your plan, I'd like to ask about output language preferences.

Your plan will generate assessment and modernization output. English output will always be produced. You can also choose to receive it in any of the supported languages listed below:

- **Portuguese** \u2014 Brazilian Portuguese (pt-BR) or European Portuguese (pt-PT)
- **German** (de)

Would you like your output translated into any of these languages, or would you prefer English only?"""
PROCEED = """Perfect. Your plan has been generated. Review the plan in the job panel on the left side of the screen.

Additional steps may have been added due to dependencies.

Proceed with this plan?"""
EXECUTING = """Your plan is now executing. The job will run asynchronously in the background. You can monitor progress in the job panel and provide information as needed through the task forms that appear.

When you're ready to provide your source code location or have any questions about the job, let me know."""


class SetupChatTests(unittest.TestCase):
    def test_the_plan_menu_is_answered_with_the_recorded_plan_and_every_setup_answer_in_one_message(self):
        decision = classify_chat(ChatQuestion("m1", PLAN_MENU), INTAKE)
        self.assertEqual(decision.cls, Class.ANSWER_FROM_INTAKE)
        self.assertEqual(decision.response["plan"], "1. Assess and reimagine")
        text = decision.response["text"]
        self.assertTrue(text.startswith("1. Assess and reimagine."))
        for answer in ("English only, no translations", "No collaborators", "reimagine connector", "proceed with it"):
            self.assertIn(answer, text)
        self.assertNotIn("s3://", text)

    def test_a_plan_the_menu_does_not_list_parks(self):
        intake = Intake(None, False, "all", plan="Refactor")
        self.assertEqual(classify_chat(ChatQuestion("m1", PLAN_MENU), intake).cls, Class.PARK)

    def test_under_ask_the_setup_message_does_not_approve_the_plan(self):
        intake = Intake(None, False, "all", aws_reviews="ask")
        text = classify_chat(ChatQuestion("m1", PLAN_MENU), intake).response["text"]
        self.assertNotIn("proceed", text.casefold().split("generate the job plan now")[1])

    def test_the_objective_confirmation_is_answered_when_aws_restates_the_recorded_plan(self):
        decision = classify_chat(ChatQuestion("m2", OBJECTIVE), INTAKE)
        self.assertEqual(decision.cls, Class.ANSWER_FROM_INTAKE)
        self.assertEqual(decision.response["text"], "Yes, this objective matches my goals.")
        self.assertEqual(classify_chat(ChatQuestion("m2", OBJECTIVE), Intake(None, False, "all", plan="Reimagine")).cls, Class.PARK)

    def test_output_language_is_answered_from_intake(self):
        decision = classify_chat(ChatQuestion("m3", LANGUAGE), INTAKE)
        self.assertEqual(decision.cls, Class.ANSWER_FROM_INTAKE)
        self.assertEqual(decision.response["text"], "English only, no translations.")

    def test_a_proceed_question_at_the_end_of_a_longer_message_is_approve_only(self):
        decision = classify_chat(ChatQuestion("m4", PROCEED), INTAKE)
        self.assertEqual(decision.cls, Class.APPROVE_ONLY)
        self.assertEqual(decision.response["text"], "Yes, proceed with this plan.")

    def test_status_notices_need_no_answer(self):
        self.assertFalse(needs_answer(EXECUTING))
        self.assertFalse(needs_answer("The job is initializing. Please wait until I notify you of successful initialization."))
        self.assertTrue(needs_answer(PLAN_MENU))


class PersonAnswerTests(unittest.TestCase):
    SCHEMA = {"type": "object", "required": ["choice"], "properties": {"choice": {"type": "string", "enum": ["a", "b"]}}}

    def test_an_answer_must_fit_the_tasks_schema(self):
        self.assertTrue(fits_schema(self.SCHEMA, {"choice": "a"}))
        self.assertFalse(fits_schema(self.SCHEMA, {"choice": "c"}))
        self.assertFalse(fits_schema(self.SCHEMA, {}))
        self.assertFalse(fits_schema(self.SCHEMA, {"choice": "a", "extra": 1}))

    def test_booleans_are_not_numbers(self):
        self.assertFalse(fits_schema({"type": "integer"}, True))


if __name__ == "__main__":
    unittest.main()
