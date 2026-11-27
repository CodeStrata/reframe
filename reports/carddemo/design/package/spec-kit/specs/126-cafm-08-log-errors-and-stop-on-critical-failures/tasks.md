# Tasks: Log errors and stop on critical failures (CAFM-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C08-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081.
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
- [ ] CAFM-C08-T2 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081. Rules: CAFM-BR-082, CAFM-BR-083. After: CAFM-C08-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C08-T3 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081. Criteria: CAFM-C08-AC-01, CAFM-C08-AC-02. After: CAFM-C08-T1, CAFM-C08-T2.
  - 2 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C08-T4 [compliance] Review the handling of audit. Requirements: CAFM-REQ-F-080, CAFM-REQ-F-081. After: CAFM-C08-T1, CAFM-C08-T2.
  - Check storage, logs, screens and audit against the rules.
