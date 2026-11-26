# Tasks: Display account and customer details (OATM-C17)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C17-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142.
  - File records: CSMSG02Y, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CSSTRPFY, CSUSR01Y, CVACT02Y, CVCRD01Y.
- [ ] OATM-C17-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-N-005. Rules: OATM-BR-141, OATM-BR-143. After: OATM-C17-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C17-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142. Rules: OATM-BR-140, OATM-BR-141, OATM-BR-142, OATM-BR-144, OATM-BR-145, OATM-BR-146, OATM-BR-147. After: OATM-C17-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C17-T4 [ui-modernization] Build the screen Account (S-ACCOUNT-VIEW). Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142. Rules: OATM-BR-140, OATM-BR-141, OATM-BR-142, OATM-BR-143, OATM-BR-144, OATM-BR-145, OATM-BR-146, OATM-BR-147. After: OATM-C17-T2, OATM-C17-T3.
  - To the prototype: ui-reference/index.html#/S-ACCOUNT-VIEW.
  - **lookup field** "Account or card number": Blank: 'No input received' - enter an account number (11 digits) or a card number (16 digits). Not digits, wrong length or all zeros: 'Account Number if supplied must be a 11 digit Non-Zero Number' (or a 16-digit card number). Not in the card cross-reference: 'Account:<number> not found in Cross ref file.' - check the number with the caller. The error shows under the field.
  - **status badge** "Account status"
  - **summary card** "Account"
  - **summary card** "Customer"
  - **summary card** "Address and phone"
- [ ] OATM-C17-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142. Criteria: OATM-C17-AC-01, OATM-C17-AC-02, OATM-C17-AC-03, OATM-C17-AC-04, OATM-C17-AC-05, OATM-C17-AC-06, OATM-C17-AC-07, OATM-C17-AC-08, OATM-C17-AC-09, OATM-C17-AC-10, OATM-C17-AC-11. After: OATM-C17-T1, OATM-C17-T2, OATM-C17-T3, OATM-C17-T4.
  - 11 acceptance criteria, each a test named by its ID.
- [ ] OATM-C17-T6 [compliance] Review the handling of money, personal data. Requirements: OATM-REQ-F-137, OATM-REQ-F-138, OATM-REQ-N-005, OATM-REQ-F-139, OATM-REQ-F-140, OATM-REQ-F-141, OATM-REQ-F-142. After: OATM-C17-T1, OATM-C17-T2, OATM-C17-T3, OATM-C17-T4.
  - Check storage, logs, screens and audit against the rules.
