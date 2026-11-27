# Requirements: Load pending authorization summaries (CAFM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as scheduled job · risk medium

## Introduction

Loads pending authorization summaries from the summary file into the pending authorization database, one per account. It must never overwrite a summary already held for an account: it reports it and moves on. Any other insert failure stops the load with a failure code.

**User story:** As an operations analyst, I want to load pending authorization summaries from the summary file into the pending authorization database, so that each account's pending authorization summary is available without overwriting a summary already held.

## Requirements

### Requirement 1: CAFM-REQ-F-166 (business rule)

#### Acceptance criteria

1. The system shall insert each record read from the summary file as a pending authorization summary. (rules CAFM-BR-181)
2. GIVEN summary record account: 00000012345; already in database: no WHEN summary load runs THEN The summary is inserted and 'ROOT INSERT SUCCESS' is displayed. (CAFM-C19-AC-01; CAFM-BR-181)

### Requirement 2: CAFM-REQ-F-167 (business rule)

#### Acceptance criteria

1. When a summary insert returns a blank status, the system shall display 'ROOT INSERT SUCCESS'. (rules CAFM-BR-181)
2. GIVEN summary record account: 00000012345; already in database: no WHEN summary load runs THEN The summary is inserted and 'ROOT INSERT SUCCESS' is displayed. (CAFM-C19-AC-01; CAFM-BR-181)

### Requirement 3: CAFM-REQ-F-168 (error handling)

#### Acceptance criteria

1. If a summary insert returns 'II' because that account's summary is already in the database, then the system shall display 'ROOT SEGMENT ALREADY IN DB', leave the existing summary unchanged and continue with the next record. (rules CAFM-BR-182)
2. GIVEN summary record account: 00000012345; already in database: yes (status 'II') WHEN a summary insert returns 'II' because that account's summary is already in the database THEN 'ROOT SEGMENT ALREADY IN DB' is displayed; the stored summary is not changed; the next record is read. (CAFM-C19-AC-02; CAFM-BR-182)

### Requirement 4: CAFM-REQ-F-169 (error handling)

#### Acceptance criteria

1. If a summary insert returns any status other than blank or 'II', then the system shall display 'ROOT INSERT FAILED :' with the status, display 'IMS LOAD ABENDING ...' and stop the load with return code 16. (rules CAFM-BR-183)
2. GIVEN a summary record for account 00000000123 whose insert returns a status other than blank or 'II', for example 'AI' WHEN the summary load inserts it THEN 'ROOT INSERT FAILED :' is displayed with AI, 'IMS LOAD ABENDING ...' is displayed, and the load stops with return code 16 without inserting further records (CAFM-C19-AC-03; CAFM-BR-183)
