# Design: Accept log requests from programs and terminals (DEML-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Gives every part of the application, and operators at a terminal, one shared way to record a diagnostic or error message. Each message is stamped with the identifier of the system that produced it, and the submitter gets the acknowledgement that suits how they sent it: a program call returns quietly, a terminal entry clears the screen. It must never lose or garble the submitted text: program messages keep up to 90 characters, terminal messages keep the 74 characters after the 5-character transaction code.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DEML-BR-001 | Use caller-supplied text as message | design note | WHEN the logging program is called by another program, THE error logger SHALL treat it as a program call (mode 'C'), build the log record as the CICS system identifier, one space, then the caller's message text (up to 90 characters), and use the caller's data length plus 5 as the record length. | high | base/src/lgstsq.cbl:17-32, base/src/lgstsq.cbl:57-80, base/src/lgstsq.cbl:90, base/src/lgapol01.cbl:41-50 |
| DEML-BR-002 | Use terminal input as message | design note | WHEN the logging program is started from a terminal rather than by another program, THE error logger SHALL read the terminal input, treat it as a terminal request (mode 'R'), drop the first 5 characters (the transaction code), use the next 74 characters as the message text, and use the received length minus 5, plus 5, as the record length. | high | base/src/lgstsq.cbl:17-32, base/src/lgstsq.cbl:57-80, base/src/lgstsq.cbl:90, base/src/lgapol01.cbl:41-50 |
| DEML-BR-003 | Terminal acknowledgement for directly entered log requests | formatting | WHEN the log request was entered at a terminal (mode 'R'), THE error logger SHALL, after writing the queues, clear the screen by sending a single blank character, unlock the keyboard and end the task. | medium | base/src/lgstsq.cbl:113-122 |
| DEML-BR-004 | Terminal acknowledgement for directly entered log requests | design note | WHEN the logger was called by another program (mode 'C'), THE error logger SHALL return to the caller without any screen output. | medium | base/src/lgstsq.cbl:113-122 |

### Worked examples

- DEML-BR-003: mode = 'R' → The terminal screen is erased, the keyboard is unlocked, and the task ends.
- DEML-BR-004: mode = 'C'; calling program = LGAPOL01 → Control returns to LGAPOL01; nothing is sent to a screen.

## Decision tables

#### Log request handling by how the logger was started

| How the logger was started | Message source, record length and acknowledgement | Rule |
|---|---|---|
| Called by another program (mode 'C') | Record is the CICS system identifier, one space, then the caller's message text (up to 90 characters); record length is the caller's data length plus 5 | DEML-BR-001 |
| Started from a terminal (mode 'R') | First 5 characters (transaction code) dropped; next 74 characters used as message text; record length is the received length minus 5, plus 5 | DEML-BR-002 |
| Started from a terminal (mode 'R') | After writing the queues, clear the screen by sending a single blank character, unlock the keyboard and end the task | DEML-BR-003 |
| Called by another program (mode 'C') | Return to the caller without any screen output | DEML-BR-004 |


## Design notes

- DEML-BR-001: Expose the logger as a callable service (in-process API or endpoint) that takes a message of up to 90 characters. The service prefixes the identifier of the producing system/instance and one space, and records the length as message length plus 5. Keep the 90-character limit and the 'system-id space text' layout so existing log readers still work.
- DEML-BR-002: Give operators a separate entry point (a console command or simple form) for typing a message by hand. When the input still carries a 5-character command/transaction prefix, strip it and keep at most the next 74 characters as the message. Then pass it through the same record-building path, with length computed as input length minus 5, plus 5.
- DEML-BR-004: A program-call submission must return straight to the caller with no user-facing output and no result the caller has to handle. Make it a fire-and-forget call that does not change the caller's flow.

## Open questions

- SME-076: When a message is written to the error log, the system drops fixed numbers of characters (5 from terminal input, 7 when a 'Q=' queue directive is removed, and adds 5 back before writing). What do these characters represent: the system identifier, the 'Q=' prefix, the 4-character queue code, and is there a separator after the queue code? Must the new system keep this exact input format, or can it define an explicit one? (Application support team) On DEML-BR-001, DEML-BR-002.
- SME-077: If writing a message to the error log queue fails, including when there is not enough storage, what should happen: stop, report it, retry, or ignore it? (Application support team) On DEML-BR-001, DEML-BR-002.
- SME-078: When the error logger is run directly from a terminal, it sends a blank reply to clear the screen and unlock the keyboard. Should this be kept as a requirement, and what should replace it in the new system? (Application owner / business analyst) On DEML-BR-002.
- SME-079: A 'Q=' directive replaces part of the default error queue name 'GENAERRS' with a 4-character code. Which characters of the queue name are replaced? (Application support team) On DEML-BR-002.
- SME-080: Should log messages be limited to a maximum length (for example 90 characters), and should a message from a calling program that is longer than that be rejected or cut short? (Application owner for error logging) On DEML-BR-002.
- DEF-001: Is this intended? The record length is taken from the caller's commarea length while the message area holds only 90 characters: callers that pass their 99-byte 'COMMAREA=' message (LGAPOL01, LGDPVS01 and others) get a length of 104 for a 95-byte record, so the logged record runs past the record into neighbouring storage and the last 9 characters of the caller's text are lost. On terminal entry the input area is 79 bytes but up to 80 are requested. (Subject-matter expert) On DEML-BR-001, DEML-BR-002.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).