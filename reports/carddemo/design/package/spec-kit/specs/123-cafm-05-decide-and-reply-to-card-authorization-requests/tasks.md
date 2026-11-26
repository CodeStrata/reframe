# Tasks: Decide and reply to card authorization requests (CAFM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C05-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060.
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
- [ ] CAFM-C05-T2 [business-rules] Implement the business rules. Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057. Rules: CAFM-BR-054, CAFM-BR-055, CAFM-BR-056, CAFM-BR-057, CAFM-BR-058. After: CAFM-C05-T1.
  - Keep each business rule exactly as specified.
- [ ] CAFM-C05-T3 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-058. Rules: CAFM-BR-059. After: CAFM-C05-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C05-T4 [api] Build the services behind the screens. Requirements: CAFM-REQ-F-059, CAFM-REQ-F-060. Rules: CAFM-BR-060. After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3.
  - CAFM-BR-060: Send each reply as a one-off, non-persistent message to the reply address named in the request, with the request's correlation id and a short time-to-live (expiry 50, which is 5 seconds in MQ's tenths of a second). This way stale replies expire instead of piling up. If the send fails, log critical error 'M004'.
- [ ] CAFM-C05-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060. Criteria: CAFM-C05-AC-01, CAFM-C05-AC-02, CAFM-C05-AC-03, CAFM-C05-AC-04, CAFM-C05-AC-05, CAFM-C05-AC-06, CAFM-C05-AC-07, CAFM-C05-AC-08, CAFM-C05-AC-09. After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3, CAFM-C05-T4.
  - 9 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C05-T6 [compliance] Review the handling of card data, money. Requirements: CAFM-REQ-F-052, CAFM-REQ-F-053, CAFM-REQ-F-054, CAFM-REQ-F-055, CAFM-REQ-F-056, CAFM-REQ-F-057, CAFM-REQ-F-058, CAFM-REQ-F-059, CAFM-REQ-F-060. After: CAFM-C05-T1, CAFM-C05-T2, CAFM-C05-T3, CAFM-C05-T4.
  - Check storage, logs, screens and audit against the rules.
