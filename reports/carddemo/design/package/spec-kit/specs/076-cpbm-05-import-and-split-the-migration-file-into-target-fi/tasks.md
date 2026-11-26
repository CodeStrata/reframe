# Tasks: Import and split the migration file into target files (CPBM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CPBM-C05-T1 [data] Model the data the capability reads and writes. Requirements: CPBM-REQ-F-013, CPBM-REQ-F-014, CPBM-REQ-F-015, CPBM-REQ-F-016, CPBM-REQ-F-017, CPBM-REQ-F-018, CPBM-REQ-F-019, CPBM-REQ-F-020, CPBM-REQ-F-021.
  - File records: CVACT01Y, CVACT02Y, CVACT03Y, CVCUS01Y, CVEXPORT, CVTRA05Y (see data-contracts.md).
- [ ] CPBM-C05-T2 [business-rules] Implement the business rules. Requirements: CPBM-REQ-F-015, CPBM-REQ-F-016, CPBM-REQ-F-020, CPBM-REQ-F-021. Rules: CPBM-BR-019, CPBM-BR-020, CPBM-BR-024, CPBM-BR-025. After: CPBM-C05-T1.
  - Keep each business rule exactly as specified.
- [ ] CPBM-C05-T3 [api] Build the scheduled job. Requirements: CPBM-REQ-F-013, CPBM-REQ-F-014, CPBM-REQ-F-017, CPBM-REQ-F-018, CPBM-REQ-F-019. Rules: CPBM-BR-017, CPBM-BR-018, CPBM-BR-021, CPBM-BR-022, CPBM-BR-023. After: CPBM-C05-T1, CPBM-C05-T2.
  - CPBM-BR-017: A scheduled import job that reads the shared migration file and creates fresh customer (500-character), account (300), cross-reference (50) and transaction (350) target files plus a 132-character error report; the outputs are kept only if the step succeeds and are removed if it fails.
  - CPBM-BR-018: The legacy job sets up no card target although the program writes card records to one; the new job must provide a card target explicitly (a known gap to confirm, not behaviour to copy).
  - CPBM-BR-021: Map an 'A' record field for field to an account record (number, active status, current balance, credit limit, cash credit limit, open/expiration/reissue dates, current-cycle credit and debit, zip, group id) and write it to the account target; any write failure stops the run.
  - CPBM-BR-022: Map an 'X' record to a cross-reference row linking card number, customer number and account number, and write it to the cross-reference target; any write failure stops the run.
  - CPBM-BR-023: Map a 'T' record field for field to a transaction record and write it to the transaction target; any write failure stops the run.
- [ ] CPBM-C05-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CPBM-REQ-F-013, CPBM-REQ-F-014, CPBM-REQ-F-015, CPBM-REQ-F-016, CPBM-REQ-F-017, CPBM-REQ-F-018, CPBM-REQ-F-019, CPBM-REQ-F-020, CPBM-REQ-F-021. Criteria: CPBM-C05-AC-01, CPBM-C05-AC-02, CPBM-C05-AC-03, CPBM-C05-AC-04, CPBM-C05-AC-05, CPBM-C05-AC-06, CPBM-C05-AC-07, CPBM-C05-AC-08, CPBM-C05-AC-09, CPBM-C05-AC-10, CPBM-C05-AC-11, CPBM-C05-AC-12, CPBM-C05-AC-13. After: CPBM-C05-T1, CPBM-C05-T2, CPBM-C05-T3.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] CPBM-C05-T5 [compliance] Review the handling of card data, money, personal data. Requirements: CPBM-REQ-F-013, CPBM-REQ-F-014, CPBM-REQ-F-015, CPBM-REQ-F-016, CPBM-REQ-F-017, CPBM-REQ-F-018, CPBM-REQ-F-019, CPBM-REQ-F-020, CPBM-REQ-F-021. After: CPBM-C05-T1, CPBM-C05-T2, CPBM-C05-T3.
  - Check storage, logs, screens and audit against the rules.
