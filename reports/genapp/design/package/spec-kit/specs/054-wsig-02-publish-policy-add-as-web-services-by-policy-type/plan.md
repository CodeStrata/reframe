# Implementation plan: Publish policy add as web services by policy type (WSIG-C02)

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

- WSIG-BR-011: Provide an add-Motor-policy API operation at the stable path GENAPP/LGAPOLM1. Its contract comes from the Motor policy layout SOAIPM1 and it routes to the shared policy add logic. Publish its service description, binding and log named LGAPOLM1. The outbound proxy is build configuration.
- WSIG-BR-012: Provide an add-Endowment-policy API operation at the stable path GENAPP/LGAPOLE1. Its contract comes from the Endowment layout SOAIPE1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLE1.
- WSIG-BR-013: Provide an add-House-policy API operation at the stable path GENAPP/LGAPOLH1. Its contract comes from the House layout SOAIPH1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLH1. The Java and platform directory settings are build-environment configuration.
- WSIG-BR-014: Provide an add-Commercial-policy API operation at the stable path GENAPP/LGAPOLB1. Its contract comes from the Commercial layout SOAIPB1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLB1. Toolchain settings are build configuration.

## Decision tables

#### Policy add web service by policy type

| Policy type | Service URI, copybook and output files for program LGAPOL01 | Rule |
|---|---|---|
| Motor | URI GENAPP/LGAPOLM1, copybook SOAIPM1, LGAPOLM1.wsbind, LGAPOLM1.wsdl, log LS2WS_LGAPOLM1.LOG | WSIG-BR-011 |
| Endowment | URI GENAPP/LGAPOLE1, copybook SOAIPE1, LGAPOLE1.wsbind, LGAPOLE1.wsdl, log LS2WS_LGAPOLE1.LOG | WSIG-BR-012 |
| House | URI GENAPP/LGAPOLH1, copybook SOAIPH1, LGAPOLH1.wsbind, LGAPOLH1.wsdl, log LS2WS_LGAPOLH1.LOG | WSIG-BR-013 |
| Commercial | URI GENAPP/LGAPOLB1, copybook SOAIPB1, LGAPOLB1.wsbind, LGAPOLB1.wsdl, log LS2WS_LGAPOLB1.LOG | WSIG-BR-014 |

