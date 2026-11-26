# Implementation plan: Record pending authorization summary and detail (CAFM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C07-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
- [ ] 2. CAFM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-077, CAFM-REQ-F-078_
  - _Rules: CAFM-BR-071, CAFM-BR-072, CAFM-BR-073, CAFM-BR-074, CAFM-BR-075, CAFM-BR-079, CAFM-BR-080_
  - _After: CAFM-C07-T1_
- [ ] 3. CAFM-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-075, CAFM-REQ-F-079_
  - _Rules: CAFM-BR-076, CAFM-BR-077, CAFM-BR-081_
  - _After: CAFM-C07-T1_
- [ ] 4. CAFM-C07-T4 [api] Build the services behind the screens
  - CAFM-BR-072: Save the pending authorization summary as an upsert keyed by account id: update it when it was found during lookup, or insert a new one when it did not exist. Report a failure as critical error 'I003' 'IMS UPDATE SUMRY FAILED'.
  - CAFM-BR-078: Insert one authorization detail row as a child of the account's summary, built from the request and reply fields listed in the rule, and keyed so details are read newest first. Report a failure as critical error 'I004' 'IMS INSERT DETL FAILED'.
  - _Requirements: CAFM-REQ-F-076_
  - _Rules: CAFM-BR-078_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3_
- [ ] 5. CAFM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
  - _Criteria: CAFM-C07-AC-01, CAFM-C07-AC-02, CAFM-C07-AC-03, CAFM-C07-AC-04, CAFM-C07-AC-05, CAFM-C07-AC-06, CAFM-C07-AC-07, CAFM-C07-AC-08, CAFM-C07-AC-09, CAFM-C07-AC-10, CAFM-C07-AC-11, CAFM-C07-AC-12, CAFM-C07-AC-13_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3, CAFM-C07-T4_
- [ ] 6. CAFM-C07-T6 [compliance] Review the handling of audit, card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3, CAFM-C07-T4_
