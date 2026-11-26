# Tasks: Accept a customer update request (CRCM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CRCM-C05-T1 [data] Model the data the capability reads and writes. Requirements: CRCM-REQ-F-019, CRCM-REQ-F-020, CRCM-REQ-F-021.
  - Working records it passes or builds: LGCMAREA.
- [ ] CRCM-C05-T2 [business-rules] Implement the business rules. Requirements: CRCM-REQ-F-020, CRCM-REQ-F-021, CRCM-REQ-F-019. Rules: CRCM-BR-026, CRCM-BR-027, CRCM-BR-028, CRCM-BR-029. After: CRCM-C05-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CRCM-BR-026, CRCM-BR-027.
- [ ] CRCM-C05-T3 [api] Build the scheduled job. Requirements: CRCM-REQ-F-019, CRCM-REQ-F-020, CRCM-REQ-F-021. Rules: CRCM-BR-026, CRCM-BR-027, CRCM-BR-028, CRCM-BR-029. After: CRCM-C05-T1, CRCM-C05-T2.
  - CRCM-BR-026: Default the update response outcome to '00' (success) before the request type is checked. The type check (failure '99') and the downstream update service overwrite it only when they fail.
- [ ] CRCM-C05-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CRCM-REQ-F-019, CRCM-REQ-F-020, CRCM-REQ-F-021. Criteria: CRCM-C05-AC-01, CRCM-C05-AC-02, CRCM-C05-AC-03, CRCM-C05-AC-04. After: CRCM-C05-T1, CRCM-C05-T2, CRCM-C05-T3.
  - 4 acceptance criteria, each a test named by its ID.
- [ ] CRCM-C05-T5 [compliance] Review the handling of personal data. Requirements: CRCM-REQ-F-019, CRCM-REQ-F-020, CRCM-REQ-F-021. After: CRCM-C05-T1, CRCM-C05-T2, CRCM-C05-T3.
  - Check storage, logs, screens and audit against the rules.
