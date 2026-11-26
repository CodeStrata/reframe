# Implementation plan: Route policy inquiries by request type (UP-C04)

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

- LGCMAREA (working storage of LGIPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGIPDB01): see data-contracts.md.

## Design notes

- UP-BR-034: Every policy inquiry reply starts with return code '00'. Only a later failure (not found, reply area too small, database error or unknown request) changes it, so a request that runs cleanly always returns '00'.
- UP-BR-035: At the start of each policy inquiry, the supplied customer number and policy number become the lookup keys. They are also kept as context for error messages, so any error logged later names the customer and policy the caller asked for.

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

