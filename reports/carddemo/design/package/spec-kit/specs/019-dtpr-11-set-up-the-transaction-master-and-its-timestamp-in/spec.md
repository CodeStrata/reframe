# Feature specification: Set up the transaction master and its timestamp index

**Feature:** DTPR-C11 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C11)

As a card operations team, I want the transaction master loaded from the initial daily transaction file and indexed by processed timestamp, so that transactions can be accessed both by ID and by when they were processed.

A setup job that recreates the transaction master empty, loads it from the initial daily transaction file, and builds an index on the processed timestamp, so transactions can be found by ID or by when they were processed. It serves the card operations team. It must load every record, and the timestamp index must allow many transactions with the same timestamp.

**Acceptance scenarios:**

1. **Given** Initial daily transaction file: 300 records; Transaction master before the job: old content, **when** transaction master setup job (TRANFILE, STEP15) runs, **then** The old master is deleted and redefined empty, then loaded with the 300 records. (DTPR-C11-AC-01)
2. **Given** Transaction master: 2 transactions with the same processed timestamp 2022-07-18-10.15.00.000000, **when** the transaction master has been loaded, **then** Both transactions are indexed under that timestamp in AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX and can be read through the alternate path. (DTPR-C11-AC-02)

## Requirements

### Functional requirements

- **DTPR-REQ-F-065** (design note): The system shall copy every record of the initial daily transaction file 'AWS.M2.CARDDEMO.DALYTRAN.PS.INIT' into the transaction master 'AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS', which earlier steps of the same setup job delete and redefine empty, opening both files for shared access. Rules: DTPR-BR-072.
- **DTPR-REQ-F-066** (design note): When the transaction master has been loaded, the system shall build the alternate index 'AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX' from the transaction master, keyed on the 26-byte processed timestamp at offset 304, with duplicate keys allowed. Rules: DTPR-BR-073.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-072 | Load transaction master from daily file | design note | THE transaction master setup job (TRANFILE, STEP15) SHALL copy every record of the initial daily transaction file 'AWS.M2.CARDDEMO.DALYTRAN.PS.INIT' into the transaction master 'AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS', which earlier steps in the same job delete and redefine empty, opening both files for shared access. | medium | app/jcl/TRANFILE.jcl:32-74 |
| DTPR-BR-073 | Build alternate index over transactions | design note | WHEN the transaction master has been loaded, THE transaction master setup job (TRANFILE, STEP30) SHALL build the alternate index 'AWS.M2.CARDDEMO.TRANSACT.VSAM.AIX' from the transaction master 'AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS'. The index is keyed on the 26-byte processed timestamp at offset 304, and duplicate keys are allowed. | medium | app/jcl/TRANFILE.jcl:76-111 |

### Key entities

None found in the source.

### Needs clarification

- SME-291: Which transaction attribute is the alternate key of the transaction alternate index? (Data architecture team) On DTPR-BR-073, DTPR-BR-072.
- SME-292: When daily transactions are loaded into the transaction master, should records with a key already present replace, merge with, or be rejected against the existing records? (Business analyst, daily transaction processing) On DTPR-BR-073, DTPR-BR-072.
- SME-293: What should happen if the transaction master store does not exist or the load fails — including whether the alternate index build is skipped? (Batch operations team) On DTPR-BR-073, DTPR-BR-072.
- SME-294: If the transaction master load is interrupted after a partial load, must it be rerunnable without duplicating or losing records? (Batch operations team) On DTPR-BR-073, DTPR-BR-072.
- SME-295: While the transaction master load and index build run, may other processes read or update the transaction master? What isolation is required? (Data architecture team) On DTPR-BR-073, DTPR-BR-072.
- DEF-105: Is this intended? No step has a condition code check, so the load and index build still run after a failed definition in STEP10. STEP05 also resets delete errors up to 8 to 0. (Subject-matter expert) On DTPR-BR-072.

### Decision table gaps

None.
