# Validate new transaction details (OATM-C32)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Checks every new transaction before it is saved. The eleven mandatory fields are checked in a fixed order, then numeric type, category and merchant codes, an amount in the form -99999999.99, and real calendar dates in the form YYYY-MM-DD. Only the first problem is reported, with its exact message and the cursor on that field. Nothing is saved until every check passes.

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

## Screens and components

### Add transaction (S-TRANSACTION-ADD)

Enter a transaction against an account or card, see what to fix at each field, confirm the summary and record it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-ADD`. Replaces the legacy screens COTRN2A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| New transaction | form | Fields are checked in screen order; the first field in error gets focus and its message; pre-filled when opened with a selected transaction |  |  | OATM-REQ-F-254, OATM-REQ-F-276 |
| Transaction type | select | Transaction type code and name | Required: 'Type CD can NOT be empty...'; numeric code: 'Type CD must be Numeric...'. |  | OATM-REQ-F-255, OATM-REQ-F-267 |
| Category | select | Category code and name for the chosen type | Required: 'Category CD can NOT be empty...'; numeric code: 'Category CD must be Numeric...'. |  | OATM-REQ-F-256, OATM-REQ-F-268 |
| Source | text |  | Required: 'Source can NOT be empty...'. |  | OATM-REQ-F-257 |
| Description | text |  | Required: 'Description can NOT be empty...'. |  | OATM-REQ-F-258 |
| Amount | money | Signed amount with 2 decimals | Required: 'Amount can NOT be empty...'; format: 'Amount should be in format -99999999.99'. |  | OATM-REQ-F-259, OATM-REQ-F-269, OATM-REQ-F-270 |
| Original date | date | YYYY-MM-DD | Required: 'Orig Date can NOT be empty...'; format: 'Orig Date should be in format YYYY-MM-DD'; real date: 'Orig Date - Not a valid date...'. |  | OATM-REQ-F-260, OATM-REQ-F-271, OATM-REQ-F-273 |
| Processed date | date | YYYY-MM-DD | Required: 'Proc Date can NOT be empty...'; format: 'Proc Date should be in format YYYY-MM-DD'; real date: 'Proc Date - Not a valid date...'. |  | OATM-REQ-F-261, OATM-REQ-F-272, OATM-REQ-F-274 |
| Merchant ID | text |  | Required: 'Merchant ID can NOT be empty...'; 9 digits: 'Merchant ID must be Numeric...'. |  | OATM-REQ-F-262, OATM-REQ-F-275 |
| Merchant name | text |  | Required: 'Merchant Name can NOT be empty...'. |  | OATM-REQ-F-263 |
| Merchant city | text |  | Required: 'Merchant City can NOT be empty...'. |  | OATM-REQ-F-264 |
| Merchant ZIP | text |  | Required: 'Merchant Zip can NOT be empty...'. |  | OATM-REQ-F-265 |


## Data models

#### CVACT03Y

File record of COTRN02C. Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVTRA05Y

File record of COTRN02C. Source: `app/cpy/CVTRA05Y.cpy`.

Record `TRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| TRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| TRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| TRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| TRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| TRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| TRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

