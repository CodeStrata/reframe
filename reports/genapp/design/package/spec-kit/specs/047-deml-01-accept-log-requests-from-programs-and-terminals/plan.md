# Implementation plan: Accept log requests from programs and terminals (DEML-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

None found in the source.

## Design notes

- DEML-BR-001: Expose the logger as a callable service (in-process API or endpoint) that takes a message of up to 90 characters. The service prefixes the identifier of the producing system/instance and one space, and records the length as message length plus 5. Keep the 90-character limit and the 'system-id space text' layout so existing log readers still work.
- DEML-BR-002: Give operators a separate entry point (a console command or simple form) for typing a message by hand. When the input still carries a 5-character command/transaction prefix, strip it and keep at most the next 74 characters as the message. Then pass it through the same record-building path, with length computed as input length minus 5, plus 5.
- DEML-BR-004: A program-call submission must return straight to the caller with no user-facing output and no result the caller has to handle. Make it a fire-and-forget call that does not change the caller's flow.

## Decision tables

#### Log request handling by how the logger was started

| How the logger was started | Message source, record length and acknowledgement | Rule |
|---|---|---|
| Called by another program (mode 'C') | Record is the CICS system identifier, one space, then the caller's message text (up to 90 characters); record length is the caller's data length plus 5 | DEML-BR-001 |
| Started from a terminal (mode 'R') | First 5 characters (transaction code) dropped; next 74 characters used as message text; record length is the received length minus 5, plus 5 | DEML-BR-002 |
| Started from a terminal (mode 'R') | After writing the queues, clear the screen by sending a single blank character, unlock the keyboard and end the task | DEML-BR-003 |
| Called by another program (mode 'C') | Return to the caller without any screen output | DEML-BR-004 |

