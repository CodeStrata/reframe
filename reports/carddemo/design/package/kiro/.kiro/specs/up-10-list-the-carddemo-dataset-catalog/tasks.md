# Implementation plan: List the CardDemo dataset catalog (UP-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C10-T1 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-047_
  - _Rules: UP-BR-050_
- [ ] 2. UP-C10-T2 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: UP-REQ-F-047_
  - _Rules: UP-BR-050_
  - _After: UP-C10-T1_
- [ ] 3. UP-C10-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-047_
  - _Criteria: UP-C10-AC-01, UP-C10-AC-02_
  - _After: UP-C10-T1, UP-C10-T2_
