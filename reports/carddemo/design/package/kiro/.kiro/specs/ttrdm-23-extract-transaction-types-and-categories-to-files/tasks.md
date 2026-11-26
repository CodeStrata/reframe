# Implementation plan: Extract transaction types and categories to files (TTRDM-C23)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C23-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-154, TTRDM-REQ-F-157_
  - _Rules: TTRDM-BR-166, TTRDM-BR-169_
- [ ] 2. TTRDM-C23-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-153, TTRDM-REQ-F-156, TTRDM-REQ-F-159_
  - _Rules: TTRDM-BR-165, TTRDM-BR-168, TTRDM-BR-171_
- [ ] 3. TTRDM-C23-T3 [api] Build the scheduled job
  - TTRDM-BR-163: The extract job's first step copies the current transaction type extract, unchanged and in its 60-character records, into a new version in the versioned transaction type backup location before anything is overwritten.
  - TTRDM-BR-164: A conditional job step that runs only when every earlier step succeeded. It copies the current transaction category extract, unchanged and in its 60-character records, into a new version in the category backup location. The orchestrator must skip it after any earlier failure.
  - TTRDM-BR-167: A fixed-width writer for the sorted transaction type extract (ordered by type code). Each record has the 2-character type code, the description right-padded with spaces to 50 characters, then the literal '00000000', 60 characters in all. Downstream consumers depend on this exact layout.
  - TTRDM-BR-170: A fixed-width writer for the sorted transaction category extract (ordered by type code, then category code). Each record has the type code, the category code, the category description right-padded with spaces to 50 characters, then the literal '0000', 60 characters in all.
  - _Requirements: TTRDM-REQ-F-151, TTRDM-REQ-F-152, TTRDM-REQ-F-155, TTRDM-REQ-F-158_
  - _Rules: TTRDM-BR-163, TTRDM-BR-164, TTRDM-BR-167, TTRDM-BR-170_
  - _After: TTRDM-C23-T1, TTRDM-C23-T2_
- [ ] 4. TTRDM-C23-T4 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-151, TTRDM-REQ-F-152, TTRDM-REQ-F-153, TTRDM-REQ-F-154, TTRDM-REQ-F-155, TTRDM-REQ-F-156, TTRDM-REQ-F-157, TTRDM-REQ-F-158, TTRDM-REQ-F-159_
  - _Criteria: TTRDM-C23-AC-01, TTRDM-C23-AC-02, TTRDM-C23-AC-03, TTRDM-C23-AC-04, TTRDM-C23-AC-05, TTRDM-C23-AC-06, TTRDM-C23-AC-07, TTRDM-C23-AC-08, TTRDM-C23-AC-09, TTRDM-C23-AC-10, TTRDM-C23-AC-11_
  - _After: TTRDM-C23-T1, TTRDM-C23-T2, TTRDM-C23-T3_
