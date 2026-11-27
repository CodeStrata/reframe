# Requirements: Validate changed account and customer fields (OATM-C04)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Checks every changed account and customer field before the operator may confirm the update: flags, dates, amounts, SSN, FICO score, names and address. Changes may be confirmed only when every check passes. Invalid details must never be saved, and only the first error found is shown.

**User story:** As an operator, I want every changed account and customer field checked before I can confirm, so that only valid details are saved.

## Requirements

### Requirement 1: OATM-REQ-F-033 (business rule)

#### Acceptance criteria

1. When account details have been fetched and the entered values differ from the fetched ones, and the changes are not already validated or saved, the system shall check every account and customer field and mark the changes not OK ('E') until all checks pass. (rules OATM-BR-034, OATM-BR-035)
2. GIVEN changed field: credit limit 5000.00 to 7000.00 WHEN account details have been fetched and the entered values differ from the fetched ones, and the changes are not already validated or saved THEN All fields are checked; if any fail, the stage becomes 'E' and the screen asks for corrections (OATM-C04-AC-01; OATM-BR-034)
3. GIVEN Changes made: credit limit changed from 5000.00 to 6000.00 WHEN the operator has changed a fetched account and the changes are not yet confirmed THEN Status, open/expiry/reissue dates and all five amounts are checked before the change can be confirmed (OATM-C04-AC-02; OATM-BR-035)
4. GIVEN Changes made: none WHEN the operator has changed a fetched account and the changes are not yet confirmed THEN No field checks run (OATM-C04-AC-03; OATM-BR-035)

### Requirement 2: OATM-REQ-F-034 (business rule)

#### Acceptance criteria

1. The system shall require the account status and the primary card holder flag to be Y or N. (rules OATM-BR-036, OATM-BR-035)
2. GIVEN Changes made: credit limit changed from 5000.00 to 6000.00 WHEN the operator has changed a fetched account and the changes are not yet confirmed THEN Status, open/expiry/reissue dates and all five amounts are checked before the change can be confirmed (OATM-C04-AC-02; OATM-BR-035)
3. GIVEN Changes made: none WHEN the operator has changed a fetched account and the changes are not yet confirmed THEN No field checks run (OATM-C04-AC-03; OATM-BR-035)
4. GIVEN account status: X WHEN Account Update validation runs THEN Rejected; the account status must be Y or N (OATM-C04-AC-04; OATM-BR-036)
5. GIVEN expiry date: 2025-13-01 WHEN Account Update validation runs THEN Rejected as an invalid date (OATM-C04-AC-05; OATM-BR-036)

### Requirement 3: OATM-REQ-F-035 (business rule)

#### Acceptance criteria

1. The system shall require the open, expiry, reissue and birth dates to be valid dates, with the birth date passing an extra date-of-birth check. (rules OATM-BR-036, OATM-BR-035)
2. GIVEN Changes made: credit limit changed from 5000.00 to 6000.00 WHEN the operator has changed a fetched account and the changes are not yet confirmed THEN Status, open/expiry/reissue dates and all five amounts are checked before the change can be confirmed (OATM-C04-AC-02; OATM-BR-035)
3. GIVEN Changes made: none WHEN the operator has changed a fetched account and the changes are not yet confirmed THEN No field checks run (OATM-C04-AC-03; OATM-BR-035)
4. GIVEN account status: X WHEN Account Update validation runs THEN Rejected; the account status must be Y or N (OATM-C04-AC-04; OATM-BR-036)
5. GIVEN expiry date: 2025-13-01 WHEN Account Update validation runs THEN Rejected as an invalid date (OATM-C04-AC-05; OATM-BR-036)

### Requirement 4: OATM-REQ-F-036 (business rule)

#### Acceptance criteria

1. The system shall require the credit limit, cash credit limit, current balance, cycle credit and cycle debit to be valid signed currency numbers. (rules OATM-BR-036, OATM-BR-035)
2. GIVEN Changes made: credit limit changed from 5000.00 to 6000.00 WHEN the operator has changed a fetched account and the changes are not yet confirmed THEN Status, open/expiry/reissue dates and all five amounts are checked before the change can be confirmed (OATM-C04-AC-02; OATM-BR-035)
3. GIVEN Changes made: none WHEN the operator has changed a fetched account and the changes are not yet confirmed THEN No field checks run (OATM-C04-AC-03; OATM-BR-035)
4. GIVEN account status: X WHEN Account Update validation runs THEN Rejected; the account status must be Y or N (OATM-C04-AC-04; OATM-BR-036)
5. GIVEN expiry date: 2025-13-01 WHEN Account Update validation runs THEN Rejected as an invalid date (OATM-C04-AC-05; OATM-BR-036)

### Requirement 5: OATM-REQ-F-037 (business rule)

#### Acceptance criteria

1. If an amount is not supplied (blank or '*'), then the system shall reject it with the message '<field> must be supplied.' (for example 'Credit Limit must be supplied.'). (rules OATM-BR-037)
2. GIVEN an account is shown for update and the operator has changed a field WHEN the operator clears the Credit Limit (or enters '*') and submits THEN the change is rejected with 'Credit Limit must be supplied.' and the update does not move to awaiting confirmation (OATM-C04-AC-15; OATM-BR-037)
3. GIVEN an account is shown for update and the operator has changed a field WHEN the operator leaves the Cash Credit Limit blank and submits THEN the change is rejected with 'Cash Credit Limit must be supplied.' (OATM-C04-AC-16; OATM-BR-037)

