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
| Search by User ID | search | User ID to start the list from; blank lists from the first user |  |  | USPM-REQ-F-035 |
| Edit | button | Row action that opens the user for update | Only Edit and Delete are offered, so 'Invalid selection. Valid values are U and D' cannot arise | S-USER-EDIT | USPM-REQ-F-034, USPM-REQ-F-036, USPM-REQ-F-038 |
| Delete | button | Row action that opens the user for deletion |  | S-USER-DELETE | USPM-REQ-F-037 |

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

- USPM-BR-039: When the list is submitted with no row marked, clear any pending selected action and user held in the session and simply reload the list, so that a stale selection can never open the update or delete screen.
- USPM-BR-040: Reset the pending selection (action code and selected User ID) to empty on every submit that has no marked row, before the routing decision is made.

## Decision tables

#### Action on the first marked row

| Selection code on first marked row | User ID on that row | Screen opened | Rule |
|---|---|---|---|
| 'U' or 'u' | Present | Transfer to Update User (COUSR02C) with the selected user ID | USPM-BR-041 |
| 'D' or 'd' | Present | Transfer to Delete User (COUSR03C) with the selected user ID | USPM-BR-042 |
| Any other code | Present | No screen opened; show 'Invalid selection. Valid values are U and D', cursor on user ID search field | USPM-BR-043 |
| None on any row | - | Clear pending selection and refresh the list | USPM-BR-039 |
| Any code | Absent | **Gap:** No rule says what happens when a selection code is entered on a row that shows no user ID. | |

