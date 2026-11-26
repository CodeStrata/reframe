# Feature specification: Convert date formats

**Feature:** UP-C07 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C07)

As a calling batch program, I want dates converted between YYYYMMDD and YYYY-MM-DD, so that account dates can be written in the format required.

A shared routine that converts dates between YYYYMMDD and YYYY-MM-DD for other batch programs, for example to write the account reissue date in the account extract. It must reject any request it cannot interpret with 'INVALID INPUT' rather than return a wrong date.

**Acceptance scenarios:**

1. **Given** Input type (COINTYPE): '3'; Output type (COOUTYPE): '2', **when** the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type, **then** The routine sets the error message to 'INVALID INPUT' and returns no converted date. (The only caller, CBACT01C, always passes input type '2' and output type '2', so this never happens today.) (UP-C07-AC-01)
2. **Given** Input type (COINTYPE): '2'; Output type (COOUTYPE): '1', **when** the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type, **then** The error message is set to 'INVALID INPUT'. (UP-C07-AC-02)
3. **Given** A conversion request with input type '1', input date '20240315' and an output type other than '2', **when** The routine converts the date, **then** It returns '2024-03-15'. (UP-C07-AC-03)
4. **Given** A conversion request with input type '2', input date '2024-03-15' and an output type other than '1', **when** The routine converts the date, **then** It returns '20240315', with the year taken from characters 1-4, the month from 6-7 and the day from 9-10. (UP-C07-AC-04)
5. **Given** A conversion request with input type '2' and input date '2024/03/15', which has no dashes, **when** The routine converts the date, **then** It still returns '20240315' and reports no error, because it does not check for dashes. (UP-C07-AC-05)
6. **Given** An account whose reissue date is '2025-07-01', **when** The account extract writes that account's record, **then** The reissue date in the written record is '20250701', converted by the date routine with input type '2' and output type '2'. (UP-C07-AC-06)

## Requirements

### Functional requirements

- **UP-REQ-F-029** (business rule): If the input type is not '1' or '2', then the system shall reject the request with the message 'INVALID INPUT' in the error message (COERMSG) and leave the output date unchanged. Rules: UP-BR-031, UP-BR-032.
- **UP-REQ-F-030** (design note): When the input type is '1' (YYYYMMDD) and the requested output type is not '2', the system shall return the date as YYYY-MM-DD, inserting dashes between year, month and day. Rules: UP-BR-033.
- **UP-REQ-F-031** (business rule): If the input type is '1' and the input date already has a dash as its fifth character or the requested output type is '2', then the system shall reject the request with the message 'INVALID INPUT'. Rules: UP-BR-034, UP-BR-031.
- **UP-REQ-F-032** (design note): When the input type is '2' (YYYY-MM-DD) and the requested output type is not '1', the system shall return the date as YYYYMMDD, taking the year from characters 1-4, the month from 6-7 and the day from 9-10, without checking that the input contains dashes. Rules: UP-BR-035.
- **UP-REQ-F-033** (business rule): If the input type is '2' and the requested output type is '1', then the system shall reject the request with the message 'INVALID INPUT'. Rules: UP-BR-036, UP-BR-031.
- **UP-REQ-F-034** (design note): When the account extract writes each account record, the system shall convert the account reissue date from YYYY-MM-DD to YYYYMMDD (input type '2', output type '2') using the date format conversion routine. Rules: UP-BR-037.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-031 | Report invalid conversion request | business rule | IF the input type is not '1' or '2', or a type-1 date already contains a dash at its fifth position, or the output type contradicts the input type, THEN THE Date Format Conversion Routine SHALL set the error message (`COERMSG`) to 'INVALID INPUT' for the caller | low | app/asm/COBDATFT.asm:55-56, app/asm/COBDATFT.asm:29-56 |
| UP-BR-032 | Route request by input date type | business rule | WHEN a date conversion request has an input type other than '1' or '2', THE date format conversion routine SHALL reject it with the message 'INVALID INPUT' and leave the output date unchanged. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-033 | Route request by input date type | design note | WHEN the input type is '1' (YYYYMMDD) and the requested output type is not '2', THE date format conversion routine SHALL return the date as YYYY-MM-DD, inserting dashes between year, month and day. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-034 | Insert dashes into undashed date | business rule | WHEN the input type is '1' and the input date already has a dash as its fifth character or the requested output type is '2', THE date format conversion routine SHALL reject the request with the message 'INVALID INPUT'. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-035 | Route request by input date type | design note | WHEN the input type is '2' (YYYY-MM-DD) and the requested output type is not '1', THE date format conversion routine SHALL return the date as YYYYMMDD, taking the year from characters 1-4, the month from 6-7 and the day from 9-10, without checking that the input contains dashes. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-036 | Remove dashes from dashed date | business rule | WHEN the input type is '2' and the requested output type is '1', THE date format conversion routine SHALL reject the request with the message 'INVALID INPUT'. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |
| UP-BR-037 | Account date format conversion between YYYYMMDD and YYYY-MM-DD | design note | WHEN the account extract writes each account record, THE account extract SHALL convert the account reissue date from YYYY-MM-DD to YYYYMMDD (input type '2', output type '2') using the date format conversion routine. | high | app/asm/COBDATFT.asm:27-57, app/maclib/COCDATFT.mac:18-23, app/cpy/CODATECN.cpy:17-52, app/cbl/CBACT01C.cbl:223-233 |

### Key entities

None found in the source.

### Needs clarification

- SME-078: The date conversion routine was designed to check that a dashed date has its dash in the right position, but that check is switched off. Should the new routine check it? (Business analyst) On UP-BR-031, UP-BR-034, UP-BR-035, UP-BR-036.
- SME-079: In date conversion requests, the output-type code has to match the input-type code, even though the output is in the other format. Is the output-type code meant to name the output format (so the check is backwards), or just to repeat the conversion direction? (Application developer) On UP-BR-031.
- DEF-007: Confirm this is deliberate: For type '2' input, the check that the fifth character is a dash is commented out, so a date with other separators or no separators is converted without error; the routine also always returns code 0 and CBACT01C never checks the error message. (Subject-matter expert) On UP-BR-034, UP-BR-035, UP-BR-036, UP-BR-037.

### Decision table gaps

None.
