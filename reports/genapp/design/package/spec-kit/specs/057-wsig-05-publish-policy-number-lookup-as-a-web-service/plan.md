# Implementation plan: Publish policy number lookup as a web service (WSIG-C05)

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

- WSIG-BR-029: Provide a read-only policy number lookup API operation at the stable path GENAPP/LGIPVS01. It has its own request contract from SOAVPII and its own response contract from SOAVPIO. Both are generated from those layouts, and the outbound proxy is build configuration.
- WSIG-BR-030: Publish the policy number service description, binding and generation log as build artifacts named LGIPVS01. The runtime directories and temp-file settings go in build-environment configuration.

## Decision tables

None.
