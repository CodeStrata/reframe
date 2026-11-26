# Tasks: List customer records (UP-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C04-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-013, UP-REQ-F-014.
  - File records: CVACT03Y, CVCUS01Y (see data-contracts.md).
- [ ] UP-C04-T2 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-013, UP-REQ-F-014. Rules: UP-BR-005, UP-BR-015, UP-BR-016. After: UP-C04-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C04-T3 [api] Build the scheduled job. Requirements: UP-REQ-F-013, UP-REQ-F-014. Rules: UP-BR-005, UP-BR-015, UP-BR-016. After: UP-C04-T1, UP-C04-T2.
  - Expose the rules as the service the screens call.
- [ ] UP-C04-T4 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-013, UP-REQ-F-014. Criteria: UP-C04-AC-01, UP-C04-AC-02, UP-C04-AC-03, UP-C04-AC-04, UP-C04-AC-05. After: UP-C04-T1, UP-C04-T2, UP-C04-T3.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] UP-C04-T5 [compliance] Review the handling of personal data. Requirements: UP-REQ-F-013, UP-REQ-F-014. After: UP-C04-T1, UP-C04-T2, UP-C04-T3.
  - Check storage, logs, screens and audit against the rules.
