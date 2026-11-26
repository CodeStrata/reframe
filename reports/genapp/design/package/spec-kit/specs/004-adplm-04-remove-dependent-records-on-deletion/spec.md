# Feature specification: Remove dependent records on deletion

**Feature:** ADPLM-C04 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C04)

As an insurance operations manager, I want deleting a customer or policy to remove everything recorded against it, so that no orphaned policy, product, claim or security records remain.

When a customer or a policy is deleted, everything recorded against it is deleted too: policies, their endowment, house, motor and commercial details, their claims, and the customer's security record. It is for insurance operations, who need the records to stay consistent. It must never leave orphaned policies, product details, claims or security records behind.

**Acceptance scenarios:**

1. **Given** policy number: 1000005; claims on policy: 2, **when** a policy is deleted, **then** Deleting policy 1000005 also removes both claims (ADPLM-C04-AC-01)
2. **Given** highest return code of earlier steps: 0, **when** no earlier step of the database set-up job has ended with a return code above 4, **then** The endowment table and its unique index on policy number are created; deleting policy 5 later also deletes its endowment row. (ADPLM-C04-AC-02)
3. **Given** highest return code of earlier steps: 8, **when** no earlier step of the database set-up job has ended with a return code above 4, **then** The step is bypassed and the endowment table is not created. (ADPLM-C04-AC-03)
4. **Given** policy number: 6; house details: 'HOUSE', 5 bedrooms, **when** a policy is deleted, **then** Deleting policy 6 removes its house details row (ADPLM-C04-AC-04)
5. **Given** policy number: 1, **when** a policy is deleted, **then** Deleting policy 1 removes its 'FORD' 'KA' motor row (ADPLM-C04-AC-05)
6. **Given** policy number: 10, **when** a policy is deleted, **then** Deleting policy 10 removes its commercial row (ADPLM-C04-AC-06)
7. **Given** customer number: 5; policies: 3 (motor) and 9 (commercial), **when** a customer is deleted, **then** Deleting customer 5 removes policies 3 and 9 and their motor and commercial details (ADPLM-C04-AC-07)
8. **Given** customer number: 3, **when** a customer is deleted, **then** Deleting customer 3 removes the customer_secure row for customer 3 (ADPLM-C04-AC-08)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-022** (business rule): When a policy is deleted, the system shall delete all claims recorded against that policy. Rules: ADPLM-BR-022.
- **ADPLM-REQ-F-023** (business rule): When a policy is deleted, the system shall delete that policy's endowment, house, motor and commercial property details. Rules: ADPLM-BR-014, ADPLM-BR-023, ADPLM-BR-024, ADPLM-BR-025.
- **ADPLM-REQ-F-024** (business rule): When a customer is deleted, the system shall delete all of that customer's policies, and with them their endowment, house, motor, commercial and claim records. Rules: ADPLM-BR-026.
- **ADPLM-REQ-F-025** (business rule): When a customer is deleted, the system shall delete that customer's security record. Rules: ADPLM-BR-027.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-022 | Create the claim table | business rule | WHEN a policy is deleted, THE Insurance Database SHALL delete all claims recorded against that policy. | medium | base/cntl/db2cre.jcl:350, base/cntl/db2cre.jcl:361-379 |
| ADPLM-BR-014 | Create the claim table | design note | WHEN no earlier step of the database set-up job has ended with a return code above 4, THE Insurance Database Provisioning SHALL create the endowment details table, keyed on the policy number, linked to its parent policy so that deleting the policy deletes its endowment details, with a unique index on the policy number. | medium | base/cntl/db2cre.jcl:189-192, base/cntl/db2cre.jcl:202-222 |
| ADPLM-BR-023 | Create the claim table | business rule | WHEN a policy is deleted, THE Insurance Database SHALL delete that policy's house details. | medium | base/cntl/db2cre.jcl:229, base/cntl/db2cre.jcl:240-256 |
| ADPLM-BR-024 | Create the claim table | business rule | WHEN a policy is deleted, THE Insurance Database SHALL delete that policy's motor details. | medium | base/cntl/db2cre.jcl:264, base/cntl/db2cre.jcl:275-294 |
| ADPLM-BR-025 | Create the claim table | business rule | WHEN a policy is deleted, THE Insurance Database SHALL delete that policy's commercial property details. | medium | base/cntl/db2cre.jcl:302, base/cntl/db2cre.jcl:313-342 |
| ADPLM-BR-026 | Create the claim table | business rule | WHEN a customer is deleted, THE Insurance Database SHALL delete all of that customer's policies, and with them their endowment, house, motor, commercial and claim records. | medium | base/cntl/db2cre.jcl:150, base/cntl/db2cre.jcl:161-185, base/cntl/db2cre.jcl:214-216, base/cntl/db2cre.jcl:250 |
| ADPLM-BR-027 | Create the claim table | business rule | WHEN a customer is deleted, THE Insurance Database SHALL delete that customer's security record. | medium | base/cntl/db2cre.jcl:99, base/cntl/db2cre.jcl:110-144 |

### Key entities

None found in the source.

### Needs clarification

- SME-009: The claim table has no standard name in the list of data entities. What should the new system call it? (Data architecture) On ADPLM-BR-022, ADPLM-BR-023, ADPLM-BR-025, ADPLM-BR-026, ADPLM-BR-024, ADPLM-BR-027, ADPLM-BR-014.
- SME-010: Customer, policy and claim numbers are generated automatically. What data type and length must these numbers have? (Data architecture) On ADPLM-BR-022, ADPLM-BR-023, ADPLM-BR-025, ADPLM-BR-026, ADPLM-BR-024, ADPLM-BR-027, ADPLM-BR-014.

### Decision table gaps

None.
