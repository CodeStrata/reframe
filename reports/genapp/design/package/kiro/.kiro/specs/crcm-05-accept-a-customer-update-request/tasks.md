# Implementation plan: Accept a customer update request (CRCM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CRCM-C05-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA.
  - _Requirements: CRCM-REQ-F-019, CRCM-REQ-F-020, CRCM-REQ-F-021_
- [ ] 2. CRCM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CRCM-BR-026, CRCM-BR-027.
  - _Requirements: CRCM-REQ-F-020, CRCM-REQ-F-021, CRCM-REQ-F-019_
  - _Rules: CRCM-BR-026, CRCM-BR-027, CRCM-BR-028, CRCM-BR-029_
  - _After: CRCM-C05-T1_
- [ ] 3. CRCM-C05-T3 [api] Build the scheduled job
  - CRCM-BR-026: Default the update response outcome to '00' (success) before the request type is checked. The type check (failure '99') and the downstream update service overwrite it only when they fail.
  - _Requirements: CRCM-REQ-F-019, CRCM-REQ-F-020, CRCM-REQ-F-021_
  - _Rules: CRCM-BR-026, CRCM-BR-027, CRCM-BR-028, CRCM-BR-029_
  - _After: CRCM-C05-T1, CRCM-C05-T2_
- [ ] 4. CRCM-C05-T4 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: CRCM-REQ-F-019, CRCM-REQ-F-020, CRCM-REQ-F-021_
  - _Criteria: CRCM-C05-AC-01, CRCM-C05-AC-02, CRCM-C05-AC-03, CRCM-C05-AC-04_
  - _After: CRCM-C05-T1, CRCM-C05-T2, CRCM-C05-T3_
- [ ] 5. CRCM-C05-T5 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CRCM-REQ-F-019, CRCM-REQ-F-020, CRCM-REQ-F-021_
  - _After: CRCM-C05-T1, CRCM-C05-T2, CRCM-C05-T3_
