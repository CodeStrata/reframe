# Implementation plan: Filter the transaction type list (TTRDM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C04-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034, TTRDM-REQ-F-035, TTRDM-REQ-F-036, TTRDM-REQ-F-037, TTRDM-REQ-F-038, TTRDM-REQ-F-039, TTRDM-REQ-F-040_
- [ ] 2. TTRDM-C04-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034, TTRDM-REQ-F-037, TTRDM-REQ-F-038, TTRDM-REQ-F-039_
  - _Rules: TTRDM-BR-038, TTRDM-BR-039, TTRDM-BR-040, TTRDM-BR-041, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-046_
  - _After: TTRDM-C04-T1_
- [ ] 3. TTRDM-C04-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-040_
  - _Rules: TTRDM-BR-047_
  - _After: TTRDM-C04-T1_
- [ ] 4. TTRDM-C04-T4 [api] Build the services behind the screens
  - TTRDM-BR-042: Keep the last-used type code filter in session state. When the submitted filter differs from it, save the new value, reset paging to the first page, and set a 'filter changed' flag. With that flag set, a pending F10 confirmation is ignored and handled as a plain refresh.
  - TTRDM-BR-043: When the submitted type code filter equals the saved one, or both are empty, keep the current page position and clear the 'filter changed' flag.
  - _Requirements: TTRDM-REQ-F-035, TTRDM-REQ-F-036_
  - _Rules: TTRDM-BR-042, TTRDM-BR-043_
  - _After: TTRDM-C04-T1, TTRDM-C04-T2, TTRDM-C04-T3_
- [ ] 5. TTRDM-C04-T5 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - form "Filter transaction types"
  - text "Type code": If supplied, must be a 2-digit number; blank or 00 means no type filter. Message: 'Type code filter, if supplied, must be a 2-digit number.'
  - search "Description contains"
  - button "Clear filters"
  - message "No matching transaction types": Supplied filters must match at least one type: 'No transaction types match these filters.' (legacy 'No Records found for these filter conditions')
  - _Requirements: TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034, TTRDM-REQ-F-035, TTRDM-REQ-F-036, TTRDM-REQ-F-037, TTRDM-REQ-F-038, TTRDM-REQ-F-039, TTRDM-REQ-F-040_
  - _Rules: TTRDM-BR-038, TTRDM-BR-039, TTRDM-BR-040, TTRDM-BR-041, TTRDM-BR-042, TTRDM-BR-043, TTRDM-BR-044, TTRDM-BR-045, TTRDM-BR-046, TTRDM-BR-047_
  - _After: TTRDM-C04-T2, TTRDM-C04-T3, TTRDM-C04-T4_
- [ ] 6. TTRDM-C04-T6 [test-generation] Write a test for every acceptance criterion
  - 12 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-032, TTRDM-REQ-F-033, TTRDM-REQ-F-034, TTRDM-REQ-F-035, TTRDM-REQ-F-036, TTRDM-REQ-F-037, TTRDM-REQ-F-038, TTRDM-REQ-F-039, TTRDM-REQ-F-040_
  - _Criteria: TTRDM-C04-AC-01, TTRDM-C04-AC-02, TTRDM-C04-AC-03, TTRDM-C04-AC-04, TTRDM-C04-AC-05, TTRDM-C04-AC-06, TTRDM-C04-AC-07, TTRDM-C04-AC-08, TTRDM-C04-AC-09, TTRDM-C04-AC-10, TTRDM-C04-AC-11, TTRDM-C04-AC-12_
  - _After: TTRDM-C04-T1, TTRDM-C04-T2, TTRDM-C04-T3, TTRDM-C04-T4, TTRDM-C04-T5_
