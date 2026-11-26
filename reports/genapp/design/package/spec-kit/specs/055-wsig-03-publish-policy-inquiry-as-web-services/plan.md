# Implementation plan: Publish policy inquiry as web services (WSIG-C03)

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

- WSIG-BR-015: Provide a read-only mobile policy lookup API operation at the stable path GENAPP/LGIPOL02 that can return several policies in one response. Its request contract comes from POLLOOK and its response contract from POLLOO2. Publish its service description, binding and log named LGIPOL02.
- WSIG-BR-016: Provide a read-only Motor policy inquiry API operation at the stable path GENAPP/LGIPOLM1. Its request and response contract comes from the Motor layout SOAIPM1 and it routes to the shared policy inquiry logic. Publish its artifacts named LGIPOLM1.
- WSIG-BR-017: Provide a read-only Commercial policy inquiry API operation at the stable path GENAPP/LGIPOLB1. Its request and response contract comes from the Commercial layout SOAIPB1. Publish its artifacts named LGIPOLB1.
- WSIG-BR-018: Provide a read-only House policy inquiry API operation at the stable path GENAPP/LGIPOLH1. Its request and response contract comes from the House layout SOAIPH1. Publish its artifacts named LGIPOLH1.
- WSIG-BR-019: Provide a read-only Endowment policy inquiry API operation at the stable path GENAPP/LGIPOLE1. Its request and response contract comes from the Endowment layout SOAIPE1. Publish its artifacts named LGIPOLE1.
- WSIG-BR-020: Generate all five policy inquiry contracts in one repeatable build step. The runtime, platform directory, temp location and file-prefix settings it needs are shared build-environment configuration, not per-service code.

## Decision tables

#### Policy inquiry web service by step

| Inquiry step | Program, structures, service URI and output files | Rule |
|---|---|---|
| Mobile multiple-return | Program IPPROGMB, request POLLOOK, response POLLOO2, URI GENAPP/LGIPOL02, LGIPOL02.wsbind/.wsdl, log LS2WS_LGIPOL02.LOG | WSIG-BR-015 |
| Motor Policy | Program LGIPOL01, structure SOAIPM1, URI GENAPP/LGIPOLM1, LGIPOLM1.wsbind/.wsdl, log LS2WS_LGIPOLM1.LOG | WSIG-BR-016 |
| Commercial Policy | Program LGIPOL01, structure SOAIPB1, URI GENAPP/LGIPOLB1, LGIPOLB1.wsbind/.wsdl, log LS2WS_LGIPOLB1.LOG | WSIG-BR-017 |
| House Policy | Program LGIPOL01, structure SOAIPH1, URI GENAPP/LGIPOLH1, LGIPOLH1.wsbind/.wsdl, log LS2WS_LGIPOLH1.LOG | WSIG-BR-018 |
| Endowment Policy | Program LGIPOL01, structure SOAIPE1, URI GENAPP/LGIPOLE1, LGIPOLE1.wsbind/.wsdl, log LS2WS_LGIPOLE1.LOG | WSIG-BR-019 |

