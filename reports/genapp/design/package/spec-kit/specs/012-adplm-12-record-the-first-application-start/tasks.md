# Tasks: Record the first application start (ADPLM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C12-T1 [data] Model the data the capability reads and writes. Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071.
  - Working records it passes or builds: LGCMAREA.
- [ ] ADPLM-C12-T2 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071. Rules: ADPLM-BR-075. After: ADPLM-C12-T1.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C12-T3 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071. Rules: ADPLM-BR-075. After: ADPLM-C12-T1, ADPLM-C12-T2.
  - Expose the rules as the service the screens call.
- [ ] ADPLM-C12-T4 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071. Criteria: ADPLM-C12-AC-01, ADPLM-C12-AC-02. After: ADPLM-C12-T1, ADPLM-C12-T2, ADPLM-C12-T3.
  - 2 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C12-T5 [compliance] Review the handling of audit. Requirements: ADPLM-REQ-F-070, ADPLM-REQ-F-071. After: ADPLM-C12-T1, ADPLM-C12-T2, ADPLM-C12-T3.
  - Check storage, logs, screens and audit against the rules.
