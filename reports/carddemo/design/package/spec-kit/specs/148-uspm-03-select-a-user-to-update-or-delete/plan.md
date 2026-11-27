# Implementation plan: Select a user to update or delete (USPM-C03)

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

Sign in to CardDemo with a user ID and password. Administrators and regular users both land on Home, which shows the functions their role allows.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Home (S-HOME)

Landing page after sign-in. It lists every function the signed-in role may use as links, and replaces the numbered Main Menu, the Admin Menu and the typed option number.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Users (S-USER-LIST)

Find a user and act on them. A searchable, paged table of all users has Edit and Delete actions on each row, plus Add user. It replaces the typed U and D selection codes and the F7 and F8 paging keys.

Prototype: `ui-reference/index.html#/S-USER-LIST`. Replaces the legacy screens COUSR0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Users | **data table** | Columns User ID, First name, Last name and User type (Admin or User), sorted by User ID. The table shows 20 rows a page, with Previous, Next and 'Page n'. Each row has an Edit action (opens Update user) and a Delete action (opens Delete user). Empty state: 'No users yet. Choose Add user to create the first one.' | Previous is disabled on page 1 and Next on the last page. The disabled buttons say 'You are already at the top of the page...' and 'You are already at the bottom of the page...', and the last page says 'You have reached the bottom of the page...'. The actions are buttons on each row, so the 'Invalid selection. Valid values are U and D' error cannot happen. If the users cannot be read while paging: 'Unable to lookup User...'. | S-USER-EDIT | USPM-REQ-F-034, USPM-REQ-F-036, USPM-REQ-F-037, USPM-REQ-F-038 |

### Update user (S-USER-EDIT)

Correct a user's name, password or user type. It opens already filled in from the Users table; you can also type a user ID to look up another user.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Delete user (S-USER-DELETE)

Remove a user who should no longer have access. The screen shows who will be deleted and asks for confirmation; the confirmation is new, because the legacy deleted on PF5 without asking.

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

- USPM-BR-039: When the list is submitted with no row marked, clear any pending action and selected User ID held in the session, so that no stale selection opens an update or delete screen. Then just refresh the list.
- USPM-BR-040: The pending selection (action code and User ID) must be reset to empty on every submit that has no marked row. It must not be carried over from an earlier interaction.

## Decision tables

#### Action on the first marked row

| Selection code on first marked row | User ID on that row | Screen opened | Rule |
|---|---|---|---|
| 'U' or 'u' | Present | Transfer to Update User (COUSR02C) with the selected user ID | USPM-BR-041 |
| 'D' or 'd' | Present | Transfer to Delete User (COUSR03C) with the selected user ID | USPM-BR-042 |
| Any other code | Present | No screen opened; show 'Invalid selection. Valid values are U and D', cursor on user ID search field | USPM-BR-043 |
| None on any row | - | Clear pending selection and refresh the list | USPM-BR-039 |
| Any code | Absent | **Gap:** No rule says what happens when a selection code is entered on a row that shows no user ID. | |

