# Feature specification: Display account and customer details

**Feature:** OATM-C17 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C17)

As a user, I want to see an account's financial details and its customer's profile on one screen, so that I can review the account and the cardholder.

Shows a user an account's financial details (status, balances, limits, cycle totals, dates and group) next to the linked customer's profile on one screen. It must show only what was actually found: account details only when the account was found, customer details only when the customer was found. The current error must always be visible. Under the current rules the full SSN is shown unmasked as NNN-NN-NNNN, so access to this screen needs care.

**Acceptance scenarios:**

1. **Given** account number: 00000012345; account master: found, status Y, balance 1500.00, credit limit 5000.00, **when** the account was found in the account master file, **then** Screen shows status Y, balance 1500.00, credit limit 5000.00 and the other account fields (OATM-C17-AC-01)
2. **Given** Account number entered: 00000000002; Customer found in master: no (record not found), **when** the customer was found in the customer master, **then** No customer identity, contact or SSN fields are filled in on the screen. (OATM-C17-AC-02)
3. **Given** customer number: 000000001; customer master: found, **when** the account's customer was found in the customer master file, **then** All customer fields shown with the account details (OATM-C17-AC-03)
4. **Given** account master: found; customer master: not found, **when** the account's customer was found in the customer master file, **then** Account fields shown, customer fields empty, error 'Did not find associated customer in master file' (OATM-C17-AC-04)
5. **Given** customer SSN: 123456789, **when** the customer is found, **then** Screen shows 123-45-6789 (OATM-C17-AC-05)
6. **Given** session data passed: none (transaction CAVW typed directly), **when** the account view screen is shown with no session data passed (started directly), **then** Empty screen with info line 'Enter or update id of account to display' (OATM-C17-AC-06)
7. **Given** entered account number: 00000012345, **when** session data exists, **then** Account number field shows 00000012345 (OATM-C17-AC-07)
8. **Given** entered account number: (blank), **when** session data exists, **then** Account number field is empty (OATM-C17-AC-08)
9. **Given** information message: (none); error message: 'Did not find this account in account master file', **when** no information message has been set, **then** Info line 'Enter or update id of account to display', error line 'Did not find this account in account master file' (OATM-C17-AC-09)
10. **Given** Account number: ABC12345678, **when** account view runs, **then** The cursor is on the account number field (OATM-C17-AC-10)
11. **Given** Account number: 00000012345 (valid), **when** account view runs, **then** The cursor is also on the account number field (OATM-C17-AC-11)

## Requirements

### Functional requirements

