# Implementation plan: Delete a policy (ADPLM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C14-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA.
  - _Requirements: ADPLM-REQ-F-078, ADPLM-REQ-F-079, ADPLM-REQ-F-080, ADPLM-REQ-F-081, ADPLM-REQ-F-082, ADPLM-REQ-F-083, ADPLM-REQ-F-084, ADPLM-REQ-F-085, ADPLM-REQ-F-086, ADPLM-REQ-F-087_
- [ ] 2. ADPLM-C14-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-080, ADPLM-REQ-F-082, ADPLM-REQ-F-083, ADPLM-REQ-F-084, ADPLM-REQ-F-086_
  - _Rules: ADPLM-BR-085, ADPLM-BR-086, ADPLM-BR-088, ADPLM-BR-089, ADPLM-BR-090, ADPLM-BR-091, ADPLM-BR-092, ADPLM-BR-094_
  - _After: ADPLM-C14-T1_
- [ ] 3. ADPLM-C14-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ADPLM-REQ-F-078, ADPLM-REQ-F-087_
  - _Rules: ADPLM-BR-083, ADPLM-BR-095_
  - _After: ADPLM-C14-T1_
- [ ] 4. ADPLM-C14-T4 [api] Build the scheduled job
  - ADPLM-BR-084: Set the response code to '00' as soon as a request with data is accepted. Only a later validation failure or the outcome of the database delete may replace it.
  - ADPLM-BR-087: Compare the request identifier case-insensitively, for example by upper-casing it before matching against '01DEND', '01DMOT', '01DHOU' and '01DCOM', so that '01dend' behaves like '01DEND'.
  - ADPLM-BR-093: Define the endowment, house, motor and commercial detail tables with a foreign key to the policy table and ON DELETE CASCADE. Deleting the policy row then removes its details in the same transaction, with no separate delete statements.
  - _Requirements: ADPLM-REQ-F-079, ADPLM-REQ-F-081, ADPLM-REQ-F-085_
  - _Rules: ADPLM-BR-084, ADPLM-BR-087, ADPLM-BR-093_
  - _After: ADPLM-C14-T1, ADPLM-C14-T2, ADPLM-C14-T3_
- [ ] 5. ADPLM-C14-T5 [test-generation] Write a test for every acceptance criterion
  - 14 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-078, ADPLM-REQ-F-079, ADPLM-REQ-F-080, ADPLM-REQ-F-081, ADPLM-REQ-F-082, ADPLM-REQ-F-083, ADPLM-REQ-F-084, ADPLM-REQ-F-085, ADPLM-REQ-F-086, ADPLM-REQ-F-087_
  - _Criteria: ADPLM-C14-AC-01, ADPLM-C14-AC-02, ADPLM-C14-AC-03, ADPLM-C14-AC-04, ADPLM-C14-AC-05, ADPLM-C14-AC-06, ADPLM-C14-AC-07, ADPLM-C14-AC-08, ADPLM-C14-AC-09, ADPLM-C14-AC-10, ADPLM-C14-AC-11, ADPLM-C14-AC-12, ADPLM-C14-AC-13, ADPLM-C14-AC-14_
  - _After: ADPLM-C14-T1, ADPLM-C14-T2, ADPLM-C14-T3, ADPLM-C14-T4_
- [ ] 6. ADPLM-C14-T6 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-078, ADPLM-REQ-F-079, ADPLM-REQ-F-080, ADPLM-REQ-F-081, ADPLM-REQ-F-082, ADPLM-REQ-F-083, ADPLM-REQ-F-084, ADPLM-REQ-F-085, ADPLM-REQ-F-086, ADPLM-REQ-F-087_
  - _After: ADPLM-C14-T1, ADPLM-C14-T2, ADPLM-C14-T3, ADPLM-C14-T4_
