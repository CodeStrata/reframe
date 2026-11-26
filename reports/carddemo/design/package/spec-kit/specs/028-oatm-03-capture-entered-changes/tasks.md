# Tasks: Capture entered changes (OATM-C03)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C03-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
- [ ] OATM-C03-T2 [api] Build the services behind the screens. Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032. Rules: OATM-BR-026, OATM-BR-027, OATM-BR-028, OATM-BR-029, OATM-BR-030, OATM-BR-031, OATM-BR-032, OATM-BR-033. After: OATM-C03-T1.
  - OATM-BR-026: Input binding for account group: map blank or '*' to an explicit 'not supplied' value (null), otherwise keep the entered text as the proposed group.
  - OATM-BR-027: Input binding for country code: map blank or '*' to null (not supplied), otherwise keep the entered value as the proposed country code.
  - OATM-BR-028: Input binding for customer number once details are shown: blank or '*' becomes null; any other value is carried as the proposed value, compared with the snapshot and written to the customer record on save.
  - OATM-BR-029: Input binding for government-issued ID once details are shown: blank or '*' becomes null; otherwise the entered value is the proposed ID, compared with the snapshot and written to the customer record on save.
  - OATM-BR-030: Input binding for the five amounts (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit): blank or '*' becomes null (not supplied) so validation can report it as missing.
  - OATM-BR-031: A currency parser that accepts an optional '$', thousands commas, a sign and decimals, and yields a decimal amount at scale 2 (use a decimal type, not floating point); unparseable text stays as entered for validation to reject.
  - OATM-BR-032: Input binding for open, expiry and reissue dates as separate year, month and day parts: each part that is blank or '*' becomes null, any other entry is kept exactly as typed for the date checks.
  - OATM-BR-033: Input binding for date of birth parts (year, month, day): blank or '*' becomes null, otherwise the part is kept as the proposed value.
- [ ] OATM-C03-T3 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT). Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-032. Rules: OATM-BR-026, OATM-BR-027, OATM-BR-028, OATM-BR-029, OATM-BR-030, OATM-BR-031, OATM-BR-033. After: OATM-C03-T2.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - text "Account group (optional)"
  - money "Credit limit": Required: 'Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Credit Limit is not valid'; negative and zero amounts are accepted.
  - money "Cash credit limit": Required: 'Cash Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Cash Credit Limit is not valid'; negative and zero amounts are accepted.
  - money "Current balance": Required: 'Current Balance must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Balance is not valid'; negative and zero amounts are accepted.
  - money "Current cycle credit": Required: 'Current Cycle Credit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Cycle Credit Limit is not valid'; negative and zero amounts are accepted.
  - money "Current cycle debit": Required: 'Current Cycle Debit Limit must be supplied.'; must be a valid amount, for example -1,250.00 or 5000: 'Current Cycle Debit Limit is not valid'; negative and zero amounts are accepted.
  - display "Customer ID"
  - date "Date of birth": Year, month and day must all be supplied: 'Date of Birth : Year must be supplied.', 'Date of Birth : Month must be supplied.', 'Date of Birth : Day must be supplied.'. The year must be 4 digits: 'Date of Birth must be 4 digit number.', starting 19 or 20: 'Date of Birth : Century is not valid.'. 'Date of Birth: Month must be a number between 1 and 12.'; 'Date of Birth:day must be a number between 1 and 31.'; 'Date of Birth:Cannot have 31 days in this month.'; 'Date of Birth:Cannot have 30 days in this month.'; 'Date of Birth:Not a leap year.Cannot have 29 days in this month.'; the date must be a real calendar date: 'Date of Birth validation error ...'. Must be before today: 'Date of Birth:cannot be in the future '.
  - display "Country"
  - text "Government-issued ID reference"
- [ ] OATM-C03-T4 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032. Criteria: OATM-C03-AC-01, OATM-C03-AC-02, OATM-C03-AC-03, OATM-C03-AC-04, OATM-C03-AC-05, OATM-C03-AC-06, OATM-C03-AC-07, OATM-C03-AC-08, OATM-C03-AC-09, OATM-C03-AC-10, OATM-C03-AC-11, OATM-C03-AC-12, OATM-C03-AC-13, OATM-C03-AC-14, OATM-C03-AC-15. After: OATM-C03-T1, OATM-C03-T2, OATM-C03-T3.
  - 15 acceptance criteria, each a test named by its ID.
- [ ] OATM-C03-T5 [compliance] Review the handling of money, personal data. Requirements: OATM-REQ-F-025, OATM-REQ-F-026, OATM-REQ-F-027, OATM-REQ-F-028, OATM-REQ-F-029, OATM-REQ-F-030, OATM-REQ-F-031, OATM-REQ-F-032. After: OATM-C03-T1, OATM-C03-T2, OATM-C03-T3.
  - Check storage, logs, screens and audit against the rules.
