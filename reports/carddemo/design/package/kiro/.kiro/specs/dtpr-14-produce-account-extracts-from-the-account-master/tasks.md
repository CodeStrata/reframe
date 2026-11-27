# Implementation plan: Produce account extracts from the account master (DTPR-C14)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

- [ ] 1. DTPR-C14-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: DTPR-REQ-F-073_
  - _Rules: DTPR-BR-081_
- [ ] 2. DTPR-C14-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: DTPR-REQ-N-009, DTPR-REQ-N-010_
  - _Rules: DTPR-BR-082_
- [ ] 3. DTPR-C14-T3 [api] Build the scheduled job
  - DTPR-BR-080: The extract job must clear out the previous run's account extract, account array extract and variable-record extract before writing, so each run's outputs are regenerated from scratch and never appended to or merged with older data.
  - _Requirements: DTPR-REQ-F-072_
  - _Rules: DTPR-BR-080_
  - _After: DTPR-C14-T1, DTPR-C14-T2_
- [ ] 4. DTPR-C14-T4 [test-generation] Write a test for every acceptance criterion
  - 3 acceptance criteria, each a test named by its ID.
  - _Requirements: DTPR-REQ-F-072, DTPR-REQ-F-073, DTPR-REQ-N-009, DTPR-REQ-N-010_
  - _Criteria: DTPR-C14-AC-01, DTPR-C14-AC-02, DTPR-C14-AC-03_
  - _After: DTPR-C14-T1, DTPR-C14-T2, DTPR-C14-T3_
- [ ] 5. DTPR-C14-T5 [compliance] Review the handling of money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: DTPR-REQ-F-072, DTPR-REQ-F-073, DTPR-REQ-N-009, DTPR-REQ-N-010_
  - _After: DTPR-C14-T1, DTPR-C14-T2, DTPR-C14-T3_
