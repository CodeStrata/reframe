# Tasks: Accept and check an add-customer request (CRCM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CRCM-C01-T1 [data] Model the data the capability reads and writes. Requirements: CRCM-REQ-F-001, CRCM-REQ-F-002, CRCM-REQ-F-003, CRCM-REQ-F-004.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] CRCM-C01-T2 [business-rules] Implement the business rules. Requirements: CRCM-REQ-F-003, CRCM-REQ-F-004. Rules: CRCM-BR-004, CRCM-BR-005, CRCM-BR-006, CRCM-BR-007, CRCM-BR-008. After: CRCM-C01-T1.
  - Keep each business rule exactly as specified.
- [ ] CRCM-C01-T3 [business-rules] Implement error handling and messages. Requirements: CRCM-REQ-F-002. Rules: CRCM-BR-003. After: CRCM-C01-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CRCM-C01-T4 [api] Build the scheduled job. Requirements: CRCM-REQ-F-001. Rules: CRCM-BR-001, CRCM-BR-002. After: CRCM-C01-T1, CRCM-C01-T2, CRCM-C01-T3.
  - CRCM-BR-001: Start every add-customer response with outcome '00' (success) and a policy count of '00'. Later checks overwrite the outcome only when they fail, so a caller always gets a defined outcome and policy count.
  - CRCM-BR-002: The customer-add data step must also default its outcome to '00' before it validates the request, so only a failed check or a failed store sets a non-success code.
  - CRCM-BR-008: Once the request passes the presence and minimum-length checks, the intake hands the complete request to the customer-creation service, which assigns the number and stores the customer. It then returns that service's outcome to the caller unchanged. In the new application this is an internal service call with a typed customer payload, not a fixed 32,500-byte buffer.
- [ ] CRCM-C01-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CRCM-REQ-F-001, CRCM-REQ-F-002, CRCM-REQ-F-003, CRCM-REQ-F-004. Criteria: CRCM-C01-AC-01, CRCM-C01-AC-02, CRCM-C01-AC-03, CRCM-C01-AC-04, CRCM-C01-AC-05, CRCM-C01-AC-06, CRCM-C01-AC-07, CRCM-C01-AC-08, CRCM-C01-AC-09, CRCM-C01-AC-10, CRCM-C01-AC-11, CRCM-C01-AC-12. After: CRCM-C01-T1, CRCM-C01-T2, CRCM-C01-T3, CRCM-C01-T4.
  - 12 acceptance criteria, each a test named by its ID.
- [ ] CRCM-C01-T6 [compliance] Review the handling of personal data. Requirements: CRCM-REQ-F-001, CRCM-REQ-F-002, CRCM-REQ-F-003, CRCM-REQ-F-004. After: CRCM-C01-T1, CRCM-C01-T2, CRCM-C01-T3, CRCM-C01-T4.
  - Check storage, logs, screens and audit against the rules.
