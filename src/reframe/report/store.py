"""The published reports in a private S3 bucket, opened with an AWS sign-in (docs/sharing.md, section 4; S-03, S-04).

The store has its own folder, ~/.reframe/reports-store, with the same records a run has: the Terraform root `reports`
with its local state, an intent and receipt for every change, and the teardown consent. Nothing is public: a reader
needs an AWS sign-in that may read the bucket.
"""

from __future__ import annotations

import getpass
import hashlib
import json
import secrets
import string
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import Changes, RunFolder, home, iso
from reframe.core.shell import Aws

ROOT = "reports"


def store_folder() -> RunFolder:
    return RunFolder(home() / "reports-store")


def signed_in(profile: str | None, region: str | None) -> Aws:
    from reframe.core.setup import load_config
    saved = load_config()
    profile = profile or saved.get("profile")
    if not profile:
        raise Stop(Outcome.REFUSED, "no AWS profile: pass --profile, or run reframe setup once to choose and save one")
    return Aws(profile, region or saved.get("region") or "us-east-1")


class Store:
    def __init__(self, aws: Aws, folder: RunFolder | None = None, terraform: str | None = None) -> None:
        from reframe.core.pipeline import terraform_binary
        self.aws, self.folder = aws, folder or store_folder()
        self.changes = Changes(self.folder, f"{getpass.getuser()} (reframe)")
        self.binary = terraform_binary(terraform)

    def terraform(self):
        from reframe.infrastructure.terraform_runner import Terraform
        return Terraform(self.folder, self.aws, self.binary)

    @property
    def bucket(self) -> str | None:
        receipt = self.changes.receipt("terraform-reports-apply")
        return (receipt or {}).get("outputs", {}).get("bucket")

    def ensure(self) -> str:
        """The bucket, created the first time (a plan checked to only create)."""
        if self.bucket:
            return self.bucket
        state = self.folder.state
        name = state.get("bucket_name") or "reframe-reports-" + "".join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(8))
        self.folder.update(bucket_name=name, region=self.aws.region, profile=self.aws.profile, created_at=state.get("created_at") or iso())
        tf = self.terraform()
        tf.install()
        tf.variables(ROOT, {"region": self.aws.region, "bucket_name": name})
        tf.apply(ROOT, self.changes)
        self.folder.event("reports_store_ready")
        return self.bucket

    def upload(self, copy: Path, project: str, run: str) -> str:
        bucket = self.ensure()
        prefix = f"{project}/{run}/"
        digest = hashlib.sha256((copy / "manifest.json").read_bytes()).hexdigest()[:16]
        self.changes.apply(f"upload-{project}-{run}-{digest}", "s3 cp --recursive", {"bucket": bucket, "prefix": prefix, "manifest": digest},
                           lambda: self.aws.write("s3", "cp", str(copy), f"s3://{bucket}/{prefix}", "--recursive", "--sse", "AES256",
                                                  "--only-show-errors", timeout=1800))
        self.folder.event("report_uploaded", project=project, run=run)
        return prefix

    def reports(self) -> list[dict[str, Any]]:
        bucket = self.bucket
        if not bucket:
            return []
        keys = self.aws.read("s3api", "list-objects-v2", "--bucket", bucket, "--query", "Contents[?ends_with(Key, 'manifest.json')].[Key,LastModified]")
        found = []
        for key, modified in keys or []:
            with tempfile.TemporaryDirectory() as scratch:
                target = Path(scratch) / "manifest.json"
                self.aws.read("s3api", "get-object", "--bucket", bucket, "--key", key, str(target))
                manifest = json.loads(target.read_text())
            found.append({"path": key.rsplit("/", 1)[0], "project": manifest.get("project"), "run": manifest.get("run"),
                          "commit": manifest.get("commit"), "published_at": manifest.get("published_at") or modified})
        return sorted(found, key=lambda r: str(r["published_at"]), reverse=True)

    def download(self, path: str) -> Path:
        bucket = self.bucket
        if not bucket:
            raise Stop(Outcome.REFUSED, "no reports have been published to AWS from this computer yet (reframe publish --to aws)")
        target = self.folder.path(f"cache/{path.strip('/')}")
        target.mkdir(parents=True, exist_ok=True)
        self.aws.read("s3", "sync", f"s3://{bucket}/{path.strip('/')}/", str(target), "--only-show-errors", timeout=1800)
        if not (target / "index.html").exists():
            raise Stop(Outcome.REFUSED, f"{path} is not a published report in the bucket; reframe reports lists them")
        return target / "index.html"

    # ---- teardown ------------------------------------------------------------------------------------

    def inventory(self) -> list[dict[str, Any]]:
        if not self.folder.exists(f"terraform/{ROOT}/terraform.tfstate"):
            return []
        return self.terraform().inventory(ROOT)

    def teardown(self, prompt: Callable[[str], str], say: Callable[[str], None]) -> bool:
        items = self.inventory()
        if not items:
            say("There is no reports bucket to remove.\n")
            return False
        bucket = self.bucket
        count = 0
        if bucket:
            listed = self.aws.read("s3api", "list-object-versions", "--bucket", bucket, "--query", "length(Versions || `[]`)")
            count = int(listed or 0)
        say(f"Reframe will delete the reports bucket {bucket} with its {count} stored object versions, and these settings, all created by "
            "Reframe for the published reports:\n\n" + "".join(f"  {n:>2}. {i['type']}  {i.get('name') or i['address']}\n" for n, i in enumerate(items, 1)))
        answer = prompt(f"Type yes to delete the bucket and every report in it, or anything else to keep it: ").strip()
        if answer != "yes":
            say("Nothing was deleted.\n")
            return False
        consents = self.folder.load("teardown/consents.json", [])
        consents.append({"at": iso(), "by": getpass.getuser(), "answer": answer, "resources": items, "objects": count})
        self.folder.save("teardown/consents.json", consents)
        deleted = self.terraform().destroy(ROOT, self.changes)["deleted"]
        say(f"Deleted {len(deleted)} resources, the bucket with its contents among them.\n")
        stamp = iso().replace(":", "")
        for step in ("terraform-reports-apply", "terraform-reports-destroy"):  # archived, so a later publish creates a new bucket
            for kind in ("intent", "receipt"):
                if self.folder.exists(f"changes/{step}.{kind}.json"):
                    self.folder.rename(f"changes/{step}.{kind}.json", f"changes/{step}.{kind}-done-{stamp}.json")
        self.folder.update(torn_down=iso(), bucket_name=None)
        return True


def open_in_browser(path: Path) -> None:
    subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", str(path)], check=False)
