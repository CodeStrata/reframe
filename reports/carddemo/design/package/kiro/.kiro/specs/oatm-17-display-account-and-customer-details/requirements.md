# Requirements: Display account and customer details (OATM-C17)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Shows a user an account's financial details (status, balances, limits, cycle totals, dates and group) next to the linked customer's profile on one screen. It must show only what was actually found: account details only when the account was found, customer details only when the customer was found. The current error must always be visible. Under the current rules the full SSN is shown unmasked as NNN-NN-NNNN, so access to this screen needs care.

**User story:** As a user, I want to see an account's financial details and its customer's profile on one screen, so that I can review the account and the cardholder.

## Requirements

### Requirement 1: OATM-REQ-F-137 (formatting)

#### Acceptance criteria

1. When the account was found in the account master file, the system shall show the account status, current balance, credit limit, cash credit limit, current cycle credit, current cycle debit, open date, expiration date, reissue date and group id. (rules OATM-BR-140)
2. GIVEN account number: 00000012345; account master: found, status Y, balance 1500.00, credit limit 5000.00 WHEN the account was found in the account master file THEN Screen shows status Y, balance 1500.00, credit limit 5000.00 and the other account fields (OATM-C17-AC-01; OATM-BR-140)

### Requirement 2: OATM-REQ-F-138 (formatting)

#### Acceptance criteria

1. When the account's customer was found in the customer master file, the system shall show the customer id, FICO score, date of birth, first, middle and last name, address lines, city, state, zip, country, both phone numbers, government-issued id, EFT account id and primary card holder indicator. (rules OATM-BR-141, OATM-BR-142)
2. GIVEN Account number entered: 00000000002; Customer found in master: no (record not found) WHEN the customer was found in the customer master THEN No customer identity, contact or SSN fields are filled in on the screen. (OATM-C17-AC-02; OATM-BR-141)
3. GIVEN customer number: 000000001; customer master: found WHEN the account's customer was found in the customer master file THEN All customer fields shown with the account details (OATM-C17-AC-03; OATM-BR-142)
4. GIVEN account master: found; customer master: not found WHEN the account's customer was found in the customer master file THEN Account fields shown, customer fields empty, error 'Did not find associated customer in master file' (OATM-C17-AC-04; OATM-BR-142)

### Requirement 3: OATM-REQ-N-005 (business rule)

#### Acceptance criteria

1. When the customer is found, the system shall show the customer's full Social Security number, unmasked, in the form NNN-NN-NNNN. (rules OATM-BR-141, OATM-BR-143)
2. GIVEN Account number entered: 00000000002; Customer found in master: no (record not found) WHEN the customer was found in the customer master THEN No customer identity, contact or SSN fields are filled in on the screen. (OATM-C17-AC-02; OATM-BR-141)
3. GIVEN customer SSN: 123456789 WHEN the customer is found THEN Screen shows 123-45-6789 (OATM-C17-AC-05; OATM-BR-143)

### Requirement 4: OATM-REQ-F-139 (formatting)

#### Acceptance criteria

1. When the account view screen is shown with no session data passed (started directly), the system shall show no account or customer details and show the information line 'Enter or update id of account to display'. (rules OATM-BR-144)
2. GIVEN session data passed: none (transaction CAVW typed directly) WHEN the account view screen is shown with no session data passed (started directly) THEN Empty screen with info line 'Enter or update id of account to display' (OATM-C17-AC-06; OATM-BR-144)

### Requirement 5: OATM-REQ-F-140 (formatting)

#### Acceptance criteria

1. While session data exists, the system shall show the account number the user entered in the account number field, or leave the field empty when no account number was entered. (rules OATM-BR-145)
2. GIVEN entered account number: 00000012345 WHEN session data exists THEN Account number field shows 00000012345 (OATM-C17-AC-07; OATM-BR-145)
3. GIVEN entered account number: (blank) WHEN session data exists THEN Account number field is empty (OATM-C17-AC-08; OATM-BR-145)

### Requirement 6: OATM-REQ-F-141 (formatting)

#### Acceptance criteria

1. The system shall show 'Enter or update id of account to display' on the information line when no information message has been set, and always show the current error message, if there is one, on the error line. (rules OATM-BR-146)
2. GIVEN information message: (none); error message: 'Did not find this account in account master file' WHEN no information message has been set THEN Info line 'Enter or update id of account to display', error line 'Did not find this account in account master file' (OATM-C17-AC-09; OATM-BR-146)

### Requirement 7: OATM-REQ-F-142 (formatting)

#### Acceptance criteria

1. The system shall place the cursor on the account number field every time the account view screen is shown, whether or not the input had an error. (rules OATM-BR-147)
2. GIVEN Account number: ABC12345678 WHEN account view runs THEN The cursor is on the account number field (OATM-C17-AC-10; OATM-BR-147)
3. GIVEN Account number: 00000012345 (valid) WHEN account view runs THEN The cursor is also on the account number field (OATM-C17-AC-11; OATM-BR-147)
