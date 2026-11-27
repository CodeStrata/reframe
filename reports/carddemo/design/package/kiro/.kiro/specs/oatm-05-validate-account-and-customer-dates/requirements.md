# Requirements: Validate account and customer dates (OATM-C05)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Checks the account open, expiry and reissue dates and the customer's date of birth, part by part and then as real calendar dates, whenever the operator changes account or customer details. Impossible dates (such as 31 April, 30 February or 29 February in a non-leap year) and years outside 19xx/20xx must never be saved. Each problem is reported with the date's name in the message.

**User story:** As an operator, I want the open, expiry, reissue and birth dates checked part by part and as real calendar dates, so that impossible dates are never saved.

## Requirements

### Requirement 1: OATM-REQ-F-045 (business rule)

#### Acceptance criteria

1. When the entered values differ from the stored account and are not awaiting or past confirmation, the system shall check the 'Open Date', 'Expiry Date', 'Reissue Date' and 'Date of Birth' in that order with the same date check, prefix each message with the date's name, and show only the first error message found. (rules OATM-BR-044)
2. GIVEN Changes: none compared with stored data WHEN the entered values differ from the stored account and are not awaiting or past confirmation THEN No date is checked. (OATM-C05-AC-01; OATM-BR-044)

### Requirement 2: OATM-REQ-F-046 (business rule)

#### Acceptance criteria

1. If the year of a date is blank, then the system shall reject the date with '<date name> : Year must be supplied.' and still go on to check the month and day. (rules OATM-BR-045)
2. GIVEN an account is shown for update with changes WHEN the operator leaves the Open Date year blank, enters month '13' and day '05', and submits THEN the date is rejected with 'Open Date : Year must be supplied.', and the month and day are still checked, so the month is also flagged in error (OATM-C05-AC-08; OATM-BR-045)

### Requirement 3: OATM-REQ-F-047 (business rule)

#### Acceptance criteria

1. If the year of a date is not a four-digit number, then the system shall reject the date with '<date name> must be 4 digit number.' (rules OATM-BR-046)
2. GIVEN an account is shown for update with changes WHEN the operator enters Expiry Date year '25' and submits THEN the date is rejected with 'Expiry Date must be 4 digit number.' (OATM-C05-AC-09; OATM-BR-046)

### Requirement 4: OATM-REQ-F-048 (business rule)

#### Acceptance criteria

1. If a numeric year does not start with 19 or 20, then the system shall reject the date with '<date name> : Century is not valid.' (rules OATM-BR-047)
2. GIVEN Expiry Date: 1999-12-31 WHEN a numeric year does not start with 19 or 20 THEN The year passes. (OATM-C05-AC-02; OATM-BR-047)

### Requirement 5: OATM-REQ-F-049 (business rule)

#### Acceptance criteria

1. If the month of a date is blank, then the system shall reject the date with '<date name> : Month must be supplied.' (rules OATM-BR-048)
2. GIVEN an account is shown for update with changes WHEN the operator enters Reissue Date year '2024', leaves the month blank, and submits THEN the date is rejected with 'Reissue Date : Month must be supplied.' (OATM-C05-AC-10; OATM-BR-048)

### Requirement 6: OATM-REQ-F-050 (business rule)

#### Acceptance criteria

1. If the month of a date is not a number from 1 to 12, then the system shall reject the date with '<date name>: Month must be a number between 1 and 12.' (rules OATM-BR-049)
2. GIVEN an account is shown for update with changes WHEN the operator enters Open Date 2024 / 13 / 01 and submits THEN the date is rejected with 'Open Date: Month must be a number between 1 and 12.' (OATM-C05-AC-11; OATM-BR-049)

### Requirement 7: OATM-REQ-F-051 (business rule)

#### Acceptance criteria

1. If the day of a date is blank, then the system shall reject the date with '<date name> : Day must be supplied.' (rules OATM-BR-050)
2. GIVEN an account is shown for update with changes WHEN the operator enters Expiry Date 2026 / 05 with the day blank and submits THEN the date is rejected with 'Expiry Date : Day must be supplied.' (OATM-C05-AC-12; OATM-BR-050)

