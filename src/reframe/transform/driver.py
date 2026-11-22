"""Stages 5 and 6: create the job and drive it to the end (specification section 4).

Built on the earlier build's job driver, with what spike 1 showed:
- AWS asks its setup questions in chat one at a time and stops a job whose question waits too long, so the
  job is polled every minute from creation;
- the business function catalog is a chat message with a SELECT interaction; it is answered with a
  structured reply (SendMessage with interactionResults), never through the console;
- the job's own status stays EXECUTING while a non-blocking form is open, so the job is done when every plan
  step has SUCCEEDED and the plan includes "Generate requirements".

A question that waits for the person (interactive mode, or one Reframe cannot answer) is written to
question.json; the driver keeps polling, and sends the answer once reframe answer writes it. Every answer
goes through Changes.apply, so it is sent once, and every autonomous one is recorded in decisions.json.
"""

from __future__ import annotations

import json
import time
import uuid
from typing import Any, Callable

from reframe.core.errors import NotSent, Outcome, Rejected, Stop
from reframe.core.runfolder import Changes, RunFolder, iso
from reframe.transform import answers
from reframe.transform.answers import Answer, Question

ORCHESTRATOR_AGENT = "mainframe-modernization-agent-v2"
"""The orchestratorAgent AWS accepted for an Assess and reimagine job (every create_job receipt so far)."""
POLL_SECONDS = 60
JOB_LIMIT_SECONDS = 10 * 3600
FAILED_JOB = frozenset({"FAILED", "STOPPED"})
OPEN_TASK = frozenset({"AWAITING_HUMAN_INPUT", "AWAITING_APPROVAL"})
FINAL_STEP = "Generate requirements"
SNAPSHOT_EVERY = 10


def job_status(snapshot: dict[str, Any]) -> str:
    job = snapshot.get("job") or {}
    job = job.get("job", job) if isinstance(job, dict) else {}
    details = job.get("statusDetails") if isinstance(job, dict) else None
    status = (details or {}).get("status") if isinstance(details, dict) else details
    return str(status or job.get("status") or "UNKNOWN").upper()


def plan_steps(snapshot: dict[str, Any]) -> list[dict[str, str]]:
    return [{"name": str(s.get("stepName")), "status": str(s.get("status"))}
            for s in ((snapshot.get("plan") or {}).get("steps") or []) if isinstance(s, dict)]


def is_done(steps: list[dict[str, str]]) -> bool:
    return bool(steps) and any(s["name"] == FINAL_STEP for s in steps) and all(s["status"] == "SUCCEEDED" for s in steps)


