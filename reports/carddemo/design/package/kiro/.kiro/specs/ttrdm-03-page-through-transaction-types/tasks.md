# Implementation plan: Page through transaction types (TTRDM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. TTRDM-C03-T1 [data] Model the data the capability reads and writes
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSDB2RPY, CSDB2RWY, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: TTRDM-REQ-F-017, TTRDM-REQ-F-018, TTRDM-REQ-F-019, TTRDM-REQ-F-020, TTRDM-REQ-F-021, TTRDM-REQ-F-022, TTRDM-REQ-F-023, TTRDM-REQ-F-024, TTRDM-REQ-F-025, TTRDM-REQ-F-026, TTRDM-REQ-F-027, TTRDM-REQ-F-028, TTRDM-REQ-F-029, TTRDM-REQ-F-030, TTRDM-REQ-F-031_
- [ ] 2. TTRDM-C03-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: TTRDM-REQ-F-018, TTRDM-REQ-F-019, TTRDM-REQ-F-020, TTRDM-REQ-F-021, TTRDM-REQ-F-024_
  - _Rules: TTRDM-BR-023, TTRDM-BR-024, TTRDM-BR-025, TTRDM-BR-026, TTRDM-BR-027, TTRDM-BR-030_
  - _After: TTRDM-C03-T1_
- [ ] 3. TTRDM-C03-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: TTRDM-REQ-F-030, TTRDM-REQ-F-031, TTRDM-REQ-F-017, TTRDM-REQ-F-022, TTRDM-REQ-F-023, TTRDM-REQ-F-025, TTRDM-REQ-F-026, TTRDM-REQ-F-027, TTRDM-REQ-F-028, TTRDM-REQ-F-029_
  - _Rules: TTRDM-BR-022, TTRDM-BR-028, TTRDM-BR-029, TTRDM-BR-031, TTRDM-BR-032, TTRDM-BR-033, TTRDM-BR-034, TTRDM-BR-035, TTRDM-BR-036, TTRDM-BR-037_
  - _After: TTRDM-C03-T1_
- [ ] 4. TTRDM-C03-T4 [ui-modernization] Build the screen Transaction types (S-TRANTYPE-LIST)
  - To the prototype: ui-reference/index.html#/S-TRANTYPE-LIST.
  - button "Apply filters"
  - table "Transaction types"
  - _Requirements: TTRDM-REQ-F-017, TTRDM-REQ-F-018, TTRDM-REQ-F-019, TTRDM-REQ-F-020, TTRDM-REQ-F-021, TTRDM-REQ-F-022, TTRDM-REQ-F-023, TTRDM-REQ-F-024, TTRDM-REQ-F-025, TTRDM-REQ-F-026, TTRDM-REQ-F-027, TTRDM-REQ-F-028, TTRDM-REQ-F-029, TTRDM-REQ-F-030, TTRDM-REQ-F-031_
  - _Rules: TTRDM-BR-022, TTRDM-BR-023, TTRDM-BR-024, TTRDM-BR-025, TTRDM-BR-026, TTRDM-BR-027, TTRDM-BR-028, TTRDM-BR-029, TTRDM-BR-030, TTRDM-BR-031, TTRDM-BR-032, TTRDM-BR-033, TTRDM-BR-034, TTRDM-BR-035, TTRDM-BR-036, TTRDM-BR-037_
  - _After: TTRDM-C03-T2, TTRDM-C03-T3_
- [ ] 5. TTRDM-C03-T5 [test-generation] Write a test for every acceptance criterion
  - 21 acceptance criteria, each a test named by its ID.
  - _Requirements: TTRDM-REQ-F-017, TTRDM-REQ-F-018, TTRDM-REQ-F-019, TTRDM-REQ-F-020, TTRDM-REQ-F-021, TTRDM-REQ-F-022, TTRDM-REQ-F-023, TTRDM-REQ-F-024, TTRDM-REQ-F-025, TTRDM-REQ-F-026, TTRDM-REQ-F-027, TTRDM-REQ-F-028, TTRDM-REQ-F-029, TTRDM-REQ-F-030, TTRDM-REQ-F-031_
  - _Criteria: TTRDM-C03-AC-01, TTRDM-C03-AC-02, TTRDM-C03-AC-03, TTRDM-C03-AC-04, TTRDM-C03-AC-05, TTRDM-C03-AC-06, TTRDM-C03-AC-07, TTRDM-C03-AC-08, TTRDM-C03-AC-09, TTRDM-C03-AC-10, TTRDM-C03-AC-11, TTRDM-C03-AC-12, TTRDM-C03-AC-13, TTRDM-C03-AC-14, TTRDM-C03-AC-15, TTRDM-C03-AC-16, TTRDM-C03-AC-17, TTRDM-C03-AC-18, TTRDM-C03-AC-19, TTRDM-C03-AC-20, TTRDM-C03-AC-21_
  - _After: TTRDM-C03-T1, TTRDM-C03-T2, TTRDM-C03-T3, TTRDM-C03-T4_
