# Implementation plan: Look up a customer's policy by type (ADPLM-C17)

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

- ADPLM-BR-112: The interactive entry point takes the policy type and the customer number as separate input fields, instead of splitting a typed line at fixed offsets after a 5-character transaction code and space.
- ADPLM-BR-113: The service entry point takes a request with a one-character policy type and a 10-digit customer number as named fields.
- ADPLM-BR-119: Return a fresh response for service callers that holds the result label ('Policy Key=' or 'Policy Bad=') and the 21-character key. Nothing from the caller's request is echoed back.

## Decision tables

#### Policy lookup answer

| Policy file read result | Retrieved policy type matches requested type | Answer returned | Rule |
|---|---|---|---|
| Succeeds | Yes | 'Policy Key=' followed by the retrieved 21-character key | ADPLM-BR-116 |
| Succeeds | No | 'Policy Bad=' followed by type 'X', customer number 0000000013 and policy number 0000000013 | ADPLM-BR-118 |
| Fails | - | 'Policy Bad=' followed by type 'X', customer number 0000000013 and policy number 0000000013 | ADPLM-BR-117 |

