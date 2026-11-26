# Implementation plan: Seed and load the user security file (USPM-C09)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. USPM-C09-T1 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: USPM-REQ-F-091, USPM-REQ-F-094_
  - _Rules: USPM-BR-099, USPM-BR-102_
- [ ] 2. USPM-C09-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: USPM-REQ-F-095, USPM-REQ-F-096_
  - _Rules: USPM-BR-103_
- [ ] 3. USPM-C09-T3 [api] Build the scheduled job
  - USPM-BR-100: The seed step should be idempotent: remove any earlier seed data before staging, keep the new staging set only if staging completes, and discard it if staging fails. A transaction or a write-then-rename of the seed file gives this.
  - USPM-BR-101: Provide a setup or migration job that drops and recreates the user table keyed on an 8-character User ID, then bulk-loads every staged seed record into it. It runs on demand at environment setup, not as part of normal operation.
  - USPM-BR-104: The legacy job also copies the staged records into an entry-sequenced copy of the user file, without regard to whether earlier steps succeeded. The new application needs this only if some consumer reads users in load order. Otherwise one keyed user table covers it, and the copy should be confirmed as unneeded rather than rebuilt.
  - USPM-BR-105: The legacy job also copies the staged records into a relative-record (record-number addressed) copy of the user file, without regard to whether earlier steps succeeded. Rebuild this only if some consumer looks users up by position. Otherwise the keyed user table is enough.
  - _Requirements: USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-097, USPM-REQ-F-098_
  - _Rules: USPM-BR-100, USPM-BR-101, USPM-BR-104, USPM-BR-105_
  - _After: USPM-C09-T1, USPM-C09-T2_
- [ ] 4. USPM-C09-T4 [test-generation] Write a test for every acceptance criterion
  - 9 acceptance criteria, each a test named by its ID.
  - _Requirements: USPM-REQ-F-091, USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-094, USPM-REQ-F-095, USPM-REQ-F-096, USPM-REQ-F-097, USPM-REQ-F-098_
  - _Criteria: USPM-C09-AC-01, USPM-C09-AC-02, USPM-C09-AC-03, USPM-C09-AC-04, USPM-C09-AC-05, USPM-C09-AC-06, USPM-C09-AC-07, USPM-C09-AC-08, USPM-C09-AC-09_
  - _After: USPM-C09-T1, USPM-C09-T2, USPM-C09-T3_
- [ ] 5. USPM-C09-T5 [compliance] Review the handling of personal data, security
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: USPM-REQ-F-091, USPM-REQ-F-092, USPM-REQ-F-093, USPM-REQ-F-094, USPM-REQ-F-095, USPM-REQ-F-096, USPM-REQ-F-097, USPM-REQ-F-098_
  - _After: USPM-C09-T1, USPM-C09-T2, USPM-C09-T3_
