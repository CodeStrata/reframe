# Implementation plan: Count transactions by request type and outcome (ADPLM-C13)

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

- LGCMAREA (working storage of LGASTAT1): see data-contracts.md.

## Design notes

- ADPLM-BR-076: The counter needs a transaction-completed event that carries the request type and the return code as separate fields. Publish it from every request handler when the handler finishes, and have the statistics consumer read these fields first.
- ADPLM-BR-077: Fallback input: if the event fields are missing, the consumer takes the request type and return code from the request payload that came with the event. Handle both shapes through one input contract instead of two code paths.

## Decision tables

#### Statistics event source selection

| Event containers readable | Request data passed | Source of request type and return code | Rule |
|---|---|---|---|
| Yes | - | Request type from DFHEP.DATA.00001, return code from DFHEP.DATA.00002 | ADPLM-BR-076 |
| No | Yes | Request type and return code from the request | ADPLM-BR-077 |
| No | No | End without counting anything | ADPLM-BR-078 |

