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
  - TTRDM-BR-048: The list form submits the two filters and, for each of up to 7 rows, the action code, type code and description. The server binds these into a request model, treating a description of '*' or only spaces as not entered and trimming any other description.
  - TTRDM-BR-049: Normalise each submitted row description on input: blank or a lone '*' becomes 'not entered' (null); any other value is trimmed of leading and trailing spaces before comparison and validation.
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042_
  - _Rules: TTRDM-BR-048, TTRDM-BR-049_
  - _After: TTRDM-C05-T1, TTRDM-C05-T2, TTRDM-C05-T3_
- [ ] 5. TTRDM-C05-T5 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - **data table** "Transaction types": In-place description: 'Transaction Desc must be supplied. Enter a description.' or 'Transaction Desc can have numbers or alphabets only. Remove other characters.'; unchanged: 'No change detected with respect to values fetched.' Row actions replace action codes, so 'Action code selected is invalid' and 'Please select only 1 action' cannot occur. If a filter or the row changes while a dialog is open, the dialog closes and nothing changes.
  - _Requirements: TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046_
  - _Rules: TTRDM-BR-050, TTRDM-BR-051, TTRDM-BR-052, TTRDM-BR-053_
  - _After: TTRDM-C05-T2, TTRDM-C05-T3, TTRDM-C05-T4_
- [ ] 6. TTRDM-C05-T6 [test-generation] Write a test for every acceptance criterion
  - 13 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-041, TTRDM-REQ-F-042, TTRDM-REQ-F-043, TTRDM-REQ-F-044, TTRDM-REQ-F-045, TTRDM-REQ-F-046, TTRDM-REQ-F-047, TTRDM-REQ-F-048, TTRDM-REQ-F-049, TTRDM-REQ-F-050, TTRDM-REQ-F-051_
  - _Criteria: TTRDM-C05-AC-01, TTRDM-C05-AC-02, TTRDM-C05-AC-03, TTRDM-C05-AC-04, TTRDM-C05-AC-05, TTRDM-C05-AC-06, TTRDM-C05-AC-07, TTRDM-C05-AC-08, TTRDM-C05-AC-09, TTRDM-C05-AC-10, TTRDM-C05-AC-11, TTRDM-C05-AC-12, TTRDM-C05-AC-13_
  - _After: TTRDM-C05-T1, TTRDM-C05-T2, TTRDM-C05-T3, TTRDM-C05-T4, TTRDM-C05-T5_
