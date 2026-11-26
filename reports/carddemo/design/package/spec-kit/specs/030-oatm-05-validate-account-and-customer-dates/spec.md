# Feature specification: Validate account and customer dates

**Feature:** OATM-C05 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C05)

As an operator, I want the open, expiry, reissue and birth dates checked part by part and as real calendar dates, so that impossible dates are never saved.

Checks the open, expiry, reissue and birth dates part by part and then as real calendar dates whenever the operator changes account details. Each message names the date it concerns and only the first error is shown. Impossible dates such as 31 April, 30 February or 29 February in a non-leap year must never be saved.

**Acceptance scenarios:**

1. **Given** Changes: none compared with stored data, **when** the entered values differ from the stored account and are not awaiting or past confirmation, **then** No date is checked. (OATM-C05-AC-01)
2. **Given** Expiry Date: 1999-12-31, **when** a numeric year does not start with 19 or 20, **then** The year passes. (OATM-C05-AC-02)
3. **Given** Open Date: 2024-02-29, **when** the date is 29 February and the year is not a leap year (a year ending in 00 must divide by 400, any other year by 4), **then** Accepted. (OATM-C05-AC-03)
4. **Given** Open Date: 1900-02-29, **when** the date is 29 February and the year is not a leap year (a year ending in 00 must divide by 400, any other year by 4), **then** Rejected as not a leap year; 2000-02-29 is accepted. (OATM-C05-AC-04)
5. **Given** Expiry Date: 2024-13-01, **when** any of the year, month or day of a date has failed its check, **then** The month error is raised and the date service is not called. (OATM-C05-AC-05)
6. **Given** Open Date: 2024-02-29; Date service severity: 0, **when** a date passes all the earlier checks, **then** The date is accepted. (OATM-C05-AC-06)
7. **Given** Date of Birth: a date the date service rejects, **when** the date service rejects a date, **then** The error message is set, but the date counts as valid, so the future-birth-date check still runs on it. (OATM-C05-AC-07)
8. **Given** a changed account where the Open Date year is blank, month is 13 and day is 01, **when** the dates are validated, **then** the date is rejected with 'Open Date : Year must be supplied.' and the month and day are still checked, so the month is also flagged in error (OATM-C05-AC-08)
9. **Given** a changed account where the Expiry Date year is entered as '20A5', **when** the dates are validated, **then** the date is rejected with 'Expiry Date must be 4 digit number.' (OATM-C05-AC-09)
10. **Given** a changed account where the Reissue Date year is 2024, month is blank and day is 15, **when** the dates are validated, **then** the date is rejected with 'Reissue Date : Month must be supplied.' (OATM-C05-AC-10)
11. **Given** a changed account where the Open Date is year 2024, month 13, day 01, **when** the dates are validated, **then** the date is rejected with 'Open Date: Month must be a number between 1 and 12.' (OATM-C05-AC-11)
12. **Given** a changed account where the Open Date month is entered as 'AB', **when** the dates are validated, **then** the date is rejected with 'Open Date: Month must be a number between 1 and 12.' (OATM-C05-AC-12)
13. **Given** a changed account where the Date of Birth is year 1980, month 06 and day blank, **when** the dates are validated, **then** the date is rejected with 'Date of Birth : Day must be supplied.' (OATM-C05-AC-13)
14. **Given** a changed account where the Expiry Date is year 2026, month 05, day 32, **when** the dates are validated, **then** the date is rejected with 'Expiry Date:day must be a number between 1 and 31.' (OATM-C05-AC-14)
15. **Given** a changed account where the Expiry Date day is entered as 'XX', **when** the dates are validated, **then** the date is rejected with 'Expiry Date:day must be a number between 1 and 31.' (OATM-C05-AC-15)
16. **Given** a changed account where the Open Date is year 2024, month 04, day 31, **when** the dates are validated, **then** the date is rejected with 'Open Date:Cannot have 31 days in this month.' and no further checks are made on the Open Date (OATM-C05-AC-16)
17. **Given** a changed account where the Open Date is year 2024, month 07, day 31, **when** the dates are validated, **then** the 31-day check does not reject the Open Date (OATM-C05-AC-17)
18. **Given** a changed account where the Reissue Date is year 2024, month 02, day 30, **when** the dates are validated, **then** the date is rejected with 'Reissue Date:Cannot have 30 days in this month.' and no further checks are made on the Reissue Date (OATM-C05-AC-18)

