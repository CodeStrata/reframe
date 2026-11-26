# Tasks: Count transactions by request type and outcome (ADPLM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C13-T1 [data] Model the data the capability reads and writes. Requirements: ADPLM-REQ-F-072, ADPLM-REQ-F-073, ADPLM-REQ-F-074, ADPLM-REQ-F-075, ADPLM-REQ-F-076, ADPLM-REQ-F-077, ADPLM-REQ-N-001.
  - Working records it passes or builds: LGCMAREA.
- [ ] ADPLM-C13-T2 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-075, ADPLM-REQ-F-076, ADPLM-REQ-F-077, ADPLM-REQ-N-001. Rules: ADPLM-BR-079, ADPLM-BR-080, ADPLM-BR-081, ADPLM-BR-082. After: ADPLM-C13-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: ADPLM-BR-082.
- [ ] ADPLM-C13-T3 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-074. Rules: ADPLM-BR-078. After: ADPLM-C13-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C13-T4 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-072, ADPLM-REQ-F-073. Rules: ADPLM-BR-076, ADPLM-BR-077. After: ADPLM-C13-T1, ADPLM-C13-T2, ADPLM-C13-T3.
  - ADPLM-BR-076: The counter needs a transaction-completed event that carries the request type and the return code as separate fields. Publish it from every request handler when the handler finishes, and have the statistics consumer read these fields first.
  - ADPLM-BR-077: Fallback input: if the event fields are missing, the consumer takes the request type and return code from the request payload that came with the event. Handle both shapes through one input contract instead of two code paths.
- [ ] ADPLM-C13-T5 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-072, ADPLM-REQ-F-073, ADPLM-REQ-F-074, ADPLM-REQ-F-075, ADPLM-REQ-F-076, ADPLM-REQ-F-077, ADPLM-REQ-N-001. Criteria: ADPLM-C13-AC-01, ADPLM-C13-AC-02, ADPLM-C13-AC-03, ADPLM-C13-AC-04, ADPLM-C13-AC-05, ADPLM-C13-AC-06, ADPLM-C13-AC-07. After: ADPLM-C13-T1, ADPLM-C13-T2, ADPLM-C13-T3, ADPLM-C13-T4.
  - 7 acceptance criteria, each a test named by its ID.
