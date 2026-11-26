# Requirements: List commercial policies by customer or postcode (UP-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk high

## Introduction

Searches commercial policies for policy administrators by customer number ('03ICOM') or by property postcode ('05ICOM'). As built today, the reply holds only the last policy read: a customer search stops after the 21st policy, a postcode search reads every match, and no match still returns code '00'. A search that cannot be started must return '89', and one that cannot be closed must return '88', each with an error message logged.

**User story:** As a policy administrator, I want to search commercial policies by customer or by property postcode, so that I can find commercial policies matching those criteria.

## Requirements

### Requirement 1: UP-REQ-F-045 (business rule)

#### Acceptance criteria

1. When a commercial policy inquiry by customer (request '03ICOM') is made, the system shall read the customer's commercial policies one at a time, placing each row's customer number, policy number, common policy details and commercial property details into the response, so the response ends up holding only the last row read. (rules UP-BR-067)
2. GIVEN request: '03ICOM'; customer number: 0000000004; commercial policies held: 3 (policies 101, 102, 103) WHEN a commercial policy inquiry by customer (request '03ICOM') is made THEN All 3 rows are read; the response shows policy 103 only, with return code '00'. (UP-C08-AC-01; UP-BR-067)

### Requirement 2: UP-REQ-F-046 (business rule)

#### Acceptance criteria

1. When more than 20 commercial policies have been read for a customer inquiry ('03ICOM'), the system shall stop reading after the 21st row, leaving the 21st row in the response and the return code at '00'. (rules UP-BR-068)
2. GIVEN request: '03ICOM'; commercial policies held by customer: 25 WHEN more than 20 commercial policies have been read for a customer inquiry ('03ICOM') THEN 21 rows are read, reading stops, the response holds the 21st row and return code '00'. (UP-C08-AC-02; UP-BR-068)
3. GIVEN request: '03ICOM'; commercial policies held by customer: 20 WHEN more than 20 commercial policies have been read for a customer inquiry ('03ICOM') THEN All 20 rows are read and the response holds the 20th row. (UP-C08-AC-03; UP-BR-068)

### Requirement 3: UP-REQ-F-047 (business rule)

#### Acceptance criteria

1. When a commercial policy inquiry by property postcode (request '05ICOM') is made, the system shall read every commercial policy whose property postcode matches, with no limit on the number of rows, placing each row's customer number, policy number, common and commercial details into the response, so only the last row read is returned. (rules UP-BR-069)
2. GIVEN request: '05ICOM'; postcode: SO21 2JN; matching commercial policies: 30 WHEN a commercial policy inquiry by property postcode (request '05ICOM') is made THEN All 30 rows are read; the response holds the 30th row with return code '00'. (UP-C08-AC-04; UP-BR-069)

### Requirement 4: UP-REQ-F-048 (error handling)

#### Acceptance criteria

1. If a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be started, then the system shall set return code '89', write an error message with date, time, customer number, policy number and SQL code to the error queue, and end the request. (rules UP-BR-070)
2. GIVEN request: '03ICOM'; database list open: fails WHEN a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be started THEN Return code '89', error message logged, request ends. (UP-C08-AC-05; UP-BR-070)

### Requirement 5: UP-REQ-F-049 (error handling)

#### Acceptance criteria

1. If a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be closed after reading, then the system shall set return code '88', write an error message to the error queue, and end the request. (rules UP-BR-071)
2. GIVEN request: '05ICOM'; database list close: fails WHEN a commercial policy list by customer ('03ICOM') or by postcode ('05ICOM') cannot be closed after reading THEN Return code '88', error message logged, request ends. (UP-C08-AC-06; UP-BR-071)

### Requirement 6: UP-REQ-F-050 (business rule)

#### Acceptance criteria

1. When no commercial policy matches the customer ('03ICOM') or postcode ('05ICOM'), the system shall return code '00' with no policy details filled in, rather than a not-found code. (rules UP-BR-072)
2. GIVEN request: '05ICOM'; postcode: ZZ99 9ZZ; matching commercial policies: none WHEN no commercial policy matches the customer ('03ICOM') or postcode ('05ICOM') THEN Return code '00'; no policy row in the response. (UP-C08-AC-07; UP-BR-072)
