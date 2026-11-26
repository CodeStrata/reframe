# Feature specification: Route policy inquiries by request type

**Feature:** UP-C04 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C04)

As a customer service user, I want my policy inquiry routed to the right lookup for the policy type I ask for, so that I get the correct endowment, house, motor or commercial policy information.

Sends each policy inquiry to the right lookup for its request ID. The lookups are endowment, house, motor, and four commercial searches: by customer and policy, by policy number alone, by customer, and by postcode. The request ID must match in any letter case. Any ID other than '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM' must get code '99' and no policy data.

**Acceptance scenarios:**

1. **Given** request: '01IHOU'; policy found: yes, **when** Policy Inquiry runs, **then** Return code '00'. (UP-C04-AC-01)
2. **Given** customer number: 0000000001; policy number: 0000000005; request ID: 01IMOT, **when** a policy inquiry is received with a request, **then** Return code starts as '00' and customer 0000000001 / policy 0000000005 are used for the motor lookup (UP-C04-AC-02)
3. **Given** request ID: 01ihou, **when** Policy Inquiry service runs, **then** Treated as '01IHOU' and a house policy lookup is performed (UP-C04-AC-03)
4. **Given** request ID: 04ICOM, **when** the request ID, after upper-casing, is not '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM', **then** Return code '99'; no policy data returned (UP-C04-AC-04)
5. **Given** request ID: 01IXYZ, **when** the request ID, after upper-casing, is not '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM', **then** Return code '99'; no policy data returned (UP-C04-AC-05)
6. **Given** request ID: 01IEND; customer number: 0000000001; policy number: 0000000002, **when** the request ID is '01IEND', **then** Endowment details of policy 0000000002 for customer 0000000001 are retrieved (UP-C04-AC-06)
7. **Given** request ID: 01IHOU; customer number: 0000000001; policy number: 0000000003, **when** the request ID is '01IHOU', **then** House details of policy 0000000003 for customer 0000000001 are retrieved (UP-C04-AC-07)
8. **Given** request ID: 01IMOT; customer number: 0000000001; policy number: 0000000004, **when** the request ID is '01IMOT', **then** Motor details of policy 0000000004 for customer 0000000001 are retrieved (UP-C04-AC-08)
9. **Given** request ID: 01ICOM; customer number: 0000000001; policy number: 0000000006, **when** the request ID is '01ICOM', **then** Commercial policy 0000000006 of customer 0000000001 is retrieved (UP-C04-AC-09)
10. **Given** request ID: 02ICOM; policy number: 0000000006, **when** the request ID is '02ICOM', **then** Commercial policy 0000000006 is retrieved without checking the customer (UP-C04-AC-10)
11. **Given** request ID: 03ICOM; customer number: 0000000001, **when** the request ID is '03ICOM', **then** All commercial policies of customer 0000000001 are listed (UP-C04-AC-11)
12. **Given** request ID: 05ICOM; postcode: PO167GZ, **when** the request ID is '05ICOM', **then** All commercial policies with postcode PO167GZ are listed (UP-C04-AC-12)

## Requirements

### Functional requirements

