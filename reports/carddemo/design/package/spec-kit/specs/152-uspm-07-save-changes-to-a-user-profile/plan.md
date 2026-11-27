# Implementation plan: Save changes to a user profile (USPM-C07)

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

### Update user (S-USER-EDIT)

Correct a user's name, password or user type. It opens already filled in from the Users table; you can also type a user ID to look up another user.

Prototype: `ui-reference/index.html#/S-USER-EDIT`. Replaces the legacy screens COUSR2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| First name | **lookup field** | The stored first name, editable, up to 20 characters. | Blank: 'First Name can NOT be empty...' |  | USPM-REQ-F-067 |
| Last name | **lookup field** | The stored last name, editable, up to 20 characters. | Blank: 'Last Name can NOT be empty...' |  | USPM-REQ-F-068 |
| Password | **lookup field** | The stored password is never shown. A masked field, up to 8 characters, with a Show password toggle: type a new password to change it, or leave the field as it is to keep the current one. | Cleared without a new password: 'Password can NOT be empty...' |  | USPM-REQ-F-069 |
| User type | **lookup field** | A choice of Admin (A) or User (U), set to the stored type. | None chosen: 'User Type can NOT be empty...' |  | USPM-REQ-F-070 |
| Save changes | **primary button** | Saves only the changed fields and shows 'User <user ID> has been updated ...'. You stay on the screen, with a link back to Users. Leaving with unsaved changes asks 'Discard your changes to <user ID>?'. This button replaces the legacy prompt 'Press PF5 key to save your updates ...'. | Checks User ID, First name, Last name, Password and User type in that order. Every blank field is listed in an error summary, each linked to its field, and nothing is saved; leaving the screen never hides these messages. Nothing changed: 'Please modify to update ...' User no longer on file: 'User ID NOT found...', and no save is tried. Any other failure: 'Unable to Update User...'. |  | USPM-REQ-F-064, USPM-REQ-F-065, USPM-REQ-F-066, USPM-REQ-F-071, USPM-REQ-F-072, USPM-REQ-F-073, USPM-REQ-F-074, USPM-REQ-F-075 |


## Data model

#### CSUSR01Y

File record of COUSR02C. Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

- COCOM01Y (working storage of COUSR02C): see data-contracts.md.
- COTTL01Y (working storage of COUSR02C): see data-contracts.md.
- CSDAT01Y (working storage of COUSR02C): see data-contracts.md.
- CSMSG01Y (working storage of COUSR02C): see data-contracts.md.

## Design notes

None.

## Decision tables

#### User update save validation

| User ID | First Name | Last Name | Password | User Type | Any of First Name, Last Name, Password, User Type differs from stored user | Save result | Rule |
|---|---|---|---|---|---|---|---|
| Blank | Any | Any | Any | Any | Any | Not saved; 'User ID can NOT be empty...'; cursor on User ID | USPM-BR-074 |
| Filled | Blank | Any | Any | Any | Any | Not saved; 'First Name can NOT be empty...'; cursor on First Name | USPM-BR-075 |
| Filled | Filled | Blank | Any | Any | Any | Not saved; 'Last Name can NOT be empty...'; cursor on Last Name | USPM-BR-076 |
| Filled | Filled | Filled | Blank | Any | Any | Not saved; 'Password can NOT be empty...'; cursor on Password | USPM-BR-077 |
| Filled | Filled | Filled | Filled | Blank | Any | Not saved; 'User Type can NOT be empty...'; cursor on User Type | USPM-BR-078 |
| Filled | Filled | Filled | Filled | Filled | Yes | Changed fields replaced and user record saved; 'User <user ID> has been updated ...' in green | USPM-BR-081 |
| Filled | Filled | Filled | Filled | Filled | No | Nothing saved; 'Please modify to update ...' in red | USPM-BR-082 |
| Filled | Filled | Filled | Filled | Filled | Stored user not found or save fails | **Gap:** No rule says what the screen shows if the re-read of the stored user or the save of the changed record fails. | |

