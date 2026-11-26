# Requirements: Create the new customer's security record (CRCM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as scheduled job · risk high

## Introduction

Creates the sign-on security record for every new customer: the customer number, the initial password, a password change count of zero and the state 'N'. Only a new-customer security request (type '02ACUS') may add a record, and any other type is refused with '99'. It must never skip a new customer or add a security record for a request that is not a new-customer request.

**User story:** As a customer service user, I want a security record to be created for each new customer, so that the customer has sign-on credentials from the start.

## Requirements

### Requirement 1: CRCM-REQ-F-015 (business rule)

#### Acceptance criteria

1. When a new customer has been added and assigned a customer number, the system shall request a customer security record with request type '02ACUS', the new customer number, initial password '5732fec825535eeafb8fac50fee3a8aa', attempt count '0000' and state 'N'. (rules CRCM-BR-021)
2. GIVEN CA-REQUEST-ID: '01ACUS'; Assigned customer number: 1000042 WHEN a new customer has been added and assigned a customer number THEN LGACDB01 LINKs to 'LGACDB02' with D2-REQUEST-ID '02ACUS', D2-CUSTOMER-NUM 1000042, D2-CUSTSECR-PASS '5732fec825535eeafb8fac50fee3a8aa', D2-CUSTSECR-COUNT '0000' and D2-CUSTSECR-STATE 'N' (CRCM-C04-AC-01; CRCM-BR-021)

### Requirement 2: CRCM-REQ-F-016 (business rule)

#### Acceptance criteria

1. When the security add request type is '02ACUS' (new customer), the system shall convert the customer number and password change count to numbers and insert the customer number, password, state indicator and password change count into the customer secure table (CUSTOMER_SECURE). (rules CRCM-BR-022, CRCM-BR-023)
2. GIVEN request type: '02ACUS'; customer number: 0000000123; change count: '0000' WHEN the security add request type is '02ACUS' (new customer) THEN A security record is inserted for customer 123 with 0 password changes (CRCM-C04-AC-02; CRCM-BR-022)
3. GIVEN customer number: 0000000123; password: '5732fec825535eeafb8fac50fee3a8aa'; state: 'N'; change count: '0000' WHEN a new-customer security add is requested THEN A CUSTOMER_SECURE row is added for customer 123 (CRCM-C04-AC-03; CRCM-BR-023)

### Requirement 3: CRCM-REQ-F-017 (business rule)

#### Acceptance criteria

1. If the security add request type is anything other than '02ACUS', then the system shall set return code '99' and return without adding a record. (rules CRCM-BR-024)
2. GIVEN A security add request has request type '01UCUS' and customer number 0000001234 WHEN Customer security registration processes the request THEN The return code is '99', and no row is added to the customer secure table for customer 0000001234 (CRCM-C04-AC-05; CRCM-BR-024)

### Requirement 4: CRCM-REQ-F-018 (error handling)

#### Acceptance criteria

1. If inserting the security record fails, then the system shall set return code '98', log an error labelled ' INSERT SECURITY' with the SQL code, date and time, and return to the caller. (rules CRCM-BR-025)
2. GIVEN insert result: SQL code -803 WHEN inserting the security record fails THEN Return code '98'; ' INSERT SECURITY' error logged (CRCM-C04-AC-04; CRCM-BR-025)
