# Tasks: Read transactions by processed timestamp (UP-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C11-T1 [api] Build the scheduled job. Requirements: UP-REQ-F-048, UP-REQ-F-049. Rules: UP-BR-051, UP-BR-052.
  - UP-BR-051: A non-unique secondary index on the transaction table's processed-timestamp column, covering every existing row. In a relational database this is a CREATE INDEX, which the database keeps up to date, not a separate rebuild job.
  - UP-BR-052: Expose a query or repository method that reads transactions by processed timestamp (exact match or range, in timestamp order) using that non-unique index. It must allow many transactions per timestamp.
- [ ] UP-C11-T2 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-048, UP-REQ-F-049. Criteria: UP-C11-AC-01, UP-C11-AC-02. After: UP-C11-T1.
  - 2 acceptance criteria, each a test named by its ID.
