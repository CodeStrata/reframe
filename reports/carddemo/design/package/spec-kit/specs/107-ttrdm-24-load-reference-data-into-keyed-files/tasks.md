# Tasks: Load reference data into keyed files (TTRDM-C24)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C24-T1 [api] Build the scheduled job. Requirements: TTRDM-REQ-F-160, TTRDM-REQ-F-161. Rules: TTRDM-BR-172, TTRDM-BR-173.
  - TTRDM-BR-172: A full-refresh load of the transaction category lookup store (a table or cache keyed by type code plus category code, the first 6 characters of each 60-character record). Truncate or recreate it, then load every record from the category extract, which is read without locking it. Hold the store exclusively, or swap it in atomically, so readers never see a half-loaded store.
  - TTRDM-BR-173: A full-refresh load of the transaction type lookup store, keyed by the 2-character type code at the start of each 60-character record. Truncate or recreate it, then load every record from the transaction type extract, which is read without locking it. Hold the store exclusively, or swap it in atomically, so readers never see a half-loaded store.
- [ ] TTRDM-C24-T2 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-160, TTRDM-REQ-F-161. Criteria: TTRDM-C24-AC-01, TTRDM-C24-AC-02, TTRDM-C24-AC-03. After: TTRDM-C24-T1.
  - 3 acceptance criteria, each a test named by its ID.
