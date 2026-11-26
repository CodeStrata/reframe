"""Pipeline 4, stage D7: what the engineer fills in to make the package ready for forward engineering (P4-08).

Reframe writes what the legacy source and the reviews settle. What only the engineer's team can give is left as a
placeholder, `[FILL IN: <what>]`, in the place it belongs:

- the target stack and its detail (versions, build, testing, hosting, security, integration, non-functional needs);
- the house conventions (coding standards, naming, error handling and logging, style reference, definition of done);
- skill templates for Claude Code (`.claude/skills/<name>/SKILL.md`), whose stack-specific steps are placeholders;
- an *On this stack* section in each role file.

START-HERE.md, in the package and in each form, takes the engineer through it: copy the package, give the stack, fill
the placeholders, settle what is still open (draft capabilities, SME questions, decision table gaps, historical
artifacts), check what is left (`--check`), prove it by building *Sign in*, then build final capabilities first.
"""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from typing import Any

MARK = "[FILL IN:"
FILL = re.compile(r"\[FILL IN: (?!\.\.\.\])([^\]]+)\]")  # "[FILL IN: ...]" in the guide is the example, not a placeholder


def fill(what: str) -> str:
    return f"[FILL IN: {what}]"


def stack_section(stack: dict[str, Any] | None, architecture: str) -> str:
    """The target stack, as given, and its detail: the context folder's target-architecture.md, or placeholders."""
    if stack:
        head = (f"- Front end: {stack.get('front_end') or fill('front end')}\n- Back end: {stack.get('back_end') or fill('back end')}\n"
                f"- Data: {stack.get('data') or fill('data store')}\n\nGiven by {stack.get('given_by', 'the engineer')} on {str(stack.get('at', ''))[:10]}.")
    else:
        head = (f"- Front end: {fill('front end, for example React with TypeScript')}\n- Back end: {fill('back end, for example Java 21 with Spring Boot')}\n"
                f"- Data: {fill('data store, for example PostgreSQL')}\n\n**Not given yet.** Give it with `reframe design --stack \"<front end>; <back end>; <data>\"` "
                "and write the package again, so the data contracts get the stack's types; Reframe never chooses a stack. Until then, build nothing that depends on it.")
    if architecture.strip():
        return head + f"\n\n### Target architecture\n\n{architecture.strip()}"
    detail = [("Versions", "language, framework and runtime versions"), ("Build and dependencies", "build tool, package manager, repository layout"),
              ("Testing", "unit, integration and end-to-end test frameworks, and the command that runs them"),
              ("Hosting and deployment", "where it runs, environments, CI/CD"), ("Security", "authentication, authorization, secrets handling"),
              ("Integration", "the systems it calls or is called by, messaging, file transfers"),
              ("Non-functional needs", "response times, volumes, availability, batch windows, retention")]
    return head + "\n\n### Target architecture\n\n" + "\n".join(f"- {k}: {fill(v)}" for k, v in detail) + \
        "\n\nOr put these in `target-architecture.md` in the design context folder and write the package again with `--context`."


def house(style: str = "") -> str:
    """The house conventions: placeholders, except the style reference when the context folder has one."""
    items = [("Coding standards", "style guide, linters and formatters"), ("Naming", "packages, modules, classes, endpoints, tables"),
             ("Error handling and logging", "exception policy, log format, what is never logged (card numbers, personal data)"),
             ("Style reference", "path or link to the house's example screens and code, or its design system"),
             ("Branching and review", "branch naming, pull request rules, who reviews"),
             ("Definition of done", "the checks a task must pass: tests, coverage, review, security scan")]
    given = {"Style reference": f"the design context's style-reference/ ({style})"} if style.strip() else {}
    return "\n".join(f"- {k}: {given[k]}" if k in given else f"- {k}: {fill(v)}" for k, v in items)


def technical_context(stack: dict[str, Any] | None) -> str:
    """Spec Kit's technical context fields, once, in the constitution."""
    s = stack or {}
    rows = [("Language and version", s.get("back_end"), "language and version"), ("Primary dependencies", None, "frameworks and libraries"),
            ("Storage", s.get("data"), "database and version"), ("Front end", s.get("front_end"), "UI framework and component library"),
            ("Testing", None, "test frameworks"), ("Target platform", None, "runtime and hosting"),
            ("Performance goals", None, "response times and batch windows"), ("Constraints", None, "limits the build must respect"),
            ("Scale and scope", None, "users, volumes, data size")]
    return "\n".join(f"- **{k}:** {v or fill(w)}" for k, v, w in rows)


