# Implementation plan: Create the new customer's security record (CRCM-C04)

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

- LGCMAREA (working storage of LGACDB01): see data-contracts.md.
- LGPOLICY (working storage of LGACDB01, LGACDB02): see data-contracts.md.

## Design notes

None.

## Decision tables

#### Customer security record add

| Security request type | Security record insert | Result | Rule |
|---|---|---|---|
| '02ACUS' | Succeeds | Security record added to CUSTOMER_SECURE | CRCM-BR-023 |
| '02ACUS' | Fails | Return code '98'; error ' INSERT SECURITY' logged | CRCM-BR-025 |
| Other than '02ACUS' | - | Return code '99'; no record added | CRCM-BR-024 |

