# Transaction list access and session handling (OATM-C27)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Governs access to the transaction list. Only signed-on users reach it: anyone without a session goes to sign-on. PF3 returns to the main menu, and unsupported keys get 'Invalid key pressed. Please see below...'. Any signed-on user, regular or admin, sees transactions from every account and card. That is current behaviour and the team must confirm it deliberately rather than change it by accident.

**User story:** As the business, I want the transaction list reachable only within a signed-on session, with clear key handling and return to the main menu, so that users move safely through the screens.

## Requirements

### Requirement 1: OATM-REQ-N-008 (business rule)

#### Acceptance criteria

1. When the transaction list program (COTRN00C) is started without any session data (no commarea), the system shall transfer the user to the sign-on program 'COSGN00C'. (rules OATM-BR-234)
2. GIVEN session data length: 0 WHEN the transaction list program (COTRN00C) is started without any session data (no commarea) THEN The user is transferred to sign-on (COSGN00C); no list is shown. (OATM-C27-AC-01; OATM-BR-234)

### Requirement 2: OATM-REQ-N-009 (business rule)

#### Acceptance criteria

1. The system shall show transactions from every account and card in transaction-ID order to any signed-on user, regular or admin, without limiting them to the user's own account or checking user type. (rules OATM-BR-235)
2. GIVEN user type: U (regular); user's account: 00000000001 WHEN transaction list runs THEN The list also includes transactions belonging to other accounts and cards. (OATM-C27-AC-02; OATM-BR-235)

### Requirement 3: OATM-REQ-F-224 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the transaction list, the system shall return the user to the main menu program 'COMEN01C'. (rules OATM-BR-236)
2. GIVEN key: PF3 WHEN the user presses PF3 on the transaction list THEN The main menu is displayed. (OATM-C27-AC-03; OATM-BR-236)

### Requirement 4: OATM-REQ-F-225 (business rule)

#### Acceptance criteria

1. If the user presses any key other than Enter, PF3, PF7 or PF8 on the transaction list, then the system shall redisplay the screen with the message 'Invalid key pressed. Please see below...' and the cursor on the transaction ID field. (rules OATM-BR-237)
2. GIVEN key: PF5 WHEN the user presses any key other than Enter, PF3, PF7 or PF8 THEN Screen redisplayed with 'Invalid key pressed. Please see below...'. (OATM-C27-AC-04; OATM-BR-237)

### Requirement 5: OATM-REQ-N-010 (design note)

#### Acceptance criteria

1. The system shall end every transaction list interaction by waiting for the next user input under transaction 'CT00', keeping the session data (page position, selection, user) for the next screen. (rules OATM-BR-238)
2. GIVEN key: PF8 WHEN transaction list runs THEN After page 2 is shown, the next key press returns to the transaction list with page 2 remembered. (OATM-C27-AC-05; OATM-BR-238)

## Screens and components

### Transactions (S-TRANSACTION-LIST)

Browse transactions page by page from a chosen ID and open any one with a row action instead of typing S against it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transactions | table | Transaction ID, date (MM/DD/YY), description and signed amount; ten rows a page in ID order, all accounts; page number; Previous and Next page controls; row action View opens the transaction | Previous on the first page: 'You are already at the top of the page...'; Next on the last page: 'You are already at the bottom of the page...'. |  | OATM-REQ-N-009 |
| List error | message | 'Unable to lookup transaction...' when the file cannot be read; focus returns to the search |  |  | OATM-REQ-F-225 |
| Back | link |  |  | S-APP-SHELL | OATM-REQ-F-224, OATM-REQ-N-008 |

### Transaction (S-TRANSACTION-VIEW)

Show one transaction's card, type, category, source, amount, dates and merchant together, opened from the list or looked up by ID.

Prototype: `ui-reference/index.html#/S-TRANSACTION-VIEW`. Replaces the legacy screens COTRN1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Application header and navigation (S-APP-SHELL)

New: the header and navigation shown once around every screen, replacing the transaction, program, date, time and title lines each 3270 map repeated and the typed option codes of the main menu. Sign-on is required before any screen opens.

