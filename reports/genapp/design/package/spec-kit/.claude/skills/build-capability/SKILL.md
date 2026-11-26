---
name: build-capability
description: Build one capability of the modernized application from its specification and tasks, keeping every ID.
---

# build-capability

Build one capability of the modernized application from its specification and tasks, keeping every ID.

## Steps

1. Read the capability's specification (specs/<nnn-capability>/spec.md and plan.md) and its tasks (specs/<nnn-capability>/tasks.md). Check its status: a draft is confirmed with the owner first.
2. Do the tasks in order, each by its role (the role files are in .claude/agents/ in the Spec Kit form; the guardrails are in the conventions).
3. Name each requirement and rule ID where it is implemented, and each acceptance criterion's ID in its test.
4. Build: `[FILL IN: the build command]`. Run the tests: `[FILL IN: the test command]`.
5. Report the IDs implemented, the criteria that pass, and anything that could not be done and why.
