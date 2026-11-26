# Tasks: Publish policy add as web services by policy type (WSIG-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] WSIG-C02-T1 [api] Build the scheduled job. Requirements: WSIG-REQ-F-009, WSIG-REQ-F-010, WSIG-REQ-F-011, WSIG-REQ-F-012, WSIG-REQ-N-003. Rules: WSIG-BR-011, WSIG-BR-012, WSIG-BR-013, WSIG-BR-014.
  - WSIG-BR-011: Provide an add-Motor-policy API operation at the stable path GENAPP/LGAPOLM1. Its contract comes from the Motor policy layout SOAIPM1 and it routes to the shared policy add logic. Publish its service description, binding and log named LGAPOLM1. The outbound proxy is build configuration.
  - WSIG-BR-012: Provide an add-Endowment-policy API operation at the stable path GENAPP/LGAPOLE1. Its contract comes from the Endowment layout SOAIPE1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLE1.
  - WSIG-BR-013: Provide an add-House-policy API operation at the stable path GENAPP/LGAPOLH1. Its contract comes from the House layout SOAIPH1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLH1. The Java and platform directory settings are build-environment configuration.
  - WSIG-BR-014: Provide an add-Commercial-policy API operation at the stable path GENAPP/LGAPOLB1. Its contract comes from the Commercial layout SOAIPB1 and it routes to the shared policy add logic. Publish its artifacts named LGAPOLB1. Toolchain settings are build configuration.
- [ ] WSIG-C02-T2 [test-generation] Write a test for every acceptance criterion. Requirements: WSIG-REQ-F-009, WSIG-REQ-F-010, WSIG-REQ-F-011, WSIG-REQ-F-012, WSIG-REQ-N-003. Criteria: WSIG-C02-AC-01, WSIG-C02-AC-02, WSIG-C02-AC-03, WSIG-C02-AC-04. After: WSIG-C02-T1.
  - 4 acceptance criteria, each a test named by its ID.
