# Feature specification: Report export reconciliation counts

**Feature:** CPBM-C03 · Customer Profile Branch Migration · Customer Data Setup

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CPBM-C03)

As a branch migration operator, I want the export to report how many records of each type it exported and in total, so that I can reconcile the migration file against the source files.

Reports how many customers, accounts, cross-references, transactions and cards were exported, and the total, so the operator can reconcile the migration file against the source data. Each type's count is shown when that type finishes, and the full set is shown when the export completes. The total must always equal the last sequence number written.

**Acceptance scenarios:**

1. **Given** cards written: 70, **when** each record type is finished, **then** 'CBEXPORT: Cards exported: ' with 70 is displayed before the final totals. (CPBM-C03-AC-01)
2. **Given** customers: 50; accounts: 60; cross-references: 70; transactions: 10,000; cards: 70, **when** the export finishes, **then** The job log shows Customers 50, Accounts 60, XRefs 70, Transactions 10,000, Cards 70 and Total Records Exported 10,250. (CPBM-C03-AC-02)

## Requirements

### Functional requirements

- **CPBM-REQ-F-008** (side effect): When each record type is finished, the system shall display that type's count, for example 'CBEXPORT: Customers exported: ' with the count. Rules: CPBM-BR-012.
- **CPBM-REQ-F-009** (side effect): When the export finishes, the system shall close all files and display 'CBEXPORT: Export completed' followed by the counts of customers, accounts, cross-references, transactions and cards exported and 'CBEXPORT: Total Records Exported: ' with the total, which equals the last sequence number. Rules: CPBM-BR-013.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CPBM-BR-012 | Export reconciliation counts per record type and in total | side effect | WHEN each record type is finished, THE Branch Migration Export SHALL display that type's count, for example 'CBEXPORT: Customers exported: ' with the count. | medium | app/cbl/CBEXPORT.cbl:554-573, app/cbl/CBEXPORT.cbl:254-255, app/cbl/CBEXPORT.cbl:309-310, app/cbl/CBEXPORT.cbl:507-508 |
| CPBM-BR-013 | Export reconciliation counts per record type and in total | side effect | WHEN the export finishes, THE Branch Migration Export SHALL close all files and display 'CBEXPORT: Export completed' followed by the counts of customers, accounts, cross-references, transactions and cards exported and 'CBEXPORT: Total Records Exported: ' with the total, which equals the last sequence number. | medium | app/cbl/CBEXPORT.cbl:554-573, app/cbl/CBEXPORT.cbl:254-255, app/cbl/CBEXPORT.cbl:309-310, app/cbl/CBEXPORT.cbl:507-508 |

### Key entities

- CVACT01Y (file record)
- CVACT02Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CVEXPORT (file record)
- CVTRA05Y (file record)

### Needs clarification

None.

### Decision table gaps

None.
