# Implementation plan: Publish customer operations as web services (WSIG-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. WSIG-C01-T1 [api] Build the scheduled job
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
  - _Requirements: WSIG-REQ-F-001, WSIG-REQ-F-002, WSIG-REQ-F-003, WSIG-REQ-F-004, WSIG-REQ-F-005, WSIG-REQ-F-006, WSIG-REQ-F-007, WSIG-REQ-F-008, WSIG-REQ-N-001, WSIG-REQ-N-002_
  - _Rules: WSIG-BR-001, WSIG-BR-002, WSIG-BR-003, WSIG-BR-004, WSIG-BR-005, WSIG-BR-006, WSIG-BR-007, WSIG-BR-008, WSIG-BR-009, WSIG-BR-010_
- [ ] 2. WSIG-C01-T2 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: WSIG-REQ-F-001, WSIG-REQ-F-002, WSIG-REQ-F-003, WSIG-REQ-F-004, WSIG-REQ-F-005, WSIG-REQ-F-006, WSIG-REQ-F-007, WSIG-REQ-F-008, WSIG-REQ-N-001, WSIG-REQ-N-002_
  - _Criteria: WSIG-C01-AC-01, WSIG-C01-AC-02, WSIG-C01-AC-03, WSIG-C01-AC-04, WSIG-C01-AC-05, WSIG-C01-AC-06, WSIG-C01-AC-07, WSIG-C01-AC-08, WSIG-C01-AC-09, WSIG-C01-AC-10, WSIG-C01-AC-11, WSIG-C01-AC-12_
  - _After: WSIG-C01-T1_
- [ ] 3. WSIG-C01-T3 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: WSIG-REQ-F-001, WSIG-REQ-F-002, WSIG-REQ-F-003, WSIG-REQ-F-004, WSIG-REQ-F-005, WSIG-REQ-F-006, WSIG-REQ-F-007, WSIG-REQ-F-008, WSIG-REQ-N-001, WSIG-REQ-N-002_
  - _After: WSIG-C01-T1_
