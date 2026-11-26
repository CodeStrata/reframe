# Implementation plan: Add a policy to the policy database (ADPLM-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C10-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: ADPLM-REQ-F-056, ADPLM-REQ-F-057, ADPLM-REQ-F-058, ADPLM-REQ-F-059, ADPLM-REQ-F-060, ADPLM-REQ-F-061_
- [ ] 2. ADPLM-C10-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-058, ADPLM-REQ-F-060_
  - _Rules: ADPLM-BR-063, ADPLM-BR-065_
  - _After: ADPLM-C10-T1_
- [ ] 3. ADPLM-C10-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ADPLM-REQ-F-056, ADPLM-REQ-F-061_
  - _Rules: ADPLM-BR-061, ADPLM-BR-066_
  - _After: ADPLM-C10-T1_
- [ ] 4. ADPLM-C10-T4 [api] Build the scheduled job
  - ADPLM-BR-062: Every request that has data starts with result code '00'. Validation and persistence steps overwrite it only when they fail.
  - ADPLM-BR-064: The entry service checks only that the 28-character header is present, then passes the whole request to the policy registration service (LGAPDB01). That service does the product-specific length check and the inserts inside a single transaction, and the entry service returns its result to the caller.
  - _Requirements: ADPLM-REQ-F-057, ADPLM-REQ-F-059_
  - _Rules: ADPLM-BR-062, ADPLM-BR-064_
  - _After: ADPLM-C10-T1, ADPLM-C10-T2, ADPLM-C10-T3_
- [ ] 5. ADPLM-C10-T5 [test-generation] Write a test for every acceptance criterion
  - 8 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-056, ADPLM-REQ-F-057, ADPLM-REQ-F-058, ADPLM-REQ-F-059, ADPLM-REQ-F-060, ADPLM-REQ-F-061_
  - _Criteria: ADPLM-C10-AC-01, ADPLM-C10-AC-02, ADPLM-C10-AC-03, ADPLM-C10-AC-04, ADPLM-C10-AC-05, ADPLM-C10-AC-06, ADPLM-C10-AC-07, ADPLM-C10-AC-08_
  - _After: ADPLM-C10-T1, ADPLM-C10-T2, ADPLM-C10-T3, ADPLM-C10-T4_
- [ ] 6. ADPLM-C10-T6 [compliance] Review the handling of audit, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-056, ADPLM-REQ-F-057, ADPLM-REQ-F-058, ADPLM-REQ-F-059, ADPLM-REQ-F-060, ADPLM-REQ-F-061_
  - _After: ADPLM-C10-T1, ADPLM-C10-T2, ADPLM-C10-T3, ADPLM-C10-T4_