## Requirements

### Functional requirements

- **OATM-REQ-F-045** (business rule): When the entered values differ from the stored account and are not awaiting or past confirmation, the system shall check the 'Open Date', 'Expiry Date', 'Reissue Date' and 'Date of Birth' in that order with the same date check, prefix each message with the date's name, and show only the first error message found. Rules: OATM-BR-044.
- **OATM-REQ-F-046** (business rule): If the year of a date is blank, then the system shall reject the date with '<date name> : Year must be supplied.' and still go on to check the month and day. Rules: OATM-BR-045.
- **OATM-REQ-F-047** (business rule): If the year of a date is not a four-digit number, then the system shall reject the date with '<date name> must be 4 digit number.' Rules: OATM-BR-046.
- **OATM-REQ-F-048** (business rule): If a numeric year does not start with 19 or 20, then the system shall reject the date with '<date name> : Century is not valid.' Rules: OATM-BR-047.
- **OATM-REQ-F-049** (business rule): If the month of a date is blank, then the system shall reject the date with '<date name> : Month must be supplied.' Rules: OATM-BR-048.
- **OATM-REQ-F-050** (business rule): If the month of a date is not a number from 1 to 12, then the system shall reject the date with '<date name>: Month must be a number between 1 and 12.' Rules: OATM-BR-049.
- **OATM-REQ-F-051** (business rule): If the day of a date is blank, then the system shall reject the date with '<date name> : Day must be supplied.' Rules: OATM-BR-050.
- **OATM-REQ-F-052** (business rule): If the day of a date is not a number or is outside 1 to 31, then the system shall reject the date with '<date name>:day must be a number between 1 and 31.' Rules: OATM-BR-051.
- **OATM-REQ-F-053** (business rule): If the day is 31 and the month is not 1, 3, 5, 7, 8, 10 or 12, then the system shall reject the date with '<date name>:Cannot have 31 days in this month.' and stop checking that date. Rules: OATM-BR-052.
- **OATM-REQ-F-054** (business rule): If the date is 30 February, then the system shall reject it with '<date name>:Cannot have 30 days in this month.' and stop checking that date. Rules: OATM-BR-053.
- **OATM-REQ-F-055** (business rule): If the date is 29 February and the year is not a leap year (a year ending in 00 must divide by 400, any other year by 4), then the system shall reject it with '<date name>:Not a leap year.Cannot have 29 days in this month.' Rules: OATM-BR-054.
- **OATM-REQ-F-056** (business rule): If any of the year, month or day of a date has failed its check, then the system shall stop checking that date without the final date-service check. Rules: OATM-BR-055.
- **OATM-REQ-F-057** (business rule): When a date passes all the earlier checks, the system shall confirm it with the date service (CSUTLDTC) in format 'YYYYMMDD' and reject it with '<date name> validation error Sev code: <severity> Message code: <message number>' if the service returns a non-zero severity. Rules: OATM-BR-056.
- **OATM-REQ-F-058** (error handling): When the date service rejects a date, the system shall still mark the date's year, month and day as valid, so that only the error message and the screen's input-error state record the failure. Rules: OATM-BR-057.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-044 | Validate the four account and customer dates | business rule | WHEN the entered values differ from the stored account and are not awaiting or past confirmation, THE Account Update validation SHALL check the 'Open Date', 'Expiry Date', 'Reissue Date' and 'Date of Birth' in that order with the same date check, prefix each message with the date's name, and show only the first error message found. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-045 | Reject missing date year | business rule | WHEN the year of a date is blank, THE Date Validation SHALL reject the date with '<date name> : Year must be supplied.' and still go on to check the month and day. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-046 | Reject non-numeric date year | business rule | WHEN the year of a date is not a four-digit number, THE Date Validation SHALL reject the date with '<date name> must be 4 digit number.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-047 | Restrict date century to 19 or 20 | business rule | WHEN a numeric year does not start with 19 or 20, THE Date Validation SHALL reject the date with '<date name> : Century is not valid.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-048 | Reject missing date month | business rule | WHEN the month of a date is blank, THE Date Validation SHALL reject the date with '<date name> : Month must be supplied.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-049 | Reject month outside 1 to 12 | business rule | WHEN the month of a date is not a number from 1 to 12, THE Date Validation SHALL reject the date with '<date name>: Month must be a number between 1 and 12.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-050 | Reject missing date day | business rule | WHEN the day of a date is blank, THE Date Validation SHALL reject the date with '<date name> : Day must be supplied.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-051 | Reject non-numeric date day | business rule | WHEN the day of a date is not a number or is outside 1 to 31, THE Date Validation SHALL reject the date with '<date name>:day must be a number between 1 and 31.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-052 | Reject day 31 in short months | business rule | WHEN the day is 31 and the month is not 1, 3, 5, 7, 8, 10 or 12, THE Date Validation SHALL reject the date with '<date name>:Cannot have 31 days in this month.' and stop checking that date. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-053 | Reject day 30 in February | business rule | WHEN the date is 30 February, THE Date Validation SHALL reject it with '<date name>:Cannot have 30 days in this month.' and stop checking that date. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-054 | Reject February 29 in non-leap years | business rule | WHEN the date is 29 February and the year is not a leap year (a year ending in 00 must divide by 400, any other year by 4), THE Date Validation SHALL reject it with '<date name>:Not a leap year.Cannot have 29 days in this month.' | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-055 | Stop date check on prior failures | business rule | WHEN any of the year, month or day of a date has failed its check, THE Date Validation SHALL stop checking that date without the final date-service check. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-056 | Verify date with date utility | business rule | WHEN a date passes all the earlier checks, THE Date Validation SHALL confirm it with the date service (CSUTLDTC) in format 'YYYYMMDD', and SHALL reject it with '<date name> validation error Sev code: <severity> Message code: <message number>' if the service returns a non-zero severity. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-057 | Confirm date with date utility | error handling | WHEN the date service rejects a date, THE Date Validation SHALL still mark the date's year, month and day as valid afterwards, so only the error message and the screen's input-error state record the failure. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSLKPCDY (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDPY (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-059: When the date-checking utility rejects a date, the date is still marked valid even though an input error is raised. Should a rejected date stay invalid, including for later checks such as 'date of birth cannot be in the future'? (Account servicing business owner) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-044, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051.
- SME-060: Should date validation check that the month is numeric before checking that it is between 1 and 12? (Account servicing business owner) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051.
- SME-061: Only years in the 1900s and 2000s are accepted for all four account and customer dates. Should this restriction still apply to card expiry and reissue dates? (Account servicing business owner) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051.
- SME-065: When a date's year fails validation, should the whole date check stop, or should the month and day still be checked? (Business analyst) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-044, OATM-BR-047, OATM-BR-049, OATM-BR-051.
- DEF-036: Is this intended? When the date service returns a non-zero severity, the check jumps to the end of the final-check paragraph (EDIT-DATE-LE-EXIT). It then runs on into the statement that marks the whole date valid (WS-EDIT-DATE-IS-VALID). The rejected date's year, month and day flags are therefore reset to valid, the field is not marked as in error, and for Date of Birth the future-date check still runs. The input-error state and the message do stay set. (Subject-matter expert) On OATM-BR-052, OATM-BR-053, OATM-BR-054, OATM-BR-055, OATM-BR-056, OATM-BR-057, OATM-BR-044, OATM-BR-045, OATM-BR-046, OATM-BR-047, OATM-BR-048, OATM-BR-049, OATM-BR-050, OATM-BR-051.

### Decision table gaps

- Date part checks: R53 says checking continues after a blank year; no rule says whether month and day are still checked after the other year, month or day failures.
- Date part checks: The extra date-of-birth check named in R10 is not described by any rule.
