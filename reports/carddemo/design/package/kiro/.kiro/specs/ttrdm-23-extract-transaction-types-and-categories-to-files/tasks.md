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
  - TTRDM-BR-163: The first step of the scheduled extract job copies the current transaction type file to a new backup version, under the retention policy set up for these backups, before any new file is produced.
  - TTRDM-BR-164: This step runs only if every earlier step of the job succeeded. It copies the current transaction category file to a new backup version. The job needs step-level success tracking so this step can be skipped.
  - TTRDM-BR-167: This is a sorted extract of the transaction type table in a fixed-width layout. Each record is the 2-character type code, the description padded to 50 characters, and eight '0' filler characters, 60 characters in total. Downstream readers depend on this exact layout.
  - TTRDM-BR-170: This is a sorted extract of the transaction category table in a fixed-width layout. Each record is the type code, the category code, the category description padded to 50 characters, and four '0' filler characters, 60 characters in total.
  - _Requirements: TTRDM-REQ-F-151, TTRDM-REQ-F-152, TTRDM-REQ-F-155, TTRDM-REQ-F-158_
  - _Rules: TTRDM-BR-163, TTRDM-BR-164, TTRDM-BR-167, TTRDM-BR-170_
  - _After: TTRDM-C23-T1, TTRDM-C23-T2_
- [ ] 4. TTRDM-C23-T4 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-151, TTRDM-REQ-F-152, TTRDM-REQ-F-153, TTRDM-REQ-F-154, TTRDM-REQ-F-155, TTRDM-REQ-F-156, TTRDM-REQ-F-157, TTRDM-REQ-F-158, TTRDM-REQ-F-159_
  - _Criteria: TTRDM-C23-AC-01, TTRDM-C23-AC-02, TTRDM-C23-AC-03, TTRDM-C23-AC-04, TTRDM-C23-AC-05, TTRDM-C23-AC-06, TTRDM-C23-AC-07, TTRDM-C23-AC-08, TTRDM-C23-AC-09, TTRDM-C23-AC-10, TTRDM-C23-AC-11_
  - _After: TTRDM-C23-T1, TTRDM-C23-T2, TTRDM-C23-T3_
