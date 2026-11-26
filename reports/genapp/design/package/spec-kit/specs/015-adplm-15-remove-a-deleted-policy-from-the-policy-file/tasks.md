# Tasks: Remove a deleted policy from the policy file (ADPLM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C15-T1 [data] Model the data the capability reads and writes. Requirements: ADPLM-REQ-F-088, ADPLM-REQ-F-089, ADPLM-REQ-F-090, ADPLM-REQ-F-091.
  - Working records it passes or builds: LGCMAREA.
- [ ] ADPLM-C15-T2 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-090, ADPLM-REQ-F-091. Rules: ADPLM-BR-098, ADPLM-BR-099. After: ADPLM-C15-T1.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C15-T3 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-089. Rules: ADPLM-BR-097. After: ADPLM-C15-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C15-T4 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-088. Rules: ADPLM-BR-096. After: ADPLM-C15-T1, ADPLM-C15-T2, ADPLM-C15-T3.
  - ADPLM-BR-096: The policy file is a keyed store. Its 21-character key is the policy type letter (the fourth character of the request identifier), then the 10-digit customer number, then the 10-digit policy number. Deletion is a single delete by that exact key.
- [ ] ADPLM-C15-T5 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-088, ADPLM-REQ-F-089, ADPLM-REQ-F-090, ADPLM-REQ-F-091. Criteria: ADPLM-C15-AC-01, ADPLM-C15-AC-02, ADPLM-C15-AC-03, ADPLM-C15-AC-04, ADPLM-C15-AC-05, ADPLM-C15-AC-06, ADPLM-C15-AC-07, ADPLM-C15-AC-08. After: ADPLM-C15-T1, ADPLM-C15-T2, ADPLM-C15-T3, ADPLM-C15-T4.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C15-T6 [compliance] Review the handling of audit. Requirements: ADPLM-REQ-F-088, ADPLM-REQ-F-089, ADPLM-REQ-F-090, ADPLM-REQ-F-091. After: ADPLM-C15-T1, ADPLM-C15-T2, ADPLM-C15-T3, ADPLM-C15-T4.
  - Check storage, logs, screens and audit against the rules.
