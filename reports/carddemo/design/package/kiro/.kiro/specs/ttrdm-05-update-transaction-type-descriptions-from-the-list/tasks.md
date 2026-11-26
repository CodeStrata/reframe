# Implementation plan: Update transaction type descriptions from the list (TTRDM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C05-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042, TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-047, TTRDM-REQ-F-048, TTRDM-REQ-F-049, TTRDM-REQ-F-050, TTRDM-REQ-F-051_
- [ ] 2. TTRDM-C05-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-050_
  - _Rules: TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053, TTRDM-BR-057_
  - _After: TTRDM-C05-T1_
- [ ] 3. TTRDM-C05-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-047, TTRDM-REQ-F-048, TTRDM-REQ-F-049, TTRDM-REQ-F-051_
  - _Rules: TTRDM-BR-054, TTRDM-BR-055, TTRDM-BR-056, TTRDM-BR-058_
  - _After: TTRDM-C05-T1_
- [ ] 4. TTRDM-C05-T4 [api] Build the services behind the screens
  - TTRDM-BR-048: The list form posts the two filters plus seven row entries, each with an action, a type code and a description. Bind them to a request model with a fixed list of 7 rows. Map a description of '*' or all spaces to 'not entered', and trim any other description.
  - TTRDM-BR-049: Normalise row descriptions when reading the request: a blank value or a lone '*' becomes null (not entered), and any other value is trimmed at both ends. Validation and change detection work on the normalised value.
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042_
  - _Rules: TTRDM-BR-048, TTRDM-BR-049_
  - _After: TTRDM-C05-T1, TTRDM-C05-T2, TTRDM-C05-T3_
- [ ] 5. TTRDM-C05-T5 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - message "No matching transaction types": Supplied filters must match at least one type: 'No transaction types match these filters.' (legacy 'No Records found for these filter conditions')
  - button "Edit description": One row action at a time, so the legacy errors 'Please select only 1 action' and 'Action code selected is invalid' cannot occur.
  - text "Description": Required; letters, digits and spaces only. Messages: 'Enter a description.' (legacy 'Transaction Desc must be supplied.'), 'Description can only contain letters, digits and spaces.' (legacy 'Transaction Desc can have numbers or alphabets only.'). If unchanged: 'No changes to save.' (legacy 'No change detected with respect to values fetched.')
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042, TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-047, TTRDM-REQ-F-048, TTRDM-REQ-F-049, TTRDM-REQ-F-050, TTRDM-REQ-F-051_
  - _Rules: TTRDM-BR-048, TTRDM-BR-049, TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053, TTRDM-BR-054, TTRDM-BR-055, TTRDM-BR-056, TTRDM-BR-057, TTRDM-BR-058_
  - _After: TTRDM-C05-T2, TTRDM-C05-T3, TTRDM-C05-T4_
- [ ] 6. TTRDM-C05-T6 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042, TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-047, TTRDM-REQ-F-048, TTRDM-REQ-F-049, TTRDM-REQ-F-050, TTRDM-REQ-F-051_
  - _Criteria: TTRDM-C05-AC-01, TTRDM-C05-AC-02, TTRDM-C05-AC-03, TTRDM-C05-AC-04, TTRDM-C05-AC-05, TTRDM-C05-AC-06, TTRDM-C05-AC-07, TTRDM-C05-AC-08, TTRDM-C05-AC-09, TTRDM-C05-AC-10, TTRDM-C05-AC-11, TTRDM-C05-AC-12, TTRDM-C05-AC-13_
  - _After: TTRDM-C05-T1, TTRDM-C05-T2, TTRDM-C05-T3, TTRDM-C05-T4, TTRDM-C05-T5_
