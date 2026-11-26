# Tasks: Seed and load the user security file (USPM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] USPM-C09-T1 [business-rules] Implement the business rules. Requirements: USPM-REQ-F-091, USPM-REQ-F-094. Rules: USPM-BR-099, USPM-BR-102.
  - Keep each business rule exactly as specified.
- [ ] USPM-C09-T2 [business-rules] Implement error handling and messages. Requirements: USPM-REQ-F-095, USPM-REQ-F-096. Rules: USPM-BR-103.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] USPM-C09-T3 [api] Build the scheduled job. Requirements: USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-097, USPM-REQ-F-098. Rules: USPM-BR-100, USPM-BR-101, USPM-BR-104, USPM-BR-105. After: USPM-C09-T1, USPM-C09-T2.
  - USPM-BR-100: The seed step must be repeatable. Remove any previous staged seed set first, keep the new one only if staging finishes successfully, and discard it if staging fails. A transactional load or a temporary table swapped in on success meets this.
  - USPM-BR-101: Recreate the user store from scratch, with the user ID (8 characters) as its unique primary key, then bulk-insert every staged seed record into it. This is a full reset, not a merge.
  - USPM-BR-104: The legacy job also copies the staged records, in arrival order, into an entry-sequenced copy of the user security file, whatever happened in earlier steps. The new application needs this only if something reads users in insertion order. Otherwise one keyed user store is enough. Confirm with the owner before building a second copy.
  - USPM-BR-105: The legacy job also copies the staged records into a relative-record (slot-numbered) copy of the user security file, whatever happened in earlier steps. The new application needs this only if a consumer looks users up by record number. Otherwise the keyed user store covers it. Confirm with the owner before building it.
- [ ] USPM-C09-T4 [test-generation] Write a test for every acceptance criterion. Requirements: USPM-REQ-F-091, USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-094, USPM-REQ-F-095, USPM-REQ-F-096, USPM-REQ-F-097, USPM-REQ-F-098. Criteria: USPM-C09-AC-01, USPM-C09-AC-02, USPM-C09-AC-03, USPM-C09-AC-04, USPM-C09-AC-05, USPM-C09-AC-06, USPM-C09-AC-07, USPM-C09-AC-08, USPM-C09-AC-09. After: USPM-C09-T1, USPM-C09-T2, USPM-C09-T3.
  - 9 acceptance criteria, each a test named by its ID.
- [ ] USPM-C09-T5 [compliance] Review the handling of personal data, security. Requirements: USPM-REQ-F-091, USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-094, USPM-REQ-F-095, USPM-REQ-F-096, USPM-REQ-F-097, USPM-REQ-F-098. After: USPM-C09-T1, USPM-C09-T2, USPM-C09-T3.
  - Check storage, logs, screens and audit against the rules.
