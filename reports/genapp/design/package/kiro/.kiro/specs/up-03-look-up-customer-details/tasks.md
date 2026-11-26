# Implementation plan: Look up customer details (UP-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C03-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
  - _Requirements: UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009, UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012, UP-REQ-F-013_
- [ ] 2. UP-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-010, UP-REQ-F-011_
  - _Rules: UP-BR-025, UP-BR-026, UP-BR-027, UP-BR-028, UP-BR-030, UP-BR-031_
  - _After: UP-C03-T1_
- [ ] 3. UP-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: UP-REQ-F-006, UP-REQ-F-012, UP-REQ-F-013_
  - _Rules: UP-BR-023, UP-BR-024, UP-BR-032, UP-BR-033_
  - _After: UP-C03-T1_
- [ ] 4. UP-C03-T4 [api] Build the scheduled job
  - UP-BR-025: Every customer inquiry reply starts as a success: return code '00' and number of policies '00' are set before any check runs. Later checks overwrite them only on failure.
  - UP-BR-029: Once a request passes the length check, the inquiry calls the customer data service (LGICDB01 today) with the whole request (32500 bytes today). It passes that service's reply and return code back to the caller unchanged. In the new application this is a call from the inquiry API to the customer lookup service, keyed by customer number.
  - _Requirements: UP-REQ-F-009_
  - _Rules: UP-BR-029_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3_
- [ ] 5. UP-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009, UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012, UP-REQ-F-013_
  - _Criteria: UP-C03-AC-01, UP-C03-AC-02, UP-C03-AC-03, UP-C03-AC-04, UP-C03-AC-05, UP-C03-AC-06, UP-C03-AC-07, UP-C03-AC-08, UP-C03-AC-09, UP-C03-AC-10, UP-C03-AC-11, UP-C03-AC-12, UP-C03-AC-13_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4_
- [ ] 6. UP-C03-T6 [compliance] Review the handling of audit, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009, UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012, UP-REQ-F-013_
  - _After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4_
