# Implementation plan: Report policy lookup outcomes (UP-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C05-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028, UP-REQ-F-029_
- [ ] 2. UP-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: UP-REQ-F-028_
  - _Rules: UP-BR-049_
  - _After: UP-C05-T1_
- [ ] 3. UP-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-029_
  - _Rules: UP-BR-045, UP-BR-046, UP-BR-047, UP-BR-048, UP-BR-050_
  - _After: UP-C05-T1_
- [ ] 4. UP-C05-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028, UP-REQ-F-029_
  - _Rules: UP-BR-045, UP-BR-046, UP-BR-047, UP-BR-048, UP-BR-049, UP-BR-050_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3_
- [ ] 5. UP-C05-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028, UP-REQ-F-029_
  - _Criteria: UP-C05-AC-01, UP-C05-AC-02, UP-C05-AC-03, UP-C05-AC-04, UP-C05-AC-05, UP-C05-AC-06, UP-C05-AC-07, UP-C05-AC-08_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4_
- [ ] 6. UP-C05-T6 [compliance] Review the handling of audit, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-024, UP-REQ-F-025, UP-REQ-F-026, UP-REQ-F-027, UP-REQ-F-028, UP-REQ-F-029_
  - _After: UP-C05-T1, UP-C05-T2, UP-C05-T3, UP-C05-T4_
