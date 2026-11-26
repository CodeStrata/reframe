# Tasks: Run daily posting and handle rejects (DTPR-C04)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C04-T1 [data] Model the data the capability reads and writes. Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037.
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA05Y, CVTRA06Y (see data-contracts.md).
- [ ] DTPR-C04-T2 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034. Rules: DTPR-BR-039, DTPR-BR-040. After: DTPR-C04-T1.
  - Keep each business rule exactly as specified.
- [ ] DTPR-C04-T3 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-F-035, DTPR-REQ-F-037, DTPR-REQ-F-036. Rules: DTPR-BR-041, DTPR-BR-042, DTPR-BR-043. After: DTPR-C04-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C04-T4 [api] Build the scheduled job. Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037. Rules: DTPR-BR-039, DTPR-BR-040, DTPR-BR-041, DTPR-BR-042, DTPR-BR-043. After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3.
  - Expose the rules as the service the screens call.
- [ ] DTPR-C04-T5 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037. Criteria: DTPR-C04-AC-01, DTPR-C04-AC-02, DTPR-C04-AC-03, DTPR-C04-AC-04, DTPR-C04-AC-05, DTPR-C04-AC-06, DTPR-C04-AC-07. After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3, DTPR-C04-T4.
  - 7 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C04-T6 [compliance] Review the handling of audit, card data, money. Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037. After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3, DTPR-C04-T4.
  - Check storage, logs, screens and audit against the rules.
