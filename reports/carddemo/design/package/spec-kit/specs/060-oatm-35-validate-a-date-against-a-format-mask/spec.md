# Feature specification: Validate a date against a format mask

**Feature:** OATM-C35 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C35)

As a screen that accepts dates (report date range, transaction add), I want a date checked against its format mask with a clear result and reason, so that invalid dates are rejected with a meaningful error.

A shared date check used by the report date range and Add Transaction screens. It tests a 10-character date against a 10-character format mask and returns a severity, a message number and a reason such as 'Date is valid', 'Datevalue error' or 'Invalid month'. Callers treat the date as invalid when the severity is not 0000, unless the message number is 2513. Real dates must be accepted and impossible dates rejected.

**Acceptance scenarios:**

1. **Given** date: 2023-02-28; mask: YYYY-MM-DD, **when** the date conversion service (CEEDAYS) returns an all-zero feedback token for the 10-character date and 10-character mask it was given, **then** Feedback token all zeros; result text 'Date is valid', severity '0000' (OATM-C35-AC-01)
2. **Given** feedback: insufficient data, severity 3, message 2507, **when** the date conversion service reports insufficient data (feedback X'000309CB59C3C5C5', message 2507), **then** Result text 'Insufficient'; the caller treats the date as invalid (OATM-C35-AC-02)
3. **Given** feedback: invalid era, severity 3, message 2509, **when** the date conversion service reports an invalid era (feedback X'000309CD59C3C5C5', message 2509), **then** Result text 'Invalid Era'; the caller treats the date as invalid (OATM-C35-AC-03)
4. **Given** date: 1500-01-01; mask: YYYY-MM-DD, **when** the date conversion service reports an unsupported date range (feedback X'000309D159C3C5C5', message 2513), **then** Result text 'Unsupp. Range', severity '0003', message '2513'; the calling screens still accept the date (OATM-C35-AC-04)
5. **Given** date: 2023-13-01; mask: YYYY-MM-DD, **when** the date conversion service reports an invalid month (feedback X'000309D559C3C5C5', message 2517), **then** Result text 'Invalid month'; the caller treats the date as invalid (OATM-C35-AC-05)
6. **Given** mask: an unrecognised format mask, **when** the date conversion service reports a bad format mask (feedback X'000309D659C3C5C5', message 2518), **then** Result text 'Bad Pic String'; the caller treats the date as invalid (OATM-C35-AC-06)
7. **Given** feedback: year-in-era zero, severity 3, message 2521, **when** the date conversion service reports a year-in-era of zero (feedback X'000309D959C3C5C5', message 2521), **then** Result text 'YearInEra is 0'; the caller treats the date as invalid (OATM-C35-AC-07)
8. **Given** date: 2024-AB-01; date format: YYYY-MM-DD, **when** the date service reports that the date contains non-numeric characters, **then** The result reads 'Nonnumeric data' with a non-zero severity; on the Add Transaction screen the user sees 'Orig Date - Not a valid date...'. (OATM-C35-AC-08)
9. **Given** feedback: any other non-zero token, **when** the date conversion feedback matches none of the recognised tokens, **then** Result text 'Date is invalid' (OATM-C35-AC-09)
10. **Given** start date: 2023-02-30; severity: 0003; message number: 2508, **when** the returned severity is not '0000' and the message number is not '2513', **then** Report screen shows 'Start Date - Not a valid date...' (OATM-C35-AC-10)
11. **Given** original transaction date: 2023-02-28; severity: 0000, **when** the returned severity is not '0000' and the message number is not '2513', **then** Date accepted; validation continues (OATM-C35-AC-11)
12. **Given** a caller supplies the date '2024-02-30' and the format mask 'YYYY-MM-DD', **when** the date check runs, **then** exactly that 10-character date and 10-character mask are what is checked, and the result records the severity and message number as 4-digit values (for a bad date value: severity 0003, message number 2508) (OATM-C35-AC-12)
13. **Given** a caller supplies the date '2024-02-30' and the format mask 'YYYY-MM-DD', **when** the date check returns, **then** the 80-character result contains, in order, the severity, 'Mesg Code:', the message number, the result text, 'TstDate:' with 2024-02-30 and 'Mask used:' with YYYY-MM-DD, and the return code equals the severity (OATM-C35-AC-13)
14. **Given** a date that the date conversion service reports as a bad date value (feedback X'000309CC59C3C5C5', severity 3, message 2508), **when** the date check runs, **then** the result text is 'Datevalue error' (OATM-C35-AC-14)

## Requirements

### Functional requirements

