# Tasks: Log policy add errors (ADPLM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C09-T1 [data] Model the data the capability reads and writes. Requirements: ADPLM-REQ-F-055.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] ADPLM-C09-T2 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-055. Rules: ADPLM-BR-060. After: ADPLM-C09-T1.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C09-T3 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-055. Rules: ADPLM-BR-060. After: ADPLM-C09-T1, ADPLM-C09-T2.
  - Expose the rules as the service the screens call.
- [ ] ADPLM-C09-T4 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-055. Criteria: ADPLM-C09-AC-01, ADPLM-C09-AC-02. After: ADPLM-C09-T1, ADPLM-C09-T2, ADPLM-C09-T3.
  - 2 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C09-T5 [compliance] Review the handling of audit, personal data. Requirements: ADPLM-REQ-F-055. After: ADPLM-C09-T1, ADPLM-C09-T2, ADPLM-C09-T3.
  - Check storage, logs, screens and audit against the rules.
