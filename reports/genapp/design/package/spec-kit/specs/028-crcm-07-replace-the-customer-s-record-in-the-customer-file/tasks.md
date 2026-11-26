# Tasks: Replace the customer's record in the customer file (CRCM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CRCM-C07-T1 [data] Model the data the capability reads and writes. Requirements: CRCM-REQ-F-027, CRCM-REQ-F-028, CRCM-REQ-F-029.
  - File records: LGCMAREA (see data-contracts.md).
- [ ] CRCM-C07-T2 [business-rules] Implement the business rules. Requirements: CRCM-REQ-F-027. Rules: CRCM-BR-035. After: CRCM-C07-T1.
  - Keep each business rule exactly as specified.
- [ ] CRCM-C07-T3 [business-rules] Implement error handling and messages. Requirements: CRCM-REQ-F-028, CRCM-REQ-F-029. Rules: CRCM-BR-036, CRCM-BR-037. After: CRCM-C07-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CRCM-C07-T4 [api] Build the service. Requirements: CRCM-REQ-F-027, CRCM-REQ-F-028, CRCM-REQ-F-029. Rules: CRCM-BR-035, CRCM-BR-036, CRCM-BR-037. After: CRCM-C07-T1, CRCM-C07-T2, CRCM-C07-T3.
  - Expose the rules as the service the screens call.
- [ ] CRCM-C07-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CRCM-REQ-F-027, CRCM-REQ-F-028, CRCM-REQ-F-029. Criteria: CRCM-C07-AC-01, CRCM-C07-AC-02, CRCM-C07-AC-03. After: CRCM-C07-T1, CRCM-C07-T2, CRCM-C07-T3, CRCM-C07-T4.
  - 3 acceptance criteria, each a test named by its ID.
- [ ] CRCM-C07-T6 [compliance] Review the handling of audit, personal data. Requirements: CRCM-REQ-F-027, CRCM-REQ-F-028, CRCM-REQ-F-029. After: CRCM-C07-T1, CRCM-C07-T2, CRCM-C07-T3, CRCM-C07-T4.
  - Check storage, logs, screens and audit against the rules.
