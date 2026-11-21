"""P1-05 (#234): the live job driver and reframe run, offline (L1). Polling every 60 seconds from #263.

AWS is a scripted stand-in that follows the order and wording recorded live on 20 November 2026 (P1 stage D):
the plan menu, the objective, the output language, the proceed question, then the source-location form
as AWS declared it, a non-blocking collaborators form, the function selection in chat beside the catalog
review form, and a spec_gen archive laid out as v1's live job delivered it (17 November 2026). No job,
task, account or workspace identifier from a real run appears here.
"""

import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace

from reframe_v2.aws_reviews import Intake
from reframe_v2.job import ENVELOPE, LIMITS, ORCHESTRATOR_AGENT, POLL_SECONDS, JobDriver, Outcome, ProjectFolder, Settings, job_status
from reframe_v2.transform import NotSent, Rejected, TransformError
from tests.test_aws_reviews import EXECUTING, LANGUAGE, OBJECTIVE, PLAN_MENU, PROCEED

FUNCTION = "Account and Customer Profile Administration"
SELECT = "Please select the business function(s) to Re-Imagine before continuing."
SOURCE_URI = "s3://sample-bucket/reframe/source/0123456789abcdef.zip"
LIVE_SOURCE_SCHEMA = {"type": "object", "additionalProperties": True, "required": ["assetLocation"], "displayOnly": False,
                      "properties": {"assetLocation": {"type": "string"}, "enableFeatures": {"type": "array", "items": {"type": "string"}},
                                     "isDownloadButtonClicked": {"type": "boolean"}, "optInChatBox": {"type": "boolean"}}}


def spec_archive(members=None):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as bundle:
        for name, data in (members or {
            f"spec/Accounts/{FUNCTION}/requirements.md": b"# Requirements\n\nREQ-1 The system keeps the customer profile.\n",
            f"spec/Accounts/{FUNCTION}/traceability.yaml": b"summary: {}\nrules: []\nrequirements:\n- req_id: REQ-1\n  rule_ids: []\n",
            "spec/coverage.md": b"coverage\n",
        }).items():
            bundle.writestr(name, data)
    return buffer.getvalue()


