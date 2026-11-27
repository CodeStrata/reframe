"""Stage 1: the source snapshot (specification section 4, stage 1).

| Source                         | Snapshot                                                                   |
|--------------------------------|----------------------------------------------------------------------------|
| a local Git checkout           | git archive of the commit (--ref, default HEAD): only committed files       |
| a local folder, not Git        | a ZIP of every file, in name order with fixed timestamps (same files, same bytes) |
| a local ZIP file               | the file itself, after checking it                                          |
| a GitHub (or other Git) URL    | cloned into the run folder at --ref, then git archive of that commit       |

Every archive is checked the same way before it is used: it opens, has no absolute or ".." paths and no
links, and unpacks to at most 2 GB.
"""

from __future__ import annotations

import hashlib
import os
import re
import shutil
import stat
import zipfile
from pathlib import Path, PurePosixPath
from typing import Any

from reframe.core.errors import Outcome, Stop
from reframe.core.runfolder import RunFolder
from reframe.core.shell import Runner, base_environment, run_subprocess

URL = re.compile(r"^(https?|ssh|git)://|^git@")
MAX_UNPACKED = 2 * 1024 ** 3
MAX_MEMBERS = 200_000
SKIPPED = frozenset({".git", ".DS_Store", "__MACOSX", ".svn", ".hg", "Thumbs.db"})
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def kind(source: str) -> str:
    if URL.match(source):
        return "git-url"
    path = Path(source).expanduser()
    if path.is_file():
        return "zip"
    if path.is_dir():
        return "folder"
    raise Stop(Outcome.REFUSED, f"the source {source!r} is not a folder, a ZIP file or a Git URL")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git(runner: Runner, *arguments: str, timeout: float = 600) -> str:
    result = runner(["git", *arguments], base_environment(), timeout, None)
    if result.returncode != 0:
        verb = arguments[2] if arguments[0] == "-C" else arguments[0]
        raise Stop(Outcome.REFUSED, f"git {verb} failed: {result.stderr.strip()[:300]}")
    return result.stdout


def is_git_toplevel(path: Path, runner: Runner) -> bool:
    result = runner(["git", "-C", str(path), "rev-parse", "--show-toplevel"], base_environment(), 60, None)
    return result.returncode == 0 and Path(result.stdout.strip()).resolve() == path.resolve()


def check_archive(path: Path) -> int:
    """Refuse an archive that does not open, escapes its folder, holds links, or unpacks too large. Returns the file count."""
    try:
        with zipfile.ZipFile(path) as archive:
            members = archive.infolist()
            if len(members) > MAX_MEMBERS:
                raise Stop(Outcome.REFUSED, f"the archive holds more than {MAX_MEMBERS} entries")
            total, files = 0, 0
            for member in members:
                name = PurePosixPath(member.filename.replace("\\", "/"))
                if name.is_absolute() or ".." in name.parts or re.match(r"^[A-Za-z]:", member.filename):
                    raise Stop(Outcome.REFUSED, f"the archive has an unsafe path: {member.filename[:120]}")
                if stat.S_ISLNK(member.external_attr >> 16):
                    raise Stop(Outcome.REFUSED, f"the archive holds a link: {member.filename[:120]}")
                total += member.file_size
                files += 0 if member.is_dir() else 1
            if total > MAX_UNPACKED:
                raise Stop(Outcome.REFUSED, "the archive unpacks to more than 2 GB")
            if files == 0:
                raise Stop(Outcome.REFUSED, "the archive holds no files")
            return files
    except zipfile.BadZipFile:
        raise Stop(Outcome.REFUSED, f"{path.name} is not a ZIP file that can be opened") from None


def zip_folder(source: Path, target: Path) -> int:
    """A ZIP of every regular file under source, in name order with fixed timestamps; links and tool folders are left out."""
    paths = []
    for root, folders, names in os.walk(source, followlinks=False):
        folders[:] = sorted(f for f in folders if f not in SKIPPED and not (Path(root) / f).is_symlink())
        for name in sorted(names):
            path = Path(root) / name
            if name in SKIPPED or path.is_symlink() or not path.is_file():
                continue
            paths.append(path)
    paths.sort(key=lambda p: p.relative_to(source).as_posix())
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in paths:
            info = zipfile.ZipInfo(path.relative_to(source).as_posix(), FIXED_TIME)
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    return len(paths)


def take(folder: RunFolder, source: str, ref: str | None, runner: Runner = run_subprocess) -> dict[str, Any]:
    recorded = folder.load("snapshot.json")
    if recorded is not None:
        if (recorded["source"], recorded.get("ref")) != (source, ref):
            raise Stop(Outcome.REFUSED, "this run's snapshot is of another source; start a new run for a different source")
        return recorded
    form = kind(source)
    archive = folder.path("source/archive.zip")
    archive.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    commit = None
    if form == "git-url":
        target = folder.path("source/repo")
        if not (target / ".git").exists():
            _git(runner, "clone", "--quiet", "--no-checkout", source, str(target), timeout=3600)
        if ref:
            _git(runner, "-C", str(target), "fetch", "--quiet", "origin", ref, timeout=3600)
        commit = _git(runner, "-C", str(target), "rev-parse", "--verify", f"{'FETCH_HEAD' if ref else 'HEAD'}^{{commit}}").strip()
        _git(runner, "-C", str(target), "archive", "--format=zip", "-o", str(archive), commit)
    elif form == "folder" and is_git_toplevel(Path(source).expanduser(), runner):
        checkout = str(Path(source).expanduser())
        commit = _git(runner, "-C", checkout, "rev-parse", "--verify", f"{ref or 'HEAD'}^{{commit}}").strip()
        _git(runner, "-C", checkout, "archive", "--format=zip", "-o", str(archive), commit)
    elif form == "folder":
        if ref:
            raise Stop(Outcome.REFUSED, "--ref needs a Git checkout or URL; this folder is not a Git checkout")
        zip_folder(Path(source).expanduser(), archive)
        form = "plain-folder"
    else:
        if ref:
            raise Stop(Outcome.REFUSED, "--ref needs a Git checkout or URL, not a ZIP file")
        shutil.copyfile(Path(source).expanduser(), archive)
    archive.chmod(0o600)
    files = check_archive(archive)
    data = archive.read_bytes()
    record: dict[str, Any] = {"source": source, "ref": ref, "form": form, "commit": commit, "files": files, "sha256": sha256_hex(data),
              "bytes": len(data), "archive": "source/archive.zip"}
    folder.save("snapshot.json", record)
    folder.event("snapshot", form=form, commit=(commit or "")[:12], files=files, sha256=record["sha256"][:16], bytes=len(data))
    return record


def archive_bytes(folder: RunFolder, record: dict[str, Any]) -> bytes:
    data = folder.path(record["archive"]).read_bytes()
    if sha256_hex(data) != record["sha256"]:
        raise Stop(Outcome.REFUSED, "the stored snapshot archive no longer matches its recorded SHA-256")
    return data
