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
| Start from user ID | **lookup field** | The user ID to start the list from; left blank, the list starts at the first user. Enter searches and returns to page 1. | If the users cannot be read, 'Unable to lookup User...' shows above the table with a Try again link. |  | USPM-REQ-F-016, USPM-REQ-F-019 |
| Users | **data table** | Columns User ID, First name, Last name and User type (Admin or User), sorted by User ID. The table shows 20 rows a page, with Previous, Next and 'Page n'. Each row has an Edit action (opens Update user) and a Delete action (opens Delete user). Empty state: 'No users yet. Choose Add user to create the first one.' | Previous is disabled on page 1 and Next on the last page. The disabled buttons say 'You are already at the top of the page...' and 'You are already at the bottom of the page...', and the last page says 'You have reached the bottom of the page...'. The actions are buttons on each row, so the 'Invalid selection. Valid values are U and D' error cannot happen. If the users cannot be read while paging: 'Unable to lookup User...'. | S-USER-EDIT | USPM-REQ-F-017, USPM-REQ-F-018, USPM-REQ-F-020, USPM-REQ-F-023, USPM-REQ-F-024, USPM-REQ-F-026, USPM-REQ-F-027, USPM-REQ-F-028, USPM-REQ-F-029, USPM-REQ-F-032 |

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

### CardDemo header and navigation (S-APP-HEADER)

New, shared by every screen: shows the application and page title, the signed-in user, today's date and the time once, with the way back to the main menu. It replaces the transaction, program, date, time and title lines that every 3270 screen repeated.

Prototype: `ui-reference/index.html#/S-APP-HEADER`.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Navigation | **data table** | The functions the signed-in role may use, as one list of links grouped Account, Card, Transaction, Bill payment and Reports. Administrators also get User administration (Users, Add user) and Transaction types. The current screen is marked. Esc goes back one screen, to the screen that opened this one or to Home. | Every screen checks on the server that a session is signed in. With no session you are sent to Sign in with 'Please sign in to continue.' Administrator-only screens check the role on the server. A regular user who opens one sees 'No access - Admin Only option... ' and stays on Home. | S-HOME | USPM-REQ-F-015 |


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

- USPM-BR-024: Remember the User ID shown in the first row of the current page. Paging backward uses it as a cursor: fetch the up to ten users whose IDs sort before it, in descending key order, then show them in ascending order.
- USPM-BR-025: Remember the User ID shown in the last row (row 10) of the current page. Paging forward uses it as a cursor: fetch the next up to ten users whose IDs sort after it.
- USPM-BR-034: Any backward-page request sets the list's 'next page available' state to yes, even when it is refused at the top, so that a forward page is allowed afterwards. Keep this flag in the paging state.
- USPM-BR-037: Keep the list's paging state (page number, first and last User ID shown, next-page flag) in the user's session or the request between interactions, so that the next action continues from the same page.

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

