# Requirements: Validate a date against a format mask (OATM-C35)

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
