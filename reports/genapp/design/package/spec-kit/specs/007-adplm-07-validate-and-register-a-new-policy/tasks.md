# Tasks: Validate and register a new policy (ADPLM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C07-T1 [data] Model the data the capability reads and writes. Requirements: ADPLM-REQ-F-037, ADPLM-REQ-F-038, ADPLM-REQ-F-039, ADPLM-REQ-F-040, ADPLM-REQ-F-041, ADPLM-REQ-F-042, ADPLM-REQ-F-043, ADPLM-REQ-F-044, ADPLM-REQ-F-045, ADPLM-REQ-F-046.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] ADPLM-C07-T2 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-038, ADPLM-REQ-F-039, ADPLM-REQ-F-040, ADPLM-REQ-F-041, ADPLM-REQ-F-042, ADPLM-REQ-F-043, ADPLM-REQ-F-044, ADPLM-REQ-F-046. Rules: ADPLM-BR-039, ADPLM-BR-040, ADPLM-BR-041, ADPLM-BR-042, ADPLM-BR-043, ADPLM-BR-044, ADPLM-BR-045, ADPLM-BR-046, ADPLM-BR-047, ADPLM-BR-048, ADPLM-BR-051. After: ADPLM-C07-T1.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C07-T3 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-045. Rules: ADPLM-BR-049, ADPLM-BR-050. After: ADPLM-C07-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C07-T4 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-037. Rules: ADPLM-BR-038. After: ADPLM-C07-T1, ADPLM-C07-T2, ADPLM-C07-T3.
  - ADPLM-BR-038: Each request has a context object whose result code starts at '00' (success). It carries the request's customer number, which is used both for the policy insert and in any error log entry.
  - ADPLM-BR-051: Once the database registration finishes without stopping early, pass the full request, including the assigned policy number, to the policy-file writer (LGAPVS01, capability 11) as the next step. A direct service call is enough. The full request is 32,500 bytes in the legacy system, but the new interface needs only the populated request fields.
- [ ] ADPLM-C07-T5 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-037, ADPLM-REQ-F-038, ADPLM-REQ-F-039, ADPLM-REQ-F-040, ADPLM-REQ-F-041, ADPLM-REQ-F-042, ADPLM-REQ-F-043, ADPLM-REQ-F-044, ADPLM-REQ-F-045, ADPLM-REQ-F-046. Criteria: ADPLM-C07-AC-01, ADPLM-C07-AC-02, ADPLM-C07-AC-03, ADPLM-C07-AC-04, ADPLM-C07-AC-05, ADPLM-C07-AC-06, ADPLM-C07-AC-07, ADPLM-C07-AC-08, ADPLM-C07-AC-09, ADPLM-C07-AC-10, ADPLM-C07-AC-11, ADPLM-C07-AC-12, ADPLM-C07-AC-13, ADPLM-C07-AC-14, ADPLM-C07-AC-15, ADPLM-C07-AC-16, ADPLM-C07-AC-17, ADPLM-C07-AC-18, ADPLM-C07-AC-19, ADPLM-C07-AC-20, ADPLM-C07-AC-21. After: ADPLM-C07-T1, ADPLM-C07-T2, ADPLM-C07-T3, ADPLM-C07-T4.
  - 21 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C07-T6 [compliance] Review the handling of audit, money, personal data. Requirements: ADPLM-REQ-F-037, ADPLM-REQ-F-038, ADPLM-REQ-F-039, ADPLM-REQ-F-040, ADPLM-REQ-F-041, ADPLM-REQ-F-042, ADPLM-REQ-F-043, ADPLM-REQ-F-044, ADPLM-REQ-F-045, ADPLM-REQ-F-046. After: ADPLM-C07-T1, ADPLM-C07-T2, ADPLM-C07-T3, ADPLM-C07-T4.
  - Check storage, logs, screens and audit against the rules.
