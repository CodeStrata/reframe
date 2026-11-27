# Tasks: Retain dataset generations (UP-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C09-T1 [business-rules] Implement error handling and messages. Requirements: UP-REQ-F-046. Rules: UP-BR-049.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] UP-C09-T2 [api] Build the scheduled job. Requirements: UP-REQ-F-038, UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044, UP-REQ-F-045. Rules: UP-BR-041, UP-BR-042, UP-BR-043, UP-BR-044, UP-BR-045, UP-BR-046, UP-BR-047, UP-BR-048. After: UP-C09-T1.
  - UP-BR-041: Keep each run's daily rejected-transactions output as a versioned object, for example a dated file in object storage. A retention policy keeps the latest 5 and deletes older ones.
  - UP-BR-042: Version the combined transaction file (the transaction backup merged with system-generated transactions) per run. Keep the latest 5 and delete the data of older versions automatically.
  - UP-BR-043: Version the daily transaction input per run. Keep the latest 5 and delete older versions automatically.
  - UP-BR-044: Version the transaction report per run and keep the latest 5. Another set-up job defines the same report history with 10 versions (rule bc474731…), so the team must choose one limit.
  - UP-BR-045: A retention policy for the daily transaction report that keeps the latest 10 versions; the oldest goes when an eleventh is created. This conflicts with the 5-version definition in the main set-up (rule 1b564856…), so the team must decide which one applies.
  - UP-BR-046: Take a versioned backup of the transaction category balances on each run. Keep the latest 5 and delete older ones automatically.
  - UP-BR-047: Take a versioned backup of the transaction master on each run. Keep the latest 5 and delete older ones automatically.
  - UP-BR-048: Version the system-generated transaction file per run. Keep the latest 5 and delete older ones automatically.
- [ ] UP-C09-T3 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-038, UP-REQ-F-039, UP-REQ-F-040, UP-REQ-F-041, UP-REQ-F-042, UP-REQ-F-043, UP-REQ-F-044, UP-REQ-F-045, UP-REQ-F-046. Criteria: UP-C09-AC-01, UP-C09-AC-02, UP-C09-AC-03, UP-C09-AC-04, UP-C09-AC-05, UP-C09-AC-06, UP-C09-AC-07, UP-C09-AC-08, UP-C09-AC-09, UP-C09-AC-10. After: UP-C09-T1, UP-C09-T2.
  - 10 acceptance criteria, each a test named by its ID.