- COCOM01Y (working storage of COTRN02C): see data-contracts.md.
- COTTL01Y (working storage of COTRN02C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN02C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN02C): see data-contracts.md.
- CVACT01Y (working storage of COTRN02C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-269 | Mandatory transaction fields and numeric code checks | business rule | WHEN Enter is pressed on the Add Transaction screen and the account or card number has passed its checks, THE Transaction Add screen SHALL check the transaction fields for blanks in this order: Type CD, Category CD, Source, Description, Amount, Orig Date, Proc Date, Merchant ID, Merchant Name, Merchant City, Merchant Zip, and report only the first blank field. | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-270 | Mandatory transaction fields and numeric code checks | business rule | WHEN a mandatory transaction field is blank (spaces or low-values), THE Transaction Add screen SHALL show that field's message, put the cursor on that field, redisplay the screen and save nothing. | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-271 | Reject missing transaction type code | business rule | WHEN the transaction type code is blank, THE Transaction Add screen SHALL show 'Type CD can NOT be empty...' with the cursor on the type code (TTYPCDI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-272 | Reject missing transaction category code | business rule | WHEN the type code is entered and the category code is blank, THE Transaction Add screen SHALL show 'Category CD can NOT be empty...' with the cursor on the category code (TCATCDI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-273 | Reject missing transaction source | business rule | WHEN the type and category codes are entered and the source is blank, THE Transaction Add screen SHALL show 'Source can NOT be empty...' with the cursor on the source (TRNSRCI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-274 | Reject missing transaction description | business rule | WHEN type, category and source are entered and the description is blank, THE Transaction Add screen SHALL show 'Description can NOT be empty...' with the cursor on the description (TDESCI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-275 | Reject missing transaction amount | business rule | WHEN type, category, source and description are entered and the amount is blank, THE Transaction Add screen SHALL show 'Amount can NOT be empty...' with the cursor on the amount (TRNAMTI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-276 | Reject missing origination date | business rule | WHEN all fields up to the amount are entered and the origination date is blank, THE Transaction Add screen SHALL show 'Orig Date can NOT be empty...' with the cursor on the origination date (TORIGDTI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-277 | Reject missing processing date | business rule | WHEN all fields up to the origination date are entered and the processing date is blank, THE Transaction Add screen SHALL show 'Proc Date can NOT be empty...' with the cursor on the processing date (TPROCDTI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-278 | Reject missing merchant identifier | business rule | WHEN all fields up to the processing date are entered and the merchant ID is blank, THE Transaction Add screen SHALL show 'Merchant ID can NOT be empty...' with the cursor on the merchant ID (MIDI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-279 | Reject missing merchant name | business rule | WHEN all fields up to the merchant ID are entered and the merchant name is blank, THE Transaction Add screen SHALL show 'Merchant Name can NOT be empty...' with the cursor on the merchant name (MNAMEI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-280 | Reject missing merchant city | business rule | WHEN all fields up to the merchant name are entered and the merchant city is blank, THE Transaction Add screen SHALL show 'Merchant City can NOT be empty...' with the cursor on the merchant city (MCITYI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-281 | Reject missing merchant zip code | business rule | WHEN all fields up to the merchant city are entered and the merchant zip is blank, THE Transaction Add screen SHALL show 'Merchant Zip can NOT be empty...' with the cursor on the merchant zip (MZIPI). | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-282 | Accept complete mandatory transaction fields | business rule | WHEN all eleven mandatory transaction fields are entered, THE Transaction Add screen SHALL pass the blank check and go on to the numeric and format checks. | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-283 | Require numeric type and category codes | business rule | WHEN the transaction type code is not numeric, THE Transaction Add screen SHALL show 'Type CD must be Numeric...' with the cursor on the type code and save nothing. | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-284 | Require numeric type and category codes | business rule | WHEN the type code is numeric and the category code is not numeric, THE Transaction Add screen SHALL show 'Category CD must be Numeric...' with the cursor on the category code and save nothing. | high | app/cbl/COTRN02C.cbl:163-166, app/cbl/COTRN02C.cbl:250-320, app/cbl/COTRN02C.cbl:322-337, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-285 | Validate transaction amount format | business rule | WHEN the amount entered on the Transaction Add screen does not start with '-' or '+', followed by eight digits, a '.', and two digits, THE Transaction Add screen SHALL reject it with 'Amount should be in format -99999999.99' and save nothing. | high | app/cbl/COTRN02C.cbl:339-351, app/cbl/COTRN02C.cbl:383-386, app/cbl/COTRN02C.cbl:456-458, app/cbl/COTRN02C.cbl:53-59 |
| OATM-BR-286 | Normalize entered transaction amount | design note | WHEN the amount passes the format check, THE Transaction Add screen SHALL convert it to a signed number with two decimals, show it back in the form +99999999.99, and store that value as the transaction amount when the transaction is added. | high | app/cbl/COTRN02C.cbl:339-351, app/cbl/COTRN02C.cbl:383-386, app/cbl/COTRN02C.cbl:456-458, app/cbl/COTRN02C.cbl:53-59 |
| OATM-BR-287 | Validate origination date format | business rule | WHEN the origination date entered on the Transaction Add screen is not in the form YYYY-MM-DD (four digits, '-', two digits, '-', two digits), THE Transaction Add screen SHALL reject the entry, show 'Orig Date should be in format YYYY-MM-DD' and save nothing. | high | app/cbl/COTRN02C.cbl:353-381, app/cbl/COTRN02C.cbl:389-427, app/cbl/COTRN02C.cbl:60, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-288 | Validate processing date format | business rule | WHEN the processing date entered on the Transaction Add screen is not in the form YYYY-MM-DD, THE Transaction Add screen SHALL reject the entry, show 'Proc Date should be in format YYYY-MM-DD' and save nothing. | high | app/cbl/COTRN02C.cbl:353-381, app/cbl/COTRN02C.cbl:389-427, app/cbl/COTRN02C.cbl:60, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-289 | Verify origination date is a real date | business rule | WHEN the origination date has the right form but the date-check service (CSUTLDTC) does not confirm it as a real calendar date (severity not '0000' and message number not '2513'), THE Transaction Add screen SHALL show 'Orig Date - Not a valid date...' and save nothing. | high | app/cbl/COTRN02C.cbl:353-381, app/cbl/COTRN02C.cbl:389-427, app/cbl/COTRN02C.cbl:60, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-290 | Verify processing date is a real date | business rule | WHEN the origination date is accepted but the date-check service (CSUTLDTC) does not confirm the processing date as a real calendar date (severity not '0000' and message number not '2513'), THE Transaction Add screen SHALL show 'Proc Date - Not a valid date...' and save nothing. | high | app/cbl/COTRN02C.cbl:353-381, app/cbl/COTRN02C.cbl:389-427, app/cbl/COTRN02C.cbl:60, app/cbl/COTRN02C.cbl:516-534 |
| OATM-BR-291 | Require numeric merchant identifier | business rule | WHEN all earlier checks pass and the Merchant ID is not entirely digits across its 9 positions, THE transaction add screen SHALL reject the entry, show 'Merchant ID must be Numeric...' and put the cursor on Merchant ID. | medium | app/cbl/COTRN02C.cbl:430-436, app/cpy-bms/COTRN02.CPY:114 |
| OATM-BR-292 | Verify processing date is a real date | business rule | THE Transaction Add screen SHALL stop at the first failed check and show only that message, so a later check (such as the processing date) is made only after every earlier check has passed. | high | app/cbl/COTRN02C.cbl:353-381, app/cbl/COTRN02C.cbl:389-427, app/cbl/COTRN02C.cbl:60, app/cbl/COTRN02C.cbl:516-534 |

### Worked examples

- OATM-BR-269: Type CD = blank; Merchant Zip = blank → Only 'Type CD can NOT be empty...' is shown
- OATM-BR-270: Type CD = 01; Category CD = blank; all other fields = filled in → 'Category CD can NOT be empty...' is shown, the cursor is on Category CD, and no transaction is added
- OATM-BR-271: Type CD = blank → 'Type CD can NOT be empty...'
- OATM-BR-272: Type CD = 01; Category CD = blank → 'Category CD can NOT be empty...'
- OATM-BR-273: Type CD = 01; Category CD = 0001; Source = blank → 'Source can NOT be empty...'
- OATM-BR-274: Source = POS TERM; Description = blank; Amount = blank → 'Description can NOT be empty...' (Description is checked before Amount)
- OATM-BR-275: Description = Grocery purchase; Amount = blank → 'Amount can NOT be empty...'
- OATM-BR-276: Amount = +00000050.00; Orig Date = blank → 'Orig Date can NOT be empty...'
- OATM-BR-277: Orig Date = 2026-11-20; Proc Date = blank → 'Proc Date can NOT be empty...'
- OATM-BR-278: Proc Date = 2026-11-21; Merchant ID = blank → 'Merchant ID can NOT be empty...'
- OATM-BR-279: Merchant ID = 800000001; Merchant Name = blank → 'Merchant Name can NOT be empty...'
- OATM-BR-280: Merchant Name = Corner Shop; Merchant City = blank → 'Merchant City can NOT be empty...'
- OATM-BR-281: Merchant City = Seattle; Merchant Zip = blank → 'Merchant Zip can NOT be empty...'
- OATM-BR-282: all eleven fields = filled in → No blank-field message; the type and category codes are checked next
- OATM-BR-283: Type CD = AB → 'Type CD must be Numeric...'
- OATM-BR-284: Type CD = 01; Category CD = 00X1 → 'Category CD must be Numeric...'
- OATM-BR-285: Amount = 125.50 → 'Amount should be in format -99999999.99' is shown and nothing is saved
- OATM-BR-285: Amount = +00000125.50 → The amount format check passes
- OATM-BR-286: Amount = +00000125.50; Confirm = Y → The transaction is stored with amount 125.50
- OATM-BR-286: Amount = -00000040.00; Confirm = Y → The transaction is stored with amount -40.00
- OATM-BR-287: Orig Date = 2024/03/01 → 'Orig Date should be in format YYYY-MM-DD' is shown and nothing is saved
- OATM-BR-287: Orig Date = 2024-03-01 → The format check passes
- OATM-BR-288: Orig Date = 2024-03-01; Proc Date = 03-01-2024 → 'Proc Date should be in format YYYY-MM-DD' is shown and nothing is saved
- OATM-BR-289: Orig Date = 2024-02-30; Proc Date = 2024-03-01 → 'Orig Date - Not a valid date...' is shown and nothing is saved
- OATM-BR-289: Orig Date = 2024-02-29; Proc Date = 2024-03-01 → The origination date is accepted
- OATM-BR-290: Orig Date = 2024-03-01; Proc Date = 2024-13-05 → 'Proc Date - Not a valid date...' is shown and nothing is saved
- OATM-BR-291: Merchant ID = ABC123456 → Rejected with 'Merchant ID must be Numeric...'
- OATM-BR-291: Merchant ID = 12345 (followed by 4 blanks) → Rejected with 'Merchant ID must be Numeric...'
- OATM-BR-291: Merchant ID = 123456789 → The check passes
- OATM-BR-292: Orig Date = 2024-02-30; Proc Date = 2024-99-99 → Only 'Orig Date - Not a valid date...' is shown

## Decision tables

#### First blank mandatory field

| First blank field in check order | Message and cursor | Rule |
|---|---|---|
| Type CD | 'Type CD can NOT be empty...', cursor on TTYPCDI | OATM-BR-271 |
| Category CD | 'Category CD can NOT be empty...', cursor on TCATCDI | OATM-BR-272 |
| Source | 'Source can NOT be empty...', cursor on TRNSRCI | OATM-BR-273 |
| Description | 'Description can NOT be empty...', cursor on TDESCI | OATM-BR-274 |
| Amount | 'Amount can NOT be empty...', cursor on TRNAMTI | OATM-BR-275 |
| Orig Date | 'Orig Date can NOT be empty...', cursor on TORIGDTI | OATM-BR-276 |
| Proc Date | 'Proc Date can NOT be empty...', cursor on TPROCDTI | OATM-BR-277 |
| Merchant ID | 'Merchant ID can NOT be empty...', cursor on MIDI | OATM-BR-278 |
| Merchant Name | 'Merchant Name can NOT be empty...', cursor on MNAMEI | OATM-BR-279 |
| Merchant City | 'Merchant City can NOT be empty...', cursor on MCITYI | OATM-BR-280 |
| Merchant Zip | 'Merchant Zip can NOT be empty...', cursor on MZIPI | OATM-BR-281 |
| none | Pass blank check; go on to numeric and format checks | OATM-BR-282 |

#### Date checks

| Orig Date form YYYY-MM-DD | Orig Date confirmed real by CSUTLDTC | Proc Date form YYYY-MM-DD | Proc Date confirmed real by CSUTLDTC | Result | Rule |
|---|---|---|---|---|---|
| no | - | - | - | 'Orig Date should be in format YYYY-MM-DD', save nothing | OATM-BR-287 |
| - | - | no | - | 'Proc Date should be in format YYYY-MM-DD', save nothing | OATM-BR-288 |
| yes | no | - | - | 'Orig Date - Not a valid date...', save nothing | OATM-BR-289 |
| yes | yes | - | no | 'Proc Date - Not a valid date...', save nothing | OATM-BR-290 |
| yes | no | no | - | **Gap:** Rules do not say whether the Proc Date format check runs before or after the Orig Date real-date check, so which single message is shown is not settled. | |
| yes | yes | yes | yes | **Gap:** No rule states the outcome when both dates pass apart from continuing to later checks (e.g. Merchant ID numeric); confirm the full check order. | |


## Design notes

- OATM-BR-286: Parse the validated amount text into an exact decimal with two places (never floating point). Echo it back to the user in the canonical form +99999999.99, and store exactly that decimal value as the transaction amount when the transaction is added.

## Open questions

- SME-176: When adding a transaction, the system accepts dates that the date check flags with message 2513 (outside the range the date utility supports). What does 2513 mean for the business, and should those dates still be accepted? Should the processing date also have to be on or after the origination date, and should future dates be refused? (Product owner) On OATM-BR-291, OATM-BR-285, OATM-BR-286, OATM-BR-284, OATM-BR-287, OATM-BR-288, OATM-BR-289, OATM-BR-292.
- DEF-053: Confirm this is deliberate: A date for which the date service returns message number '2513' (CEEDAYS feedback X'09D1' = 2513, 'Unsupp. Range', i.e. a year outside the supported range) is accepted as valid instead of rejected. (Subject-matter expert) On OATM-BR-287, OATM-BR-288, OATM-BR-289, OATM-BR-292.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (30 in all).
