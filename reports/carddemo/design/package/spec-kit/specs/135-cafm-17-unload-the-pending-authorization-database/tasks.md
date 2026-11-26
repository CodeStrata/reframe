# Tasks: Unload the pending authorization database (CAFM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C17-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155.
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PADFLPCB, PASFLPCB, PAUTBPCB.
- [ ] CAFM-C17-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-149. Rules: CAFM-BR-164. After: CAFM-C17-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C17-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155. Rules: CAFM-BR-168, CAFM-BR-169, CAFM-BR-170, CAFM-BR-171. After: CAFM-C17-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C17-T4 [api] Build the scheduled job. Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152. Rules: CAFM-BR-162, CAFM-BR-163, CAFM-BR-165, CAFM-BR-166, CAFM-BR-167. After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3.
  - CAFM-BR-162: Needs a scheduled full-database export of pending authorizations that reads the live data without locking out online users, writes a new variable-length extract (records up to 27990 bytes) under a fixed name, and removes the extract if the job fails so no partial file is left registered as complete.
  - CAFM-BR-163: The export walks all account summaries in storage order and, for each with a numeric account id, writes the summary and then all its details, so every detail follows its parent summary in the output. In a relational model this is an ordered scan of summaries joined to their details.
  - CAFM-BR-165: Reaching the end of the summaries is the normal finish of the export, not an error; the job completes successfully.
  - CAFM-BR-166: For each exported summary, every detail belonging to that account is read in turn and each successfully read detail is written to the detail export file.
  - CAFM-BR-167: Running out of details for a summary is normal: log 'CHILD SEG FLAG GE : Y', reset the per-summary state and move on to the next summary. It must not be treated as an error or stop the job.
- [ ] CAFM-C17-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155. Criteria: CAFM-C17-AC-01, CAFM-C17-AC-02, CAFM-C17-AC-03, CAFM-C17-AC-04, CAFM-C17-AC-05, CAFM-C17-AC-06, CAFM-C17-AC-07, CAFM-C17-AC-08, CAFM-C17-AC-09, CAFM-C17-AC-10. After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3, CAFM-C17-T4.
  - 10 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C17-T6 [compliance] Review the handling of card data. Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155. After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3, CAFM-C17-T4.
  - Check storage, logs, screens and audit against the rules.
