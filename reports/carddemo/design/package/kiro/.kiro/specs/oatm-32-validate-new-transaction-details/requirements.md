# Requirements: Validate new transaction details (OATM-C32)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Checks every field of a new transaction in a fixed order: the eleven mandatory fields, numeric type and category codes, the amount format -99999999.99, real YYYY-MM-DD origination and processing dates, and a numeric merchant ID. It stops at the first problem and shows only that field's message. Nothing may be saved while any check fails.

**User story:** As a staff user, I want every new transaction's fields checked for presence, numeric codes, amount format and real dates, with one clear message for the first problem, so that only complete and well-formed transactions are recorded.

## Requirements

### Requirement 1: OATM-REQ-F-253 (business rule)

#### Acceptance criteria

1. When Enter is pressed on the Add Transaction screen and the account or card number has passed its checks, the system shall check the transaction fields for blanks in this order: Type CD, Category CD, Source, Description, Amount, Orig Date, Proc Date, Merchant ID, Merchant Name, Merchant City, Merchant Zip, and report only the first blank field. (rules OATM-BR-269)
2. GIVEN Type CD: blank; Merchant Zip: blank WHEN Enter is pressed on the Add Transaction screen and the account or card number has passed its checks THEN Only 'Type CD can NOT be empty...' is shown (OATM-C32-AC-01; OATM-BR-269)

### Requirement 2: OATM-REQ-F-254 (business rule)

#### Acceptance criteria

1. If a mandatory transaction field is blank (spaces or low-values), then the system shall show that field's message, put the cursor on that field, redisplay the screen and save nothing. (rules OATM-BR-270)
2. GIVEN Type CD: 01; Category CD: blank; all other fields: filled in WHEN a mandatory transaction field is blank (spaces or low-values) THEN 'Category CD can NOT be empty...' is shown, the cursor is on Category CD, and no transaction is added (OATM-C32-AC-02; OATM-BR-270)

### Requirement 3: OATM-REQ-F-255 (business rule)

#### Acceptance criteria

1. If the transaction type code is blank, then the system shall show 'Type CD can NOT be empty...' with the cursor on the type code (TTYPCDI). (rules OATM-BR-271)
2. GIVEN Type CD: blank WHEN the transaction type code is blank THEN 'Type CD can NOT be empty...' (OATM-C32-AC-03; OATM-BR-271)

### Requirement 4: OATM-REQ-F-256 (business rule)

#### Acceptance criteria

1. If the type code is entered and the category code is blank, then the system shall show 'Category CD can NOT be empty...' with the cursor on the category code (TCATCDI). (rules OATM-BR-272)
2. GIVEN Type CD: 01; Category CD: blank WHEN the type code is entered and the category code is blank THEN 'Category CD can NOT be empty...' (OATM-C32-AC-04; OATM-BR-272)

### Requirement 5: OATM-REQ-F-257 (business rule)

#### Acceptance criteria

1. If the type and category codes are entered and the source is blank, then the system shall show 'Source can NOT be empty...' with the cursor on the source (TRNSRCI). (rules OATM-BR-273)
2. GIVEN Type CD: 01; Category CD: 0001; Source: blank WHEN the type and category codes are entered and the source is blank THEN 'Source can NOT be empty...' (OATM-C32-AC-05; OATM-BR-273)

### Requirement 6: OATM-REQ-F-258 (business rule)

#### Acceptance criteria

1. If type, category and source are entered and the description is blank, then the system shall show 'Description can NOT be empty...' with the cursor on the description (TDESCI). (rules OATM-BR-274)
2. GIVEN Source: POS TERM; Description: blank; Amount: blank WHEN type, category and source are entered and the description is blank THEN 'Description can NOT be empty...' (Description is checked before Amount) (OATM-C32-AC-06; OATM-BR-274)

### Requirement 7: OATM-REQ-F-259 (business rule)

#### Acceptance criteria

1. If type, category, source and description are entered and the amount is blank, then the system shall show 'Amount can NOT be empty...' with the cursor on the amount (TRNAMTI). (rules OATM-BR-275)
2. GIVEN Description: Grocery purchase; Amount: blank WHEN type, category, source and description are entered and the amount is blank THEN 'Amount can NOT be empty...' (OATM-C32-AC-07; OATM-BR-275)

### Requirement 8: OATM-REQ-F-260 (business rule)

#### Acceptance criteria

1. If all fields up to the amount are entered and the origination date is blank, then the system shall show 'Orig Date can NOT be empty...' with the cursor on the origination date (TORIGDTI). (rules OATM-BR-276)
2. GIVEN Amount: +00000050.00; Orig Date: blank WHEN all fields up to the amount are entered and the origination date is blank THEN 'Orig Date can NOT be empty...' (OATM-C32-AC-08; OATM-BR-276)

### Requirement 9: OATM-REQ-F-261 (business rule)

#### Acceptance criteria

