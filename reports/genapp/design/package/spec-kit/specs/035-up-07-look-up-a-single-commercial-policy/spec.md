# Feature specification: Look up a single commercial policy

**Feature:** UP-C07 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C07)

As a policy administrator, I want to retrieve a commercial policy by customer and policy number or by policy number alone, so that I can see its stored peril values, premiums, status and owning customer.

Returns one commercial policy to policy administrators, found by customer and policy number or by policy number alone. It shows the policy's peril values, premiums, status and owning customer exactly as stored, with no recalculation. When the policy is found by policy number alone, the reply must name the customer who owns it, not the one the caller supplied, and a reply area smaller than 33 + 1174 bytes must get code '98'.

**Acceptance scenarios:**

1. **Given** request: '01ICOM'; policy found: yes, **when** commercial policy data has been returned for a customer-and-policy ('01ICOM') or policy-number ('02ICOM') inquiry, **then** 'FINAL' follows the rejection reason in the reply area. (UP-C07-AC-01)
2. **Given** Request: '02ICOM'; Policy number: 0000000012 (owned by customer 0000000003); Customer number: blank or any other customer, **when** a commercial policy inquiry by policy number (request '02ICOM') is made, **then** Policy 0000000012 is found. (UP-C07-AC-02)
3. **Given** Caller's area length: 1000, **when** a commercial policy is found by policy number, **then** Return code '98'; no policy data is returned. (UP-C07-AC-03)
4. **Given** Caller's area length: 32500, **when** a commercial policy is found by policy number, **then** The policy is returned. (UP-C07-AC-04)
5. **Given** Database lookup result: unexpected error (for example SQLCODE -911), **when** the commercial policy lookup by policy number fails for any reason other than the policy not being found, **then** Return code '90'; a ' SELECT Commercial ' error message is written to the error queue. (UP-C07-AC-05)
6. **Given** Database lookup result: no row (SQLCODE 100), **when** the commercial policy lookup by policy number fails for any reason other than the policy not being found, **then** Return code '01'; no error message is logged. (UP-C07-AC-06)
7. **Given** A commercial policy is stored with fire peril 3, fire premium 150, crime peril 2, crime premium 75, flood peril 1, flood premium 40, weather peril 4, weather premium 90, status 1 and rejection reason 'Inspection pending', **when** The policy is returned by a commercial inquiry, **then** The reply holds those values as plain numbers: fire peril 3, fire premium 150, crime peril 2, crime premium 75, flood peril 1, flood premium 40, weather peril 4, weather premium 90 and status 1. The rejection reason is the stored text 'Inspection pending', and nothing is recalculated (UP-C07-AC-07)
8. **Given** Commercial policy 0000000005 is owned by customer 0000000003, and the caller's reply area is at least 33 + 1174 bytes, **when** A '02ICOM' inquiry arrives with policy number 0000000005 and customer number 0000000009, **then** The reply carries customer number 0000000003 in place of 0000000009, with the common policy details and commercial details, and the data ends with 'FINAL' (UP-C07-AC-08)

## Requirements

### Functional requirements