### Requirement 6: OATM-REQ-F-038 (business rule)

#### Acceptance criteria

1. If a supplied amount is not a valid currency number, then the system shall reject it with the message '<field> is not valid', using the names 'Credit Limit', 'Cash Credit Limit', 'Current Balance', 'Current Cycle Credit Limit' or 'Current Cycle Debit Limit'. (rules OATM-BR-038)
2. GIVEN an account is shown for update WHEN the operator enters 'ABC' as the Current Balance and submits THEN the change is rejected with 'Current Balance is not valid' (OATM-C04-AC-17; OATM-BR-038)
3. GIVEN an account is shown for update WHEN the operator enters '12x.50' as the current cycle credit and submits THEN the change is rejected with 'Current Cycle Credit Limit is not valid'; an invalid current cycle debit is rejected the same way with 'Current Cycle Debit Limit is not valid' (OATM-C04-AC-18; OATM-BR-038)

### Requirement 7: OATM-REQ-F-039 (business rule)

#### Acceptance criteria

1. The system shall accept any valid currency number for the five amounts, including negative values and zero, without a range or sign check. (rules OATM-BR-039)
2. GIVEN Cash credit limit entered: -100 WHEN Account Update validation runs THEN Accepted as -100.00 (OATM-C04-AC-06; OATM-BR-039)
3. GIVEN Credit limit entered: 12a; Current balance entered: (blank) WHEN Account Update validation runs THEN Only 'Credit Limit is not valid' is shown (OATM-C04-AC-07; OATM-BR-039)

### Requirement 8: OATM-REQ-F-040 (business rule)

#### Acceptance criteria

1. If the first 3 digits of the SSN are 000, 666 or 900-999, then the system shall reject the SSN with ': should not be 000, 666, or between 900 and 999'. (rules OATM-BR-040)
2. GIVEN SSN: 666-12-3456 WHEN Account Update validation runs THEN Rejected with ': should not be 000, 666, or between 900 and 999' (OATM-C04-AC-08; OATM-BR-040)
3. GIVEN FICO score: 900 WHEN Account Update validation runs THEN Rejected with ': should be between 300 and 850' (OATM-C04-AC-09; OATM-BR-040)

### Requirement 9: OATM-REQ-F-041 (business rule)

#### Acceptance criteria

1. The system shall require the FICO score to be 3 digits between 300 and 850, rejecting it otherwise with ': should be between 300 and 850'. (rules OATM-BR-040)
2. GIVEN SSN: 666-12-3456 WHEN Account Update validation runs THEN Rejected with ': should not be 000, 666, or between 900 and 999' (OATM-C04-AC-08; OATM-BR-040)
3. GIVEN FICO score: 900 WHEN Account Update validation runs THEN Rejected with ': should be between 300 and 850' (OATM-C04-AC-09; OATM-BR-040)

### Requirement 10: OATM-REQ-F-042 (business rule)

#### Acceptance criteria

1. The system shall require the first and last names (25 characters), city (50) and country (3) to be letters only, allow the middle name (25) to be blank but letters only, and require address line 1 (50). (rules OATM-BR-041)
2. GIVEN first name: J0hn WHEN Account Update validation runs THEN Rejected because the name contains a digit (OATM-C04-AC-10; OATM-BR-041)
3. GIVEN middle name: (blank) WHEN Account Update validation runs THEN Accepted (OATM-C04-AC-11; OATM-BR-041)

### Requirement 11: OATM-REQ-F-043 (business rule)

#### Acceptance criteria

1. The system shall require the state to be a valid 2-letter US state code (': is not a valid state code'), the ZIP to be 5 digits, the state and ZIP to match each other, both phone numbers to be valid US numbers, and the EFT account id to be 10 digits. (rules OATM-BR-042)
2. GIVEN state: ZZ WHEN Account Update validation runs THEN Rejected with ': is not a valid state code' (OATM-C04-AC-12; OATM-BR-042)
3. GIVEN EFT account id: 12345 WHEN Account Update validation runs THEN Rejected because 10 digits are required (OATM-C04-AC-13; OATM-BR-042)

### Requirement 12: OATM-REQ-N-003 (business rule)

#### Acceptance criteria

1. The system shall show only the first error message found on the screen. (rules OATM-BR-039)
2. GIVEN Cash credit limit entered: -100 WHEN Account Update validation runs THEN Accepted as -100.00 (OATM-C04-AC-06; OATM-BR-039)
3. GIVEN Credit limit entered: 12a; Current balance entered: (blank) WHEN Account Update validation runs THEN Only 'Credit Limit is not valid' is shown (OATM-C04-AC-07; OATM-BR-039)

### Requirement 13: OATM-REQ-F-044 (business rule)

#### Acceptance criteria

1. When all field checks pass, the system shall set the stage to changes validated but not confirmed ('N'). (rules OATM-BR-043)
2. GIVEN all changed fields: valid WHEN all field checks pass THEN Stage 'N'; the screen prompts 'Changes validated.Press F5 to save' (OATM-C04-AC-14; OATM-BR-043)
