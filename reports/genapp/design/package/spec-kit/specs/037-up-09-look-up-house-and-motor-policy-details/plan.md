# Implementation plan: Look up house and motor policy details (UP-C09)

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

- UP-BR-075: A house reply ends with 'FINAL' in the first 5 positions of the free space straight after the house details. Callers use it to find where the policy data ends.
- UP-BR-076: A motor reply ends with 'FINAL' in the first 5 positions of the free space straight after the motor details, after the accidents count. Callers use it to find where the policy data ends.

## Decision tables

None.
