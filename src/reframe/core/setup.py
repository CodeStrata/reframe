"""The guided setup: prerequisites, installed only on a yes, and the AWS sign-in (specification section 3).

What a run needs is checked as one table. A missing tool is named with the install command for this operating system,
from a fixed list below, and the command runs in the person's terminal only after they say yes. Terraform is installed
by Reframe: the pinned HashiCorp release, checked against HashiCorp's SHA-256 sums, kept in ~/.reframe/tools. Paths and
the chosen profile are saved in ~/.reframe/config.json; no shell file or PATH outside Reframe is changed.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from reframe.core.preflight import MCP_SERVER, MINIMUM_TERRAFORM, terraform_version
from reframe.core.runfolder import home
from reframe.core.shell import base_environment

TERRAFORM_VERSION = "1.17.2"
TERRAFORM_RELEASES = "https://releases.hashicorp.com/terraform"
USER_BINS = ("~/.local/bin", "~/.cargo/bin", "/opt/homebrew/bin", "/usr/local/bin")  # where uv, brew and the AWS CLI install


# ---- saved settings ------------------------------------------------------------------------------


def config_path() -> Path:
    return home() / "config.json"


def load_config() -> dict[str, Any]:
    try:
        value = json.loads(config_path().read_text())
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def save_config(**changes: Any) -> dict[str, Any]:
    config = {**load_config(), **{k: v for k, v in changes.items() if v is not None}}
    path = config_path()
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(config, indent=2, sort_keys=True) + "\n")
    temporary.chmod(0o600)
    temporary.replace(path)
    return config


def use_saved_paths() -> None:
    """Put the folders where installers leave tools at the end of PATH, for this process and what it starts."""
    parts = os.environ.get("PATH", "").split(os.pathsep)
    for folder in [str(Path(p).expanduser()) for p in USER_BINS] + list(load_config().get("path") or []):
        if folder not in parts and Path(folder).is_dir():
            parts.append(folder)
    os.environ["PATH"] = os.pathsep.join(parts)


def saved_terraform() -> str | None:
    path = load_config().get("terraform")
    return path if path and Path(path).is_file() else None


# ---- this computer ---------------------------------------------------------------------------------


@dataclass(frozen=True)
class Machine:
    system: str  # darwin, linux or windows
    arch: str  # arm64 or amd64
    brew: bool
    linux_installer: str | None  # apt-get, dnf or yum

    @property
    def name(self) -> str:
        return {"darwin": "macOS", "linux": "Linux", "windows": "Windows"}.get(self.system, self.system) + f" ({self.arch})"


def machine(which: Callable[[str], str | None] = shutil.which) -> Machine:
    system = "darwin" if sys.platform == "darwin" else "linux" if sys.platform.startswith("linux") else "windows"
    arch = "arm64" if platform.machine().lower() in ("arm64", "aarch64") else "amd64"
    if system == "darwin" and arch == "amd64":
        # Python running under Rosetta on Apple silicon still reports x86_64; the hardware decides the Terraform build.
        try:
            if subprocess.run(["sysctl", "-n", "hw.optional.arm64"], capture_output=True, text=True, timeout=10).stdout.strip() == "1":
                arch = "arm64"
        except (OSError, subprocess.TimeoutExpired):
            pass
    installer = next((tool for tool in ("apt-get", "dnf", "yum") if which(tool)), None) if system == "linux" else None
    return Machine(system, arch, bool(which("brew")), installer)


# ---- the prerequisites ------------------------------------------------------------------------------


@dataclass
class Tool:
    key: str
    name: str
    needed: str
    found: str | None = None
    ready: bool = False
    optional: bool = False
    path: str | None = None
    install: str | None = None  # a shell command for this machine, or "reframe" for Reframe's own Terraform install
    note: str = ""


def _version(argv: list[str], pattern: str) -> str | None:
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=60, env=base_environment())
    except (OSError, subprocess.TimeoutExpired):
        return None
    match = re.search(pattern, (result.stdout or "") + (result.stderr or ""))
    return match.group(1) if match else None


def install_command(key: str, m: Machine) -> str | None:
    """The install command for one tool on this machine, from a fixed list; None when there is no sensible one."""
    mac, linux = m.system == "darwin", m.system == "linux"
    package = {"apt-get": "sudo apt-get update && sudo apt-get install -y", "dnf": "sudo dnf install -y", "yum": "sudo yum install -y"}.get(m.linux_installer or "")
    if key == "git":
        return "brew install git" if mac and m.brew else "xcode-select --install" if mac else f"{package} git" if package else None
    if key == "aws":
        if mac and m.brew:
            return "brew install awscli"
        if mac:
            return 'curl -fsSL "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o /tmp/AWSCLIV2.pkg && sudo installer -pkg /tmp/AWSCLIV2.pkg -target /'
        if linux:
            return ('cd "$(mktemp -d)" && curl -fsSL "https://awscli.amazonaws.com/awscli-exe-linux-$(uname -m).zip" -o awscliv2.zip '
                    '&& unzip -q awscliv2.zip && sudo ./aws/install --update')
    if key == "uv":
        return "brew install uv" if mac and m.brew else "curl -LsSf https://astral.sh/uv/install.sh | sh" if mac or linux else None
    if key == "terraform":
        return "reframe" if mac or linux else None
    if key == "mcp":
        return f"uvx --from {MCP_SERVER} python -c pass"
    if key == "plugin":
        return "reframe-plugin" if mac or linux else None
    if key == "claude":
        return "brew install --cask claude-code" if mac and m.brew else "curl -fsSL https://claude.ai/install.sh | bash" if mac or linux else None
    return None


def check(m: Machine, which: Callable[[str], str | None] = shutil.which) -> list[Tool]:
    tools = [Tool("git", "Git", "any"), Tool("aws", "AWS CLI", "version 2"), Tool("uv", "uv (uvx)", "any"),
             Tool("terraform", "Terraform", ".".join(map(str, MINIMUM_TERRAFORM)) + " or later"),
             Tool("mcp", "AWS Transform MCP server", MCP_SERVER.split("==")[1]),
             Tool("claude", "Claude Code", "any", optional=True, note="for pipeline 2"),
             Tool("plugin", "code-modernization plugin", "1.1.0, pinned", optional=True, note="for pipeline 2")]
    for tool in tools:
        tool.install = install_command(tool.key, m)
    git, aws, uvx, claude = which("git"), which("aws"), which("uvx"), which("claude")
    tools[0].path, tools[0].found = git, _version(["git", "--version"], r"git version (\S+)") if git else None
    tools[0].ready = bool(tools[0].found)
    tools[1].path, tools[1].found = aws, _version(["aws", "--version"], r"aws-cli/(\S+)") if aws else None
    tools[1].ready = bool(tools[1].found and tools[1].found.startswith("2."))
    tools[2].path, tools[2].found = uvx, _version(["uv", "--version"], r"uv (\S+)") if uvx and which("uv") else ("found" if uvx else None)
    tools[2].ready = bool(uvx)
    terraform = saved_terraform() or os.environ.get("REFRAME_TERRAFORM") or which("terraform")
    version = terraform_version(terraform) if terraform else None
    tools[3].path, tools[3].found = terraform, ".".join(map(str, version)) if version else None
    tools[3].ready = bool(version and version >= MINIMUM_TERRAFORM)
    if version and not tools[3].ready:
        tools[3].note = f"too old at {terraform}"
    tools[4].found = "fetched" if uvx and _cached_mcp() else None
    tools[4].ready = bool(tools[4].found)
    if not uvx:
        tools[4].note = "needs uv first"
    tools[5].path, tools[5].found = claude, _version(["claude", "--version"], r"(\d+\.\d+\.\d+)") if claude else None
    tools[5].ready = bool(tools[5].found)
    from reframe.claude import plugin
    tools[6].found = f"{plugin.VERSION} at {plugin.COMMIT[:12]}" if plugin.fetched() else None
    tools[6].ready = plugin.fetched()
    if not claude:
        tools[6].note = "needs Claude Code first"
    return tools


def _cached_mcp() -> bool:
    try:
        return subprocess.run(["uvx", "--offline", "--from", MCP_SERVER, "python", "-c", "pass"], capture_output=True,
                              timeout=180, env=base_environment()).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def run_in_terminal(command: str) -> bool:
    """Run one install command from the fixed list in the person's terminal, so sudo and installers can ask them."""
    return subprocess.run(["/bin/sh", "-c", command]).returncode == 0


