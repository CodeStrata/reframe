# Tasks: Print the daily transaction report with totals (DTPR-C17)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C17-T1 [data] Model the data the capability reads and writes. Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087.
  - File records: CVACT03Y, CVTRA03Y, CVTRA04Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: CVTRA07Y.
- [ ] DTPR-C17-T2 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087. Rules: DTPR-BR-093, DTPR-BR-094, DTPR-BR-096, DTPR-BR-097, DTPR-BR-098. After: DTPR-C17-T1.
  - Keep each business rule exactly as specified.
- [ ] DTPR-C17-T3 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-F-084. Rules: DTPR-BR-095. After: DTPR-C17-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C17-T4 [api] Build the scheduled job. Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087. Rules: DTPR-BR-093, DTPR-BR-094, DTPR-BR-095, DTPR-BR-096, DTPR-BR-097, DTPR-BR-098. After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3.
  - Expose the rules as the service the screens call.
- [ ] DTPR-C17-T5 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087. Criteria: DTPR-C17-AC-01, DTPR-C17-AC-02, DTPR-C17-AC-03, DTPR-C17-AC-04, DTPR-C17-AC-05, DTPR-C17-AC-06, DTPR-C17-AC-07. After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3, DTPR-C17-T4.
  - 7 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C17-T6 [compliance] Review the handling of card data, money. Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087. After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3, DTPR-C17-T4.
  - Check storage, logs, screens and audit against the rules.
