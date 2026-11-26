# Implementation plan: Unload the pending authorization database (CAFM-C17)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C17-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: CIPAUDTY, CIPAUSMY, IMSFUNCS, PADFLPCB, PASFLPCB, PAUTBPCB.
  - _Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155_
- [ ] 2. CAFM-C17-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-149_
  - _Rules: CAFM-BR-164_
  - _After: CAFM-C17-T1_
- [ ] 3. CAFM-C17-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155_
  - _Rules: CAFM-BR-168, CAFM-BR-169, CAFM-BR-170, CAFM-BR-171_
  - _After: CAFM-C17-T1_
- [ ] 4. CAFM-C17-T4 [api] Build the scheduled job
  - CAFM-BR-162: A scheduled full extract of the pending authorization store into a single new file of variable-length records (up to 27990 bytes), read without locking out online users. The file must only be published when the job succeeds: write to a temporary name and rename on success, or delete it on failure, so a failed run never leaves a usable-looking extract.
  - CAFM-BR-163: The extract walks all summaries in a stable order (by account id) and, for each one with a numeric account id, writes the summary and then all its details before moving to the next summary. With a relational store this is a query of summaries ordered by account id joined to their details, streamed out so memory use does not grow with volume.
  - CAFM-BR-165: The job ends normally when there are no more summaries to read; reaching the end of the data is a normal finish, not an error.
  - CAFM-BR-166: For each summary, every one of its details is written to the separate detail file, in the order they are held under that summary (newest first in the legacy store), so a reload can attach each detail to its summary.
  - CAFM-BR-167: Running out of details for a summary is a normal step, not an error: log 'CHILD SEG FLAG GE : Y', reset the per-summary state and continue with the next summary.
  - _Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152_
  - _Rules: CAFM-BR-162, CAFM-BR-163, CAFM-BR-165, CAFM-BR-166, CAFM-BR-167_
  - _After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3_
- [ ] 5. CAFM-C17-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155_
  - _Criteria: CAFM-C17-AC-01, CAFM-C17-AC-02, CAFM-C17-AC-03, CAFM-C17-AC-04, CAFM-C17-AC-05, CAFM-C17-AC-06, CAFM-C17-AC-07, CAFM-C17-AC-08, CAFM-C17-AC-09, CAFM-C17-AC-10_
  - _After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3, CAFM-C17-T4_
- [ ] 6. CAFM-C17-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-147, CAFM-REQ-F-148, CAFM-REQ-F-149, CAFM-REQ-F-150, CAFM-REQ-F-151, CAFM-REQ-F-152, CAFM-REQ-F-153, CAFM-REQ-F-154, CAFM-REQ-F-155_
  - _After: CAFM-C17-T1, CAFM-C17-T2, CAFM-C17-T3, CAFM-C17-T4_
