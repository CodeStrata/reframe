# Validate a date against a format mask (OATM-C35)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as service · risk low

## Introduction

A shared date check used by the report date range and Add Transaction screens. It tests a 10-character date against a 10-character format mask and returns a severity, a message number and a reason such as 'Date is valid', 'Datevalue error' or 'Invalid month'. Callers treat the date as invalid when the severity is not 0000, unless the message number is 2513. Real dates must be accepted and impossible dates rejected.

**User story:** As a screen that accepts dates (report date range, transaction add), I want a date checked against its format mask with a clear result and reason, so that invalid dates are rejected with a meaningful error.

## Requirements

### Requirement 1: OATM-REQ-F-286 (design note)

#### Acceptance criteria

1. The system shall pass the caller's 10-character date and 10-character format mask to the date conversion service (CEEDAYS) and record the returned severity and message number as 4-digit values in its result. (rules OATM-BR-303)
2. GIVEN a caller supplies the date '2024-02-30' and the format mask 'YYYY-MM-DD' WHEN the date check runs THEN exactly that 10-character date and 10-character mask are what is checked, and the result records the severity and message number as 4-digit values (for a bad date value: severity 0003, message number 2508) (OATM-C35-AC-12; OATM-BR-303)

### Requirement 2: OATM-REQ-F-287 (design note)

#### Acceptance criteria

1. The system shall return an 80-character result made of the severity, 'Mesg Code:', the message number, the result text, 'TstDate:' with the tested date and 'Mask used:' with the mask, and shall set the program return code to the severity. (rules OATM-BR-304)
2. GIVEN a caller supplies the date '2024-02-30' and the format mask 'YYYY-MM-DD' WHEN the date check returns THEN the 80-character result contains, in order, the severity, 'Mesg Code:', the message number, the result text, 'TstDate:' with 2024-02-30 and 'Mask used:' with YYYY-MM-DD, and the return code equals the severity (OATM-C35-AC-13; OATM-BR-304)

### Requirement 3: OATM-REQ-F-288 (business rule)

#### Acceptance criteria

1. When the date conversion service returns an all-zero feedback token for the date and mask it was given, the system shall set the result text to 'Date is valid'. (rules OATM-BR-305)
2. GIVEN date: 2023-02-28; mask: YYYY-MM-DD WHEN the date conversion service (CEEDAYS) returns an all-zero feedback token for the 10-character date and 10-character mask it was given THEN Feedback token all zeros; result text 'Date is valid', severity '0000' (OATM-C35-AC-01; OATM-BR-305)

### Requirement 4: OATM-REQ-F-289 (business rule)

#### Acceptance criteria

1. If the date conversion service reports insufficient data (feedback X'000309CB59C3C5C5', message 2507), then the system shall set the result text to 'Insufficient'. (rules OATM-BR-306)
2. GIVEN feedback: insufficient data, severity 3, message 2507 WHEN the date conversion service reports insufficient data (feedback X'000309CB59C3C5C5', message 2507) THEN Result text 'Insufficient'; the caller treats the date as invalid (OATM-C35-AC-02; OATM-BR-306)

### Requirement 5: OATM-REQ-F-290 (business rule)

#### Acceptance criteria

1. If the date conversion service reports a bad date value (feedback X'000309CC59C3C5C5', severity 3, message 2508), then the system shall set the result text to 'Datevalue error'. (rules OATM-BR-307)
2. GIVEN a date that the date conversion service reports as a bad date value (feedback X'000309CC59C3C5C5', severity 3, message 2508) WHEN the date check runs THEN the result text is 'Datevalue error' (OATM-C35-AC-14; OATM-BR-307)

### Requirement 6: OATM-REQ-F-291 (business rule)

#### Acceptance criteria

1. If the date conversion service reports an invalid era (feedback X'000309CD59C3C5C5', message 2509), then the system shall set the result text to 'Invalid Era'. (rules OATM-BR-308)
2. GIVEN feedback: invalid era, severity 3, message 2509 WHEN the date conversion service reports an invalid era (feedback X'000309CD59C3C5C5', message 2509) THEN Result text 'Invalid Era'; the caller treats the date as invalid (OATM-C35-AC-03; OATM-BR-308)

