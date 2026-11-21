"""The live job driver: one AWS Transform job from creation to retrieved requirements (P1-05, #234; polling, #263).

What it does, in order, with no person unless something is parked:
1. Creates the project's one job, or resumes the one already recorded (FR-14). A second job, a changed
   snapshot or a changed scope is refused; a creation whose outcome is unknown is settled first.
2. Polls the job every 60 seconds from creation (P2-10), so each setup question AWS asks is answered
   within one interval. AWS stops a job's agent when a question waits too long (HTTP 409, live
   20 November 2026), and that job cannot be restarted.
3. Classifies every open form and chat question (section 4, aws_reviews) and sends the answer once.
   Anything parked waits for a person; the run then exits WAITING_HUMAN and a rerun resumes.
4. When AWS reports the job COMPLETED, retrieves requirements.md and traceability.yaml for each
   function, unchanged, with their SHA-256, linked to the source snapshot, status NOT_CHECKED.

Every change follows the uncertain-dispatch rules (section 4): its intent is written before the call
and its receipt after, nothing is ever re-sent automatically, an intent without a receipt is UNCERTAIN,
and a refusal keeps AWS's reason and stops the run. Each change is counted against the execution
envelope's limits. Evidence stays in the local project folder (mode 700, files 600), never in GitHub.

Shapes this module relies on, and where they were seen:
- the detailed status snapshot (job.job.statusDetails.status, plan.steps, tasks.hitlTasks,
  messages.messages): the pinned server's get_job_status, and P1 stage D, 20 November 2026;
- terminal statuses COMPLETED, FAILED and STOPPED: the pinned server's own list;
- artifacts and assets from list_resources, and get_resource asset with connectorId, assetKey,
  savePath and fileName: the pinned server's schemas;
- requirements delivered inside spec_gen/spec_gen_specs_<timestamp>.zip at
  spec/<Domain>/<Function>/: v1's live job, 17 November 2026 (docs/validation/acceptance-defects.md).
"""

from __future__ import annotations

import enum
import json
import os
import re
import secrets
import time
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Callable

from reframe_v2.aws_reviews import (FUNCTION_SELECTION_QUESTIONS, ChatQuestion, Class, Decision, Form, Intake, classify_chat, classify_form,
                                    closing_line, fits_schema, menu_options, needs_answer)
from reframe_v2.intake import IntakeError, read_zip, sha256
from reframe_v2.transform import Authorization, NotSent, Rejected, TransformError

ENVELOPE = "p1-live-path r5"
"""The execution envelope every change is authorized under (docs/v2/envelopes/p1-live-path.md)."""

ORCHESTRATOR_AGENT = "mainframe-modernization-agent-v2"
"""The orchestratorAgent AWS accepted for an Assess and reimagine job: v1's receipt (#173) and both create_job
receipts of P1 stage D (20 November 2026). Never guessed; a different plan needs its own recorded value."""

LIMITS = {"create_job": 1, "send_message": 15, "complete_task": 15}
"""Changes the envelope allows for one job."""

POLL_SECONDS = 60
JOB_LIMIT_SECONDS = 8 * 3600
TERMINAL = frozenset({"COMPLETED", "FAILED", "STOPPED"})
"""The pinned server's terminal job statuses."""
OPEN_TASK = frozenset({"AWAITING_HUMAN_INPUT", "AWAITING_APPROVAL"})
"""Task statuses that wait for an answer (the pinned server's actionable statuses, without IN_PROGRESS)."""
REQUIREMENTS_FILE = "requirements.md"
TRACEABILITY_FILES = ("traceability.yaml", "traceability.yml")
MAX_FOLDERS = 1000
MAX_ITEMS = 10_000
MEMBER_LIMIT = 50 * 1024 * 1024
RUN_ID = re.compile(r"^RUN-[0-9a-f]{16}$")


