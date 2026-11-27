# Tasks: Set up the transaction master and its timestamp index (DTPR-C11)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C11-T1 [api] Build the scheduled job. Requirements: DTPR-REQ-F-065, DTPR-REQ-F-066. Rules: DTPR-BR-072, DTPR-BR-073.
  - DTPR-BR-072: Provide a setup or seeding job that empties the transaction store (drop and recreate, or truncate) and bulk-loads every record from the initial daily transaction file. It is for environment setup only and must never be part of the regular daily schedule.
  - DTPR-BR-073: Add a secondary, non-unique index on the transaction's processed timestamp, the 26-character value at offset 304 in the legacy record, alongside the primary key on transaction ID. In a relational store this is an ordinary database index kept up to date automatically rather than rebuilt after loading.
- [ ] DTPR-C11-T2 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-065, DTPR-REQ-F-066. Criteria: DTPR-C11-AC-01, DTPR-C11-AC-02. After: DTPR-C11-T1.
  - 2 acceptance criteria, each a test named by its ID.
