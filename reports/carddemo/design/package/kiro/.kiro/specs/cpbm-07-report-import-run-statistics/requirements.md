# Requirements: Report import run statistics (CPBM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as scheduled job · risk high

## Introduction

Reports at the end of an import how many records were read, how many customers, accounts, cross-references, transactions and cards were imported, and how many error records and unknown types were found, so the operator can reconcile the targets. The legacy import then always prints 'CBIMPORT: Import validation completed' and 'CBIMPORT: No validation errors detected' without checking anything. That message must not be read as proof of reconciliation; the counts are the only real check.

**User story:** As a branch migration operator, I want the import to report how many records it read, imported and rejected, so that I can reconcile the target files against the migration file.

## Requirements

### Requirement 1: CPBM-REQ-F-024 (side effect)

#### Acceptance criteria

1. When the import completes without abending, the system shall close all files and display 'CBIMPORT: Import completed' followed by the counts of records read, customers, accounts, cross-references, transactions and cards imported, error records written and unknown record types. (rules CPBM-BR-029)
2. GIVEN records in export: 10 C, 12 A, 15 X, 40 T, 15 D, 2 unknown WHEN the import completes without abending THEN The totals displayed are Read 94, Customers 10, Accounts 12, XRefs 15, Transactions 40, Cards 15, Errors Written 2, Unknown Record Types 2. (CPBM-C07-AC-01; CPBM-BR-029)
3. GIVEN outcome: abend on a write WHEN the import completes without abending THEN No totals are displayed. (CPBM-C07-AC-02; CPBM-BR-029)

### Requirement 2: CPBM-REQ-F-025 (historical artifact)

#### Acceptance criteria

1. When the import has processed every record in the export file, the system shall always display 'CBIMPORT: Import validation completed' and 'CBIMPORT: No validation errors detected' without performing any checksum, record-count reconciliation or cross-file check, even when error records were written. (rules CPBM-BR-030, CPBM-BR-031)
2. GIVEN Export file: accounts present but no matching card records; Records read: 1,200 WHEN the customer data import has processed every record in the export file THEN The job log shows 'CBIMPORT: Import validation completed' and 'CBIMPORT: No validation errors detected'; no mismatch is reported. (CPBM-C07-AC-03; CPBM-BR-030)
3. GIVEN Unknown record types in export file: 5; Errors written: 5 WHEN the customer data import has processed every record in the export file THEN The job log still shows 'CBIMPORT: No validation errors detected' before the final totals list 'Errors Written' as 5. (CPBM-C07-AC-04; CPBM-BR-030)
4. GIVEN unknown record types found: 3 WHEN Imported records are copied verbatim with no business validation applies THEN The run still displays 'CBIMPORT: No validation errors detected'. (CPBM-C07-AC-05; CPBM-BR-031)
