# Implementation plan: Filter the transaction type list (TTRDM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C07-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054, TTRDM-REQ-F-055_
- [ ] 2. TTRDM-C07-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054_
  - _Rules: TTRDM-BR-061, TTRDM-BR-062, TTRDM-BR-063_
  - _After: TTRDM-C07-T1_
- [ ] 3. TTRDM-C07-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-055_
  - _Rules: TTRDM-BR-064_
  - _After: TTRDM-C07-T1_
- [ ] 4. TTRDM-C07-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **lookup field** "Type code": 'Type code filter, if supplied, must be a 2 digit number. Enter two digits, for example 01, or leave it blank.' No type matches: 'No Records found for these filter conditions. Change or clear the filters.'
  - **lookup field** "Description contains": Checked against the data only when a filter holds a value: 'No Records found for these filter conditions. Change or clear the filters.'
  - _Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-054_
  - _Rules: TTRDM-BR-061, TTRDM-BR-063_
  - _After: TTRDM-C07-T2, TTRDM-C07-T3_
- [ ] 5. TTRDM-C07-T5 [test-generation] Write a test for every acceptance criterion
  - 4 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-052, TTRDM-REQ-F-053, TTRDM-REQ-F-054, TTRDM-REQ-F-055_
  - _Criteria: TTRDM-C07-AC-01, TTRDM-C07-AC-02, TTRDM-C07-AC-03, TTRDM-C07-AC-04_
  - _After: TTRDM-C07-T1, TTRDM-C07-T2, TTRDM-C07-T3, TTRDM-C07-T4_