- **UP-REQ-F-014** (design note): When a policy inquiry is received with a request, the system shall start with return code '00', which is returned unless a later step sets another code, and use the supplied customer number and policy number as the lookup keys, keeping both for any error message it writes. Rules: UP-BR-034, UP-BR-035.
- **UP-REQ-F-015** (business rule): The system shall match the policy inquiry request ID regardless of letter case, converting it to upper case before choosing the lookup. Rules: UP-BR-036.
- **UP-REQ-F-016** (business rule): If the request ID, after upper-casing, is not '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM', then the system shall return code '99' and perform no lookup, returning no policy data. Rules: UP-BR-037.
- **UP-REQ-F-017** (business rule): When the request ID is '01IEND', the system shall clear the endowment details and retrieve the endowment policy for the given customer and policy number. Rules: UP-BR-038.
- **UP-REQ-F-018** (business rule): When the request ID is '01IHOU', the system shall clear the house details and retrieve the house policy for the given customer and policy number. Rules: UP-BR-039.
- **UP-REQ-F-019** (business rule): When the request ID is '01IMOT', the system shall clear the motor details and retrieve the motor policy for the given customer and policy number. Rules: UP-BR-040.
- **UP-REQ-F-020** (business rule): When the request ID is '01ICOM', the system shall clear the commercial details and retrieve the commercial policy matching both the given customer number and policy number. Rules: UP-BR-041.
- **UP-REQ-F-021** (business rule): When the request ID is '02ICOM', the system shall clear the commercial details and retrieve the commercial policy by policy number alone, whatever customer number is supplied. Rules: UP-BR-042.
- **UP-REQ-F-022** (business rule): When the request ID is '03ICOM', the system shall clear the commercial details and retrieve the list of commercial policies held by the given customer number. Rules: UP-BR-043.
- **UP-REQ-F-023** (business rule): When the request ID is '05ICOM', the system shall clear the commercial details and retrieve the list of commercial policies whose property postcode equals the supplied postcode (CA-B-POSTCODE). Rules: UP-BR-044.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-034 | Missing request area aborts the transaction | design note | THE Policy Inquiry SHALL start every request with return code '00', which is returned unless a later step sets another code. | medium | base/src/lgipdb01.cbl:251-258, base/src/lgipol01.cbl:79-93 |
| UP-BR-035 | Prepare inquiry keys and default outcome | design note | WHEN a policy inquiry is received with a request, THE Policy Inquiry service SHALL start with return code '00', use the supplied customer number and policy number as the lookup keys, and keep both for any error message it writes. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-036 | Prepare inquiry keys and default outcome | business rule | THE Policy Inquiry service SHALL match the request ID regardless of letter case, converting it to upper case before choosing the lookup. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-037 | Reject unrecognised request type | business rule | WHEN the request ID, after upper-casing, is not '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM', THE Policy Inquiry service SHALL return code '99' and perform no lookup, returning no policy data. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-038 | Route endowment policy inquiry | business rule | WHEN the request ID is '01IEND', THE Policy Inquiry service SHALL clear the endowment details and retrieve the endowment policy for the given customer and policy number. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-039 | Route house policy inquiry | business rule | WHEN the request ID is '01IHOU', THE Policy Inquiry service SHALL clear the house details and retrieve the house policy for the given customer and policy number. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-040 | Route motor policy inquiry | business rule | WHEN the request ID is '01IMOT', THE Policy Inquiry service SHALL clear the motor details and retrieve the motor policy for the given customer and policy number. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-041 | Route commercial inquiry by customer and policy | business rule | WHEN the request ID is '01ICOM', THE Policy Inquiry service SHALL clear the commercial details and retrieve the commercial policy matching both the given customer number and policy number. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-042 | Route commercial inquiry by policy only | business rule | WHEN the request ID is '02ICOM', THE Policy Inquiry service SHALL clear the commercial details and retrieve the commercial policy by policy number alone, whatever customer number is supplied. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-043 | Route commercial policies list for customer | business rule | WHEN the request ID is '03ICOM', THE Policy Inquiry service SHALL clear the commercial details and retrieve the list of commercial policies held by the given customer number. | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |
| UP-BR-044 | Route commercial policies search by postcode | business rule | WHEN the request ID is '05ICOM', THE Policy Inquiry service SHALL clear the commercial details and retrieve the list of commercial policies whose property postcode equals the supplied postcode (CA-B-POSTCODE). | high | base/src/lgipdb01.cbl:251-267, base/src/lgipdb01.cbl:275-310, base/src/lgipdb01.cbl:114-117, base/src/lgipdb01.cbl:145-148 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-037, UP-BR-036, UP-BR-038, UP-BR-039, UP-BR-040, UP-BR-041, UP-BR-042, UP-BR-043, UP-BR-044.
- DEF-056: Confirm this is deliberate: LGIPDB01's no-request-area abend (LGCA) is defensive code that cannot fire through its only caller, which checks the same condition first and always passes 32500 bytes. (Subject-matter expert) On UP-BR-034.

### Decision table gaps

None.
