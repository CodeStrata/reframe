# Requirements: Record log messages to the standard and error queues (DEML-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Diagnostic and Error Message Logging · runs as service · risk high

## Introduction

Writes every diagnostic and error message to the standard system log, and also to an application error queue that support staff review. The error queue is 'GENAERRS' by default, but a caller can redirect a message to another queue by starting it with 'Q=' and a 4-character code. It must never block or fail the calling business transaction: messages go to both destinations, but a write that fails or has no room is dropped silently.

**User story:** As an operations or support team member, I want every diagnostic and error message written to the standard log queue and to an error queue that callers can redirect, so that I can find and review application errors.

## Requirements

### Requirement 1: DEML-REQ-F-005 (side effect)

#### Acceptance criteria

1. The system shall write every log record, with length message length plus 5, to the transient data queue 'CSMT'. (rules DEML-BR-005)
2. GIVEN A log record 'GENA LGAPDB01 INSERT POLICY FAILED' with message length 29 WHEN The logger records it THEN The record is written to the standard log queue 'CSMT' with length 34 (29 plus 5) (DEML-C02-AC-03; DEML-BR-005)

### Requirement 2: DEML-REQ-F-006 (business rule)

#### Acceptance criteria

1. The system shall write to the temporary storage queue 'GENAERRS' unless the message text begins with 'Q='. (rules DEML-BR-006)
2. GIVEN A message text that does not begin with 'Q=', e.g. 'LGAPDB01 INSERT POLICY FAILED' WHEN The logger records it THEN The record is written to the error queue 'GENAERRS' (DEML-C02-AC-04; DEML-BR-006)
3. GIVEN A message text that contains 'Q=' but not at the start, e.g. 'ERROR Q=ABCD' WHEN The logger records it THEN The record is written to the error queue 'GENAERRS' and the text is logged unchanged (DEML-C02-AC-05; DEML-BR-006)

### Requirement 3: DEML-REQ-F-007 (business rule)

#### Acceptance criteria

1. When the message text begins with 'Q=', the system shall write to the queue named 'GENA' plus the 4 characters after 'Q=', remove the first 7 characters ('Q=', the 4-character code and the following character) from the logged text, and reduce the record length by 7. (rules DEML-BR-007)
2. GIVEN A message text 'Q=TEST CUSTOMER 0001 ADDED' with record length 31 WHEN The logger records it THEN The record is written to the queue 'GENATEST', the logged text is 'CUSTOMER 0001 ADDED' (first 7 characters removed) and the record length is 24 (31 minus 7) (DEML-C02-AC-06; DEML-BR-007)

### Requirement 4: DEML-REQ-F-008 (side effect)

#### Acceptance criteria

1. The system shall also write the same record to the temporary storage queue ('GENAERRS' or its 'Q=' override) without waiting for storage, so the record is dropped when no space is available. (rules DEML-BR-008)
2. GIVEN temporary storage: full WHEN error logger runs THEN The record goes to 'CSMT' only; the queue write is skipped and the task carries on. (DEML-C02-AC-01; DEML-BR-008)

### Requirement 5: DEML-REQ-N-001 (error handling)

#### Acceptance criteria

1. If either queue write fails, then the system shall ignore the response code and shall not tell the caller. (rules DEML-BR-009)
2. GIVEN queue write result: failure WHEN either queue write fails THEN No error is raised and the caller receives control back as normal. (DEML-C02-AC-02; DEML-BR-009)
