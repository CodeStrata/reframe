# Implementation plan: Self-scheduled statistics refresh (TSM-C01)

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

- TSM-BR-001: The new application needs a scheduled job that starts the statistics collection once a minute. The legacy run books its own next run first, before it reads any counters, and never checks whether the booking worked. A scheduler with a fixed one-minute interval, such as a cron trigger or a timer service, replaces that self-booking. It must still run every minute even if a run fails partway, so that one failure does not stop the cycle.

## Decision tables

None.