### Requirement 7: OATM-REQ-F-292 (business rule)

#### Acceptance criteria

1. If the date conversion service reports an unsupported date range (feedback X'000309D159C3C5C5', message 2513), then the system shall set the result text to 'Unsupp. Range'. (rules OATM-BR-309)
2. GIVEN date: 1500-01-01; mask: YYYY-MM-DD WHEN the date conversion service reports an unsupported date range (feedback X'000309D159C3C5C5', message 2513) THEN Result text 'Unsupp. Range', severity '0003', message '2513'; the calling screens still accept the date (OATM-C35-AC-04; OATM-BR-309)

### Requirement 8: OATM-REQ-F-293 (business rule)

#### Acceptance criteria

1. If the date conversion service reports an invalid month (feedback X'000309D559C3C5C5', message 2517), then the system shall set the result text to 'Invalid month'. (rules OATM-BR-310)
2. GIVEN date: 2023-13-01; mask: YYYY-MM-DD WHEN the date conversion service reports an invalid month (feedback X'000309D559C3C5C5', message 2517) THEN Result text 'Invalid month'; the caller treats the date as invalid (OATM-C35-AC-05; OATM-BR-310)

### Requirement 9: OATM-REQ-F-294 (business rule)

#### Acceptance criteria

1. If the date conversion service reports a bad format mask (feedback X'000309D659C3C5C5', message 2518), then the system shall set the result text to 'Bad Pic String'. (rules OATM-BR-311)
2. GIVEN mask: an unrecognised format mask WHEN the date conversion service reports a bad format mask (feedback X'000309D659C3C5C5', message 2518) THEN Result text 'Bad Pic String'; the caller treats the date as invalid (OATM-C35-AC-06; OATM-BR-311)

### Requirement 10: OATM-REQ-F-295 (business rule)

#### Acceptance criteria

1. If the date conversion service reports a year-in-era of zero (feedback X'000309D959C3C5C5', message 2521), then the system shall set the result text to 'YearInEra is 0'. (rules OATM-BR-312)
2. GIVEN feedback: year-in-era zero, severity 3, message 2521 WHEN the date conversion service reports a year-in-era of zero (feedback X'000309D959C3C5C5', message 2521) THEN Result text 'YearInEra is 0'; the caller treats the date as invalid (OATM-C35-AC-07; OATM-BR-312)

### Requirement 11: OATM-REQ-F-296 (business rule)

#### Acceptance criteria

1. If the date conversion service reports that the date contains non-numeric characters, then the system shall return the result text 'Nonnumeric data' together with the service's severity and message code, so the caller treats the date as invalid. (rules OATM-BR-313)
2. GIVEN date: 2024-AB-01; date format: YYYY-MM-DD WHEN the date service reports that the date contains non-numeric characters THEN The result reads 'Nonnumeric data' with a non-zero severity; on the Add Transaction screen the user sees 'Orig Date - Not a valid date...'. (OATM-C35-AC-08; OATM-BR-313)

### Requirement 12: OATM-REQ-F-297 (business rule)

#### Acceptance criteria

1. If the date conversion feedback matches none of the recognised tokens, then the system shall set the result text to 'Date is invalid'. (rules OATM-BR-314)
2. GIVEN feedback: any other non-zero token WHEN the date conversion feedback matches none of the recognised tokens THEN Result text 'Date is invalid' (OATM-C35-AC-09; OATM-BR-314)

### Requirement 13: OATM-REQ-F-298 (business rule)

#### Acceptance criteria

1. If the returned severity is not '0000' and the message number is not '2513', then the calling screens (report date range, transaction add) shall treat the date as invalid and show their error, for example 'Start Date - Not a valid date...' or 'Orig Date - Not a valid date...'. (rules OATM-BR-315)
2. GIVEN start date: 2023-02-30; severity: 0003; message number: 2508 WHEN the returned severity is not '0000' and the message number is not '2513' THEN Report screen shows 'Start Date - Not a valid date...' (OATM-C35-AC-10; OATM-BR-315)
3. GIVEN original transaction date: 2023-02-28; severity: 0000 WHEN the returned severity is not '0000' and the message number is not '2513' THEN Date accepted; validation continues (OATM-C35-AC-11; OATM-BR-315)

