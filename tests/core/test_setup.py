import contextlib
import hashlib
import io
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from reframe.core import guide, setup

MAC = setup.Machine("darwin", "arm64", brew=True, linux_installer=None)
MAC_NO_BREW = setup.Machine("darwin", "amd64", brew=False, linux_installer=None)
UBUNTU = setup.Machine("linux", "amd64", brew=False, linux_installer="apt-get")


class InstallCommandsTest(unittest.TestCase):
    def test_commands_follow_the_operating_system(self):
        self.assertEqual(setup.install_command("aws", MAC), "brew install awscli")
        self.assertIn("AWSCLIV2.pkg", setup.install_command("aws", MAC_NO_BREW))
        self.assertIn("awscli-exe-linux", setup.install_command("aws", UBUNTU))
        self.assertEqual(setup.install_command("git", UBUNTU), "sudo apt-get update && sudo apt-get install -y git")
        self.assertEqual(setup.install_command("uv", MAC), "brew install uv")
        self.assertIn("astral.sh/uv/install.sh", setup.install_command("uv", UBUNTU))
        self.assertEqual(setup.install_command("terraform", UBUNTU), "reframe")
        self.assertIn("awslabs.aws-transform-mcp-server==", setup.install_command("mcp", MAC))
        self.assertEqual(setup.install_command("claude", MAC), "brew install --cask claude-code")
        self.assertIsNone(setup.install_command("terraform", setup.Machine("windows", "amd64", False, None)))


class TerraformInstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = mock.patch.dict(os.environ, {"REFRAME_HOME": self.tmp.name})
        self.env.start()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as z:
            z.writestr("terraform", b"#!/bin/sh\necho Terraform v1.17.2\n")
        self.archive = buffer.getvalue()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def fetcher(self, digest):
        name = f"terraform_{setup.TERRAFORM_VERSION}_linux_amd64.zip"
        urls = []

        def fetch(url, target):
            urls.append(url)
            target.write_bytes(f"{digest}  {name}\n".encode() if url.endswith("SHA256SUMS") else self.archive)
        return fetch, urls

    def test_installed_when_the_sum_matches_and_remembered(self):
        fetch, urls = self.fetcher(hashlib.sha256(self.archive).hexdigest())
        path = setup.install_terraform(UBUNTU, fetch)
        self.assertTrue(path.is_file() and os.access(path, os.X_OK))
        self.assertEqual(setup.load_config()["terraform"], str(path))
        self.assertTrue(all(u.startswith("https://releases.hashicorp.com/terraform/") for u in urls))

    def test_nothing_installed_when_the_sum_differs(self):
        fetch, _ = self.fetcher("0" * 64)
        with self.assertRaises(RuntimeError):
            setup.install_terraform(UBUNTU, fetch)
        self.assertNotIn("terraform", setup.load_config())
        self.assertFalse((Path(self.tmp.name) / "tools").exists())


class ConfigTest(unittest.TestCase):
    def test_saved_and_merged(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.dict(os.environ, {"REFRAME_HOME": tmp}):
            setup.save_config(profile="p", region="us-east-1")
            setup.save_config(region="eu-west-1", terraform=None)
            self.assertEqual(setup.load_config(), {"profile": "p", "region": "eu-west-1"})
            self.assertEqual(oct((Path(tmp) / "config.json").stat().st_mode & 0o777), "0o600")


class PrerequisitesTest(unittest.TestCase):
    def tools(self, uv_ready):
        return [setup.Tool("git", "Git", "any", "2.4", True), setup.Tool("uv", "uv (uvx)", "any", "0.1" if uv_ready else None, uv_ready, install="brew install uv"),
                setup.Tool("mcp", "AWS Transform MCP server", "0.2.4", None, False, install="uvx --from x python -c pass"),
                setup.Tool("claude", "Claude Code", "any", None, False, optional=True, install="brew install --cask claude-code", note="for the Claude assessment")]

    def test_declining_everything_ends_and_names_what_is_missing(self):
        with mock.patch.object(setup, "check", return_value=self.tools(uv_ready=False)), \
                mock.patch("reframe.core.ui.yes", return_value=False) as asked, contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertFalse(guide.prerequisites(MAC))
        self.assertEqual(asked.call_count, 2)  # uv and the optional Claude Code; the MCP server waits for uv
        self.assertIn("Still missing: uv (uvx), AWS Transform MCP server", out.getvalue())

    def test_ready_when_only_the_optional_tool_is_declined(self):
        tools = self.tools(uv_ready=True)
        tools[2].ready = True
        with mock.patch.object(setup, "check", return_value=tools), mock.patch("reframe.core.ui.yes", return_value=False), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertTrue(guide.prerequisites(MAC))
        self.assertIn("Everything a run needs is ready", out.getvalue())

    def test_nothing_runs_without_a_yes(self):
        with mock.patch.object(setup, "check", return_value=self.tools(uv_ready=False)), mock.patch("reframe.core.ui.yes", return_value=False), \
                mock.patch.object(setup, "run_in_terminal") as ran, contextlib.redirect_stdout(io.StringIO()):
            guide.prerequisites(MAC)
        ran.assert_not_called()


if __name__ == "__main__":
    unittest.main()
