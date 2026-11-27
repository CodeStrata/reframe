# Consolidate transactions into the transaction master (DTPR-C09)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-066 | Combine and order transactions by identifier | design note | THE transaction consolidation job SHALL combine the latest transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP) with the latest system-generated transactions (AWS.M2.CARDDEMO.SYSTRAN) into a new generation of AWS.M2.CARDDEMO.TRANSACT.COMBINED, sorted ascending by transaction ID (first 16 characters). | medium | app/jcl/COMBTRAN.jcl:22-37 |
| DTPR-BR-067 | Combine and order transactions by identifier | error handling | WHEN the sort step fails, THE transaction consolidation job SHALL delete the new combined generation instead of cataloguing it. | medium | app/jcl/COMBTRAN.jcl:22-37 |
| DTPR-BR-068 | Load combined transactions into transaction master | design note | THE transaction consolidation job SHALL then copy every record of the new combined transaction generation (AWS.M2.CARDDEMO.TRANSACT.COMBINED) into the keyed transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS). | medium | app/jcl/COMBTRAN.jcl:41-48, app/jcl/COMBTRAN.jcl:33-37 |

### Worked examples

- DTPR-BR-066: backup transaction ID = 0000000000000005; system transaction ID = 0000000000000003 → The combined file lists 0000000000000003 before 0000000000000005
- DTPR-BR-067: sort step = abends → No new generation of AWS.M2.CARDDEMO.TRANSACT.COMBINED is catalogued
- DTPR-BR-068: records in combined file = 1,250 → All 1,250 records are loaded into the transaction master in transaction-ID order

## Decision tables

None.

## Design notes

- DTPR-BR-066: Build a sorted extract that merges the latest transaction backup with the latest system-transaction batch, ordered ascending by the 16-character transaction ID, and publish it as a new version. Make it a scheduled step that depends on the backup and interest jobs, and discard its output if it fails.
- DTPR-BR-068: Load every record of the combined, sorted set into the transaction store keyed by transaction ID, as a bulk load or upsert in one step. Decide explicitly what to do with duplicate transaction IDs.

## Open questions

- SME-125: When combined transactions are loaded into the transaction master, what should happen if a transaction ID already exists there: replace it, keep the existing record, or fail the load? (Business analyst / data owner) On DTPR-BR-067, DTPR-BR-068.
- SME-126: When the transaction backup file and the system transaction file are merged, how should two records with the same transaction ID be handled: keep both, keep one, or treat it as an error? (Business analyst) On DTPR-BR-067, DTPR-BR-068.
- SME-127: While the transaction combine-and-load job runs, may other processes read or update the input files and the transaction master? (Batch operations team) On DTPR-BR-067, DTPR-BR-068.
- DEF-109: Is this intended? The load step has no return-code test on the sort step. A failed sort does not stop the job; the step is attempted anyway and fails only when the new generation it needs cannot be found. (Subject-matter expert) On DTPR-BR-068.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
