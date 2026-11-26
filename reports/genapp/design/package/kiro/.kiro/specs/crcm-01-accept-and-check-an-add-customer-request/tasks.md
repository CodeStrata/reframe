# Implementation plan: Accept and check an add-customer request (CRCM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CRCM-C01-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: CRCM-REQ-F-001, CRCM-REQ-F-002, CRCM-REQ-F-003, CRCM-REQ-F-004_
- [ ] 2. CRCM-C01-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CRCM-REQ-F-003, CRCM-REQ-F-004_
  - _Rules: CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-007, CRCM-BR-008_
  - _After: CRCM-C01-T1_
- [ ] 3. CRCM-C01-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CRCM-REQ-F-002_
  - _Rules: CRCM-BR-003_
  - _After: CRCM-C01-T1_
- [ ] 4. CRCM-C01-T4 [api] Build the scheduled job
  - CRCM-BR-001: Start every add-customer response with outcome '00' (success) and a policy count of '00'. Later checks overwrite the outcome only when they fail, so a caller always gets a defined outcome and policy count.
  - CRCM-BR-002: The customer-add data step must also default its outcome to '00' before it validates the request, so only a failed check or a failed store sets a non-success code.
  - CRCM-BR-008: Once the request passes the presence and minimum-length checks, the intake hands the complete request to the customer-creation service, which assigns the number and stores the customer. It then returns that service's outcome to the caller unchanged. In the new application this is an internal service call with a typed customer payload, not a fixed 32,500-byte buffer.
  - _Requirements: CRCM-REQ-F-001_
  - _Rules: CRCM-BR-001, CRCM-BR-002_
  - _After: CRCM-C01-T1, CRCM-C01-T2, CRCM-C01-T3_
- [ ] 5. CRCM-C01-T5 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: CRCM-REQ-F-001, CRCM-REQ-F-002, CRCM-REQ-F-003, CRCM-REQ-F-004_
  - _Criteria: CRCM-C01-AC-01, CRCM-C01-AC-02, CRCM-C01-AC-03, CRCM-C01-AC-04, CRCM-C01-AC-05, CRCM-C01-AC-06, CRCM-C01-AC-07, CRCM-C01-AC-08, CRCM-C01-AC-09, CRCM-C01-AC-10, CRCM-C01-AC-11, CRCM-C01-AC-12_
  - _After: CRCM-C01-T1, CRCM-C01-T2, CRCM-C01-T3, CRCM-C01-T4_
- [ ] 6. CRCM-C01-T6 [compliance] Review the handling of personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CRCM-REQ-F-001, CRCM-REQ-F-002, CRCM-REQ-F-003, CRCM-REQ-F-004_
  - _After: CRCM-C01-T1, CRCM-C01-T2, CRCM-C01-T3, CRCM-C01-T4_
