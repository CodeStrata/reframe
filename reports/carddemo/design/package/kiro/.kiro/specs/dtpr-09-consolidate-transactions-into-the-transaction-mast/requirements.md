# Requirements: Consolidate transactions into the transaction master (DTPR-C09)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Combines the latest transaction backup with the latest system-generated (interest) transactions into one set sorted by transaction ID, then loads that set into the transaction master. It serves the card operations team, so the master holds all activity including interest. It must never publish a combined set from a failed sort, and it must keep the transaction ID order.

**User story:** As a card operations team, I want backed-up and system-generated transactions combined in transaction ID order and loaded into the transaction master, so that the master holds all activity including interest.

## Requirements

### Requirement 1: DTPR-REQ-F-062 (design note)

#### Acceptance criteria

1. The system shall combine the latest transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP) with the latest system-generated transactions (AWS.M2.CARDDEMO.SYSTRAN) into a new generation of AWS.M2.CARDDEMO.TRANSACT.COMBINED, sorted ascending by transaction ID (first 16 characters). (rules DTPR-BR-066)
2. GIVEN backup transaction ID: 0000000000000005; system transaction ID: 0000000000000003 WHEN transaction consolidation job runs THEN The combined file lists 0000000000000003 before 0000000000000005 (DTPR-C09-AC-01; DTPR-BR-066)

### Requirement 2: DTPR-REQ-N-003 (error handling)

#### Acceptance criteria

1. If the sort step fails, then the system shall delete the new combined generation instead of cataloguing it. (rules DTPR-BR-067)
2. GIVEN sort step: abends WHEN the sort step fails THEN No new generation of AWS.M2.CARDDEMO.TRANSACT.COMBINED is catalogued (DTPR-C09-AC-02; DTPR-BR-067)

### Requirement 3: DTPR-REQ-F-063 (design note)

#### Acceptance criteria

1. The system shall then copy every record of the new combined transaction generation (AWS.M2.CARDDEMO.TRANSACT.COMBINED) into the keyed transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS). (rules DTPR-BR-068)
2. GIVEN records in combined file: 1,250 WHEN transaction consolidation job runs THEN All 1,250 records are loaded into the transaction master in transaction-ID order (DTPR-C09-AC-03; DTPR-BR-068)
