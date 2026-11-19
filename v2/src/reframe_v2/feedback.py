"""Gate feedback through GitHub issues and local files (FR-18, FR-04, FR-09, FR-12; P2-03).

Feedback is untrusted input. Every item records its author, channel, the
version reviewed, the ids it is about and the time, and gets a disposition.
Its text is data: it is stored and shown, never followed. Only a decision by
an authorized person changes an operative rule or closes a gate, and a
GitHub comment is never a decision by itself.

GitHub is one channel; local feedback files are the other, and a client
without GitHub completes every gate with them. With GitHub, Reframe opens one
issue per gate and updates it. The person sees exactly what will be posted,
and the post goes out only with that exact text (its hash is confirmed).

Version rules: feedback on the version under review is recorded as open.
Feedback on an older version is rebased when none of the ids it is about
changed since, and refused visibly (refused_stale) when they did. Feedback
after the gate closed goes to the next revision (section 4).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Protocol

from reframe_v2.model.records import Ref
from reframe_v2.policy import PolicyRefusal, check_destination
from reframe_v2.workflow.gates import GATES, Gate, GateState, evaluate_deadline

CHANNELS = ("github", "local_file", "cli")
ID_IN_TEXT = re.compile(r"`([A-Za-z0-9][A-Za-z0-9._:/-]{0,199})`")
MARKER = re.compile(r"<!-- reframe-gate: (gate[123]) version: ([^ ]+) revision: ([0-9]+) hash: (sha256:[0-9a-f]{64}) -->")


class FeedbackError(Exception):
    """Feedback was refused; the reason is shown to the person."""


@dataclass(frozen=True)
class Person:
    name: str
    verified: bool
    login: str | None = None

    def as_json(self) -> dict[str, Any]:
        return {"name": self.name, "verified": self.verified, "login": self.login}


@dataclass(frozen=True)
class Item:
    """One piece of feedback as received, before any rule is applied."""

    gate: str
    reviewed: Ref
    author: Person
    channel: str
    text: str
    affected_ids: tuple[str, ...]
    received_at: datetime
    external_ref: str | None = None


@dataclass(frozen=True)
class Recorded:
    """An item after the rules: its human_input body, the version it attaches to, and why."""

    body: dict[str, Any]
    attaches_to: Ref | None
    """The version the feedback is recorded against; None when it goes to the next revision."""
    next_revision: bool
    reason: str


def _utc(moment: datetime) -> str:
    if moment.tzinfo is None:
        raise FeedbackError("feedback times are timezone-aware")
    return moment.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def record(item: Item, gate: Gate, now: datetime, recorded_by: str,
           changed_since: Callable[[Ref, Ref], set[str]]) -> Recorded:
    """Apply the version and gate rules to one item and return its human_input body (kind feedback).

    changed_since(old, new) returns the ids whose content differs between two versions.
    """
    if item.channel not in CHANNELS:
        raise FeedbackError(f"unknown feedback channel {item.channel!r}")
    if item.gate != gate.name:
        raise FeedbackError(f"this feedback is for {item.gate}, not {gate.name}")
    gate = evaluate_deadline(gate, now)
    current = gate.snapshot
    if item.reviewed.id != current.id:
        raise FeedbackError(f"this feedback reviewed {item.reviewed.id}, which {gate.name} is not about")
    if item.reviewed.revision > current.revision:
        raise FeedbackError("this feedback names a version newer than the one under review")

    disposition, attaches, reason = "open", current, "on the version under review"
    if item.reviewed.revision < current.revision:
        changed = changed_since(item.reviewed, current) & set(item.affected_ids)
        if changed or not item.affected_ids:
            disposition, attaches = "refused_stale", None
            reason = (f"written against revision {item.reviewed.revision}; "
                      + (f"{', '.join(sorted(changed))} changed since" if changed else "it names no ids, so it cannot be rebased")
                      + f". Review revision {current.revision} and send it again")
        else:
            disposition, reason = "rebased", f"written against revision {item.reviewed.revision}; nothing it is about has changed since"

    next_revision = gate.state is not GateState.OPEN and disposition != "refused_stale"
    if next_revision:
        attaches, reason = None, f"{gate.name} is {gate.state.value}; recorded for the next revision, not the closed snapshot"

    body = {
        "kind": "feedback",
        "text": item.text,
        "affected_ids": list(item.affected_ids),
        "external_ref": item.external_ref,
        "disposition": disposition,
        "author": item.author.as_json(),
        "recorded_by": recorded_by,
        "channel": item.channel,
        "recorded_at": _utc(item.received_at),
    }
    return Recorded(body, attaches, next_revision, reason)


# Decisions -------------------------------------------------------------------


@dataclass(frozen=True)
class Authority:
    """Who may decide. GitHub logins are verified by GitHub; names are recorded as stated (section 4, identity)."""

    logins: frozenset[str] = frozenset()
    names: frozenset[str] = frozenset()
    design_owner: str | None = None

    def allows(self, person: Person) -> bool:
        if person.verified and person.login:
            return person.login in self.logins
        return person.name in self.names


def decision(subject: str, outcome: str, reason: str, binds_to: Ref, by: Person, authority: Authority,
             channel: str, recorded_by: str, now: datetime) -> dict[str, Any]:
    """A human_input body (kind decision). Refused unless the person is authorized; the text of any issue is never one."""
    if channel == "github":
        raise FeedbackError("a GitHub comment is feedback, never a decision; an authorized person records the decision with reframe continue")
    if not authority.allows(by):
        raise FeedbackError(f"{by.login or by.name} is not authorized to decide; the feedback stays open")
    return {"kind": "decision", "subject": subject, "outcome": outcome, "reason": reason,
            "binds_to": {"id": binds_to.id, "revision": binds_to.revision, "content_hash": binds_to.content_hash},
            "author": by.as_json(), "recorded_by": recorded_by, "channel": channel, "recorded_at": _utc(now)}


def may_accept_design(by: Person, authority: Authority) -> bool:
    """Only the named design owner's acceptance closes gate 3 as accepted."""
    if authority.design_owner is None:
        return False
    return by.name == authority.design_owner or (by.verified and by.login == authority.design_owner)