# ---- Terraform, installed by Reframe ---------------------------------------------------------------


def _fetch(url: str, target: Path) -> None:
    subprocess.run(["curl", "-fsSL", "--retry", "2", "-o", str(target), url], check=True, timeout=600)


def install_terraform(m: Machine, fetch: Callable[[str, Path], None] = _fetch) -> Path:
    """The pinned Terraform release for this machine, checked against HashiCorp's SHA-256 sums, in ~/.reframe/tools."""
    if m.system not in ("darwin", "linux"):
        raise RuntimeError("Reframe installs Terraform on macOS and Linux; on Windows, use WSL2")
    name = f"terraform_{TERRAFORM_VERSION}_{m.system}_{m.arch}.zip"
    base = f"{TERRAFORM_RELEASES}/{TERRAFORM_VERSION}"
    target_dir = home() / "tools" / "terraform" / TERRAFORM_VERSION
    with tempfile.TemporaryDirectory() as scratch:
        sums, archive = Path(scratch) / "SHA256SUMS", Path(scratch) / name
        fetch(f"{base}/terraform_{TERRAFORM_VERSION}_SHA256SUMS", sums)
        expected = next((line.split()[0] for line in sums.read_text().splitlines() if line.strip().endswith(" " + name)), None)
        if not expected:
            raise RuntimeError(f"HashiCorp's SHA-256 sums do not list {name}")
        fetch(f"{base}/{name}", archive)
        actual = hashlib.sha256(archive.read_bytes()).hexdigest()
        if actual != expected:
            raise RuntimeError(f"{name} does not match HashiCorp's SHA-256 sum; nothing was installed")
        with zipfile.ZipFile(archive) as z:
            data = z.read("terraform")
    target_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
    binary = target_dir / "terraform"
    binary.write_bytes(data)
    binary.chmod(0o755)
    save_config(terraform=str(binary))
    return binary


# ---- the AWS sign-in ---------------------------------------------------------------------------------


def profiles() -> list[str]:
    try:
        result = subprocess.run(["aws", "configure", "list-profiles"], capture_output=True, text=True, timeout=60, env=base_environment())
    except (OSError, subprocess.TimeoutExpired):
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


@dataclass
class SignIn:
    profile: str
    region: str
    account: str | None = None
    expired: bool = False
    problem: str | None = None
    sso: bool = field(default=False)


def signed_in(profile: str, region: str) -> SignIn:
    from reframe.core.errors import NotSent
    from reframe.core.shell import Aws, SigninExpired
    state = SignIn(profile, region, sso=_is_sso(profile))
    try:
        state.account = Aws(profile, region).identity().get("Account")
    except SigninExpired:
        state.expired = True
    except NotSent as error:
        state.problem = str(error)
    return state


def _is_sso(profile: str) -> bool:
    for key in ("sso_session", "sso_start_url"):
        try:
            result = subprocess.run(["aws", "configure", "get", key, "--profile", profile], capture_output=True, text=True, timeout=30,
                                    env=base_environment())
        except (OSError, subprocess.TimeoutExpired):
            return False
        if result.returncode == 0 and result.stdout.strip():
            return True
    return False
