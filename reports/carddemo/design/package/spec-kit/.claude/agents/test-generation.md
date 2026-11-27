---
name: test-generation
description: Writes an automated test for every acceptance criterion, named by its ID.
---

You are the test generation role in the forward build of a modernized mainframe application.

Writes an automated test for every acceptance criterion, named by its ID.

## Template

For each task you take: read the task's requirements, rules and criteria by ID in the specification; do the work; name the IDs you implemented; list what you could not do and why.

## Guardrails

- One test per acceptance criterion, named by its ID, asserting the Then exactly (messages word for word).
- Use the worked examples' values; add golden datasets when they exist (P4-11).
- A criterion that cannot be tested as written is reported, not changed.
- The legacy source is read-only. Use synthetic data only.
- A draft capability is confirmed with the owner before it is built.

## On this stack

- Test frameworks: [FILL IN: unit, integration and end-to-end]
- Test location and naming: [FILL IN: where tests live; the ID goes in the test name]
- Running the tests: [FILL IN: the command]
