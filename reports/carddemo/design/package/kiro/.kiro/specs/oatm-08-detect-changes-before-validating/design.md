# Design: Detect changes before validating (OATM-C08)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Overview

Compares what the operator entered with the values fetched for the account, ignoring upper or lower case, and runs the field checks only when something has actually changed. If nothing changed, it says 'No change detected with respect to values fetched.' and does not validate or save anything. It must never save or re-validate unchanged details. When several fields fail, it flags all of them but shows only the first message.

Runs as online. Journeys: J02.

## Screens and components

### Account (S-ACCOUNT-VIEW)

Look up an account by account number or card number and show its status, balances, limits and dates beside the customer profile on one screen, while the caller waits. Tab order: search, the cards, then Update account.

Prototype: `ui-reference/index.html#/S-ACCOUNT-VIEW`. Replaces the legacy screens CACTVWA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Update account (S-ACCOUNT-EDIT)

Change an account's and its customer's details after confirming the caller. Each field is checked as it is left and again on save; every failing field shows its own message and a summary lists them all. Save asks for confirmation, listing each change from old to new value. Tab order: account and status, dates, amounts, customer identity, name and address, contact, then Save changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Status and group | **summary card** | Account status as a choice of Active or Inactive (stored Y/N); Account group (optional, up to 10 characters) | Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values. |  |  |
| Phone and payments | **summary card** | Phone 1 and Phone 2 (optional), each as labelled Area code, Prefix and Line number; EFT account ID; Primary card holder as a choice of Yes or No | A phone may be left wholly blank; otherwise '<Phone Number 1 or 2>: Area code must be supplied.', ': Area code must be A 3 digit number.', ': Area code cannot be zero', ': Not valid North America general purpose area code' (from the list of general-purpose codes), ': Prefix code must be supplied.', ': Prefix code must be A 3 digit number.', ': Prefix code cannot be zero', ': Line number code must be supplied.', ': Line number code must be A 4 digit number.', ': Line number code cannot be zero'. EFT account ID: 'EFT Account Id must be supplied.', all numeric, 10 digits, not zero. Primary card holder: 'Primary Card Holder must be supplied.' and must be Yes or No ('must be Y or N.'). |  |  |
| Fix these before saving | **summary card** | Shown after a save attempt with errors: each field in error with its message, each a link that moves focus to the field; focus moves to this summary. Replaces the legacy single message line, which showed only the first error; every invalid field is still flagged |  |  | OATM-REQ-F-072 |
| Save changes | **primary button** | Runs every check; with no change shows 'No change detected with respect to values fetched.' and saves nothing; when all checks pass, a confirmation dialog lists each change (old to new) with Confirm and Cancel; success shows 'Changes committed to database' and the account returns to view | If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved. |  | OATM-REQ-F-068, OATM-REQ-F-069, OATM-REQ-F-070, OATM-REQ-F-071 |


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
| OATM-BR-067 | Detect changes between old and new details | business rule | WHEN the operator presses Enter on an account already shown, THE account update SHALL compare every entered value with the value fetched, ignoring upper/lower case and surrounding spaces for text fields (status, group, names, address, state, country, ZIP, government ID, primary-holder flag) and comparing amounts, dates, phone parts, SSN, EFT account and FICO exactly; any difference counts as a change. | high | app/cbl/COACTUPC.cbl:1429-1470, app/cbl/COACTUPC.cbl:1670-1675, app/cbl/COACTUPC.cbl:1681-1779, app/cbl/COACTUPC.cbl:165-170 |
| OATM-BR-068 | Detect changes against fetched values | business rule | WHEN no entered value differs from the fetched values, THE account update SHALL show 'No change detected with respect to values fetched.', run no field checks, save nothing and leave the details on screen without asking for confirmation. | high | app/cbl/COACTUPC.cbl:1429-1470, app/cbl/COACTUPC.cbl:1670-1675, app/cbl/COACTUPC.cbl:1681-1779, app/cbl/COACTUPC.cbl:165-170 |
| OATM-BR-069 | Gate validation on detected changes | business rule | WHEN a change is detected and the update is neither awaiting confirmation ('N') nor completed ('C'), THE account update SHALL mark the changes as not yet accepted ('E') and run every field check; if all checks pass it SHALL move the update to awaiting confirmation ('N'). | high | app/cbl/COACTUPC.cbl:1429-1470, app/cbl/COACTUPC.cbl:1670-1675, app/cbl/COACTUPC.cbl:1681-1779, app/cbl/COACTUPC.cbl:165-170 |
| OATM-BR-070 | Require mandatory text present | business rule | WHEN the account update checks the operator's changes, THE account update SHALL show only the first error message found, while still flagging every invalid field, and it SHALL run these checks only when the operator has changed something that is not yet awaiting confirmation. | high | app/cbl/COACTUPC.cbl:1288-1334, app/cbl/COACTUPC.cbl:1410-1415, app/cbl/COACTUPC.cbl:1462-1471, app/cbl/COACTUPC.cbl:1560-1675 |
| OATM-BR-071 | Yes/No flags: account active status and primary cardholder | business rule | WHEN several fields fail validation, THE Account Update screen SHALL show only the message of the first failing field, and SHALL run these Y/N checks only after the account has been fetched and the operator has changed at least one value. | high | app/cbl/COACTUPC.cbl:1064-1070, app/cbl/COACTUPC.cbl:1419-1424, app/cbl/COACTUPC.cbl:1458-1476, app/cbl/COACTUPC.cbl:1657-1662 |
| OATM-BR-072 | Skip edits when nothing changed | design note | WHEN no change is detected, or the update is awaiting confirmation ('N') or completed ('C'), THE account update SHALL clear all field error flags and skip every field check, including the date checks. | high | app/cbl/COACTUPC.cbl:1429-1470, app/cbl/COACTUPC.cbl:1670-1675, app/cbl/COACTUPC.cbl:1681-1779, app/cbl/COACTUPC.cbl:165-170 |
| OATM-BR-073 | Validate phone area code | formatting | WHEN more than one phone number part fails its checks, THE Account Update SHALL flag every failing part in error but show only the first message raised on the screen (no later message replaces one already set). | high | app/cbl/COACTUPC.cbl:1357-1397, app/cbl/COACTUPC.cbl:1632-1646, app/cbl/COACTUPC.cbl:2225-2429, app/cbl/COACTUPC.cbl:82-100 |

