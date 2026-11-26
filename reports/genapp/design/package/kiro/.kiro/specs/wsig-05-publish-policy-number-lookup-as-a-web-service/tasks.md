# Implementation plan: Publish policy number lookup as a web service (WSIG-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. WSIG-C05-T1 [api] Build the scheduled job
  - WSIG-BR-029: Provide a read-only policy number lookup API operation at the stable path GENAPP/LGIPVS01. It has its own request contract from SOAVPII and its own response contract from SOAVPIO. Both are generated from those layouts, and the outbound proxy is build configuration.
  - WSIG-BR-030: Publish the policy number service description, binding and generation log as build artifacts named LGIPVS01. The runtime directories and temp-file settings go in build-environment configuration.
  - _Requirements: WSIG-REQ-F-026, WSIG-REQ-F-027, WSIG-REQ-N-006_
  - _Rules: WSIG-BR-029, WSIG-BR-030_
- [ ] 2. WSIG-C05-T2 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: WSIG-REQ-F-026, WSIG-REQ-F-027, WSIG-REQ-N-006_
  - _Criteria: WSIG-C05-AC-01, WSIG-C05-AC-02, WSIG-C05-AC-03_
  - _After: WSIG-C05-T1_
