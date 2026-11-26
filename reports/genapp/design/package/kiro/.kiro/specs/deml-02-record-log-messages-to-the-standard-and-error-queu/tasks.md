# Implementation plan: Record log messages to the standard and error queues (DEML-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. DEML-C02-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DEML-REQ-F-006, DEML-REQ-F-007, DEML-REQ-F-005, DEML-REQ-F-008_
  - _Rules: DEML-BR-005, DEML-BR-006, DEML-BR-007, DEML-BR-008_
- [ ] 2. DEML-C02-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DEML-REQ-N-001_
  - _Rules: DEML-BR-009_
- [ ] 3. DEML-C02-T3 [api] Build the service
  - Expose the rules as the service the screens call.
  - _Requirements: DEML-REQ-F-005, DEML-REQ-F-006, DEML-REQ-F-007, DEML-REQ-F-008, DEML-REQ-N-001_
  - _Rules: DEML-BR-005, DEML-BR-006, DEML-BR-007, DEML-BR-008, DEML-BR-009_
  - _After: DEML-C02-T1, DEML-C02-T2_
- [ ] 4. DEML-C02-T4 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: DEML-REQ-F-005, DEML-REQ-F-006, DEML-REQ-F-007, DEML-REQ-F-008, DEML-REQ-N-001_
  - _Criteria: DEML-C02-AC-01, DEML-C02-AC-02, DEML-C02-AC-03, DEML-C02-AC-04, DEML-C02-AC-05, DEML-C02-AC-06_
  - _After: DEML-C02-T1, DEML-C02-T2, DEML-C02-T3_
- [ ] 5. DEML-C02-T5 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DEML-REQ-F-005, DEML-REQ-F-006, DEML-REQ-F-007, DEML-REQ-F-008, DEML-REQ-N-001_
  - _After: DEML-C02-T1, DEML-C02-T2, DEML-C02-T3_
