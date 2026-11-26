# Implementation plan: Return policy details (UP-C06)

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

- UP-BR-053: Before replying, the inquiry works out the space the reply needs: 33 bytes of header plus the length for the policy type. That is 124 for endowment plus any padding data, 130 for house, 137 for motor and 1174 for commercial. In a message-based API this becomes a check that the reply fits the caller's limit, with '98' when it does not.
- UP-BR-054: For an endowment policy, the space needed is 33 + 124 bytes plus the length of the policy's free-form padding data when present. The padding length must be read with the policy, so the size check and the reply use the same value.
- UP-BR-056: An endowment reply ends with the end-of-data marker 'FINAL', written straight after the padding data: at position 1 plus the padding length, or position 1 when there is none. Callers use it to find where the policy data ends. An API with explicit field lengths may not need it, but it must stay while existing callers read it.

## Decision tables

None.
