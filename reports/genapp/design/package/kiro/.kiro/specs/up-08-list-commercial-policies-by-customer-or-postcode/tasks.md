# Implementation plan: List commercial policies by customer or postcode (UP-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C08-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-048, UP-REQ-F-049, UP-REQ-F-050_
- [ ] 2. UP-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-050_
  - _Rules: UP-BR-067, UP-BR-068, UP-BR-069, UP-BR-072_
  - _After: UP-C08-T1_
- [ ] 3. UP-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-048, UP-REQ-F-049_
  - _Rules: UP-BR-070, UP-BR-071_
  - _After: UP-C08-T1_
- [ ] 4. UP-C08-T4 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-048, UP-REQ-F-049, UP-REQ-F-050_
  - _Rules: UP-BR-067, UP-BR-068, UP-BR-069, UP-BR-070, UP-BR-071, UP-BR-072_
  - _After: UP-C08-T1, UP-C08-T2, UP-C08-T3_
- [ ] 5. UP-C08-T5 [test-generation] Write a test for every acceptance criterion
  - 7 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-048, UP-REQ-F-049, UP-REQ-F-050_
  - _Criteria: UP-C08-AC-01, UP-C08-AC-02, UP-C08-AC-03, UP-C08-AC-04, UP-C08-AC-05, UP-C08-AC-06, UP-C08-AC-07_
  - _After: UP-C08-T1, UP-C08-T2, UP-C08-T3, UP-C08-T4_
- [ ] 6. UP-C08-T6 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-045, UP-REQ-F-046, UP-REQ-F-047, UP-REQ-F-048, UP-REQ-F-049, UP-REQ-F-050_
  - _After: UP-C08-T1, UP-C08-T2, UP-C08-T3, UP-C08-T4_
