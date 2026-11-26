# Implementation plan: Remove dependent records on deletion (ADPLM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

None found in the source.

## Design notes

- ADPLM-BR-014: Enforce this in the database. A foreign key from endowment details to the policy cascades on delete, so removing a policy removes its endowment row in the same transaction, whichever code path deletes the policy.

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