1. If all fields up to the origination date are entered and the processing date is blank, then the system shall show 'Proc Date can NOT be empty...' with the cursor on the processing date (TPROCDTI). (rules OATM-BR-277)
2. GIVEN Orig Date: 2026-11-20; Proc Date: blank WHEN all fields up to the origination date are entered and the processing date is blank THEN 'Proc Date can NOT be empty...' (OATM-C32-AC-09; OATM-BR-277)

### Requirement 10: OATM-REQ-F-262 (business rule)

#### Acceptance criteria

1. If all fields up to the processing date are entered and the merchant ID is blank, then the system shall show 'Merchant ID can NOT be empty...' with the cursor on the merchant ID (MIDI). (rules OATM-BR-278)
2. GIVEN Proc Date: 2026-11-21; Merchant ID: blank WHEN all fields up to the processing date are entered and the merchant ID is blank THEN 'Merchant ID can NOT be empty...' (OATM-C32-AC-10; OATM-BR-278)

### Requirement 11: OATM-REQ-F-263 (business rule)

#### Acceptance criteria

1. If all fields up to the merchant ID are entered and the merchant name is blank, then the system shall show 'Merchant Name can NOT be empty...' with the cursor on the merchant name (MNAMEI). (rules OATM-BR-279)
2. GIVEN Merchant ID: 800000001; Merchant Name: blank WHEN all fields up to the merchant ID are entered and the merchant name is blank THEN 'Merchant Name can NOT be empty...' (OATM-C32-AC-11; OATM-BR-279)

### Requirement 12: OATM-REQ-F-264 (business rule)

#### Acceptance criteria

1. If all fields up to the merchant name are entered and the merchant city is blank, then the system shall show 'Merchant City can NOT be empty...' with the cursor on the merchant city (MCITYI). (rules OATM-BR-280)
2. GIVEN Merchant Name: Corner Shop; Merchant City: blank WHEN all fields up to the merchant name are entered and the merchant city is blank THEN 'Merchant City can NOT be empty...' (OATM-C32-AC-12; OATM-BR-280)

### Requirement 13: OATM-REQ-F-265 (business rule)

#### Acceptance criteria

1. If all fields up to the merchant city are entered and the merchant zip is blank, then the system shall show 'Merchant Zip can NOT be empty...' with the cursor on the merchant zip (MZIPI). (rules OATM-BR-281)
2. GIVEN Merchant City: Seattle; Merchant Zip: blank WHEN all fields up to the merchant city are entered and the merchant zip is blank THEN 'Merchant Zip can NOT be empty...' (OATM-C32-AC-13; OATM-BR-281)

### Requirement 14: OATM-REQ-F-266 (business rule)

#### Acceptance criteria

1. When all eleven mandatory transaction fields are entered, the system shall pass the blank check and go on to the numeric and format checks. (rules OATM-BR-282)
2. GIVEN all eleven fields: filled in WHEN all eleven mandatory transaction fields are entered THEN No blank-field message; the type and category codes are checked next (OATM-C32-AC-14; OATM-BR-282)

### Requirement 15: OATM-REQ-F-267 (business rule)

#### Acceptance criteria

1. If the transaction type code is not numeric, then the system shall show 'Type CD must be Numeric...' with the cursor on the type code and save nothing. (rules OATM-BR-283)
2. GIVEN Type CD: AB WHEN the transaction type code is not numeric THEN 'Type CD must be Numeric...' (OATM-C32-AC-15; OATM-BR-283)

### Requirement 16: OATM-REQ-F-268 (business rule)

#### Acceptance criteria

1. If the type code is numeric and the category code is not numeric, then the system shall show 'Category CD must be Numeric...' with the cursor on the category code and save nothing. (rules OATM-BR-284)
2. GIVEN Type CD: 01; Category CD: 00X1 WHEN the type code is numeric and the category code is not numeric THEN 'Category CD must be Numeric...' (OATM-C32-AC-16; OATM-BR-284)

### Requirement 17: OATM-REQ-F-269 (business rule)

#### Acceptance criteria

1. If the amount entered does not start with '-' or '+', followed by eight digits, a '.', and two digits, then the system shall reject it with 'Amount should be in format -99999999.99' and save nothing. (rules OATM-BR-285)
2. GIVEN Amount: 125.50 WHEN the amount entered on the Transaction Add screen does not start with '-' or '+', followed by eight digits, a '.', and two digits THEN 'Amount should be in format -99999999.99' is shown and nothing is saved (OATM-C32-AC-17; OATM-BR-285)
3. GIVEN Amount: +00000125.50 WHEN the amount entered on the Transaction Add screen does not start with '-' or '+', followed by eight digits, a '.', and two digits THEN The amount format check passes (OATM-C32-AC-18; OATM-BR-285)

### Requirement 18: OATM-REQ-F-270 (design note)

#### Acceptance criteria

1. When the amount passes the format check, the system shall convert it to a signed number with two decimals, show it back in the form +99999999.99, and store that value as the transaction amount when the transaction is added. (rules OATM-BR-286)
2. GIVEN Amount: +00000125.50; Confirm: Y WHEN the amount passes the format check THEN The transaction is stored with amount 125.50 (OATM-C32-AC-19; OATM-BR-286)
3. GIVEN Amount: -00000040.00; Confirm: Y WHEN the amount passes the format check THEN The transaction is stored with amount -40.00 (OATM-C32-AC-20; OATM-BR-286)