## Screens and components

### Add transaction (S-TRANSACTION-ADD)

Enter a transaction against an account or card, see what to fix at each field, confirm the summary and record it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction reports (S-REPORT-REQUEST)

Choose a monthly, yearly or custom period and submit the transaction report for printing after confirming.

Prototype: `ui-reference/index.html#/S-REPORT-REQUEST`. Replaces the legacy screens CORPT0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|


## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-303 | Submit date and mask for conversion | design note | THE Date Validation Utility SHALL pass the caller's 10-character date and 10-character format mask to the date conversion service (CEEDAYS) and record the returned severity and message number as 4-digit values in its result. | high | app/cbl/CSUTLDTC.cbl:42-57, app/cbl/CSUTLDTC.cbl:88-124, app/cbl/CORPT00C.cbl:128-136, app/cbl/CORPT00C.cbl:388-405 |
| OATM-BR-304 | Submit date and mask for conversion | design note | THE Date Validation Utility SHALL return an 80-character result made of the severity, 'Mesg Code:', the message number, the result text, 'TstDate:' with the tested date and 'Mask used:' with the mask, and SHALL set the program return code to the severity. | high | app/cbl/CSUTLDTC.cbl:42-57, app/cbl/CSUTLDTC.cbl:88-124, app/cbl/CORPT00C.cbl:128-136, app/cbl/CORPT00C.cbl:388-405 |
| OATM-BR-305 | Report date as valid | business rule | WHEN the date conversion service (CEEDAYS) returns an all-zero feedback token for the 10-character date and 10-character mask it was given, THE Date Validation Utility SHALL set the result text to 'Date is valid'. | high | app/cbl/CSUTLDTC.cbl:62-64, app/cbl/CSUTLDTC.cbl:103-134, app/cbl/CORPT00C.cbl:72 |
| OATM-BR-306 | Report insufficient date data | business rule | WHEN the date conversion service reports insufficient data (feedback X'000309CB59C3C5C5', message 2507), THE Date Validation Utility SHALL set the result text to 'Insufficient'. | medium | app/cbl/CSUTLDTC.cbl:63, app/cbl/CSUTLDTC.cbl:131-132 |
| OATM-BR-307 | Report bad date value | business rule | WHEN the date conversion service reports a bad date value (feedback X'000309CC59C3C5C5', severity 3, message 2508), THE Date Validation Utility SHALL set the result text to 'Datevalue error'. | high | app/cbl/CSUTLDTC.cbl:62-64, app/cbl/CSUTLDTC.cbl:103-134, app/cbl/CORPT00C.cbl:72 |
| OATM-BR-308 | Report invalid era | business rule | WHEN the date conversion service reports an invalid era (feedback X'000309CD59C3C5C5', message 2509), THE Date Validation Utility SHALL set the result text to 'Invalid Era'. | medium | app/cbl/CSUTLDTC.cbl:65, app/cbl/CSUTLDTC.cbl:135-136 |
| OATM-BR-309 | Report unsupported date range | business rule | WHEN the date conversion service reports an unsupported date range (feedback X'000309D159C3C5C5', message 2513), THE Date Validation Utility SHALL set the result text to 'Unsupp. Range'. | medium | app/cbl/CSUTLDTC.cbl:66, app/cbl/CSUTLDTC.cbl:137-138, app/cbl/CORPT00C.cbl:396-405, app/cbl/COTRN02C.cbl:397-406 |
| OATM-BR-310 | Report invalid month | business rule | WHEN the date conversion service reports an invalid month (feedback X'000309D559C3C5C5', message 2517), THE Date Validation Utility SHALL set the result text to 'Invalid month'. | medium | app/cbl/CSUTLDTC.cbl:67, app/cbl/CSUTLDTC.cbl:139-140 |
| OATM-BR-311 | Report bad format mask | business rule | WHEN the date conversion service reports a bad format mask (feedback X'000309D659C3C5C5', message 2518), THE Date Validation Utility SHALL set the result text to 'Bad Pic String'. | medium | app/cbl/CSUTLDTC.cbl:68, app/cbl/CSUTLDTC.cbl:141-142 |
| OATM-BR-312 | Report zero year in era | business rule | WHEN the date conversion service reports a year-in-era of zero (feedback X'000309D959C3C5C5', message 2521), THE Date Validation Utility SHALL set the result text to 'YearInEra is 0'. | medium | app/cbl/CSUTLDTC.cbl:70, app/cbl/CSUTLDTC.cbl:145-146 |
| OATM-BR-313 | Report non-numeric date data | business rule | WHEN the date service reports that the date contains non-numeric characters, THE Date Validation SHALL return the result text 'Nonnumeric data' together with the service's severity and message code (returned in WS-RESULT), so the caller treats the date as invalid. | medium | app/cbl/CSUTLDTC.cbl:69, app/cbl/CSUTLDTC.cbl:116-124, app/cbl/CSUTLDTC.cbl:143-144, app/cbl/CSUTLDTC.cbl:97-98 |
| OATM-BR-314 | Report unrecognized date validation failure | business rule | WHEN the date conversion feedback matches none of the recognised tokens, THE Date Validation Utility SHALL set the result text to 'Date is invalid'. | medium | app/cbl/CSUTLDTC.cbl:128, app/cbl/CSUTLDTC.cbl:147-149 |
| OATM-BR-315 | Date validation result contract: severity becomes return code, message number drives caller acceptance | business rule | WHEN the returned severity is not '0000' and the message number is not '2513', THE calling screens (report date range, transaction add) SHALL treat the date as invalid and show their error, for example 'Start Date - Not a valid date...' or 'Orig Date - Not a valid date...'. | high | app/cbl/CSUTLDTC.cbl:42-57, app/cbl/CSUTLDTC.cbl:88-124, app/cbl/CORPT00C.cbl:128-136, app/cbl/CORPT00C.cbl:388-405 |