- **OATM-REQ-F-137** (formatting): When the account was found in the account master file, the system shall show the account status, current balance, credit limit, cash credit limit, current cycle credit, current cycle debit, open date, expiration date, reissue date and group id. Rules: OATM-BR-140.
- **OATM-REQ-F-138** (formatting): When the account's customer was found in the customer master file, the system shall show the customer id, FICO score, date of birth, first, middle and last name, address lines, city, state, zip, country, both phone numbers, government-issued id, EFT account id and primary card holder indicator. Rules: OATM-BR-141, OATM-BR-142.
- **OATM-REQ-N-005** (business rule): When the customer is found, the system shall show the customer's full Social Security number, unmasked, in the form NNN-NN-NNNN. Rules: OATM-BR-141, OATM-BR-143.
- **OATM-REQ-F-139** (formatting): When the account view screen is shown with no session data passed (started directly), the system shall show no account or customer details and show the information line 'Enter or update id of account to display'. Rules: OATM-BR-144.
- **OATM-REQ-F-140** (formatting): While session data exists, the system shall show the account number the user entered in the account number field, or leave the field empty when no account number was entered. Rules: OATM-BR-145.
- **OATM-REQ-F-141** (formatting): The system shall show 'Enter or update id of account to display' on the information line when no information message has been set, and always show the current error message, if there is one, on the error line. Rules: OATM-BR-146.
- **OATM-REQ-F-142** (formatting): The system shall place the cursor on the account number field every time the account view screen is shown, whether or not the input had an error. Rules: OATM-BR-147.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-140 | Display account financial details | formatting | WHEN the account was found in the account master file, THE Account View Screen SHALL show the account status, current balance, credit limit, cash credit limit, current cycle credit, current cycle debit, open date, expiration date, reissue date and group id. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-141 | Display customer profile with formatted SSN | formatting | WHEN the customer was found in the customer master, THE Account View Screen Display SHALL display the customer identity, contact, credit score and indicators, with the SSN formatted as NNN-NN-NNNN | medium | app/cbl/COACTVWC.cbl:493-494,496-523,525, app/cbl/COACTVWC.cbl:493-507 |
| OATM-BR-142 | Account and customer details displayed only when found in master files | formatting | WHEN the account's customer was found in the customer master file, THE Account View Screen SHALL show the customer id, FICO score, date of birth, first, middle and last name, address lines, city, state, zip, country, both phone numbers, government-issued id, EFT account id and primary card holder indicator. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-143 | Account and customer details displayed only when found in master files | business rule | WHEN the customer is found, THE Account View Screen SHALL show the customer's full Social Security number, unmasked, in the form NNN-NN-NNNN. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-144 | Show prompt or entered account number | formatting | WHEN the account view screen is shown with no session data passed (started directly), THE Account View Screen SHALL show no account or customer details and SHALL show the information line 'Enter or update id of account to display'. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-145 | Show prompt or entered account number | formatting | WHEN session data exists, THE Account View Screen SHALL show the account number the user entered in the account number field, or leave the field empty when no account number was entered. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-146 | Set default prompt and screen messages | formatting | WHEN no information message has been set, THE Account View Screen SHALL show 'Enter or update id of account to display' on the information line, and SHALL always show the current error message, if there is one, on the error line. | high | app/cbl/COACTVWC.cbl:460-535, app/cbl/COACTVWC.cbl:687-718, app/cbl/COACTVWC.cbl:110-116 |
| OATM-BR-147 | Account ID search key must be a non-zero 11-digit number | formatting | THE account view SHALL place the cursor on the account number field every time the screen is shown, whether or not the input had an error. | high | app/cbl/COACTVWC.cbl:622-643, app/cbl/COACTVWC.cbl:649-685, app/cbl/COACTVWC.cbl:117-124, app/cbl/COACTVWC.cbl:362-367 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CVACT02Y (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-067: When an account number is entered on the account view screen and the account is not found, or the file cannot be read, should the lookup stop at that point? (Currently it stops only on one exact message, 'Did not find this account in account master file', and the real not-found path produces a different message.) (Business analyst) On OATM-BR-141, OATM-BR-145, OATM-BR-140, OATM-BR-146.
- SME-068: On the account view screen, if the account number is left blank, which message should the operator see: 'Account number not provided' or 'No input received'? (Business analyst) On OATM-BR-141, OATM-BR-145, OATM-BR-140, OATM-BR-146.
- SME-069: On the account view screen, the error message says the account number must be 'a non-zero 11 digit number', but only 'numeric and non-zero' is checked. Should exactly 11 digits be required? Should the message keep its current double space? (Business analyst) On OATM-BR-141, OATM-BR-145, OATM-BR-140, OATM-BR-146.
- SME-070: On the account view screen, if the customer record is found but the account record is not, should the account's financial details still be shown? After a successful lookup, should the screen show a success message ('Displaying details of given Account') instead of the input prompt? (Customer service operations lead) On OATM-BR-141, OATM-BR-145, OATM-BR-140, OATM-BR-146.
- SME-072: The account view shows every user the customer's full, unmasked Social Security number. Is that acceptable under privacy policy, or should the new system show only the last 4 digits or limit the full number to certain roles? (Privacy and compliance officer) On OATM-BR-141.
- DEF-044: Is this intended? A blank account number first sets the message 'Account number not provided', which is then replaced at once with 'No input received', so the more specific message can never be shown. The 'only if no message yet' guard in front of it has no effect. (Subject-matter expert) On OATM-BR-147.
- DEF-091: Is this intended? The success message 'Displaying details of given Account' is defined but never set, and the account read clears the information message. As a result, the info line still says 'Enter or update id of account to display' after an account is shown successfully. (Subject-matter expert) On OATM-BR-145, OATM-BR-140, OATM-BR-146.

### Decision table gaps

None.
