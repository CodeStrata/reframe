# Feature specification: Validate changed account and customer fields

**Feature:** OATM-C04 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C04)

As an operator, I want every changed account and customer field checked before I can confirm, so that only valid details are saved.

Checks every changed account and customer field before the operator may confirm the update: flags, dates, amounts, SSN, FICO score, names and address. Changes may be confirmed only when every check passes. Invalid details must never be saved, and only the first error found is shown.

**Acceptance scenarios:**

1. **Given** changed field: credit limit 5000.00 to 7000.00, **when** account details have been fetched and the entered values differ from the fetched ones, and the changes are not already validated or saved, **then** All fields are checked; if any fail, the stage becomes 'E' and the screen asks for corrections (OATM-C04-AC-01)
2. **Given** Changes made: credit limit changed from 5000.00 to 6000.00, **when** the operator has changed a fetched account and the changes are not yet confirmed, **then** Status, open/expiry/reissue dates and all five amounts are checked before the change can be confirmed (OATM-C04-AC-02)
3. **Given** Changes made: none, **when** the operator has changed a fetched account and the changes are not yet confirmed, **then** No field checks run (OATM-C04-AC-03)
4. **Given** account status: X, **when** Account Update validation runs, **then** Rejected; the account status must be Y or N (OATM-C04-AC-04)
5. **Given** expiry date: 2025-13-01, **when** Account Update validation runs, **then** Rejected as an invalid date (OATM-C04-AC-05)
6. **Given** Cash credit limit entered: -100, **when** Account Update validation runs, **then** Accepted as -100.00 (OATM-C04-AC-06)
7. **Given** Credit limit entered: 12a; Current balance entered: (blank), **when** Account Update validation runs, **then** Only 'Credit Limit is not valid' is shown (OATM-C04-AC-07)
8. **Given** SSN: 666-12-3456, **when** Account Update validation runs, **then** Rejected with ': should not be 000, 666, or between 900 and 999' (OATM-C04-AC-08)
9. **Given** FICO score: 900, **when** Account Update validation runs, **then** Rejected with ': should be between 300 and 850' (OATM-C04-AC-09)
10. **Given** first name: J0hn, **when** Account Update validation runs, **then** Rejected because the name contains a digit (OATM-C04-AC-10)
11. **Given** middle name: (blank), **when** Account Update validation runs, **then** Accepted (OATM-C04-AC-11)
12. **Given** state: ZZ, **when** Account Update validation runs, **then** Rejected with ': is not a valid state code' (OATM-C04-AC-12)
13. **Given** EFT account id: 12345, **when** Account Update validation runs, **then** Rejected because 10 digits are required (OATM-C04-AC-13)
14. **Given** all changed fields: valid, **when** all field checks pass, **then** Stage 'N'; the screen prompts 'Changes validated.Press F5 to save' (OATM-C04-AC-14)
15. **Given** an account is shown for update and the operator has changed a field, **when** the operator clears the Credit Limit (or enters '*') and submits, **then** the change is rejected with 'Credit Limit must be supplied.' and the update does not move to awaiting confirmation (OATM-C04-AC-15)
16. **Given** an account is shown for update and the operator has changed a field, **when** the operator leaves the Cash Credit Limit blank and submits, **then** the change is rejected with 'Cash Credit Limit must be supplied.' (OATM-C04-AC-16)
17. **Given** an account is shown for update, **when** the operator enters 'ABC' as the Current Balance and submits, **then** the change is rejected with 'Current Balance is not valid' (OATM-C04-AC-17)
18. **Given** an account is shown for update, **when** the operator enters '12x.50' as the current cycle credit and submits, **then** the change is rejected with 'Current Cycle Credit Limit is not valid'; an invalid current cycle debit is rejected the same way with 'Current Cycle Debit Limit is not valid' (OATM-C04-AC-18)

## Requirements

### Functional requirements

