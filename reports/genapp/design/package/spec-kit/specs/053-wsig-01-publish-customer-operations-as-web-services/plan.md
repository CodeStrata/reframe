# Implementation plan: Publish customer operations as web services (WSIG-C01)

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

- WSIG-BR-001: Expose add customer as an API operation at the stable path GENAPP/LGACUS01. Its request and response contract comes from the one shared customer layout (SOAIC01), the same layout that inquiry and update use. Generate the contract from that layout so the two cannot drift apart.
- WSIG-BR-002: Publish the add-customer service description, any runtime binding, and a generation log as build artifacts named after the service (LGACUS01). Put them where the deployment step and callers can find them under the installation home. Generation failures must show up in that log.
- WSIG-BR-003: Expose customer inquiry as a read-only API operation at the stable path GENAPP/LGICUS01. It uses the shared customer layout SOAIC01 for both request and response.
- WSIG-BR-004: Publish the customer inquiry service description, binding and generation log as build artifacts named LGICUS01, in the same published-services and logs locations as the other customer services.
- WSIG-BR-005: Expose customer update as an API operation at the stable path GENAPP/LGUCUS01, with the shared customer layout SOAIC01 for both request and response. The legacy generator reached the network through PROXY.HURSLEY.IBM.COM:80. Make the build's outbound proxy a configuration setting, not a fixed value.
- WSIG-BR-006: Publish the customer update service description, binding and log as build artifacts named LGUCUS01. The legacy toolchain settings (Java 'java601_bit64_ga/J6.0.1_64', 'cics660', '/tmp', 'LS2WS') belong in build-environment configuration. They are not product behaviour.
- WSIG-BR-007: Expose customer number lookup as an API operation at the stable path GENAPP/LGICVS01. Unlike the other customer services, it has its own request layout (SOAVCII) and its own response layout (SOAVCIO), and the contract must keep those two shapes separate.
- WSIG-BR-008: Publish the customer number service description, binding and log as build artifacts named LGICVS01. The toolchain directories and temp-file settings go in build configuration.
- WSIG-BR-009: Contract generation for add customer runs as a repeatable build or pipeline step from the source layouts. The Java runtime, platform directory, temp location and HTTP proxy it needs become build-environment settings.
- WSIG-BR-010: Contract generation for customer inquiry runs in the same repeatable build step as add customer, with the same configurable runtime, temp location and proxy settings.

## Decision tables

#### Customer web service by operation

| Customer operation | Program, service address and request/response layout | Rule |
|---|---|---|
| Add customer | Program LGACUS01 at GENAPP/LGACUS01 using SOAIC01 for request and response | WSIG-BR-001 |
| Customer inquiry | Program LGICUS01 at GENAPP/LGICUS01 using SOAIC01 for request and response | WSIG-BR-003 |
| Customer update | Program LGUCUS01 at GENAPP/LGUCUS01 using SOAIC01 for request and response | WSIG-BR-005 |
| Customer number | Program LGICVS01 at GENAPP/LGICVS01 using request SOAVCII and response SOAVCIO | WSIG-BR-007 |