### Worked examples

- OATM-BR-305: date = 2023-02-28; mask = YYYY-MM-DD → Feedback token all zeros; result text 'Date is valid', severity '0000'
- OATM-BR-306: feedback = insufficient data, severity 3, message 2507 → Result text 'Insufficient'; the caller treats the date as invalid
- OATM-BR-308: feedback = invalid era, severity 3, message 2509 → Result text 'Invalid Era'; the caller treats the date as invalid
- OATM-BR-309: date = 1500-01-01; mask = YYYY-MM-DD → Result text 'Unsupp. Range', severity '0003', message '2513'; the calling screens still accept the date
- OATM-BR-310: date = 2023-13-01; mask = YYYY-MM-DD → Result text 'Invalid month'; the caller treats the date as invalid
- OATM-BR-311: mask = an unrecognised format mask → Result text 'Bad Pic String'; the caller treats the date as invalid
- OATM-BR-312: feedback = year-in-era zero, severity 3, message 2521 → Result text 'YearInEra is 0'; the caller treats the date as invalid
- OATM-BR-313: date = 2024-AB-01; date format = YYYY-MM-DD → The result reads 'Nonnumeric data' with a non-zero severity; on the Add Transaction screen the user sees 'Orig Date - Not a valid date...'.
- OATM-BR-314: feedback = any other non-zero token → Result text 'Date is invalid'
- OATM-BR-315: start date = 2023-02-30; severity = 0003; message number = 2508 → Report screen shows 'Start Date - Not a valid date...'
- OATM-BR-315: original transaction date = 2023-02-28; severity = 0000 → Date accepted; validation continues

## Decision tables

#### Date validation result text by conversion feedback

