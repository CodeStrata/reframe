# Feature specification: Report import run statistics

**Feature:** CPBM-C07 · Customer Profile Branch Migration · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CPBM-C07)

As a branch migration operator, I want the import to report how many records it read, imported and rejected, so that I can reconcile the target files against the migration file.

Reports at the end of an import how many records were read, how many customers, accounts, cross-references, transactions and cards were imported, and how many error records and unknown types were found, so the operator can reconcile the targets. The legacy import then always prints 'CBIMPORT: Import validation completed' and 'CBIMPORT: No validation errors detected' without checking anything. That message must not be read as proof of reconciliation; the counts are the only real check.

**Acceptance scenarios:**

1. **Given** records in export: 10 C, 12 A, 15 X, 40 T, 15 D, 2 unknown, **when** the import completes without abending, **then** The totals displayed are Read 94, Customers 10, Accounts 12, XRefs 15, Transactions 40, Cards 15, Errors Written 2, Unknown Record Types 2. (CPBM-C07-AC-01)
2. **Given** outcome: abend on a write, **when** the import completes without abending, **then** No totals are displayed. (CPBM-C07-AC-02)
3. **Given** Export file: accounts present but no matching card records; Records read: 1,200, **when** the customer data import has processed every record in the export file, **then** The job log shows 'CBIMPORT: Import validation completed' and 'CBIMPORT: No validation errors detected'; no mismatch is reported. (CPBM-C07-AC-03)
4. **Given** Unknown record types in export file: 5; Errors written: 5, **when** the customer data import has processed every record in the export file, **then** The job log still shows 'CBIMPORT: No validation errors detected' before the final totals list 'Errors Written' as 5. (CPBM-C07-AC-04)
5. **Given** unknown record types found: 3, **when** Imported records are copied verbatim with no business validation applies, **then** The run still displays 'CBIMPORT: No validation errors detected'. (CPBM-C07-AC-05)

## Requirements

### Functional requirements

- **CPBM-REQ-F-024** (side effect): When the import completes without abending, the system shall close all files and display 'CBIMPORT: Import completed' followed by the counts of records read, customers, accounts, cross-references, transactions and cards imported, error records written and unknown record types. Rules: CPBM-BR-029.
- **CPBM-REQ-F-025** (historical artifact): When the import has processed every record in the export file, the system shall always display 'CBIMPORT: Import validation completed' and 'CBIMPORT: No validation errors detected' without performing any checksum, record-count reconciliation or cross-file check, even when error records were written. Rules: CPBM-BR-030, CPBM-BR-031.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CPBM-BR-029 | Import run statistics and reconciliation counts | side effect | WHEN the import completes without abending, THE import batch SHALL close all files and display 'CBIMPORT: Import completed' followed by the counts of records read, customers, accounts, cross-references, transactions and cards imported, error records written and unknown record types. | medium | app/cbl/CBIMPORT.cbl:139-147, app/cbl/CBIMPORT.cbl:252-256, app/cbl/CBIMPORT.cbl:455-478, app/cbl/CBIMPORT.cbl:425-446 |
| CPBM-BR-030 | Post-import validation and checksum step is a no-op | historical artifact | WHEN the customer data import has processed every record in the export file, THE import job SHALL always print 'CBIMPORT: Import validation completed' and 'CBIMPORT: No validation errors detected' without performing any checksum, record-count reconciliation or cross-file check (3000-VALIDATE-IMPORT), even when error records were written. | medium | app/cbl/CBIMPORT.cbl:165-171, app/cbl/CBIMPORT.cbl:449-452, app/cbl/CBIMPORT.cbl:425-447, app/cbl/CBIMPORT.cbl:455-477 |
| CPBM-BR-031 | Imported records are copied verbatim with no business validation | historical artifact | AFTER the export file is processed, THE import batch SHALL always display 'CBIMPORT: Import validation completed' and 'CBIMPORT: No validation errors detected', although no validation was carried out. | high | app/cbl/CBIMPORT.cbl:288-422, app/cbl/CBIMPORT.cbl:323-349, app/cbl/CBIMPORT.cbl:449-452, app/cbl/CBIMPORT.cbl:8-11 |

### Key entities

- CVACT01Y (file record)
- CVACT02Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CVEXPORT (file record)
- CVTRA05Y (file record)

### Needs clarification

- SME-026: Should the migration import apply the same checks as online maintenance (valid account status, balance within credit limit, FICO 300-850, valid dates, existing account and customer for cross-references and cards), or can the export be trusted as already valid? (Business analyst) On CPBM-BR-031.
- DEF-033: Is this intended? The program header promises validation and checksum checks, but the validation step only displays 'No validation errors detected' and no data is checked. (Subject-matter expert) On CPBM-BR-031.
- DEF-161: Confirm this is deliberate: The validation step always reports 'No validation errors detected', even when the run has written error records for unknown record types or the export was incomplete, so the job log can contradict the 'Errors Written' total printed right after it. (Subject-matter expert) On CPBM-BR-030.

### Decision table gaps

None.