ROLE_FILL = {
    "business-rules": [("Where business logic lives", "package or module, service layer conventions"), ("Exact decimals", "the decimal type and rounding mode")],
    "ui-modernization": [("UI framework and component library", "for example React with the house component library"),
                         ("Design tokens", "where colours, type and spacing come from"), ("Routing and state", "router, form and state libraries")],
    "data": [("Persistence", "ORM or data access library, and the migration tool"), ("Table and column naming", "the house convention"),
             ("Test data", "where synthetic data is generated and loaded")],
    "api": [("API style", "REST, GraphQL or messaging, and the specification format"), ("Scheduled jobs", "the scheduler or batch framework"),
            ("Errors", "the error response format")],
    "test-generation": [("Test frameworks", "unit, integration and end-to-end"), ("Test location and naming", "where tests live; the ID goes in the test name"),
                        ("Running the tests", "the command")],
    "compliance": [("Standards", "PCI DSS, GDPR or house policies that apply"), ("Tools", "secret scanning, dependency and static analysis")],
}


def role_fill(role: str) -> list[str]:
    return ["## On this stack", ""] + [f"- {k}: {fill(v)}" for k, v in ROLE_FILL.get(role, [])] + [""]


SKILLS = {
    "build-capability": ("Build one capability of the modernized application from its specification and tasks, keeping every ID.", [
        "1. Read the capability's specification ({specs}) and its tasks ({tasks}). Check its status: a draft is confirmed with the owner first.",
        "2. Do the tasks in order, each by its role (the role files are in .claude/agents/ in the Spec Kit form; the guardrails are in the conventions).",
        "3. Name each requirement and rule ID where it is implemented, and each acceptance criterion's ID in its test.",
        "4. Build: `{build}`. Run the tests: `{test}`.",
        "5. Report the IDs implemented, the criteria that pass, and anything that could not be done and why."]),
    "write-acceptance-tests": ("Write an automated test for each acceptance criterion of a capability, named by its ID.", [
        "1. For each criterion (GIVEN, WHEN, THEN, with its ID), write one test named by the ID, using the values the criterion gives.",
        "2. Assert the THEN exactly; messages word for word.",
        "3. Test framework: {framework}. Tests live in: {where}. Run them with `{test}`.",
        "4. A criterion that cannot be tested as written is reported, not changed."]),
    "model-data-contract": ("Turn a data contract (a copybook record) into the target stack's entity and table.", [
        "1. Read the record in data-contracts.md: each field's type, digits, scale, OCCURS, REDEFINES and 88-level values.",
        "2. Keep the precision: a decimal stays an exact decimal; text keeps its length; an OCCURS becomes a child table or a list; 88-level values become an enumeration.",
        "3. Persistence: {orm}. Migrations: {migrations}. Naming: {naming}.",
        "4. Keep the copybook and field names in a comment or mapping for data migration."]),
    "build-screen": ("Build a modern screen to the prototype in ui-reference/ and its screen specification.", [
        "1. Open ui-reference/index.html#/<screen id> and the screen's components in its capability's specification.",
        "2. Build each component with {components}; every validation shows the rule's own message; meet WCAG 2.2 AA.",
        "3. Routing: {routing}. Design tokens: {tokens}.",
        "4. The screen calls the services its capability's API task builds; name the requirement IDs each component serves."]),
}


def skill(name: str, specs: str, tasks: str) -> str:
    what, steps = SKILLS[name]
    values = {"specs": specs, "tasks": tasks, "build": fill("the build command"), "test": fill("the test command"), "framework": fill("test frameworks"),
              "where": fill("test folders"), "orm": fill("ORM or data access library"), "migrations": fill("migration tool"), "naming": fill("table and column naming"),
              "components": fill("UI framework and component library"), "routing": fill("router"), "tokens": fill("where the design tokens come from")}
    return "\n".join(["---", f"name: {name}", f"description: {what}", "---", "", f"# {name}", "", what, "", "## Steps", ""]
                     + [s.format(**values) for s in steps] + [""])


# ---- the guide ---------------------------------------------------------------------------------------------------------

def facts(specs: list[dict[str, Any]], journeys: list[dict[str, Any]], programs: dict[str, list[str]]) -> dict[str, Any]:
    """What is still open, and the proof slice: the capabilities whose rules come from the programs behind the legacy
    screen most journeys start on (the sign-on). `programs` is each legacy screen's programs, from the inventory."""
    starts = Counter(j["steps"][0]["screen"] for j in journeys if j.get("steps"))
    first = starts.most_common(1)[0][0] if starts else ""
    behind = {p.upper() for p in programs.get(first) or []}
    proof = [s for s in specs if behind & {str(r.get("program", "")).upper() for r in s["rules"]}]
    drafts = Counter(s["function_name"] for s in specs if s["status"] == "draft")
    return {"drafts": dict(drafts), "draft_count": sum(drafts.values()), "final_count": sum(1 for s in specs if s["status"] == "final"),
            "questions": len({q["id"] or q["question"] for s in specs for q in s["questions"]}),
            "gaps": sum(len(t.get("gaps") or []) for s in specs for t in s["tables"]),
            "artifacts": sorted({s["rule_ids"][r["key"]] for s in specs for r in s["rules"] if r["class"] == "historical artifact"}),
            "first_screen": first, "proof": [{"id": s["id"], "title": s["title"], "criteria": len(s["acceptance"]), "folder": s["folder"], "status": s["status"]} for s in proof]}


