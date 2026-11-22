import json
import tempfile
import unittest

from reframe.infrastructure import terraform_runner as terraform
from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import Changes, new_run
from reframe.core.shell import Aws, Result

from tests.fakes import FakeRunner

CREDENTIALS = {"AccessKeyId": "AKIAEXAMPLE", "SecretAccessKey": "secret", "SessionToken": "token"}


def plan(*changes):
    return {"resource_changes": [{"address": a, "mode": "managed", "change": {"actions": list(acts)}} for a, acts in changes]
            + [{"address": "data.aws_caller_identity.current", "mode": "data", "change": {"actions": ["read"]}}]}


class PlanCheckTest(unittest.TestCase):
    def test_only_creates(self):
        self.assertEqual(terraform.only_creates(plan(("a", ["create"]), ("b", ["no-op"]))), ["a"])
        with self.assertRaises(Stop) as stop:
            terraform.only_creates(plan(("a", ["create"]), ("b", ["delete", "create"])))
        self.assertEqual(stop.exception.outcome, Outcome.REFUSED)

    def test_only_deletes_what_the_run_created(self):
        self.assertEqual(terraform.only_deletes(plan(("a", ["delete"])), {"a"}), ["a"])
        with self.assertRaises(Stop):
            terraform.only_deletes(plan(("a", ["delete"]), ("other", ["delete"])), {"a"})
        with self.assertRaises(Stop):
            terraform.only_deletes(plan(("a", ["update"])), {"a"})

    def test_names_fit_aws_limits(self):
        n = terraform.names("a" * 30, "abc123")
        self.assertLessEqual(len(n["bucket"]), 63)
        self.assertLessEqual(len(n["state_bucket"]), 63)


class ApplyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = {"REFRAME_HOME": self.tmp.name}
        import os
        self.old = os.environ.get("REFRAME_HOME")
        os.environ["REFRAME_HOME"] = self.tmp.name
        self.folder = new_run("demo", self.env)

    def tearDown(self):
        import os
        if self.old is None:
            os.environ.pop("REFRAME_HOME", None)
        else:
            os.environ["REFRAME_HOME"] = self.old
        self.tmp.cleanup()

    def fake(self, plans):
        plans = iter(plans)
        fake = FakeRunner().add(["aws", "configure", "export-credentials"], 0, CREDENTIALS)
        fake.add(["terraform"], 0, "")  # replaced per call below
        fake.script.pop()

        def tf(argv, env, data):
            command = argv[2]
            if command == "show":
                return Result(0, json.dumps(next(plans)), "")
            if command == "output":
                return Result(0, json.dumps({"bucket": {"value": "reframe-demo-x-src"}}), "")
            return Result(0, "", "")
        fake.script.append((("terraform",), tf))
        return fake

    def test_apply_records_created_and_outputs(self):
        fake = self.fake([plan(("module.repo.aws_s3_bucket.source", ["create"]))])
        tf = terraform.Terraform(self.folder, Aws("p", "us-east-1", fake), "terraform", fake)
        tf.install()
        receipt = tf.apply("project", Changes(self.folder, "t"), {"bucket": "s", "key": "k", "region": "us-east-1"})
        self.assertEqual(receipt["created"], ["module.repo.aws_s3_bucket.source"])
        self.assertEqual(receipt["outputs"]["bucket"], "reframe-demo-x-src")
        applied = fake.ran("terraform", f"-chdir={tf.base / 'project'}", "apply")
        self.assertEqual(len(applied), 1)
        env = fake.calls[-1][1]
        self.assertEqual(env["AWS_SESSION_TOKEN"], "token")
        self.assertNotIn("AWS_PROFILE", env)
        self.assertTrue((tf.base / "modules" / "neptune_graph" / "main.tf").exists())

    def test_refused_plan_is_not_applied(self):
        fake = self.fake([plan(("module.repo.aws_s3_bucket.source", ["update"]))])
        tf = terraform.Terraform(self.folder, Aws("p", "us-east-1", fake), "terraform", fake)
        tf.install()
        with self.assertRaises(Stop):
            tf.apply("project", Changes(self.folder, "t"))
        self.assertEqual(fake.ran("terraform", f"-chdir={tf.base / 'project'}", "apply"), [])

    def test_destroy_after_apply(self):
        fake = self.fake([plan(("a", ["create"])), plan(("a", ["delete"]))])
        tf = terraform.Terraform(self.folder, Aws("p", "us-east-1", fake), "terraform", fake)
        tf.install()
        changes = Changes(self.folder, "t")
        tf.apply("bootstrap", changes)
        self.assertEqual(tf.destroy("bootstrap", changes)["deleted"], ["a"])


if __name__ == "__main__":
    unittest.main()