| Date conversion feedback | Result text | Rule |
|---|---|---|
| All-zero feedback token | 'Date is valid' | OATM-BR-305 |
| X'000309CB59C3C5C5' (message 2507, insufficient data) | 'Insufficient' | OATM-BR-306 |
| X'000309CC59C3C5C5' (severity 3, message 2508, bad date value) | 'Datevalue error' | OATM-BR-307 |
| X'000309CD59C3C5C5' (message 2509, invalid era) | 'Invalid Era' | OATM-BR-308 |
| X'000309D159C3C5C5' (message 2513, unsupported range) | 'Unsupp. Range' | OATM-BR-309 |
| X'000309D559C3C5C5' (message 2517, invalid month) | 'Invalid month' | OATM-BR-310 |
| X'000309D659C3C5C5' (message 2518, bad format mask) | 'Bad Pic String' | OATM-BR-311 |
| X'000309D959C3C5C5' (message 2521, year-in-era zero) | 'YearInEra is 0' | OATM-BR-312 |
| Non-numeric characters in date | 'Nonnumeric data' with severity and message code | OATM-BR-313 |
| Any other feedback token | 'Date is invalid' | OATM-BR-314 |
| Non-numeric characters in date | **Gap:** The rules do not give the feedback token or message number for the non-numeric case; confirm which token the service returns. | |
| X'000309D159C3C5C5' (message 2513, unsupported range) | **Gap:** Callers accept message 2513 as not invalid even though the result text is 'Unsupp. Range'; confirm that dates outside the supported range should be accepted. | |


## Design notes

- OATM-BR-303: Provide a reusable date-validation function that takes a date string and a format pattern and returns a structured result: a 4-digit severity, a 4-digit message number and a reason. Implement it with the platform's standard strict date parsing, which rejects impossible dates. Map outcomes to the legacy message numbers (2507, 2508, 2509, 2513, 2517, 2518, 2521) where callers depend on them, for example the 2513 exception.
- OATM-BR-304: Return the result as a structured value (severity, message number, result text, tested date, mask used) with severity as the outcome code. Keep a formatter that renders the legacy 80-character text ('Mesg Code:', 'TstDate:', 'Mask used:') only if a consumer still needs that exact layout.

## Open questions

- SME-237: The date-check service returns an all-zeros code to mean 'date is valid', but the legacy code labels that code 'invalid date'. Can you confirm the code keeps meaning success and the misleading label is dropped? (Development lead) On OATM-BR-306, OATM-BR-314, OATM-BR-310, OATM-BR-308, OATM-BR-312, OATM-BR-311, OATM-BR-309, OATM-BR-313, OATM-BR-305, OATM-BR-307, OATM-BR-304.
- SME-238: The date-check service reports one of ten outcomes (valid, insufficient data, bad value, invalid era, unsupported range, invalid month, bad format, non-numeric, zero year, unrecognized). How should the new date-check service's own results map to these ten outcomes? (Application architect) On OATM-BR-306, OATM-BR-314, OATM-BR-310, OATM-BR-308, OATM-BR-312, OATM-BR-311, OATM-BR-309, OATM-BR-313, OATM-BR-307, OATM-BR-304.
- SME-239: Screens currently accept a date that the date check flags as outside the supported range. Is accepting out-of-range dates a business rule, or a workaround the new validation should drop? (Card operations business analyst) On OATM-BR-315.
- DEF-055: Is this intended? The condition for the all-zero (successful) feedback token is named FC-INVALID-DATE, although it means the date is valid; the behaviour is correct but the name is misleading. (Subject-matter expert) On OATM-BR-305, OATM-BR-307.
- DEF-095: Is this intended? After the call the whole date structure, including its 2-byte binary length prefix, is moved into the 10-character tested-date field, so the 'TstDate:' part of the result shows two binary bytes followed by only the first 8 characters of the date instead of the date itself. (Subject-matter expert) On OATM-BR-304, OATM-BR-315.
- DEF-119: Confirm this is deliberate: The calling screens accept a date when the message number is 2513, which is this unsupported-range result, so a date that the date service cannot handle is let through as valid. (Subject-matter expert) On OATM-BR-309.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (14 in all).