WHERE = {
    "kiro": "- Specifications: `.kiro/specs/<capability>/` (requirements.md, design.md, tasks.md).\n- Stack and house conventions: `.kiro/steering/tech.md` and `house-conventions.md`.",
    "claude-code": "- Specifications: `specs/`; tasks: `tasks.md`; the UI to build to: `ui-reference/index.html`.\n- Stack and house conventions: `CLAUDE.md`. Skills: `.claude/skills/`.",
    "spec-kit": "- Specifications: `specs/<nnn-capability>/` (spec.md, plan.md, tasks.md).\n- Stack, technical context and house conventions: `.specify/memory/constitution.md`. "
                "Roles: `.claude/agents/`; skills: `.claude/skills/`.",
}


def start_here(f: dict[str, Any], project: str, stack: dict[str, Any] | None, form: str | None) -> str:
    where = WHERE[form] if form else "\n\n".join(f"**{k}**\n\n{v}" for k, v in WHERE.items()) + "\n"
    drafts = "\n".join(f"  - {name}: {n} draft" for name, n in sorted(f["drafts"].items())) or "  - None."
    proof = "\n".join(f"  - {p['id']} {p['title']} ({p['criteria']} acceptance criteria; {p['status']}"
                      + (": confirm it with the owner first, or sign off its function" if p["status"] == "draft" else "") + ")" for p in f["proof"]) or "  - The capabilities of your first journey."
    artifacts = ", ".join(f["artifacts"]) or "none"
    return f"""# Start here

This package was written by Reframe from {project}'s legacy source, its reconciled requirements and rules, and the reviewers' sign-offs. It holds what
those settle. What only your team can give is marked `[FILL IN: ...]`. These steps make it ready for forward engineering.

{where}
- Every form: `data-contracts.md` (the copybooks as typed records) and `traceability.md` (every ID back to the legacy source).

## 1. Copy the package

`reframe design --package <empty folder> --form kiro|claude-code|spec-kit|all` (today: `python -m reframe.design.package --out <empty folder>`).
Work in the copy. Reframe will not copy over files you have filled in: when the design changes, copy the new version into a new folder and
carry your filled-in files across; `CHANGES.md` says what changed, by ID.

## 2. Give the target stack

{"The stack is given: " + stack["stack"] + "." if stack else "The stack is not given yet."} Give or change it with
`reframe design --stack "<front end>; <back end>; <data>"` (today: `python -m reframe.design.specs --stack ...`, then write the package again).
Reframe adds the stack's code and column types to the data contracts, with no model step. It never chooses a stack for you.

## 3. Fill in the placeholders

- **Target architecture:** versions, build, testing, hosting, security, integration and non-functional needs. Put them in `target-architecture.md`
  in the design context folder and write the package again with `--context <folder>`, or fill them where they are.
- **House conventions:** coding standards, naming, error handling and logging, style reference, review rules, definition of done.
- **Skills** (`.claude/skills/`): the build and test commands, frameworks and libraries each skill uses.
- **Roles** (`.claude/agents/`): the *On this stack* section of each role.

`personas.md` and `decisions.md` in the context folder are added to the product description the same way.

## 4. Settle what is still open

- **Draft capabilities:** {f["draft_count"]} of {f["draft_count"] + f["final_count"]} are draft because their function is not signed off. Sign off
  each function on the reconciliation page, read the review download with `reframe reconcile --context <folder>`, and write the design again.
{drafts}
- **SME questions:** {f["questions"]} open. Answer them in `reconcile/questions.csv` and run `reframe reconcile --context <folder>`.
- **Decision table gaps:** {f["gaps"]} combinations no rule covers, listed in each design. Decide each with the owner.
- **Historical artifacts:** rules to keep or drop with the owner before anyone builds them: {artifacts}.

## 5. Check what is left

`python -m reframe.design.package --check <your copy>` lists every `[FILL IN: ...]` still there and the draft capabilities. It is ready when no
placeholder is left and the capabilities you are building are final.

## 6. Prove it: build Sign in

In a scratch repository, with the Claude Code form and the stack filled in, ask Claude Code to build the sign-in slice:
{proof}

Use the `build-capability` and `write-acceptance-tests` skills. Record whether it builds and which acceptance criteria pass, by ID. A failure
here is a gap in the package or the placeholders: fix it before the full build.

## 7. Build

Final capabilities first; each task names its role and the requirement, rule and criterion IDs it implements. Keep every ID in code and tests.
"""


def readiness(root: Path) -> dict[str, Any]:
    """The placeholders left in a copy of the package, and its draft capabilities."""
    left: dict[str, list[str]] = {}
    drafts = set()
    for p in sorted(root.rglob("*.md")):
        text = p.read_text(errors="replace")
        found = FILL.findall(text)
        if found:
            left[p.relative_to(root).as_posix()] = found
        for m in re.finditer(r"^# [^\n]*\(([A-Z0-9]+-C\d+)\)\n\n\*\*Status: DRAFT\*\*", text, re.M):
            drafts.add(m.group(1))
    return {"ready": not left, "placeholders": sum(len(v) for v in left.values()), "files": left, "drafts": sorted(drafts)}