Prototype: `ui-reference/index.html#/S-APP-SHELL`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| CardDemo | header | Application name and titles (legacy TITLE01/TITLE02), the signed-on user, and today's date and time (legacy CURDATE/CURTIME); a user with no session is sent to sign-on |  |  | OATM-REQ-N-008 |


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
| OATM-BR-234 | Transaction list screen navigation and session routing | business rule | WHEN the transaction list program (COTRN00C) is started without any session data (no commarea), THE transaction list SHALL transfer the user to the sign-on program 'COSGN00C'. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-235 | Transaction list visible to any signed-on user (no account scoping) | business rule | THE transaction list SHALL show transactions from every account and card in transaction-ID order to any signed-on user, regular or admin, without limiting them to the user's own account or checking user type. | medium | app/cbl/COTRN00C.cbl:591-600, app/cbl/COTRN00C.cbl:279-325, app/cpy/COMEN02Y.cpy:55-58, app/cbl/COMEN01C.cbl:136-141 |
| OATM-BR-236 | Transaction list screen navigation and session routing | business rule | WHEN the user presses PF3 on the transaction list, THE transaction list SHALL return the user to the main menu program 'COMEN01C'. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-237 | Reject unsupported key | business rule | WHEN the user presses any key other than Enter, PF3, PF7 or PF8, THE transaction list SHALL redisplay the screen with the message 'Invalid key pressed. Please see below...' and the cursor on the transaction ID field. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |
| OATM-BR-238 | Transaction list screen navigation and session routing | design note | THE transaction list SHALL end every interaction by waiting for the next user input under transaction 'CT00', keeping the session data (page position, selection, user) for the next screen. | high | app/cbl/COTRN00C.cbl:95-141, app/cbl/COTRN00C.cbl:510-522, app/cpy/CSMSG01Y.cpy:20-21, app/cpy/COCOM01Y.cpy:29-31 |

### Worked examples

- OATM-BR-234: session data length = 0 → The user is transferred to sign-on (COSGN00C); no list is shown.
- OATM-BR-235: user type = U (regular); user's account = 00000000001 → The list also includes transactions belonging to other accounts and cards.
- OATM-BR-236: key = PF3 → The main menu is displayed.
- OATM-BR-237: key = PF5 → Screen redisplayed with 'Invalid key pressed. Please see below...'.
- OATM-BR-238: key = PF8 → After page 2 is shown, the next key press returns to the transaction list with page 2 remembered.

## Decision tables

#### Transaction list key handling

| Key pressed | Screen action | Rule |
|---|---|---|
| Enter | Run search and selection |  |
| PF3 | Return to main menu 'COMEN01C' | OATM-BR-236 |
| PF7 | Show the previous page |  |
| PF8 | Show the next page |  |
| Any other key | Redisplay with 'Invalid key pressed. Please see below...', cursor on transaction ID field | OATM-BR-237 |


## Design notes

- OATM-BR-238: The list is a stateful interaction. Between requests the application must keep the user's session state: signed-on user, current page number, first and last transaction IDs of the page, next-page flag and any selection. This can be a server-side session keyed by an authenticated session token, or signed state round-tripped with the client. Each response then waits for the user's next action.

## Open questions

- SME-164: When the operator pages back through the transaction list, the page number is reset to 1 "otherwise". Which situation triggers that reset: when the look-back read failed or the page number is already 1 or less, when no next page is flagged as available, or both? (Business analyst) On OATM-BR-237.
- SME-165: The transaction list only describes how transactions are placed in rows 1 and 10. How should transactions be placed in rows 2 through 9? (Business analyst) On OATM-BR-237.
- SME-166: On the transaction list, how is the next screen chosen when the operator selects a transaction, what should PF3 do, and what should happen when the list is opened without any information from a calling screen? (Application owner) On OATM-BR-237.
- SME-167: When the operator presses PF8 (next page) and no last transaction ID is held, the list currently starts after the highest possible key, which probably shows an empty page. Should the new system keep this behaviour? (Business analyst) On OATM-BR-237.
- SME-168: Should any signed-on user, including regular users, be able to list and open every transaction in the system, or should each user see only the transactions for their own account or cards? (Security/compliance officer) On OATM-BR-235.
- DEF-177: Confirm this is deliberate: Any regular user can see all customers' transactions (card-holder data) because the list is not scoped to the user's account. (Subject-matter expert) On OATM-BR-235.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
