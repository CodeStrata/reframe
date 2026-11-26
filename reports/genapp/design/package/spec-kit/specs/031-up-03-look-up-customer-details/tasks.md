# Tasks: Look up customer details (UP-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C03-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009, UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012, UP-REQ-F-013.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] UP-C03-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-010, UP-REQ-F-011. Rules: UP-BR-025, UP-BR-026, UP-BR-027, UP-BR-028, UP-BR-030, UP-BR-031. After: UP-C03-T1.
  - Keep each business rule exactly as specified.
- [ ] UP-C03-T3 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-006, UP-REQ-F-012, UP-REQ-F-013. Rules: UP-BR-023, UP-BR-024, UP-BR-032, UP-BR-033. After: UP-C03-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C03-T4 [api] Build the scheduled job. Requirements: UP-REQ-F-009. Rules: UP-BR-029. After: UP-C03-T1, UP-C03-T2, UP-C03-T3.
  - UP-BR-025: Every customer inquiry reply starts as a success: return code '00' and number of policies '00' are set before any check runs. Later checks overwrite them only on failure.
  - UP-BR-029: Once a request passes the length check, the inquiry calls the customer data service (LGICDB01 today) with the whole request (32500 bytes today). It passes that service's reply and return code back to the caller unchanged. In the new application this is a call from the inquiry API to the customer lookup service, keyed by customer number.
- [ ] UP-C03-T5 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009, UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012, UP-REQ-F-013. Criteria: UP-C03-AC-01, UP-C03-AC-02, UP-C03-AC-03, UP-C03-AC-04, UP-C03-AC-05, UP-C03-AC-06, UP-C03-AC-07, UP-C03-AC-08, UP-C03-AC-09, UP-C03-AC-10, UP-C03-AC-11, UP-C03-AC-12, UP-C03-AC-13. After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] UP-C03-T6 [compliance] Review the handling of audit, personal data. Requirements: UP-REQ-F-006, UP-REQ-F-007, UP-REQ-F-008, UP-REQ-F-009, UP-REQ-F-010, UP-REQ-F-011, UP-REQ-F-012, UP-REQ-F-013. After: UP-C03-T1, UP-C03-T2, UP-C03-T3, UP-C03-T4.
  - Check storage, logs, screens and audit against the rules.
