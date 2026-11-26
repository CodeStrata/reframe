# Implementation plan: Display account and customer details (OATM-C17)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C17-T1 [data] Model the data the capability reads and writes
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
- [ ] 2. OATM-C17-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-N-005_
  - _Rules: OATM-BR-141, OATM-BR-143_
  - _After: OATM-C17-T1_
- [ ] 3. OATM-C17-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
  - _Rules: OATM-BR-140, OATM-BR-141, OATM-BR-142, OATM-BR-144, OATM-BR-145, OATM-BR-146, OATM-BR-147_
  - _After: OATM-C17-T1_
- [ ] 4. OATM-C17-T4 [ui-modernization] Build the screen Account (S-ACCOUNT-VIEW)
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-VIEW.
  - search "Account number": Required: 'No input received' when blank; must be 11 digits and not all zeros: 'Account Filter must be a non-zero 11 digit number'.
  - message "Guidance"
  - display "Status"
  - display "Customer ID"
  - display "Social Security number"
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141_
  - _Rules: OATM-BR-140, OATM-BR-141, OATM-BR-142, OATM-BR-143, OATM-BR-144, OATM-BR-145, OATM-BR-146_
  - _After: OATM-C17-T2, OATM-C17-T3_
- [ ] 5. OATM-C17-T5 [test-generation] Write a test for every acceptance criterion
  - 11 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
  - _Criteria: OATM-C17-AC-01, OATM-C17-AC-02, OATM-C17-AC-03, OATM-C17-AC-04, OATM-C17-AC-05, OATM-C17-AC-06, OATM-C17-AC-07, OATM-C17-AC-08, OATM-C17-AC-09, OATM-C17-AC-10, OATM-C17-AC-11_
  - _After: OATM-C17-T1, OATM-C17-T2, OATM-C17-T3, OATM-C17-T4_
- [ ] 6. OATM-C17-T6 [compliance] Review the handling of money, personal data
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142_
  - _After: OATM-C17-T1, OATM-C17-T2, OATM-C17-T3, OATM-C17-T4_
