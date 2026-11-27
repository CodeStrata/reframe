"""The AWS Transform client: a server that starts "not configured" is started again (the second test codebase, 26 November 2026)."""
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from reframe.core.errors import Rejected
from reframe.transform.client import ServerConfig, TransformClient


class RetryTest(unittest.TestCase):
    def client(self):
        tmp = tempfile.mkdtemp()
        c = TransformClient(ServerConfig("p", "us-east-1", Path(tmp)))
        c.sleep = mock.Mock()
        return c

    def test_not_configured_at_start_is_tried_again(self):
        c = self.client()
        failed = Rejected("load_instructions", "NOT_CONFIGURED: Not connected to AWS Transform.")
        with mock.patch.object(c, "_session_once", side_effect=[failed, failed, ["ok"]]) as once:
            self.assertEqual(c.session([("get_job_status", {"workspaceId": "w", "jobId": "j", "detailed": True})]), ["ok"])
        self.assertEqual(once.call_count, 3)
        self.assertEqual([call.args[0] for call in c.sleep.call_args_list], [5, 15])

    def test_it_gives_up_after_the_waits_and_other_refusals_are_not_retried(self):
        c = self.client()
        failed = Rejected("load_instructions", "NOT_CONFIGURED: Not connected to AWS Transform.")
        with mock.patch.object(c, "_session_once", side_effect=[failed] * 4), self.assertRaises(Rejected):
            c.session([])
        self.assertEqual(c.sleep.call_count, 3)
        other = Rejected("get_job_status", "AccessDenied")
        with mock.patch.object(c, "_session_once", side_effect=[other]) as once, self.assertRaises(Rejected):
            c.session([])
        self.assertEqual(once.call_count, 1)


if __name__ == "__main__":
    unittest.main()