### Requirement 8: OATM-REQ-F-052 (business rule)

#### Acceptance criteria

1. If the day of a date is not a number or is outside 1 to 31, then the system shall reject the date with '<date name>:day must be a number between 1 and 31.' (rules OATM-BR-051)
2. GIVEN an account is shown for update with changes WHEN the operator enters Open Date 2024 / 05 / 32 and submits (or day 'AB') THEN the date is rejected with 'Open Date:day must be a number between 1 and 31.' (OATM-C05-AC-13; OATM-BR-051)

### Requirement 9: OATM-REQ-F-053 (business rule)

#### Acceptance criteria

1. If the day is 31 and the month is not 1, 3, 5, 7, 8, 10 or 12, then the system shall reject the date with '<date name>:Cannot have 31 days in this month.' and stop checking that date. (rules OATM-BR-052)
2. GIVEN an account is shown for update with changes WHEN the operator enters Reissue Date 2024 / 04 / 31 and submits THEN the date is rejected with 'Reissue Date:Cannot have 31 days in this month.' and no further check is made on that date (OATM-C05-AC-14; OATM-BR-052)

### Requirement 10: OATM-REQ-F-054 (business rule)

#### Acceptance criteria

1. If the date is 30 February, then the system shall reject it with '<date name>:Cannot have 30 days in this month.' and stop checking that date. (rules OATM-BR-053)
2. GIVEN an account is shown for update with changes WHEN the operator enters Open Date 2024 / 02 / 30 and submits THEN the date is rejected with 'Open Date:Cannot have 30 days in this month.' and no further check is made on that date (OATM-C05-AC-15; OATM-BR-053)

### Requirement 11: OATM-REQ-F-055 (business rule)

#### Acceptance criteria

1. If the date is 29 February and the year is not a leap year (a year ending in 00 must divide by 400, any other year by 4), then the system shall reject it with '<date name>:Not a leap year.Cannot have 29 days in this month.' (rules OATM-BR-054)
2. GIVEN Open Date: 2024-02-29 WHEN the date is 29 February and the year is not a leap year (a year ending in 00 must divide by 400, any other year by 4) THEN Accepted. (OATM-C05-AC-03; OATM-BR-054)
3. GIVEN Open Date: 1900-02-29 WHEN the date is 29 February and the year is not a leap year (a year ending in 00 must divide by 400, any other year by 4) THEN Rejected as not a leap year; 2000-02-29 is accepted. (OATM-C05-AC-04; OATM-BR-054)

### Requirement 12: OATM-REQ-F-056 (business rule)

#### Acceptance criteria

1. If any of the year, month or day of a date has failed its check, then the system shall stop checking that date without the final date-service check. (rules OATM-BR-055)
2. GIVEN Expiry Date: 2024-13-01 WHEN any of the year, month or day of a date has failed its check THEN The month error is raised and the date service is not called. (OATM-C05-AC-05; OATM-BR-055)

### Requirement 13: OATM-REQ-F-057 (business rule)

#### Acceptance criteria

1. When a date passes all the earlier checks, the system shall confirm it with the date service (CSUTLDTC) in format 'YYYYMMDD' and reject it with '<date name> validation error Sev code: <severity> Message code: <message number>' if the service returns a non-zero severity. (rules OATM-BR-056)
2. GIVEN Open Date: 2024-02-29; Date service severity: 0 WHEN a date passes all the earlier checks THEN The date is accepted. (OATM-C05-AC-06; OATM-BR-056)

### Requirement 14: OATM-REQ-F-058 (error handling)

#### Acceptance criteria

1. When the date service rejects a date, the system shall still mark the date's year, month and day as valid, so that only the error message and the screen's input-error state record the failure. (rules OATM-BR-057)
2. GIVEN Date of Birth: a date the date service rejects WHEN the date service rejects a date THEN The error message is set, but the date counts as valid, so the future-birth-date check still runs on it. (OATM-C05-AC-07; OATM-BR-057)
