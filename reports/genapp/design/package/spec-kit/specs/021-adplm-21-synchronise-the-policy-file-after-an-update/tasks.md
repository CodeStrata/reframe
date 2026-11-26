# Tasks: Synchronise the policy file after an update (ADPLM-C21)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] ADPLM-C21-T1 [data] Model the data the capability reads and writes. Requirements: ADPLM-REQ-F-144, ADPLM-REQ-F-145, ADPLM-REQ-F-146, ADPLM-REQ-F-147, ADPLM-REQ-F-148, ADPLM-REQ-F-149, ADPLM-REQ-F-150, ADPLM-REQ-F-151, ADPLM-REQ-F-152, ADPLM-REQ-F-153, ADPLM-REQ-F-154.
  - Working records it passes or builds: LGCMAREA.
- [ ] ADPLM-C21-T2 [business-rules] Implement the business rules. Requirements: ADPLM-REQ-F-146, ADPLM-REQ-F-147, ADPLM-REQ-F-148, ADPLM-REQ-F-149, ADPLM-REQ-F-150, ADPLM-REQ-F-151, ADPLM-REQ-F-154. Rules: ADPLM-BR-163, ADPLM-BR-164, ADPLM-BR-165, ADPLM-BR-166, ADPLM-BR-167, ADPLM-BR-168, ADPLM-BR-171. After: ADPLM-C21-T1.
  - Keep each business rule exactly as specified.
- [ ] ADPLM-C21-T3 [business-rules] Implement error handling and messages. Requirements: ADPLM-REQ-F-152, ADPLM-REQ-F-153. Rules: ADPLM-BR-169, ADPLM-BR-170. After: ADPLM-C21-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] ADPLM-C21-T4 [api] Build the scheduled job. Requirements: ADPLM-REQ-F-144, ADPLM-REQ-F-145. Rules: ADPLM-BR-160, ADPLM-BR-161, ADPLM-BR-162. After: ADPLM-C21-T1, ADPLM-C21-T2, ADPLM-C21-T3.
  - ADPLM-BR-160: Build the policy-file key from the policy type letter (the fourth character of the request ID), the customer number and the policy number. Use typed fields for the request instead of a length the caller passes in.
  - ADPLM-BR-161: Same key as the delete and lookup paths: the type letter, then the 10-digit customer number, then the 10-digit policy number. Put the key build in one shared function so that all policy-file operations agree.
  - ADPLM-BR-162: Do a keyed read with a row lock (select for update) on the policy-file record, then a full replace of that record in the same transaction.
- [ ] ADPLM-C21-T5 [test-generation] Write a test for every acceptance criterion. Requirements: ADPLM-REQ-F-144, ADPLM-REQ-F-145, ADPLM-REQ-F-146, ADPLM-REQ-F-147, ADPLM-REQ-F-148, ADPLM-REQ-F-149, ADPLM-REQ-F-150, ADPLM-REQ-F-151, ADPLM-REQ-F-152, ADPLM-REQ-F-153, ADPLM-REQ-F-154. Criteria: ADPLM-C21-AC-01, ADPLM-C21-AC-02, ADPLM-C21-AC-03, ADPLM-C21-AC-04, ADPLM-C21-AC-05, ADPLM-C21-AC-06, ADPLM-C21-AC-07, ADPLM-C21-AC-08, ADPLM-C21-AC-09, ADPLM-C21-AC-10, ADPLM-C21-AC-11, ADPLM-C21-AC-12. After: ADPLM-C21-T1, ADPLM-C21-T2, ADPLM-C21-T3, ADPLM-C21-T4.
  - 12 acceptance criteria, each a test named by its ID.
- [ ] ADPLM-C21-T6 [compliance] Review the handling of audit, money, personal data. Requirements: ADPLM-REQ-F-144, ADPLM-REQ-F-145, ADPLM-REQ-F-146, ADPLM-REQ-F-147, ADPLM-REQ-F-148, ADPLM-REQ-F-149, ADPLM-REQ-F-150, ADPLM-REQ-F-151, ADPLM-REQ-F-152, ADPLM-REQ-F-153, ADPLM-REQ-F-154. After: ADPLM-C21-T1, ADPLM-C21-T2, ADPLM-C21-T3, ADPLM-C21-T4.
  - Check storage, logs, screens and audit against the rules.
