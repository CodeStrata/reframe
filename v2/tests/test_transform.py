"""P1-03 (#232), offline part: the AWS Transform MCP client and read-only capability discovery. L1, L2.

L2 runs against a local synthetic MCP server (fixtures/transform_server.py);
nothing contacts AWS. The live read-only discovery waits for the execution
envelope (P1-01).
"""

import os
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from reframe_v2.transform import (
    LIVE_PATH_OPERATIONS,
    MUTATING,
    READ_ONLY,
    Authorization,
    ServerConfig,
    TransformClient,
    TransformError,
    Unauthorized,
    discover,
    unwrap,
)

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "transform_server.py"
NOW = datetime(2026, 11, 18, 12, 0, tzinfo=timezone.utc)


class ConfigTests(unittest.TestCase):
    def test_latest_is_refused_and_an_exact_pin_is_accepted(self):
        with self.assertRaises(TransformError):
            ServerConfig(("uvx", "awslabs.aws-transform-mcp-server@latest"), "p", "us-east-1", Path("/tmp/x"))
        with self.assertRaises(TransformError):
            ServerConfig(("uvx", "awslabs.aws-transform-mcp-server"), "p", "us-east-1", Path("/tmp/x"))
        ServerConfig(("uvx", "awslabs.aws-transform-mcp-server@1.2.3"), "p", "us-east-1", Path("/tmp/x"))
        ServerConfig(("uvx", "awslabs.aws-transform-mcp-server==1.2.3"), "p", "us-east-1", Path("/tmp/x"))

    def test_the_server_gets_only_allowlisted_environment(self):
        config = ServerConfig(("server",), "sample-profile", "us-east-1", Path("/tmp/w"))
        env = config.environment({"HOME": "/h", "PATH": "/p", "AWS_SECRET_ACCESS_KEY": "x", "GITHUB_TOKEN": "y"})
        self.assertEqual(env, {"HOME": "/h", "PATH": "/p", "AWS_REGION": "us-east-1", "AWS_PROFILE": "sample-profile",
                               "AWS_TRANSFORM_MCP_WRITE_DIR": "/tmp/w"})


class UnwrapTests(unittest.TestCase):
    def test_envelopes_are_removed(self):
        self.assertEqual(unwrap({"result": {"success": True, "data": {"a": 1}}}), {"a": 1})
        self.assertEqual(unwrap({"content": [{"type": "text", "text": '{"success": true, "data": {"b": 2}}'}]}), {"b": 2})

    def test_failures_are_refused(self):
        for value in ({"isError": True}, {"success": False}, {"error": "x"}, ["not", "a", "dict"],
                      {"content": [{"type": "text", "text": "not json"}]}):
            with self.subTest(value=value), self.assertRaises(TransformError):
                unwrap(value)


