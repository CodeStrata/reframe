# Feature specification: Accept log requests from programs and terminals

**Feature:** DEML-C01 · Diagnostic and Error Message Logging · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (DEML-C01)

As an application component or terminal operator, I want to submit a diagnostic or error message to the shared logger, either by calling it from a program or by entering it at a terminal, so that the message is recorded and I get the right acknowledgement for how I submitted it.

Gives every part of the application, and operators at a terminal, one shared way to record a diagnostic or error message. Each message is stamped with the identifier of the system that produced it, and the submitter gets the acknowledgement that suits how they sent it: a program call returns quietly, a terminal entry clears the screen. It must never lose or garble the submitted text: program messages keep up to 90 characters, terminal messages keep the 74 characters after the 5-character transaction code.

**Acceptance scenarios:**

1. **Given** mode: 'R', **when** the log request was entered at a terminal (mode 'R'), **then** The terminal screen is erased, the keyboard is unlocked, and the task ends. (DEML-C01-AC-01)
2. **Given** mode: 'C'; calling program: LGAPOL01, **when** the logger was called by another program (mode 'C'), **then** Control returns to LGAPOL01; nothing is sent to a screen. (DEML-C01-AC-02)
3. **Given** The logger runs on system 'GENA' and is called by another program with the message text 'LGAPDB01 INSERT POLICY FAILED' and a data length of 29, **when** The call is processed, **then** The request is handled as a program call (mode 'C'), the log record is 'GENA LGAPDB01 INSERT POLICY FAILED' (system identifier, one space, then the caller's text) and the record length is 34 (29 plus 5) (DEML-C01-AC-03)
4. **Given** A calling program supplies message text longer than 90 characters, **when** The call is processed, **then** Only the first 90 characters of the caller's text follow the system identifier and space in the log record (DEML-C01-AC-04)
5. **Given** An operator at a terminal enters the transaction code followed by a message, e.g. 'LGSTCHECK CUSTOMER FILE', received length 23, **when** The logger is started from the terminal, **then** The request is handled as a terminal request (mode 'R'), the first 5 characters are dropped, the message text is 'CHECK CUSTOMER FILE' and the record length is 23 (23 minus 5, plus 5) (DEML-C01-AC-05)
6. **Given** Terminal input whose text after the 5-character transaction code is longer than 74 characters, **when** The logger is started from the terminal, **then** Only the 74 characters following the transaction code are used as the message text (DEML-C01-AC-06)

## Requirements

### Functional requirements

- **DEML-REQ-F-001** (design note): When the logging program is called by another program, the system shall treat it as a program call (mode 'C'), build the log record as the CICS system identifier, one space, then the caller's message text (up to 90 characters), and use the caller's data length plus 5 as the record length. Rules: DEML-BR-001.
- **DEML-REQ-F-002** (design note): When the logging program is started from a terminal rather than by another program, the system shall read the terminal input, treat it as a terminal request (mode 'R'), drop the first 5 characters (the transaction code), use the next 74 characters as the message text, and use the received length minus 5, plus 5, as the record length. Rules: DEML-BR-002.
- **DEML-REQ-F-003** (formatting): When the log request was entered at a terminal (mode 'R'), the system shall, after writing the queues, clear the screen by sending a single blank character, unlock the keyboard and end the task. Rules: DEML-BR-003.
- **DEML-REQ-F-004** (design note): When the logger was called by another program (mode 'C'), the system shall return to the caller without any screen output. Rules: DEML-BR-004.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DEML-BR-001 | Use caller-supplied text as message | design note | WHEN the logging program is called by another program, THE error logger SHALL treat it as a program call (mode 'C'), build the log record as the CICS system identifier, one space, then the caller's message text (up to 90 characters), and use the caller's data length plus 5 as the record length. | high | base/src/lgstsq.cbl:17-32, base/src/lgstsq.cbl:57-80, base/src/lgstsq.cbl:90, base/src/lgapol01.cbl:41-50 |
| DEML-BR-002 | Use terminal input as message | design note | WHEN the logging program is started from a terminal rather than by another program, THE error logger SHALL read the terminal input, treat it as a terminal request (mode 'R'), drop the first 5 characters (the transaction code), use the next 74 characters as the message text, and use the received length minus 5, plus 5, as the record length. | high | base/src/lgstsq.cbl:17-32, base/src/lgstsq.cbl:57-80, base/src/lgstsq.cbl:90, base/src/lgapol01.cbl:41-50 |
| DEML-BR-003 | Terminal acknowledgement for directly entered log requests | formatting | WHEN the log request was entered at a terminal (mode 'R'), THE error logger SHALL, after writing the queues, clear the screen by sending a single blank character, unlock the keyboard and end the task. | medium | base/src/lgstsq.cbl:113-122 |
| DEML-BR-004 | Terminal acknowledgement for directly entered log requests | design note | WHEN the logger was called by another program (mode 'C'), THE error logger SHALL return to the caller without any screen output. | medium | base/src/lgstsq.cbl:113-122 |

### Key entities

None found in the source.

### Needs clarification

- SME-076: When a message is written to the error log, the system drops fixed numbers of characters (5 from terminal input, 7 when a 'Q=' queue directive is removed, and adds 5 back before writing). What do these characters represent: the system identifier, the 'Q=' prefix, the 4-character queue code, and is there a separator after the queue code? Must the new system keep this exact input format, or can it define an explicit one? (Application support team) On DEML-BR-001, DEML-BR-002.
- SME-077: If writing a message to the error log queue fails, including when there is not enough storage, what should happen: stop, report it, retry, or ignore it? (Application support team) On DEML-BR-001, DEML-BR-002.
- SME-078: When the error logger is run directly from a terminal, it sends a blank reply to clear the screen and unlock the keyboard. Should this be kept as a requirement, and what should replace it in the new system? (Application owner / business analyst) On DEML-BR-002.
- SME-079: A 'Q=' directive replaces part of the default error queue name 'GENAERRS' with a 4-character code. Which characters of the queue name are replaced? (Application support team) On DEML-BR-002.
- SME-080: Should log messages be limited to a maximum length (for example 90 characters), and should a message from a calling program that is longer than that be rejected or cut short? (Application owner for error logging) On DEML-BR-002.
- DEF-001: Is this intended? The record length is taken from the caller's commarea length while the message area holds only 90 characters: callers that pass their 99-byte 'COMMAREA=' message (LGAPOL01, LGDPVS01 and others) get a length of 104 for a 95-byte record, so the logged record runs past the record into neighbouring storage and the last 9 characters of the caller's text are lost. On terminal entry the input area is 79 bytes but up to 80 are requested. (Subject-matter expert) On DEML-BR-001, DEML-BR-002.

### Decision table gaps

None.
