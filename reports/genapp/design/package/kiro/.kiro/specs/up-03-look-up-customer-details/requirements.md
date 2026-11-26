# Requirements: Look up customer details (UP-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk high

## Introduction

Looks up one customer by customer number for customer service users and calling applications. It returns the customer's name, date of birth, address, phone numbers and email. It must return '98' for a request shorter than 90 bytes, '01' for an unknown customer, and '90' with an error log entry for any other database failure. A request with no data must be logged as ' NO COMMAREA RECEIVED' and end with code 'LGCA'.

**User story:** As a customer service user, I want to retrieve a customer's details by customer number, so that I can see who the customer is and how to contact them.

## Requirements

### Requirement 1: UP-REQ-F-006 (error handling)

#### Acceptance criteria

1. If a customer inquiry is started with no request data (a length of zero), then the system shall log the message ' NO COMMAREA RECEIVED' with the date and time to the error queue and end the transaction abnormally with abend code 'LGCA' without a dump. (rules UP-BR-023, UP-BR-024)
2. GIVEN request length: 0 WHEN the customer inquiry database program receives no request data (a length of zero) THEN Message ' NO COMMAREA RECEIVED' logged; transaction abends with code 'LGCA' (UP-C03-AC-01; UP-BR-023)
3. GIVEN request length: 0 WHEN the customer inquiry service is started with no request data THEN Error ' NO COMMAREA RECEIVED' is logged and the task abends with 'LGCA' (UP-C03-AC-02; UP-BR-024)

### Requirement 2: UP-REQ-F-007 (business rule)

#### Acceptance criteria

1. When a customer inquiry request with data is received, the system shall first set the return code to '00' (success) and the number of policies to '00' before checking the request length. (rules UP-BR-025, UP-BR-026)
2. GIVEN request length: 32500; customer number: 0000000123 WHEN a customer inquiry request with data is received THEN Return code starts as '00' and policy count as '00' before the lookup (UP-C03-AC-03; UP-BR-025)
3. GIVEN request length: 85 bytes WHEN a customer inquiry request is shorter than 90 bytes (72 bytes of customer data plus 18 bytes of header and trailer) THEN Outcome code '98'; no customer lookup (UP-C03-AC-04; UP-BR-026)
4. GIVEN request length: 90 bytes WHEN a customer inquiry request is shorter than 90 bytes (72 bytes of customer data plus 18 bytes of header and trailer) THEN Request continues to the customer lookup (UP-C03-AC-05; UP-BR-026)

### Requirement 3: UP-REQ-F-008 (business rule)

#### Acceptance criteria

1. If a customer inquiry request is shorter than 90 bytes (customer record length 72 plus header and trailer length 18), then the system shall return to the caller with return code '98' without looking up the customer. (rules UP-BR-026, UP-BR-027, UP-BR-028)
2. GIVEN request length: 85 bytes WHEN a customer inquiry request is shorter than 90 bytes (72 bytes of customer data plus 18 bytes of header and trailer) THEN Outcome code '98'; no customer lookup (UP-C03-AC-04; UP-BR-026)
3. GIVEN request length: 90 bytes WHEN a customer inquiry request is shorter than 90 bytes (72 bytes of customer data plus 18 bytes of header and trailer) THEN Request continues to the customer lookup (UP-C03-AC-05; UP-BR-026)
4. GIVEN request length: 60 WHEN a customer inquiry request is shorter than the customer record length (72) plus the header and trailer length (18), i.e. under 90 bytes THEN Return code '98'; no customer lookup is made (UP-C03-AC-06; UP-BR-027)
5. GIVEN request length: 32500 WHEN a customer inquiry request is shorter than the customer record length (72) plus the header and trailer length (18), i.e. under 90 bytes THEN Length check passes and the customer lookup proceeds (UP-C03-AC-07; UP-BR-027)
6. GIVEN request length: 89 WHEN a customer inquiry request is shorter than 90 bytes (customer record length 72 plus header and trailer length 18) THEN Return code '98'; LGICDB01 is not called (UP-C03-AC-08; UP-BR-028)

### Requirement 4: UP-REQ-F-009 (design note)

#### Acceptance criteria

1. When a customer inquiry request is at least 90 bytes long, the system shall pass the whole request (32500 bytes) to the customer database service (LGICDB01) to look up the customer and return its result to the caller. (rules UP-BR-029)
2. GIVEN request length: 32500; customer number: 0000000123 WHEN a customer inquiry request is at least 90 bytes long THEN The request is handed to LGICDB01 and its outcome is returned to the caller (UP-C03-AC-09; UP-BR-029)

### Requirement 5: UP-REQ-F-010 (business rule)

#### Acceptance criteria

1. When a customer inquiry passes the request checks, the system shall look up the customer by customer number in the CUSTOMER table and return first name, last name, date of birth, house name, house number, postcode, mobile phone, home phone and email address, with return code '00'. (rules UP-BR-030)
2. GIVEN customer number: 0001000042; customer on file: yes WHEN a customer inquiry passes the request checks THEN Name, date of birth, address, phones and email are returned with outcome code '00' (UP-C03-AC-10; UP-BR-030)

### Requirement 6: UP-REQ-F-011 (business rule)

#### Acceptance criteria

1. If no customer exists with the requested customer number (SQLCODE 100), then the system shall return code '01' without writing an error log entry. (rules UP-BR-031)
2. GIVEN customer number: 0009999999; customer on file: no WHEN no customer exists with the requested customer number (SQLCODE 100) THEN Outcome code '01'; no customer details returned (UP-C03-AC-11; UP-BR-031)

### Requirement 7: UP-REQ-F-012 (error handling)

#### Acceptance criteria

1. If the customer lookup fails because of a database deadlock or timeout (SQLCODE -913), then the system shall return code '01', the same code as customer not found, without writing an error log entry. (rules UP-BR-032)
2. GIVEN customer number: 0001000042; database result: deadlock/timeout (-913) WHEN the customer lookup fails because of a database deadlock or timeout (SQLCODE -913) THEN Outcome code '01' (UP-C03-AC-12; UP-BR-032)

### Requirement 8: UP-REQ-F-013 (error handling)

#### Acceptance criteria

1. If the customer lookup fails with any other database error, then the system shall return code '90' and write an error log entry with date, time, customer number and SQLCODE, followed by up to the first 90 bytes of the request, via the logging program (LGSTSQ). (rules UP-BR-033)
2. GIVEN customer number: 0001000042; database result: SQLCODE -805 WHEN the customer lookup fails with any other database error THEN Outcome code '90'; error message and request data written to the log queue (UP-C03-AC-13; UP-BR-033)
