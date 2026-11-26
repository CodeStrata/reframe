# Update account details with validation and confirmation (OATM-C15)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Lets an operator change an account's and its customer's details. Every changed value is checked, and a save happens only after the operator explicitly confirms with PF5. Changes that fail a check, or that are not confirmed, must never be saved. The operator must always be told whether there was nothing to change, whether the changes were validated, or whether the save was committed or failed.

**User story:** As an operator, I want my changes to account details checked and then saved only when I confirm them with PF5, so that only validated changes reach the account record and I know whether the save succeeded.

## Requirements

### Requirement 1: OATM-REQ-F-118 (business rule)

#### Acceptance criteria

1. While details are shown, when the operator changes one or more values, the system shall check every field and set the state to 'N' with the message 'Changes validated.Press F5 to save' if no check fails, or to 'E' (changes not OK) if any check fails. (rules OATM-BR-121)
2. GIVEN credit limit: changed from 5000.00 to 7000.00; all other fields: valid WHEN details are shown and the operator changes one or more values THEN State 'N'; message 'Changes validated.Press F5 to save' (OATM-C15-AC-01; OATM-BR-121)
3. GIVEN account status: changed to 'X' WHEN details are shown and the operator changes one or more values THEN State 'E'; an error message is shown and nothing can be saved (OATM-C15-AC-02; OATM-BR-121)

### Requirement 2: OATM-REQ-F-119 (business rule)

#### Acceptance criteria

1. While details are shown, when the operator submits without changing any value, the system shall keep the details shown (state 'S') and report 'No change detected with respect to values fetched.'. (rules OATM-BR-122)
2. GIVEN update state: 'S'; screen values: same as fetched WHEN details are shown and the operator submits without changing any value THEN State stays 'S'; message 'No change detected with respect to values fetched.' (OATM-C15-AC-03; OATM-BR-122)

### Requirement 3: OATM-REQ-F-120 (business rule)

#### Acceptance criteria

1. When the state is changes not OK ('E'), or validated changes ('N') are submitted without PF5, the system shall save nothing and show the details again for correction or confirmation. (rules OATM-BR-123)
2. GIVEN update state: 'N'; key: Enter WHEN the state is changes not OK ('E'), or validated changes ('N') are submitted without PF5 THEN Nothing saved; state stays 'N' with 'Changes validated.Press F5 to save' (OATM-C15-AC-04; OATM-BR-123)

### Requirement 4: OATM-REQ-F-121 (business rule)

#### Acceptance criteria

1. When validated changes ('N') are confirmed with PF5, the system shall save them and set the state to 'L' if the account cannot be locked, 'F' if the locked update fails, 'S' (details shown again) if someone else changed the record since it was read, or 'C' otherwise. (rules OATM-BR-124)
2. GIVEN update state: 'N'; key: PF5; record: unchanged by others, lock and update succeed WHEN validated changes ('N') are confirmed with PF5 THEN State 'C' (OATM-C15-AC-05; OATM-BR-124)
3. GIVEN update state: 'N'; key: PF5; record: changed by another user since it was read WHEN validated changes ('N') are confirmed with PF5 THEN State 'S'; the details are shown again (OATM-C15-AC-06; OATM-BR-124)

### Requirement 5: OATM-REQ-F-122 (formatting)

#### Acceptance criteria