### Worked examples

- OATM-BR-067: Fetched last name = SMITH; Entered last name = smith → No change is counted
- OATM-BR-067: Fetched last name = SMITH; Entered last name = SMYTH → A change is counted
- OATM-BR-067: Fetched credit limit = 5000.00; Entered credit limit = 5500.00 → A change is counted
- OATM-BR-068: Fetched status = Y; Entered status = y; Other fields = unchanged → Message 'No change detected with respect to values fetched.'; nothing validated or saved
- OATM-BR-069: Change detected = yes; Update state = details shown ('S'); All fields valid = yes → State becomes 'N' and the operator is asked to confirm
- OATM-BR-069: Change detected = yes; Update state = details shown ('S'); FICO entered = 900 → State stays 'E' and the field error is shown
- OATM-BR-071: Changes made = none → No Y/N check is made
- OATM-BR-072: Update state = 'N' (awaiting confirmation); Key pressed = Enter → No field is re-checked and no field is highlighted as in error

## Decision tables

#### Change detection and validation gating

| Change detected | Update state | Validation action | Rule |
|---|---|---|---|
| No | Any | Show 'No change detected with respect to values fetched.', clear error flags, run no checks, save nothing | OATM-BR-068 |
| Yes | Not 'N' and not 'C' | Mark changes 'E', run every field check; move to 'N' if all pass | OATM-BR-069 |
| Yes | Awaiting confirmation ('N') | Clear error flags and skip every field check | OATM-BR-072 |
| Yes | Completed ('C') | Clear error flags and skip every field check | OATM-BR-072 |


## Design notes

- OATM-BR-072: Before validating, decide from the update stage and the change-detection result: if nothing changed, or the update is awaiting confirmation or already completed, clear all field-error flags and skip every field and date check. Validation is a step the server runs only when a change is detected while editing.

## Open questions

- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-070, OATM-BR-073.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-070, OATM-BR-073.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-070, OATM-BR-073.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-070.
- DEF-039: Confirm this is deliberate: Text fields are compared ignoring case and surrounding spaces, so a correction that only changes capitalisation (for example 'smith' to 'Smith') counts as no change and cannot be saved. (Subject-matter expert) On OATM-BR-067, OATM-BR-068, OATM-BR-069, OATM-BR-072.
- DEF-041: Is this intended? The 'phone not supplied' test checks the area code twice and never checks that the line number is blank-spaces (third condition tests area code = spaces OR line number = low-values). Because the screen input turns blanks into low-values first, this has no visible effect today, but a number arriving with a spaces area code and prefix would be accepted as omitted even with a line number entered. (Subject-matter expert) On OATM-BR-073.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).