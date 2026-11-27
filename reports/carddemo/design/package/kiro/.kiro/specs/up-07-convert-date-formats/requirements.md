# Requirements: Convert date formats (UP-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

A shared routine that converts dates between YYYYMMDD and YYYY-MM-DD for other batch programs, for example to write the account reissue date in the account extract. It must reject any request it cannot interpret with 'INVALID INPUT' rather than return a wrong date.

**User story:** As a calling batch program, I want dates converted between YYYYMMDD and YYYY-MM-DD, so that account dates can be written in the format required.

## Requirements

### Requirement 1: UP-REQ-F-029 (business rule)

#### Acceptance criteria

1. If the input type is not '1' or '2', then the system shall reject the request with the message 'INVALID INPUT' in the error message (COERMSG) and leave the output date unchanged. (rules UP-BR-031, UP-BR-032)
2. GIVEN Input type (COINTYPE): '3'; Output type (COOUTYPE): '2' WHEN the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type THEN The routine sets the error message to 'INVALID INPUT' and returns no converted date. (The only caller, CBACT01C, always passes input type '2' and output type '2', so this never happens today.) (UP-C07-AC-01; UP-BR-031)
3. GIVEN Input type (COINTYPE): '2'; Output type (COOUTYPE): '1' WHEN the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type THEN The error message is set to 'INVALID INPUT'. (UP-C07-AC-02; UP-BR-031)

### Requirement 2: UP-REQ-F-030 (design note)

#### Acceptance criteria

1. When the input type is '1' (YYYYMMDD) and the requested output type is not '2', the system shall return the date as YYYY-MM-DD, inserting dashes between year, month and day. (rules UP-BR-033)
2. GIVEN A conversion request with input type '1', input date '20240315' and an output type other than '2' WHEN The routine converts the date THEN It returns '2024-03-15'. (UP-C07-AC-03; UP-BR-033)

### Requirement 3: UP-REQ-F-031 (business rule)

#### Acceptance criteria

1. If the input type is '1' and the input date already has a dash as its fifth character or the requested output type is '2', then the system shall reject the request with the message 'INVALID INPUT'. (rules UP-BR-034, UP-BR-031)
2. GIVEN Input type (COINTYPE): '3'; Output type (COOUTYPE): '2' WHEN the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type THEN The routine sets the error message to 'INVALID INPUT' and returns no converted date. (The only caller, CBACT01C, always passes input type '2' and output type '2', so this never happens today.) (UP-C07-AC-01; UP-BR-031)
3. GIVEN Input type (COINTYPE): '2'; Output type (COOUTYPE): '1' WHEN the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type THEN The error message is set to 'INVALID INPUT'. (UP-C07-AC-02; UP-BR-031)

### Requirement 4: UP-REQ-F-032 (design note)

#### Acceptance criteria

1. When the input type is '2' (YYYY-MM-DD) and the requested output type is not '1', the system shall return the date as YYYYMMDD, taking the year from characters 1-4, the month from 6-7 and the day from 9-10, without checking that the input contains dashes. (rules UP-BR-035)
2. GIVEN A conversion request with input type '2', input date '2024-03-15' and an output type other than '1' WHEN The routine converts the date THEN It returns '20240315', with the year taken from characters 1-4, the month from 6-7 and the day from 9-10. (UP-C07-AC-04; UP-BR-035)
3. GIVEN A conversion request with input type '2' and input date '2024/03/15', which has no dashes WHEN The routine converts the date THEN It still returns '20240315' and reports no error, because it does not check for dashes. (UP-C07-AC-05; UP-BR-035)

### Requirement 5: UP-REQ-F-033 (business rule)

#### Acceptance criteria

1. If the input type is '2' and the requested output type is '1', then the system shall reject the request with the message 'INVALID INPUT'. (rules UP-BR-036, UP-BR-031)
2. GIVEN Input type (COINTYPE): '3'; Output type (COOUTYPE): '2' WHEN the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type THEN The routine sets the error message to 'INVALID INPUT' and returns no converted date. (The only caller, CBACT01C, always passes input type '2' and output type '2', so this never happens today.) (UP-C07-AC-01; UP-BR-031)
3. GIVEN Input type (COINTYPE): '2'; Output type (COOUTYPE): '1' WHEN the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type THEN The error message is set to 'INVALID INPUT'. (UP-C07-AC-02; UP-BR-031)

### Requirement 6: UP-REQ-F-034 (design note)

#### Acceptance criteria

1. When the account extract writes each account record, the system shall convert the account reissue date from YYYY-MM-DD to YYYYMMDD (input type '2', output type '2') using the date format conversion routine. (rules UP-BR-037)
2. GIVEN An account whose reissue date is '2025-07-01' WHEN The account extract writes that account's record THEN The reissue date in the written record is '20250701', converted by the date routine with input type '2' and output type '2'. (UP-C07-AC-06; UP-BR-037)
