# Tasks: Update the customer's personal and contact details (CRCM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CRCM-C06-T1 [data] Model the data the capability reads and writes. Requirements: CRCM-REQ-F-022, CRCM-REQ-F-023, CRCM-REQ-F-024, CRCM-REQ-F-025, CRCM-REQ-F-026.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] CRCM-C06-T2 [business-rules] Implement the business rules. Requirements: CRCM-REQ-F-023. Rules: CRCM-BR-031. After: CRCM-C06-T1.
  - Keep each business rule exactly as specified.
- [ ] CRCM-C06-T3 [business-rules] Implement error handling and messages. Requirements: CRCM-REQ-F-024, CRCM-REQ-F-025. Rules: CRCM-BR-032, CRCM-BR-033. After: CRCM-C06-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CRCM-C06-T4 [api] Build the scheduled job. Requirements: CRCM-REQ-F-022, CRCM-REQ-F-026. Rules: CRCM-BR-030, CRCM-BR-034. After: CRCM-C06-T1, CRCM-C06-T2, CRCM-C06-T3.
  - CRCM-BR-030: Default the outcome to '00', then update the customer row found by a keyed lookup on the customer number in the request. The update has to tell 'no matching row' (outcome '01') apart from any other database failure (outcome '90').
  - CRCM-BR-034: When the database update step has finished, hand the customer record (225 bytes of customer data) and its return code to the customer-file update step, which brings the customer file into line with the database.
- [ ] CRCM-C06-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CRCM-REQ-F-022, CRCM-REQ-F-023, CRCM-REQ-F-024, CRCM-REQ-F-025, CRCM-REQ-F-026. Criteria: CRCM-C06-AC-01, CRCM-C06-AC-02, CRCM-C06-AC-03, CRCM-C06-AC-04, CRCM-C06-AC-05. After: CRCM-C06-T1, CRCM-C06-T2, CRCM-C06-T3, CRCM-C06-T4.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] CRCM-C06-T6 [compliance] Review the handling of audit, personal data. Requirements: CRCM-REQ-F-022, CRCM-REQ-F-023, CRCM-REQ-F-024, CRCM-REQ-F-025, CRCM-REQ-F-026. After: CRCM-C06-T1, CRCM-C06-T2, CRCM-C06-T3, CRCM-C06-T4.
  - Check storage, logs, screens and audit against the rules.
