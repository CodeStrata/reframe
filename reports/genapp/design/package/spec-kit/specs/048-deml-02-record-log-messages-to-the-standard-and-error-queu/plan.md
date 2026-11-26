# Implementation plan: Record log messages to the standard and error queues (DEML-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as service.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as service.

## Data model

None found in the source.

## Design notes

None.

## Decision tables

#### Temporary storage queue selection

| Message text begins with 'Q=' | Temporary storage queue written and logged text | Rule |
|---|---|---|
| No | Write to temporary storage queue 'GENAERRS' with the message text unchanged | DEML-BR-006 |
| Yes | Write to queue 'GENA' plus the 4 characters after 'Q='; remove the first 7 characters from the logged text and reduce the record length by 7 | DEML-BR-007 |
| Either | Same record also written to the selected temporary storage queue without waiting for storage; dropped when no space is available | DEML-BR-008 |
| Yes | **Gap:** No rule says what happens when fewer than 4 characters (or no following character) come after 'Q=', so the queue name and the 7-character strip are undefined for short messages. | |

