# Implementation plan: Read transactions by processed timestamp (UP-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. UP-C11-T1 [api] Build the scheduled job
  - UP-BR-051: A non-unique secondary index on the transaction table's processed-timestamp column, covering every existing row. In a relational database this is a CREATE INDEX, which the database keeps up to date, not a separate rebuild job.
  - UP-BR-052: Expose a query or repository method that reads transactions by processed timestamp (exact match or range, in timestamp order) using that non-unique index. It must allow many transactions per timestamp.
  - _Requirements: UP-REQ-F-048, UP-REQ-F-049_
  - _Rules: UP-BR-051, UP-BR-052_
- [ ] 2. UP-C11-T2 [test-generation] Write a test for every acceptance criterion
  - 2 acceptance criteria, each a test named by its ID.
  - _Requirements: UP-REQ-F-048, UP-REQ-F-049_
  - _Criteria: UP-C11-AC-01, UP-C11-AC-02_
  - _After: UP-C11-T1_
