# Tasks: Produce daily transaction report (DTPR-C06)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] DTPR-C06-T1 [data] Model the data the capability reads and writes. Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056.
  - File records: CVACT03Y, CVTRA03Y, CVTRA04Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: CVTRA07Y.
- [ ] DTPR-C06-T2 [business-rules] Implement error handling and messages. Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-056. Rules: DTPR-BR-057, DTPR-BR-058, DTPR-BR-060. After: DTPR-C06-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] DTPR-C06-T3 [api] Build the services and the scheduled job. Requirements: DTPR-REQ-F-054, DTPR-REQ-F-055. Rules: DTPR-BR-059. After: DTPR-C06-T1, DTPR-C06-T2.
  - DTPR-BR-059: For each in-range transaction, look up the card's cross-reference (giving the account) by card number, the type description by type code, and the category description by type and category code. A missing reference record must fail the report run rather than print a blank. The type and category tables are small and can be cached for the run.
- [ ] DTPR-C06-T4 [test-generation] Write a test for every acceptance criterion. Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056. Criteria: DTPR-C06-AC-01, DTPR-C06-AC-02, DTPR-C06-AC-03, DTPR-C06-AC-04, DTPR-C06-AC-05, DTPR-C06-AC-06, DTPR-C06-AC-07, DTPR-C06-AC-08. After: DTPR-C06-T1, DTPR-C06-T2, DTPR-C06-T3.
  - 8 acceptance criteria, each a test named by its ID.
- [ ] DTPR-C06-T5 [compliance] Review the handling of card data, money. Requirements: DTPR-REQ-F-052, DTPR-REQ-F-053, DTPR-REQ-F-054, DTPR-REQ-F-055, DTPR-REQ-F-056. After: DTPR-C06-T1, DTPR-C06-T2, DTPR-C06-T3.
  - Check storage, logs, screens and audit against the rules.
