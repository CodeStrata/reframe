# Requirements: Produce account extracts from the account master (DTPR-C14)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Produces fresh extracts of the account master in three layouts (fixed account records, account array records and variable-length records) so downstream processes can use account data without reading the master directly. The account master is only read, never changed. Every run must replace the extracts completely, and the run must never leave behind extracts from a failed run.

**User story:** As a card operations team, I want fresh extracts of the account master in fixed, array and variable-record formats, so that downstream processes can use account data without accessing the master directly.

## Requirements

### Requirement 1: DTPR-REQ-F-072 (design note)

#### Acceptance criteria

1. The system shall first delete any earlier account extract, account array extract and variable-record extract (AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, .ARRYPS, .VBPS) so that each run writes them afresh. (rules DTPR-BR-080)
2. GIVEN AWS.M2.CARDDEMO.ACCTDATA.PSCOMP: exists from last run WHEN Account Master Extract Run runs THEN It is deleted before the reader runs and a new one is created. (DTPR-C14-AC-01; DTPR-BR-080)

### Requirement 2: DTPR-REQ-F-073 (side effect)

#### Acceptance criteria

1. The system shall run the account master reader (CBACT01C) with shared read access to the account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS) and write three new extracts: the account extract (107-byte fixed records), the account array extract (110-byte fixed records) and the variable-record extract (variable records up to 84 bytes). (rules DTPR-BR-081)
2. GIVEN account master: 50 accounts WHEN Account Master Extract Run runs THEN AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, AWS.M2.CARDDEMO.ACCTDATA.ARRYPS and AWS.M2.CARDDEMO.ACCTDATA.VBPS are created from those accounts. (DTPR-C14-AC-02; DTPR-BR-081)

### Requirement 3: DTPR-REQ-N-009 (error handling)

#### Acceptance criteria

1. When the reader step completes normally, the system shall catalog each extract. (rules DTPR-BR-082)
2. GIVEN CBACT01C step: abends WHEN the reader step completes normally THEN None of the three extracts is kept. (DTPR-C14-AC-03; DTPR-BR-082)

### Requirement 4: DTPR-REQ-N-010 (error handling)

#### Acceptance criteria

1. If the reader step fails, then the system shall delete the extracts. (rules DTPR-BR-082)
2. GIVEN CBACT01C step: abends WHEN the reader step completes normally THEN None of the three extracts is kept. (DTPR-C14-AC-03; DTPR-BR-082)
