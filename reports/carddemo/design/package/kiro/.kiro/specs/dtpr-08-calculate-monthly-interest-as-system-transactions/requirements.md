# Requirements: Calculate monthly interest as system transactions (DTPR-C08)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

The scheduled monthly interest job, run at billing-cycle close for a supplied processing date. It turns interest on category balances into system transactions and writes them to a new system transaction file of 350-byte records. It serves the card operations team. It must run before transactions are combined, and it must never leave a partial system transaction file when it fails.

**User story:** As a card operations team, I want monthly interest calculated at billing-cycle close and produced as system transactions, so that interest charges are added to the transaction history before transactions are combined.

## Requirements

### Requirement 1: DTPR-REQ-F-059 (design note)

#### Acceptance criteria

1. The system shall run the interest program (CBACT04C) with the processing date supplied as an external parameter ('2022071800' in the delivered job), reading the transaction category balances, card cross-reference (by card and by account), account master and disclosure groups in shared mode. (rules DTPR-BR-063)
2. GIVEN Job parameter: '2022071800' WHEN Interest Calculation job runs THEN The interest program runs with processing date 2022071800 and the input files remain open to other readers (DTPR-C08-AC-01; DTPR-BR-063)

### Requirement 2: DTPR-REQ-F-060 (design note)

#### Acceptance criteria

1. The system shall write the generated system transactions to a new generation of the system transaction file (AWS.M2.CARDDEMO.SYSTRAN) of fixed 350-byte records. (rules DTPR-BR-064)
2. GIVEN Step outcome: normal end WHEN Interest Calculation job runs THEN A new SYSTRAN generation is cataloged (DTPR-C08-AC-02; DTPR-BR-064)
3. GIVEN Step outcome: abend WHEN Interest Calculation job runs THEN The new SYSTRAN generation is deleted (DTPR-C08-AC-03; DTPR-BR-064)

### Requirement 3: DTPR-REQ-N-002 (design note)

#### Acceptance criteria

1. If the interest step fails, then the system shall delete the new system transaction generation, cataloguing it only when the step ends normally. (rules DTPR-BR-064)
2. GIVEN Step outcome: normal end WHEN Interest Calculation job runs THEN A new SYSTRAN generation is cataloged (DTPR-C08-AC-02; DTPR-BR-064)
3. GIVEN Step outcome: abend WHEN Interest Calculation job runs THEN The new SYSTRAN generation is deleted (DTPR-C08-AC-03; DTPR-BR-064)

### Requirement 4: DTPR-REQ-F-061 (business rule)

#### Acceptance criteria

1. When the billing cycle closes each month, the system shall run the interest calculation before the job that combines the system transactions (COMBTRAN). (rules DTPR-BR-065)
2. GIVEN Billing cycle: closes 31 July WHEN Interest Calculation job runs THEN The interest job runs once for that cycle, then COMBTRAN runs (DTPR-C08-AC-04; DTPR-BR-065)
