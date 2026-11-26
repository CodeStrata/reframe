# Tasks: Request a bill payment (OATM-C19)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C19-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-N-006, OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-151, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159.
  - File records: CVACT01Y, CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] OATM-C19-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-N-006, OATM-REQ-F-150, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159. Rules: OATM-BR-154, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-161, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165. After: OATM-C19-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C19-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-149, OATM-REQ-F-151, OATM-REQ-F-152. Rules: OATM-BR-155, OATM-BR-157, OATM-BR-158. After: OATM-C19-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C19-T4 [ui-modernization] Build the screen Pay balance (S-BILL-PAY). Requirements: OATM-REQ-N-006, OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159. Rules: OATM-BR-154, OATM-BR-155, OATM-BR-156, OATM-BR-158, OATM-BR-159, OATM-BR-160, OATM-BR-161, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165. After: OATM-C19-T2, OATM-C19-T3.
  - To the prototype: ui-reference/index.html#/S-BILL-PAY.
  - **lookup field** "Account number": Blank: 'Acct ID can NOT be empty...' - enter the 11-digit account number. Not found: 'Account ID NOT found...' - check the number with the caller.
  - **summary card** "Balance to pay": When the balance is zero or less: 'You have nothing to pay...' and Pay balance is unavailable.
  - **primary button** "Pay balance": The dialog offers only Pay or Cancel, so no other value can be entered (legacy: 'Invalid value. Valid values are (Y/N)...'). If the card linked to the account is not found, nothing is paid and the message says so. The payment and the balance change are saved together or not at all.
- [ ] OATM-C19-T5 [ui-modernization] Build the screen Application header and navigation (S-APP-SHELL). Requirements: OATM-REQ-N-006, OATM-REQ-F-150, OATM-REQ-F-151. Rules: OATM-BR-154, OATM-BR-156, OATM-BR-157. After: OATM-C19-T2, OATM-C19-T3.
  - To the prototype: ui-reference/index.html#/S-APP-SHELL.
  - **summary card** "CardDemo"
  - **primary button** "Pay balance"
- [ ] OATM-C19-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-N-006, OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-151, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159. Criteria: OATM-C19-AC-01, OATM-C19-AC-02, OATM-C19-AC-03, OATM-C19-AC-04, OATM-C19-AC-05, OATM-C19-AC-06, OATM-C19-AC-07, OATM-C19-AC-08, OATM-C19-AC-09, OATM-C19-AC-10, OATM-C19-AC-11, OATM-C19-AC-12, OATM-C19-AC-13, OATM-C19-AC-14, OATM-C19-AC-15, OATM-C19-AC-16. After: OATM-C19-T1, OATM-C19-T2, OATM-C19-T3, OATM-C19-T4, OATM-C19-T5.
  - 16 acceptance criteria, each a test named by its ID.
- [ ] OATM-C19-T7 [compliance] Review the handling of money, security. Requirements: OATM-REQ-N-006, OATM-REQ-F-149, OATM-REQ-F-150, OATM-REQ-F-151, OATM-REQ-F-152, OATM-REQ-F-153, OATM-REQ-F-154, OATM-REQ-F-155, OATM-REQ-F-156, OATM-REQ-F-157, OATM-REQ-F-158, OATM-REQ-F-159. After: OATM-C19-T1, OATM-C19-T2, OATM-C19-T3, OATM-C19-T4, OATM-C19-T5.
  - Check storage, logs, screens and audit against the rules.
