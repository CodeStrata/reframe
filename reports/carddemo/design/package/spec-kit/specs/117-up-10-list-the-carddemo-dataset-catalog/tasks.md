# Tasks: List the CardDemo dataset catalog (UP-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C10-T1 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-047. Rules: UP-BR-050.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C10-T2 [api] Build the scheduled job. Requirements: UP-REQ-F-047. Rules: UP-BR-050. After: UP-C10-T1.
  - Expose the rules as the service the screens call.
- [ ] UP-C10-T3 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-047. Criteria: UP-C10-AC-01, UP-C10-AC-02. After: UP-C10-T1, UP-C10-T2.
  - 2 acceptance criteria, each a test named by its ID.
