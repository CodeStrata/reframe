# Requirements: Accept log requests from programs and terminals (DEML-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Diagnostic and Error Message Logging · runs as scheduled job · risk high

## Introduction

Gives every part of the application, and operators at a terminal, one shared way to record a diagnostic or error message. Each message is stamped with the identifier of the system that produced it, and the submitter gets the acknowledgement that suits how they sent it: a program call returns quietly, a terminal entry clears the screen. It must never lose or garble the submitted text: program messages keep up to 90 characters, terminal messages keep the 74 characters after the 5-character transaction code.

**User story:** As an application component or terminal operator, I want to submit a diagnostic or error message to the shared logger, either by calling it from a program or by entering it at a terminal, so that the message is recorded and I get the right acknowledgement for how I submitted it.

## Requirements

### Requirement 1: DEML-REQ-F-001 (design note)

#### Acceptance criteria

1. When the logging program is called by another program, the system shall treat it as a program call (mode 'C'), build the log record as the CICS system identifier, one space, then the caller's message text (up to 90 characters), and use the caller's data length plus 5 as the record length. (rules DEML-BR-001)
2. GIVEN The logger runs on system 'GENA' and is called by another program with the message text 'LGAPDB01 INSERT POLICY FAILED' and a data length of 29 WHEN The call is processed THEN The request is handled as a program call (mode 'C'), the log record is 'GENA LGAPDB01 INSERT POLICY FAILED' (system identifier, one space, then the caller's text) and the record length is 34 (29 plus 5) (DEML-C01-AC-03; DEML-BR-001)
3. GIVEN A calling program supplies message text longer than 90 characters WHEN The call is processed THEN Only the first 90 characters of the caller's text follow the system identifier and space in the log record (DEML-C01-AC-04; DEML-BR-001)

### Requirement 2: DEML-REQ-F-002 (design note)

#### Acceptance criteria

1. When the logging program is started from a terminal rather than by another program, the system shall read the terminal input, treat it as a terminal request (mode 'R'), drop the first 5 characters (the transaction code), use the next 74 characters as the message text, and use the received length minus 5, plus 5, as the record length. (rules DEML-BR-002)
2. GIVEN An operator at a terminal enters the transaction code followed by a message, e.g. 'LGSTCHECK CUSTOMER FILE', received length 23 WHEN The logger is started from the terminal THEN The request is handled as a terminal request (mode 'R'), the first 5 characters are dropped, the message text is 'CHECK CUSTOMER FILE' and the record length is 23 (23 minus 5, plus 5) (DEML-C01-AC-05; DEML-BR-002)
3. GIVEN Terminal input whose text after the 5-character transaction code is longer than 74 characters WHEN The logger is started from the terminal THEN Only the 74 characters following the transaction code are used as the message text (DEML-C01-AC-06; DEML-BR-002)

### Requirement 3: DEML-REQ-F-003 (formatting)

#### Acceptance criteria

1. When the log request was entered at a terminal (mode 'R'), the system shall, after writing the queues, clear the screen by sending a single blank character, unlock the keyboard and end the task. (rules DEML-BR-003)
2. GIVEN mode: 'R' WHEN the log request was entered at a terminal (mode 'R') THEN The terminal screen is erased, the keyboard is unlocked, and the task ends. (DEML-C01-AC-01; DEML-BR-003)

### Requirement 4: DEML-REQ-F-004 (design note)

#### Acceptance criteria

1. When the logger was called by another program (mode 'C'), the system shall return to the caller without any screen output. (rules DEML-BR-004)
2. GIVEN mode: 'C'; calling program: LGAPOL01 WHEN the logger was called by another program (mode 'C') THEN Control returns to LGAPOL01; nothing is sent to a screen. (DEML-C01-AC-02; DEML-BR-004)
