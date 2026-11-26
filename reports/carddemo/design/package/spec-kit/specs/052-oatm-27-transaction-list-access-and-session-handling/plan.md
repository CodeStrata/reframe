# Implementation plan: Transaction list access and session handling (OATM-C27)

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
| Transactions | **data table** | Columns Transaction ID, Date (26 Nov 2026), Description, Amount (right-aligned, two decimals), sortable; 20 rows a page with page number and next/previous; the row opens the transaction | Rows open on Enter or click, so there is no selection code to mistype (legacy: 'Invalid selection. Valid value is S'). At the first or last page the previous or next control is disabled and says 'You are already at the top of the page...' / 'You have reached the bottom of the page...'. Empty state: 'No transactions yet. Use Add transaction to record the first one.' | S-TRANSACTION-VIEW | OATM-REQ-F-225, OATM-REQ-N-008, OATM-REQ-N-009, OATM-REQ-N-010 |

### Transaction (S-TRANSACTION-VIEW)

Show one transaction in full with its merchant, opened from the list or by typing its ID. Tab order: transaction ID, details, merchant, Back to transactions.

Prototype: `ui-reference/index.html#/S-TRANSACTION-VIEW`. Replaces the legacy screens COTRN1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Application header and navigation (S-APP-SHELL)

New, shared by every screen: the header and navigation shown once, replacing the transaction, program, date, time and title lines every 3270 screen repeated and the numbered main-menu options. A sign-in is required; with no session the user is sent to sign-in. The navigation carries the account in context, so going from an account to Pay balance, Update account or Add transaction keeps it. Tab order: account search, navigation, then the page.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| CardDemo | **summary card** | Application name and the current page title as the page heading |  |  | OATM-REQ-N-008 |
| Transactions | **primary button** |  |  | S-TRANSACTION-LIST | OATM-REQ-F-224 |


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

- OATM-BR-238: The list needs server-side session state (or a signed cursor carried with each request) that holds the page position (first/last IDs, page number), the current selection and the signed-on user between requests and across the hand-off to the detail screen. No other transaction routing is needed.

## Decision tables

#### Transaction list key handling

| Key pressed | Screen action | Rule |
|---|---|---|
| Enter | Run search and selection |  |
| PF3 | Return to main menu 'COMEN01C' | OATM-BR-236 |
| PF7 | Show the previous page |  |
| PF8 | Show the next page |  |
| Any other key | Redisplay with 'Invalid key pressed. Please see below...', cursor on transaction ID field | OATM-BR-237 |

