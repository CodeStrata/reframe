# Feature specification: Record log messages to the standard and error queues

**Feature:** DEML-C02 · Diagnostic and Error Message Logging · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (DEML-C02)

As an operations or support team member, I want every diagnostic and error message written to the standard log queue and to an error queue that callers can redirect, so that I can find and review application errors.

Writes every diagnostic and error message to the standard system log, and also to an application error queue that support staff review. The error queue is 'GENAERRS' by default, but a caller can redirect a message to another queue by starting it with 'Q=' and a 4-character code. It must never block or fail the calling business transaction: messages go to both destinations, but a write that fails or has no room is dropped silently.

**Acceptance scenarios:**

1. **Given** temporary storage: full, **when** error logger runs, **then** The record goes to 'CSMT' only; the queue write is skipped and the task carries on. (DEML-C02-AC-01)
2. **Given** queue write result: failure, **when** either queue write fails, **then** No error is raised and the caller receives control back as normal. (DEML-C02-AC-02)
3. **Given** A log record 'GENA LGAPDB01 INSERT POLICY FAILED' with message length 29, **when** The logger records it, **then** The record is written to the standard log queue 'CSMT' with length 34 (29 plus 5) (DEML-C02-AC-03)
4. **Given** A message text that does not begin with 'Q=', e.g. 'LGAPDB01 INSERT POLICY FAILED', **when** The logger records it, **then** The record is written to the error queue 'GENAERRS' (DEML-C02-AC-04)
5. **Given** A message text that contains 'Q=' but not at the start, e.g. 'ERROR Q=ABCD', **when** The logger records it, **then** The record is written to the error queue 'GENAERRS' and the text is logged unchanged (DEML-C02-AC-05)
6. **Given** A message text 'Q=TEST CUSTOMER 0001 ADDED' with record length 31, **when** The logger records it, **then** The record is written to the queue 'GENATEST', the logged text is 'CUSTOMER 0001 ADDED' (first 7 characters removed) and the record length is 24 (31 minus 7) (DEML-C02-AC-06)

## Requirements

### Functional requirements

- **DEML-REQ-F-005** (side effect): The system shall write every log record, with length message length plus 5, to the transient data queue 'CSMT'. Rules: DEML-BR-005.
- **DEML-REQ-F-006** (business rule): The system shall write to the temporary storage queue 'GENAERRS' unless the message text begins with 'Q='. Rules: DEML-BR-006.
- **DEML-REQ-F-007** (business rule): When the message text begins with 'Q=', the system shall write to the queue named 'GENA' plus the 4 characters after 'Q=', remove the first 7 characters ('Q=', the 4-character code and the following character) from the logged text, and reduce the record length by 7. Rules: DEML-BR-007.
- **DEML-REQ-F-008** (side effect): The system shall also write the same record to the temporary storage queue ('GENAERRS' or its 'Q=' override) without waiting for storage, so the record is dropped when no space is available. Rules: DEML-BR-008.
- **DEML-REQ-N-001** (error handling): If either queue write fails, then the system shall ignore the response code and shall not tell the caller. Rules: DEML-BR-009.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DEML-BR-005 | Write message to standard log queue | side effect | THE error logger SHALL write every log record, with length message length plus 5, to the transient data queue 'CSMT'. | high | base/src/lgstsq.cbl:40, base/src/lgstsq.cbl:90-111, base/src/lgstsq.cbl:121-122 |
| DEML-BR-006 | Select target error queue name | business rule | THE error logger SHALL write to the temporary storage queue 'GENAERRS' unless the message text begins with 'Q='. | high | base/src/lgstsq.cbl:5-6, base/src/lgstsq.cbl:29-37, base/src/lgstsq.cbl:82-88 |
| DEML-BR-007 | Strip queue directive prefix | business rule | WHEN the message text begins with 'Q=', THE error logger SHALL write to the queue named 'GENA' plus the 4 characters after 'Q=', remove the first 7 characters ('Q=', the 4-character code and the following character) from the logged text, and reduce the record length by 7. | high | base/src/lgstsq.cbl:5-6, base/src/lgstsq.cbl:29-37, base/src/lgstsq.cbl:82-88 |
| DEML-BR-008 | Dual-destination error logging with non-blocking TS write | side effect | THE error logger SHALL also write the same record to the temporary storage queue ('GENAERRS' or its 'Q=' override) without waiting for storage, so the record is dropped when no space is available. | high | base/src/lgstsq.cbl:40, base/src/lgstsq.cbl:90-111, base/src/lgstsq.cbl:121-122 |
| DEML-BR-009 | Dual-destination error logging with non-blocking TS write | error handling | WHEN either queue write fails, THE error logger SHALL ignore the response code and SHALL NOT tell the caller. | high | base/src/lgstsq.cbl:40, base/src/lgstsq.cbl:90-111, base/src/lgstsq.cbl:121-122 |

### Key entities

None found in the source.

### Needs clarification

- SME-076: When a message is written to the error log, the system drops fixed numbers of characters (5 from terminal input, 7 when a 'Q=' queue directive is removed, and adds 5 back before writing). What do these characters represent: the system identifier, the 'Q=' prefix, the 4-character queue code, and is there a separator after the queue code? Must the new system keep this exact input format, or can it define an explicit one? (Application support team) On DEML-BR-007, DEML-BR-005.
- SME-077: If writing a message to the error log queue fails, including when there is not enough storage, what should happen: stop, report it, retry, or ignore it? (Application support team) On DEML-BR-007, DEML-BR-005.
- SME-079: A 'Q=' directive replaces part of the default error queue name 'GENAERRS' with a 4-character code. Which characters of the queue name are replaced? (Application support team) On DEML-BR-007.

### Decision table gaps

- Temporary storage queue selection: No rule says what happens when fewer than 4 characters (or no following character) come after 'Q=', so the queue name and the 7-character strip are undefined for short messages.
