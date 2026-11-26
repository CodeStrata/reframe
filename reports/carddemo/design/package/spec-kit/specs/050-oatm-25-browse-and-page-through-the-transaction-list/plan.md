# Implementation plan: Browse and page through the transaction list (OATM-C25)

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
| Start from transaction ID | search | Optional; the list starts at this ID or the next higher one; blank starts at the first | Digits only: 'Tran ID must be Numeric ...'; above every ID on file: 'You are at the top of the page...'. |  | OATM-REQ-F-198, OATM-REQ-F-199, OATM-REQ-F-200 |
| Transactions | table | Transaction ID, date (MM/DD/YY), description and signed amount; ten rows a page in ID order, all accounts; page number; Previous and Next page controls; row action View opens the transaction | Previous on the first page: 'You are already at the top of the page...'; Next on the last page: 'You are already at the bottom of the page...'. |  | OATM-REQ-F-212 |
| List error | message | 'Unable to lookup transaction...' when the file cannot be read; focus returns to the search |  |  | OATM-REQ-F-197, OATM-REQ-F-211 |

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

- OATM-BR-206: Every request to the list starts from a clean state: no leftover message, no error, end-of-list or next-page flags carried over, and focus on the transaction ID filter. Page position comes only from the paging state the server keeps (or the request carries), not from previous screen contents.
- OATM-BR-216: Each page response must keep the transaction ID of its first row and of its last row as paging cursors. The first ID is where the next previous-page request starts. Keep them in the user's session or return them as opaque cursors.
- OATM-BR-217: The ID of the tenth row is the cursor for the next-page request. The next page is a keyed range read of transactions with ID strictly greater than this cursor, in ascending ID order, limited to 10 (plus one look-ahead to tell whether more exist).
- OATM-BR-226: The previous page is a keyed range read of transactions with ID strictly less than the current page's first ID, in descending order, limited to 10, then reversed for display. The current first transaction is never repeated. Use an index on transaction ID that supports reading in both directions from a key.

## Decision tables

#### Transaction list paging keys

| Key pressed | Current page number | Next page available | Paging result | Rule |
|---|---|---|---|---|
| PF7 | Greater than 1 | Any | Read from the page's first transaction ID, mark next page available, show previous page | OATM-BR-224 |
| PF7 | 1 or lower | Any | Redisplay current screen with 'You are already at the top of the page...', mark next page available | OATM-BR-225 |
| PF8 | Any | Yes | Restart after the page's last transaction ID and show up to the next 10 transactions | OATM-BR-222 |
| PF8 | Any | No | Redisplay current screen with 'You are already at the bottom of the page...' | OATM-BR-223 |

#### Transaction ID filter on Enter

| Tran ID filter content | Transaction at or above the filter ID on file | List result | Rule |
|---|---|---|---|
| Blank | Any | Show first page from the first transaction on file | OATM-BR-208 |
| Numeric (all 16 digits) | Yes | Start list at that ID or the next higher ID | OATM-BR-209 |
| Numeric (all 16 digits) | No | Show 'You are at the top of the page...' with no rows and page number 0 | OATM-BR-212 |
| Not entirely digits | Any | Show 'Tran ID must be Numeric ...', cursor on filter, keep entry, no new page | OATM-BR-210 |
| Blank | No | **Gap:** No rule states what is shown when the filter is blank and the transaction file holds no transactions. | |

#### Page completion and next-page indicator

| Direction | All 10 rows filled | Further transaction exists | Page number and indicator | Rule |
|---|---|---|---|---|
| Forward | Yes | Yes | Add 1 to page number; next page available Y | OATM-BR-218 |
| Forward | Yes | No | Add 1 to page number; next page available N; show 'You have reached the bottom of the page...' | OATM-BR-218 |
| Forward | No | No | Next page available N; add 1 to page number only if at least one transaction placed | OATM-BR-219 |
| Backward | Yes | Yes | Decrease page number by 1 if above 1, otherwise set to 1 | OATM-BR-228 |
| Backward | Yes | No | Set page number to 1 | OATM-BR-228 |
| Backward | No | No | Show 'You have reached the top of the page...', leave top rows blank, page number unchanged | OATM-BR-229 |
| Backward | No | Any | **Gap:** No rule states the page number or message when backward paging stops early because a read fails rather than reaching the start of the file. | |

