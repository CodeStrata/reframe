# Design: Produce account extracts from the account master (DTPR-C14)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Overview

Produces fresh extracts of the account master in three layouts (fixed account records, account array records and variable-length records) so downstream processes can use account data without reading the master directly. The account master is only read, never changed. Every run must replace the extracts completely, and the run must never leave behind extracts from a failed run.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-080 | Produce account extracts from account master | design note | THE Account Master Extract Run SHALL first delete any earlier account extract, account array extract and variable-record extract (AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, .ARRYPS, .VBPS) so that each run writes them afresh. | medium | app/jcl/READACCT.jcl:22-28, app/jcl/READACCT.jcl:32-50, app/cbl/CBACT01C.cbl:29-50, app/cbl/CBACT01C.cbl:80-85 |
| DTPR-BR-081 | Produce account extracts from account master | side effect | THE Account Master Extract Run SHALL run the account master reader (CBACT01C) with shared read access to the account master (AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS) and write three new extracts: the account extract (107-byte fixed records), the account array extract (110-byte fixed records) and the variable-record extract (variable records up to 84 bytes). | medium | app/jcl/READACCT.jcl:22-28, app/jcl/READACCT.jcl:32-50, app/cbl/CBACT01C.cbl:29-50, app/cbl/CBACT01C.cbl:80-85 |
| DTPR-BR-082 | Produce account extracts from account master | error handling | WHEN the reader step completes normally, THE Account Master Extract Run SHALL catalog each extract, and WHEN the step fails it SHALL delete them. | medium | app/jcl/READACCT.jcl:22-28, app/jcl/READACCT.jcl:32-50, app/cbl/CBACT01C.cbl:29-50, app/cbl/CBACT01C.cbl:80-85 |

### Worked examples

- DTPR-BR-080: AWS.M2.CARDDEMO.ACCTDATA.PSCOMP = exists from last run → It is deleted before the reader runs and a new one is created.
- DTPR-BR-081: account master = 50 accounts → AWS.M2.CARDDEMO.ACCTDATA.PSCOMP, AWS.M2.CARDDEMO.ACCTDATA.ARRYPS and AWS.M2.CARDDEMO.ACCTDATA.VBPS are created from those accounts.
- DTPR-BR-082: CBACT01C step = abends → None of the three extracts is kept.

## Decision tables

None.

## Design notes

- DTPR-BR-080: The extract job must clear out the previous run's account extract, account array extract and variable-record extract before writing, so each run's outputs are regenerated from scratch and never appended to or merged with older data.

## Open questions

- SME-006: The account extract replaces a zero cycle debit with 2,525.00, and the balance array record is filled with fixed amounts (cycle debits 1,005.00, 1,525.00 and -2,500.00; a balance of -1,025.00). Are these real business values or test data to be replaced? And when an account has a non-zero cycle debit, should its own value be carried through to the extract? (Business analyst) On DTPR-BR-082.
- SME-007: The extract accepts a write result of '10' as well as '00' as success. Should accepting '10' be kept in the new system? (Technical lead) On DTPR-BR-082.
- SME-008: Do downstream consumers depend on the exact fixed record layouts of the account extracts (including the different status and financial record lengths), so they must be kept? (Integration team) On DTPR-BR-082.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).