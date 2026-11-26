# Tasks: Store product details for a new policy (ADPLM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C08-T1 [data] Model the data the capability reads and writes. Requirements: ADPLM-REQ-F-047, ADPLM-REQ-F-048, ADPLM-REQ-F-049, ADPLM-REQ-F-050, ADPLM-REQ-F-051, ADPLM-REQ-F-052, ADPLM-REQ-F-053, ADPLM-REQ-F-054.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] ADPLM-C08-T2 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-047, ADPLM-REQ-F-048, ADPLM-REQ-F-050, ADPLM-REQ-F-051, ADPLM-REQ-F-052. Rules: ADPLM-BR-052, ADPLM-BR-053, ADPLM-BR-055, ADPLM-BR-056, ADPLM-BR-057. After: ADPLM-C08-T1.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C08-T3 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-049, ADPLM-REQ-F-054. Rules: ADPLM-BR-054, ADPLM-BR-059. After: ADPLM-C08-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C08-T4 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-053. Rules: ADPLM-BR-058. After: ADPLM-C08-T1, ADPLM-C08-T2, ADPLM-C08-T3.
  - ADPLM-BR-058: A plain field-to-column mapping for the commercial details: address, postcode, latitude, longitude, customer name, property type, the four perils and premiums, status and rejection reason, stored exactly as supplied. There is no rating engine or status derivation in this step.
- [ ] ADPLM-C08-T5 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-047, ADPLM-REQ-F-048, ADPLM-REQ-F-049, ADPLM-REQ-F-050, ADPLM-REQ-F-051, ADPLM-REQ-F-052, ADPLM-REQ-F-053, ADPLM-REQ-F-054. Criteria: ADPLM-C08-AC-01, ADPLM-C08-AC-02, ADPLM-C08-AC-03, ADPLM-C08-AC-04, ADPLM-C08-AC-05, ADPLM-C08-AC-06, ADPLM-C08-AC-07, ADPLM-C08-AC-08, ADPLM-C08-AC-09. After: ADPLM-C08-T1, ADPLM-C08-T2, ADPLM-C08-T3, ADPLM-C08-T4.
  - 9 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C08-T6 [compliance] Review the handling of money, personal data. Requirements: ADPLM-REQ-F-047, ADPLM-REQ-F-048, ADPLM-REQ-F-049, ADPLM-REQ-F-050, ADPLM-REQ-F-051, ADPLM-REQ-F-052, ADPLM-REQ-F-053, ADPLM-REQ-F-054. After: ADPLM-C08-T1, ADPLM-C08-T2, ADPLM-C08-T3, ADPLM-C08-T4.
  - Check storage, logs, screens and audit against the rules.
