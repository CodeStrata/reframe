# Implementation plan: Business-monitor symbol list (not delivered) (TSM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TSM-C04-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: TSM-BR-013, TSM-BR-015.
  - _Requirements: TSM-REQ-F-016, TSM-REQ-F-017, TSM-REQ-F-018_
  - _Rules: TSM-BR-013, TSM-BR-015_
- [ ] 2. TSM-C04-T2 [api] Build the scheduled job
  - Expose the rules as the service the screens call.
  - _Requirements: TSM-REQ-F-016, TSM-REQ-F-017, TSM-REQ-F-018_
  - _Rules: TSM-BR-013, TSM-BR-015_
  - _After: TSM-C04-T1_
- [ ] 3. TSM-C04-T3 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: TSM-REQ-F-016, TSM-REQ-F-017, TSM-REQ-F-018_
  - _Criteria: TSM-C04-AC-01, TSM-C04-AC-02, TSM-C04-AC-03_
  - _After: TSM-C04-T1, TSM-C04-T2_
