# Implementation plan: Publish statistics to shared queues (TSM-C03)

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

- TSM-BR-009: Each statistic needs a small keyed record, keyed by its queue name (for example 'GENA100V' or 'GENAX00V'), that holds the current value, the previous value and the change. Publishing reads the stored current value as the previous value and then replaces the whole record with new, previous and change (new minus previous). Do this as one atomic replace, such as a keyed upsert in a cache or table, so readers never see an empty or half-written statistic. Keep the order new, previous, change wherever consumers read it as a list.

## Decision tables

None.
