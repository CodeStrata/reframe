# Tasks: Route policy inquiries by request type (UP-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C04-T1 [data] Model the data the capability reads and writes. Requirements: UP-REQ-F-014, UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023.
  - Working records it passes or builds: LGCMAREA, LGPOLICY.
- [ ] UP-C04-T2 [business-rules] Implement the business rules. Requirements: UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023. Rules: UP-BR-036, UP-BR-037, UP-BR-038, UP-BR-039, UP-BR-040, UP-BR-041, UP-BR-042, UP-BR-043, UP-BR-044. After: UP-C04-T1.
  - Keep each business rule exactly as specified.
- [ ] UP-C04-T3 [api] Build the scheduled job. Requirements: UP-REQ-F-014. Rules: UP-BR-034, UP-BR-035. After: UP-C04-T1, UP-C04-T2.
  - UP-BR-034: Every policy inquiry reply starts with return code '00'. Only a later failure (not found, reply area too small, database error or unknown request) changes it, so a request that runs cleanly always returns '00'.
  - UP-BR-035: At the start of each policy inquiry, the supplied customer number and policy number become the lookup keys. They are also kept as context for error messages, so any error logged later names the customer and policy the caller asked for.
- [ ] UP-C04-T4 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-014, UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023. Criteria: UP-C04-AC-01, UP-C04-AC-02, UP-C04-AC-03, UP-C04-AC-04, UP-C04-AC-05, UP-C04-AC-06, UP-C04-AC-07, UP-C04-AC-08, UP-C04-AC-09, UP-C04-AC-10, UP-C04-AC-11, UP-C04-AC-12. After: UP-C04-T1, UP-C04-T2, UP-C04-T3.
  - 12 acceptance criteria, each a test named by its ID.
- [ ] UP-C04-T5 [compliance] Review the handling of personal data. Requirements: UP-REQ-F-014, UP-REQ-F-015, UP-REQ-F-016, UP-REQ-F-017, UP-REQ-F-018, UP-REQ-F-019, UP-REQ-F-020, UP-REQ-F-021, UP-REQ-F-022, UP-REQ-F-023. After: UP-C04-T1, UP-C04-T2, UP-C04-T3.
  - Check storage, logs, screens and audit against the rules.
