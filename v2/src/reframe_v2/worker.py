"""Background worker contract: lease, event log, backoff and stop (specification section 4, section 8).

- One worker per project holds a renewable lease in the account's Reframe
  state bucket, written with conditional writes, so two machines never
  dispatch the same operation. Takeover happens only after the lease expires.
- A durable event log records dispatches, receipts, parked work, gate changes
  and notifications; it is append-only, one object per event.
- Polling uses capped exponential backoff.
- reframe stop waits for the current step up to a time limit; if it does not
  return, the worker stops and the step's in-flight calls are UNCERTAIN, never
  free to replay.
- macOS and Linux; no automatic restart after a reboot (reframe run resumes).

The object store is an interface. FakeBucket implements S3's conditional-write
semantics for tests; the real bucket adapter must pass the same tests.
"""

from __future__ import annotations

import json
import sys
import threading
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Protocol

SUPPORTED_PLATFORMS = ("darwin", "linux")


class PreconditionFailed(Exception):
    """A conditional write lost: the object exists, or changed since it was read."""


class LeaseHeld(Exception):
    """Another worker holds a live lease on this project."""


class LeaseLost(Exception):
    """This worker's lease was taken over or expired; it must stop dispatching."""


class ObjectStore(Protocol):
    def get(self, key: str) -> tuple[bytes, str] | None: ...
    def put(self, key: str, data: bytes, *, if_none_match: bool = False, if_match: str | None = None) -> str: ...
    def list(self, prefix: str) -> list[str]: ...


