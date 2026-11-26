# Implementation plan: Store product details for a new policy (ADPLM-C08)

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

- LGCMAREA (working storage of LGAPDB01): see data-contracts.md.
- LGPOLICY (working storage of LGAPDB01): see data-contracts.md.

## Design notes

- ADPLM-BR-058: A plain field-to-column mapping for the commercial details: address, postcode, latitude, longitude, customer name, property type, the four perils and premiums, status and rejection reason, stored exactly as supplied. There is no rating engine or status derivation in this step.

## Decision tables

None.
