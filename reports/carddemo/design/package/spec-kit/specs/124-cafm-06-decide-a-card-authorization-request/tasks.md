# Tasks: Decide a card authorization request (CAFM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C06-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070.
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
- [ ] CAFM-C06-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-065, CAFM-REQ-F-070. Rules: CAFM-BR-061, CAFM-BR-062, CAFM-BR-063, CAFM-BR-064, CAFM-BR-065, CAFM-BR-067, CAFM-BR-068, CAFM-BR-069, CAFM-BR-070. After: CAFM-C06-T1.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: CAFM-BR-070.
- [ ] CAFM-C06-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-066. Rules: CAFM-BR-066. After: CAFM-C06-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C06-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070. Criteria: CAFM-C06-AC-01, CAFM-C06-AC-02, CAFM-C06-AC-03, CAFM-C06-AC-04, CAFM-C06-AC-05, CAFM-C06-AC-06, CAFM-C06-AC-07, CAFM-C06-AC-08, CAFM-C06-AC-09, CAFM-C06-AC-10, CAFM-C06-AC-11, CAFM-C06-AC-12, CAFM-C06-AC-13. After: CAFM-C06-T1, CAFM-C06-T2, CAFM-C06-T3.
  - 13 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C06-T5 [compliance] Review the handling of audit, card data, money, security. Requirements: CAFM-REQ-F-061, CAFM-REQ-F-062, CAFM-REQ-F-063, CAFM-REQ-F-064, CAFM-REQ-F-065, CAFM-REQ-F-066, CAFM-REQ-F-067, CAFM-REQ-F-068, CAFM-REQ-F-069, CAFM-REQ-F-070. After: CAFM-C06-T1, CAFM-C06-T2, CAFM-C06-T3.
  - Check storage, logs, screens and audit against the rules.