def open_tasks(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    container = snapshot.get("tasks") or {}
    tasks = container.get("hitlTasks", []) if isinstance(container, dict) else container
    return [t for t in tasks or [] if isinstance(t, dict) and t.get("status") in OPEN_TASK and t.get("taskId")]


def latest_unanswered(messages: list[dict[str, Any]]) -> dict[str, Any] | None:
    """AWS's latest finished chat turn, when nothing has been said after it."""
    final = [m for m in messages if m.get("messageOrigin") == "SYSTEM"
             and (m.get("processingInfo") or {}).get("messageType") in ("FINAL_RESPONSE", None)
             and (m.get("text") or m.get("interactions"))]
    if not final:
        return None
    latest = max(final, key=lambda m: str(m.get("createdAt", "")))
    later = [m for m in messages if m.get("messageOrigin") != "SYSTEM" and str(m.get("createdAt", "")) > str(latest.get("createdAt", ""))]
    return None if later or not latest.get("messageId") else latest


class Driver:
    def __init__(self, client, api, folder: RunFolder, changes: Changes, *, workspace_id: str, job_name: str, source_uri: str,
                 mode: str, clock: Callable[[], float] = time.time, sleep: Callable[[float], None] = time.sleep) -> None:
        self.client, self.api, self.folder, self.changes = client, api, folder, changes
        self.workspace_id, self.job_name, self.source_uri, self.mode = workspace_id, job_name, source_uri, mode
        self.clock, self.sleep = clock, sleep
        self.state: dict[str, Any] = folder.load("job.json") or {}

    # ---- the run -------------------------------------------------------------------------------

    def run(self) -> dict[str, Any]:
        self._ensure_job()
        while True:
            if self.clock() - self.state["created_at"] > JOB_LIMIT_SECONDS:
                raise Stop(Outcome.FAILED, "the job has run for 10 hours; Reframe stops polling and leaves the job as it is")
            wait = self.state.get("last_poll", 0) + POLL_SECONDS - self.clock()
            if wait > 0:
                self.sleep(wait)
            summary = self.poll_once()
            if summary["done"]:
                self.folder.remove("question.json")
                self.folder.event("job_done", steps=len(summary["steps"]))
                return summary
            if summary["status"] in FAILED_JOB:
                raise Stop(Outcome.FAILED, f"AWS ended the job as {summary['status']}")
            failed = [s["name"] for s in summary["steps"] if s["status"] == "FAILED"]
            if failed:
                raise Stop(Outcome.FAILED, "AWS reports failed steps: " + ", ".join(failed))

    def _ensure_job(self) -> None:
        if self.state.get("job_id"):
            return

        def find():
            listing = self.client.call("list_resources", {"resource": "jobs", "workspaceId": self.workspace_id})
            match = [j for j in (listing.get("items", []) if isinstance(listing, dict) else [])
                     if (j.get("jobName") or j.get("name")) == self.job_name]
            return match[0] if match else None

        arguments = {"workspaceId": self.workspace_id, "jobName": self.job_name,
                     "objective": (f"{answers.PLAN} for the uploaded source archive, and generate requirements with traceability "
                                   "for every business function found in it."),
                     "intent": "Generate business requirements for the whole source.",
                     "orchestratorAgent": ORCHESTRATOR_AGENT}
        receipt = self.changes.apply("job", "create_job", {"workspaceId": self.workspace_id, "jobName": self.job_name},
                                     lambda: self.client.change("create_job", arguments), find)
        job_id = _find_job_id(receipt)
        if not job_id:
            raise Stop(Outcome.UNCERTAIN, "create_job returned no job id; check the workspace's jobs")
        self.state.update(job_id=job_id, created_at=self.clock(), polls=0)
        self._save()
        self.folder.update(transform={**(self.folder.state.get("transform") or {}), "job_id": job_id})
        self.folder.event("job_created")

    # ---- one poll ------------------------------------------------------------------------------

    def poll_once(self) -> dict[str, Any]:
        identity = self._identity()
        self.state["last_poll"] = self.clock()
        snapshot = self._read(lambda: self.client.call("get_job_status", {**identity, "detailed": True}), "get_job_status")
        number = self.state.get("polls", 0) + 1
        self.state["polls"] = number
        if number % SNAPSHOT_EVERY == 1:
            self.folder.save(f"snapshots/{number:04d}.json", snapshot)
        self.folder.save("snapshots/latest.json", snapshot)
        status, steps = job_status(snapshot), plan_steps(snapshot)
        summary: dict[str, Any] = {"poll": number, "at": iso(self.clock()), "status": status, "steps": steps,
                                   "done": is_done(steps), "answered": [], "waiting": None}
        if summary["done"]:
            self._finish_poll(summary)
            return summary
        for task in open_tasks(snapshot):
            self._task(task, summary)
        running = any(s["status"] == "IN_PROGRESS" for s in steps)
        if status == "AWAITING_HUMAN_INPUT" or not running or self.folder.exists("question.json"):
            self._chat(summary, awaiting=status == "AWAITING_HUMAN_INPUT")
        self._finish_poll(summary)
        return summary

    def _finish_poll(self, summary: dict[str, Any]) -> None:
        self.state["status"] = summary["status"]
        self._save()
        self.folder.save("latest.json", summary)
        self.folder.update(job={"status": summary["status"], "steps": summary["steps"], "poll": summary["poll"], "at": summary["at"]})
        self.folder.event("poll", number=summary["poll"], status=summary["status"], answered=len(summary["answered"]),
                          waiting=bool(summary["waiting"]))

    # ---- forms ---------------------------------------------------------------------------------

    def _task(self, task: dict[str, Any], summary: dict[str, Any]) -> None:
        task_id = str(task["taskId"])
        step = f"task-{task_id}"
        if self.changes.receipt(step) is not None or task_id in self.state.setdefault("ignored_tasks", []):
            return
        detail = self.folder.load(f"tasks/{task_id}.json")
        if detail is None:
            detail = self._read(lambda: self.client.call("get_resource", {**self._identity(), "resource": "task", "taskId": task_id}),
                                "get_resource task")
            self.folder.save(f"tasks/{task_id}.json", detail)
        body = detail.get("task", detail) if isinstance(detail, dict) else {}
        component = body.get("uxComponentId") or task.get("uxComponentId")
        schema = body.get("_outputSchema") or {}
        title = str(body.get("title") or task.get("title") or "")
        decision = answers.form_decision(component, schema, task.get("blockingType"), self.source_uri)
        self.folder.event("task_seen", task=task_id, title=title, component=component, action=decision.action, reason=decision.reason)
        if decision.action == "ignore":
            self.state["ignored_tasks"].append(task_id)
            return
        if decision.action == "approve" and self.mode == "interactive":
            decision = answers.FormDecision("ask", "an approval; interactive mode asks the person")
        if decision.action == "ask":
            answer = self._waiting(Question(f"task-{task_id}", "form", f"{title}\n\nAWS's form expects: {json.dumps(schema)[:1500]}",
                                            ("Approve",) if not (schema.get("required")) else (), ("{}",) if not schema.get("required") else (),
                                            schema=schema), summary)
            if answer is None:
                return
            try:
                content = json.loads(answer.text)
            except ValueError:
                content = None
            if not answers.fits_schema(schema, content):
                self.folder.remove("answer.json")
                summary["waiting"] = {"id": f"task-{task_id}", "problem": "the answer does not fit the form's schema; answer again"}
                return
            decision = answers.FormDecision("answer", answer.reason, content)
        content = decision.content if decision.content is not None else {}
        self.changes.apply(step, "complete_task", {"taskId": task_id, "content": content},
                           lambda: self.client.change("complete_task", {**self._identity(), "taskId": task_id,
                                                                        "content": json.dumps(content), "action": "APPROVE"}))
        if self.mode == "autonomous" or decision.action == "answer" and decision.reason.startswith("the source location"):
            self.folder.decide(title or component or "form", content, decision.reason, task=task_id)
        self._answered(f"task-{task_id}")
        summary["answered"].append({"task": task_id, "title": title, "how": decision.reason})

    # ---- chat ----------------------------------------------------------------------------------

    def _chat(self, summary: dict[str, Any], awaiting: bool) -> None:
        identity = self._identity()
        messages = self._read(lambda: self.api.messages(identity["workspaceId"], identity["jobId"]), "list messages")
        message = latest_unanswered(messages)
        if message is None:
            if self.folder.exists("question.json") and not str(self.folder.load("question.json").get("id", "")).startswith("task-"):
                self.folder.remove("question.json")
            return
        message_id = str(message["messageId"])
        step = f"reply-{message_id}"
        if self.changes.receipt(step) is not None:
            return
        question = answers.chat_question(message, awaiting=awaiting)
        if question is None:
            # Looked at again on every poll, so a message read as a notice is answered once AWS says it waits.
            if message_id not in self.state.setdefault("noted", []):
                self.state["noted"].append(message_id)
                self.folder.event("chat_noted", message=message_id, reason="a notice, not a question")
            return
        if question.kind == "chat" and not awaiting:
            # AWS also posts open offers ("Is there anything you'd like to know while the plan executes?"); the job
            # does not wait on them, so they are left unanswered unless AWS says the job awaits input (spike 1).
            return
        answer = answers.autonomous(question) if self.mode == "autonomous" else None
        if answer is None:
            answer = self._waiting(question, summary)
            if answer is None:
                return
        elif self.mode == "autonomous":
            self.folder.decide(answers.closing_line(question.text) or question.kind, answer.text, answer.reason, message=message_id)

        def settle():
            again = self._read(lambda: self.api.messages(identity["workspaceId"], identity["jobId"]), "list messages")
            sent = [m for m in again if m.get("messageOrigin") != "SYSTEM" and m.get("text") == answer.text
                    and str(m.get("createdAt", "")) > str(message.get("createdAt", ""))]
            return {"message": sent[-1], "settled_from": "the job's chat"} if sent else None

        token = str(uuid.uuid5(uuid.NAMESPACE_URL, f"reframe/{self.folder.root.name}/{message_id}"))
        self.changes.apply(step, "send message", {"in_reply_to": message_id, "text": answer.text, "structured": bool(answer.interaction_origin_id)},
                           lambda: self.api.send(identity["workspaceId"], identity["jobId"], answer.text, answer.interaction_origin_id, token),
                           settle)
        self._answered(question.id)
        summary["answered"].append({"message": message_id, "kind": question.kind, "how": answer.reason})

    # ---- waiting for the person ----------------------------------------------------------------

    def _waiting(self, question: Question, summary: dict[str, Any]) -> Answer | None:
        """The person's answer when reframe answer has written one for this question; otherwise publish it and wait."""
        pending = self.folder.load("question.json")
        if not pending or pending.get("id") != question.id:
            self.folder.save("question.json", {**question.as_json(), "asked_at": iso(self.clock())})
            self.folder.remove("answer.json")
            self.folder.event("question_waiting", id=question.id, kind=question.kind)
        reply = self.folder.load("answer.json")
        if reply and reply.get("id") == question.id:
            return Answer(reply["text"], reply.get("reason", "answered by the person"), question.interaction_origin_id)
        summary["waiting"] = {"id": question.id, "kind": question.kind}
        return None

    def _answered(self, question_id: str) -> None:
        pending = self.folder.load("question.json")
        if pending and pending.get("id") == question_id:
            self.folder.remove("question.json")
            self.folder.remove("answer.json")

    # ---- calls ---------------------------------------------------------------------------------

    def _identity(self) -> dict[str, str]:
        return {"workspaceId": self.workspace_id, "jobId": self.state["job_id"]}

    def _read(self, call: Callable[[], Any], what: str) -> Any:
        try:
            return call()
        except (NotSent, Rejected) as error:
            raise Stop(Outcome.WAITING_SIGNIN, f"the read {what} failed ({str(error)[:300]}). If the AWS sign-in expired, "
                                               "sign in and run reframe resume") from None

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
