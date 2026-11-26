# Tasks: Publish statistics to shared queues (TSM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TSM-C03-T1 [business-rules] Implement the business rules. Requirements: TSM-REQ-F-011, TSM-REQ-F-012, TSM-REQ-F-013, TSM-REQ-F-014, TSM-REQ-F-015. Rules: TSM-BR-009, TSM-BR-010, TSM-BR-011, TSM-BR-012, TSM-BR-013, TSM-BR-014.
  - Keep each business rule exactly as specified.
- [ ] TSM-C03-T2 [api] Build the scheduled job. Requirements: TSM-REQ-F-011, TSM-REQ-F-012, TSM-REQ-F-013, TSM-REQ-F-014, TSM-REQ-F-015. Rules: TSM-BR-009, TSM-BR-010, TSM-BR-011, TSM-BR-012, TSM-BR-013, TSM-BR-014. After: TSM-C03-T1.
  - TSM-BR-009: Each statistic needs a small keyed record, keyed by its queue name (for example 'GENA100V' or 'GENAX00V'), that holds the current value, the previous value and the change. Publishing reads the stored current value as the previous value and then replaces the whole record with new, previous and change (new minus previous). Do this as one atomic replace, such as a keyed upsert in a cache or table, so readers never see an empty or half-written statistic. Keep the order new, previous, change wherever consumers read it as a list.
- [ ] TSM-C03-T3 [test-generation] Write a test for every acceptance criterion. Requirements: TSM-REQ-F-011, TSM-REQ-F-012, TSM-REQ-F-013, TSM-REQ-F-014, TSM-REQ-F-015. Criteria: TSM-C03-AC-01, TSM-C03-AC-02, TSM-C03-AC-03, TSM-C03-AC-04. After: TSM-C03-T1, TSM-C03-T2.
  - 4 acceptance criteria, each a test named by its ID.
