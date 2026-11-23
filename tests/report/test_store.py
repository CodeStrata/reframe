import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from reframe.report.store import Store


class FakeAws:
    profile, region = "p", "us-east-1"

    def __init__(self):
        self.calls, self.objects = [], {}

    def write(self, *args, timeout=0):
        self.calls.append(args)
        if args[:2] == ("s3", "cp"):
            source, target = Path(args[2]), args[3]
            for f in source.rglob("*"):
                if f.is_file():
                    self.objects[target.removeprefix("s3://").split("/", 1)[1] + str(f.relative_to(source))] = f.read_bytes()
        return {}

    def read(self, *args, timeout=0):
        self.calls.append(args)
        if args[:2] == ("s3api", "list-objects-v2"):
            return [[k, "2026-11-23T00:00:00Z"] for k in self.objects if k.endswith("manifest.json")]
        if args[:2] == ("s3api", "get-object"):
            Path(args[-1]).write_bytes(self.objects[args[args.index("--key") + 1]])
            return {}
        if args[:2] == ("s3api", "list-object-versions"):
            return len(self.objects)
        if args[:2] == ("s3", "sync"):
            prefix, target = args[2].removeprefix("s3://").split("/", 1)[1], Path(args[3])
            for k, v in self.objects.items():
                if k.startswith(prefix):
                    (target / k[len(prefix):]).parent.mkdir(parents=True, exist_ok=True)
                    (target / k[len(prefix):]).write_bytes(v)
            return {}
        raise AssertionError(args)


class FakeTerraform:
    applied, destroyed = [], []

    def __init__(self, store):
        self.store = store

    def install(self):
        pass

    def variables(self, root, values):
        self.store.folder.save(f"terraform/{root}/reframe.auto.tfvars.json", values)

    def apply(self, root, changes, backend=None):
        name = self.store.folder.load(f"terraform/{root}/reframe.auto.tfvars.json")["bucket_name"]
        FakeTerraform.applied.append(name)
        return changes.apply("terraform-reports-apply", "terraform apply", {}, lambda: {"created": ["aws_s3_bucket.reports"], "outputs": {"bucket": name}})

    def inventory(self, root, backend=None):
        return [{"root": root, "address": "aws_s3_bucket.reports", "type": "aws_s3_bucket", "name": self.store.bucket, "id": self.store.bucket}]

    def destroy(self, root, changes, backend=None):
        FakeTerraform.destroyed.append(root)
        return changes.apply("terraform-reports-destroy", "terraform destroy", {}, lambda: {"deleted": ["aws_s3_bucket.reports"]})


class StoreTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        self.aws = FakeAws()
        self.store = Store(self.aws, terraform="terraform")
        self.store.terraform = lambda: FakeTerraform(self.store)
        FakeTerraform.applied, FakeTerraform.destroyed = [], []

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def copy(self, run):
        folder = Path(self.tmp.name) / f"copy-{run}"
        (folder / "aws").mkdir(parents=True)
        (folder / "index.html").write_text("<h1>index</h1>")
        (folder / "aws" / "index.html").write_text("aws")
        (folder / "manifest.json").write_text(json.dumps({"project": "demo", "run": run, "commit": "c" * 40, "published_at": "2026-11-23"}))
        return folder

    def test_publish_list_open(self):
        prefix = self.store.upload(self.copy("abc123"), "demo", "abc123")
        self.assertEqual(prefix, "demo/abc123/")
        self.store.upload(self.copy("def456"), "demo", "def456")
        self.assertEqual(len(FakeTerraform.applied), 1)  # one bucket, made once
        self.assertRegex(FakeTerraform.applied[0], r"^reframe-reports-[a-z0-9]{8}$")
        cp = next(c for c in self.aws.calls if c[:2] == ("s3", "cp"))
        self.assertIn("--sse", cp)
        self.assertEqual(sorted(r["run"] for r in self.store.reports()), ["abc123", "def456"])
        page = self.store.download("demo/abc123")
        self.assertEqual(page.read_text(), "<h1>index</h1>")

    def test_teardown_needs_yes_and_a_new_publish_makes_a_new_bucket(self):
        self.store.upload(self.copy("abc123"), "demo", "abc123")
        state = self.store.folder.path(f"terraform/reports/terraform.tfstate")
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text("{}")
        said = []
        self.assertFalse(self.store.teardown(lambda q: "no", said.append))
        self.assertEqual(FakeTerraform.destroyed, [])
        self.assertTrue(self.store.teardown(lambda q: "yes", said.append))
        self.assertEqual(FakeTerraform.destroyed, ["reports"])
        self.assertIsNone(self.store.bucket)
        self.assertEqual(len(self.store.folder.load("teardown/consents.json")), 1)
        self.store.upload(self.copy("def456"), "demo", "def456")
        self.assertEqual(len(FakeTerraform.applied), 2)
        self.assertNotEqual(FakeTerraform.applied[0], FakeTerraform.applied[1])


if __name__ == "__main__":
    unittest.main()


class PlanCheckTest(unittest.TestCase):
    def plan(self, *changes):
        return {"resource_changes": [{"mode": "managed", "address": a, "change": {"actions": acts}} for a, acts in changes]}

    def test_named_updates_only(self):
        from reframe.core.errors import Stop
        from reframe.infrastructure.terraform_runner import only_creates
        from reframe.report.store import SITE_UPDATES
        plan = self.plan(("aws_cloudfront_distribution.site[0]", ["create"]), ("aws_s3_bucket_policy.reports", ["update"]),
                         ("terraform_data.callback[0]", ["delete", "create"]))
        self.assertEqual(only_creates(plan, SITE_UPDATES), ["aws_cloudfront_distribution.site[0]", "terraform_data.callback[0]"])
        with self.assertRaises(Stop):
            only_creates(self.plan(("aws_s3_bucket.reports", ["update"])), SITE_UPDATES)
        with self.assertRaises(Stop):
            only_creates(self.plan(("aws_s3_bucket_policy.reports", ["update"])))
