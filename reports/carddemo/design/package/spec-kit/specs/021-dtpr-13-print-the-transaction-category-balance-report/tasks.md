# Tasks: Print the transaction category balance report (DTPR-C13)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C13-T1 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-N-007, DTPR-REQ-N-008, DTPR-REQ-F-071. Rules: DTPR-BR-078, DTPR-BR-079.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C13-T2 [api] Build the scheduled job. Requirements: DTPR-REQ-F-070. Rules: DTPR-BR-077. After: DTPR-C13-T1.
  - DTPR-BR-077: Before reporting, remove the previous category balance report and take a complete point-in-time snapshot of all category balance records as a new numbered backup version. The report is then built from that snapshot, not from the live balances, so it reflects one consistent moment.
- [ ] DTPR-C13-T3 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-070, DTPR-REQ-F-071, DTPR-REQ-N-007, DTPR-REQ-N-008. Criteria: DTPR-C13-AC-01, DTPR-C13-AC-02, DTPR-C13-AC-03. After: DTPR-C13-T1, DTPR-C13-T2.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C13-T4 [compliance] Review the handling of money. Requirements: DTPR-REQ-F-070, DTPR-REQ-F-071, DTPR-REQ-N-007, DTPR-REQ-N-008. After: DTPR-C13-T1, DTPR-C13-T2.
  - Check storage, logs, screens and audit against the rules.
