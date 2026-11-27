# Implementation plan: Print the daily transaction report with totals (DTPR-C17)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C17-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA03Y, CVTRA04Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: CVTRA07Y.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
- [ ] 2. DTPR-C17-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
  - _Rules: DTPR-BR-093, DTPR-BR-094, DTPR-BR-096, DTPR-BR-097, DTPR-BR-098_
  - _After: DTPR-C17-T1_
- [ ] 3. DTPR-C17-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-084_
  - _Rules: DTPR-BR-095_
  - _After: DTPR-C17-T1_
- [ ] 4. DTPR-C17-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
  - _Rules: DTPR-BR-093, DTPR-BR-094, DTPR-BR-095, DTPR-BR-096, DTPR-BR-097, DTPR-BR-098_
  - _After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3_
- [ ] 5. DTPR-C17-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
  - _Criteria: DTPR-C17-AC-01, DTPR-C17-AC-02, DTPR-C17-AC-03, DTPR-C17-AC-04, DTPR-C17-AC-05, DTPR-C17-AC-06, DTPR-C17-AC-07_
  - _After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3, DTPR-C17-T4_
- [ ] 6. DTPR-C17-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-082, DTPR-REQ-F-083, DTPR-REQ-F-084, DTPR-REQ-F-085, DTPR-REQ-F-086, DTPR-REQ-F-087_
  - _After: DTPR-C17-T1, DTPR-C17-T2, DTPR-C17-T3, DTPR-C17-T4_