class FixtureServerTests(unittest.TestCase):
    def client(self, drop=""):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.marker = Path(self.tmp.name) / "create-job-called"
        self.chat = Path(self.tmp.name) / "chat-posted"
        self.deleted = Path(self.tmp.name) / "deleted"
        config = ServerConfig((sys.executable, str(FIXTURE)), None, "us-east-1", Path(self.tmp.name) / "artifacts", timeout_seconds=60)
        parent = {"PATH": os.environ.get("PATH", ""), "HOME": os.environ.get("HOME", "")}
        client = TransformClient(config, parent)
        client.env.update({"FIXTURE_DROP": drop, "FIXTURE_MARKER": str(self.marker), "FIXTURE_CHAT": str(self.chat),
                           "FIXTURE_DELETED": str(self.deleted)})
        return client

    def test_discovery_records_every_live_path_operation_and_calls_nothing(self):
        capability = discover(self.client(), NOW)
        self.assertTrue(capability.live_path_supported)
        self.assertEqual(capability.missing, ())
        self.assertEqual(set(capability.available), set(LIVE_PATH_OPERATIONS))
        self.assertEqual(capability.unrecognized, ("reject",))
        self.assertTrue(all(value.startswith("sha256:") for value in capability.tools.values()))
        self.assertFalse(self.marker.exists())
        self.assertFalse(self.deleted.exists())
        self.assertEqual(capability.as_json()["checked_at"], "2026-11-18T12:00:00Z")

    def test_a_missing_operation_is_a_recorded_capability_gap(self):
        capability = discover(self.client(drop="complete_task"), NOW)
        self.assertFalse(capability.live_path_supported)
        self.assertEqual(capability.missing, ("complete_task",))
        self.assertIn("cannot run", capability.notes[0])

    def test_read_only_calls_work_without_authorization(self):
        client = self.client()
        self.assertEqual(client.call("get_job_status", {"workspaceId": "w", "jobId": "j", "detailed": True}), {"status": "IN_PROGRESS"})
        self.assertFalse(self.chat.exists())

    def test_a_status_read_without_detailed_is_refused_before_it_reaches_the_job_chat(self):
        client = self.client()
        for arguments in ({"workspaceId": "w", "jobId": "j"}, {"workspaceId": "w", "jobId": "j", "detailed": False}):
            with self.subTest(arguments=arguments), self.assertRaises(TransformError):
                client.call("get_job_status", arguments)
        self.assertFalse(self.chat.exists())

    def test_create_job_without_an_orchestrator_is_refused_before_dispatch(self):
        client = self.client()
        with self.assertRaises(TransformError):
            client.call("create_job", {"workspaceId": "w", "objective": "o"}, Authorization("envelope-1", "create_job", "Owner"))
        self.assertFalse(self.marker.exists())

    def test_a_mutating_call_without_authorization_is_refused_before_dispatch(self):
        client = self.client()
        with self.assertRaises(Unauthorized):
            client.call("create_job", {"workspaceId": "w", "objective": "o", "orchestratorAgent": "a"})
        with self.assertRaises(Unauthorized):
            client.call("create_job", {"workspaceId": "w", "objective": "o", "orchestratorAgent": "a"},
                        Authorization("envelope-1", "send_message", "Owner"))
        self.assertFalse(self.marker.exists())

    def test_an_authorized_mutating_call_is_sent(self):
        client = self.client()
        result = client.call("create_job", {"workspaceId": "w", "objective": "o", "orchestratorAgent": "a"}, Authorization("envelope-1", "create_job", "Owner"))
        self.assertEqual(result, {"jobId": "job-fixture"})
        self.assertTrue(self.marker.exists())

    def test_a_missing_teardown_operation_is_a_recorded_capability_gap(self):
        capability = discover(self.client(drop="delete_job,delete_workspace"), NOW)
        self.assertFalse(capability.live_path_supported)
        self.assertEqual(capability.missing, ("delete_job", "delete_workspace"))

    def test_every_envelope_operation_that_changes_aws_needs_authorization(self):
        self.assertEqual(MUTATING, {"create_workspace", "create_connector", "accept_connector", "create_job",
                                    "send_message", "complete_task", "delete_job", "delete_workspace"})
        self.assertEqual(set(LIVE_PATH_OPERATIONS), MUTATING | READ_ONLY)

    def test_a_delete_without_authorization_is_refused_before_dispatch(self):
        client = self.client()
        with self.assertRaises(Unauthorized):
            client.call("delete_workspace", {"workspaceId": "w", "confirm": True})
        with self.assertRaises(Unauthorized):
            client.call("delete_job", {"workspaceId": "w", "jobId": "j", "confirm": True},
                        Authorization("envelope-1", "delete_workspace", "Owner"))
        self.assertFalse(self.deleted.exists())

    def test_an_authorized_delete_is_sent(self):
        client = self.client()
        client.call("delete_job", {"workspaceId": "w", "jobId": "j", "confirm": True}, Authorization("envelope-1", "delete_job", "Owner"))
        self.assertTrue(self.deleted.exists())

    def test_an_unclassified_tool_is_never_called(self):
        with self.assertRaises(Unauthorized):
            self.client().call("reject", {"workspaceId": "w"})

    def test_arguments_are_never_guessed(self):
        client = self.client()
        with self.assertRaises(TransformError):
            client.call("get_job_status", {"workspaceId": "w", "detailed": True})
        with self.assertRaises(TransformError):
            client.call("get_job_status", {"workspaceId": "w", "jobId": "j", "detailed": True, "extra": "x"})


if __name__ == "__main__":
    unittest.main()
