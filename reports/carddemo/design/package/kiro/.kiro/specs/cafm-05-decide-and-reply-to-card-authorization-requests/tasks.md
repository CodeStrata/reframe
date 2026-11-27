# Implementation plan: Decide and reply to card authorization requests (CAFM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C05-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060_
- [ ] 2. CAFM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057_
  - _Rules: CAFM-BR-054, CAFM-BR-055, CAFM-BR-056, CAFM-BR-057, CAFM-BR-058_
  - _After: CAFM-C05-T1_
- [ ] 3. CAFM-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-058_
  - _Rules: CAFM-BR-059_
  - _After: CAFM-C05-T1_
- [ ] 4. CAFM-C05-T4 [api] Build the services behind the screens
  - CAFM-BR-060: Publish each authorization reply once to the reply queue the requester named, carrying the request's correlation id. Send it non-persistent with a short expiry (50, in tenths of a second, so 5 seconds), so stale answers are dropped. If publishing fails, log critical error 'M004'.
  - _Requirements: CAFM-REQ-F-059, CAFM-REQ-F-060_
  - _Rules: CAFM-BR-060_
  - _After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3_
- [ ] 5. CAFM-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060_
  - _Criteria: CAFM-C05-AC-01, CAFM-C05-AC-02, CAFM-C05-AC-03, CAFM-C05-AC-04, CAFM-C05-AC-05, CAFM-C05-AC-06, CAFM-C05-AC-07, CAFM-C05-AC-08, CAFM-C05-AC-09_
  - _After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3, CAFM-C05-T4_
- [ ] 6. CAFM-C05-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060_
  - _After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3, CAFM-C05-T4_