class FakeBucket:
    """In-memory store with S3 conditional writes: If-None-Match: * and If-Match: <etag>."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._objects: dict[str, tuple[bytes, str]] = {}
        self._version = 0

    def get(self, key: str) -> tuple[bytes, str] | None:
        with self._lock:
            return self._objects.get(key)

    def put(self, key: str, data: bytes, *, if_none_match: bool = False, if_match: str | None = None) -> str:
        with self._lock:
            current = self._objects.get(key)
            if if_none_match and current is not None:
                raise PreconditionFailed(f"{key} already exists")
            if if_match is not None and (current is None or current[1] != if_match):
                raise PreconditionFailed(f"{key} changed since it was read")
            self._version += 1
            etag = f'"{self._version}"'
            self._objects[key] = (data, etag)
            return etag

    def list(self, prefix: str) -> list[str]:
        with self._lock:
            return sorted(key for key in self._objects if key.startswith(prefix))


def check_platform(platform: str | None = None) -> None:
    name = platform or sys.platform
    if not name.startswith(SUPPORTED_PLATFORMS):
        raise RuntimeError(f"the background worker runs on macOS and Linux; on Windows use WSL2 (found {name})")


@dataclass(frozen=True)
class Lease:
    project: str
    holder: str
    expires_at: datetime
    generation: int
    etag: str


class LeaseManager:
    def __init__(self, store: ObjectStore, project: str, holder: str, ttl: timedelta) -> None:
        if ttl <= timedelta(0):
            raise ValueError("a lease lasts some time")
        self.store, self.project, self.holder, self.ttl = store, project, holder, ttl
        self.key = f"projects/{project}/worker-lease.json"
        self.current: Lease | None = None

    def acquire(self, now: datetime) -> Lease:
        existing = self.store.get(self.key)
        if existing is None:
            return self._write(now, generation=1, if_none_match=True)
        data, etag = existing
        held = json.loads(data)
        expires = datetime.fromisoformat(held["expires_at"])
        if held["holder"] != self.holder and now < expires:
            raise LeaseHeld(f"{held['holder']} holds the lease until {expires.isoformat()}")
        return self._write(now, generation=held["generation"] + 1, if_match=etag)

    def renew(self, now: datetime) -> Lease:
        if self.current is None:
            raise LeaseLost("no lease to renew")
        existing = self.store.get(self.key)
        if existing is None or existing[1] != self.current.etag:
            self.current = None
            raise LeaseLost("the lease was taken over")
        if now >= self.current.expires_at:
            self.current = None
            raise LeaseLost("the lease expired before it was renewed")
        return self._write(now, generation=self.current.generation, if_match=self.current.etag)

    def may_dispatch(self, now: datetime) -> bool:
        if self.current is None or now >= self.current.expires_at:
            return False
        existing = self.store.get(self.key)
        return existing is not None and existing[1] == self.current.etag

    def _write(self, now: datetime, generation: int, if_none_match: bool = False, if_match: str | None = None) -> Lease:
        expires = now + self.ttl
        body = json.dumps({"project": self.project, "holder": self.holder, "expires_at": expires.isoformat(),
                           "generation": generation}, sort_keys=True).encode()
        try:
            etag = self.store.put(self.key, body, if_none_match=if_none_match, if_match=if_match)
        except PreconditionFailed:
            self.current = None
            raise LeaseHeld("another worker wrote the lease first") from None
        self.current = Lease(self.project, self.holder, expires, generation, etag)
        return self.current


EVENT_KINDS = ("dispatch", "receipt", "parked", "resumed", "gate_opened", "gate_closed", "notification", "uncertain", "stopped")


class EventLog:
    """Append-only, one object per event, numbered in order. Concurrent appenders never overwrite each other."""

    def __init__(self, store: ObjectStore, project: str) -> None:
        self.store = store
        self.prefix = f"projects/{project}/events/"

    def append(self, kind: str, at: datetime, detail: dict) -> int:
        if kind not in EVENT_KINDS:
            raise ValueError(f"unknown event kind {kind!r}")
        body = json.dumps({"kind": kind, "at": at.astimezone(timezone.utc).isoformat(), "detail": detail}, sort_keys=True).encode()
        sequence = len(self.store.list(self.prefix)) + 1
        while True:
            try:
                self.store.put(f"{self.prefix}{sequence:012d}.json", body, if_none_match=True)
                return sequence
            except PreconditionFailed:
                sequence += 1

    def read(self, since: int = 0) -> list[dict]:
        events = []
        for key in self.store.list(self.prefix):
            sequence = int(key.rsplit("/", 1)[1].split(".")[0])
            if sequence > since:
                data, _ = self.store.get(key)
                events.append({"sequence": sequence, **json.loads(data)})
        return events


def backoff(attempt: int, base: timedelta = timedelta(seconds=15), cap: timedelta = timedelta(minutes=10)) -> timedelta:
    """Delay before poll attempt N (starting at 0): doubling from base, never above cap."""
    if attempt < 0:
        raise ValueError("attempts start at 0")
    return min(cap, base * (2 ** min(attempt, 30)))


@dataclass(frozen=True)
class StopOutcome:
    graceful: bool
    uncertain_operations: tuple[str, ...]
    message: str


def stop(in_flight: list[str], returned_within_limit: bool) -> StopOutcome:
    """reframe stop: after the current step if it returns in time; otherwise forced, with in-flight calls UNCERTAIN."""
    if returned_within_limit:
        return StopOutcome(True, (), "stopped after the current step; reframe run resumes")
    return StopOutcome(False, tuple(sorted(in_flight)),
                       "forced stop: in-flight calls are UNCERTAIN and are never replayed; settle them with reframe resolve, then reframe run")


@dataclass(frozen=True)
class Notification:
    channel: str
    subject: str
    gate: str | None = None


def gate_notifications(gate: str, feedback_channel: str, people: list[str]) -> list[Notification]:
    """Notifications for an opened gate: the event log and status always, plus one GitHub issue per gate when feedback uses GitHub."""
    notes = [Notification("event_log", f"{gate} is open for review", gate), Notification("status", f"{gate} is open", gate)]
    if feedback_channel == "github":
        notes.append(Notification("github_issue", f"{gate} review ({', '.join(people)})", gate))
    return notes