- **UP-REQ-F-039** (formatting): When a commercial policy is returned, the system shall report the peril values, premiums and status exactly as stored, converted to plain numbers, and the rejection reason as stored text, with no recalculation. Rules: UP-BR-061.
- **UP-REQ-F-040** (design note): When commercial policy data has been returned for a customer-and-policy ('01ICOM') or policy-number ('02ICOM') inquiry, the system shall write 'FINAL' in the first 5 positions of the free space after the rejection reason. Rules: UP-BR-062.
- **UP-REQ-F-041** (business rule): When a commercial policy inquiry by policy number (request '02ICOM') is made, the system shall look up the commercial policy by policy number alone, without checking that it belongs to the customer number supplied. Rules: UP-BR-063.
- **UP-REQ-F-042** (error handling): If a commercial policy is found by policy number and the caller's area is smaller than 33 plus 1174 bytes, then the system shall set return code '98' and return without policy details. Rules: UP-BR-064.
- **UP-REQ-F-043** (business rule): When a commercial policy is found by policy number and the caller's area is large enough, the system shall return the owning customer number in place of the one supplied, with the common policy and commercial details, and mark the end of the data with 'FINAL'. Rules: UP-BR-065.
- **UP-REQ-F-044** (error handling): If the commercial policy lookup by policy number fails for any reason other than the policy not being found, then the system shall set return code '90' and log an error message labelled ' SELECT Commercial ' with the date, time, customer number, policy number and database code, plus up to the first 90 bytes of the request. Rules: UP-BR-066.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-061 | Return commercial policy by customer and policy | formatting | WHEN a commercial policy is returned, THE Commercial Policy Inquiry SHALL report the peril values, premiums and status exactly as stored, converted to plain numbers, and the rejection reason as stored text, with no recalculation. | high | base/src/lgipdb01.cbl:627-708, base/src/lgipdb01.cbl:808-813, base/src/lgpolicy.cpy:83-99, base/src/lgcmarea.cpy:78-94 |
| UP-BR-062 | Return commercial policy by customer and policy | design note | WHEN commercial policy data has been returned for a customer-and-policy ('01ICOM') or policy-number ('02ICOM') inquiry, THE Commercial Policy Inquiry SHALL write 'FINAL' in the first 5 positions of the free space after the rejection reason. | high | base/src/lgipdb01.cbl:627-708, base/src/lgipdb01.cbl:808-813, base/src/lgpolicy.cpy:83-99, base/src/lgcmarea.cpy:78-94 |
| UP-BR-063 | Retrieve commercial policy by policy only | business rule | WHEN a commercial policy inquiry by policy number (request '02ICOM') is made, THE Policy Inquiry SHALL look up the commercial policy by policy number alone, without checking that it belongs to the customer number supplied. | high | base/src/lgipdb01.cbl:295-297, base/src/lgipdb01.cbl:726-829, base/src/lgipdb01.cbl:993-1030, base/src/lgpolicy.cpy:27 |
| UP-BR-064 | Return commercial policy by policy number | error handling | WHEN a commercial policy is found by policy number, THE Policy Inquiry SHALL work out the space needed as 33 plus 1174 bytes, and if the caller's area is smaller SHALL set return code '98' and return without policy details. | high | base/src/lgipdb01.cbl:295-297, base/src/lgipdb01.cbl:726-829, base/src/lgipdb01.cbl:993-1030, base/src/lgpolicy.cpy:27 |
| UP-BR-065 | Return commercial policy by policy number | business rule | WHEN a commercial policy is found by policy number and the caller's area is large enough, THE Policy Inquiry SHALL return the owning customer number in place of the one supplied, with the common policy and commercial details, and mark the end of the data with 'FINAL'. | high | base/src/lgipdb01.cbl:295-297, base/src/lgipdb01.cbl:726-829, base/src/lgipdb01.cbl:993-1030, base/src/lgpolicy.cpy:27 |
| UP-BR-066 | Retrieve commercial policy by policy only | error handling | WHEN the commercial policy lookup by policy number fails for any reason other than the policy not being found, THE Policy Inquiry SHALL set return code '90' and log an error message labelled ' SELECT Commercial ' with the date, time, customer number, policy number and database code, plus up to the first 90 bytes of the request. | high | base/src/lgipdb01.cbl:295-297, base/src/lgipdb01.cbl:726-829, base/src/lgipdb01.cbl:993-1030, base/src/lgpolicy.cpy:27 |

### Key entities

- LGCMAREA (working storage)
- LGPOLICY (working storage)

### Needs clarification

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-062, UP-BR-065, UP-BR-066.
- SME-062: What are the valid status values for a commercial policy and what does each mean (for example quoted, accepted, rejected)? Which part of the system sets them? (Commercial underwriting SME) On UP-BR-061.
- SME-063: Anyone with a policy number can look up a commercial policy (02ICOM) without any check that the policy belongs to their customer. Is this meant to be a back-office lookup? Should the new system check customer ownership or user role? (Security / compliance officer) On UP-BR-065.
- DEF-017: Confirm this is deliberate: The '98' reply-too-small check can never trigger: the only caller, LGIPOL01, always passes a 32500-byte area, far more than the 1207 bytes needed. (Subject-matter expert) On UP-BR-061, UP-BR-062.
- DEF-026: Confirm this is deliberate: An inquiry by policy number alone returns any commercial policy, and the owning customer's number, to the caller, without checking that the caller's customer owns the policy. The header comment and the calling screen (which uses '02ICOM' only when no customer number is given) show this is intended as a lookup by policy number. (Subject-matter expert) On UP-BR-065, UP-BR-066.

### Decision table gaps

- Commercial policy single inquiry outcomes: No rule says what return code or response is given when the policy number does not exist.
- Commercial policy single inquiry outcomes: No rule covers a customer-and-policy inquiry that finds no matching policy.
- Commercial policy single inquiry outcomes: No rule covers a database failure on the customer-and-policy inquiry.
- Commercial policy single inquiry outcomes: No rule says whether the caller's area size is checked for the customer-and-policy inquiry.
