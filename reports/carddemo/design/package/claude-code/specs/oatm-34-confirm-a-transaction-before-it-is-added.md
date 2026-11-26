# Confirm a transaction before it is added (OATM-C34)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Makes the operator explicitly confirm a valid transaction before it is added. 'Y' or 'y' adds it. 'N', 'n' or blank asks 'Confirm to add this transaction...', and any other value gets 'Invalid value. Valid values are (Y/N)...'. No transaction may ever be added without an explicit 'Y'.

**User story:** As an operator entering a transaction, I want the system to ask me to confirm before adding it and to reject an invalid confirmation, so that no transaction is added without my explicit confirmation.

## Requirements

### Requirement 1: OATM-REQ-F-284 (business rule)

#### Acceptance criteria

1. When every field passes validation and Confirm is 'N', 'n' or left blank, the system shall redisplay the Transaction Add screen with 'Confirm to add this transaction...' and the cursor on Confirm, and add nothing. (rules OATM-BR-301)
2. GIVEN All fields: valid; Confirm: N WHEN every field passes validation and Confirm is 'N', 'n' or left blank THEN 'Confirm to add this transaction...' is shown and nothing is written (OATM-C34-AC-01; OATM-BR-301)
3. GIVEN All fields: valid; Confirm: (blank) WHEN every field passes validation and Confirm is 'N', 'n' or left blank THEN 'Confirm to add this transaction...' is shown and nothing is written (OATM-C34-AC-02; OATM-BR-301)

### Requirement 2: OATM-REQ-F-285 (business rule)

#### Acceptance criteria

1. If every field passes validation and Confirm holds any value other than 'Y', 'N', 'n' or blank, then the system shall redisplay the Transaction Add screen with 'Invalid value. Valid values are (Y/N)...' and the cursor on Confirm, and add nothing. (rules OATM-BR-302)
2. GIVEN All fields: valid; Confirm: X WHEN every field passes validation and Confirm holds any other value THEN 'Invalid value. Valid values are (Y/N)...' is shown and nothing is written (OATM-C34-AC-03; OATM-BR-302)

## Screens and components

### Transactions (S-TRANSACTION-LIST)

Browse transactions in a sortable, paged table or jump to a transaction ID, and open one with Enter or a click instead of typing S beside it. Tab order: search, table, pager, Add transaction.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Add transaction (S-TRANSACTION-ADD)

Record a new transaction against an account or card, every field checked before it is added. One field takes the account or the card number; the resolved account and card show at once. Tab order: account or card, transaction details, merchant, Add transaction.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Add transaction | **primary button** | Runs every check, then a confirmation dialog repeats the transaction (account, card, type, amount, dates, merchant) with Add and Cancel; success shows 'Transaction added successfully. Your Tran ID is <id>.' and clears the form | The dialog offers only Add or Cancel, replacing the typed confirmation and its messages 'Confirm to add this transaction...' and 'Invalid value. Valid values are (Y/N)...'. If the ID already exists: 'Tran ID already exist...'; other failures: 'Unable to Add Transaction...'. |  | OATM-REQ-F-284, OATM-REQ-F-285 |


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
