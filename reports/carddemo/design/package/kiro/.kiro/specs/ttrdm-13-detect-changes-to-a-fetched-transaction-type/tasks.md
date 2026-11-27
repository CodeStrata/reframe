# Implementation plan: Detect changes to a fetched transaction type (TTRDM-C13)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C13-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDWY, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102_
- [ ] 2. TTRDM-C13-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102_
  - _Rules: TTRDM-BR-112, TTRDM-BR-113, TTRDM-BR-114, TTRDM-BR-115_
  - _After: TTRDM-C13-T1_
- [ ] 3. TTRDM-C13-T3 [ui-modernization] Build the screen Add or change a transaction type (S-TRANTYPE-EDIT)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-EDIT.
  - **primary button** "Save transaction type": Code and description match what is stored (ignoring case and surrounding spaces): 'No change detected with respect to values fetched.'
  - _Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101_
  - _Rules: TTRDM-BR-112, TTRDM-BR-113, TTRDM-BR-114_
  - _After: TTRDM-C13-T2_
- [ ] 4. TTRDM-C13-T4 [test-generation] Write a test for every acceptance criterion
  - 6 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-100, TTRDM-REQ-F-101, TTRDM-REQ-F-102_
  - _Criteria: TTRDM-C13-AC-01, TTRDM-C13-AC-02, TTRDM-C13-AC-03, TTRDM-C13-AC-04, TTRDM-C13-AC-05, TTRDM-C13-AC-06_
  - _After: TTRDM-C13-T1, TTRDM-C13-T2, TTRDM-C13-T3_
