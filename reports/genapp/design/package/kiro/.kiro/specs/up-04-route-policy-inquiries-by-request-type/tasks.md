# Implementation plan: Route policy inquiries by request type (UP-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C04-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: UP-REQ-F-014, UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023_
- [ ] 2. UP-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023_
  - _Rules: UP-BR-036, UP-BR-037, UP-BR-038, UP-BR-039, UP-BR-040, UP-BR-041, UP-BR-042, UP-BR-043, UP-BR-044_
  - _After: UP-C04-T1_
- [ ] 3. UP-C04-T3 [api] Build the scheduled job
  - UP-BR-034: Every policy inquiry reply starts with return code '00'. Only a later failure (not found, reply area too small, database error or unknown request) changes it, so a request that runs cleanly always returns '00'.
  - UP-BR-035: At the start of each policy inquiry, the supplied customer number and policy number become the lookup keys. They are also kept as context for error messages, so any error logged later names the customer and policy the caller asked for.
  - _Requirements: UP-REQ-F-014_
  - _Rules: UP-BR-034, UP-BR-035_
  - _After: UP-C04-T1, UP-C04-T2_
- [ ] 4. UP-C04-T4 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-014, UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023_
  - _Criteria: UP-C04-AC-01, UP-C04-AC-02, UP-C04-AC-03, UP-C04-AC-04, UP-C04-AC-05, UP-C04-AC-06, UP-C04-AC-07, UP-C04-AC-08, UP-C04-AC-09, UP-C04-AC-10, UP-C04-AC-11, UP-C04-AC-12_
  - _After: UP-C04-T1, UP-C04-T2, UP-C04-T3_
- [ ] 5. UP-C04-T5 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-014, UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023_
  - _After: UP-C04-T1, UP-C04-T2, UP-C04-T3_
