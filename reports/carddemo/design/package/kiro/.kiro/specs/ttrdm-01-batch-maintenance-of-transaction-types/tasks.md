# Implementation plan: Batch maintenance of transaction types (TTRDM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C01-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-001, TTRDM-REQ-F-002, TTRDM-REQ-F-003, TTRDM-REQ-F-004, TTRDM-REQ-F-006, TTRDM-REQ-F-009_
  - _Rules: TTRDM-BR-001, TTRDM-BR-002, TTRDM-BR-003, TTRDM-BR-004, TTRDM-BR-006, TTRDM-BR-010_
- [ ] 2. TTRDM-C01-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-005, TTRDM-REQ-F-007, TTRDM-REQ-F-008, TTRDM-REQ-F-010, TTRDM-REQ-F-011, TTRDM-REQ-N-001_
  - _Rules: TTRDM-BR-005, TTRDM-BR-007, TTRDM-BR-008, TTRDM-BR-009, TTRDM-BR-011, TTRDM-BR-012, TTRDM-BR-013_
- [ ] 3. TTRDM-C01-T3 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: TTRDM-REQ-F-001, TTRDM-REQ-F-002, TTRDM-REQ-F-003, TTRDM-REQ-F-004, TTRDM-REQ-F-005, TTRDM-REQ-F-006, TTRDM-REQ-F-007, TTRDM-REQ-F-008, TTRDM-REQ-F-009, TTRDM-REQ-F-010, TTRDM-REQ-F-011, TTRDM-REQ-N-001_
  - _Rules: TTRDM-BR-001, TTRDM-BR-002, TTRDM-BR-003, TTRDM-BR-004, TTRDM-BR-005, TTRDM-BR-006, TTRDM-BR-007, TTRDM-BR-008, TTRDM-BR-009, TTRDM-BR-010, TTRDM-BR-011, TTRDM-BR-012, TTRDM-BR-013_
  - _After: TTRDM-C01-T1, TTRDM-C01-T2_
- [ ] 4. TTRDM-C01-T4 [test-generation] Write a test for every acceptance criterion
  - 16 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-001, TTRDM-REQ-F-002, TTRDM-REQ-F-003, TTRDM-REQ-F-004, TTRDM-REQ-F-005, TTRDM-REQ-F-006, TTRDM-REQ-F-007, TTRDM-REQ-F-008, TTRDM-REQ-F-009, TTRDM-REQ-F-010, TTRDM-REQ-F-011, TTRDM-REQ-N-001_
  - _Criteria: TTRDM-C01-AC-01, TTRDM-C01-AC-02, TTRDM-C01-AC-03, TTRDM-C01-AC-04, TTRDM-C01-AC-05, TTRDM-C01-AC-06, TTRDM-C01-AC-07, TTRDM-C01-AC-08, TTRDM-C01-AC-09, TTRDM-C01-AC-10, TTRDM-C01-AC-11, TTRDM-C01-AC-12, TTRDM-C01-AC-13, TTRDM-C01-AC-14, TTRDM-C01-AC-15, TTRDM-C01-AC-16_
  - _After: TTRDM-C01-T1, TTRDM-C01-T2, TTRDM-C01-T3_
