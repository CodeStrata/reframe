# Design: Look up a single transaction (OATM-C28)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Opens the transaction view for a signed-on user, already filled in and looked up when a transaction was picked on the list. The user can also type a Transaction ID to look one up. It must never look up a blank ID: it shows 'Tran ID can NOT be empty...' and puts the cursor on the ID field.

Runs as online. Journeys: J04.

## Screens and components

### Transactions (S-TRANSACTION-LIST)

Browse transactions in a sortable, paged table or jump to a transaction ID, and open one with Enter or a click instead of typing S beside it. Tab order: search, table, pager, Add transaction.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction (S-TRANSACTION-VIEW)

Show one transaction in full with its merchant, opened from the list or by typing its ID. Tab order: transaction ID, details, merchant, Back to transactions.

Prototype: `ui-reference/index.html#/S-TRANSACTION-VIEW`. Replaces the legacy screens COTRN1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction ID | **lookup field** | Transaction ID, pre-filled when opened from the list | Blank: 'Tran ID can NOT be empty...' - enter a transaction ID. Not found: 'Transaction ID NOT found...' - check the ID or find it in Transactions. |  | OATM-REQ-F-226, OATM-REQ-F-227 |


## Data models

#### CVTRA05Y

File record of COTRN01C. Source: `app/cpy/CVTRA05Y.cpy`.

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

- COCOM01Y (working storage of COTRN01C): see data-contracts.md.
- COTTL01Y (working storage of COTRN01C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN01C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN01C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-239 | Show initial screen with preselected transaction | formatting | WHILE the caller's data is present and the program is not being re-entered (`CDEMO-PGM-REENTER` not true), WHEN the transaction view is opened, optionally with a transaction pre-selected on a prior screen (`CDEMO-CT01-TRN-SELECTED` not spaces or low-values), THE Transaction View SHALL reset the screen and position the cursor on the transaction ID entry field; when a transaction was pre-selected, pre-fill its ID and perform the transaction lookup; then display the transaction view screen | medium | app/cbl/COTRN01C.cbl:86,88,91-92,94,97-99,101-109, app/cbl/COTRN01C.cbl:94-109 |
| OATM-BR-240 | Require non-empty transaction ID | business rule | IF the entered transaction ID (`TRNIDINI`) is spaces or low-values, THEN THE Transaction Lookup Validation SHALL flag an error, show the message 'Tran ID can NOT be empty...' and redisplay the screen with the cursor on the transaction ID field | medium | app/cbl/COTRN01C.cbl:144,146-154,156, app/cbl/COTRN01C.cbl:144-156 |

### Worked examples

- OATM-BR-239: Opened from = Main menu option 7 'Transaction View'; CDEMO-CT01-TRN-SELECTED = spaces → An empty Transaction View screen is shown with the cursor on the Tran ID field
- OATM-BR-240: Key pressed = Enter; Tran ID (TRNIDINI) = (blank) → The screen is redisplayed with 'Tran ID can NOT be empty...' and the cursor on the Tran ID field; no lookup is done

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-172: The transaction view screen only displays a transaction, but today it reads the record as if for update, which locks it. Is the lock needed, for example to guarantee a consistent read, or should the new system use a plain read with no lock? (Solution architect) On OATM-BR-240, OATM-BR-239.
- SME-173: On the transaction view screen, PF3 and PF5 are accepted as valid keys. What should each one do? (Business analyst) On OATM-BR-240, OATM-BR-239.
- SME-174: What should the transaction view screen do when it is opened without any information from a calling screen? (Business analyst) On OATM-BR-240, OATM-BR-239.
- SME-175: When looking up a transaction fails for a reason other than 'not found', what message should the operator see and what should happen next? (Business analyst) On OATM-BR-240, OATM-BR-239.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).