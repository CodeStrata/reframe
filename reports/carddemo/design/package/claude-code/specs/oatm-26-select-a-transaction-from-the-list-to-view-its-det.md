# Select a transaction from the list to view its details (OATM-C26)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Lets a signed-on user mark one transaction on the list with 'S' (or 's') and open its details on the Transaction View. Only the first marked row, top to bottom, counts. Any other code is rejected with 'Invalid selection. Valid value is S'. A stale earlier selection must never open a transaction the user did not choose.

**User story:** As a signed-on user, I want to mark a transaction in the list with 'S' and open its details, so that I can look at one transaction closely.

## Requirements

### Requirement 1: OATM-REQ-F-220 (business rule)

#### Acceptance criteria

1. When the user presses Enter on the transaction list, the system shall take the first of the ten rows, top to bottom, whose selection field is not blank, recording that row's selection code and transaction ID (CDEMO-CT00-TRN-SEL-FLG, CDEMO-CT00-TRN-SELECTED) and ignoring any later marked rows. (rules OATM-BR-230)
2. GIVEN Row 3 selection: S; Row 3 transaction ID: 0000000000000042; Rows 1-2 selection: blank WHEN the user presses Enter on the transaction list THEN Row 3 is taken: selection 'S', transaction 0000000000000042 (OATM-C26-AC-01; OATM-BR-230)
3. GIVEN Row 2 selection: S; Row 7 selection: S WHEN the user presses Enter on the transaction list THEN Only row 2 is taken; row 7 is ignored (OATM-C26-AC-02; OATM-BR-230)
4. GIVEN All row selections: blank WHEN the user presses Enter on the transaction list THEN No selection is recorded; the list is refreshed (OATM-C26-AC-03; OATM-BR-230)

### Requirement 2: OATM-REQ-F-221 (business rule)

#### Acceptance criteria

1. When the taken row's selection code is 'S' or 's' and the row has a transaction ID, the system shall pass that transaction ID to the Transaction Detail program (COTRN01C) as a fresh entry (context 0), recording the list screen (CT00, COTRN00C) as the caller. (rules OATM-BR-231)
2. GIVEN Row 3 selection: s; Row 3 transaction ID: 0000000000000042 WHEN the taken row's selection code is 'S' or 's' and the row has a transaction ID THEN Transaction Detail (COTRN01C) opens for transaction 0000000000000042 (OATM-C26-AC-04; OATM-BR-231)

### Requirement 3: OATM-REQ-F-222 (business rule)

#### Acceptance criteria

1. If the taken row's selection code is anything other than 'S' or 's', then the system shall show the message 'Invalid selection. Valid value is S', place the cursor on the transaction ID search field and redisplay the list. (rules OATM-BR-232)
2. GIVEN Row 3 selection: X; Row 3 transaction ID: 0000000000000042 WHEN the taken row's selection code is anything other than 'S' or 's' THEN Message 'Invalid selection. Valid value is S'; the list is shown again (OATM-C26-AC-05; OATM-BR-232)

### Requirement 4: OATM-REQ-F-223 (design note)

#### Acceptance criteria

1. When Enter is processed and none of the 10 list rows has a selection code, the system shall clear any remembered selection code and selected transaction ID, so no transaction is opened and the list is redisplayed. (rules OATM-BR-233)
2. GIVEN selection column on all rows: blank; key: Enter WHEN Enter is processed and none of the 10 list rows has a selection code THEN No transaction is opened; the selection is cleared and the list is shown again. (OATM-C26-AC-06; OATM-BR-233)

## Screens and components

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


## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-230 | Capture selection from first list row | business rule | WHEN the user presses Enter on the transaction list, THE Transaction List SHALL take the first of the ten rows, top to bottom, whose selection field is not blank, recording that row's selection code and transaction ID (CDEMO-CT00-TRN-SEL-FLG, CDEMO-CT00-TRN-SELECTED) and ignoring any later marked rows. | high | app/cbl/COTRN00C.cbl:146-181, app/cbl/COTRN00C.cbl:182-204, app/cbl/COTRN00C.cbl:221-225, app/cbl/COTRN00C.cbl:36-37 |
| OATM-BR-231 | Open details for selected transaction | business rule | WHEN the taken row's selection code is 'S' or 's' and the row has a transaction ID, THE Transaction List SHALL pass that transaction ID to the Transaction Detail program (COTRN01C) as a fresh entry (context 0), recording the list screen (CT00, COTRN00C) as the caller. | high | app/cbl/COTRN00C.cbl:146-181, app/cbl/COTRN00C.cbl:182-204, app/cbl/COTRN00C.cbl:221-225, app/cbl/COTRN00C.cbl:36-37 |
| OATM-BR-232 | Reject invalid selection code | business rule | WHEN the taken row's selection code is anything other than 'S' or 's', THE Transaction List SHALL show the message 'Invalid selection. Valid value is S', place the cursor on the transaction ID search field and redisplay the list. | high | app/cbl/COTRN00C.cbl:146-181, app/cbl/COTRN00C.cbl:182-204, app/cbl/COTRN00C.cbl:221-225, app/cbl/COTRN00C.cbl:36-37 |
| OATM-BR-233 | Clear selection when no row chosen | design note | WHEN Enter is processed and none of the 10 list rows has a selection code, THE transaction list SHALL clear any remembered selection code and selected transaction ID, so no transaction is opened and the list is redisplayed. | medium | app/cbl/COTRN00C.cbl:146-183, app/cbl/COTRN00C.cbl:184-186 |

### Worked examples

- OATM-BR-230: Row 3 selection = S; Row 3 transaction ID = 0000000000000042; Rows 1-2 selection = blank → Row 3 is taken: selection 'S', transaction 0000000000000042
- OATM-BR-230: Row 2 selection = S; Row 7 selection = S → Only row 2 is taken; row 7 is ignored
- OATM-BR-230: All row selections = blank → No selection is recorded; the list is refreshed
- OATM-BR-231: Row 3 selection = s; Row 3 transaction ID = 0000000000000042 → Transaction Detail (COTRN01C) opens for transaction 0000000000000042
- OATM-BR-232: Row 3 selection = X; Row 3 transaction ID = 0000000000000042 → Message 'Invalid selection. Valid value is S'; the list is shown again
- OATM-BR-233: selection column on all rows = blank; key = Enter → No transaction is opened; the selection is cleared and the list is shown again.

## Decision tables

#### Row selection on Enter

| A row has a selection code | Selection code of first marked row | Row has a transaction ID | Selection result | Rule |
|---|---|---|---|---|
| No | - | - | Clear remembered selection; open nothing; redisplay list | OATM-BR-233 |
| Yes | 'S' or 's' | Yes | Open Transaction Detail (COTRN01C) for that ID as a fresh entry | OATM-BR-231 |
| Yes | Any other value | Any | Show 'Invalid selection. Valid value is S', cursor on search field, redisplay list | OATM-BR-232 |
| Yes | 'S' or 's' | No | **Gap:** No rule states what happens when 'S' is entered on a row with no transaction ID. | |


## Design notes

- OATM-BR-233: When a list submission has no row selected, the server must clear any selection code and selected transaction ID held in the session. That way a later step cannot open a transaction from an earlier interaction. The selection lives only for the request that made it.

## Open questions

- SME-164: When the operator pages back through the transaction list, the page number is reset to 1 "otherwise". Which situation triggers that reset: when the look-back read failed or the page number is already 1 or less, when no next page is flagged as available, or both? (Business analyst) On OATM-BR-233, OATM-BR-230, OATM-BR-231, OATM-BR-232.
- SME-165: The transaction list only describes how transactions are placed in rows 1 and 10. How should transactions be placed in rows 2 through 9? (Business analyst) On OATM-BR-233, OATM-BR-230, OATM-BR-231, OATM-BR-232.
- SME-166: On the transaction list, how is the next screen chosen when the operator selects a transaction, what should PF3 do, and what should happen when the list is opened without any information from a calling screen? (Application owner) On OATM-BR-233, OATM-BR-230, OATM-BR-231, OATM-BR-232.
- SME-167: When the operator presses PF8 (next page) and no last transaction ID is held, the list currently starts after the highest possible key, which probably shows an empty page. Should the new system keep this behaviour? (Business analyst) On OATM-BR-233, OATM-BR-230, OATM-BR-231, OATM-BR-232.
- DEF-049: Is this intended? When a selection code is typed on a row with no transaction ID, the selection is silently ignored with no message; and when several rows are marked only the first is acted on, also without a message. (Subject-matter expert) On OATM-BR-230, OATM-BR-231, OATM-BR-232.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).
