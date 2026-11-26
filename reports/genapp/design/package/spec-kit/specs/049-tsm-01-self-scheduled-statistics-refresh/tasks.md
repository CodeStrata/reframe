# Tasks: Self-scheduled statistics refresh (TSM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TSM-C01-T1 [business-rules] Implement the business rules. Requirements: TSM-REQ-F-002, TSM-REQ-F-003, TSM-REQ-F-004. Rules: TSM-BR-002.
  - Keep each business rule exactly as specified.
- [ ] TSM-C01-T2 [api] Build the scheduled job. Requirements: TSM-REQ-F-001. Rules: TSM-BR-001. After: TSM-C01-T1.
  - TSM-BR-001: The new application needs a scheduled job that starts the statistics collection once a minute. The legacy run books its own next run first, before it reads any counters, and never checks whether the booking worked. A scheduler with a fixed one-minute interval, such as a cron trigger or a timer service, replaces that self-booking. It must still run every minute even if a run fails partway, so that one failure does not stop the cycle.
- [ ] TSM-C01-T3 [test-generation] Write a test for every acceptance criterion. Requirements: TSM-REQ-F-001, TSM-REQ-F-002, TSM-REQ-F-003, TSM-REQ-F-004. Criteria: TSM-C01-AC-01, TSM-C01-AC-02, TSM-C01-AC-03, TSM-C01-AC-04. After: TSM-C01-T1, TSM-C01-T2.
  - 4 acceptance criteria, each a test named by its ID.
