# Feature specification: Produce account extracts from the account master

**Feature:** DTPR-C14 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C14)

As a card operations team, I want fresh extracts of the account master in fixed, array and variable-record formats, so that downstream processes can use account data without accessing the master directly.

Produces fresh extracts of the account master in three layouts (fixed account records, account array records and variable-length records) so downstream processes can use account data without reading the master directly. The account master is only read, never changed. Every run must replace the extracts completely, and the run must never leave behind extracts from a failed run.

**Acceptance scenarios:**

1. **Given** AWS.M2.CARDDEMO.ACCTDATA.PSCOMP: exists from last run, **when** Account Master Extract Run runs, **then** It is deleted before the reader runs and a new one is created. (DTPR-C14-AC-01)
2. **Given** account master: 50 accounts, **when** Account Master Extract Run runs, **then** AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, AWS.M2.CARDDEMO.ACCTDATA.ARRYPS and AWS.M2.CARDDEMO.ACCTDATA.VBPS are created from those accounts. (DTPR-C14-AC-02)
3. **Given** CBACT01C step: abends, **when** the reader step completes normally, **then** None of the three extracts is kept. (DTPR-C14-AC-03)

## Requirements

### Functional requirements

- **DTPR-REQ-F-072** (design note): The system shall first delete any earlier account extract, account array extract and variable-record extract (AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, .ARRYPS, .VBPS) so that each run writes them afresh. Rules: DTPR-BR-080.
- **DTPR-REQ-F-073** (side effect): The system shall run the account master reader (CBACT01C) with shared read access to the account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS) and write three new extracts: the account extract (107-byte fixed records), the account array extract (110-byte fixed records) and the variable-record extract (variable records up to 84 bytes). Rules: DTPR-BR-081.
- **DTPR-REQ-N-009** (error handling): When the reader step completes normally, the system shall catalog each extract. Rules: DTPR-BR-082.
- **DTPR-REQ-N-010** (error handling): If the reader step fails, then the system shall delete the extracts. Rules: DTPR-BR-082.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-080 | Produce account extracts from account master | design note | THE Account Master Extract Run SHALL first delete any earlier account extract, account array extract and variable-record extract (AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, .ARRYPS, .VBPS) so that each run writes them afresh. | medium | app/jcl/READACCT.jcl:22-28, app/jcl/READACCT.jcl:32-50, app/cbl/CBACT01C.cbl:29-50, app/cbl/CBACT01C.cbl:80-85 |
| DTPR-BR-081 | Produce account extracts from account master | side effect | THE Account Master Extract Run SHALL run the account master reader (CBACT01C) with shared read access to the account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS) and write three new extracts: the account extract (107-byte fixed records), the account array extract (110-byte fixed records) and the variable-record extract (variable records up to 84 bytes). | medium | app/jcl/READACCT.jcl:22-28, app/jcl/READACCT.jcl:32-50, app/cbl/CBACT01C.cbl:29-50, app/cbl/CBACT01C.cbl:80-85 |
| DTPR-BR-082 | Produce account extracts from account master | error handling | WHEN the reader step completes normally, THE Account Master Extract Run SHALL catalog each extract, and WHEN the step fails it SHALL delete them. | medium | app/jcl/READACCT.jcl:22-28, app/jcl/READACCT.jcl:32-50, app/cbl/CBACT01C.cbl:29-50, app/cbl/CBACT01C.cbl:80-85 |

### Key entities

None found in the source.

### Needs clarification

- SME-006: The account extract replaces a zero cycle debit with 2,525.00, and the balance array record is filled with fixed amounts (cycle debits 1,005.00, 1,525.00 and -2,500.00; a balance of -1,025.00). Are these real business values or test data to be replaced? And when an account has a non-zero cycle debit, should its own value be carried through to the extract? (Business analyst) On DTPR-BR-082.
- SME-007: The extract accepts a write result of '10' as well as '00' as success. Should accepting '10' be kept in the new system? (Technical lead) On DTPR-BR-082.
- SME-008: Do downstream consumers depend on the exact fixed record layouts of the account extracts (including the different status and financial record lengths), so they must be kept? (Integration team) On DTPR-BR-082.

### Decision table gaps

None.
