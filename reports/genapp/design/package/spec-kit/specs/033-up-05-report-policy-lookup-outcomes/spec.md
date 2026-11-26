# Feature specification: Report policy lookup outcomes

**Feature:** UP-C05 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C05)

As a customer service user, I want a clear outcome code when a policy cannot be returned, so that I know whether the policy does not exist, my request area was too small, or the system failed, and support staff can investigate failures.

Tells customer service users and calling applications why a policy could not be returned: '01' when the customer or policy does not match, '98' when the caller's reply area is too small, and '90' when the database failed. A plain not-found must never be logged. Every '90' failure must reach the error log with the customer, policy, lookup and database code, so support staff can investigate.

**Acceptance scenarios:**

1. **Given** request: '01IMOT'; customer number: 0000000002; policy number: 0000000777 (does not exist), **when** no policy matches the customer number and policy number for the requested policy type, **then** Return code '01'; no policy data and no error log. (UP-C05-AC-01)
2. **Given** request: '02ICOM'; policy number: 9999999999 (not on file), **when** a commercial inquiry by policy number alone ('02ICOM') finds no matching policy, **then** Return code '01'; no policy data is returned. (UP-C05-AC-02)
3. **Given** request: '01IEND'; database result: unavailable (SQLCODE -904), **when** the policy lookup fails for any reason other than no matching policy, **then** Return code '90' and an error log is written. (UP-C05-AC-03)
4. **Given** request: '02ICOM'; database result: SQLCODE -904 (resource unavailable), **when** a commercial inquiry by policy number alone ('02ICOM') fails for any reason other than the policy not existing, **then** Return code '90'; an error message is logged. (UP-C05-AC-04)
5. **Given** Caller's area length: 150; Space needed: 197, **when** the caller's request area is smaller than the space needed for the endowment reply, **then** Return code '98'; no policy data is returned and no 'FINAL' marker is written. (UP-C05-AC-05)
6. **Given** Caller's area length: 200; Space needed: 197, **when** the caller's request area is smaller than the space needed for the endowment reply, **then** The policy data is returned. (UP-C05-AC-06)
7. **Given** A house policy inquiry ('01IHOU') for customer number 0000000001 and policy number 0000000001, where the house policy lookup fails with a database error other than not found, **when** The inquiry sets return code '90', **then** The error log program (LGSTSQ) first receives a message with the date, time, 'LGIPDB01', customer number 0000000001, policy number 0000000001, the label ' SELECT HOUSE ' and the database code. It then receives a second message with up to the first 90 bytes of the request (UP-C05-AC-07)
8. **Given** An endowment, motor or commercial policy inquiry whose lookup fails with return code '90', **when** The error is logged, **then** The first message carries the label ' SELECT ENDOW ', ' SELECT MOTOR ' or ' SELECT Commercial ' to match the lookup, with the date, time, 'LGIPDB01', customer number, policy number and database code. The second message carries up to the first 90 bytes of the request (UP-C05-AC-08)

## Requirements

### Functional requirements

- **UP-REQ-F-024** (error handling): If no policy matches the customer number and policy number for the requested policy type, then the system shall set return code '01' (customer or policy not valid) and write no error log. Rules: UP-BR-045.
- **UP-REQ-F-025** (error handling): If a commercial inquiry by policy number alone ('02ICOM') finds no matching policy, then the system shall return code '01'. Rules: UP-BR-046.
- **UP-REQ-F-026** (error handling): If the policy lookup fails for any reason other than no matching policy, then the system shall set return code '90' and write an error log. Rules: UP-BR-047.
- **UP-REQ-F-027** (error handling): If a commercial inquiry by policy number alone ('02ICOM') fails for any reason other than the policy not existing, then the system shall return code '90' and write an error message with date, time, customer number, policy number and database code to the error log queue. Rules: UP-BR-048.
- **UP-REQ-F-028** (side effect): When a policy lookup fails with return code '90', the system shall send the error log program (LGSTSQ) a message with date, time, 'LGIPDB01', customer number, policy number, the lookup label (' SELECT ENDOW ', ' SELECT HOUSE ', ' SELECT MOTOR ' or ' SELECT Commercial ') and the database code, then a second message with up to the first 90 bytes of the request. Rules: UP-BR-049.
- **UP-REQ-F-029** (error handling): If the caller's request area is smaller than the space needed for the endowment reply, then the system shall set return code '98' and return to the caller without any policy details. Rules: UP-BR-050.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-045 | Report endowment lookup failure | error handling | WHEN no policy matches the customer number and policy number for the requested policy type, THE Policy Inquiry SHALL set return code '01' (customer or policy not valid) and write no error log. | high | base/src/lgipdb01.cbl:327-431, base/src/lgipdb01.cbl:441-523, base/src/lgipdb01.cbl:529-621, base/src/lgipdb01.cbl:627-724 |
| UP-BR-046 | Report commercial policy-number lookup failure | error handling | WHEN a commercial inquiry by policy number alone ('02ICOM') finds no matching policy, THE Commercial Policy Inquiry SHALL return code '01'. | medium | base/src/lgipdb01.cbl:730-782, base/src/lgipdb01.cbl:815-826, base/src/lgipdb01.cbl:992-1030 |
| UP-BR-047 | Report endowment lookup failure | error handling | WHEN the policy lookup fails for any reason other than no matching policy, THE Policy Inquiry SHALL set return code '90' and write an error log. | high | base/src/lgipdb01.cbl:327-431, base/src/lgipdb01.cbl:441-523, base/src/lgipdb01.cbl:529-621, base/src/lgipdb01.cbl:627-724 |
| UP-BR-048 | Report commercial policy-number lookup failure | error handling | WHEN a commercial inquiry by policy number alone ('02ICOM') fails for any reason other than the policy not existing, THE Commercial Policy Inquiry SHALL return code '90' and write an error message with date, time, customer number, policy number and database code to the error log queue. | medium | base/src/lgipdb01.cbl:730-782, base/src/lgipdb01.cbl:815-826, base/src/lgipdb01.cbl:992-1030 |
| UP-BR-049 | Retrieve endowment policy details | side effect | WHEN a lookup fails with return code '90', THE Policy Inquiry SHALL send the error log program (LGSTSQ) a message with date, time, 'LGIPDB01', customer number, policy number, the lookup label (' SELECT ENDOW ', ' SELECT HOUSE ', ' SELECT MOTOR ' or ' SELECT Commercial ') and the database code, then a second message with up to the first 90 bytes of the request. | high | base/src/lgipdb01.cbl:327-431, base/src/lgipdb01.cbl:441-523, base/src/lgipdb01.cbl:529-621, base/src/lgipdb01.cbl:627-724 |
| UP-BR-050 | Reject endowment inquiry for insufficient space | error handling | WHEN the caller's request area is smaller than the space needed for the endowment reply, THE Policy Inquiry SHALL set return code '98' and return to the caller without any policy details. | high | base/src/lgipdb01.cbl:327-368, base/src/lgipdb01.cbl:370-417, base/src/lgipdb01.cbl:73, base/src/lgipdb01.cbl:78 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-048, UP-BR-050, UP-BR-047, UP-BR-049.

### Decision table gaps

- Policy lookup outcome: Reply sizes are worked out for house, motor and commercial (R46), but no rule says what happens when the caller's area is too small for them; confirm whether return code '98' applies.
- Policy lookup outcome: No rule gives the return code or logging when a 03ICOM or 05ICOM lookup finds nothing or fails.
