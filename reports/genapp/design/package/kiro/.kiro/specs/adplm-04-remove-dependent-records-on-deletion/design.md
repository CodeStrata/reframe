# Design: Remove dependent records on deletion (ADPLM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

When a customer or a policy is deleted, everything recorded against it is deleted too: policies, their endowment, house, motor and commercial details, their claims, and the customer's security record. It is for insurance operations, who need the records to stay consistent. It must never leave orphaned policies, product details, claims or security records behind.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-022 | Create the claim table | business rule | WHEN a policy is deleted, THE Insurance Database SHALL delete all claims recorded against that policy. | medium | base/cntl/db2cre.jcl:350, base/cntl/db2cre.jcl:361-379 |
| ADPLM-BR-014 | Create the claim table | design note | WHEN no earlier step of the database set-up job has ended with a return code above 4, THE Insurance Database Provisioning SHALL create the endowment details table, keyed on the policy number, linked to its parent policy so that deleting the policy deletes its endowment details, with a unique index on the policy number. | medium | base/cntl/db2cre.jcl:189-192, base/cntl/db2cre.jcl:202-222 |
| ADPLM-BR-023 | Create the claim table | business rule | WHEN a policy is deleted, THE Insurance Database SHALL delete that policy's house details. | medium | base/cntl/db2cre.jcl:229, base/cntl/db2cre.jcl:240-256 |
| ADPLM-BR-024 | Create the claim table | business rule | WHEN a policy is deleted, THE Insurance Database SHALL delete that policy's motor details. | medium | base/cntl/db2cre.jcl:264, base/cntl/db2cre.jcl:275-294 |
| ADPLM-BR-025 | Create the claim table | business rule | WHEN a policy is deleted, THE Insurance Database SHALL delete that policy's commercial property details. | medium | base/cntl/db2cre.jcl:302, base/cntl/db2cre.jcl:313-342 |
| ADPLM-BR-026 | Create the claim table | business rule | WHEN a customer is deleted, THE Insurance Database SHALL delete all of that customer's policies, and with them their endowment, house, motor, commercial and claim records. | medium | base/cntl/db2cre.jcl:150, base/cntl/db2cre.jcl:161-185, base/cntl/db2cre.jcl:214-216, base/cntl/db2cre.jcl:250 |
| ADPLM-BR-027 | Create the claim table | business rule | WHEN a customer is deleted, THE Insurance Database SHALL delete that customer's security record. | medium | base/cntl/db2cre.jcl:99, base/cntl/db2cre.jcl:110-144 |

### Worked examples

- ADPLM-BR-022: policy number = 1000005; claims on policy = 2 → Deleting policy 1000005 also removes both claims
- ADPLM-BR-014: highest return code of earlier steps = 0 → The endowment table and its unique index on policy number are created; deleting policy 5 later also deletes its endowment row.
- ADPLM-BR-014: highest return code of earlier steps = 8 → The step is bypassed and the endowment table is not created.
- ADPLM-BR-023: policy number = 6; house details = 'HOUSE', 5 bedrooms → Deleting policy 6 removes its house details row
- ADPLM-BR-024: policy number = 1 → Deleting policy 1 removes its 'FORD' 'KA' motor row
- ADPLM-BR-025: policy number = 10 → Deleting policy 10 removes its commercial row
- ADPLM-BR-026: customer number = 5; policies = 3 (motor) and 9 (commercial) → Deleting customer 5 removes policies 3 and 9 and their motor and commercial details
- ADPLM-BR-027: customer number = 3 → Deleting customer 3 removes the customer_secure row for customer 3

## Decision tables

#### Records removed on deletion

| Record deleted | Dependent records deleted | Rule |
|---|---|---|
| Policy | All claims recorded against the policy are deleted | ADPLM-BR-022 |
| Policy | The policy's endowment details are deleted | ADPLM-BR-014 |
| Policy | The policy's house details are deleted | ADPLM-BR-023 |
| Policy | The policy's motor details are deleted | ADPLM-BR-024 |
| Policy | The policy's commercial property details are deleted | ADPLM-BR-025 |
| Customer | All the customer's policies and their endowment, house, motor, commercial and claim records are deleted | ADPLM-BR-026 |
| Customer | The customer's security record is deleted | ADPLM-BR-027 |


## Design notes

- ADPLM-BR-014: Enforce this in the database. A foreign key from endowment details to the policy cascades on delete, so removing a policy removes its endowment row in the same transaction, whichever code path deletes the policy.

## Open questions

- SME-009: The claim table has no standard name in the list of data entities. What should the new system call it? (Data architecture) On ADPLM-BR-022, ADPLM-BR-023, ADPLM-BR-025, ADPLM-BR-026, ADPLM-BR-024, ADPLM-BR-027, ADPLM-BR-014.
- SME-010: Customer, policy and claim numbers are generated automatically. What data type and length must these numbers have? (Data architecture) On ADPLM-BR-022, ADPLM-BR-023, ADPLM-BR-025, ADPLM-BR-026, ADPLM-BR-024, ADPLM-BR-027, ADPLM-BR-014.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (8 in all).