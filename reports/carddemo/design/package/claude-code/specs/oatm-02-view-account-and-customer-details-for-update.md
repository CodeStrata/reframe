# View account and customer details for update (OATM-C02)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Shows the operator the stored account and customer details, or the values they have entered, with the right fields open for editing at each stage of the update. Only editable fields may be opened. Account number, customer number and country stay protected while editing, and every field is locked once changes are waiting for confirmation or saved. The screen must always show the current information and error messages.

**User story:** As an operator, I want the fetched or entered account and customer values shown with the right fields open for editing, so that I can see what is stored and change only what may be changed.

## Requirements

### Requirement 1: OATM-REQ-F-015 (formatting)

#### Acceptance criteria

1. The system shall always show the current information message and the current error or return message in their message lines. (rules OATM-BR-015)
2. GIVEN information message: 'Update account details presented above.'; return message: 'No change detected with respect to values fetched.' WHEN Account Update screen runs THEN Both messages appear on the screen (OATM-C02-AC-01; OATM-BR-015)

### Requirement 2: OATM-REQ-F-016 (formatting)

#### Acceptance criteria

1. When the account update screen shows the original values, the system shall clear all field-error flags and set the information message to 'Update account details presented above.' (rules OATM-BR-016)
2. GIVEN update stage: 'S' (details shown) WHEN the account update screen shows the original values THEN Error highlights are cleared and the message reads 'Update account details presented above.' (OATM-C02-AC-02; OATM-BR-016)

### Requirement 3: OATM-REQ-F-017 (formatting)

#### Acceptance criteria

1. When the account update screen is shown after details were fetched and the stage is details shown ('S') or changes not OK ('E'), the system shall set the information message to 'Update account details presented above.' (rules OATM-BR-017)
2. GIVEN update stage: 'S' WHEN the account update screen is shown after details were fetched and the stage is details shown ('S') or changes not OK ('E') THEN Message 'Update account details presented above.' (OATM-C02-AC-03; OATM-BR-017)
3. GIVEN update stage: 'E' WHEN the account update screen is shown after details were fetched and the stage is details shown ('S') or changes not OK ('E') THEN Message 'Update account details presented above.' (OATM-C02-AC-04; OATM-BR-017)

### Requirement 4: OATM-REQ-F-018 (formatting)

#### Acceptance criteria

1. When the original values are shown and either the account or the customer was found, the system shall show the stored account status, the current balance, credit limit, cash credit limit and cycle credit and debit as formatted amounts, the open, expiry and reissue dates as year, month and day, and the account group. (rules OATM-BR-018)
2. GIVEN account found: yes; stored credit limit: 5000.00; stored open date: 2015-03-14 WHEN the original values are shown and either the account or the customer was found THEN Credit limit shows as a formatted 5,000.00 and the open date shows as year 2015, month 03, day 14 (OATM-C02-AC-05; OATM-BR-018)

### Requirement 5: OATM-REQ-F-019 (formatting)

#### Acceptance criteria

1. When the original values are shown and the customer was found, the system shall show the stored customer details, with the SSN split into 3-2-4 digits, both phone numbers split into area code, prefix and line number, and the date of birth split into year, month and day. (rules OATM-BR-019)
2. GIVEN customer found: yes; stored SSN: 123456789; stored phone 1: (212)555-1234 WHEN the original values are shown and the customer was found THEN SSN shows as 123 / 45 / 6789 and phone 1 shows as 212 / 555 / 1234 (OATM-C02-AC-06; OATM-BR-019)

### Requirement 6: OATM-REQ-F-020 (formatting)

#### Acceptance criteria

1. When the account update screen is shown on re-entry, the system shall show the entered account id, but leave it blank when the id is zero and the account search is valid. (rules OATM-BR-020)
2. GIVEN account id: 00000000001 WHEN the account update screen is shown on re-entry THEN Account id 00000000001 is shown (OATM-C02-AC-07; OATM-BR-020)

### Requirement 7: OATM-REQ-F-021 (formatting)

