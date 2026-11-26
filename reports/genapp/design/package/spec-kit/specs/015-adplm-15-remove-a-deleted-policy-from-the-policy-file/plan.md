# Implementation plan: Remove a deleted policy from the policy file (ADPLM-C15)

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

- LGCMAREA (working storage of LGDPVS01): see data-contracts.md.

## Design notes

- ADPLM-BR-096: The policy file is a keyed store. Its 21-character key is the policy type letter (the fourth character of the request identifier), then the 10-digit customer number, then the 10-digit policy number. Deletion is a single delete by that exact key.

## Decision tables

None.
