# Implementation plan: Print the daily transaction report with totals (DTPR-C17)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

No screens: it runs as scheduled job.

## Data model

#### CVACT03Y

File record of CBTRN03C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA03Y

File record of CBTRN03C. Source: `app/cpy/CVTRA03Y.cpy`.

Record `TRAN-TYPE-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-TYPE |  | X(02) | text, 2 characters |  |  |  |
| TRAN-TYPE-DESC |  | X(50) | text, 50 characters |  |  |  |
| FILLER |  | X(08) | text, 8 characters |  |  |  |

#### CVTRA04Y

File record of CBTRN03C. Source: `app/cpy/CVTRA04Y.cpy`.

Record `TRAN-CAT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-CAT-KEY |  |  | group |  |  |  |
| TRAN-TYPE-CD | TRAN-CAT-KEY | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD | TRAN-CAT-KEY | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-CAT-TYPE-DESC |  | X(50) | text, 50 characters |  |  |  |
| FILLER |  | X(04) | text, 4 characters |  |  |  |

#### CVTRA05Y

File record of CBTRN03C. Source: `app/cpy/CVTRA05Y.cpy`.

Record `TRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| TRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| TRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| TRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| TRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| TRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| TRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

- CVTRA07Y (working storage of CBTRN03C): see data-contracts.md.

## Design notes

None.

## Decision tables

#### Report handling of each read

| Read result | Processing date within reporting period | Report action | Rule |
|---|---|---|---|
| Transaction read | Yes | Add amount to page total and account total, then print detail line | DTPR-BR-094 |
| Transaction read | No | Stop at once, skip this and all later transactions, close files without final page, account or grand totals | DTPR-BR-098 |
| End of transaction file | Not applicable | Add last transaction's amount to page and account totals a second time, print final 'Page Total', then 'Grand Total' | DTPR-BR-097 |
| End of transaction file | No transaction read at all | **Gap:** No rule says what amount is added a second time, or what totals print, when the file is empty. | |