#### Acceptance criteria

1. When the screen is shown on re-entry and either no details have been fetched or the account id is zero, the system shall show all account and customer fields blank. (rules OATM-BR-021)
2. GIVEN update stage: not fetched WHEN the screen is shown on re-entry and either no details have been fetched or the account id is zero THEN All detail fields are blank (OATM-C02-AC-08; OATM-BR-021)

### Requirement 8: OATM-REQ-F-022 (formatting)

#### Acceptance criteria

1. When the screen is shown on re-entry with details shown ('S'), the system shall show the original fetched values, and when changes have been made ('E', 'N', 'C', 'L', 'F'), the system shall show the values the operator entered. (rules OATM-BR-022)
2. GIVEN update stage: 'S' WHEN the screen is shown on re-entry with details shown ('S') THEN Original stored values are shown (OATM-C02-AC-09; OATM-BR-022)
3. GIVEN update stage: 'E'; entered credit limit: 7000.00 WHEN the screen is shown on re-entry with details shown ('S') THEN The entered 7000.00 is shown again, so the operator can correct it (OATM-C02-AC-10; OATM-BR-022)

### Requirement 9: OATM-REQ-F-023 (formatting)

#### Acceptance criteria

1. While account details are shown for editing (state 'S') or shown again with input errors (state 'E'), the system shall let the operator change status, credit and cash limits, balance, cycle credit and debit, open, expiry and reissue dates, group, SSN, FICO score, date of birth, names, address lines, city, state, ZIP, both phones, government ID, EFT account and primary-holder flag. (rules OATM-BR-023)
2. GIVEN Screen state: 'S'; Field: Credit limit WHEN account details are shown for editing (state 'S') or shown again with input errors (state 'E') THEN The field can be typed in (OATM-C02-AC-11; OATM-BR-023)

### Requirement 10: OATM-REQ-N-001 (formatting)

#### Acceptance criteria

1. While account details are shown for editing (state 'S' or 'E'), the system shall keep the account number, customer number and country protected so they cannot be changed. (rules OATM-BR-024)
2. GIVEN Screen state: 'E'; Field: Country WHEN account details are shown for editing (state 'S' or 'E') THEN The field is protected (OATM-C02-AC-12; OATM-BR-024)
3. GIVEN Screen state: 'S'; Field: Customer number WHEN account details are shown for editing (state 'S' or 'E') THEN The field is protected (OATM-C02-AC-13; OATM-BR-024)

### Requirement 11: OATM-REQ-N-002 (formatting)

#### Acceptance criteria

1. While changes are waiting for confirmation (state 'N') or have been saved (state 'C'), the system shall protect every field. (rules OATM-BR-025)
2. GIVEN Screen state: 'N' WHEN changes are waiting for confirmation (state 'N') or have been saved (state 'C') THEN All fields are protected while the operator decides whether to press F5 to save (OATM-C02-AC-14; OATM-BR-025)
3. GIVEN Screen state: not fetched (blank) WHEN changes are waiting for confirmation (state 'N') or have been saved (state 'C') THEN Only the account number can be entered (OATM-C02-AC-15; OATM-BR-025)

### Requirement 12: OATM-REQ-F-024 (formatting)

#### Acceptance criteria

