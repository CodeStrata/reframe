# Implementation plan: Log errors and stop on critical failures (CAFM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C08-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081_
- [ ] 2. CAFM-C08-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081_
  - _Rules: CAFM-BR-082, CAFM-BR-083_
  - _After: CAFM-C08-T1_
- [ ] 3. CAFM-C08-T3 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081_
  - _Criteria: CAFM-C08-AC-01, CAFM-C08-AC-02_
  - _After: CAFM-C08-T1, CAFM-C08-T2_
- [ ] 4. CAFM-C08-T4 [compliance] Review the handling of audit
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081_
  - _After: CAFM-C08-T1, CAFM-C08-T2_
