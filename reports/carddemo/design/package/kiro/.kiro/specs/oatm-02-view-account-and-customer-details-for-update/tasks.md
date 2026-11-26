# Implementation plan: View account and customer details for update (OATM-C02)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C02-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSLKPCDY, CSMSG01Y, CSSETATY, CSSTRPFY, CSUSR01Y, CSUTLDPY, CSUTLDWY, CVCRD01Y.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
- [ ] 2. OATM-C02-T2 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
  - _Rules: OATM-BR-015, OATM-BR-016, OATM-BR-017, OATM-BR-018, OATM-BR-019, OATM-BR-020, OATM-BR-021, OATM-BR-022, OATM-BR-023, OATM-BR-024, OATM-BR-025_
  - _After: OATM-C02-T1_
- [ ] 3. OATM-C02-T3 [ui-modernization] Build the screen Update account (S-ACCOUNT-EDIT)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-EDIT.
  - **lookup field** "Account number": Blank: 'No input received' - enter an account number. Not 11 digits or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number'. Not in the card cross-reference: 'Account:<account> not found in Cross ref file.' - check the number with the caller. Only the account number is checked until an account is fetched.
  - **summary card** "Status and group": Status is required: 'Account Status must be supplied.' and must be Active or Inactive ('Account Status must be Y or N.'). The choice offers only those two values.
  - **summary card** "Fix these before saving"
  - **primary button** "Save changes": If no value differs: 'No change detected with respect to values fetched.' If the record was changed by someone else since it was fetched: 'Record changed by some one else. Please review' and the latest values are shown. If a lock or update fails: 'Changes unsuccessful. Please try again'; nothing is half-saved.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
  - _Rules: OATM-BR-015, OATM-BR-016, OATM-BR-017, OATM-BR-018, OATM-BR-019, OATM-BR-020, OATM-BR-021, OATM-BR-022, OATM-BR-023, OATM-BR-024, OATM-BR-025_
  - _After: OATM-C02-T2_
- [ ] 4. OATM-C02-T4 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
  - _Criteria: OATM-C02-AC-01, OATM-C02-AC-02, OATM-C02-AC-03, OATM-C02-AC-04, OATM-C02-AC-05, OATM-C02-AC-06, OATM-C02-AC-07, OATM-C02-AC-08, OATM-C02-AC-09, OATM-C02-AC-10, OATM-C02-AC-11, OATM-C02-AC-12, OATM-C02-AC-13, OATM-C02-AC-14, OATM-C02-AC-15_
  - _After: OATM-C02-T1, OATM-C02-T2, OATM-C02-T3_
- [ ] 5. OATM-C02-T5 [compliance] Review the handling of card data, money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-015, OATM-REQ-F-016, OATM-REQ-F-017, OATM-REQ-F-018, OATM-REQ-F-019, OATM-REQ-F-020, OATM-REQ-F-021, OATM-REQ-F-022, OATM-REQ-F-023, OATM-REQ-N-001, OATM-REQ-N-002, OATM-REQ-F-024_
  - _After: OATM-C02-T1, OATM-C02-T2, OATM-C02-T3_
