# Requirements: Report export reconciliation counts (CPBM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Data Setup · Customer Profile Branch Migration · runs as service · risk high

## Introduction

Reports how many customers, accounts, cross-references, transactions and cards were exported, and the total, so the operator can reconcile the migration file against the source data. Each type's count is shown when that type finishes, and the full set is shown when the export completes. The total must always equal the last sequence number written.

**User story:** As a branch migration operator, I want the export to report how many records of each type it exported and in total, so that I can reconcile the migration file against the source files.

## Requirements

### Requirement 1: CPBM-REQ-F-008 (side effect)

#### Acceptance criteria

1. When each record type is finished, the system shall display that type's count, for example 'CBEXPORT: Customers exported: ' with the count. (rules CPBM-BR-012)
2. GIVEN cards written: 70 WHEN each record type is finished THEN 'CBEXPORT: Cards exported: ' with 70 is displayed before the final totals. (CPBM-C03-AC-01; CPBM-BR-012)

### Requirement 2: CPBM-REQ-F-009 (side effect)

#### Acceptance criteria

1. When the export finishes, the system shall close all files and display 'CBEXPORT: Export completed' followed by the counts of customers, accounts, cross-references, transactions and cards exported and 'CBEXPORT: Total Records Exported: ' with the total, which equals the last sequence number. (rules CPBM-BR-013)
2. GIVEN customers: 50; accounts: 60; cross-references: 70; transactions: 10,000; cards: 70 WHEN the export finishes THEN The job log shows Customers 50, Accounts 60, XRefs 70, Transactions 10,000, Cards 70 and Total Records Exported 10,250. (CPBM-C03-AC-02; CPBM-BR-013)
