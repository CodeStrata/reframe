# Tasks: Detect changes to a fetched transaction type (TTRDM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C13-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102.
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
- [ ] TTRDM-C13-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102. Rules: TTRDM-BR-112, TTRDM-BR-113, TTRDM-BR-114, TTRDM-BR-115. After: TTRDM-C13-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C13-T3 [ui-modernization] Build the screen Transaction type (S-TRANTYPE-EDIT). Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102. Rules: TTRDM-BR-112, TTRDM-BR-113, TTRDM-BR-114, TTRDM-BR-115. After: TTRDM-C13-T2.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - message "No changes": Description must differ from the stored value (ignoring case and surrounding spaces): 'No changes to save.' (legacy 'No change detected with respect to values fetched.')
- [ ] TTRDM-C13-T4 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102. Criteria: TTRDM-C13-AC-01, TTRDM-C13-AC-02, TTRDM-C13-AC-03, TTRDM-C13-AC-04, TTRDM-C13-AC-05, TTRDM-C13-AC-06. After: TTRDM-C13-T1, TTRDM-C13-T2, TTRDM-C13-T3.
  - 6 acceptance criteria, each a test named by its ID.
