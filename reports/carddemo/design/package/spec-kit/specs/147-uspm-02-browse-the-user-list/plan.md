# Implementation plan: Browse the user list (USPM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

### Sign in (S-SIGN-IN)

Sign in to CardDemo with User ID and password; on success the user lands on the home page for their role. Also shows the signed-out confirmation.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

One role-aware home page replacing both the Main Menu and the Admin Menu: each allowed function is a link, grouped by subject, instead of a typed option number. Administrators see Administration; regular users see accounts, cards, transactions and payments.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Users (S-USER-LIST)

Find users and act on them: search by User ID, page through a table of users, and edit or delete a user from its row; add a new user from here.

Prototype: `ui-reference/index.html#/S-USER-LIST`. Replaces the legacy screens COUSR0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Users | page | Requires a signed-in administrator session; otherwise opens Sign in. Opens on the first page of users. |  |  | USPM-REQ-F-015, USPM-REQ-F-016, USPM-REQ-F-017, USPM-REQ-F-033 |
| Search by User ID | search | User ID to start the list from; blank lists from the first user |  |  | USPM-REQ-F-019 |
| Users | table | User ID, First name, Last name, User type (Admin or Regular user), 10 rows per page in User ID order, with page number and Previous and Next page controls; Previous is disabled on the first page and Next on the last | On the first page: 'You are already at the top of the page...'; on the last page: 'You are already at the bottom of the page...' |  | USPM-REQ-F-020, USPM-REQ-F-021, USPM-REQ-F-022, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-025, USPM-REQ-F-026, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-030, USPM-REQ-F-031 |
| List messages | message | 'Unable to lookup User...' when the list cannot be read; unassigned keys are ignored | An unsupported action shows 'Invalid key pressed. Please see below...' |  | USPM-REQ-F-018, USPM-REQ-F-027, USPM-REQ-F-032 |

### Update user (S-USER-EDIT)

Change a user's name, password or user type. Opens with the user already loaded when chosen from the list; another user can be looked up by User ID.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Delete user (S-USER-DELETE)

Check a user's name and type and delete them so they can no longer sign in; deletion is confirmed in a dialog (new).

Prototype: `ui-reference/index.html#/S-USER-DELETE`. Replaces the legacy screens COUSR3A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data model

#### CSUSR01Y

File record of COUSR00C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COUSR00C): see data-contracts.md.
- COTTL01Y (working storage of COUSR00C): see data-contracts.md.
- CSDAT01Y (working storage of COUSR00C): see data-contracts.md.
- CSMSG01Y (working storage of COUSR00C): see data-contracts.md.

## Design notes

- USPM-BR-024: Keep the User ID of the first row on the current page as the backward paging cursor. 'Previous page' reads the users whose keys come before this ID, in descending key order.
- USPM-BR-025: Keep the User ID of the tenth row on the current page as the forward paging cursor. 'Next page' reads users with keys after this ID, in ascending order (keyset pagination on User ID).
- USPM-BR-034: Set the 'next page available' flag to true every time the user pages backward, including when the request is refused at the top of the list, so that 'Next page' is always allowed after a 'Previous page' request.
- USPM-BR-037: Keep the list's paging state between requests: page number, first and last User ID shown, and the next-page flag. Store it in the session or as a cursor token passed with each request, so the next action continues from the same position.

## Decision tables

#### User list key handling

| Key pressed | Page number | Next page marked | User list action | Rule |
|---|---|---|---|---|
| Enter | Any | Any | Process the selection or filter | USPM-BR-020 |
| PF3 | Any | Any | Return to the Admin menu (COADM01C) | USPM-BR-020 |
| PF7 | 1 or lower | Any | Show 'You are already at the top of the page...' and redisplay without clearing | USPM-BR-033 |
| PF7 | Greater than 1 | Any | Show up to ten users before the first user on the current page | USPM-BR-032 |
| PF8 | Any | No | Show 'You are already at the bottom of the page...' and redisplay without clearing | USPM-BR-028 |
| PF8 | Any | Yes | Show up to the next ten users after the last user on the current page | USPM-BR-026 |
| Any other key | Any | Any | Redisplay with 'Invalid key pressed. Please see below...', cursor on user ID entry | USPM-BR-021 |

#### Page number after paging

| Paging direction | Rows filled | Further user exists beyond the page | Page number and next-page marking | Rule |
|---|---|---|---|---|
| Forward | All ten | Yes | Add 1 to page number; mark next page 'Y' | USPM-BR-029 |
| Forward | All ten | No | Add 1 to page number; mark next page 'N' | USPM-BR-029 |
| Forward | Fewer than ten (end of file) | No | Mark no next page; add 1 only if at least one user shown; show 'You have reached the bottom of the page...' | USPM-BR-030 |
| Backward | All ten | Yes (and page above 1) | Lower page number by 1 | USPM-BR-035 |
| Backward | All ten | No | Set page number to 1 and show 'You have reached the top of the page...' | USPM-BR-035 |
| Backward | Fewer than ten | - | Page number left unchanged | USPM-BR-035 |
| Backward | Fewer than ten | - | **Gap:** No rule says what message is shown or what rows are displayed when fewer than ten earlier users are found on a backward page. | |

