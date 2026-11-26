# Tasks: Reset the application environment (ADPLM-C18)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C18-T1 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-112, ADPLM-REQ-F-113, ADPLM-REQ-F-114, ADPLM-REQ-F-115. Rules: ADPLM-BR-121, ADPLM-BR-122, ADPLM-BR-123, ADPLM-BR-124.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C18-T2 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-118. Rules: ADPLM-BR-128.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C18-T3 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-116, ADPLM-REQ-F-117, ADPLM-REQ-N-003. Rules: ADPLM-BR-125, ADPLM-BR-126, ADPLM-BR-127. After: ADPLM-C18-T1, ADPLM-C18-T2.
  - ADPLM-BR-125: Reset is an admin operation. It clears the error log, the start-time records and the statistics records, and it rewrites the control record. Only the control record is recreated straight away; the other stores fill again as the application writes to them.
  - ADPLM-BR-126: Replace the control record as a whole in one transaction with the header '**** GENAPP CNTL', the 10-digit low customer number and the 10-digit high customer number, so that no reader sees a partly rewritten record.
  - ADPLM-BR-127: The legacy writes do not wait for space and never check the result. The new reset should check the write of the control record and report a failure to the operator; the fixed lengths of 20, 23 and 24 characters only matter where the old text format is kept.
- [ ] ADPLM-C18-T4 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-112, ADPLM-REQ-F-113, ADPLM-REQ-F-114, ADPLM-REQ-F-115, ADPLM-REQ-F-116, ADPLM-REQ-F-117, ADPLM-REQ-N-003, ADPLM-REQ-F-118. Criteria: ADPLM-C18-AC-01, ADPLM-C18-AC-02, ADPLM-C18-AC-03, ADPLM-C18-AC-04, ADPLM-C18-AC-05, ADPLM-C18-AC-06, ADPLM-C18-AC-07, ADPLM-C18-AC-08, ADPLM-C18-AC-09. After: ADPLM-C18-T1, ADPLM-C18-T2, ADPLM-C18-T3.
  - 9 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C18-T5 [compliance] Review the handling of audit. Requirements: ADPLM-REQ-F-112, ADPLM-REQ-F-113, ADPLM-REQ-F-114, ADPLM-REQ-F-115, ADPLM-REQ-F-116, ADPLM-REQ-F-117, ADPLM-REQ-N-003, ADPLM-REQ-F-118. After: ADPLM-C18-T1, ADPLM-C18-T2, ADPLM-C18-T3.
  - Check storage, logs, screens and audit against the rules.
