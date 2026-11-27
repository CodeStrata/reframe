# Implementation plan: Export complete customer profiles for branch migration (CPBM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CPBM-C01-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
  - _Requirements: CPBM-REQ-F-001, CPBM-REQ-F-002, CPBM-REQ-F-003, CPBM-REQ-F-004, CPBM-REQ-F-005, CPBM-REQ-F-006, CPBM-REQ-F-007_
- [ ] 2. CPBM-C01-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CPBM-REQ-F-003, CPBM-REQ-F-006_
  - _Rules: CPBM-BR-003, CPBM-BR-006_
  - _After: CPBM-C01-T1_
- [ ] 3. CPBM-C01-T3 [api] Build the scheduled job
  - CPBM-BR-001: A scheduled batch job that starts from an empty migration file every run (replace, never append), keyed by sequence number with room for a 500-character record, then runs the export with no parameters against the shared customer, account, cross-reference, transaction and card data, writing its messages to the job log.
  - CPBM-BR-002: One run: take the timestamp, open all five sources and the target, then stream each source in its key order — customers, accounts, cross-references, transactions, cards — one after another; a sorted extract per source in key order, never interleaved.
  - CPBM-BR-004: A one-to-one mapping from each source record to an export record tagged with its type code ('C', 'A', 'X', 'T', 'D') and carrying that record's fields; the migration file is a tagged union of the five record layouts.
  - CPBM-BR-005: A single counter starting at 1, incremented for each record written across all types in output order, used as the unique key of the migration file; the last value equals the total written.
  - CPBM-BR-007: Format the run timestamp from the system clock as 'YYYY-MM-DD HH:MM:SS.00', with the fraction fixed at '00' rather than real hundredths.
  - CPBM-BR-008: Capture the timestamp once at run start and reuse that value on every record; do not read the clock per record.
  - _Requirements: CPBM-REQ-F-001, CPBM-REQ-F-002, CPBM-REQ-F-004, CPBM-REQ-F-005, CPBM-REQ-F-007_
  - _Rules: CPBM-BR-001, CPBM-BR-002, CPBM-BR-004, CPBM-BR-005, CPBM-BR-007, CPBM-BR-008_
  - _After: CPBM-C01-T1, CPBM-C01-T2_
- [ ] 4. CPBM-C01-T4 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CPBM-REQ-F-001, CPBM-REQ-F-002, CPBM-REQ-F-003, CPBM-REQ-F-004, CPBM-REQ-F-005, CPBM-REQ-F-006, CPBM-REQ-F-007_
  - _Criteria: CPBM-C01-AC-01, CPBM-C01-AC-02, CPBM-C01-AC-03, CPBM-C01-AC-04, CPBM-C01-AC-05, CPBM-C01-AC-06, CPBM-C01-AC-07, CPBM-C01-AC-08, CPBM-C01-AC-09, CPBM-C01-AC-10_
  - _After: CPBM-C01-T1, CPBM-C01-T2, CPBM-C01-T3_
- [ ] 5. CPBM-C01-T5 [compliance] Review the handling of card data, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CPBM-REQ-F-001, CPBM-REQ-F-002, CPBM-REQ-F-003, CPBM-REQ-F-004, CPBM-REQ-F-005, CPBM-REQ-F-006, CPBM-REQ-F-007_
  - _After: CPBM-C01-T1, CPBM-C01-T2, CPBM-C01-T3_
