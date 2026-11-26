# Implementation plan: Store product details for a new policy (ADPLM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. ADPLM-C08-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: ADPLM-REQ-F-047, ADPLM-REQ-F-048, ADPLM-REQ-F-049, ADPLM-REQ-F-050, ADPLM-REQ-F-051, ADPLM-REQ-F-052, ADPLM-REQ-F-053, ADPLM-REQ-F-054_
- [ ] 2. ADPLM-C08-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: ADPLM-REQ-F-047, ADPLM-REQ-F-048, ADPLM-REQ-F-050, ADPLM-REQ-F-051, ADPLM-REQ-F-052_
  - _Rules: ADPLM-BR-052, ADPLM-BR-053, ADPLM-BR-055, ADPLM-BR-056, ADPLM-BR-057_
  - _After: ADPLM-C08-T1_
- [ ] 3. ADPLM-C08-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: ADPLM-REQ-F-049, ADPLM-REQ-F-054_
  - _Rules: ADPLM-BR-054, ADPLM-BR-059_
  - _After: ADPLM-C08-T1_
- [ ] 4. ADPLM-C08-T4 [api] Build the scheduled job
  - ADPLM-BR-058: A plain field-to-column mapping for the commercial details: address, postcode, latitude, longitude, customer name, property type, the four perils and premiums, status and rejection reason, stored exactly as supplied. There is no rating engine or status derivation in this step.
  - _Requirements: ADPLM-REQ-F-053_
  - _Rules: ADPLM-BR-058_
  - _After: ADPLM-C08-T1, ADPLM-C08-T2, ADPLM-C08-T3_
- [ ] 5. ADPLM-C08-T5 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: ADPLM-REQ-F-047, ADPLM-REQ-F-048, ADPLM-REQ-F-049, ADPLM-REQ-F-050, ADPLM-REQ-F-051, ADPLM-REQ-F-052, ADPLM-REQ-F-053, ADPLM-REQ-F-054_
  - _Criteria: ADPLM-C08-AC-01, ADPLM-C08-AC-02, ADPLM-C08-AC-03, ADPLM-C08-AC-04, ADPLM-C08-AC-05, ADPLM-C08-AC-06, ADPLM-C08-AC-07, ADPLM-C08-AC-08, ADPLM-C08-AC-09_
  - _After: ADPLM-C08-T1, ADPLM-C08-T2, ADPLM-C08-T3, ADPLM-C08-T4_
- [ ] 6. ADPLM-C08-T6 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: ADPLM-REQ-F-047, ADPLM-REQ-F-048, ADPLM-REQ-F-049, ADPLM-REQ-F-050, ADPLM-REQ-F-051, ADPLM-REQ-F-052, ADPLM-REQ-F-053, ADPLM-REQ-F-054_
  - _After: ADPLM-C08-T1, ADPLM-C08-T2, ADPLM-C08-T3, ADPLM-C08-T4_
