# Tasks: Unload all pending authorizations (CAFM-C20)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C20-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-170, CAFM-REQ-F-171, CAFM-REQ-F-172, CAFM-REQ-F-173, CAFM-REQ-F-174, CAFM-REQ-F-175, CAFM-REQ-F-176, CAFM-REQ-F-177, CAFM-REQ-F-178, CAFM-REQ-F-179.
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PAUTBPCB.
- [ ] CAFM-C20-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-170, CAFM-REQ-F-172, CAFM-REQ-F-174. Rules: CAFM-BR-184, CAFM-BR-186, CAFM-BR-188. After: CAFM-C20-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C20-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-176, CAFM-REQ-F-179. Rules: CAFM-BR-190, CAFM-BR-193. After: CAFM-C20-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C20-T4 [api] Build the scheduled job. Requirements: CAFM-REQ-F-171, CAFM-REQ-F-173, CAFM-REQ-F-175, CAFM-REQ-F-177, CAFM-REQ-F-178. Rules: CAFM-BR-185, CAFM-BR-187, CAFM-BR-189, CAFM-BR-191, CAFM-BR-192. After: CAFM-C20-T1, CAFM-C20-T2, CAFM-C20-T3.
  - CAFM-BR-185: The job walks all summaries one by one in a stable order (by account id), finishing each summary and its details before moving to the next; stream the results rather than loading them all into memory.
  - CAFM-BR-187: The summary file holds one fixed 100-byte record per summary, the summary exactly as stored. The new application needs a defined summary export layout of the same fields, byte-compatible with the legacy layout for as long as anything still reads these files.
  - CAFM-BR-189: When there are no more summaries, the job closes both output files and ends normally (return code 0); reaching the end of the data is not an error.
  - CAFM-BR-191: The detail file holds one fixed 206-byte record per detail: the parent account id (6 bytes, packed decimal in the legacy layout) followed by the 200-byte detail as stored. The account id prefix is what lets a reload attach each detail to its summary, so the new export must always carry it; keep packed decimal only while legacy consumers need it.
  - CAFM-BR-192: Running out of details for a summary is a normal step: log 'CHILD SEG FLAG GE : ' with the end flag and continue with the next summary.
- [ ] CAFM-C20-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-170, CAFM-REQ-F-171, CAFM-REQ-F-172, CAFM-REQ-F-173, CAFM-REQ-F-174, CAFM-REQ-F-175, CAFM-REQ-F-176, CAFM-REQ-F-177, CAFM-REQ-F-178, CAFM-REQ-F-179. Criteria: CAFM-C20-AC-01, CAFM-C20-AC-02, CAFM-C20-AC-03, CAFM-C20-AC-04, CAFM-C20-AC-05, CAFM-C20-AC-06, CAFM-C20-AC-07, CAFM-C20-AC-08, CAFM-C20-AC-09, CAFM-C20-AC-10. After: CAFM-C20-T1, CAFM-C20-T2, CAFM-C20-T3, CAFM-C20-T4.
  - 10 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C20-T6 [compliance] Review the handling of card data. Requirements: CAFM-REQ-F-170, CAFM-REQ-F-171, CAFM-REQ-F-172, CAFM-REQ-F-173, CAFM-REQ-F-174, CAFM-REQ-F-175, CAFM-REQ-F-176, CAFM-REQ-F-177, CAFM-REQ-F-178, CAFM-REQ-F-179. After: CAFM-C20-T1, CAFM-C20-T2, CAFM-C20-T3, CAFM-C20-T4.
  - Check storage, logs, screens and audit against the rules.
