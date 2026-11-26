# Tasks: Authorize online transaction under the card security profile (SOM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] SOM-C06-T1 [business-rules] Implement the business rules. Requirements: SOM-REQ-F-031. Rules: SOM-BR-035.
  - Keep each business rule exactly as specified.
- [ ] SOM-C06-T2 [api] Build the scheduled job. Requirements: SOM-REQ-F-031. Rules: SOM-BR-035. After: SOM-C06-T1.
  - Expose the rules as the service the screens call.
- [ ] SOM-C06-T3 [test-generation] Write a test for every acceptance criterion. Requirements: SOM-REQ-F-031. Criteria: SOM-C06-AC-01. After: SOM-C06-T1, SOM-C06-T2.
  - 1 acceptance criteria, each a test named by its ID.
- [ ] SOM-C06-T4 [compliance] Review the handling of audit, security. Requirements: SOM-REQ-F-031. After: SOM-C06-T1, SOM-C06-T2.
  - Check storage, logs, screens and audit against the rules.
