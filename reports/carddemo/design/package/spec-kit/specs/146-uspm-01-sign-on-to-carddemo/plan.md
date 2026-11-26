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

Sign in to CardDemo with User ID and password; on success the user lands on the home page for their role. Also shows the signed-out confirmation.

Prototype: `ui-reference/index.html#/S-SIGN-IN`. Replaces the legacy screens COSGN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Sign in to CardDemo | page | Blank form with focus on User ID |  |  | USPM-REQ-F-001, USPM-REQ-F-014 |
| Sign in | form | User ID and password, submitted together; User ID and password are compared without regard to case |  |  | USPM-REQ-F-002, USPM-REQ-F-005, USPM-REQ-F-009 |
| User ID | text | User ID, up to 8 characters; focused when the page opens | Required: 'Please enter User ID ...'. Unknown ID: 'User not found. Try again ...'. Lookup failure: 'Unable to verify the User ...'. Focus returns to User ID. |  | USPM-REQ-F-003, USPM-REQ-F-006, USPM-REQ-F-007 |
| Password | password | Password, up to 8 characters, hidden as typed, with a Show password toggle | Required: 'Please enter Password ...'. Mismatch: 'Wrong Password. Try again ...' and focus returns to Password. |  | USPM-REQ-F-004, USPM-REQ-F-008, USPM-REQ-N-001 |
| Sign in | button | Opens the home page for the user type: administration for type A, account functions for any other type |  | S-HOME | USPM-REQ-F-010, USPM-REQ-F-011 |
| Sign-in problem | message | Error summary linked to the field to fix, announced to screen readers; unassigned keys are ignored | An unsupported action shows 'Invalid key pressed. Please see below...' |  | USPM-REQ-F-013 |
| Signed out | message | After sign-out: 'Thank you for using CardDemo application...' |  |  | USPM-REQ-F-012 |

### Home (S-HOME)

One role-aware home page replacing both the Main Menu and the Admin Menu: each allowed function is a link, grouped by subject, instead of a typed option number. Administrators see Administration; regular users see accounts, cards, transactions and payments.

Prototype: `ui-reference/index.html#/S-HOME`. Replaces the legacy screens COMEN1A, COADM1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


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

- USPM-BR-010: After a successful sign-on, create a server-side session that holds the upper-cased user ID, the user type read from the user security record, the origin (sign-on, transaction 'CC00' / program 'COSGN00C') and a first-entry flag (context 0). Every later screen reads this session to identify the user and decide what they may do.
- USPM-BR-017: Whenever the sign-on page is shown again (first visit, an input error or an unsupported action), keep the user on the sign-on step and carry any existing session data forward to the next request. No separate state is needed beyond the normal web request/response cycle.

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

