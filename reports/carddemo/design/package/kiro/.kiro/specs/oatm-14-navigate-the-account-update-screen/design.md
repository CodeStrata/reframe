# Design: Navigate the account update screen (OATM-C14)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Controls how the account update screen moves between its steps: a blank search on first arrival, checking entries on each submit, and a fresh start after a save has completed or failed. It is for operators maintaining accounts. It must never act on PF5 unless validated changes are waiting for confirmation, and never on PF12 unless account details have been fetched.

Runs as online. Journeys: J02.

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Account number | search | 11-digit account number; the only editable field until an account is fetched | Required: 'No input received' when blank; 'Account Number if supplied must be a 11 digit Non-Zero Number' when not numeric or all zeros; 'Account:<number> not found in Cross ref file' when the account has no card cross-reference. |  |  |
| Account and customer details | form | All account and customer fields, fetched values pre-filled; editable only while details are shown or have errors | If nothing differs from the fetched values (ignoring case): 'No change detected with respect to values fetched.' and nothing is checked or saved. |  |  |
| Discard changes | button | Re-fetches the stored values; available once an account is fetched |  |  | OATM-REQ-F-117 |
| Save these changes? | dialog | Each changed field with its old and new value; all fields are locked while it is open |  |  | OATM-REQ-F-117 |
| Save result | message | Success: 'Changes committed to database'; failure: 'Changes unsuccessful. Please try again' or 'Update of record failed'; the next submit starts a new search |  |  |  |
| Back | link |  |  | S-APP-SHELL | OATM-REQ-F-116 |


## Data models

#### CSMSG02Y

File record of COACTUPC. Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CVACT01Y

File record of COACTUPC. Source: `app/cpy/CVACT01Y.cpy`.

Record `ACCOUNT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| ACCT-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| ACCT-CURR-BAL |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CASH-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-OPEN-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-REISSUE-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-CURR-CYC-CREDIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CURR-CYC-DEBIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| ACCT-GROUP-ID |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(178) | text, 178 characters |  |  |  |

#### CVACT03Y

File record of COACTUPC. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCUS01Y

File record of COACTUPC. Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

- COCOM01Y (working storage of COACTUPC): see data-contracts.md.
- COTTL01Y (working storage of COACTUPC): see data-contracts.md.
- CSDAT01Y (working storage of COACTUPC): see data-contracts.md.
- CSLKPCDY (working storage of COACTUPC): see data-contracts.md.
- CSMSG01Y (working storage of COACTUPC): see data-contracts.md.
- CSSETATY (working storage of COACTUPC): see data-contracts.md.
- CSSTRPFY (working storage of COACTUPC): see data-contracts.md.
- CSUSR01Y (working storage of COACTUPC): see data-contracts.md.
- CSUTLDPY (working storage of COACTUPC): see data-contracts.md.
- CSUTLDWY (working storage of COACTUPC): see data-contracts.md.
- CVCRD01Y (working storage of COACTUPC): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-117 | Show blank search screen on first entry | formatting | WHEN the operator arrives with no saved context, or comes from the main menu ('COMEN01C') for the first time, THE account update screen SHALL clear any previous update data and show an empty screen asking 'Enter or update id of account to update'. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-118 | Restart after completed or failed save | business rule | WHEN the operator submits the screen with any key other than PF3 after a committed ('C') or failed ('L', 'F') save, THE account update screen SHALL clear the update data and account number and show an empty screen asking for a new account number. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-119 | Route other requests to input processing | business rule | WHEN the operator submits the screen with any key other than PF3, and it is not a first arrival and not the interaction after a committed or failed save, THE account update screen SHALL read and check the entries, decide the next step from the update state, and show the screen again. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-120 | Account update screen lifecycle (change-action state machine) | business rule | THE account update screen SHALL accept PF5 only while validated changes await confirmation ('N') and PF12 only once account details have been fetched, and SHALL treat any other key, or PF5/PF12 outside those states, as Enter. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

### Worked examples

- OATM-BR-117: previous program = COMEN01C; first arrival = yes → Empty account update screen with 'Enter or update id of account to update'
- OATM-BR-118: update state = 'C'; key = Enter → Screen cleared; prompt 'Enter or update id of account to update'
- OATM-BR-118: update state = 'F'; key = Enter → Screen cleared; a new account number must be entered
- OATM-BR-119: key = Enter; update state = 'S' (details shown) → Entries are checked and the screen is shown again with the outcome
- OATM-BR-120: key = PF5; update state = 'S' → Treated as Enter; nothing is saved
- OATM-BR-120: key = PF12; update state = not fetched → Treated as Enter

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-054: When saving an account update, a failure to lock the customer record is reported as a successful save. Is that intended, or should it be reported as a lock error? (Account servicing business owner) On OATM-BR-117, OATM-BR-118, OATM-BR-119.
- SME-062: What should the account update screen do in each of these cases: exit (PF3), first entry before any details are fetched, arriving from the menu, a completed save, a failed save, cancel (PF12), details shown, and answering 'N' to confirmation (PF5)? (Business analyst) On OATM-BR-119.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-117, OATM-BR-118, OATM-BR-119, OATM-BR-120.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).