# Tasks: Load account master (MDFI-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] MDFI-C01-T1 [api] Build the scheduled job. Requirements: MDFI-REQ-F-001, MDFI-REQ-F-002. Rules: MDFI-BR-001, MDFI-BR-002.
  - MDFI-BR-001: The scheduled load job starts by clearing out the account store (drop and recreate, or truncate the accounts table). It must succeed whether or not the store already exists. The rebuilt store has the 11-digit account ID as its unique primary key, so later processing can look up an account by its ID.
  - MDFI-BR-002: A bulk import that reads every record of the account extract file into the freshly emptied account store, keyed by account ID. The job should check that the number of rows loaded equals the number of input records, and it should fail visibly rather than load only part of the file.
- [ ] MDFI-C01-T2 [test-generation] Write a test for every acceptance criterion. Requirements: MDFI-REQ-F-001, MDFI-REQ-F-002. Criteria: MDFI-C01-AC-01, MDFI-C01-AC-02. After: MDFI-C01-T1.
  - 2 acceptance criteria, each a test named by its ID.
