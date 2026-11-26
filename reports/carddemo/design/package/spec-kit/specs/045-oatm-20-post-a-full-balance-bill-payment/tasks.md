# Tasks: Post a full-balance bill payment (OATM-C20)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C20-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170.
  - File records: CVACT01Y, CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y.
- [ ] OATM-C20-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-160, OATM-REQ-F-162, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166. Rules: OATM-BR-166, OATM-BR-168, OATM-BR-170, OATM-BR-171, OATM-BR-172, OATM-BR-173, OATM-BR-174. After: OATM-C20-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C20-T3 [business-rules] Implement error handling and messages. Requirements: OATM-REQ-F-163, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170, OATM-REQ-F-167. Rules: OATM-BR-169, OATM-BR-175, OATM-BR-176, OATM-BR-177, OATM-BR-178. After: OATM-C20-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] OATM-C20-T4 [api] Build the services behind the screens. Requirements: OATM-REQ-F-161. Rules: OATM-BR-167. After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3.
  - OATM-BR-167: Needs the highest existing transaction ID (a 'max ID' query or a descending keyed read of the last record). When there are no transactions it returns zero. Because 'highest plus 1' can race between concurrent payments, the new application should use a database sequence or an atomic ID generator, with the unique key as a safety net.
  - OATM-BR-174: After the payment transaction is written, the account read for update earlier is saved with its reduced current balance. This should be an update on the same locked or version-checked account row. Ideally it runs in the same database transaction as the payment insert, so the balance and the payment record cannot disagree (subject to the decision on the non-atomic legacy behaviour).
- [ ] OATM-C20-T5 [ui-modernization] Build the screen Pay balance (S-BILL-PAY). Requirements: OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-169. Rules: OATM-BR-170, OATM-BR-171, OATM-BR-172, OATM-BR-173, OATM-BR-174, OATM-BR-175, OATM-BR-177. After: OATM-C20-T2, OATM-C20-T3, OATM-C20-T4.
  - To the prototype: ui-reference/index.html#/S-BILL-PAY.
  - button "Pay full balance"
  - message "Payment result"
- [ ] OATM-C20-T6 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170. Criteria: OATM-C20-AC-01, OATM-C20-AC-02, OATM-C20-AC-03, OATM-C20-AC-04, OATM-C20-AC-05, OATM-C20-AC-06, OATM-C20-AC-07, OATM-C20-AC-08, OATM-C20-AC-09, OATM-C20-AC-10, OATM-C20-AC-11, OATM-C20-AC-12, OATM-C20-AC-13, OATM-C20-AC-14, OATM-C20-AC-15. After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3, OATM-C20-T4, OATM-C20-T5.
  - 15 acceptance criteria, each a test named by its ID.
- [ ] OATM-C20-T7 [compliance] Review the handling of card data, money. Requirements: OATM-REQ-F-160, OATM-REQ-F-161, OATM-REQ-F-162, OATM-REQ-F-163, OATM-REQ-F-164, OATM-REQ-F-165, OATM-REQ-F-166, OATM-REQ-F-167, OATM-REQ-F-168, OATM-REQ-F-169, OATM-REQ-F-170. After: OATM-C20-T1, OATM-C20-T2, OATM-C20-T3, OATM-C20-T4, OATM-C20-T5.
  - Check storage, logs, screens and audit against the rules.
