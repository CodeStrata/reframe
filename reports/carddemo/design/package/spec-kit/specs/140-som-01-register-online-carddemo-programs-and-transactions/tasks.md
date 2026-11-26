# Tasks: Register online CardDemo programs and transactions (SOM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] SOM-C01-T1 [api] Build the scheduled job. Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003. Rules: SOM-BR-001, SOM-BR-002, SOM-BR-003.
  - SOM-BR-001: The sign-on entry point must be set up as part of deployment configuration, such as a route table or service registration. Its legacy code CC00 maps to the sign-on screen, and it must be usable from any node or region (the legacy data location ANY). Keep CC00 as an alias only if outside links or operators still use it.
  - SOM-BR-002: Register the admin menu as a deployable entry point (a route or service) that answers to the legacy code CCAD. It must be declared in the same deployment configuration as sign-on (the CARDDEMO group), so the two are always released together.
  - SOM-BR-003: A second legacy code, CCDM, must open the same admin menu. Model it as an alias route or redirect to the admin menu entry point, not as a separate screen. No location restriction is needed (ANY).
- [ ] SOM-C01-T2 [test-generation] Write a test for every acceptance criterion. Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003. Criteria: SOM-C01-AC-01, SOM-C01-AC-02, SOM-C01-AC-03. After: SOM-C01-T1.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] SOM-C01-T3 [compliance] Review the handling of security. Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003. After: SOM-C01-T1.
  - Check storage, logs, screens and audit against the rules.
