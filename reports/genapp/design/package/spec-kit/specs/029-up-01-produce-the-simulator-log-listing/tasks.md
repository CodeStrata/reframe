# Tasks: Produce the simulator log listing (UP-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C01-T1 [api] Build the scheduled job. Requirements: UP-REQ-F-001, UP-REQ-F-002. Rules: UP-BR-001, UP-BR-002.
  - UP-BR-001: A scheduled or on-demand job reads the simulator log in shared, read-only mode, so other runs can read it at the same time. It formats the records with the same options as today: console, SNA formatting, display, data, run and end. If the simulator is retired, this job goes with it.
  - UP-BR-002: The formatted listing goes to the job's printed report output (print class A today) and is kept where operators can view it. The job opens the simulator log as input only and needs no write access to it.
- [ ] UP-C01-T2 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-001, UP-REQ-F-002. Criteria: UP-C01-AC-01, UP-C01-AC-02. After: UP-C01-T1.
  - 2 acceptance criteria, each a test named by its ID.
