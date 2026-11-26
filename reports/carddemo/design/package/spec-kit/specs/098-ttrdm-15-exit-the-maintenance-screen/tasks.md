# Tasks: Exit the maintenance screen (TTRDM-C15)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C15-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-106, TTRDM-REQ-F-107.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C15-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-107. Rules: TTRDM-BR-120. After: TTRDM-C15-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C15-T3 [api] Build the services behind the screens. Requirements: TTRDM-REQ-F-106. Rules: TTRDM-BR-119. After: TTRDM-C15-T1, TTRDM-C15-T2.
  - TTRDM-BR-119: On exit, the new application must commit or close any open database transaction for the session before navigating. It then redirects to the return route stored in the session, falling back to the Admin menu route when none is stored. No unit of work may be left open across the navigation.
- [ ] TTRDM-C15-T4 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: TTRDM-REQ-F-106. Rules: TTRDM-BR-119. After: TTRDM-C15-T2, TTRDM-C15-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **data table** "Transaction types"
- [ ] TTRDM-C15-T5 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-106, TTRDM-REQ-F-107. Criteria: TTRDM-C15-AC-01, TTRDM-C15-AC-02, TTRDM-C15-AC-03. After: TTRDM-C15-T1, TTRDM-C15-T2, TTRDM-C15-T3, TTRDM-C15-T4.
  - 3 acceptance criteria, each a test named by its ID.
