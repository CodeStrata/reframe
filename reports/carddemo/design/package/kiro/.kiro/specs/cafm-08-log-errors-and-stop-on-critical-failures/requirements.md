# Requirements: Log errors and stop on critical failures (CAFM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Makes authorization processing errors traceable for operations analysts. Every error is written to the log. A warning lets processing continue, but a critical error stops the task safely, releasing the database and the request queue. Unread requests must never be lost: they stay on the queue for the next run.

**User story:** As an operations analyst, I want authorization processing errors logged and critical failures to stop processing safely, so that problems are traceable and unread requests are left for a later run.

## Requirements

### Requirement 1: CAFM-REQ-F-080 (error handling)

#### Acceptance criteria

1. When any error is logged as critical, the system shall write the error record to the CSSL log, release the IMS database, close the request queue and end the task, leaving any unread request messages on the queue for a later trigger. (rules CAFM-BR-082)
2. GIVEN Error: 'I003' critical; Messages still on request queue: 40 WHEN any error is logged as critical THEN The task ends after logging; the 40 messages stay on the queue unprocessed. (CAFM-C08-AC-01; CAFM-BR-082)

### Requirement 2: CAFM-REQ-F-081 (error handling)

#### Acceptance criteria

1. When an error is logged as a warning, the system shall write the error record to the CSSL log and continue processing. (rules CAFM-BR-083)
2. GIVEN Error: 'A001' warning 'CARD NOT FOUND IN XREF' WHEN an error is logged as a warning THEN The error is logged and the request continues to a decision and reply. (CAFM-C08-AC-02; CAFM-BR-083)