# Local feedback files --------------------------------------------------------


def read_local_file(path: Path, known_ids: set[str], received_at: datetime) -> list[Item]:
    """A local feedback file: JSON with gate, version (id, revision, content_hash), author and items.

    Each item has text and affected_ids. An id the version does not contain is refused, so a typo
    never attaches feedback to nothing. The author's name is recorded as stated.
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        raise FeedbackError(f"{path.name} is not JSON: {error}") from None
    try:
        gate, version, author, items = data["gate"], data["version"], data["author"], data["items"]
        reviewed = Ref(version["id"], int(version["revision"]), version["content_hash"])
    except (KeyError, TypeError, ValueError):
        raise FeedbackError(f"{path.name} needs gate, version (id, revision, content_hash), author and items") from None
    if gate not in GATES or not isinstance(author, str) or not author.strip() or not isinstance(items, list) or not items:
        raise FeedbackError(f"{path.name}: gate must be gate1, gate2 or gate3, author a name, and items a non-empty list")
    result = []
    for number, entry in enumerate(items, 1):
        text, ids = entry.get("text") if isinstance(entry, dict) else None, entry.get("affected_ids", []) if isinstance(entry, dict) else None
        if not isinstance(text, str) or not text.strip() or not isinstance(ids, list):
            raise FeedbackError(f"{path.name} item {number}: needs text and affected_ids")
        unknown = sorted(set(ids) - known_ids)
        if unknown:
            raise FeedbackError(f"{path.name} item {number}: {', '.join(unknown)} not in this version")
        result.append(Item(gate, reviewed, Person(author.strip(), False), "local_file", text, tuple(ids), received_at,
                           f"{path.name}#{number}"))
    return result


# GitHub ----------------------------------------------------------------------


@dataclass(frozen=True)
class Comment:
    id: str
    login: str
    body: str
    created_at: datetime


class GitHub(Protocol):
    def create_issue(self, repository: str, title: str, body: str) -> int: ...
    def update_issue(self, repository: str, number: int, body: str) -> None: ...
    def comments(self, repository: str, number: int) -> list[Comment]: ...


@dataclass(frozen=True)
class Draft:
    """Exactly what will be posted. Posting needs its hash, so nothing else can go out."""

    repository: str
    title: str
    body: str
    issue: int | None = None

    @property
    def digest(self) -> str:
        return "sha256:" + hashlib.sha256(json.dumps([self.repository, self.title, self.body, self.issue]).encode()).hexdigest()

    def preview(self) -> str:
        where = f"update issue #{self.issue}" if self.issue else "open a new issue"
        return (f"This is exactly what will be sent to GitHub ({self.repository}, {where}). Nothing else leaves the workspace.\n\n"
                f"Title: {self.title}\n\n{self.body}\n\nConfirm with {self.digest}")


def gate_issue(policy: dict[str, Any], gate: Gate, summary: list[str], site_note: str, issue: int | None = None) -> Draft:
    """The one issue for this gate: what is under review, until when, and how to answer. No source text goes in it."""
    feedback = policy["feedback"]
    if feedback["channel"] != "github" or not feedback["repository"]:
        raise FeedbackError("feedback for this project uses local files; nothing is posted to GitHub")
    try:
        check_destination(policy, "github")
    except PolicyRefusal as error:
        raise FeedbackError(str(error)) from None
    snapshot = gate.snapshot
    lines = [
        f"{gate.name} review of `{snapshot.id}` revision {snapshot.revision}.",
        f"Open until {gate.deadline.strftime('%Y-%m-%d %H:%M UTC')}. The run carries on meanwhile; this review is not an approval.",
        "",
        *[f"- {line}" for line in summary],
        "",
        site_note,
        "",
        "Comment with feedback, naming the ids it is about in backticks. Comments are recorded as feedback; "
        "decisions are recorded by an authorized person with `reframe continue`.",
        f"<!-- reframe-gate: {gate.name} version: {snapshot.id} revision: {snapshot.revision} hash: {snapshot.content_hash} -->",
    ]
    return Draft(feedback["repository"], f"Reframe {gate.name} review: {snapshot.id} revision {snapshot.revision}", "\n".join(lines), issue)


def post(github: GitHub, draft: Draft, confirmed: str) -> int:
    """Send the draft, only if the person confirmed exactly this text."""
    if confirmed != draft.digest:
        raise FeedbackError("the confirmation does not match this draft; nothing was posted. Show the preview again")
    if draft.issue is None:
        return github.create_issue(draft.repository, draft.title, draft.body)
    github.update_issue(draft.repository, draft.issue, draft.body)
    return draft.issue


def read_issue(github: GitHub, draft_body: str, repository: str, number: int, known_ids: set[str],
               since: datetime | None = None) -> list[Item]:
    """Comments on a gate issue, as feedback items. Logins are verified by GitHub; text is data.

    Ids are taken only from backticked words that exist in the reviewed version; anything else in
    the comment is kept as text and never acted on.
    """
    found = MARKER.search(draft_body)
    if not found:
        raise FeedbackError("this issue was not opened by Reframe for a gate; its comments are not read")
    gate, version_id, revision, content_hash = found.groups()
    reviewed = Ref(version_id, int(revision), content_hash)
    items = []
    for comment in github.comments(repository, number):
        if since is not None and comment.created_at <= since:
            continue
        ids = tuple(sorted({word for word in ID_IN_TEXT.findall(comment.body) if word in known_ids}))
        items.append(Item(gate, reviewed, Person(comment.login, True, comment.login), "github", comment.body, ids,
                          comment.created_at, f"{repository}#{number}/comment/{comment.id}"))
    return items


def _run_gh(argv: list[str], env: dict[str, str], timeout: float, stdin: str | None):
    return subprocess.run(argv, env=env, input=stdin, capture_output=True, text=True, timeout=timeout, shell=False)


class GhCli:
    """GitHub through the gh CLI the engineer is signed in to, with no shell. Only issues are touched."""

    def __init__(self, runner=_run_gh, parent_environment: dict[str, str] | None = None, timeout_seconds: float = 60) -> None:
        self.runner = runner
        source = os.environ if parent_environment is None else parent_environment
        self.env = {name: source[name] for name in ("HOME", "PATH", "LANG", "GH_CONFIG_DIR", "GH_HOST") if name in source}
        self.env["GH_PROMPT_DISABLED"] = "1"
        self.timeout = timeout_seconds

    def _api(self, *arguments: str, payload: dict[str, Any] | None = None) -> Any:
        argv = ["gh", "api", *arguments] + (["--input", "-"] if payload is not None else [])
        try:
            result = self.runner(argv, self.env, self.timeout, None if payload is None else json.dumps(payload))
        except (subprocess.TimeoutExpired, OSError) as error:
            raise FeedbackError(f"the gh CLI did not complete ({type(error).__name__}); check the issue before posting again") from None
        if result.returncode != 0:
            raise FeedbackError(f"GitHub refused the request: {result.stderr.strip()[:200]}")
        try:
            return json.loads(result.stdout or "null")
        except ValueError:
            raise FeedbackError("GitHub returned a reply that is not JSON") from None

    def create_issue(self, repository: str, title: str, body: str) -> int:
        return int(self._api("-X", "POST", f"repos/{repository}/issues", payload={"title": title, "body": body})["number"])

    def update_issue(self, repository: str, number: int, body: str) -> None:
        self._api("-X", "PATCH", f"repos/{repository}/issues/{number}", payload={"body": body})

    def comments(self, repository: str, number: int) -> list[Comment]:
        """Every comment by a person; bot comments are skipped."""
        pages = self._api("--paginate", "--slurp", f"repos/{repository}/issues/{number}/comments")
        if not isinstance(pages, list):
            raise FeedbackError("GitHub returned an unexpected comment listing")
        result = []
        for page in pages:
            for item in page if isinstance(page, list) else []:
                user = item.get("user") or {}
                if not user.get("login") or user.get("type") == "Bot":
                    continue
                created = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
                result.append(Comment(str(item["id"]), user["login"], item.get("body") or "", created))
        return result


@dataclass
class GateFeedback:
    """Collected feedback for one gate, with the reasons people see."""

    recorded: list[Recorded] = field(default_factory=list)

    def summary(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for item in self.recorded:
            key = "next_revision" if item.next_revision else item.body["disposition"]
            counts[key] = counts.get(key, 0) + 1
        return dict(sorted(counts.items()))
