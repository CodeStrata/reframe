# Tasks: Select a card to view or update (CCLDV-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CCLDV-C03-T1 [data] Model the data the capability reads and writes. Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-031, CCLDV-REQ-F-032, CCLDV-REQ-F-033.
  - File records: CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y.
- [ ] CCLDV-C03-T2 [business-rules] Implement the business rules. Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-032, CCLDV-REQ-F-033. Rules: CCLDV-BR-029, CCLDV-BR-030, CCLDV-BR-031. After: CCLDV-C03-T1.
  - Keep each business rule exactly as specified.
- [ ] CCLDV-C03-T3 [business-rules] Implement error handling and messages. Requirements: CCLDV-REQ-F-031. Rules: CCLDV-BR-028. After: CCLDV-C03-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CCLDV-C03-T4 [ui-modernization] Build the screen Cards (S-CARD-LIST). Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-032, CCLDV-REQ-F-033. Rules: CCLDV-BR-029, CCLDV-BR-030, CCLDV-BR-031. After: CCLDV-C03-T2, CCLDV-C03-T3.
  - To the prototype: ui-reference/index.html#/S-CARD-LIST.
  - **data table** "Cards found": Each row is its own link and only one opens at a time, so no selection code is typed and 'PLEASE SELECT ONLY ONE RECORD TO VIEW OR UPDATE' and 'INVALID ACTION CODE' cannot occur
- [ ] CCLDV-C03-T5 [test-generation] Write a test for every acceptance criterion. Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-031, CCLDV-REQ-F-032, CCLDV-REQ-F-033. Criteria: CCLDV-C03-AC-01, CCLDV-C03-AC-02, CCLDV-C03-AC-03, CCLDV-C03-AC-04, CCLDV-C03-AC-05, CCLDV-C03-AC-06, CCLDV-C03-AC-07. After: CCLDV-C03-T1, CCLDV-C03-T2, CCLDV-C03-T3, CCLDV-C03-T4.
  - 7 acceptance criteria, each a test named by its ID.
- [ ] CCLDV-C03-T6 [compliance] Review the handling of card data. Requirements: CCLDV-REQ-F-028, CCLDV-REQ-F-029, CCLDV-REQ-F-030, CCLDV-REQ-F-031, CCLDV-REQ-F-032, CCLDV-REQ-F-033. After: CCLDV-C03-T1, CCLDV-C03-T2, CCLDV-C03-T3, CCLDV-C03-T4.
  - Check storage, logs, screens and audit against the rules.
