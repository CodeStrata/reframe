# Implementation plan: Remove dependent records on deletion (ADPLM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C04-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-022, ADPLM-REQ-F-023, ADPLM-REQ-F-024, ADPLM-REQ-F-025_
  - _Rules: ADPLM-BR-014, ADPLM-BR-022, ADPLM-BR-023, ADPLM-BR-024, ADPLM-BR-025, ADPLM-BR-026, ADPLM-BR-027_
- [ ] 2. ADPLM-C04-T2 [api] Build the scheduled job
  - ADPLM-BR-014: Enforce this in the database. A foreign key from endowment details to the policy cascades on delete, so removing a policy removes its endowment row in the same transaction, whichever code path deletes the policy.
  - _Requirements: ADPLM-REQ-F-022, ADPLM-REQ-F-023, ADPLM-REQ-F-024, ADPLM-REQ-F-025_
  - _Rules: ADPLM-BR-014, ADPLM-BR-022, ADPLM-BR-023, ADPLM-BR-024, ADPLM-BR-025, ADPLM-BR-026, ADPLM-BR-027_
  - _After: ADPLM-C04-T1_
- [ ] 3. ADPLM-C04-T3 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-022, ADPLM-REQ-F-023, ADPLM-REQ-F-024, ADPLM-REQ-F-025_
  - _Criteria: ADPLM-C04-AC-01, ADPLM-C04-AC-02, ADPLM-C04-AC-03, ADPLM-C04-AC-04, ADPLM-C04-AC-05, ADPLM-C04-AC-06, ADPLM-C04-AC-07, ADPLM-C04-AC-08_
  - _After: ADPLM-C04-T1, ADPLM-C04-T2_
- [ ] 4. ADPLM-C04-T4 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-022, ADPLM-REQ-F-023, ADPLM-REQ-F-024, ADPLM-REQ-F-025_
  - _After: ADPLM-C04-T1, ADPLM-C04-T2_
