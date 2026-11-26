# Tasks: Business-monitor symbol list (not delivered) (TSM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TSM-C04-T1 [business-rules] Implement the business rules. Requirements: TSM-REQ-F-016, TSM-REQ-F-017, TSM-REQ-F-018. Rules: TSM-BR-013, TSM-BR-015.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: TSM-BR-013, TSM-BR-015.
- [ ] TSM-C04-T2 [api] Build the scheduled job. Requirements: TSM-REQ-F-016, TSM-REQ-F-017, TSM-REQ-F-018. Rules: TSM-BR-013, TSM-BR-015. After: TSM-C04-T1.
  - Expose the rules as the service the screens call.
- [ ] TSM-C04-T3 [test-generation] Write a test for every acceptance criterion. Requirements: TSM-REQ-F-016, TSM-REQ-F-017, TSM-REQ-F-018. Criteria: TSM-C04-AC-01, TSM-C04-AC-02, TSM-C04-AC-03. After: TSM-C04-T1, TSM-C04-T2.
  - 3 acceptance criteria, each a test named by its ID.
