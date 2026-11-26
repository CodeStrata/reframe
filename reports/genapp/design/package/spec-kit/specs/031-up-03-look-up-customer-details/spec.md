# Feature specification: Look up customer details

**Feature:** UP-C03 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C03)

As a customer service user, I want to retrieve a customer's details by customer number, so that I can see who the customer is and how to contact them.

Looks up one customer by customer number for customer service users and calling applications. It returns the customer's name, date of birth, address, phone numbers and email. It must return '98' for a request shorter than 90 bytes, '01' for an unknown customer, and '90' with an error log entry for any other database failure. A request with no data must be logged as ' NO COMMAREA RECEIVED' and end with code 'LGCA'.

**Acceptance scenarios:**

1. **Given** request length: 0, **when** the customer inquiry database program receives no request data (a length of zero), **then** Message ' NO COMMAREA RECEIVED' logged; transaction abends with code 'LGCA' (UP-C03-AC-01)
2. **Given** request length: 0, **when** the customer inquiry service is started with no request data, **then** Error ' NO COMMAREA RECEIVED' is logged and the task abends with 'LGCA' (UP-C03-AC-02)
3. **Given** request length: 32500; customer number: 0000000123, **when** a customer inquiry request with data is received, **then** Return code starts as '00' and policy count as '00' before the lookup (UP-C03-AC-03)
4. **Given** request length: 85 bytes, **when** a customer inquiry request is shorter than 90 bytes (72 bytes of customer data plus 18 bytes of header and trailer), **then** Outcome code '98'; no customer lookup (UP-C03-AC-04)
5. **Given** request length: 90 bytes, **when** a customer inquiry request is shorter than 90 bytes (72 bytes of customer data plus 18 bytes of header and trailer), **then** Request continues to the customer lookup (UP-C03-AC-05)
6. **Given** request length: 60, **when** a customer inquiry request is shorter than the customer record length (72) plus the header and trailer length (18), i.e. under 90 bytes, **then** Return code '98'; no customer lookup is made (UP-C03-AC-06)
7. **Given** request length: 32500, **when** a customer inquiry request is shorter than the customer record length (72) plus the header and trailer length (18), i.e. under 90 bytes, **then** Length check passes and the customer lookup proceeds (UP-C03-AC-07)
8. **Given** request length: 89, **when** a customer inquiry request is shorter than 90 bytes (customer record length 72 plus header and trailer length 18), **then** Return code '98'; LGICDB01 is not called (UP-C03-AC-08)
9. **Given** request length: 32500; customer number: 0000000123, **when** a customer inquiry request is at least 90 bytes long, **then** The request is handed to LGICDB01 and its outcome is returned to the caller (UP-C03-AC-09)
10. **Given** customer number: 0001000042; customer on file: yes, **when** a customer inquiry passes the request checks, **then** Name, date of birth, address, phones and email are returned with outcome code '00' (UP-C03-AC-10)
11. **Given** customer number: 0009999999; customer on file: no, **when** no customer exists with the requested customer number (SQLCODE 100), **then** Outcome code '01'; no customer details returned (UP-C03-AC-11)
12. **Given** customer number: 0001000042; database result: deadlock/timeout (-913), **when** the customer lookup fails because of a database deadlock or timeout (SQLCODE -913), **then** Outcome code '01' (UP-C03-AC-12)
13. **Given** customer number: 0001000042; database result: SQLCODE -805, **when** the customer lookup fails with any other database error, **then** Outcome code '90'; error message and request data written to the log queue (UP-C03-AC-13)

## Requirements

### Functional requirements

