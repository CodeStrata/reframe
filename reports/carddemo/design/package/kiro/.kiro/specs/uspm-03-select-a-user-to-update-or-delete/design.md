# Design: Select a user to update or delete (USPM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Lets an administrator mark one user on the list with 'U' to open the update screen or 'D' to open the delete screen for that user. Only the first marked row counts, and any other code is rejected with a message. It must never open an update or delete screen for a user the administrator did not mark, or for a code other than U/D.

Runs as online. Journeys: J15, J17.

## Screens and components

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


## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| USPM-BR-038 | Capture selection from first list row | business rule | WHEN the operator presses Enter on the user list and one or more of the 10 rows has a selection code entered, THE User List SHALL take only the first marked row from the top, saving its selection code and user ID as the pending selection (CDEMO-CU00-USR-SEL-FLG, CDEMO-CU00-USR-SELECTED), and ignore marks on later rows. | high | app/cbl/COUSR00C.cbl:36-37, app/cbl/COUSR00C.cbl:147-185, app/cbl/COUSR00C.cbl:187-210 |
| USPM-BR-039 | Clear selection when no row marked | design note | WHEN the user list is submitted with no selection code in any of the ten rows, THE user list SHALL clear any pending selected action and user (CDEMO-CU00-USR-SEL-FLG, CDEMO-CU00-USR-SELECTED) so that no update or delete screen is opened, and SHALL just refresh the list. | medium | app/cbl/COUSR00C.cbl:152-185, app/cbl/COUSR00C.cbl:187-189, app/cbl/COUSR00C.cbl:218-229 |
| USPM-BR-040 | Row selection action routes to update or delete user | design note | WHEN the operator presses Enter and no row has a selection code entered, THE User List SHALL clear the pending selection code and selected user ID to blanks. | high | app/cbl/COUSR00C.cbl:36-37, app/cbl/COUSR00C.cbl:147-185, app/cbl/COUSR00C.cbl:187-210 |
| USPM-BR-041 | Transfer selected user for update or delete | business rule | WHEN the pending selection code is 'U' or 'u' and a user ID was selected, THE User List SHALL transfer to the Update User program (COUSR02C), passing the selected user ID with from-transaction 'CU00', from-program 'COUSR00C' and context 0. | high | app/cbl/COUSR00C.cbl:36-37, app/cbl/COUSR00C.cbl:147-185, app/cbl/COUSR00C.cbl:187-210 |
| USPM-BR-042 | Transfer selected user for update or delete | business rule | WHEN the pending selection code is 'D' or 'd' and a user ID was selected, THE User List SHALL transfer to the Delete User program (COUSR03C), passing the selected user ID with from-transaction 'CU00', from-program 'COUSR00C' and context 0. | high | app/cbl/COUSR00C.cbl:36-37, app/cbl/COUSR00C.cbl:147-185, app/cbl/COUSR00C.cbl:187-210 |
| USPM-BR-043 | Reject invalid selection action | business rule | WHEN a row with a user ID is selected with an action code other than 'U', 'u', 'D' or 'd', THE user list SHALL not open any user screen, SHALL show the message 'Invalid selection. Valid values are U and D', and SHALL place the cursor on the user ID search field. | medium | app/cbl/COUSR00C.cbl:188-216, app/cbl/COUSR00C.cbl:526 |

### Worked examples

- USPM-BR-038: Row 3 selection = 'd'; Row 3 user ID = USER0003 → The pending selection is 'd' for user USER0003
- USPM-BR-038: Row 2 selection = 'U'; Row 2 user ID = USER0002; Row 7 selection = 'D'; Row 7 user ID = USER0007 → Only row 2 is used: the pending selection is 'U' for USER0002 and the row 7 mark is ignored
- USPM-BR-039: Selection in rows 1-10 = all blank → No user screen is opened; the list is shown again from the search user ID
- USPM-BR-040: Rows 1-10 selection = blank → The pending selection and selected user are cleared to blanks, and no transfer takes place
- USPM-BR-041: Selection code = 'u'; Selected user ID = USER0005 → The Update User screen (COUSR02C) opens for USER0005, with the list recorded as 'CU00'/'COUSR00C' to return to
- USPM-BR-042: Selection code = 'd'; Selected user ID = USER0003 → The Delete User screen (COUSR03C) opens for USER0003, with the list recorded as 'CU00'/'COUSR00C' to return to
- USPM-BR-043: Row 3 selection = X; Row 3 user ID = USER0003 → Message 'Invalid selection. Valid values are U and D' is shown and the list is redisplayed
- USPM-BR-043: Row 1 selection = u; Row 1 user ID = USER0001 → The update user screen (COUSR02C) is opened for USER0001

## Decision tables

#### Action on the first marked row

| Selection code on first marked row | User ID on that row | Screen opened | Rule |
|---|---|---|---|
| 'U' or 'u' | Present | Transfer to Update User (COUSR02C) with the selected user ID | USPM-BR-041 |
| 'D' or 'd' | Present | Transfer to Delete User (COUSR03C) with the selected user ID | USPM-BR-042 |
| Any other code | Present | No screen opened; show 'Invalid selection. Valid values are U and D', cursor on user ID search field | USPM-BR-043 |
| None on any row | - | Clear pending selection and refresh the list | USPM-BR-039 |
| Any code | Absent | **Gap:** No rule says what happens when a selection code is entered on a row that shows no user ID. | |


## Design notes

- USPM-BR-039: When the list is submitted with no row marked, clear any pending action and selected User ID held in the session, so that no stale selection opens an update or delete screen. Then just refresh the list.
- USPM-BR-040: The pending selection (action code and User ID) must be reset to empty on every submit that has no marked row. It must not be carried over from an earlier interaction.

## Open questions

- SME-209: On the user list, selecting 'U' (update) or 'D' (delete) against a row currently goes to the same place. Which function should handle update requests, and which should handle delete requests? (Business analyst (user security)) On USPM-BR-043, USPM-BR-039, USPM-BR-038, USPM-BR-042.
- SME-210: After paging back through the user list, what page number should be shown? Should it reset to 1 when there is no next page, or only when it cannot go back any further? (Business analyst (user security)) On USPM-BR-043, USPM-BR-039, USPM-BR-038, USPM-BR-042.
- SME-211: What should happen when the operator presses PF3 on the user list? (Business analyst (user security)) On USPM-BR-043, USPM-BR-039, USPM-BR-038, USPM-BR-042.
- SME-212: What should happen when the user list is opened directly, without coming from another screen? (Business analyst (user security)) On USPM-BR-043, USPM-BR-039, USPM-BR-038, USPM-BR-042.
- SME-215: Should the rule that a row selection on the user list routes to update or delete user be treated as top priority (P0)? (Product owner) On USPM-BR-042.
- DEF-155: Is this intended? A selection code typed on an empty row (no user ID) is silently ignored, with no message. (Subject-matter expert) On USPM-BR-043.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).