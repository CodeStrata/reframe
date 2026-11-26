# Design: Record log messages to the standard and error queues (DEML-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Writes every diagnostic and error message to the standard system log, and also to an application error queue that support staff review. The error queue is 'GENAERRS' by default, but a caller can redirect a message to another queue by starting it with 'Q=' and a 4-character code. It must never block or fail the calling business transaction: messages go to both destinations, but a write that fails or has no room is dropped silently.

Runs as service.

## Screens and components

No screens: it runs as service.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DEML-BR-005 | Write message to standard log queue | side effect | THE error logger SHALL write every log record, with length message length plus 5, to the transient data queue 'CSMT'. | high | base/src/lgstsq.cbl:40, base/src/lgstsq.cbl:90-111, base/src/lgstsq.cbl:121-122 |
| DEML-BR-006 | Select target error queue name | business rule | THE error logger SHALL write to the temporary storage queue 'GENAERRS' unless the message text begins with 'Q='. | high | base/src/lgstsq.cbl:5-6, base/src/lgstsq.cbl:29-37, base/src/lgstsq.cbl:82-88 |
| DEML-BR-007 | Strip queue directive prefix | business rule | WHEN the message text begins with 'Q=', THE error logger SHALL write to the queue named 'GENA' plus the 4 characters after 'Q=', remove the first 7 characters ('Q=', the 4-character code and the following character) from the logged text, and reduce the record length by 7. | high | base/src/lgstsq.cbl:5-6, base/src/lgstsq.cbl:29-37, base/src/lgstsq.cbl:82-88 |
| DEML-BR-008 | Dual-destination error logging with non-blocking TS write | side effect | THE error logger SHALL also write the same record to the temporary storage queue ('GENAERRS' or its 'Q=' override) without waiting for storage, so the record is dropped when no space is available. | high | base/src/lgstsq.cbl:40, base/src/lgstsq.cbl:90-111, base/src/lgstsq.cbl:121-122 |
| DEML-BR-009 | Dual-destination error logging with non-blocking TS write | error handling | WHEN either queue write fails, THE error logger SHALL ignore the response code and SHALL NOT tell the caller. | high | base/src/lgstsq.cbl:40, base/src/lgstsq.cbl:90-111, base/src/lgstsq.cbl:121-122 |

### Worked examples

- DEML-BR-008: temporary storage = full → The record goes to 'CSMT' only; the queue write is skipped and the task carries on.
- DEML-BR-009: queue write result = failure → No error is raised and the caller receives control back as normal.

## Decision tables

#### Temporary storage queue selection

| Message text begins with 'Q=' | Temporary storage queue written and logged text | Rule |
|---|---|---|
| No | Write to temporary storage queue 'GENAERRS' with the message text unchanged | DEML-BR-006 |
| Yes | Write to queue 'GENA' plus the 4 characters after 'Q='; remove the first 7 characters from the logged text and reduce the record length by 7 | DEML-BR-007 |
| Either | Same record also written to the selected temporary storage queue without waiting for storage; dropped when no space is available | DEML-BR-008 |
| Yes | **Gap:** No rule says what happens when fewer than 4 characters (or no following character) come after 'Q=', so the queue name and the 7-character strip are undefined for short messages. | |


## Design notes

None.

## Open questions

- SME-076: When a message is written to the error log, the system drops fixed numbers of characters (5 from terminal input, 7 when a 'Q=' queue directive is removed, and adds 5 back before writing). What do these characters represent: the system identifier, the 'Q=' prefix, the 4-character queue code, and is there a separator after the queue code? Must the new system keep this exact input format, or can it define an explicit one? (Application support team) On DEML-BR-007, DEML-BR-005.
- SME-077: If writing a message to the error log queue fails, including when there is not enough storage, what should happen: stop, report it, retry, or ignore it? (Application support team) On DEML-BR-007, DEML-BR-005.
- SME-079: A 'Q=' directive replaces part of the default error queue name 'GENAERRS' with a 4-character code. Which characters of the queue name are replaced? (Application support team) On DEML-BR-007.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).