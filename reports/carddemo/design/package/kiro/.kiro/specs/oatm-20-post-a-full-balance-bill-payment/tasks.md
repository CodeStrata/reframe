# Implementation plan: Post a full-balance bill payment (OATM-C20)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C20-T1 [data] Model the data the capability reads and writes
  - File records: CVACT01Y, CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170_
- [ ] 2. OATM-C20-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-162, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166_
  - _Rules: OATM-BR-166, OATM-BR-168, OATM-BR-170, OATM-BR-171, OATM-BR-172, OATM-BR-173, OATM-BR-174_
  - _After: OATM-C20-T1_
- [ ] 3. OATM-C20-T3 [business-rules] Implement error handling and messages
  - Show every message word for word; formatting rules may be restyled to the design system.
  - _Requirements: OATM-REQ-F-163, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170, OATM-REQ-F-167_
  - _Rules: OATM-BR-169, OATM-BR-175, OATM-BR-176, OATM-BR-177, OATM-BR-178_
  - _After: OATM-C20-T1_
- [ ] 4. OATM-C20-T4 [api] Build the services behind the screens
  - OATM-BR-167: Needs the highest existing transaction ID, taken as the last key in transaction-ID order (equivalent to a max query over transactions), so the new payment can be numbered one higher. Because two payments could otherwise get the same number, the new application should allocate IDs safely under concurrency, for example with a database sequence or a locked read of the max. It must still treat an empty transaction store as ID 0.
  - OATM-BR-174: After the payment transaction is written, the account read earlier for update must be saved with its current balance reduced by the payment amount. This needs a locked or version-checked update of that account by account ID, so that no change made in between is overwritten.
  - _Requirements: OATM-REQ-F-161_
  - _Rules: OATM-BR-167_
  - _After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3_
- [ ] 5. OATM-C20-T5 [ui-modernization] Build the screen Pay balance (S-BILL-PAY)
  - To the prototype: ui-reference/index.html#/S-BILL-PAY.
  - **summary card** "Balance to pay": When the balance is zero or less: 'You have nothing to pay...' and Pay balance is unavailable.
  - **primary button** "Pay balance": The dialog offers only Pay or Cancel, so no other value can be entered (legacy: 'Invalid value. Valid values are (Y/N)...'). If the card linked to the account is not found, nothing is paid and the message says so. The payment and the balance change are saved together or not at all.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170_
  - _Rules: OATM-BR-166, OATM-BR-167, OATM-BR-168, OATM-BR-169, OATM-BR-170, OATM-BR-171, OATM-BR-172, OATM-BR-173, OATM-BR-174, OATM-BR-175, OATM-BR-176, OATM-BR-177, OATM-BR-178_
  - _After: OATM-C20-T2, OATM-C20-T3, OATM-C20-T4_
- [ ] 6. OATM-C20-T6 [test-generation] Write a test for every acceptance criterion
  - 15 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170_
  - _Criteria: OATM-C20-AC-01, OATM-C20-AC-02, OATM-C20-AC-03, OATM-C20-AC-04, OATM-C20-AC-05, OATM-C20-AC-06, OATM-C20-AC-07, OATM-C20-AC-08, OATM-C20-AC-09, OATM-C20-AC-10, OATM-C20-AC-11, OATM-C20-AC-12, OATM-C20-AC-13, OATM-C20-AC-14, OATM-C20-AC-15_
  - _After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3, OATM-C20-T4, OATM-C20-T5_
- [ ] 7. OATM-C20-T7 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170_
  - _After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3, OATM-C20-T4, OATM-C20-T5_