class FakeAWS:
    """Answers the adapter's session() as AWS and the pinned server did live; records every call."""

    def __init__(self, write_dir: Path, clock):
        self.config = SimpleNamespace(write_dir=write_dir)
        self.clock = clock
        self.calls, self.replies, self.completed = [], [], []
        self.job = None
        self.status = "EXECUTING"
        self.messages, self.tasks = [], []
        self.stage = 0
        self.archive = spec_archive()
        self.asset_root = "transform-output/{job}/"
        self.catalog_names_function = True
        self.refuse_chat = False
        self.fail_reads = False
        self.unknown_question = None

    # The conversation, in the live order. Each reply moves AWS to its next turn.
    def _say(self, text, origin="SYSTEM"):
        self.stage += 1
        self.messages.append({"messageId": f"m{len(self.messages) + 1}", "messageOrigin": origin, "text": text,
                              "createdAt": f"2026-11-20T15:{len(self.messages):02d}:00Z",
                              "processingInfo": {"messageType": "FINAL_RESPONSE"} if origin == "SYSTEM" else {}})

    def session(self, calls):
        results = []
        for name, arguments, authorization in calls:
            self.calls.append((name, arguments, authorization))
            results.append(self._one(name, arguments, authorization))
        return results

    def _one(self, name, arguments, authorization):
        if self.fail_reads and authorization is None:
            raise NotSent("the MCP transport failed before any change was sent (the token has expired)")
        if name == "create_job":
            assert authorization.envelope == ENVELOPE and arguments["orchestratorAgent"] == ORCHESTRATOR_AGENT
            self.job = "job-1"
            self._say("The job is initializing. Please wait until I notify you of successful initialization.")
            self._say(self.unknown_question or PLAN_MENU)
            return {"job": {"jobId": self.job}}
        if name == "get_job_status":
            assert arguments["detailed"] is True
            return {"job": {"job": {"jobId": self.job, "statusDetails": {"status": self.status}}},
                    "messages": {"messages": list(self.messages)}, "tasks": {"hitlTasks": [dict(t) for t in self.tasks]},
                    "plan": {"steps": [{"stepName": "Kickoff", "status": "IN_PROGRESS"}]} if self.stage >= 4 else {"steps": []}}
        if name == "send_message":
            if self.refuse_chat:
                raise Rejected("send_message", "REQUEST_FAILED: HTTP 409: The job's agent is stopping and cannot chat right now.")
            self.replies.append(arguments["text"])
            self.messages.append({"messageId": f"u{len(self.messages) + 1}", "messageOrigin": "USER", "text": arguments["text"],
                                  "createdAt": f"2026-11-20T15:{len(self.messages):02d}:30Z"})
            last = [m["text"] for m in self.messages if m["messageOrigin"] == "SYSTEM"][-1]
            if last == PLAN_MENU:
                self._say(OBJECTIVE)
            elif last == OBJECTIVE:
                self._say(LANGUAGE)
            elif last == LANGUAGE:
                self._say(PROCEED)
            elif last == PROCEED:
                self._say(EXECUTING)
                self.tasks = [
                    {"taskId": "t-source", "status": "AWAITING_HUMAN_INPUT", "title": "Specify resource location",
                     "uxComponentId": "SpecifyAssetsLocation", "blockingType": "BLOCKING"},
                    {"taskId": "t-collab", "status": "AWAITING_HUMAN_INPUT", "title": "Add collaborators",
                     "uxComponentId": "InviteCollaboratorsContent", "blockingType": "NON_BLOCKING"}]
            elif last == SELECT:
                self.tasks = []
                self.status = "COMPLETED"
            return {}
        if name == "complete_task":
            self.completed.append((arguments["taskId"], json.loads(arguments["content"])))
            if arguments["taskId"] == "t-source":
                self.tasks = [{"taskId": "t-review", "status": "AWAITING_HUMAN_INPUT", "title": "Review business functions discovery results",
                               "uxComponentId": "MainframeAssessmentBusinessProcessDiscoveryComponent", "blockingType": "BLOCKING"}]
                self._say(SELECT)
            return {}
        if name == "get_resource" and arguments["resource"] == "task":
            schemas = {"t-source": LIVE_SOURCE_SCHEMA,
                       "t-collab": {"type": "object", "required": ["collaborators"], "properties": {"collaborators": {"type": "array"}}},
                       "t-review": {"type": "object", "required": ["selection"], "properties": {"selection": {"type": "string"}}}}
            body = {"taskId": arguments["taskId"], "_outputSchema": schemas[arguments["taskId"]]}
            if arguments["taskId"] == "t-review":
                names = [FUNCTION if self.catalog_names_function else "Account Administration", "Bill Payment"]
                body["description"] = "Business functions found:\n" + "\n".join(f"- {n}" for n in names)
            return {"task": body}
        if name == "list_resources":
            root = self.asset_root.format(job=self.job)
            if "pathPrefix" not in arguments:
                return {"assets": [], "artifacts": [], "folders": [root + "spec_gen/"], "connectorId": "c-1"}
            return {"assets": [{"assetKey": root + "spec_gen/spec_gen_specs_20261120.zip"}], "folders": [], "connectorId": "c-1"}
        if name == "get_resource" and arguments["resource"] == "asset":
            target = Path(arguments["savePath"]) / arguments["fileName"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(self.archive)
            return {"assetKey": arguments["assetKey"], "savedTo": str(target), "sizeBytes": len(self.archive)}
        raise AssertionError(f"unexpected call {name} {arguments}")

    def sent(self, name):
        return [arguments for called, arguments, _ in self.calls if called == name]


class Clock:
    def __init__(self):
        self.now = 1_800_000_000.0
        self.polls = []

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class DriverTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "project"
        self.clock = Clock()
        self.aws = FakeAWS(self.root / "server-write-dir", self.clock)

    def settings(self, **changes):
        values = dict(workspace_id="w-1", source_uri=SOURCE_URI, source_sha256="sha256:" + "0123456789abcdef" * 4,
                      snapshot_id="snapshot:0123456789abcdef", commit="59cc6c2", by="tester (reframe run)",
                      intake=Intake(SOURCE_URI, True, "list", (FUNCTION,)))
        values.update(changes)
        return Settings(**values)

    def driver(self, **changes):
        return JobDriver(self.aws, ProjectFolder(self.root), self.settings(**changes), clock=self.clock, sleep=self.clock.sleep)

    def poll_times(self):
        events = [json.loads(line) for line in (self.root / "events.jsonl").read_text().splitlines()]
        return [e["at"] for e in events if e["event"] == "poll"]

    def test_a_job_runs_from_creation_to_retrieved_requirements_with_no_person(self):
        result = self.driver().run()
        self.assertEqual(result.outcome, Outcome.RETRIEVED, result.message)
        self.assertEqual(len(self.aws.sent("create_job")), 1)
        menu_reply, *rest = self.aws.replies
        self.assertTrue(menu_reply.startswith("1. Assess and reimagine."))
        self.assertIn("English only", menu_reply)
        self.assertEqual(rest, ["Yes, this objective matches my goals.", "English only, no translations.", "Yes, proceed with this plan.",
                                FUNCTION])
        self.assertEqual(self.aws.completed, [("t-source", {"assetLocation": SOURCE_URI})])
        stored = json.loads((self.root / "outputs/requirements.json").read_text())
        self.assertEqual(stored["status"], "NOT_CHECKED")
        self.assertEqual(stored["functions"], [FUNCTION])
        self.assertEqual(sorted(f["kind"] for f in stored["files"]), ["requirements", "traceability"])
        for item in stored["files"]:
            data = (self.root / item["stored"]).read_bytes()
            self.assertEqual(item["sha256"].split(":")[0], "sha256")
            self.assertTrue(item["original_path"].endswith(f"{FUNCTION}/{Path(item['original_path']).name}"))
            self.assertIn(b"REQ-1", data)
        self.assertEqual(stored["snapshot"], self.settings().source_sha256)
        self.assertFalse(any((self.root / "server-write-dir" / "downloads").iterdir()))

    def test_polls_are_at_least_60_seconds_apart_from_creation(self):
        self.driver().run()
        times = [__import__("calendar").timegm(__import__("time").strptime(t, "%Y-%m-%dT%H:%M:%SZ")) for t in self.poll_times()]
        self.assertGreater(len(times), 5)
        self.assertTrue(all(b - a >= POLL_SECONDS for a, b in zip(times, times[1:])))
        self.assertTrue(all(b - a <= POLL_SECONDS for a, b in zip(times, times[1:])), "each question is answered within one interval")

    def test_every_change_has_an_intent_and_a_receipt_under_the_envelope(self):
        self.driver().run()
        changes = self.root / "changes"
        intents = sorted(p.name[:-len(".intent.json")] for p in changes.glob("*.intent.json"))
        receipts = sorted(p.name[:-len(".receipt.json")] for p in changes.glob("*.receipt.json"))
        self.assertEqual(intents, receipts)
        for path in changes.glob("*.intent.json"):
            self.assertEqual(json.loads(path.read_text())["envelope"], ENVELOPE)
        self.assertEqual(oct((self.root / "job.json").stat().st_mode & 0o777), "0o600")
        self.assertEqual(oct(self.root.stat().st_mode & 0o777), "0o700")

    def test_rerunning_after_retrieval_resumes_and_calls_nothing(self):
        self.driver().run()
        before = len(self.aws.calls)
        self.assertEqual(self.driver().run().outcome, Outcome.RETRIEVED)
        self.assertEqual(len(self.aws.calls), before)

    def test_an_interrupted_run_resumes_the_same_job_and_never_creates_a_second(self):
        self.aws.refuse_chat = True
        self.assertEqual(self.driver().run().outcome, Outcome.REFUSED)
        self.aws.refuse_chat = False
        self.driver().run()
        self.assertEqual(len(self.aws.sent("create_job")), 1)

    def test_an_intent_without_a_receipt_is_uncertain_and_nothing_is_sent(self):
        folder = ProjectFolder(self.root)
        folder.save("changes/create-job.intent.json", {"operation": "create_job"})
        result = self.driver().run()
        self.assertEqual(result.outcome, Outcome.UNCERTAIN)
        self.assertEqual(self.aws.calls, [])
        self.assertEqual(self.driver().run().outcome, Outcome.UNCERTAIN)

    def test_a_changed_snapshot_or_scope_is_refused_without_new_assessment(self):
        self.driver().run()
        before = len(self.aws.calls)
        self.assertEqual(self.driver(source_sha256="sha256:" + "f" * 64).run().outcome, Outcome.REFUSED)
        self.assertEqual(self.driver(intake=Intake(SOURCE_URI, True, "list", ("Bill Payment",))).run().outcome, Outcome.REFUSED)
        self.assertEqual(self.driver().run(new_assessment=True).outcome, Outcome.REFUSED)
        self.assertEqual(len(self.aws.calls), before)

    def test_a_refused_reply_keeps_awss_reason_and_is_never_resent(self):
        self.aws.refuse_chat = True
        result = self.driver().run()
        self.assertEqual(result.outcome, Outcome.REFUSED)
        self.assertIn("409", result.message)
        rejected = list((self.root / "changes").glob("*.rejected.json"))
        self.assertEqual(len(rejected), 1)
        self.assertIn("agent is stopping", json.loads(rejected[0].read_text())["reason"])
        attempts = len(self.aws.sent("send_message"))
        self.assertEqual(self.driver().run().outcome, Outcome.REFUSED)
        self.assertEqual(len(self.aws.sent("send_message")), attempts)

    def test_an_unrecognized_question_parks_and_nothing_is_sent(self):
        self.aws.unknown_question = "Which database should the target application use?"
        result = self.driver().run()
        self.assertEqual(result.outcome, Outcome.WAITING_HUMAN)
        self.assertIn("console", result.message)
        self.assertEqual(self.aws.sent("send_message"), [])

    def test_a_function_aws_does_not_name_exactly_parks(self):
        self.aws.catalog_names_function = False
        result = self.driver().run()
        self.assertEqual(result.outcome, Outcome.WAITING_HUMAN)
        self.assertNotIn(FUNCTION, self.aws.replies)

    def test_under_ask_every_approval_parks(self):
        result = self.driver(intake=Intake(SOURCE_URI, True, "list", (FUNCTION,), aws_reviews="ask")).run()
        self.assertEqual(result.outcome, Outcome.WAITING_HUMAN)
        self.assertNotIn("Yes, proceed with this plan.", self.aws.replies)

    def test_the_job_limit_parks_without_stopping_the_job(self):
        self.aws.unknown_question = None
        driver = self.driver(job_limit_seconds=120)
        original = self.aws._one

        def stall(name, arguments, authorization):
            if name == "send_message":
                return {}
            return original(name, arguments, authorization)
        self.aws._one = stall
        self.aws.messages = []
        result = driver.run()
        self.assertEqual(result.outcome, Outcome.WAITING_HUMAN)
        self.assertIn("8-hour limit", result.message)
        self.assertFalse(any(name == "control_job" for name, _, _ in self.aws.calls))

    def test_an_expired_sign_in_waits_externally_and_retries_nothing(self):
        driver = self.driver()
        driver.state.update(job_id="job-1", workspace_id="w-1", created_at=self.clock(), counts={"create_job": 1},
                            source={"snapshot": self.settings().source_sha256, "snapshot_id": "snapshot:0123456789abcdef", "uri": SOURCE_URI,
                                    "commit": "59cc6c2", "scope": [FUNCTION], "scope mode": "list"})
        self.aws.job = "job-1"
        self.aws.fail_reads = True
        result = driver.run()
        self.assertEqual(result.outcome, Outcome.WAITING_EXTERNAL)
        self.assertEqual(len(self.aws.calls), 1)

    def test_an_archive_with_an_unsafe_path_is_refused(self):
        self.aws.archive = spec_archive({"../requirements.md": b"x"})
        result = self.driver().run()
        self.assertEqual(result.outcome, Outcome.REFUSED)
        self.assertFalse((self.root / "outputs" / "requirements.json").exists())

    def test_an_output_outside_the_jobs_folders_is_refused(self):
        self.aws.asset_root = "transform-output/another-job/"
        self.assertEqual(self.driver().run().outcome, Outcome.REFUSED)

    def test_limits_are_the_envelopes(self):
        self.assertEqual(LIMITS, {"create_job": 1, "send_message": 15, "complete_task": 15})

    def test_the_status_comes_from_the_job_record_not_the_servers_guidance(self):
        snapshot = {"job": {"job": {"statusDetails": {"status": "EXECUTING"}}}, "_pollingGuidance": {"jobStatus": "UNKNOWN"}}
        self.assertEqual(job_status(snapshot), "EXECUTING")


class SourceCopyTests(unittest.TestCase):
    def setUp(self):
        from reframe_v2.resources_file import Resources

        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.folder = ProjectFolder(Path(self.tmp.name) / "p")
        self.resources = Resources("111122223333", "us-east-1", "state", ("reframe/",), "bucket", ("reframe/",), "role", "w-1", None,
                                   "c-1", "stack")
        self.archive = b"PK-sample"
        import hashlib

        self.digest = "sha256:" + hashlib.sha256(self.archive).hexdigest()

    def writer(self, head=None, put_ok=True):
        from reframe_v2.source_copy import CopyUncertain

        calls = []

        class Writer:
            def head(_, bucket, key, owner):
                calls.append(("head", key))
                return head

            def put(_, bucket, key, owner, data, digest_hex):
                calls.append(("put", key))
                if not put_ok:
                    raise CopyUncertain("put-object failed after it was sent")
                return {"VersionId": "v1"}
        return Writer(), calls

    def test_the_archive_is_written_once_under_the_declared_prefix(self):
        from reframe_v2.source_copy import ensure_copy

        writer, calls = self.writer()
        copy = ensure_copy(writer, self.resources, self.archive, self.digest, self.folder)
        self.assertTrue(copy.key.startswith("reframe/source/"))
        self.assertEqual([c[0] for c in calls], ["head", "put"])
        again = ensure_copy(writer, self.resources, self.archive, self.digest, self.folder)
        self.assertTrue(again.reused)
        self.assertEqual([c[0] for c in calls], ["head", "put"])

    def test_a_copy_already_in_s3_with_the_same_bytes_is_reused(self):
        from reframe_v2.source_copy import ensure_copy

        writer, calls = self.writer(head={"Metadata": {"reframe-sha256": self.digest.split(":")[1]}, "VersionId": "v0"})
        self.assertTrue(ensure_copy(writer, self.resources, self.archive, self.digest, self.folder).reused)
        self.assertEqual([c[0] for c in calls], ["head"])

    def test_different_content_at_the_key_is_never_overwritten(self):
        from reframe_v2.source_copy import CopyError, ensure_copy

        writer, calls = self.writer(head={"Metadata": {"reframe-sha256": "0" * 64}})
        with self.assertRaises(CopyError):
            ensure_copy(writer, self.resources, self.archive, self.digest, self.folder)
        self.assertNotIn("put", [c[0] for c in calls])

    def test_an_uncertain_write_is_never_resent_automatically(self):
        from reframe_v2.source_copy import CopyUncertain, ensure_copy

        writer, calls = self.writer(put_ok=False)
        with self.assertRaises(CopyUncertain):
            ensure_copy(writer, self.resources, self.archive, self.digest, self.folder)
        with self.assertRaises(CopyUncertain):
            ensure_copy(self.writer()[0], self.resources, self.archive, self.digest, self.folder)

    def test_an_uncertain_write_is_settled_when_s3_holds_the_same_bytes(self):
        from reframe_v2.source_copy import ensure_copy

        self.folder.save("changes/source-copy.intent.json", {"operation": "s3 put-object"})
        writer, calls = self.writer(head={"ChecksumSHA256": __import__("base64").b64encode(bytes.fromhex(self.digest[7:])).decode()})
        self.assertTrue(ensure_copy(writer, self.resources, self.archive, self.digest, self.folder).reused)
        self.assertEqual(self.folder.load("changes/source-copy.receipt.json")["settled_from"], "head-object")


class RunCommandTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        from tests.model_samples import SAMPLES

        policy = dict(SAMPLES["project_policy"], aws={"account": "111122223333", "region": "us-east-1", "profile": None})
        (base / "policy.json").write_text(json.dumps(policy))
        (base / "resources.json").write_text(json.dumps({
            "schema": "resources_file/1", "account": "111122223333", "region": "us-east-1",
            "state_bucket": {"name": "state", "write_prefixes": ["reframe/"]},
            "bucket": {"name": "bucket", "write_prefixes": ["reframe/"]}, "sandbox_role": {"name": "role"},
            "transform": {"workspace_id": "w-1", "assessment_connector": None, "reimagine_connector": "c-1"},
            "neptune_stack": {"name": "stack"}}))
        self.base = base

    def args(self, **changes):
        values = dict(repo=self.base / "repo", profile="p", region="us-east-1", policy=self.base / "policy.json",
                      resources=self.base / "resources.json", scope=None, new_assessment=False, foreground=True)
        values.update(changes)
        return SimpleNamespace(**values)

    def run_command(self, args, **kwargs):
        from reframe_v2.run_command import run

        out, err = io.StringIO(), io.StringIO()
        code = run(args, environment={"REFRAME_HOME": str(self.base / "home")}, out=out, err=err, **kwargs)
        return code, out.getvalue(), err.getvalue()

    def test_the_command_is_wired_with_the_specifications_arguments(self):
        from reframe_v2.cli import build_parser

        parsed = build_parser().parse_args(["run", "--repo", "r", "--profile", "p", "--region", "us-east-1", "--policy", "x",
                                            "--resources", "y", "--foreground"])
        self.assertEqual((parsed.command, parsed.foreground, parsed.new_assessment), ("run", True, False))

    def test_a_region_that_differs_from_the_resources_file_is_refused(self):
        code, _, err = self.run_command(self.args(region="eu-west-1"))
        self.assertEqual(code, 3)
        self.assertIn("region", err)

    def test_a_checkout_with_local_changes_is_refused(self):
        import subprocess

        repo = self.base / "repo"
        repo.mkdir()
        for command in (["git", "init", "-q"], ["git", "-c", "user.name=t", "-c", "user.email=t@example.invalid", "commit", "-q",
                                                      "--allow-empty", "-m", "start"]):
            subprocess.run(command, cwd=repo, check=True)
        (repo / "PROG.cbl").write_text("       IDENTIFICATION DIVISION.\n")
        code, _, err = self.run_command(self.args())
        self.assertEqual(code, 3)
        self.assertIn("local changes", err)

    def test_without_foreground_the_run_continues_in_the_background(self):
        launched = []
        code, out, _ = self.run_command(self.args(foreground=False), launch=lambda argv, log: launched.append(argv))
        self.assertEqual(code, 0)
        self.assertIn("--foreground", launched[0])
        self.assertIn("background", out)


if __name__ == "__main__":
    unittest.main()