class Outcome(enum.Enum):
    RETRIEVED = "RETRIEVED"
    WAITING_HUMAN = "WAITING_HUMAN"
    WAITING_EXTERNAL = "WAITING_EXTERNAL"
    REFUSED = "REFUSED"
    UNCERTAIN = "UNCERTAIN"


@dataclass(frozen=True)
class Result:
    outcome: Outcome
    message: str
    detail: dict[str, Any] = field(default_factory=dict)


class Stop(Exception):
    def __init__(self, outcome: Outcome, message: str) -> None:
        super().__init__(message)
        self.outcome, self.message = outcome, message


@dataclass(frozen=True)
class Settings:
    workspace_id: str
    source_uri: str
    """The S3 URI of the source copy the job reads; given to AWS's source-location form."""
    source_sha256: str
    """The snapshot archive's hash, "sha256:<hex>"; a different one is a changed snapshot (FR-14)."""
    snapshot_id: str
    commit: str
    intake: Intake
    by: str
    """Who started the run; recorded on every change."""
    job_limit_seconds: int = JOB_LIMIT_SECONDS


class ProjectFolder:
    """The local project folder: private, every JSON record written whole, originals written once."""

    def __init__(self, root: Path) -> None:
        self.root = root
        root.mkdir(parents=True, exist_ok=True, mode=0o700)
        root.chmod(0o700)

    def path(self, name: str) -> Path:
        path = (self.root / name).resolve()
        if self.root.resolve() not in path.parents:
            raise ValueError(f"{name} is outside the project folder")
        return path

    def save(self, name: str, value: Any) -> None:
        path = self.path(name)
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        temporary = path.with_name(path.name + ".tmp")
        temporary.write_text(json.dumps(value, indent=1, sort_keys=True) + "\n")
        temporary.chmod(0o600)
        os.replace(temporary, path)

    def load(self, name: str, default: Any = None) -> Any:
        path = self.path(name)
        return json.loads(path.read_text()) if path.exists() else default

    def exists(self, name: str) -> bool:
        return self.path(name).exists()

    def remove(self, name: str) -> None:
        self.path(name).unlink()

    def rename(self, name: str, new: str) -> None:
        os.replace(self.path(name), self.path(new))

    def write_original(self, name: str, data: bytes) -> None:
        """Store an AWS original once and unchanged. A different existing copy is an integrity failure."""
        path = self.path(name)
        if path.exists():
            if path.read_bytes() != data:
                raise Stop(Outcome.REFUSED, f"{name} is already stored with different content; the stored copy is kept")
            return
        path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        path.write_bytes(data)
        path.chmod(0o400)

    def event(self, kind: str, at: float, **detail: Any) -> None:
        path = self.path("events.jsonl")
        with path.open("a") as log:
            log.write(json.dumps({"at": _iso(at), "event": kind, **detail}, sort_keys=True) + "\n")
        path.chmod(0o600)


def _iso(moment: float) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(moment))


def job_status(snapshot: dict[str, Any]) -> str:
    """The job's status from a detailed snapshot. The server's own _pollingGuidance reads the wrong level
    (it reported UNKNOWN for an EXECUTING job live), so it is not used."""
    job = snapshot.get("job") or {}
    job = job.get("job", job) if isinstance(job, dict) else {}
    details = job.get("statusDetails") if isinstance(job, dict) else None
    status = (details or {}).get("status") if isinstance(details, dict) else details
    return str(status or job.get("status") or "UNKNOWN").upper()


