# Requirements: View account and customer details for update (OATM-C02)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Shows the operator the fetched or entered account and customer values on the Update account screen, with the right message and only the permitted fields open for editing at each stage of the update. Account number, customer number and country must never be editable, and every field must be locked once changes await confirmation or have been saved.

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
