# Detect changes before validating (OATM-C08)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Compares what the operator entered against the values fetched and runs field checks only when something has actually changed and the update is not already awaiting confirmation or saved. Text is compared ignoring case and surrounding spaces; numbers, dates and codes exactly. It must never re-validate or save unchanged details, and shows 'No change detected with respect to values fetched.' instead.

**User story:** As an operator, I want the system to check my entries only when I have actually changed something, so that unchanged details are not re-validated or saved.

## Requirements

### Requirement 1: OATM-REQ-F-068 (business rule)

#### Acceptance criteria

1. When the operator presses Enter on an account already shown, the system shall compare every entered value with the value fetched, ignoring upper/lower case and surrounding spaces for text fields (status, group, names, address, state, country, ZIP, government ID, primary-holder flag) and comparing amounts, dates, phone parts, SSN, EFT account and FICO exactly, counting any difference as a change. (rules OATM-BR-067)
2. GIVEN Fetched last name: SMITH; Entered last name: smith WHEN the operator presses Enter on an account already shown THEN No change is counted (OATM-C08-AC-01; OATM-BR-067)
3. GIVEN Fetched last name: SMITH; Entered last name: SMYTH WHEN the operator presses Enter on an account already shown THEN A change is counted (OATM-C08-AC-02; OATM-BR-067)
4. GIVEN Fetched credit limit: 5000.00; Entered credit limit: 5500.00 WHEN the operator presses Enter on an account already shown THEN A change is counted (OATM-C08-AC-03; OATM-BR-067)

### Requirement 2: OATM-REQ-F-069 (business rule)

#### Acceptance criteria

1. When no entered value differs from the fetched values, the system shall show 'No change detected with respect to values fetched.', run no field checks, save nothing and leave the details on screen without asking for confirmation. (rules OATM-BR-068)
2. GIVEN Fetched status: Y; Entered status: y; Other fields: unchanged WHEN no entered value differs from the fetched values THEN Message 'No change detected with respect to values fetched.'; nothing validated or saved (OATM-C08-AC-04; OATM-BR-068)

### Requirement 3: OATM-REQ-F-070 (business rule)

#### Acceptance criteria

1. While the update is neither awaiting confirmation ('N') nor completed ('C'), when a change is detected, the system shall mark the changes as not yet accepted ('E'), run every field check, and move the update to awaiting confirmation ('N') if all checks pass. (rules OATM-BR-069, OATM-BR-070, OATM-BR-071)
2. GIVEN Change detected: yes; Update state: details shown ('S'); All fields valid: yes WHEN a change is detected and the update is neither awaiting confirmation ('N') nor completed ('C') THEN State becomes 'N' and the operator is asked to confirm (OATM-C08-AC-05; OATM-BR-069)
3. GIVEN Change detected: yes; Update state: details shown ('S'); FICO entered: 900 WHEN a change is detected and the update is neither awaiting confirmation ('N') nor completed ('C') THEN State stays 'E' and the field error is shown (OATM-C08-AC-06; OATM-BR-069)
4. GIVEN Changes made: none WHEN several fields fail validation THEN No Y/N check is made (OATM-C08-AC-07; OATM-BR-071)

### Requirement 4: OATM-REQ-F-071 (design note)

#### Acceptance criteria

1. When no change is detected, or the update is awaiting confirmation ('N') or completed ('C'), the system shall clear all field error flags and skip every field check, including the date checks. (rules OATM-BR-072)
2. GIVEN Update state: 'N' (awaiting confirmation); Key pressed: Enter WHEN no change is detected, or the update is awaiting confirmation ('N') or completed ('C') THEN No field is re-checked and no field is highlighted as in error (OATM-C08-AC-08; OATM-BR-072)

### Requirement 5: OATM-REQ-F-072 (business rule)

#### Acceptance criteria

1. When several fields fail validation, the system shall flag every invalid field but show only the message of the first failing field. (rules OATM-BR-070, OATM-BR-071, OATM-BR-073)
2. GIVEN Changes made: none WHEN several fields fail validation THEN No Y/N check is made (OATM-C08-AC-07; OATM-BR-071)

## Screens and components

### Update account (S-ACCOUNT-EDIT)

Fetch an account, change its account and customer details in one form, see every error at its field, and save both records together only after reviewing the changes.

Prototype: `ui-reference/index.html#/S-ACCOUNT-EDIT`. Replaces the legacy screens CACTUPA.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Fix these fields | message | A summary listing every field in error, each linking to its field, in screen order; focus moves to the summary. Each field also shows its own message (the 3270 screen showed only the first message). |  |  | OATM-REQ-F-072 |
| Account and customer details | form | All account and customer fields, fetched values pre-filled; editable only while details are shown or have errors | If nothing differs from the fetched values (ignoring case): 'No change detected with respect to values fetched.' and nothing is checked or saved. |  |  |


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

- OATM-BR-072: Validation is a step gated by update state: when no change is detected or the update is awaiting confirmation or completed, reset all per-field error flags and skip the validators entirely, including date checks.

## Open questions

- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-070, OATM-BR-073.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-070, OATM-BR-073.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-070, OATM-BR-073.
- DEF-038: Confirm this is deliberate: The name, city, state and country fields accept only the letters A-Z and a-z and spaces. Real names and places with apostrophes, hyphens or periods ('O'Brien', 'St. Louis') are rejected. Separately, the blank-phone check tests the area-code part twice where it should test the line-number part. (Subject-matter expert) On OATM-BR-070.
- DEF-039: Confirm this is deliberate: Text fields are compared ignoring case and surrounding spaces, so a correction that only changes capitalisation (for example 'smith' to 'Smith') counts as no change and cannot be saved. (Subject-matter expert) On OATM-BR-067, OATM-BR-068, OATM-BR-069, OATM-BR-072.
- DEF-041: Is this intended? The 'phone not supplied' test checks the area code twice and never checks that the line number is blank-spaces (third condition tests area code = spaces OR line number = low-values). Because the screen input turns blanks into low-values first, this has no visible effect today, but a number arriving with a spaces area code and prefix would be accepted as omitted even with a line number entered. (Subject-matter expert) On OATM-BR-073.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).
