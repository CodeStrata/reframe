# Implementation plan: Record pending authorization summary and detail (CAFM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CAFM-C07-T1 [data] Model the data the capability reads and writes
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
- [ ] 2. CAFM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-077, CAFM-REQ-F-078_
  - _Rules: CAFM-BR-071, CAFM-BR-072, CAFM-BR-073, CAFM-BR-074, CAFM-BR-075, CAFM-BR-079, CAFM-BR-080_
  - _After: CAFM-C07-T1_
- [ ] 3. CAFM-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CAFM-REQ-F-075, CAFM-REQ-F-079_
  - _Rules: CAFM-BR-076, CAFM-BR-077, CAFM-BR-081_
  - _After: CAFM-C07-T1_
- [ ] 4. CAFM-C07-T4 [api] Build the services behind the screens
  - CAFM-BR-072: Save the account's summary as an upsert keyed by account id: update it if one was found, insert it if not. Do the save in the same transaction as the detail insert, so the summary and its details cannot drift apart.
  - CAFM-BR-078: Insert the authorization detail as a child of the account's summary (a foreign key to the account summary). It holds the request fields and the reply's authorization id, response code, reason and approved amount, and is keyed newest first for paging and purge.
  - _Requirements: CAFM-REQ-F-076_
  - _Rules: CAFM-BR-078_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3_
- [ ] 5. CAFM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
  - _Criteria: CAFM-C07-AC-01, CAFM-C07-AC-02, CAFM-C07-AC-03, CAFM-C07-AC-04, CAFM-C07-AC-05, CAFM-C07-AC-06, CAFM-C07-AC-07, CAFM-C07-AC-08, CAFM-C07-AC-09, CAFM-C07-AC-10, CAFM-C07-AC-11, CAFM-C07-AC-12, CAFM-C07-AC-13_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3, CAFM-C07-T4_
- [ ] 6. CAFM-C07-T6 [compliance] Review the handling of audit, card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CAFM-REQ-F-071, CAFM-REQ-F-072, CAFM-REQ-F-073, CAFM-REQ-F-074, CAFM-REQ-F-075, CAFM-REQ-F-076, CAFM-REQ-F-077, CAFM-REQ-F-078, CAFM-REQ-F-079_
  - _After: CAFM-C07-T1, CAFM-C07-T2, CAFM-C07-T3, CAFM-C07-T4_
