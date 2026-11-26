# Tasks: Load disclosure group and category balance masters (DTPR-C12)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C12-T1 [api] Build the scheduled job. Requirements: DTPR-REQ-F-067, DTPR-REQ-N-006, DTPR-REQ-F-068, DTPR-REQ-F-069. Rules: DTPR-BR-074, DTPR-BR-075, DTPR-BR-076.
  - DTPR-BR-074: Make the disclosure group load a full replace: clear or recreate the store, keyed on the 16-character key of group ID, type and category over 50-byte records, before loading. Treat an absent previous store as normal, not an error.
  - DTPR-BR-075: Bulk-load every record of the disclosure group feed into the keyed disclosure group store. Load it as one unit (in a single transaction, or by swapping in a staging table) so the interest job never sees a partly loaded rate table.
  - DTPR-BR-076: Bulk-load every category balance record from the flat feed into the category balance store, keyed on account ID, type and category. Hold exclusive write access during the load, and schedule it so it never overlaps the posting or interest jobs.
- [ ] DTPR-C12-T2 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-067, DTPR-REQ-N-006, DTPR-REQ-F-068, DTPR-REQ-F-069. Criteria: DTPR-C12-AC-01, DTPR-C12-AC-02, DTPR-C12-AC-03, DTPR-C12-AC-04, DTPR-C12-AC-05. After: DTPR-C12-T1.
  - 5 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C12-T3 [compliance] Review the handling of money. Requirements: DTPR-REQ-F-067, DTPR-REQ-N-006, DTPR-REQ-F-068, DTPR-REQ-F-069. After: DTPR-C12-T1.
  - Check storage, logs, screens and audit against the rules.
