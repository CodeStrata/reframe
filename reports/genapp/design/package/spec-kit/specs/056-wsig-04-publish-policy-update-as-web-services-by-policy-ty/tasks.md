# Tasks: Publish policy update as web services by policy type (WSIG-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] WSIG-C04-T1 [api] Build the scheduled job. Requirements: WSIG-REQ-F-018, WSIG-REQ-F-019, WSIG-REQ-F-020, WSIG-REQ-F-021, WSIG-REQ-F-022, WSIG-REQ-F-023, WSIG-REQ-F-024, WSIG-REQ-F-025, WSIG-REQ-N-005. Rules: WSIG-BR-021, WSIG-BR-022, WSIG-BR-023, WSIG-BR-024, WSIG-BR-025, WSIG-BR-026, WSIG-BR-027, WSIG-BR-028.
  - WSIG-BR-021: Provide an update-Motor-policy API operation at the stable path GENAPP/LGUPOLM1. Its request and response contract comes from the Motor layout SOAIPM1 and it routes to the shared policy update logic. The outbound proxy is build configuration.
  - WSIG-BR-022: Publish the Motor update service description, binding and generation log as build artifacts named LGUPOLM1. The toolchain directories and temp settings go in build configuration.
  - WSIG-BR-023: Provide an update-Commercial-policy API operation at the stable path GENAPP/LGUPOLB1. Its request and response contract comes from the Commercial layout SOAIPB1 and it routes to the shared policy update logic.
  - WSIG-BR-024: Publish the Commercial update service description, binding and generation log as build artifacts named LGUPOLB1. Toolchain settings are build configuration.
  - WSIG-BR-025: Provide an update-Endowment-policy API operation at the stable path GENAPP/LGUPOLE1. Its request and response contract comes from the Endowment layout SOAIPE1 and it routes to the shared policy update logic.
  - WSIG-BR-026: Publish the Endowment update service description, binding and generation log as build artifacts named LGUPOLE1. Toolchain settings are build configuration.
  - WSIG-BR-027: Provide an update-House-policy API operation at the stable path GENAPP/LGUPOLH1. Its request and response contract comes from the House layout SOAIPH1 and it routes to the shared policy update logic.
  - WSIG-BR-028: Publish the House update service description, binding and generation log as build artifacts named LGUPOLH1. Toolchain settings are build configuration.
- [ ] WSIG-C04-T2 [test-generation] Write a test for every acceptance criterion. Requirements: WSIG-REQ-F-018, WSIG-REQ-F-019, WSIG-REQ-F-020, WSIG-REQ-F-021, WSIG-REQ-F-022, WSIG-REQ-F-023, WSIG-REQ-F-024, WSIG-REQ-F-025, WSIG-REQ-N-005. Criteria: WSIG-C04-AC-01, WSIG-C04-AC-02, WSIG-C04-AC-03, WSIG-C04-AC-04, WSIG-C04-AC-05, WSIG-C04-AC-06, WSIG-C04-AC-07, WSIG-C04-AC-08. After: WSIG-C04-T1.
  - 8 acceptance criteria, each a test named by its ID.
