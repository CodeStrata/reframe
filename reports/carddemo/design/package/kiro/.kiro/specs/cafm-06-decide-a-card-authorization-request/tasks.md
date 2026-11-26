# Implementation plan: Decide a card authorization request (CAFM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C06-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070_
- [ ] 2. CAFM-C06-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CAFM-BR-070.
  - _Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-065, CAFM-REQ-F-070_
  - _Rules: CAFM-BR-061, CAFM-BR-062, CAFM-BR-063, CAFM-BR-064, CAFM-BR-065, CAFM-BR-067, CAFM-BR-068, CAFM-BR-069, CAFM-BR-070_
  - _After: CAFM-C06-T1_
- [ ] 3. CAFM-C06-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-066_
  - _Rules: CAFM-BR-066_
  - _After: CAFM-C06-T1_
- [ ] 4. CAFM-C06-T4 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070_
  - _Criteria: CAFM-C06-AC-01, CAFM-C06-AC-02, CAFM-C06-AC-03, CAFM-C06-AC-04, CAFM-C06-AC-05, CAFM-C06-AC-06, CAFM-C06-AC-07, CAFM-C06-AC-08, CAFM-C06-AC-09, CAFM-C06-AC-10, CAFM-C06-AC-11, CAFM-C06-AC-12, CAFM-C06-AC-13_
  - _After: CAFM-C06-T1, CAFM-C06-T2, CAFM-C06-T3_
- [ ] 5. CAFM-C06-T5 [compliance] Review the handling of audit, card data, money, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070_
  - _After: CAFM-C06-T1, CAFM-C06-T2, CAFM-C06-T3_