1. When a save completes ('C'), the system shall show the message 'Changes committed to database'. (rules OATM-BR-125)
2. GIVEN save outcome: success WHEN a save completes ('C') THEN Message 'Changes committed to database' (OATM-C15-AC-07; OATM-BR-125)

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
| Name and address | **summary card** | First name, Middle name (optional), Last name; Address line 1, Address line 2 (optional); City; State (a choice of US state codes); ZIP; Country | '<field> must be supplied.' for First Name, Last Name, City, State, Country and Address Line 1; '<field> can have alphabets only.' for names, city, state and country; 'Middle Name can have alphabets only.'; 'State: is not a valid state code'; ZIP: 'ZIP must be supplied.', must be all numeric, 5 digits and not zero; 'Invalid zip code for state' - check the state and ZIP together. |  |  |
| Fix these before saving | **summary card** | Shown after a save attempt with errors: each field in error with its message, each a link that moves focus to the field; focus moves to this summary. Replaces the legacy single message line, which showed only the first error; every invalid field is still flagged |  |  | OATM-REQ-F-120 |
| Save changes | **primary button** | Runs every check; with no change shows 'No change detected with respect to values fetched.' and saves nothing; when all checks pass, a confirmation dialog lists each change (old to new) with Confirm and Cancel; success shows 'Changes committed to database' and the account returns to view | If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved. |  | OATM-REQ-F-118, OATM-REQ-F-119, OATM-REQ-F-120, OATM-REQ-F-121, OATM-REQ-F-122 |


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
| OATM-BR-121 | Cross-check state and ZIP, set verdict | business rule | WHEN details are shown and the operator changes one or more values, THE account update screen SHALL check every field and SHALL set the state to 'N' with the message 'Changes validated.Press F5 to save' if no check fails, or to 'E' (changes not OK) if any check fails. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-122 | Request confirmation for valid changes | business rule | WHEN details are shown and the operator submits without changing any value, THE account update screen SHALL keep the details shown (state 'S') and report 'No change detected with respect to values fetched.'. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-123 | Redisplay when edits fail or confirmation pending | business rule | WHEN the state is changes not OK ('E'), or validated changes ('N') are submitted without PF5, THE account update screen SHALL save nothing and show the details again for correction or confirmation. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-124 | Save confirmed changes and record outcome | business rule | WHEN validated changes ('N') are confirmed with PF5, THE account update screen SHALL save them and set the state to 'L' if the account cannot be locked, 'F' if the locked update fails, 'S' (details shown again) if someone else changed the record since it was read, or 'C' otherwise. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |
| OATM-BR-125 | Confirm successful update commit | formatting | WHEN a save completes ('C'), THE account update screen SHALL show the message 'Changes committed to database'. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

### Worked examples

- OATM-BR-121: credit limit = changed from 5000.00 to 7000.00; all other fields = valid → State 'N'; message 'Changes validated.Press F5 to save'
- OATM-BR-121: account status = changed to 'X' → State 'E'; an error message is shown and nothing can be saved
- OATM-BR-122: update state = 'S'; screen values = same as fetched → State stays 'S'; message 'No change detected with respect to values fetched.'
- OATM-BR-123: update state = 'N'; key = Enter → Nothing saved; state stays 'N' with 'Changes validated.Press F5 to save'
- OATM-BR-124: update state = 'N'; key = PF5; record = unchanged by others, lock and update succeed → State 'C'
- OATM-BR-124: update state = 'N'; key = PF5; record = changed by another user since it was read → State 'S'; the details are shown again
- OATM-BR-125: save outcome = success → Message 'Changes committed to database'

## Decision tables

#### Account update outcome by state, key and save result

| State | Key pressed | Save result | Resulting action and state | Rule |
|---|---|---|---|---|
| Details shown, values changed | Any | All checks pass | State 'N', message 'Changes validated.Press F5 to save' | OATM-BR-121 |
| Details shown, values changed | Any | Any check fails | State 'E' (changes not OK) | OATM-BR-121 |
| Details shown, no value changed | Any | — | State 'S', message 'No change detected with respect to values fetched.' | OATM-BR-122 |
| 'E' | Any | — | Save nothing; show details again for correction | OATM-BR-123 |
| 'N' | Not PF5 | — | Save nothing; show details again for confirmation | OATM-BR-123 |
| 'N' | PF5 | Account cannot be locked | State 'L' | OATM-BR-124 |
| 'N' | PF5 | Locked update fails | State 'F' | OATM-BR-124 |
| 'N' | PF5 | Record changed by someone else since read | State 'S' (details shown again) | OATM-BR-124 |
| 'N' | PF5 | Saved | State 'C', message 'Changes committed to database' | OATM-BR-125 |
| 'L', 'F' or 'C' | Any | — | **Gap:** No rule says what happens on the next submission after a failed lock ('L'), failed update ('F') or completed save ('C'). | |


## Design notes

None.

## Open questions

- SME-054: When saving an account update, a failure to lock the customer record is reported as a successful save. Is that intended, or should it be reported as a lock error? (Account servicing business owner) On OATM-BR-122, OATM-BR-123, OATM-BR-124.
- SME-062: What should the account update screen do in each of these cases: exit (PF3), first entry before any details are fetched, arriving from the menu, a completed save, a failed save, cancel (PF12), details shown, and answering 'N' to confirmation (PF5)? (Business analyst) On OATM-BR-123.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-121, OATM-BR-122, OATM-BR-123, OATM-BR-124, OATM-BR-125.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (7 in all).