- **UP-REQ-F-006** (error handling): If a customer inquiry is started with no request data (a length of zero), then the system shall log the message ' NO COMMAREA RECEIVED' with the date and time to the error queue and end the transaction abnormally with abend code 'LGCA' without a dump. Rules: UP-BR-023, UP-BR-024.
- **UP-REQ-F-007** (business rule): When a customer inquiry request with data is received, the system shall first set the return code to '00' (success) and the number of policies to '00' before checking the request length. Rules: UP-BR-025, UP-BR-026.
- **UP-REQ-F-008** (business rule): If a customer inquiry request is shorter than 90 bytes (customer record length 72 plus header and trailer length 18), then the system shall return to the caller with return code '98' without looking up the customer. Rules: UP-BR-026, UP-BR-027, UP-BR-028.
- **UP-REQ-F-009** (design note): When a customer inquiry request is at least 90 bytes long, the system shall pass the whole request (32500 bytes) to the customer database service (LGICDB01) to look up the customer and return its result to the caller. Rules: UP-BR-029.
- **UP-REQ-F-010** (business rule): When a customer inquiry passes the request checks, the system shall look up the customer by customer number in the CUSTOMER table and return first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address, with return code '00'. Rules: UP-BR-030.
- **UP-REQ-F-011** (business rule): If no customer exists with the requested customer number (SQLCODE 100), then the system shall return code '01' without writing an error log entry. Rules: UP-BR-031.
- **UP-REQ-F-012** (error handling): If the customer lookup fails because of a database deadlock or timeout (SQLCODE -913), then the system shall return code '01', the same code as customer not found, without writing an error log entry. Rules: UP-BR-032.
- **UP-REQ-F-013** (error handling): If the customer lookup fails with any other database error, then the system shall return code '90' and write an error log entry with date, time, customer number and SQLCODE, followed by up to the first 90 bytes of the request, via the logging program (LGSTSQ). Rules: UP-BR-033.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-023 | Customer data requests must carry a request area | error handling | WHEN the customer inquiry database program receives no request data (a length of zero), THE Customer Inquiry SHALL log the message ' NO COMMAREA RECEIVED' with the date and time, and end the transaction abnormally with abend code 'LGCA'. | medium | base/src/lgicdb01.cbl:118-123, base/src/lgicdb01.cbl:212-228 |
| UP-BR-024 | Reject invocation without request data | error handling | WHEN the customer inquiry service is started with no request data, THE customer inquiry service SHALL log the error ' NO COMMAREA RECEIVED' with date and time to the error queue and end abnormally with abend code 'LGCA' without a dump. | medium | base/src/lgicus01.cbl:87-91, base/src/lgicus01.cbl:135-149 |
| UP-BR-025 | Default success outcome and policy count | design note | WHEN a customer inquiry request with data is received, THE customer inquiry service SHALL first set the return code to '00' (success) and the number of policies to '00' before checking the request length. | medium | base/src/lgicus01.cbl:87-95 |
| UP-BR-026 | Reject request shorter than required length | business rule | WHEN a customer inquiry request is shorter than 90 bytes (72 bytes of customer data plus 18 bytes of header and trailer), THE Customer Inquiry SHALL return outcome code '98' to the caller without looking up the customer; otherwise it SHALL continue with outcome code '00'. | high | base/src/lgicdb01.cbl:58-60, base/src/lgpolicy.cpy:17, base/src/lgicdb01.cbl:125-126, base/src/lgicdb01.cbl:136-143 |
| UP-BR-027 | Reject request shorter than required length | business rule | WHEN a customer inquiry request is shorter than the customer record length (72) plus the header and trailer length (18), i.e. under 90 bytes, THE customer inquiry service SHALL set the return code to '98' and return to the caller without looking up the customer. | medium | base/src/lgicus01.cbl:102-107, base/src/lgpolicy.cpy:17, base/src/lgicus01.cbl:57 |
| UP-BR-028 | Reject undersized customer request | business rule | WHEN a customer inquiry request is shorter than 90 bytes (customer record length 72 plus header and trailer length 18), THE customer inquiry service SHALL return to the caller with return code '98' without calling the customer database service. | medium | base/src/lgicus01.cbl:102-109 |
| UP-BR-029 | Delegate customer lookup to database service | design note | WHEN a customer inquiry request is at least 90 bytes long, THE customer inquiry service SHALL pass the whole request (32500 bytes) to the customer database service (LGICDB01) to look up the customer and return its result to the caller. | medium | base/src/lgicus01.cbl:93-94, base/src/lgicus01.cbl:109, base/src/lgicus01.cbl:120-125 |
| UP-BR-030 | Retrieve customer details by customer number | business rule | WHEN a customer inquiry passes the request checks, THE Customer Inquiry SHALL look up the customer by customer number in the CUSTOMER table and return first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address, with outcome code '00'. | high | base/src/lgicdb01.cbl:145-154, base/src/lgicdb01.cbl:167-205, base/src/lgicdb01.cbl:212-244 |
| UP-BR-031 | Report customer not found or unavailable | business rule | WHEN no customer exists with the requested customer number (SQLCODE 100), THE Customer Inquiry SHALL return outcome code '01' without writing an error log entry. | high | base/src/lgicdb01.cbl:145-154, base/src/lgicdb01.cbl:167-205, base/src/lgicdb01.cbl:212-244 |
| UP-BR-032 | Report customer not found or unavailable | error handling | WHEN the customer lookup fails because of a database deadlock or timeout (SQLCODE -913), THE Customer Inquiry SHALL return outcome code '01', the same code as customer not found, without writing an error log entry. | high | base/src/lgicdb01.cbl:145-154, base/src/lgicdb01.cbl:167-205, base/src/lgicdb01.cbl:212-244 |
| UP-BR-033 | Customer inquiry outcome classification | error handling | WHEN the customer lookup fails with any other database error, THE Customer Inquiry SHALL return outcome code '90' and write an error log entry with date, time, customer number and SQLCODE, followed by up to the first 90 bytes of the request, via the logging program (LGSTSQ). | high | base/src/lgicdb01.cbl:145-154, base/src/lgicdb01.cbl:167-205, base/src/lgicdb01.cbl:212-244 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- DEF-007: Confirm this is deliberate: The only caller in the source (LGICUS01) always links with a length of 32500 and already makes the same 90-byte check itself, so this check can never fail in practice. It is a defensive duplicate. (Subject-matter expert) On UP-BR-026.
- DEF-008: Is this intended? Error log entries written by LGICDB01 carry the program name ' LGICUS01', not LGICDB01, so database errors look as if they came from the front-end program. Also, a deadlock or timeout (-913) returns the same '01' code as customer not found, so callers report a temporary database problem as a missing customer. (Subject-matter expert) On UP-BR-030, UP-BR-032, UP-BR-033.
- DEF-060: Is this intended? The logged message names the program as ' LGICUS01' rather than LGICDB01. Also, the only caller in the source always passes 32500 bytes, so this abend cannot be triggered through the application. (Subject-matter expert) On UP-BR-023.

### Decision table gaps

None.