def open_tasks(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    container = snapshot.get("tasks") or {}
    tasks = container.get("hitlTasks", []) if isinstance(container, dict) else container
    return [t for t in tasks or [] if isinstance(t, dict) and t.get("status") in OPEN_TASK and t.get("taskId")]


def open_question(snapshot: dict[str, Any]) -> dict[str, Any] | None:
    """AWS's latest finished chat turn, when no one has answered it and it asks something (v1's live rule)."""
    container = snapshot.get("messages") or {}
    messages = [m for m in (container.get("messages") if isinstance(container, dict) else container) or [] if isinstance(m, dict)]
    final = [m for m in messages if m.get("messageOrigin") == "SYSTEM"
             and (m.get("processingInfo") or {}).get("messageType") == "FINAL_RESPONSE"]
    if not final:
        return None
    latest = max(final, key=lambda m: str(m.get("createdAt", "")))
    answered = any(m.get("messageOrigin") != "SYSTEM" and str(m.get("createdAt", "")) > str(latest.get("createdAt", ""))
                   for m in messages)
    text = str(latest.get("text") or "").strip()
    return None if answered or not latest.get("messageId") or not needs_answer(text) else latest


def _mentions(value: Any, name: str) -> bool:
    """Whether AWS's own records name a function exactly, as a whole JSON string or a line of text."""
    if isinstance(value, str):
        return value.strip() == name or any(line.strip(" -*\t").split(":")[0].strip() == name for line in value.splitlines())
    if isinstance(value, dict):
        return any(_mentions(item, name) for item in value.values())
    if isinstance(value, list):
        return any(_mentions(item, name) for item in value)
    return False


class JobDriver:
    def __init__(self, client, folder: ProjectFolder, settings: Settings, *,
                 clock: Callable[[], float] = time.time, sleep: Callable[[float], None] = time.sleep) -> None:
        self.client, self.folder, self.settings = client, folder, settings
        self.clock, self.sleep = clock, sleep
        self.state: dict[str, Any] = folder.load("job.json") or {"counts": {}}

    # ---- the run -------------------------------------------------------------------------------

    def run(self, new_assessment: bool = False) -> Result:
        try:
            self._check_resumable(new_assessment)
            self._ensure_job()
            while True:
                if self.state.get("retrieved"):
                    return Result(Outcome.RETRIEVED, "requirements and traceability are retrieved and stored", self.state["retrieved"])
                if self.clock() - self.state["created_at"] > self.settings.job_limit_seconds:
                    raise Stop(Outcome.WAITING_HUMAN, "the job's 8-hour limit is reached. Reframe stops polling and does not stop the job; "
                                                      "stop it in the AWS Transform console if it should not continue")
                wait = self.state.get("last_poll", 0) + POLL_SECONDS - self.clock()
                if wait > 0:
                    self.sleep(wait)
                summary = self.poll_once()
                if summary["status"] == "COMPLETED":
                    self.retrieve()
                elif summary["status"] in TERMINAL:
                    raise Stop(Outcome.WAITING_HUMAN, f"AWS ended the job as {summary['status']}; nothing was retrieved")
                elif summary["park"]:
                    raise Stop(Outcome.WAITING_HUMAN, "; ".join(summary["park"]))
        except Stop as stop:
            self.state["outcome"] = {"outcome": stop.outcome.value, "message": stop.message, "at": _iso(self.clock())}
            self._save()
            self.folder.event("run_stopped", self.clock(), outcome=stop.outcome.value, message=stop.message)
            return Result(stop.outcome, stop.message)

    def _check_resumable(self, new_assessment: bool) -> None:
        if self.state.get("uncertain"):
            raise Stop(Outcome.UNCERTAIN, f"{self.state['uncertain']} is UNCERTAIN; settle it from AWS's own state "
                                          "with reframe resolve before anything else")
        if new_assessment:
            raise Stop(Outcome.REFUSED, "the P1 envelope allows one job; --new-assessment is outside it")
        recorded = self.state.get("source")
        if recorded:
            changed = [name for name, now in (("snapshot", self.settings.source_sha256),
                                              ("scope", sorted(self.settings.intake.scope_functions)),
                                              ("scope mode", self.settings.intake.scope_mode))
                       if recorded.get(name) != now]
            if changed:
                raise Stop(Outcome.REFUSED, "the " + " and ".join(changed) + " changed since this project's job was created; "
                                            "a changed snapshot or scope needs --new-assessment (FR-14)")

    def _ensure_job(self) -> None:
        if self.state.get("job_id"):
            self.folder.event("resumed", self.clock(), polls=self.state.get("polls", 0))
            return
        settings = self.settings
        self.state.setdefault("run_id", "RUN-" + secrets.token_hex(8))
        self.state.update(workspace_id=settings.workspace_id,
                          source={"snapshot": settings.source_sha256, "snapshot_id": settings.snapshot_id, "uri": settings.source_uri,
                                  "commit": settings.commit, "scope": sorted(settings.intake.scope_functions),
                                  "scope mode": settings.intake.scope_mode})
        self._save()
        arguments = {"workspaceId": settings.workspace_id, "jobName": self.state["run_id"],
                     "objective": (f"{settings.intake.plan} for the source archive at {settings.source_uri} (commit {settings.commit}), "
                                   "and generate requirements with traceability for the business functions selected in this job."),
                     "intent": "Generate business requirements for the selected business functions.",
                     "orchestratorAgent": ORCHESTRATOR_AGENT}
        receipt = self._change("create-job", "create_job", arguments)
        job_id = _find_job_id(receipt)
        if not job_id:
            self.state["uncertain"] = "create-job (the receipt names no job)"
            self._save()
            raise Stop(Outcome.UNCERTAIN, "create_job returned no job id; settle it from AWS's job listing")
        self.state.update(job_id=job_id, created_at=self.clock())
        self._save()

    # ---- one poll ------------------------------------------------------------------------------

    def poll_once(self) -> dict[str, Any]:
        """One detailed status read, then every open form and the open chat question, each answered at most once."""
        identity = self._identity()
        self.state["last_poll"] = self.clock()
        snapshot = self._read("get_job_status", {**identity, "detailed": True})
        number = self.state.get("polls", 0) + 1
        self.state["polls"] = number
        self.folder.save(f"snapshots/{number:04d}.json", snapshot)
        status = job_status(snapshot)
        summary: dict[str, Any] = {"poll": number, "at": _iso(self.clock()), "status": status, "answered": [], "park": [],
                                   "steps": [{"name": s.get("stepName"), "status": s.get("status")}
                                             for s in ((snapshot.get("plan") or {}).get("steps") or []) if isinstance(s, dict)]}
        blocking_parked = blocking_open = False
        for task in open_tasks(snapshot):
            blocking_open |= task.get("blockingType") != "NON_BLOCKING"
            parked = self._task(task, summary)
            blocking_parked |= parked and task.get("blockingType") != "NON_BLOCKING"
        # AWS's chat asks Reframe something only when AWS says the job awaits input, or when no step is running
        # (v1's live rule, 17 November 2026). While a step runs, AWS also posts open offers such as "What would
        # you like to know about your codebase?" after its code analysis (live, 21 November 2026); the job does not
        # wait on them, so they are recorded and left unanswered.
        question = open_question(snapshot)
        if question is not None:
            awaiting = status == "AWAITING_HUMAN_INPUT"
            running = any(str(step.get("status")) == "IN_PROGRESS" for step in summary["steps"])
            if awaiting or not running:
                # With a blocking form open, the form explains the wait; an unrecognized chat message does not park.
                self._question(question, snapshot, summary, may_park=not (awaiting and blocking_open))
            else:
                self._note(question, "AWS posted in chat while a step runs; the job does not wait on it", summary)
        # A blocking form Reframe cannot answer stops the run only when nothing was answered in this poll or
        # the one before: answering the chat (the function selection) can close a form AWS opened alongside it.
        if blocking_parked and not summary["answered"] and not self.state.get("answered_last_poll"):
            summary["park"].append("a blocking AWS form waits for a person")
        self.state["answered_last_poll"] = bool(summary["answered"])
        self.state["status"] = status
        self._save()
        self.folder.save("latest.json", summary)
        self.folder.event("poll", self.clock(), number=number, status=status, answered=len(summary["answered"]), parked=len(summary["park"]))
        return summary

    def _task(self, task: dict[str, Any], summary: dict[str, Any]) -> bool:
        """Classify one open form and answer it if its class allows. True when it stays parked."""
        task_id = str(task["taskId"])
        step = f"task-{task_id}"
        if self.folder.exists(f"changes/{step}.receipt.json"):
            return False
        # A form's detail is read once; a parked form is not read again on every poll.
        detail = self.folder.load(f"tasks/{task_id}.json")
        if detail is None:
            detail = self._read("get_resource", {**self._identity(), "resource": "task", "taskId": task_id})
            self.folder.save(f"tasks/{task_id}.json", detail)
        body = detail.get("task", detail) if isinstance(detail, dict) else {}
        form = Form(task_id, str(body.get("title") or task.get("title") or ""), body.get("uxComponentId") or task.get("uxComponentId"),
                    body.get("_outputSchema") or {})
        decision = classify_form(form, self.settings.intake)
        record = {"task": task_id, "title": form.title, "component": form.component, "class": decision.cls.value,
                  "reason": decision.reason, "blocking": task.get("blockingType")}
        self.folder.event("task_classified", self.clock(), **record)
        if decision.cls in (Class.ANSWER_FROM_INTAKE, Class.APPROVE_ONLY):
            if not fits_schema(form.schema, decision.response):
                summary["park"].append(f"the answer for {form.title!r} does not fit its own schema")
                return True
            self._change(step, "complete_task", {**self._identity(), "taskId": task_id, "content": json.dumps(decision.response),
                                                 "action": "APPROVE"},
                         note={"class": decision.cls.value, "evidence_status": decision.evidence_status})
            summary["answered"].append({**record, "how": "from intake" if decision.cls is Class.ANSWER_FROM_INTAKE
                                        else "approved by Reframe, not reviewed by a person (NOT_CHECKED)"})
            return False
        if decision.cls is Class.DISPLAY_ONLY:
            return False
        summary.setdefault("parked_tasks", []).append(record)
        return True

    def _note(self, message: dict[str, Any], reason: str, summary: dict[str, Any]) -> None:
        message_id = str(message["messageId"])
        if message_id not in self.state.setdefault("noted", []):
            self.state["noted"].append(message_id)
            self.folder.event("chat_noted", self.clock(), message=message_id, reason=reason)
        summary.setdefault("noted", []).append({"message": message_id, "reason": reason})

    def _question(self, message: dict[str, Any], snapshot: dict[str, Any], summary: dict[str, Any], may_park: bool = True) -> None:
        message_id = str(message["messageId"])
        step = f"reply-{message_id}"
        if self.folder.exists(f"changes/{step}.receipt.json"):
            return
        text = str(message.get("text") or "")
        options = tuple(label for _, label in menu_options(text))
        decision = classify_chat(ChatQuestion(message_id, text, options), self.settings.intake)
        if decision.cls is Class.PARK and not options and closing_line(text) in FUNCTION_SELECTION_QUESTIONS:
            decision = self._select_functions(message_id, text, snapshot)
        record = {"message": message_id, "class": decision.cls.value, "reason": decision.reason}
        self.folder.event("chat_classified", self.clock(), **record)
        reply = (decision.response or {}).get("text") if decision.cls in (Class.ANSWER_FROM_INTAKE, Class.APPROVE_ONLY) else None
        if not reply and not may_park:
            self._note(message, f"not answered ({decision.reason}); a blocking AWS form explains the wait", summary)
            return
        if not reply:
            summary["park"].append(f"AWS asks in chat and Reframe cannot answer it ({decision.reason}). "
                                   "Answer it in the AWS Transform console soon: AWS stops a job whose question waits too long")
            summary["question"] = {**record, "text": text}
            return
        self._change(step, "send_message", {**self._identity(), "text": reply, "skipPolling": True},
                     note={"class": decision.cls.value, "evidence_status": decision.evidence_status})
        summary["answered"].append({**record, "reply": reply})

    def _select_functions(self, message_id: str, text: str, snapshot: dict[str, Any]):
        """AWS asks for the functions in chat and lists its catalog in the review form, whose shape it does not publish
        (v1, 17 November 2026). Each function the scope names is sent only when AWS's own records name it exactly."""
        intake = self.settings.intake
        if intake.scope_mode != "list" or not intake.scope_functions:
            return Decision(Class.PARK, "AWS lists no selectable catalog and the scope does not name the functions; a person selects")
        records = [snapshot] + [self.folder.load(f"tasks/{t['taskId']}.json") for t in open_tasks(snapshot)
                                if self.folder.exists(f"tasks/{t['taskId']}.json")]
        missing = [name for name in intake.scope_functions if not _mentions(records, name)]
        if missing:
            return Decision(Class.PARK, "AWS's own records do not name " + ", ".join(missing) + " exactly; a person selects")
        selected = list(intake.scope_functions)
        return Decision(Class.ANSWER_FROM_INTAKE, "function selection answered from the recorded scope, by AWS's exact names",
                        {"selected": selected, "text": ", ".join(selected)})

    # ---- retrieval -----------------------------------------------------------------------------

    def retrieve(self) -> dict[str, Any]:
        """Find the job's requirements and traceability, download them through the server, and store them unchanged."""
        identity = self._identity()
        listing = self._list_outputs(identity)
        self.folder.save("outputs/listing.json", listing)
        loose = [a for a in listing["assets"] if PurePosixPath(a["assetKey"]).name.casefold() in (REQUIREMENTS_FILE, *TRACEABILITY_FILES)]
        originals: list[dict[str, Any]] = []
        if loose:
            for asset in loose:
                data = self._download(identity, asset)
                originals.append(self._original(asset["assetKey"], PurePosixPath(asset["assetKey"]).parent.name, data))
        else:
            archives = sorted((a for a in listing["assets"] if PurePosixPath(a["assetKey"]).parent.name == "spec_gen"
                               and PurePosixPath(a["assetKey"]).name.startswith("spec_gen_specs") and a["assetKey"].endswith(".zip")),
                              key=lambda a: str(a.get("createdTimestamp") or a.get("lastModified") or a["assetKey"]))
            if not archives:
                raise Stop(Outcome.WAITING_HUMAN, "the completed job lists no requirements.md, traceability.yaml or spec_gen archive; "
                                                  "nothing was retrieved")
            archive = archives[-1]
            data = self._download(identity, archive)
            name = f"outputs/originals/{sha256(data)[7:23]}-{PurePosixPath(archive['assetKey']).name}"
            self.folder.write_original(name, data)
            try:
                members = read_zip(data)
            except IntakeError as error:
                raise Stop(Outcome.REFUSED, f"the requirements archive is refused: {error}") from None
            for member, content in sorted(members.items()):
                path = PurePosixPath(member)
                if path.name.casefold() not in (REQUIREMENTS_FILE, *TRACEABILITY_FILES):
                    continue
                if len(content) > MEMBER_LIMIT:
                    raise Stop(Outcome.REFUSED, f"{member} in the requirements archive is larger than 50 MB")
                originals.append(self._original(f"{archive['assetKey']}!/{member}", path.parent.name, content))
            self.state["archive"] = {"asset_key": archive["assetKey"], "sha256": sha256(data), "bytes": len(data), "stored": name}
        if not any(o["kind"] == "requirements" for o in originals):
            raise Stop(Outcome.WAITING_HUMAN, "the job's outputs hold no requirements.md; nothing was retrieved")
        retrieved = {"snapshot": self.settings.source_sha256, "snapshot_id": self.settings.snapshot_id, "status": "NOT_CHECKED",
                     "functions": sorted({o["function"] for o in originals}), "files": originals, "at": _iso(self.clock())}
        self.folder.save("outputs/requirements.json", retrieved)
        self.state["retrieved"] = {"functions": retrieved["functions"], "files": len(originals), "status": "NOT_CHECKED"}
        self._save()
        self.folder.event("retrieved", self.clock(), files=len(originals), functions=len(retrieved["functions"]))
        return retrieved

    def _original(self, original_path: str, function: str, data: bytes) -> dict[str, Any]:
        kind = "requirements" if PurePosixPath(original_path).name.casefold() == REQUIREMENTS_FILE else "traceability"
        digest = sha256(data)
        stored = f"outputs/originals/{digest[7:23]}-{PurePosixPath(original_path).name}"
        self.folder.write_original(stored, data)
        return {"function": function, "kind": kind, "original_path": original_path, "sha256": digest, "bytes": len(data),
                "stored": stored, "status": "NOT_CHECKED"}

    def _list_outputs(self, identity: dict[str, str]) -> dict[str, Any]:
        """Every asset under this job's own output folders, following only folders AWS returned."""
        roots = (f"transform-output/{identity['jobId']}/", f"AWSTransform/Workspaces/{identity['workspaceId']}/Jobs/{identity['jobId']}/")
        queue: list[str | None] = [None]
        seen: set[str | None] = set()
        merged: dict[str, Any] = {"assets": [], "artifacts": []}
        while queue:
            prefix = queue.pop(0)
            if prefix in seen:
                continue
            seen.add(prefix)
            if len(seen) > MAX_FOLDERS:
                raise Stop(Outcome.REFUSED, f"the job's outputs have more than {MAX_FOLDERS} folders")
            arguments = {**identity, "resource": "artifacts"}
            if prefix is not None:
                arguments["pathPrefix"] = prefix
            listing = self._read("list_resources", arguments)
            connector = listing.get("connectorId")
            for asset in listing.get("assets") or []:
                key = asset.get("assetKey") if isinstance(asset, dict) else None
                if not isinstance(key, str) or not key.startswith(roots) or ".." in key.split("/"):
                    raise Stop(Outcome.REFUSED, "AWS listed an output outside this job's folders; nothing was downloaded")
                merged["assets"].append({**asset, "connectorId": asset.get("connectorId") or connector})
            merged["artifacts"].extend(listing.get("artifacts") or [])
            for folder in listing.get("folders") or []:
                if not isinstance(folder, str) or not folder.startswith(roots) or not folder.endswith("/") or ".." in folder.split("/"):
                    raise Stop(Outcome.REFUSED, "AWS listed a folder outside this job's outputs; nothing was downloaded")
                if folder not in seen and folder not in queue:
                    queue.append(folder)
            if len(merged["assets"]) + len(merged["artifacts"]) > MAX_ITEMS:
                raise Stop(Outcome.REFUSED, f"the job's outputs list more than {MAX_ITEMS} items")
        return merged

    def _download(self, identity: dict[str, str], asset: dict[str, Any]) -> bytes:
        """The server saves the file under its write folder (AWS_TRANSFORM_MCP_WRITE_DIR); Reframe reads it from there."""
        if not asset.get("connectorId"):
            raise Stop(Outcome.WAITING_HUMAN, f"AWS names no connector for {PurePosixPath(asset['assetKey']).name}; it cannot be downloaded")
        base = Path(self.client.config.write_dir).resolve()
        name = secrets.token_hex(8) + "-" + PurePosixPath(asset["assetKey"]).name
        reply = self._read("get_resource", {**identity, "resource": "asset", "connectorId": asset["connectorId"],
                                            "assetKey": asset["assetKey"], "savePath": str(base / "downloads") + "/", "fileName": name})
        saved = Path(str((reply or {}).get("savedTo") or base / "downloads" / name)).resolve()
        if base not in saved.parents or not saved.is_file() or saved.is_symlink():
            raise Stop(Outcome.WAITING_EXTERNAL, f"the download of {PurePosixPath(asset['assetKey']).name} produced no file")
        data = saved.read_bytes()
        saved.unlink()
        return data

    # ---- calls ---------------------------------------------------------------------------------

    def _identity(self) -> dict[str, str]:
        return {"workspaceId": self.state["workspace_id"], "jobId": self.state["job_id"]}

    def _read(self, operation: str, arguments: dict[str, Any]) -> Any:
        try:
            return self.client.session([(operation, arguments, None)])[0]
        except TransformError as error:
            reason = error.reason if isinstance(error, Rejected) else str(error)
            raise Stop(Outcome.WAITING_EXTERNAL, f"the read {operation} failed ({reason[:300]}). If the AWS sign-in expired, "
                                                 "sign in again and rerun; nothing was retried") from None

    def _change(self, step: str, operation: str, arguments: dict[str, Any], note: dict[str, Any] | None = None) -> Any:
        """One counted change: intent first, receipt after, never twice, within the envelope's limit."""
        folder = self.folder
        receipt = folder.load(f"changes/{step}.receipt.json")
        if receipt is not None:
            return receipt
        if folder.exists(f"changes/{step}.rejected.json"):
            raise Stop(Outcome.REFUSED, f"{step}: AWS refused it before; another attempt needs a person (reframe resolve)")
        if folder.exists(f"changes/{step}.intent.json"):
            self.state["uncertain"] = step
            self._save()
            raise Stop(Outcome.UNCERTAIN, f"{step}: an intent is recorded without a receipt; it is UNCERTAIN")
        used = self.state["counts"].get(operation, 0)
        if used >= LIMITS[operation]:
            raise Stop(Outcome.REFUSED, f"{operation} has reached the envelope's limit of {LIMITS[operation]}")
        folder.save(f"changes/{step}.intent.json", {"operation": operation, "arguments": arguments, "by": self.settings.by,
                                                    "envelope": ENVELOPE, "at": _iso(self.clock()), **(note or {})})
        self.state["counts"][operation] = used + 1
        self._save()
        try:
            result = self.client.session([(operation, arguments, Authorization(ENVELOPE, operation, self.settings.by))])[0]
        except NotSent as error:
            folder.remove(f"changes/{step}.intent.json")
            self.state["counts"][operation] = used
            self._save()
            folder.event("change_not_sent", self.clock(), step=step, operation=operation)
            raise Stop(Outcome.WAITING_EXTERNAL, f"{operation} was not sent ({str(error)[:300]}); sign in again if needed and rerun") from None
        except Rejected as error:
            folder.save(f"changes/{step}.rejected.json", {"operation": operation, "reason": error.reason, "at": _iso(self.clock())})
            folder.rename(f"changes/{step}.intent.json", f"changes/{step}.rejected-intent.json")
            folder.event("change_rejected", self.clock(), step=step, operation=operation)
            raise Stop(Outcome.REFUSED, f"AWS refused {operation}: {error.reason[:300]}") from None
        except TransformError as error:
            folder.save(f"changes/{step}.error.json", {"operation": operation, "error": str(error)[:600]})
            self.state["uncertain"] = step
            self._save()
            raise Stop(Outcome.UNCERTAIN, f"{operation} may or may not have reached AWS; it is UNCERTAIN and not retried") from None
        folder.save(f"changes/{step}.receipt.json", result)
        folder.event("change", self.clock(), step=step, operation=operation, by=self.settings.by)
        return result

    def _save(self) -> None:
        self.folder.save("job.json", self.state)


def _find_job_id(value: Any) -> str | None:
    for _ in range(6):
        if not isinstance(value, dict):
            return None
        if isinstance(value.get("jobId"), str):
            return value["jobId"]
        value = value.get("job") or value.get("data")
    return None
