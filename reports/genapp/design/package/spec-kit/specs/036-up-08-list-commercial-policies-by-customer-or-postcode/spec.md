# Feature specification: List commercial policies by customer or postcode

**Feature:** UP-C08 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C08)

As a policy administrator, I want to search commercial policies by customer or by property postcode, so that I can find commercial policies matching those criteria.

Searches commercial policies for policy administrators by customer number ('03ICOM') or by property postcode ('05ICOM'). As built today, the reply holds only the last policy read: a customer search stops after the 21st policy, a postcode search reads every match, and no match still returns code '00'. A search that cannot be started must return '89', and one that cannot be closed must return '88', each with an error message logged.

**Acceptance scenarios:**

1. **Given** request: '03ICOM'; customer number: 0000000004; commercial policies held: 3 (policies 101, 102, 103), **when** a commercial policy inquiry by customer (request '03ICOM') is made, **then** All 3 rows are read; the response shows policy 103 only, with return code '00'. (UP-C08-AC-01)
2. **Given** request: '03ICOM'; commercial policies held by customer: 25, **when** more than 20 commercial policies have been read for a customer inquiry ('03ICOM'), **then** 21 rows are read, reading stops, the response holds the 21st row and return code '00'. (UP-C08-AC-02)
3. **Given** request: '03ICOM'; commercial policies held by customer: 20, **when** more than 20 commercial policies have been read for a customer inquiry ('03ICOM'), **then** All 20 rows are read and the response holds the 20th row. (UP-C08-AC-03)
4. **Given** request: '05ICOM'; postcode: SO21 2JN; matching commercial policies: 30, **when** a commercial policy inquiry by property postcode (request '05ICOM') is made, **then** All 30 rows are read; the response holds the 30th row with return code '00'. (UP-C08-AC-04)
5. **Given** request: '03ICOM'; database list open: fails, **when** a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be started, **then** Return code '89', error message logged, request ends. (UP-C08-AC-05)
6. **Given** request: '05ICOM'; database list close: fails, **when** a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be closed after reading, **then** Return code '88', error message logged, request ends. (UP-C08-AC-06)
7. **Given** request: '05ICOM'; postcode: ZZ99 9ZZ; matching commercial policies: none, **when** no commercial policy matches the customer ('03ICOM') or postcode ('05ICOM'), **then** Return code '00'; no policy row in the response. (UP-C08-AC-07)

## Requirements

### Functional requirements

- **UP-REQ-F-045** (business rule): When a commercial policy inquiry by customer (request '03ICOM') is made, the system shall read the customer's commercial policies one at a time, placing each row's customer number, policy number, common policy details and commercial property details into the response, so the response ends up holding only the last row read. Rules: UP-BR-067.
- **UP-REQ-F-046** (business rule): When more than 20 commercial policies have been read for a customer inquiry ('03ICOM'), the system shall stop reading after the 21st row, leaving the 21st row in the response and the return code at '00'. Rules: UP-BR-068.
- **UP-REQ-F-047** (business rule): When a commercial policy inquiry by property postcode (request '05ICOM') is made, the system shall read every commercial policy whose property postcode matches, with no limit on the number of rows, placing each row's customer number, policy number, common and commercial details into the response, so only the last row read is returned. Rules: UP-BR-069.
- **UP-REQ-F-048** (error handling): If a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be started, then the system shall set return code '89', write an error message with date, time, customer number, policy number and SQL code to the error queue, and end the request. Rules: UP-BR-070.
- **UP-REQ-F-049** (error handling): If a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be closed after reading, then the system shall set return code '88', write an error message to the error queue, and end the request. Rules: UP-BR-071.
- **UP-REQ-F-050** (business rule): When no commercial policy matches the customer ('03ICOM') or postcode ('05ICOM'), the system shall return code '00' with no policy details filled in, rather than a not-found code. Rules: UP-BR-072.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-067 | Scan commercial policies for a customer | business rule | WHEN a commercial policy inquiry by customer (request '03ICOM') is made, THE policy inquiry service SHALL read the customer's commercial policies one at a time, placing each row's customer number, policy number, common policy details and commercial property details into the response, so the response ends up holding only the last row read. | high | base/src/lgipdb01.cbl:89-149, base/src/lgipdb01.cbl:299-305, base/src/lgipdb01.cbl:835-913, base/src/lgipdb01.cbl:919-990 |
| UP-BR-068 | Scan commercial policies for a customer | business rule | WHEN more than 20 commercial policies have been read for a customer inquiry ('03ICOM'), THE policy inquiry service SHALL stop reading after the 21st row (by forcing the stop value 17), leaving the 21st row in the response and the return code at '00'. | high | base/src/lgipdb01.cbl:89-149, base/src/lgipdb01.cbl:299-305, base/src/lgipdb01.cbl:835-913, base/src/lgipdb01.cbl:919-990 |
| UP-BR-069 | Scan commercial policies by postcode | business rule | WHEN a commercial policy inquiry by property postcode (request '05ICOM') is made, THE policy inquiry service SHALL read every commercial policy whose property postcode matches, with no limit on the number of rows, placing each row's customer number, policy number, common and commercial details into the response, so only the last row read is returned. | high | base/src/lgipdb01.cbl:89-149, base/src/lgipdb01.cbl:299-305, base/src/lgipdb01.cbl:835-913, base/src/lgipdb01.cbl:919-990 |
| UP-BR-070 | List customer commercial policies | error handling | WHEN a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be started, THE policy inquiry service SHALL set return code '89', write an error message with date, time, customer number, policy number and SQL code to the error queue, and end the request. | high | base/src/lgipdb01.cbl:89-149, base/src/lgipdb01.cbl:299-305, base/src/lgipdb01.cbl:835-913, base/src/lgipdb01.cbl:919-990 |
| UP-BR-071 | List customer commercial policies | error handling | WHEN a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be closed after reading, THE policy inquiry service SHALL set return code '88', write an error message to the error queue, and end the request. | high | base/src/lgipdb01.cbl:89-149, base/src/lgipdb01.cbl:299-305, base/src/lgipdb01.cbl:835-913, base/src/lgipdb01.cbl:919-990 |
| UP-BR-072 | List commercial policies by customer (capped) or by postcode | business rule | WHEN no commercial policy matches the customer ('03ICOM') or postcode ('05ICOM'), THE policy inquiry service SHALL return code '00' with no policy details filled in, rather than a not-found code. | high | base/src/lgipdb01.cbl:89-149, base/src/lgipdb01.cbl:299-305, base/src/lgipdb01.cbl:835-913, base/src/lgipdb01.cbl:919-990 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-068, UP-BR-069, UP-BR-071, UP-BR-072.
- DEF-027: Is this intended? Both lists overwrite the single response record with each row, so only the last row (the 21st for a customer) is returned and the 20-row cap does not deliver a list; also the read loop stops only on a positive SQL code, so a fetch error (negative SQL code) is not caught and the loop keeps fetching; an empty result returns '00' with no not-found code. (Subject-matter expert) On UP-BR-068, UP-BR-069, UP-BR-071, UP-BR-072.

### Decision table gaps

- Commercial policy list outcomes: No rule says what happens if reading a row fails after the list has started.
