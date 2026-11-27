# Implementation plan: Filter the card list by account and card number (CCLDV-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

- [ ] 1. CCLDV-C02-T1 [data] Model the data the capability reads and writes
  - File records: CVACT02Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVCRD01Y.
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027_
- [ ] 2. CCLDV-C02-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026_
  - _Rules: CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-025, CCLDV-BR-026, CCLDV-BR-027_
  - _After: CCLDV-C02-T1_
- [ ] 3. CCLDV-C02-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: CCLDV-REQ-F-027_
  - _Rules: CCLDV-BR-021, CCLDV-BR-028_
  - _After: CCLDV-C02-T1_
- [ ] 4. CCLDV-C02-T4 [ui-modernization] Build the screen Cards (S-CARD-LIST)
  - To the prototype: ui-reference/index.html#/S-CARD-LIST.
  - **lookup field** "Account number": Must be an 11-digit number if entered: 'Account filter, if supplied, must be an 11 digit number. Enter the 11 digits or leave it blank.'
  - **lookup field** "Card number": Must be a 16-digit number if entered: 'Card ID filter, if supplied, must be a 16 digit number. Enter the 16 digits or leave it blank.'
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-025, CCLDV-REQ-F-026_
  - _Rules: CCLDV-BR-023, CCLDV-BR-024, CCLDV-BR-025, CCLDV-BR-026, CCLDV-BR-027_
  - _After: CCLDV-C02-T2, CCLDV-C02-T3_
- [ ] 5. CCLDV-C02-T5 [test-generation] Write a test for every acceptance criterion
  - 10 acceptance criteria, each a test named by its ID.
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027_
  - _Criteria: CCLDV-C02-AC-01, CCLDV-C02-AC-02, CCLDV-C02-AC-03, CCLDV-C02-AC-04, CCLDV-C02-AC-05, CCLDV-C02-AC-06, CCLDV-C02-AC-07, CCLDV-C02-AC-08, CCLDV-C02-AC-09, CCLDV-C02-AC-10_
  - _After: CCLDV-C02-T1, CCLDV-C02-T2, CCLDV-C02-T3, CCLDV-C02-T4_
- [ ] 6. CCLDV-C02-T6 [compliance] Review the handling of card data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: CCLDV-REQ-F-021, CCLDV-REQ-F-022, CCLDV-REQ-F-023, CCLDV-REQ-F-024, CCLDV-REQ-F-025, CCLDV-REQ-F-026, CCLDV-REQ-F-027_
  - _After: CCLDV-C02-T1, CCLDV-C02-T2, CCLDV-C02-T3, CCLDV-C02-T4_
