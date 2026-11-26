# Tasks: Look up a single commercial policy (UP-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C07-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] UP-C07-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-041, UP-REQ-F-043. Rules: UP-BR-063, UP-BR-065. After: UP-C07-T1.
  - Keep each business rule exactly as specified.
- [ ] UP-C07-T3 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-042, UP-REQ-F-044, UP-REQ-F-039. Rules: UP-BR-061, UP-BR-064, UP-BR-066. After: UP-C07-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C07-T4 [api] Build the scheduled job. Requirements: UP-REQ-F-040. Rules: UP-BR-062. After: UP-C07-T1, UP-C07-T2, UP-C07-T3.
  - UP-BR-062: In a '01ICOM' or '02ICOM' reply, the marker 'FINAL' goes in the first 5 positions of the free space after the rejection reason, so callers can find where the data ends. Keep it in the reply layout while existing callers depend on it.
- [ ] UP-C07-T5 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044. Criteria: UP-C07-AC-01, UP-C07-AC-02, UP-C07-AC-03, UP-C07-AC-04, UP-C07-AC-05, UP-C07-AC-06, UP-C07-AC-07, UP-C07-AC-08. After: UP-C07-T1, UP-C07-T2, UP-C07-T3, UP-C07-T4.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] UP-C07-T6 [compliance] Review the handling of money, personal data. Requirements: UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044. After: UP-C07-T1, UP-C07-T2, UP-C07-T3, UP-C07-T4.
  - Check storage, logs, screens and audit against the rules.
