# Implementation plan: Run daily posting and handle rejects (DTPR-C04)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C04-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA05Y, CVTRA06Y (see data-contracts.md).
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037_
- [ ] 2. DTPR-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034_
  - _Rules: DTPR-BR-039, DTPR-BR-040_
  - _After: DTPR-C04-T1_
- [ ] 3. DTPR-C04-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-F-035, DTPR-REQ-F-037, DTPR-REQ-F-036_
  - _Rules: DTPR-BR-041, DTPR-BR-042, DTPR-BR-043_
  - _After: DTPR-C04-T1_
- [ ] 4. DTPR-C04-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037_
  - _Rules: DTPR-BR-039, DTPR-BR-040, DTPR-BR-041, DTPR-BR-042, DTPR-BR-043_
  - _After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3_
- [ ] 5. DTPR-C04-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037_
  - _Criteria: DTPR-C04-AC-01, DTPR-C04-AC-02, DTPR-C04-AC-03, DTPR-C04-AC-04, DTPR-C04-AC-05, DTPR-C04-AC-06, DTPR-C04-AC-07_
  - _After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3, DTPR-C04-T4_
- [ ] 6. DTPR-C04-T6 [compliance] Review the handling of audit, card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-033, DTPR-REQ-F-034, DTPR-REQ-F-035, DTPR-REQ-F-036, DTPR-REQ-F-037_
  - _After: DTPR-C04-T1, DTPR-C04-T2, DTPR-C04-T3, DTPR-C04-T4_
