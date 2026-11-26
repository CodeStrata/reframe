# Tasks: Publish policy inquiry as web services (WSIG-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] WSIG-C03-T1 [api] Build the scheduled job. Requirements: WSIG-REQ-F-013, WSIG-REQ-F-014, WSIG-REQ-F-015, WSIG-REQ-F-016, WSIG-REQ-F-017, WSIG-REQ-N-004. Rules: WSIG-BR-015, WSIG-BR-016, WSIG-BR-017, WSIG-BR-018, WSIG-BR-019, WSIG-BR-020.
  - WSIG-BR-015: Provide a read-only mobile policy lookup API operation at the stable path GENAPP/LGIPOL02 that can return several policies in one response. Its request contract comes from POLLOOK and its response contract from POLLOO2. Publish its service description, binding and log named LGIPOL02.
  - WSIG-BR-016: Provide a read-only Motor policy inquiry API operation at the stable path GENAPP/LGIPOLM1. Its request and response contract comes from the Motor layout SOAIPM1 and it routes to the shared policy inquiry logic. Publish its artifacts named LGIPOLM1.
  - WSIG-BR-017: Provide a read-only Commercial policy inquiry API operation at the stable path GENAPP/LGIPOLB1. Its request and response contract comes from the Commercial layout SOAIPB1. Publish its artifacts named LGIPOLB1.
  - WSIG-BR-018: Provide a read-only House policy inquiry API operation at the stable path GENAPP/LGIPOLH1. Its request and response contract comes from the House layout SOAIPH1. Publish its artifacts named LGIPOLH1.
  - WSIG-BR-019: Provide a read-only Endowment policy inquiry API operation at the stable path GENAPP/LGIPOLE1. Its request and response contract comes from the Endowment layout SOAIPE1. Publish its artifacts named LGIPOLE1.
  - WSIG-BR-020: Generate all five policy inquiry contracts in one repeatable build step. The runtime, platform directory, temp location and file-prefix settings it needs are shared build-environment configuration, not per-service code.
- [ ] WSIG-C03-T2 [test-generation] Write a test for every acceptance criterion. Requirements: WSIG-REQ-F-013, WSIG-REQ-F-014, WSIG-REQ-F-015, WSIG-REQ-F-016, WSIG-REQ-F-017, WSIG-REQ-N-004. Criteria: WSIG-C03-AC-01, WSIG-C03-AC-02, WSIG-C03-AC-03, WSIG-C03-AC-04, WSIG-C03-AC-05, WSIG-C03-AC-06. After: WSIG-C03-T1.
  - 6 acceptance criteria, each a test named by its ID.
