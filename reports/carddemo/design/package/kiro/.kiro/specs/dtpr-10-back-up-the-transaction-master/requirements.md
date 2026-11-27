# Requirements: Back up the transaction master (DTPR-C10)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Copies the whole transaction master into a new backup version of 350-byte records, giving a point-in-time copy for consolidation, extracts and recovery. It serves the card operations team. It must copy every record, must not block other jobs reading the master, and must keep the new backup only when the copy succeeds.

**User story:** As a card operations team, I want the transaction master copied into a new backup generation, so that a point-in-time copy of transaction history is available for consolidation, extracts and recovery.

## Requirements

### Requirement 1: DTPR-REQ-F-064 (design note)

#### Acceptance criteria

1. The system shall copy every record of the transaction master (AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS), read shared with other jobs, into a new generation of the transaction backup (AWS.M2.CARDDEMO.TRANSACT.BKUP(+1)) of fixed-length 350-byte records. (rules DTPR-BR-069, DTPR-BR-070)
2. GIVEN transaction master: 500 transaction records; latest backup generation: G0074V00 WHEN Transaction History Backup job runs THEN A new backup generation G0075V00 holding the 500 records as 350-byte records is catalogued. (DTPR-C10-AC-01; DTPR-BR-069)
3. GIVEN copy step: fails WHEN Transaction History Backup job runs THEN The new backup generation is deleted and not catalogued. (DTPR-C10-AC-02; DTPR-BR-069)
4. GIVEN Records in transaction master: 5,000 WHEN Transaction History Backup runs THEN A new backup generation is created holding the same 5,000 records, each 350 bytes. (DTPR-C10-AC-03; DTPR-BR-070)

### Requirement 2: DTPR-REQ-N-004 (error handling)

#### Acceptance criteria

1. When the backup step ends normally, the system shall keep (catalog) the new backup generation. (rules DTPR-BR-069, DTPR-BR-071)
2. GIVEN transaction master: 500 transaction records; latest backup generation: G0074V00 WHEN Transaction History Backup job runs THEN A new backup generation G0075V00 holding the 500 records as 350-byte records is catalogued. (DTPR-C10-AC-01; DTPR-BR-069)
3. GIVEN copy step: fails WHEN Transaction History Backup job runs THEN The new backup generation is deleted and not catalogued. (DTPR-C10-AC-02; DTPR-BR-069)
4. GIVEN Backup step outcome: ends normally WHEN the backup step ends normally THEN The new backup generation is catalogued and becomes the current backup. (DTPR-C10-AC-04; DTPR-BR-071)
5. GIVEN Backup step outcome: abends WHEN the backup step ends normally THEN The new backup generation is deleted. (DTPR-C10-AC-05; DTPR-BR-071)

### Requirement 3: DTPR-REQ-N-005 (error handling)

#### Acceptance criteria

1. If the backup step fails, then the system shall delete the new backup generation. (rules DTPR-BR-069, DTPR-BR-071)
2. GIVEN transaction master: 500 transaction records; latest backup generation: G0074V00 WHEN Transaction History Backup job runs THEN A new backup generation G0075V00 holding the 500 records as 350-byte records is catalogued. (DTPR-C10-AC-01; DTPR-BR-069)
3. GIVEN copy step: fails WHEN Transaction History Backup job runs THEN The new backup generation is deleted and not catalogued. (DTPR-C10-AC-02; DTPR-BR-069)
4. GIVEN Backup step outcome: ends normally WHEN the backup step ends normally THEN The new backup generation is catalogued and becomes the current backup. (DTPR-C10-AC-04; DTPR-BR-071)
5. GIVEN Backup step outcome: abends WHEN the backup step ends normally THEN The new backup generation is deleted. (DTPR-C10-AC-05; DTPR-BR-071)
