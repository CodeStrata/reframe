# Implementation plan: Identify the account and card for a new transaction (OATM-C31)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

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
| Account or card number | **lookup field** | 11-digit account number or 16-digit card number, pre-filled from the account in context; the resolved account and card number show beneath it | Blank: 'Account or Card Number must be entered...'. Not digits: 'Account ID must be Numeric...' / 'Card Number must be Numeric...'. Not in the card cross-reference: 'Account ID NOT found...' / 'Card Number NOT found...' - check the number with the caller. |  | OATM-REQ-F-245, OATM-REQ-F-246, OATM-REQ-F-247, OATM-REQ-F-248, OATM-REQ-F-249, OATM-REQ-F-250, OATM-REQ-F-251, OATM-REQ-F-252, OATM-REQ-N-013, OATM-REQ-N-014 |


## Data model

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

## Design notes

None.

## Decision tables

#### Account and card resolution

| Account ID | Card number | Cross-reference lookup result | Result | Rule |
|---|---|---|---|---|
| blank | blank | not looked up | Message 'Account or Card Number must be entered...', cursor on account ID, save nothing | OATM-BR-260 |
| entered, not all digits | any | not looked up | Message 'Account ID must be Numeric...', cursor on account ID, save nothing | OATM-BR-261 |
| numeric | any | account found (CXACAIX) | Card number filled with linked card, replacing any typed card number | OATM-BR-262 |
| numeric | any | account not found | Message 'Account ID NOT found...', cursor on account ID, save nothing | OATM-BR-263 |
| numeric | any | other lookup failure | Log response codes; message 'Unable to lookup Acct in XREF AIX file...', save nothing | OATM-BR-264 |
| blank | entered, not all digits | not looked up | Message 'Card Number must be Numeric...', cursor on card number, save nothing | OATM-BR-265 |
| blank | numeric | card found (CCXREF) | Account ID filled with account linked to the card | OATM-BR-266 |
| blank | numeric | card not found | Message 'Card Number NOT found...', cursor on card number, save nothing | OATM-BR-267 |
| blank | numeric | other lookup failure | Log response codes; message 'Unable to lookup Card # in XREF file...', save nothing | OATM-BR-268 |