- **OATM-REQ-F-033** (business rule): When account details have been fetched and the entered values differ from the fetched ones, and the changes are not already validated or saved, the system shall check every account and customer field and mark the changes not OK ('E') until all checks pass. Rules: OATM-BR-034, OATM-BR-035.
- **OATM-REQ-F-034** (business rule): The system shall require the account status and the primary card holder flag to be Y or N. Rules: OATM-BR-036, OATM-BR-035.
- **OATM-REQ-F-035** (business rule): The system shall require the open, expiry, reissue and birth dates to be valid dates, with the birth date passing an extra date-of-birth check. Rules: OATM-BR-036, OATM-BR-035.
- **OATM-REQ-F-036** (business rule): The system shall require the credit limit, cash credit limit, current balance, cycle credit and cycle debit to be valid signed currency numbers. Rules: OATM-BR-036, OATM-BR-035.
- **OATM-REQ-F-037** (business rule): If an amount is not supplied (blank or '*'), then the system shall reject it with the message '<field> must be supplied.' (for example 'Credit Limit must be supplied.'). Rules: OATM-BR-037.
- **OATM-REQ-F-038** (business rule): If a supplied amount is not a valid currency number, then the system shall reject it with the message '<field> is not valid', using the names 'Credit Limit', 'Cash Credit Limit', 'Current Balance', 'Current Cycle Credit Limit' or 'Current Cycle Debit Limit'. Rules: OATM-BR-038.
- **OATM-REQ-F-039** (business rule): The system shall accept any valid currency number for the five amounts, including negative values and zero, without a range or sign check. Rules: OATM-BR-039.
- **OATM-REQ-F-040** (business rule): If the first 3 digits of the SSN are 000, 666 or 900-999, then the system shall reject the SSN with ': should not be 000, 666, or between 900 and 999'. Rules: OATM-BR-040.
- **OATM-REQ-F-041** (business rule): The system shall require the FICO score to be 3 digits between 300 and 850, rejecting it otherwise with ': should be between 300 and 850'. Rules: OATM-BR-040.
- **OATM-REQ-F-042** (business rule): The system shall require the first and last names (25 characters), city (50) and country (3) to be letters only, allow the middle name (25) to be blank but letters only, and require address line 1 (50). Rules: OATM-BR-041.
- **OATM-REQ-F-043** (business rule): The system shall require the state to be a valid 2-letter US state code (': is not a valid state code'), the ZIP to be 5 digits, the state and ZIP to match each other, both phone numbers to be valid US numbers, and the EFT account id to be 10 digits. Rules: OATM-BR-042.
- **OATM-REQ-N-003** (business rule): The system shall show only the first error message found on the screen. Rules: OATM-BR-039.
- **OATM-REQ-F-044** (business rule): When all field checks pass, the system shall set the stage to changes validated but not confirmed ('N'). Rules: OATM-BR-043.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-034 | Validate each changed account field | business rule | WHEN account details have been fetched and the entered values differ from the fetched ones, and the changes are not already validated or saved, THE Account Update validation SHALL check every account and customer field and mark the changes not OK ('E') until all checks pass. | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-035 | Validate account status, dates and amounts | business rule | WHEN the operator has changed a fetched account and the changes are not yet confirmed, THE Account Update validation SHALL mark the changes as not OK ('E') and check the account status as Y/N, the open, expiry and reissue dates as calendar dates, and the five amounts as signed currency numbers. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-036 | Validate each changed account field | business rule | THE Account Update validation SHALL require the account status and the primary card holder flag to be Y or N; the open, expiry, reissue and birth dates to be valid dates, with the birth date passing an extra date-of-birth check; and the credit limit, cash credit limit, current balance, cycle credit and cycle debit to be valid signed amounts. | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-037 | Validate signed monetary amount | business rule | WHEN an amount is not supplied (blank or '*'), THE Account Update validation SHALL reject it with the message '<field> must be supplied.' (for example 'Credit Limit must be supplied.'). | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-038 | Validate signed monetary amount | business rule | WHEN a supplied amount is not a valid currency number, THE Account Update validation SHALL reject it with the message '<field> is not valid', using the names 'Credit Limit', 'Cash Credit Limit', 'Current Balance', 'Current Cycle Credit Limit' or 'Current Cycle Debit Limit'. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-039 | Validate signed monetary amount | business rule | THE Account Update validation SHALL accept any valid currency number for the five amounts, including negative values and zero, without a range or sign check, and SHALL show only the first error message found on the screen. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-040 | Validate each changed account field | business rule | THE Account Update validation SHALL reject an SSN whose first 3 digits are 000, 666 or 900-999 (': should not be 000, 666, or between 900 and 999'), and SHALL require the FICO score to be 3 digits between 300 and 850 (': should be between 300 and 850'). | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-041 | Validate each changed account field | business rule | THE Account Update validation SHALL require the first and last names (25 characters), city (50) and country (3) to be letters only; allow the middle name (25) to be blank but letters only; and require address line 1 (50). | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-042 | Validate each changed account field | business rule | THE Account Update validation SHALL require the state to be a valid 2-letter US state code (': is not a valid state code'), the ZIP to be 5 digits, the state and ZIP to match each other, both phone numbers to be valid US numbers, and the EFT account id to be 10 digits. | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |
| OATM-BR-043 | Validate each changed account field | business rule | WHEN all field checks pass, THE Account Update validation SHALL set the stage to changes validated but not confirmed ('N'). | medium | app/cbl/COACTUPC.cbl:1429-1475, app/cbl/COACTUPC.cbl:1476-1676, app/cbl/COACTUPC.cbl:2431-2531 |

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

- SME-057: Please supply the complete, authoritative list of valid general-purpose phone area codes. Today it is described only as running from '201' to '989'. (Data governance team) On OATM-BR-038.
- SME-063: At present, a phone number counts as 'not supplied' when the area code and exchange are blank, even if a line number was entered. Is that intended, or should a phone count as not supplied only when all three parts are blank? (Business analyst) On OATM-BR-038.
- SME-064: Should the second and third parts of a social security number be validated only when the first part is valid, or always? (Business analyst) On OATM-BR-038.
- DEF-011: Confirm this is deliberate: The amount check accepts any signed currency number, so a negative or zero credit limit, cash credit limit or cycle amount passes validation and can be saved. (Subject-matter expert) On OATM-BR-035, OATM-BR-038, OATM-BR-039.
- DEF-113: Confirm this is deliberate: The SSN middle and last parts, the government id and address line 2 get no content check beyond the SSN edit, and address line 2 is deliberately left optional. (Subject-matter expert) On OATM-BR-043.

### Decision table gaps

- Validation stage: No rule says what happens when the operator submits without changing any value.
