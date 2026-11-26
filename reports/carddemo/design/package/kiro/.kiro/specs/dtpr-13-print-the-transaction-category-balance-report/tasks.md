# Implementation plan: Print the transaction category balance report (DTPR-C13)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C13-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-007, DTPR-REQ-N-008, DTPR-REQ-F-071_
  - _Rules: DTPR-BR-078, DTPR-BR-079_
- [ ] 2. DTPR-C13-T2 [api] Build the scheduled job
  - DTPR-BR-077: Before reporting, remove the previous category balance report and take a complete point-in-time snapshot of all category balance records as a new numbered backup version. The report is then built from that snapshot, not from the live balances, so it reflects one consistent moment.
  - _Requirements: DTPR-REQ-F-070_
  - _Rules: DTPR-BR-077_
  - _After: DTPR-C13-T1_
- [ ] 3. DTPR-C13-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-070, DTPR-REQ-F-071, DTPR-REQ-N-007, DTPR-REQ-N-008_
  - _Criteria: DTPR-C13-AC-01, DTPR-C13-AC-02, DTPR-C13-AC-03_
  - _After: DTPR-C13-T1, DTPR-C13-T2_
- [ ] 4. DTPR-C13-T4 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-070, DTPR-REQ-F-071, DTPR-REQ-N-007, DTPR-REQ-N-008_
  - _After: DTPR-C13-T1, DTPR-C13-T2_
