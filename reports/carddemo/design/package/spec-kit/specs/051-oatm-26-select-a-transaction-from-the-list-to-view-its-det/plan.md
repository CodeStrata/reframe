# Implementation plan: Select a transaction from the list to view its details (OATM-C26)

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

Browse transactions page by page from a chosen ID and open any one with a row action instead of typing S against it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transactions | table | Transaction ID, date (MM/DD/YY), description and signed amount; ten rows a page in ID order, all accounts; page number; Previous and Next page controls; row action View opens the transaction | Previous on the first page: 'You are already at the top of the page...'; Next on the last page: 'You are already at the bottom of the page...'. |  | OATM-REQ-F-220 |

### Transaction (S-TRANSACTION-VIEW)

Show one transaction's card, type, category, source, amount, dates and merchant together, opened from the list or looked up by ID.

Prototype: `ui-reference/index.html#/S-TRANSACTION-VIEW`. Replaces the legacy screens COTRN1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data model

#### CVTRA05Y

File record of COTRN00C. Source: `app/cpy/CVTRA05Y.cpy`.

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

- COCOM01Y (working storage of COTRN00C): see data-contracts.md.
- COTTL01Y (working storage of COTRN00C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN00C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN00C): see data-contracts.md.

## Design notes

- OATM-BR-233: When a list submission has no row selected, the server must clear any selection code and selected transaction ID held in the session. That way a later step cannot open a transaction from an earlier interaction. The selection lives only for the request that made it.

## Decision tables

#### Row selection on Enter

| A row has a selection code | Selection code of first marked row | Row has a transaction ID | Selection result | Rule |
|---|---|---|---|---|
| No | - | - | Clear remembered selection; open nothing; redisplay list | OATM-BR-233 |
| Yes | 'S' or 's' | Yes | Open Transaction Detail (COTRN01C) for that ID as a fresh entry | OATM-BR-231 |
| Yes | Any other value | Any | Show 'Invalid selection. Valid value is S', cursor on search field, redisplay list | OATM-BR-232 |
| Yes | 'S' or 's' | No | **Gap:** No rule states what happens when 'S' is entered on a row with no transaction ID. | |

