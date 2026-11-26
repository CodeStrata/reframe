# Implementation plan: Publish policy update as web services by policy type (WSIG-C04)

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

- WSIG-BR-021: Provide an update-Motor-policy API operation at the stable path GENAPP/LGUPOLM1. Its request and response contract comes from the Motor layout SOAIPM1 and it routes to the shared policy update logic. The outbound proxy is build configuration.
- WSIG-BR-022: Publish the Motor update service description, binding and generation log as build artifacts named LGUPOLM1. The toolchain directories and temp settings go in build configuration.
- WSIG-BR-023: Provide an update-Commercial-policy API operation at the stable path GENAPP/LGUPOLB1. Its request and response contract comes from the Commercial layout SOAIPB1 and it routes to the shared policy update logic.
- WSIG-BR-024: Publish the Commercial update service description, binding and generation log as build artifacts named LGUPOLB1. Toolchain settings are build configuration.
- WSIG-BR-025: Provide an update-Endowment-policy API operation at the stable path GENAPP/LGUPOLE1. Its request and response contract comes from the Endowment layout SOAIPE1 and it routes to the shared policy update logic.
- WSIG-BR-026: Publish the Endowment update service description, binding and generation log as build artifacts named LGUPOLE1. Toolchain settings are build configuration.
- WSIG-BR-027: Provide an update-House-policy API operation at the stable path GENAPP/LGUPOLH1. Its request and response contract comes from the House layout SOAIPH1 and it routes to the shared policy update logic.
- WSIG-BR-028: Publish the House update service description, binding and generation log as build artifacts named LGUPOLH1. Toolchain settings are build configuration.

## Decision tables

#### Policy update web service by policy type

| Policy type | Layout and service URI for program LGUPOL01 | Rule |
|---|---|---|
| Motor | Layout SOAIPM1, URI GENAPP/LGUPOLM1 | WSIG-BR-021 |
| Commercial | Layout SOAIPB1, URI GENAPP/LGUPOLB1 | WSIG-BR-023 |
| Endowment | Layout SOAIPE1, URI GENAPP/LGUPOLE1 | WSIG-BR-025 |
| House | Layout SOAIPH1, URI GENAPP/LGUPOLH1 | WSIG-BR-027 |

