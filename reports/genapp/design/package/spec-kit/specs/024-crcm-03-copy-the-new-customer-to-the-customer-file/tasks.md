# Tasks: Copy the new customer to the customer file (CRCM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CRCM-C03-T1 [data] Model the data the capability reads and writes. Requirements: CRCM-REQ-F-010, CRCM-REQ-F-011, CRCM-REQ-F-012, CRCM-REQ-F-013, CRCM-REQ-F-014.
  - File records: LGCMAREA (see data-contracts.md).
  - Working records it passes or builds: LGPOLICY.
- [ ] CRCM-C03-T2 [business-rules] Implement the business rules. Requirements: CRCM-REQ-F-013, CRCM-REQ-F-014. Rules: CRCM-BR-019, CRCM-BR-020. After: CRCM-C03-T1.
  - Keep each business rule exactly as specified.
- [ ] CRCM-C03-T3 [business-rules] Implement error handling and messages. Requirements: CRCM-REQ-F-012. Rules: CRCM-BR-018. After: CRCM-C03-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CRCM-C03-T4 [api] Build the scheduled job. Requirements: CRCM-REQ-F-010, CRCM-REQ-F-011. Rules: CRCM-BR-016, CRCM-BR-017. After: CRCM-C03-T1, CRCM-C03-T2, CRCM-C03-T3.
  - CRCM-BR-016: Call the customer-file copy step only after the customer row is stored, and pass it the whole customer record including the newly assigned number. The step can be an in-process call or a message to the service that owns the customer file, but it must not run when the insert failed.
  - CRCM-BR-017: The customer file needs a store keyed by the 10-digit customer number, with one record per customer holding the number, first and last name, date of birth, house name, house number, postcode, number of policies, mobile phone, home phone and email. Adding a customer is an insert-only write, so an existing key must make the write fail.
- [ ] CRCM-C03-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CRCM-REQ-F-010, CRCM-REQ-F-011, CRCM-REQ-F-012, CRCM-REQ-F-013, CRCM-REQ-F-014. Criteria: CRCM-C03-AC-01, CRCM-C03-AC-02, CRCM-C03-AC-03, CRCM-C03-AC-04, CRCM-C03-AC-05. After: CRCM-C03-T1, CRCM-C03-T2, CRCM-C03-T3, CRCM-C03-T4.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] CRCM-C03-T6 [compliance] Review the handling of audit, personal data. Requirements: CRCM-REQ-F-010, CRCM-REQ-F-011, CRCM-REQ-F-012, CRCM-REQ-F-013, CRCM-REQ-F-014. After: CRCM-C03-T1, CRCM-C03-T2, CRCM-C03-T3, CRCM-C03-T4.
  - Check storage, logs, screens and audit against the rules.
