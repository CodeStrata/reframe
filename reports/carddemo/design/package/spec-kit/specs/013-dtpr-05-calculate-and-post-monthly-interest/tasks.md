# Tasks: Calculate and post monthly interest (DTPR-C05)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C05-T1 [data] Model the data the capability reads and writes. Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051.
  - File records: CVACT01Y, CVACT03Y, CVTRA01Y, CVTRA02Y, CVTRA05Y (see data-contracts.md).
- [ ] DTPR-C05-T2 [business-rules] Implement the business rules. Requirements: DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-046. Rules: DTPR-BR-045, DTPR-BR-046, DTPR-BR-047, DTPR-BR-048, DTPR-BR-049, DTPR-BR-050, DTPR-BR-051, DTPR-BR-052, DTPR-BR-053. After: DTPR-C05-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: DTPR-BR-051.
- [ ] DTPR-C05-T3 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051. Rules: DTPR-BR-054, DTPR-BR-055, DTPR-BR-056. After: DTPR-C05-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C05-T4 [api] Build the scheduled job. Requirements: DTPR-REQ-F-038. Rules: DTPR-BR-044. After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3.
  - DTPR-BR-044: Read all category balances in key order (account ID, then type, then category) as one sorted stream, so each account's balances come together. The per-account interest total and the account rewrite depend on that grouping.
- [ ] DTPR-C05-T5 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051. Criteria: DTPR-C05-AC-01, DTPR-C05-AC-02, DTPR-C05-AC-03, DTPR-C05-AC-04, DTPR-C05-AC-05, DTPR-C05-AC-06, DTPR-C05-AC-07, DTPR-C05-AC-08, DTPR-C05-AC-09, DTPR-C05-AC-10, DTPR-C05-AC-11, DTPR-C05-AC-12, DTPR-C05-AC-13, DTPR-C05-AC-14, DTPR-C05-AC-15, DTPR-C05-AC-16, DTPR-C05-AC-17. After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3, DTPR-C05-T4.
  - 17 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C05-T6 [compliance] Review the handling of card data, money. Requirements: DTPR-REQ-F-038, DTPR-REQ-F-039, DTPR-REQ-F-040, DTPR-REQ-F-041, DTPR-REQ-F-042, DTPR-REQ-F-043, DTPR-REQ-F-044, DTPR-REQ-F-045, DTPR-REQ-F-046, DTPR-REQ-F-047, DTPR-REQ-F-048, DTPR-REQ-F-049, DTPR-REQ-F-050, DTPR-REQ-F-051. After: DTPR-C05-T1, DTPR-C05-T2, DTPR-C05-T3, DTPR-C05-T4.
  - Check storage, logs, screens and audit against the rules.
