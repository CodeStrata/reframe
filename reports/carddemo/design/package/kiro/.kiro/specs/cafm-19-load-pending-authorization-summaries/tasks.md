# Implementation plan: Load pending authorization summaries (CAFM-C19)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C19-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169_
- [ ] 2. CAFM-C19-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167_
  - _Rules: CAFM-BR-181_
  - _After: CAFM-C19-T1_
- [ ] 3. CAFM-C19-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-168, CAFM-REQ-F-169_
  - _Rules: CAFM-BR-182, CAFM-BR-183_
  - _After: CAFM-C19-T1_
- [ ] 4. CAFM-C19-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169_
  - _Rules: CAFM-BR-181, CAFM-BR-182, CAFM-BR-183_
  - _After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3_
- [ ] 5. CAFM-C19-T5 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169_
  - _Criteria: CAFM-C19-AC-01, CAFM-C19-AC-02, CAFM-C19-AC-03_
  - _After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3, CAFM-C19-T4_
- [ ] 6. CAFM-C19-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-166, CAFM-REQ-F-167, CAFM-REQ-F-168, CAFM-REQ-F-169_
  - _After: CAFM-C19-T1, CAFM-C19-T2, CAFM-C19-T3, CAFM-C19-T4_
