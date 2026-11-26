# Design: Look up customer details (UP-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Looks up one customer by customer number for customer service users and calling applications. It returns the customer's name, date of birth, address, phone numbers and email. It must return '98' for a request shorter than 90 bytes, '01' for an unknown customer, and '90' with an error log entry for any other database failure. A request with no data must be logged as ' NO COMMAREA RECEIVED' and end with code 'LGCA'.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGICDB01, LGICUS01): see data-contracts.md.
- LGPOLICY (working storage of LGICDB01, LGICUS01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- UP-BR-023: request length = 0 → Message ' NO COMMAREA RECEIVED' logged; transaction abends with code 'LGCA'
- UP-BR-024: request length = 0 → Error ' NO COMMAREA RECEIVED' is logged and the task abends with 'LGCA'
- UP-BR-025: request length = 32500; customer number = 0000000123 → Return code starts as '00' and policy count as '00' before the lookup
- UP-BR-026: request length = 85 bytes → Outcome code '98'; no customer lookup
- UP-BR-026: request length = 90 bytes → Request continues to the customer lookup
- UP-BR-027: request length = 60 → Return code '98'; no customer lookup is made
- UP-BR-027: request length = 32500 → Length check passes and the customer lookup proceeds
- UP-BR-028: request length = 89 → Return code '98'; LGICDB01 is not called
- UP-BR-029: request length = 32500; customer number = 0000000123 → The request is handed to LGICDB01 and its outcome is returned to the caller
- UP-BR-030: customer number = 0001000042; customer on file = yes → Name, date of birth, address, phones and email are returned with outcome code '00'
- UP-BR-031: customer number = 0009999999; customer on file = no → Outcome code '01'; no customer details returned
- UP-BR-032: customer number = 0001000042; database result = deadlock/timeout (-913) → Outcome code '01'
- UP-BR-033: customer number = 0001000042; database result = SQLCODE -805 → Outcome code '90'; error message and request data written to the log queue

## Decision tables

#### Customer inquiry outcome

| Request data received | Request length | Customer lookup result | Return code and logging | Rule |
|---|---|---|---|---|
| No (length zero) | - | - | Log ' NO COMMAREA RECEIVED' and abend 'LGCA' | UP-BR-023 |
| Yes | Under 90 bytes | Not attempted | Return code '98', no lookup | UP-BR-026 |
| Yes | At least 90 bytes | Customer found | Return customer details, return code '00' | UP-BR-030 |
| Yes | At least 90 bytes | Not found (SQLCODE 100) | Return code '01', no error log | UP-BR-031 |
| Yes | At least 90 bytes | Deadlock or timeout (SQLCODE -913) | Return code '01', no error log | UP-BR-032 |
| Yes | At least 90 bytes | Any other database error | Return code '90', error log via LGSTSQ | UP-BR-033 |


## Design notes

- UP-BR-025: Every customer inquiry reply starts as a success: return code '00' and number of policies '00' are set before any check runs. Later checks overwrite them only on failure.
- UP-BR-029: Once a request passes the length check, the inquiry calls the customer data service (LGICDB01 today) with the whole request (32500 bytes today). It passes that service's reply and return code back to the caller unchanged. In the new application this is a call from the inquiry API to the customer lookup service, keyed by customer number.

## Open questions

- DEF-007: Confirm this is deliberate: The only caller in the source (LGICUS01) always links with a length of 32500 and already makes the same 90-byte check itself, so this check can never fail in practice. It is a defensive duplicate. (Subject-matter expert) On UP-BR-026.
- DEF-008: Is this intended? Error log entries written by LGICDB01 carry the program name ' LGICUS01', not LGICDB01, so database errors look as if they came from the front-end program. Also, a deadlock or timeout (-913) returns the same '01' code as customer not found, so callers report a temporary database problem as a missing customer. (Subject-matter expert) On UP-BR-030, UP-BR-032, UP-BR-033.
- DEF-060: Is this intended? The logged message names the program as ' LGICUS01' rather than LGICDB01. Also, the only caller in the source always passes 32500 bytes, so this abend cannot be triggered through the application. (Subject-matter expert) On UP-BR-023.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).