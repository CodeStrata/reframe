"""The AI-DLC-ready package: layout, manifest and adapter rules for AI-DLC v2.11.4 (specification section 9, NFR-11).

- Paths starting with knowledge/ or memory/ are AI-DLC workspace files under
  aidlc/spaces/default/; every other path, dot folders included, is at the
  package root.
- Knowledge files are text and stay under 200,000 characters each; larger
  content is split at section, then paragraph, then line boundaries, never cut.
- reframe/manifest.json lists every path with its hash, canonical source and
  adapter version; the package is validated against it, and it cannot mix
  versions or name a version that does not exist.
- Reframe never overwrites existing team or AI-DLC files; a collision stops
  with the list. There is no codekb/.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any

from reframe_v2.model.records import Ref
from reframe_v2.model.schemas import validate_document
from reframe_v2.model.store import VersionStore

AIDLC_RELEASE = "v2.11.4"
HARNESSES = ("claude", "kiro")
ADAPTER_VERSION = "1"
KNOWLEDGE_LIMIT = 200_000
WORKSPACE_PREFIX = "aidlc/spaces/default/"
MANIFEST_PATH = "reframe/manifest.json"
PROVENANCE_PATH = "reframe/provenance.json"


class PackageError(Exception):
    """The package would break an adapter or manifest rule. Nothing was written."""


def package_path(logical: str) -> str:
    """Where a logical package path lands."""
    if logical.startswith("/") or ".." in logical.split("/") or "\\" in logical:
        raise PackageError(f"unsafe package path {logical!r}")
    if logical.startswith("codekb/"):
        raise PackageError("there is no codekb/; the package starts a new build")
    if logical.startswith(("knowledge/", "memory/")):
        return WORKSPACE_PREFIX + logical
    return logical


def skill_paths(name: str, tool: str) -> list[str]:
    """Skill locations for the chosen AI tool; both when no tool was chosen."""
    if tool not in ("claude", "kiro", "both"):
        raise PackageError(f"unknown AI tool {tool!r}")
    paths = []
    if tool in ("claude", "both"):
        paths.append(f".claude/skills/reframe-{name}/SKILL.md")
    if tool in ("kiro", "both"):
        paths.append(f".kiro/steering/reframe-{name}.md")
    return paths


def split_knowledge(name: str, sections: list[str], limit: int = KNOWLEDGE_LIMIT) -> dict[str, str]:
    """Split knowledge text into files under the limit, at section, paragraph, then line boundaries. Nothing is cut."""
    pieces: list[str] = []
    for section in sections:
        pieces.extend(_fit(section, limit, ["\n\n", "\n"]))
    files: list[str] = []
    current = ""
    for piece in pieces:
        candidate = current + ("\n\n" if current else "") + piece
        if current and len(candidate) > limit:
            files.append(current)
            current = piece
        else:
            current = candidate
    if current:
        files.append(current)
    if len(files) == 1:
        return {f"{name}.md": files[0]}
    return {f"{name}.part{index:02d}.md": text for index, text in enumerate(files, start=1)}


def _fit(text: str, limit: int, separators: list[str]) -> list[str]:
    if len(text) <= limit:
        return [text]
    if not separators:
        raise PackageError(f"a single line of {len(text)} characters exceeds the {limit}-character knowledge limit; it is not truncated")
    separator, rest = separators[0], separators[1:]
    out: list[str] = []
    current = ""
    for part in text.split(separator):
        for piece in _fit(part, limit, rest):
            candidate = current + (separator if current else "") + piece
            if current and len(candidate) > limit:
                out.append(current)
                current = piece
            else:
                current = candidate
    if current:
        out.append(current)
    return out


@dataclass(frozen=True)
class PackageFile:
    logical_path: str
    content: bytes
    canonical_source: Ref | None


def sha256(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def build(store: VersionStore, files: list[PackageFile], harnesses: tuple[str, ...], existing_paths: set[str] | frozenset[str] = frozenset()) -> dict[str, bytes]:
    """Lay out the package and write its manifest. Refuses stale or mixed versions, unknown references and collisions."""
    if not harnesses or any(h not in HARNESSES for h in harnesses):
        raise PackageError(f"harnesses must be chosen from {HARNESSES}")
    laid_out: dict[str, PackageFile] = {}
    for item in files:
        path = package_path(item.logical_path)
        if path in laid_out or path in (MANIFEST_PATH,):
            raise PackageError(f"{path} appears twice in the package")
        if path.startswith(WORKSPACE_PREFIX + "knowledge/") and len(item.content.decode("utf-8")) > KNOWLEDGE_LIMIT:
            raise PackageError(f"{path} is over {KNOWLEDGE_LIMIT} characters; split it first")
        laid_out[path] = item
    collisions = sorted(set(laid_out) & set(existing_paths))
    if collisions:
        raise PackageError("existing team or AI-DLC files would be overwritten: " + ", ".join(collisions))
    sources = sorted({item.canonical_source for item in laid_out.values() if item.canonical_source is not None})
    versions = store.check_version_set(sources)
    stale = sorted({reason for ref in sources for reason in store.stale_reasons(ref)})
    if stale:
        raise PackageError("the package would contain stale versions: " + "; ".join(stale))
    manifest = {
        "schema": "package_manifest/1",
        "aidlc_release": AIDLC_RELEASE,
        "harnesses": sorted(harnesses),
        "adapter_version": ADAPTER_VERSION,
        "versions": [ref.as_json() for ref in versions],
        "files": [
            {
                "path": path,
                "sha256": sha256(item.content),
                "size": len(item.content),
                "canonical_source": item.canonical_source.as_json() if item.canonical_source else None,
            }
            for path, item in sorted(laid_out.items())
        ],
    }
    validate_document("package_manifest", manifest)
    output = {path: item.content for path, item in laid_out.items()}
    output[MANIFEST_PATH] = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    return output


def check(package: dict[str, bytes], store: VersionStore | None = None) -> list[str]:
    """Validate a written package against its manifest. Returns every problem found."""
    if MANIFEST_PATH not in package:
        return [f"{MANIFEST_PATH} is missing"]
    manifest = json.loads(package[MANIFEST_PATH])
    problems = []
    try:
        validate_document("package_manifest", manifest)
    except Exception as error:  # noqa: BLE001 - reported, not raised
        problems.append(str(error))
        return problems
    listed = {entry["path"]: entry for entry in manifest["files"]}
    for path in sorted(set(package) - set(listed) - {MANIFEST_PATH}):
        problems.append(f"{path} is in the package but not in the manifest")
    for path, entry in sorted(listed.items()):
        if path not in package:
            problems.append(f"{path} is in the manifest but missing from the package")
        elif sha256(package[path]) != entry["sha256"]:
            problems.append(f"{path} does not match its manifest hash")
    if store is not None:
        for entry in manifest["versions"]:
            ref = Ref.from_json(entry)
            try:
                for reason in store.stale_reasons(ref):
                    problems.append(f"stale: {reason}")
            except Exception as error:  # noqa: BLE001
                problems.append(f"unknown reference {ref.id} revision {ref.revision}: {error}")
    return problems


def provenance_document(snapshot: Ref, aws_jobs: list[str], model_backend: dict[str, Any], gates: list[dict[str, Any]],
                        versions: list[Ref], manifest_bytes: bytes) -> dict[str, Any]:
    document = {
        "schema": "provenance/1",
        "snapshot": snapshot.as_json(),
        "aws_jobs": list(aws_jobs),
        "model_backend": model_backend,
        "gates": gates,
        "versions": [ref.as_json() for ref in sorted(versions)],
        "manifest_sha256": sha256(manifest_bytes),
    }
    validate_document("provenance", document)
    return document