1. While no account is fetched yet or the save failed, the system shall leave only the account number open for entry. (rules OATM-BR-025)
2. GIVEN Screen state: 'N' WHEN changes are waiting for confirmation (state 'N') or have been saved (state 'C') THEN All fields are protected while the operator decides whether to press F5 to save (OATM-C02-AC-14; OATM-BR-025)
3. GIVEN Screen state: not fetched (blank) WHEN changes are waiting for confirmation (state 'N') or have been saved (state 'C') THEN Only the account number can be entered (OATM-C02-AC-15; OATM-BR-025)

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
| Account number | **lookup field** | Pre-filled from the account in context; editable to fetch another account. Account number and customer ID are shown read-only once fetched | Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched. |  |  |
| Status and group | **summary card** | Account status as a choice of Active or Inactive (stored Y/N); Account group (optional, up to 10 characters) | Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values. |  | OATM-REQ-F-023 |
| Fix these before saving | **summary card** | Shown after a save attempt with errors: each field in error with its message, each a link that moves focus to the field; focus moves to this summary. Replaces the legacy single message line, which showed only the first error; every invalid field is still flagged |  |  | OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017 |
| Save changes | **primary button** | Runs every check; with no change shows 'No change detected with respect to values fetched.' and saves nothing; when all checks pass, a confirmation dialog lists each change (old to new) with Confirm and Cancel; success shows 'Changes committed to database' and the account returns to view | If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved. |  | OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-024, OATM-REQ-N-001, OATM-REQ-N-002 |


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
| OATM-BR-015 | Default to search prompt and show messages | formatting | THE Account Update screen SHALL always show the current information message and the current error or return message in their message lines. | medium | app/cbl/COACTUPC.cbl:2955-2982, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-016 | Display fetched original values | formatting | WHEN the account update screen shows the original values, THE Account Update screen SHALL clear all field-error flags (WS-NON-KEY-FLAGS) and set the information message to 'Update account details presented above.' | medium | app/cbl/COACTUPC.cbl:2785-2864, app/cbl/COACTUPC.cbl:2698-2725 |
| OATM-BR-017 | Prompt operator to edit shown details | formatting | WHEN the account update screen is shown after details were fetched and the stage is details shown ('S') or changes not OK ('E'), THE Account Update messaging SHALL set the information message to 'Update account details presented above.' | medium | app/cbl/COACTUPC.cbl:2962-2965, app/cbl/COACTUPC.cbl:470-471 |
| OATM-BR-018 | Display fetched original values | formatting | WHEN the original values are shown and either the account or the customer was found, THE Account Update screen SHALL show the stored account status, the current balance, credit limit, cash credit limit and cycle credit and debit as formatted amounts, the open, expiry and reissue dates as year, month and day, and the account group. | medium | app/cbl/COACTUPC.cbl:2785-2864, app/cbl/COACTUPC.cbl:2698-2725 |
| OATM-BR-019 | Display fetched original values | formatting | WHEN the original values are shown and the customer was found, THE Account Update screen SHALL show the stored customer details, with the SSN split into 3-2-4 digits, both phone numbers split into area code, prefix and line number, and the date of birth split into year, month and day. | medium | app/cbl/COACTUPC.cbl:2785-2864, app/cbl/COACTUPC.cbl:2698-2725 |
| OATM-BR-020 | Choose which account values to display | formatting | WHEN the account update screen is shown on re-entry, THE Account Update screen SHALL show the entered account id, but leave it blank when the id is zero and the account search is valid. | medium | app/cbl/COACTUPC.cbl:2698-2725, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-021 | Choose which account values to display | formatting | WHEN the screen is shown on re-entry and either no details have been fetched or the account id is zero, THE Account Update screen SHALL show all account and customer fields blank. | medium | app/cbl/COACTUPC.cbl:2698-2725, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-022 | Choose which account values to display | formatting | WHEN the screen is shown on re-entry with details shown ('S'), THE Account Update screen SHALL show the original fetched values; WHEN changes have been made ('E','N','C','L','F'), it SHALL show the values the operator entered. | medium | app/cbl/COACTUPC.cbl:2698-2725, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-023 | Editable versus protected fields | formatting | WHEN account details are shown for editing (state 'S') or shown again with input errors (state 'E'), THE account update screen SHALL let the operator change status, credit and cash limits, balance, cycle credit and debit, open, expiry and reissue dates, group, SSN, FICO score, date of birth, names, address lines, city, state, ZIP, both phones, government ID, EFT account and primary-holder flag. | medium | app/cbl/COACTUPC.cbl:2986-3005, app/cbl/COACTUPC.cbl:3441-3495, app/cbl/COACTUPC.cbl:3500-3560, app/cbl/COACTUPC.cbl:654-668 |
| OATM-BR-024 | Editable versus protected fields | formatting | WHEN account details are shown for editing (state 'S' or 'E'), THE account update screen SHALL keep the account number, customer number and country protected so they cannot be changed. | medium | app/cbl/COACTUPC.cbl:2986-3005, app/cbl/COACTUPC.cbl:3441-3495, app/cbl/COACTUPC.cbl:3500-3560, app/cbl/COACTUPC.cbl:654-668 |
| OATM-BR-025 | Editable versus protected fields | formatting | WHEN changes are waiting for confirmation (state 'N') or have been saved (state 'C'), THE account update screen SHALL protect every field; WHEN no account is fetched yet or the save failed, it SHALL leave only the account number open for entry. | medium | app/cbl/COACTUPC.cbl:2986-3005, app/cbl/COACTUPC.cbl:3441-3495, app/cbl/COACTUPC.cbl:3500-3560, app/cbl/COACTUPC.cbl:654-668 |

