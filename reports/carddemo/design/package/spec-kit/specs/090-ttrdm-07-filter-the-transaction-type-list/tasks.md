# Tasks: Filter the transaction type list (TTRDM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] TTRDM-C07-T1 [data] Model the data the capability reads and writes. Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054, TTRDM-REQ-F-055.
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
- [ ] TTRDM-C07-T2 [business-rules] Implement the business rules. Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054. Rules: TTRDM-BR-061, TTRDM-BR-062, TTRDM-BR-063. After: TTRDM-C07-T1.
  - Keep each business rule exactly as specified.
- [ ] TTRDM-C07-T3 [business-rules] Implement error handling and messages. Requirements: TTRDM-REQ-F-055. Rules: TTRDM-BR-064. After: TTRDM-C07-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] TTRDM-C07-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST). Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-054. Rules: TTRDM-BR-061, TTRDM-BR-063. After: TTRDM-C07-T2, TTRDM-C07-T3.
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **lookup field** "Type code": 'Type code filter, if supplied, must be a 2 digit number. Enter two digits, for example 01, or leave it blank.' No type matches: 'No Records found for these filter conditions. Change or clear the filters.'
  - **lookup field** "Description contains": Checked against the data only when a filter holds a value: 'No Records found for these filter conditions. Change or clear the filters.'
- [ ] TTRDM-C07-T5 [test-generation] Write a test for every acceptance criterion. Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054, TTRDM-REQ-F-055. Criteria: TTRDM-C07-AC-01, TTRDM-C07-AC-02, TTRDM-C07-AC-03, TTRDM-C07-AC-04. After: TTRDM-C07-T1, TTRDM-C07-T2, TTRDM-C07-T3, TTRDM-C07-T4.
  - 4 acceptance criteria, each a test named by its ID.
