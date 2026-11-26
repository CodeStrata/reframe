# Design: Route policy inquiries by request type (UP-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Sends each policy inquiry to the right lookup for its request ID. The lookups are endowment, house, motor, and four commercial searches: by customer and policy, by policy number alone, by customer, and by postcode. The request ID must match in any letter case. Any ID other than '01IEND', '01IHOU', '01IMOT', '01ICOM', '02ICOM', '03ICOM' or '05ICOM' must get code '99' and no policy data.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

- LGCMAREA (working storage of LGIPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGIPDB01): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- UP-BR-034: request = '01IHOU'; policy found = yes → Return code '00'.
- UP-BR-035: customer number = 0000000001; policy number = 0000000005; request ID = 01IMOT → Return code starts as '00' and customer 0000000001 / policy 0000000005 are used for the motor lookup
- UP-BR-036: request ID = 01ihou → Treated as '01IHOU' and a house policy lookup is performed
- UP-BR-037: request ID = 04ICOM → Return code '99'; no policy data returned
- UP-BR-037: request ID = 01IXYZ → Return code '99'; no policy data returned
- UP-BR-038: request ID = 01IEND; customer number = 0000000001; policy number = 0000000002 → Endowment details of policy 0000000002 for customer 0000000001 are retrieved
- UP-BR-039: request ID = 01IHOU; customer number = 0000000001; policy number = 0000000003 → House details of policy 0000000003 for customer 0000000001 are retrieved
- UP-BR-040: request ID = 01IMOT; customer number = 0000000001; policy number = 0000000004 → Motor details of policy 0000000004 for customer 0000000001 are retrieved
- UP-BR-041: request ID = 01ICOM; customer number = 0000000001; policy number = 0000000006 → Commercial policy 0000000006 of customer 0000000001 is retrieved
- UP-BR-042: request ID = 02ICOM; policy number = 0000000006 → Commercial policy 0000000006 is retrieved without checking the customer
- UP-BR-043: request ID = 03ICOM; customer number = 0000000001 → All commercial policies of customer 0000000001 are listed
- UP-BR-044: request ID = 05ICOM; postcode = PO167GZ → All commercial policies with postcode PO167GZ are listed

## Decision tables

#### Policy inquiry routing by request ID

| Request ID (upper-cased) | Lookup performed | Rule |
|---|---|---|
| 01IEND | Clear endowment details; retrieve endowment policy by customer and policy number | UP-BR-038 |
| 01IHOU | Clear house details; retrieve house policy by customer and policy number | UP-BR-039 |
| 01IMOT | Clear motor details; retrieve motor policy by customer and policy number | UP-BR-040 |
| 01ICOM | Clear commercial details; retrieve commercial policy by customer and policy number | UP-BR-041 |
| 02ICOM | Clear commercial details; retrieve commercial policy by policy number alone | UP-BR-042 |
| 03ICOM | Clear commercial details; retrieve list of commercial policies for the customer | UP-BR-043 |
| 05ICOM | Clear commercial details; retrieve list of commercial policies by property postcode | UP-BR-044 |
| Any other value | Return code '99', no lookup, no policy data | UP-BR-037 |


## Design notes

- UP-BR-034: Every policy inquiry reply starts with return code '00'. Only a later failure (not found, reply area too small, database error or unknown request) changes it, so a request that runs cleanly always returns '00'.
- UP-BR-035: At the start of each policy inquiry, the supplied customer number and policy number become the lookup keys. They are also kept as context for error messages, so any error logged later names the customer and policy the caller asked for.

## Open questions

- SME-059: When commercial policies are listed by customer (03ICOM) or by postcode (05ICOM), should the caller get every matching policy or only one? Should the list by customer stop at 20 policies (today a 21st can slip through), and should the postcode search also be limited? (Commercial underwriting SME) On UP-BR-037, UP-BR-036, UP-BR-038, UP-BR-039, UP-BR-040, UP-BR-041, UP-BR-042, UP-BR-043, UP-BR-044.
- DEF-056: Confirm this is deliberate: LGIPDB01's no-request-area abend (LGCA) is defensive code that cannot fire through its only caller, which checks the same condition first and always passes 32500 bytes. (Subject-matter expert) On UP-BR-034.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (12 in all).