### Worked examples

- OATM-BR-015: information message = 'Update account details presented above.'; return message = 'No change detected with respect to values fetched.' → Both messages appear on the screen
- OATM-BR-016: update stage = 'S' (details shown) → Error highlights are cleared and the message reads 'Update account details presented above.'
- OATM-BR-017: update stage = 'S' → Message 'Update account details presented above.'
- OATM-BR-017: update stage = 'E' → Message 'Update account details presented above.'
- OATM-BR-018: account found = yes; stored credit limit = 5000.00; stored open date = 2015-03-14 → Credit limit shows as a formatted 5,000.00 and the open date shows as year 2015, month 03, day 14
- OATM-BR-019: customer found = yes; stored SSN = 123456789; stored phone 1 = (212)555-1234 → SSN shows as 123 / 45 / 6789 and phone 1 shows as 212 / 555 / 1234
- OATM-BR-020: account id = 00000000001 → Account id 00000000001 is shown
- OATM-BR-021: update stage = not fetched → All detail fields are blank
- OATM-BR-022: update stage = 'S' → Original stored values are shown
- OATM-BR-022: update stage = 'E'; entered credit limit = 7000.00 → The entered 7000.00 is shown again, so the operator can correct it
- OATM-BR-023: Screen state = 'S'; Field = Credit limit → The field can be typed in
- OATM-BR-024: Screen state = 'E'; Field = Country → The field is protected
- OATM-BR-024: Screen state = 'S'; Field = Customer number → The field is protected
- OATM-BR-025: Screen state = 'N' → All fields are protected while the operator decides whether to press F5 to save
- OATM-BR-025: Screen state = not fetched (blank) → Only the account number can be entered

## Decision tables

#### Field protection by update stage

| Update stage | Fields open for entry | Rule |
|---|---|---|
| Details shown ('S') | Account and customer detail fields editable; account number, customer number and country protected | OATM-BR-023 |
| Changes not OK ('E') | Account and customer detail fields editable; account number, customer number and country protected | OATM-BR-024 |
| Awaiting confirmation ('N') | Every field protected | OATM-BR-025 |
| Saved ('C') | Every field protected | OATM-BR-025 |
| No account fetched yet | Only account number open | OATM-BR-025 |
| Save failed | Only account number open | OATM-BR-025 |
| Stage 'L' | **Gap:** R31 lists stage 'L' among change stages, but no rule says which fields are open or protected in that stage. | |

#### Which values are shown on re-entry

| Details fetched | Account id zero | Update stage | Values shown | Rule |
|---|---|---|---|---|
| No | - | - | All account and customer fields blank | OATM-BR-021 |
| - | Yes | - | All account and customer fields blank | OATM-BR-021 |
| Yes | No | Details shown ('S') | Original fetched values | OATM-BR-022 |
| Yes | No | Changes made ('E','N','C','L','F') | Values the operator entered | OATM-BR-022 |


## Design notes

None.

## Open questions

None.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (15 in all).