- **OATM-REQ-F-286** (design note): The system shall pass the caller's 10-character date and 10-character format mask to the date conversion service (CEEDAYS) and record the returned severity and message number as 4-digit values in its result. Rules: OATM-BR-303.
- **OATM-REQ-F-287** (design note): The system shall return an 80-character result made of the severity, 'Mesg Code:', the message number, the result text, 'TstDate:' with the tested date and 'Mask used:' with the mask, and shall set the program return code to the severity. Rules: OATM-BR-304.
- **OATM-REQ-F-288** (business rule): When the date conversion service returns an all-zero feedback token for the date and mask it was given, the system shall set the result text to 'Date is valid'. Rules: OATM-BR-305.
- **OATM-REQ-F-289** (business rule): If the date conversion service reports insufficient data (feedback X'000309CB59C3C5C5', message 2507), then the system shall set the result text to 'Insufficient'. Rules: OATM-BR-306.
- **OATM-REQ-F-290** (business rule): If the date conversion service reports a bad date value (feedback X'000309CC59C3C5C5', severity 3, message 2508), then the system shall set the result text to 'Datevalue error'. Rules: OATM-BR-307.
- **OATM-REQ-F-291** (business rule): If the date conversion service reports an invalid era (feedback X'000309CD59C3C5C5', message 2509), then the system shall set the result text to 'Invalid Era'. Rules: OATM-BR-308.
- **OATM-REQ-F-292** (business rule): If the date conversion service reports an unsupported date range (feedback X'000309D159C3C5C5', message 2513), then the system shall set the result text to 'Unsupp. Range'. Rules: OATM-BR-309.
- **OATM-REQ-F-293** (business rule): If the date conversion service reports an invalid month (feedback X'000309D559C3C5C5', message 2517), then the system shall set the result text to 'Invalid month'. Rules: OATM-BR-310.
- **OATM-REQ-F-294** (business rule): If the date conversion service reports a bad format mask (feedback X'000309D659C3C5C5', message 2518), then the system shall set the result text to 'Bad Pic String'. Rules: OATM-BR-311.
- **OATM-REQ-F-295** (business rule): If the date conversion service reports a year-in-era of zero (feedback X'000309D959C3C5C5', message 2521), then the system shall set the result text to 'YearInEra is 0'. Rules: OATM-BR-312.
- **OATM-REQ-F-296** (business rule): If the date conversion service reports that the date contains non-numeric characters, then the system shall return the result text 'Nonnumeric data' together with the service's severity and message code, so the caller treats the date as invalid. Rules: OATM-BR-313.
- **OATM-REQ-F-297** (business rule): If the date conversion feedback matches none of the recognised tokens, then the system shall set the result text to 'Date is invalid'. Rules: OATM-BR-314.
- **OATM-REQ-F-298** (business rule): If the returned severity is not '0000' and the message number is not '2513', then the calling screens (report date range, transaction add) shall treat the date as invalid and show their error, for example 'Start Date - Not a valid date...' or 'Orig Date - Not a valid date...'. Rules: OATM-BR-315.

### Business rules

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

### Key entities

None found in the source.

### Needs clarification

- SME-237: The date-check service returns an all-zeros code to mean 'date is valid', but the legacy code labels that code 'invalid date'. Can you confirm the code keeps meaning success and the misleading label is dropped? (Development lead) On OATM-BR-306, OATM-BR-314, OATM-BR-310, OATM-BR-308, OATM-BR-312, OATM-BR-311, OATM-BR-309, OATM-BR-313, OATM-BR-305, OATM-BR-307, OATM-BR-304.
- SME-238: The date-check service reports one of ten outcomes (valid, insufficient data, bad value, invalid era, unsupported range, invalid month, bad format, non-numeric, zero year, unrecognized). How should the new date-check service's own results map to these ten outcomes? (Application architect) On OATM-BR-306, OATM-BR-314, OATM-BR-310, OATM-BR-308, OATM-BR-312, OATM-BR-311, OATM-BR-309, OATM-BR-313, OATM-BR-307, OATM-BR-304.
- SME-239: Screens currently accept a date that the date check flags as outside the supported range. Is accepting out-of-range dates a business rule, or a workaround the new validation should drop? (Card operations business analyst) On OATM-BR-315.
- DEF-055: Is this intended? The condition for the all-zero (successful) feedback token is named FC-INVALID-DATE, although it means the date is valid; the behaviour is correct but the name is misleading. (Subject-matter expert) On OATM-BR-305, OATM-BR-307.
- DEF-095: Is this intended? After the call the whole date structure, including its 2-byte binary length prefix, is moved into the 10-character tested-date field, so the 'TstDate:' part of the result shows two binary bytes followed by only the first 8 characters of the date instead of the date itself. (Subject-matter expert) On OATM-BR-304, OATM-BR-315.
- DEF-119: Confirm this is deliberate: The calling screens accept a date when the message number is 2513, which is this unsupported-range result, so a date that the date service cannot handle is let through as valid. (Subject-matter expert) On OATM-BR-309.

### Decision table gaps

- Date validation result text by conversion feedback: The rules do not give the feedback token or message number for the non-numeric case; confirm which token the service returns.
- Date validation result text by conversion feedback: Callers accept message 2513 as not invalid even though the result text is 'Unsupp. Range'; confirm that dates outside the supported range should be accepted.
