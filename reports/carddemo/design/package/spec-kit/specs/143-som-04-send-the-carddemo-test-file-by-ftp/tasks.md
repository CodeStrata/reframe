# Tasks: Send the CardDemo test file by FTP (SOM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] SOM-C04-T1 [business-rules] Implement the business rules. Requirements: SOM-REQ-F-026, SOM-REQ-F-027. Rules: SOM-BR-030, SOM-BR-031.
  - Keep each business rule exactly as specified.
- [ ] SOM-C04-T2 [api] Build the scheduled job. Requirements: SOM-REQ-F-026, SOM-REQ-F-027. Rules: SOM-BR-030, SOM-BR-031. After: SOM-C04-T1.
  - Expose the rules as the service the screens call.
- [ ] SOM-C04-T3 [test-generation] Write a test for every acceptance criterion. Requirements: SOM-REQ-F-026, SOM-REQ-F-027. Criteria: SOM-C04-AC-01, SOM-C04-AC-02. After: SOM-C04-T1, SOM-C04-T2.
  - 2 acceptance criteria, each a test named by its ID.
- [ ] SOM-C04-T4 [compliance] Review the handling of security. Requirements: SOM-REQ-F-026, SOM-REQ-F-027. After: SOM-C04-T1, SOM-C04-T2.
  - Check storage, logs, screens and audit against the rules.
