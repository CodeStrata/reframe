# Feature specification: Calculate monthly interest as system transactions

**Feature:** DTPR-C08 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C08)

As a card operations team, I want monthly interest calculated at billing-cycle close and produced as system transactions, so that interest charges are added to the transaction history before transactions are combined.

The scheduled monthly interest job, run at billing-cycle close for a supplied processing date. It turns interest on category balances into system transactions and writes them to a new system transaction file of 350-byte records. It serves the card operations team. It must run before transactions are combined, and it must never leave a partial system transaction file when it fails.

**Acceptance scenarios:**

1. **Given** Job parameter: '2022071800', **when** Interest Calculation job runs, **then** The interest program runs with processing date 2022071800 and the input files remain open to other readers (DTPR-C08-AC-01)
2. **Given** Step outcome: normal end, **when** Interest Calculation job runs, **then** A new SYSTRAN generation is cataloged (DTPR-C08-AC-02)
3. **Given** Step outcome: abend, **when** Interest Calculation job runs, **then** The new SYSTRAN generation is deleted (DTPR-C08-AC-03)
4. **Given** Billing cycle: closes 31 July, **when** Interest Calculation job runs, **then** The interest job runs once for that cycle, then COMBTRAN runs (DTPR-C08-AC-04)

## Requirements

### Functional requirements

- **DTPR-REQ-F-059** (design note): The system shall run the interest program (CBACT04C) with the processing date supplied as an external parameter ('2022071800' in the delivered job), reading the transaction category balances, card cross-reference (by card and by account), account master and disclosure groups in shared mode. Rules: DTPR-BR-063.
- **DTPR-REQ-F-060** (design note): The system shall write the generated system transactions to a new generation of the system transaction file (AWS.M2.CARDDEMO.SYSTRAN) of fixed 350-byte records. Rules: DTPR-BR-064.
- **DTPR-REQ-N-002** (design note): If the interest step fails, then the system shall delete the new system transaction generation, cataloguing it only when the step ends normally. Rules: DTPR-BR-064.
- **DTPR-REQ-F-061** (business rule): When the billing cycle closes each month, the system shall run the interest calculation before the job that combines the system transactions (COMBTRAN). Rules: DTPR-BR-065.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-063 | Run interest step producing system transactions | design note | THE Interest Calculation job SHALL run the interest program (CBACT04C) with the processing date supplied as an external parameter, '2022071800' in the delivered job, reading the transaction category balances, card cross-reference (by card and by account), account master and disclosure groups in shared mode. | medium | app/jcl/INTCALC.jcl:22-41, app/cbl/CBACT04C.cbl:28-56, app/cbl/CBACT04C.cbl:175-180, app/cbl/CBACT04C.cbl:473-480 |
| DTPR-BR-064 | Run interest step producing system transactions | design note | THE Interest Calculation job SHALL write the generated system transactions to a new generation of the system transaction file (AWS.M2.CARDDEMO.SYSTRAN) of fixed 350-byte records, cataloged when the step ends normally and deleted if the step fails. | medium | app/jcl/INTCALC.jcl:22-41, app/cbl/CBACT04C.cbl:28-56, app/cbl/CBACT04C.cbl:175-180, app/cbl/CBACT04C.cbl:473-480 |
| DTPR-BR-065 | Run interest step producing system transactions | business rule | THE Interest Calculation job SHALL run monthly, at billing-cycle close, before the job that combines the system transactions (COMBTRAN). | medium | app/jcl/INTCALC.jcl:22-41, app/cbl/CBACT04C.cbl:28-56, app/cbl/CBACT04C.cbl:175-180, app/cbl/CBACT04C.cbl:473-480 |

### Key entities

None found in the source.

### Needs clarification

- SME-012: Interest transaction IDs are made from the run date plus a sequence number. What type and length must the ID and the sequence part have, and what should happen if the sequence runs out of digits? (Data architecture team) On DTPR-BR-065.
- SME-013: If the interest run fails, the interest transactions are discarded but accounts already updated with interest are not rolled back. Should account updates and interest transactions be saved together as one unit, and how should a restart avoid charging interest twice? (Batch operations) On DTPR-BR-065.

### Decision table gaps

None.
