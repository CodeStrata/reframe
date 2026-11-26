# Implementation plan: Validate new transaction details (OATM-C32)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

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


## Data model

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

## Design notes

- OATM-BR-286: Parse the validated amount text into an exact decimal with two places (never floating point). Echo it back to the user in the canonical form +99999999.99, and store exactly that decimal value as the transaction amount when the transaction is added.

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

