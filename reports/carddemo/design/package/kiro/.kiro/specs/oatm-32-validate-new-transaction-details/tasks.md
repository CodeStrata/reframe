# Implementation plan: Validate new transaction details (OATM-C32)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

- [ ] 1. OATM-C32-T1 [data] Model the data the capability reads and writes
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
- [ ] 2. OATM-C32-T2 [business-rules] Implement the business rules
  - Keep each business rule exactly as specified.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
  - _Rules: OATM-BR-269, OATM-BR-270, OATM-BR-271, OATM-BR-272, OATM-BR-273, OATM-BR-274, OATM-BR-275, OATM-BR-276, OATM-BR-277, OATM-BR-278, OATM-BR-279, OATM-BR-280, OATM-BR-281, OATM-BR-282, OATM-BR-283, OATM-BR-284, OATM-BR-285, OATM-BR-287, OATM-BR-288, OATM-BR-289, OATM-BR-290, OATM-BR-291, OATM-BR-292_
  - _After: OATM-C32-T1_
- [ ] 3. OATM-C32-T3 [api] Build the services behind the screens
  - OATM-BR-286: Parse the accepted amount text into an exact signed decimal with two decimal places (no floating point), echo it back formatted as +99999999.99, and use that same parsed value as the stored transaction amount.
  - _Requirements: OATM-REQ-F-270_
  - _Rules: OATM-BR-286_
  - _After: OATM-C32-T1, OATM-C32-T2_
- [ ] 4. OATM-C32-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD)
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - **summary card** "Transaction details": Each is required, in the rule's words: 'Type CD can NOT be empty...', 'Category CD can NOT be empty...', 'Source can NOT be empty...', 'Description can NOT be empty...', 'Amount can NOT be empty...', 'Orig Date can NOT be empty...', 'Proc Date can NOT be empty...'. 'Type CD must be Numeric...', 'Category CD must be Numeric...'. 'Amount should be in format -99999999.99'. 'Orig Date should be in format YYYY-MM-DD', 'Proc Date should be in format YYYY-MM-DD', and 'Orig Date - Not a valid date...' / 'Proc Date - Not a valid date...' for a date not on the calendar. Every failing field shows its message under it.
  - **summary card** "Merchant": 'Merchant ID can NOT be empty...', 'Merchant Name can NOT be empty...', 'Merchant City can NOT be empty...', 'Merchant Zip can NOT be empty...'; 'Merchant ID must be Numeric...'.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
  - _Rules: OATM-BR-269, OATM-BR-270, OATM-BR-271, OATM-BR-272, OATM-BR-273, OATM-BR-274, OATM-BR-275, OATM-BR-276, OATM-BR-277, OATM-BR-278, OATM-BR-279, OATM-BR-280, OATM-BR-281, OATM-BR-282, OATM-BR-283, OATM-BR-284, OATM-BR-285, OATM-BR-286, OATM-BR-287, OATM-BR-288, OATM-BR-289, OATM-BR-290, OATM-BR-291, OATM-BR-292_
  - _After: OATM-C32-T2, OATM-C32-T3_
- [ ] 5. OATM-C32-T5 [test-generation] Write a test for every acceptance criterion
  - 30 acceptance criteria, each a test named by its ID.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
  - _Criteria: OATM-C32-AC-01, OATM-C32-AC-02, OATM-C32-AC-03, OATM-C32-AC-04, OATM-C32-AC-05, OATM-C32-AC-06, OATM-C32-AC-07, OATM-C32-AC-08, OATM-C32-AC-09, OATM-C32-AC-10, OATM-C32-AC-11, OATM-C32-AC-12, OATM-C32-AC-13, OATM-C32-AC-14, OATM-C32-AC-15, OATM-C32-AC-16, OATM-C32-AC-17, OATM-C32-AC-18, OATM-C32-AC-19, OATM-C32-AC-20, OATM-C32-AC-21, OATM-C32-AC-22, OATM-C32-AC-23, OATM-C32-AC-24, OATM-C32-AC-25, OATM-C32-AC-26, OATM-C32-AC-27, OATM-C32-AC-28, OATM-C32-AC-29, OATM-C32-AC-30_
  - _After: OATM-C32-T1, OATM-C32-T2, OATM-C32-T3, OATM-C32-T4_
- [ ] 6. OATM-C32-T6 [compliance] Review the handling of card data, money
  - Check storage, logs, screens and audit against the rules.
  - _Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276_
  - _After: OATM-C32-T1, OATM-C32-T2, OATM-C32-T3, OATM-C32-T4_
