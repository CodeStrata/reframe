# Convert date formats (UP-C07)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-031 | Report invalid conversion request | business rule | IF the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type, THEN THE Date Format Conversion Routine SHALL set the error message (`COERMSG`) to 'INVALID INPUT' for the caller | low | app/asm/COBDATFT.asm:55-56, app/asm/COBDATFT.asm:29-56 |
| UP-BR-032 | Route request by input date type | business rule | WHEN a date conversion request has an input type other than '1' or '2', THE date format conversion routine SHALL reject it with the message 'INVALID INPUT' and leave the output date unchanged. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-033 | Route request by input date type | design note | WHEN the input type is '1' (YYYYMMDD) and the requested output type is not '2', THE date format conversion routine SHALL return the date as YYYY-MM-DD, inserting dashes between year, month and day. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-034 | Insert dashes into undashed date | business rule | WHEN the input type is '1' and the input date already has a dash as its fifth character or the requested output type is '2', THE date format conversion routine SHALL reject the request with the message 'INVALID INPUT'. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-035 | Route request by input date type | design note | WHEN the input type is '2' (YYYY-MM-DD) and the requested output type is not '1', THE date format conversion routine SHALL return the date as YYYYMMDD, taking the year from characters 1-4, the month from 6-7 and the day from 9-10, without checking that the input contains dashes. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-036 | Remove dashes from dashed date | business rule | WHEN the input type is '2' and the requested output type is '1', THE date format conversion routine SHALL reject the request with the message 'INVALID INPUT'. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-037 | Account date format conversion between YYYYMMDD and YYYY-MM-DD | design note | WHEN the account extract writes each account record, THE account extract SHALL convert the account reissue date from YYYY-MM-DD to YYYYMMDD (input type '2', output type '2') using the date format conversion routine. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |

### Worked examples

- UP-BR-031: Input type (COINTYPE) = '3'; Output type (COOUTYPE) = '2' → The routine sets the error message to 'INVALID INPUT' and returns no converted date. (The only caller, CBACT01C, always passes input type '2' and output type '2', so this never happens today.)
- UP-BR-031: Input type (COINTYPE) = '2'; Output type (COOUTYPE) = '1' → The error message is set to 'INVALID INPUT'.

## Decision tables

#### Date format conversion routing

| Input type | Requested output type | Dash at fifth character of input | Conversion result | Rule |
|---|---|---|---|---|
| not '1' or '2' | any | any | Reject with 'INVALID INPUT'; output date unchanged | UP-BR-032 |
| '1' | not '2' | No | Return date as YYYY-MM-DD | UP-BR-033 |
| '1' | any | Yes | Reject with 'INVALID INPUT' | UP-BR-034 |
| '1' | '2' | any | Reject with 'INVALID INPUT' | UP-BR-034 |
| '2' | not '1' | any (not checked) | Return date as YYYYMMDD from characters 1-4, 6-7 and 9-10 | UP-BR-035 |
| '2' | '1' | any | Reject with 'INVALID INPUT' | UP-BR-036 |


## Design notes

- UP-BR-033: A pure, reusable date-formatting function that takes YYYYMMDD and returns YYYY-MM-DD. Build it as a library function, not a separate service call.
- UP-BR-035: The same library function going the other way: it takes YYYY-MM-DD and returns YYYYMMDD by position (characters 1-4, 6-7 and 9-10). It does not validate the separators.
- UP-BR-037: The account extract calls the date-formatting function on the reissue date for every record it writes, so the extract carries the date as YYYYMMDD.

## Open questions

- SME-078: The date conversion routine was designed to check that a dashed date has its dash in the right position, but that check is switched off. Should the new routine check it? (Business analyst) On UP-BR-031, UP-BR-034, UP-BR-035, UP-BR-036.
- SME-079: In date conversion requests, the output-type code has to match the input-type code, even though the output is in the other format. Is the output-type code meant to name the output format (so the check is backwards), or just to repeat the conversion direction? (Application developer) On UP-BR-031.
- DEF-007: Confirm this is deliberate: For type '2' input, the check that the fifth character is a dash is commented out, so a date with other separators or no separators is converted without error; the routine also always returns code 0 and CBACT01C never checks the error message. (Subject-matter expert) On UP-BR-034, UP-BR-035, UP-BR-036, UP-BR-037.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).
