# Tasks: Register online CardDemo programs and transactions (SOM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] SOM-C01-T1 [api] Build the scheduled job. Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003. Rules: SOM-BR-001, SOM-BR-002, SOM-BR-003.
  - SOM-BR-001: Register the sign-on screen as a routable entry point (for example a route or deep-link code that matches legacy code CC00) in the application's deployment or route configuration, which is applied when the environment is provisioned. It must be open to any user who has not signed on. No data-location setting is needed.
  - SOM-BR-002: Register the Admin Menu as a routable entry point under the code CCAD in the same deployment or route configuration as the sign-on screen, so the configuration is versioned and applied with each release.
  - SOM-BR-003: Map a second entry code, CCDM, to the same Admin Menu route, so both CCAD and CCDM open the Admin Menu. Keep it as an alias in the route configuration, not a separate screen.
- [ ] SOM-C01-T2 [test-generation] Write a test for every acceptance criterion. Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003. Criteria: SOM-C01-AC-01, SOM-C01-AC-02, SOM-C01-AC-03. After: SOM-C01-T1.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] SOM-C01-T3 [compliance] Review the handling of security. Requirements: SOM-REQ-F-001, SOM-REQ-F-002, SOM-REQ-F-003. After: SOM-C01-T1.
  - Check storage, logs, screens and audit against the rules.
