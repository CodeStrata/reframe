# Tasks: Create the new customer's security record (CRCM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CRCM-C04-T1 [data] Model the data the capability reads and writes. Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017, CRCM-REQ-F-018.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] CRCM-C04-T2 [business-rules] Implement the business rules. Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017. Rules: CRCM-BR-021, CRCM-BR-022, CRCM-BR-023, CRCM-BR-024. After: CRCM-C04-T1.
  - Keep each business rule exactly as specified.
- [ ] CRCM-C04-T3 [business-rules] Implement error handling and messages. Requirements: CRCM-REQ-F-018. Rules: CRCM-BR-025. After: CRCM-C04-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CRCM-C04-T4 [api] Build the scheduled job. Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017, CRCM-REQ-F-018. Rules: CRCM-BR-021, CRCM-BR-022, CRCM-BR-023, CRCM-BR-024, CRCM-BR-025. After: CRCM-C04-T1, CRCM-C04-T2, CRCM-C04-T3.
  - Expose the rules as the service the screens call.
- [ ] CRCM-C04-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017, CRCM-REQ-F-018. Criteria: CRCM-C04-AC-01, CRCM-C04-AC-02, CRCM-C04-AC-03, CRCM-C04-AC-04, CRCM-C04-AC-05. After: CRCM-C04-T1, CRCM-C04-T2, CRCM-C04-T3, CRCM-C04-T4.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] CRCM-C04-T6 [compliance] Review the handling of audit, personal data, security. Requirements: CRCM-REQ-F-015, CRCM-REQ-F-016, CRCM-REQ-F-017, CRCM-REQ-F-018. After: CRCM-C04-T1, CRCM-C04-T2, CRCM-C04-T3, CRCM-C04-T4.
  - Check storage, logs, screens and audit against the rules.