### Requirement 19: OATM-REQ-F-271 (business rule)

#### Acceptance criteria

1. If the origination date is not in the form YYYY-MM-DD (four digits, '-', two digits, '-', two digits), then the system shall reject the entry, show 'Orig Date should be in format YYYY-MM-DD' and save nothing. (rules OATM-BR-287)
2. GIVEN Orig Date: 2024/03/01 WHEN the origination date entered on the Transaction Add screen is not in the form YYYY-MM-DD (four digits, '-', two digits, '-', two digits) THEN 'Orig Date should be in format YYYY-MM-DD' is shown and nothing is saved (OATM-C32-AC-21; OATM-BR-287)
3. GIVEN Orig Date: 2024-03-01 WHEN the origination date entered on the Transaction Add screen is not in the form YYYY-MM-DD (four digits, '-', two digits, '-', two digits) THEN The format check passes (OATM-C32-AC-22; OATM-BR-287)

### Requirement 20: OATM-REQ-F-272 (business rule)

#### Acceptance criteria

1. If the processing date is not in the form YYYY-MM-DD, then the system shall reject the entry, show 'Proc Date should be in format YYYY-MM-DD' and save nothing. (rules OATM-BR-288)
2. GIVEN Orig Date: 2024-03-01; Proc Date: 03-01-2024 WHEN the processing date entered on the Transaction Add screen is not in the form YYYY-MM-DD THEN 'Proc Date should be in format YYYY-MM-DD' is shown and nothing is saved (OATM-C32-AC-23; OATM-BR-288)

### Requirement 21: OATM-REQ-F-273 (business rule)

#### Acceptance criteria

1. If the origination date has the right form but the date-check service (CSUTLDTC) does not confirm it as a real calendar date (severity not '0000' and message number not '2513'), then the system shall show 'Orig Date - Not a valid date...' and save nothing. (rules OATM-BR-289)
2. GIVEN Orig Date: 2024-02-30; Proc Date: 2024-03-01 WHEN the origination date has the right form but the date-check service (CSUTLDTC) does not confirm it as a real calendar date (severity not '0000' and message number not '2513') THEN 'Orig Date - Not a valid date...' is shown and nothing is saved (OATM-C32-AC-24; OATM-BR-289)
3. GIVEN Orig Date: 2024-02-29; Proc Date: 2024-03-01 WHEN the origination date has the right form but the date-check service (CSUTLDTC) does not confirm it as a real calendar date (severity not '0000' and message number not '2513') THEN The origination date is accepted (OATM-C32-AC-25; OATM-BR-289)

### Requirement 22: OATM-REQ-F-274 (business rule)

#### Acceptance criteria

1. If the origination date is accepted but the date-check service (CSUTLDTC) does not confirm the processing date as a real calendar date (severity not '0000' and message number not '2513'), then the system shall show 'Proc Date - Not a valid date...' and save nothing. (rules OATM-BR-290)
2. GIVEN Orig Date: 2024-03-01; Proc Date: 2024-13-05 WHEN the origination date is accepted but the date-check service (CSUTLDTC) does not confirm the processing date as a real calendar date (severity not '0000' and message number not '2513') THEN 'Proc Date - Not a valid date...' is shown and nothing is saved (OATM-C32-AC-26; OATM-BR-290)

### Requirement 23: OATM-REQ-F-275 (business rule)

#### Acceptance criteria

1. If all earlier checks pass and the Merchant ID is not entirely digits across its 9 positions, then the system shall reject the entry, show 'Merchant ID must be Numeric...' and put the cursor on Merchant ID. (rules OATM-BR-291)
2. GIVEN Merchant ID: ABC123456 WHEN all earlier checks pass and the Merchant ID is not entirely digits across its 9 positions THEN Rejected with 'Merchant ID must be Numeric...' (OATM-C32-AC-27; OATM-BR-291)
3. GIVEN Merchant ID: 12345 (followed by 4 blanks) WHEN all earlier checks pass and the Merchant ID is not entirely digits across its 9 positions THEN Rejected with 'Merchant ID must be Numeric...' (OATM-C32-AC-28; OATM-BR-291)
4. GIVEN Merchant ID: 123456789 WHEN all earlier checks pass and the Merchant ID is not entirely digits across its 9 positions THEN The check passes (OATM-C32-AC-29; OATM-BR-291)

### Requirement 24: OATM-REQ-F-276 (business rule)

#### Acceptance criteria

1. The system shall stop the Transaction Add checks at the first failed check and show only that message, so a later check is made only after every earlier check has passed. (rules OATM-BR-292)
2. GIVEN Orig Date: 2024-02-30; Proc Date: 2024-99-99 WHEN Transaction Add screen runs THEN Only 'Orig Date - Not a valid date...' is shown (OATM-C32-AC-30; OATM-BR-292)
