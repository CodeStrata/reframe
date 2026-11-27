# Implementation plan: Sign on to CardDemo (USPM-C01)

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
| You have signed out | **summary card** | Shown only after Sign out: 'Thank you for using CardDemo application...' |  |  | USPM-REQ-F-012 |
| User ID | **lookup field** | User ID, up to 8 characters, not case-sensitive. Focus starts here on a blank form. | Blank: 'Please enter User ID ...', with focus back on User ID. Not on file: 'User not found. Try again ...' Read failure: 'Unable to verify the User ...' Each message shows under User ID. |  | USPM-REQ-F-001, USPM-REQ-F-003, USPM-REQ-F-005, USPM-REQ-F-006, USPM-REQ-F-007 |
| Password | **lookup field** | Password, masked, up to 8 characters, not case-sensitive, with a Show password toggle. | Blank: 'Please enter Password ...' Wrong password: 'Wrong Password. Try again ...' Each message shows under Password, with focus on it. Failed attempts are logged; the owner decides the attempt limit and lockout (the legacy allows unlimited attempts). |  | USPM-REQ-F-004, USPM-REQ-F-008, USPM-REQ-N-001 |
| Sign in | **primary button** | Checks the User ID and Password and opens Home with the signed-in role: Administrator for type A, User for any other type. Only Enter and the button act; other keys do nothing, so the 'Invalid key pressed. Please see below...' message is no longer needed. | Checks User ID first, then Password, and reports the first problem under its field. | S-HOME | USPM-REQ-F-002, USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011, USPM-REQ-F-013, USPM-REQ-F-014 |

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

### Add user (S-USER-ADD)

Create a user profile so a new person can sign in. The form clears after each add, so several users can be added in a row.

Prototype: `ui-reference/index.html#/S-USER-ADD`. Replaces the legacy screens COUSR1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| User type | **lookup field** | A choice of Admin (A) or User (U), with no default. Only these two values can be saved; the legacy accepted any character, and every type other than A signed in as a regular user. | None chosen: 'User Type can NOT be empty...' |  |  |

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
| Signed in as | **summary card** | Signed-in user ID and role (Administrator or User), set at sign-in. |  |  | USPM-REQ-F-009, USPM-REQ-F-010, USPM-REQ-F-011 |
| Sign out | **primary button** | Ends the session and returns to Sign in, which shows 'Thank you for using CardDemo application...'. |  | S-SIGN-IN | USPM-REQ-F-012 |


## Data model

#### CSUSR01Y

File record of COSGN00C, COUSR01C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COSGN00C, COUSR01C): see data-contracts.md.
- COTTL01Y (working storage of COSGN00C, COUSR01C): see data-contracts.md.
- CSDAT01Y (working storage of COSGN00C, COUSR01C): see data-contracts.md.
- CSMSG01Y (working storage of COSGN00C, COUSR01C): see data-contracts.md.

## Design notes

- USPM-BR-010: After a successful sign-on, create a session that holds the upper-cased user ID, the user type read from the user record, where the user came from (sign-on) and a 'first entry' marker. Every later screen reads this session to know who the user is and what role they have.
- USPM-BR-017: While the sign-on screen is showing (first visit, after an input error or after an invalid key), keep the session alive and wait for the user's next action on that screen. Do not lose session data between round trips.

## Decision tables

#### Sign-on outcome on Enter

| User ID entered | Password entered | User security record read | Stored password equals upper-cased entered password | User type | Sign-on result | Rule |
|---|---|---|---|---|---|---|
| No | Any | Not read | - | - | Redisplay with 'Please enter User ID ...', cursor on User ID | USPM-BR-003 |
| Yes | No | Not read | - | - | Redisplay with 'Please enter Password ...', cursor on Password | USPM-BR-004 |
| Yes | Yes | User not found | - | - | Redisplay with 'User not found. Try again ...', cursor on User ID | USPM-BR-006 |
| Yes | Yes | Read failed for any other reason | - | - | Redisplay with 'Unable to verify the User ...', cursor on User ID | USPM-BR-007 |
| Yes | Yes | Found | No | - | Redisplay with 'Wrong Password. Try again ...', cursor on Password; no lockout | USPM-BR-008 |
| Yes | Yes | Found | Yes | 'A' | Transfer to administrator menu (COADM01C) with session context | USPM-BR-012 |
| Yes | Yes | Found | Yes | Anything other than 'A' | Transfer to regular user main menu (COMEN01C) with session context | USPM-BR-013 |

#### Sign-on screen key handling

| Key pressed | Sign-on screen action | Rule |
|---|---|---|
| Enter | Check User ID and Password and try to sign on | USPM-BR-002 |
| PF3 | Clear terminal, show 'Thank you for using CardDemo application...' and end | USPM-BR-015 |
| Any other key | Redisplay with 'Invalid key pressed. Please see below...' | USPM-BR-016 |

