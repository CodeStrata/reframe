# Feature specification: Stop the export on any file error

**Feature:** CPBM-C04 · Customer Profile Branch Migration · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CPBM-C04)

As a branch migration operator, I want the export to stop at once on any file open, read or write error, so that a failed export is never mistaken for a complete one.

Stops the export at once on any open, read or write failure, so the operator never mistakes a failed export for a complete one. It shows which file failed and its status, then 'CBEXPORT: ABENDING PROGRAM', and ends abnormally without retrying or skipping records. A failed run must never report success, and it leaves only the records already written in a partial file.

**Acceptance scenarios:**

1. **Given** the customer source file cannot be opened and the open returns status '35', **when** the export starts, **then** the job log shows 'ERROR: Cannot open CUSTOMER-INPUT, Status: ' with '35', then 'CBEXPORT: ABENDING PROGRAM', the run ends abnormally, and the export file holds no records (CPBM-C04-AC-01)
2. **Given** all five source files open with status '00' but the export file open returns a status other than '00', **when** the export starts, **then** the job log shows 'ERROR: Cannot open EXPORT-OUTPUT, Status: ' with that status and 'CBEXPORT: ABENDING PROGRAM', and the run ends abnormally before any record is written (CPBM-C04-AC-02)
3. **Given** a read of the account source file returns a status other than '00' or '10', **when** the export reaches the accounts, **then** the job log shows 'ERROR: Reading ACCOUNT-INPUT, Status: ' with that status, then 'CBEXPORT: ABENDING PROGRAM', and the run ends abnormally (CPBM-C04-AC-03)
4. **Given** a read returns status '10' (end of file) on the customer source file, **when** the export finishes the customers, **then** no error is shown and the export continues with the accounts (CPBM-C04-AC-04)
5. **Given** writing an export record returns a status other than '00', **when** the export writes that record, **then** the job log shows 'ERROR: Writing export record, Status: ' with that status, then 'CBEXPORT: ABENDING PROGRAM', and the run ends abnormally (CPBM-C04-AC-05)
6. **Given** 100 customers and 50 accounts exist and the write of the 3rd account's export record fails (records 1 to 102 already written), **when** the export runs, **then** the run ends abnormally at that record without retrying it or moving on to the 4th account, and the export file still holds the 102 records written before the failure (CPBM-C04-AC-06)

## Requirements

### Functional requirements

- **CPBM-REQ-F-010** (error handling): If opening any source file or the export file returns a status other than '00', then the system shall display 'ERROR: Cannot open <file>, Status: ' with the status and 'CBEXPORT: ABENDING PROGRAM', and abend before any record is written. Rules: CPBM-BR-014.
- **CPBM-REQ-F-011** (error handling): If reading any source file returns a status other than '00' or '10' (end of file), or writing an export record returns a status other than '00', then the system shall display 'ERROR: Reading <file>, Status: ' or 'ERROR: Writing export record, Status: ' with the status, then 'CBEXPORT: ABENDING PROGRAM', and abend. Rules: CPBM-BR-015.
- **CPBM-REQ-F-012** (error handling): If a read or a write fails during the export, then the system shall abend at once, without retrying or skipping the record, leaving the records already written in the partial export file. Rules: CPBM-BR-016.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CPBM-BR-014 | Fail-fast abend on any file open, read or write error | error handling | WHEN opening any source file or the export file returns a status other than '00', THE Branch Migration Export SHALL display 'ERROR: Cannot open <file>, Status: ' with the status and 'CBEXPORT: ABENDING PROGRAM', and abend before any record is written. | medium | app/cbl/CBEXPORT.cbl:198-240, app/cbl/CBEXPORT.cbl:327-335, app/cbl/CBEXPORT.cbl:364-370, app/cbl/CBEXPORT.cbl:576-579 |
| CPBM-BR-015 | Export each customer as type C record | error handling | WHEN reading any source file returns a status other than '00' or '10' (end of file), or writing an export record returns a status other than '00', THE Branch Migration Export SHALL display 'ERROR: Reading <file>, Status: ' or 'ERROR: Writing export record, Status: ' with the status, then 'CBEXPORT: ABENDING PROGRAM', and abend. | high | app/cbl/CBEXPORT.cbl:243-310, app/cbl/CBEXPORT.cbl:312-373, app/cbl/CBEXPORT.cbl:376-428, app/cbl/CBEXPORT.cbl:431-493 |
| CPBM-BR-016 | Fail-fast abend on any file open, read or write error | error handling | WHEN a read or a write fails during the export, THE Branch Migration Export SHALL abend at once, without retrying or skipping the record, and the records already written stay in the partial export file. | medium | app/cbl/CBEXPORT.cbl:198-240, app/cbl/CBEXPORT.cbl:327-335, app/cbl/CBEXPORT.cbl:364-370, app/cbl/CBEXPORT.cbl:576-579 |

### Key entities

- CVACT01Y (file record)
- CVACT02Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CVEXPORT (file record)
- CVTRA05Y (file record)

### Needs clarification

- SME-018: Does the first record in the data export get sequence number 1? (Migration team) On CPBM-BR-015.
- SME-019: Every exported record is stamped with branch 0001 and region NORTH. Is that right for all customers, or should branch and region come from customer or account data, or from a run setting? (Data migration lead) On CPBM-BR-015.
- SME-020: When the export is rerun, should it replace or add to the previous export contents, and how should a run that ended abnormally be recovered? (Batch operations) On CPBM-BR-015.
- SME-021: Customer SSNs and card verification codes are copied into the export unmasked. Must the new export protect or leave out these values? (Security team) On CPBM-BR-015.
- SME-022: If the export cannot open one of its files, should the run end abnormally? (Batch operations) On CPBM-BR-015.
- DEF-088: Confirm this is deliberate: The card's CVV code and the customer's SSN and government ID go into the migration file unmasked. Storing a CVV after authorisation is not allowed under PCI DSS. (Subject-matter expert) On CPBM-BR-015.

### Decision table gaps

- Export file error handling: No rule says what happens if closing a file fails at the end of the export.
