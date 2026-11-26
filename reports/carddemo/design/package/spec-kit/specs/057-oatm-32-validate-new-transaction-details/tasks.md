# Tasks: Validate new transaction details (OATM-C32)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] OATM-C32-T1 [data] Model the data the capability reads and writes. Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276.
  - File records: CVACT03Y, CVTRA05Y (see data-contracts.md).
  - Working records it passes or builds: COCOM01Y, COTTL01Y, CSDAT01Y, CSMSG01Y, CVACT01Y.
- [ ] OATM-C32-T2 [business-rules] Implement the business rules. Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276. Rules: OATM-BR-269, OATM-BR-270, OATM-BR-271, OATM-BR-272, OATM-BR-273, OATM-BR-274, OATM-BR-275, OATM-BR-276, OATM-BR-277, OATM-BR-278, OATM-BR-279, OATM-BR-280, OATM-BR-281, OATM-BR-282, OATM-BR-283, OATM-BR-284, OATM-BR-285, OATM-BR-287, OATM-BR-288, OATM-BR-289, OATM-BR-290, OATM-BR-291, OATM-BR-292. After: OATM-C32-T1.
  - Keep each business rule exactly as specified.
- [ ] OATM-C32-T3 [api] Build the services behind the screens. Requirements: OATM-REQ-F-270. Rules: OATM-BR-286. After: OATM-C32-T1, OATM-C32-T2.
  - OATM-BR-286: Parse the validated amount text into an exact decimal with two places (never floating point). Echo it back to the user in the canonical form +99999999.99, and store exactly that decimal value as the transaction amount when the transaction is added.
- [ ] OATM-C32-T4 [ui-modernization] Build the screen Add transaction (S-TRANSACTION-ADD). Requirements: OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276. Rules: OATM-BR-270, OATM-BR-271, OATM-BR-272, OATM-BR-273, OATM-BR-274, OATM-BR-275, OATM-BR-276, OATM-BR-277, OATM-BR-278, OATM-BR-279, OATM-BR-280, OATM-BR-281, OATM-BR-283, OATM-BR-284, OATM-BR-285, OATM-BR-286, OATM-BR-287, OATM-BR-288, OATM-BR-289, OATM-BR-290, OATM-BR-291, OATM-BR-292. After: OATM-C32-T2, OATM-C32-T3.
  - To the prototype: ui-reference/index.html#/S-TRANSACTION-ADD.
  - form "New transaction"
  - select "Transaction type": Required: 'Type CD can NOT be empty...'; numeric code: 'Type CD must be Numeric...'.
  - select "Category": Required: 'Category CD can NOT be empty...'; numeric code: 'Category CD must be Numeric...'.
  - text "Source": Required: 'Source can NOT be empty...'.
  - text "Description": Required: 'Description can NOT be empty...'.
  - money "Amount": Required: 'Amount can NOT be empty...'; format: 'Amount should be in format -99999999.99'.
  - date "Original date": Required: 'Orig Date can NOT be empty...'; format: 'Orig Date should be in format YYYY-MM-DD'; real date: 'Orig Date - Not a valid date...'.
  - date "Processed date": Required: 'Proc Date can NOT be empty...'; format: 'Proc Date should be in format YYYY-MM-DD'; real date: 'Proc Date - Not a valid date...'.
  - text "Merchant ID": Required: 'Merchant ID can NOT be empty...'; 9 digits: 'Merchant ID must be Numeric...'.
  - text "Merchant name": Required: 'Merchant Name can NOT be empty...'.
  - text "Merchant city": Required: 'Merchant City can NOT be empty...'.
  - text "Merchant ZIP": Required: 'Merchant Zip can NOT be empty...'.
- [ ] OATM-C32-T5 [test-generation] Write a test for every acceptance criterion. Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276. Criteria: OATM-C32-AC-01, OATM-C32-AC-02, OATM-C32-AC-03, OATM-C32-AC-04, OATM-C32-AC-05, OATM-C32-AC-06, OATM-C32-AC-07, OATM-C32-AC-08, OATM-C32-AC-09, OATM-C32-AC-10, OATM-C32-AC-11, OATM-C32-AC-12, OATM-C32-AC-13, OATM-C32-AC-14, OATM-C32-AC-15, OATM-C32-AC-16, OATM-C32-AC-17, OATM-C32-AC-18, OATM-C32-AC-19, OATM-C32-AC-20, OATM-C32-AC-21, OATM-C32-AC-22, OATM-C32-AC-23, OATM-C32-AC-24, OATM-C32-AC-25, OATM-C32-AC-26, OATM-C32-AC-27, OATM-C32-AC-28, OATM-C32-AC-29, OATM-C32-AC-30. After: OATM-C32-T1, OATM-C32-T2, OATM-C32-T3, OATM-C32-T4.
  - 30 acceptance criteria, each a test named by its ID.
- [ ] OATM-C32-T6 [compliance] Review the handling of card data, money. Requirements: OATM-REQ-F-253, OATM-REQ-F-254, OATM-REQ-F-255, OATM-REQ-F-256, OATM-REQ-F-257, OATM-REQ-F-258, OATM-REQ-F-259, OATM-REQ-F-260, OATM-REQ-F-261, OATM-REQ-F-262, OATM-REQ-F-263, OATM-REQ-F-264, OATM-REQ-F-265, OATM-REQ-F-266, OATM-REQ-F-267, OATM-REQ-F-268, OATM-REQ-F-269, OATM-REQ-F-270, OATM-REQ-F-271, OATM-REQ-F-272, OATM-REQ-F-273, OATM-REQ-F-274, OATM-REQ-F-275, OATM-REQ-F-276. After: OATM-C32-T1, OATM-C32-T2, OATM-C32-T3, OATM-C32-T4.
  - Check storage, logs, screens and audit against the rules.
