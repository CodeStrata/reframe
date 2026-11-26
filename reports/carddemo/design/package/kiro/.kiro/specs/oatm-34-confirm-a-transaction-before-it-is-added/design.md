# Design: Confirm a transaction before it is added (OATM-C34)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Makes the operator explicitly confirm a validated transaction before it is added. 'N', 'n' or blank asks 'Confirm to add this transaction...'. Any value other than Y/y, N/n or blank gets 'Invalid value. Valid values are (Y/N)...'. No transaction may ever be added without an explicit 'Y' or 'y'.

Runs as online. Journeys: J04.

## Screens and components

### Add transaction (S-TRANSACTION-ADD)

Enter a transaction against an account or card, see what to fix at each field, confirm the summary and record it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add this transaction? | dialog | Summary of the transaction with 'Confirm to add this transaction...'. Confirm adds it; Cancel returns to the form with nothing added. Buttons replace typing Y/N, so 'Invalid value. Valid values are (Y/N)...' cannot arise. |  |  | OATM-REQ-F-284, OATM-REQ-F-285 |


## Data models

#### CVACT03Y

File record of COTRN02C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA05Y

File record of COTRN02C. Source: `app/cpy/CVTRA05Y.cpy`.

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

- COCOM01Y (working storage of COTRN02C): see data-contracts.md.
- COTTL01Y (working storage of COTRN02C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN02C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN02C): see data-contracts.md.
- CVACT01Y (working storage of COTRN02C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-301 | Prompt operator to confirm addition | business rule | WHEN every field passes validation and Confirm is 'N', 'n' or left blank, THE Transaction Add screen SHALL redisplay with 'Confirm to add this transaction...' and the cursor on Confirm, and add nothing. | high | app/cbl/COTRN02C.cbl:160-188, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-302 | Reject invalid confirmation value | business rule | WHEN every field passes validation and Confirm holds any other value, THE Transaction Add screen SHALL redisplay with 'Invalid value. Valid values are (Y/N)...' and the cursor on Confirm, and add nothing. | high | app/cbl/COTRN02C.cbl:160-188, app/cbl/COTRN02C.cbl:516-534 |

### Worked examples

- OATM-BR-301: All fields = valid; Confirm = N → 'Confirm to add this transaction...' is shown and nothing is written
- OATM-BR-301: All fields = valid; Confirm = (blank) → 'Confirm to add this transaction...' is shown and nothing is written
- OATM-BR-302: All fields = valid; Confirm = X → 'Invalid value. Valid values are (Y/N)...' is shown and nothing is written

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-177: What type and length should the transaction number have in the transaction master store, so that new transaction numbers meet that format? (Data architect) On OATM-BR-301, OATM-BR-302.
- SME-178: When the origination and processing dates entered as YYYY-MM-DD are stored as timestamps, what time portion and timestamp format should be used? (Data architect) On OATM-BR-301, OATM-BR-302.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).