# Replace the customer's record in the customer file (CRCM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as service · risk high

## Introduction

Keeps the customer file in line with a customer update by replacing the customer's whole stored record with the updated data, found by customer number and locked while it is changed. If the record cannot be read for update, including when the customer is not on the file, the service returns '81'. If the rewrite fails, it returns '82'. Both failures are logged and stop processing, and it must never apply a partial update.

**User story:** As a customer service user, I want a customer update to also replace the customer's record in the customer file, so that the customer file matches the updated details.

## Requirements

### Requirement 1: CRCM-REQ-F-027 (business rule)

#### Acceptance criteria

1. When a customer update reaches the customer file step, the system shall read the customer's record in the customer file (KSDSCUST) by the 10-digit customer number, lock it for update, and replace the whole stored record with the 225 bytes of customer data from the request. (rules CRCM-BR-035)
2. GIVEN The customer file KSDSCUST holds a record for customer number 0000001234 with last name 'SMITH', and a customer update for 0000001234 carries 225 bytes of customer data with last name 'JONES' WHEN The customer update reaches the customer file step THEN The record for 0000001234 is read by its 10-digit customer number and locked for update, and the whole stored record is replaced with the 225 bytes from the request, so the stored last name is 'JONES' and every other field matches the request (CRCM-C07-AC-03; CRCM-BR-035)

### Requirement 2: CRCM-REQ-F-028 (error handling)

#### Acceptance criteria

1. If the customer record cannot be read for update for any reason, including the customer not being on the file, then the system shall set return code '81', write an error message with date, time, customer number and response codes to the error queue, and end the task abnormally with code 'LGV1'. (rules CRCM-BR-036)
2. GIVEN customer number: 0001000099; customer on file: no WHEN the customer record cannot be read for update for any reason, including the customer not being on the file THEN Return code '81', error message logged, task abends with 'LGV1'; nothing is rewritten. (CRCM-C07-AC-01; CRCM-BR-036)

### Requirement 3: CRCM-REQ-F-029 (error handling)

#### Acceptance criteria

1. If rewriting the locked customer record fails, then the system shall set return code '82', write an error message with date, time, customer number and response codes to the error queue, and end the task abnormally with code 'LGV2'. (rules CRCM-BR-037)
2. GIVEN customer number: 0001000042; rewrite result: failed WHEN rewriting the locked customer record fails THEN Return code '82', error message logged, task abends with 'LGV2'. (CRCM-C07-AC-02; CRCM-BR-037)

## Screens and components

No screens: it runs as service.

## Data models

#### LGCMAREA

File record of LGUCVS01. Source: `base/src/lgcmarea.cpy`.

Record `CA-REQUEST-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CA-REQUEST-ID |  | X(6) | text, 6 characters |  |  |  |

Record `CA-RETURN-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CA-RETURN-CODE |  | 9(2) | unsigned integer, 2 digits (zoned decimal) |  |  |  |

Record `CA-CUSTOMER-NUM`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CA-CUSTOMER-NUM |  | 9(10) | unsigned integer, 10 digits (zoned decimal) |  |  |  |

Record `CA-REQUEST-SPECIFIC`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CA-REQUEST-SPECIFIC |  | X(32482) | text, 32482 characters |  |  |  |

Record `CA-CUSTOMER-REQUEST`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CA-FIRST-NAME |  | X(10) | text, 10 characters |  |  |  |
| CA-LAST-NAME |  | X(20) | text, 20 characters |  |  |  |
| CA-DOB |  | X(10) | text, 10 characters |  |  |  |
| CA-HOUSE-NAME |  | X(20) | text, 20 characters |  |  |  |
| CA-HOUSE-NUM |  | X(4) | text, 4 characters |  |  |  |
| CA-POSTCODE |  | X(8) | text, 8 characters |  |  |  |
| CA-NUM-POLICIES |  | 9(3) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| CA-PHONE-MOBILE |  | X(20) | text, 20 characters |  |  |  |
| CA-PHONE-HOME |  | X(20) | text, 20 characters |  |  |  |
| CA-EMAIL-ADDRESS |  | X(100) | text, 100 characters |  |  |  |
| CA-POLICY-DATA |  | X(32267) | text, 32267 characters |  |  |  |

Record `CA-CUSTSECR-REQUEST`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CA-CUSTSECR-PASS |  | X(32) | text, 32 characters |  |  |  |
| CA-CUSTSECR-COUNT |  | X(4) | text, 4 characters |  |  |  |
| CA-CUSTSECR-STATE |  | X | text, 1 character |  |  |  |
| CA-CUSTSECR-DATA |  | X(32445) | text, 32445 characters |  |  |  |

Record `CA-POLICY-REQUEST`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CA-POLICY-NUM |  | 9(10) | unsigned integer, 10 digits (zoned decimal) |  |  |  |
| CA-POLICY-COMMON |  |  | group |  |  |  |
| CA-ISSUE-DATE | CA-POLICY-COMMON | X(10) | text, 10 characters |  |  |  |
| CA-EXPIRY-DATE | CA-POLICY-COMMON | X(10) | text, 10 characters |  |  |  |
| CA-LASTCHANGED | CA-POLICY-COMMON | X(26) | text, 26 characters |  |  |  |
| CA-BROKERID | CA-POLICY-COMMON | 9(10) | unsigned integer, 10 digits (zoned decimal) |  |  |  |
| CA-BROKERSREF | CA-POLICY-COMMON | X(10) | text, 10 characters |  |  |  |
| CA-PAYMENT | CA-POLICY-COMMON | 9(6) | unsigned integer, 6 digits (zoned decimal) |  |  |  |
| CA-POLICY-SPECIFIC |  | X(32400) | text, 32400 characters |  |  |  |
| CA-ENDOWMENT |  |  | group |  |  | redefines CA-POLICY-SPECIFIC |
| CA-E-WITH-PROFITS | CA-ENDOWMENT | X | text, 1 character |  |  |  |
| CA-E-EQUITIES | CA-ENDOWMENT | X | text, 1 character |  |  |  |
| CA-E-MANAGED-FUND | CA-ENDOWMENT | X | text, 1 character |  |  |  |
| CA-E-FUND-NAME | CA-ENDOWMENT | X(10) | text, 10 characters |  |  |  |
| CA-E-TERM | CA-ENDOWMENT | 99 | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| CA-E-SUM-ASSURED | CA-ENDOWMENT | 9(6) | unsigned integer, 6 digits (zoned decimal) |  |  |  |
| CA-E-LIFE-ASSURED | CA-ENDOWMENT | X(31) | text, 31 characters |  |  |  |
| CA-E-PADDING-DATA | CA-ENDOWMENT | X(32348) | text, 32348 characters |  |  |  |
| CA-HOUSE |  |  | group |  |  | redefines CA-POLICY-SPECIFIC |
| CA-H-PROPERTY-TYPE | CA-HOUSE | X(15) | text, 15 characters |  |  |  |
| CA-H-BEDROOMS | CA-HOUSE | 9(3) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| CA-H-VALUE | CA-HOUSE | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  |  |
| CA-H-HOUSE-NAME | CA-HOUSE | X(20) | text, 20 characters |  |  |  |
| CA-H-HOUSE-NUMBER | CA-HOUSE | X(4) | text, 4 characters |  |  |  |
| CA-H-POSTCODE | CA-HOUSE | X(8) | text, 8 characters |  |  |  |
| CA-H-FILLER | CA-HOUSE | X(32342) | text, 32342 characters |  |  |  |
| CA-MOTOR |  |  | group |  |  | redefines CA-POLICY-SPECIFIC |
| CA-M-MAKE | CA-MOTOR | X(15) | text, 15 characters |  |  |  |
| CA-M-MODEL | CA-MOTOR | X(15) | text, 15 characters |  |  |  |
| CA-M-VALUE | CA-MOTOR | 9(6) | unsigned integer, 6 digits (zoned decimal) |  |  |  |
| CA-M-REGNUMBER | CA-MOTOR | X(7) | text, 7 characters |  |  |  |
| CA-M-COLOUR | CA-MOTOR | X(8) | text, 8 characters |  |  |  |
| CA-M-CC | CA-MOTOR | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| CA-M-MANUFACTURED | CA-MOTOR | X(10) | text, 10 characters |  |  |  |
| CA-M-PREMIUM | CA-MOTOR | 9(6) | unsigned integer, 6 digits (zoned decimal) |  |  |  |
| CA-M-ACCIDENTS | CA-MOTOR | 9(6) | unsigned integer, 6 digits (zoned decimal) |  |  |  |
| CA-M-FILLER | CA-MOTOR | X(32323) | text, 32323 characters |  |  |  |
| CA-COMMERCIAL |  |  | group |  |  | redefines CA-POLICY-SPECIFIC |
| CA-B-ADDRESS | CA-COMMERCIAL | X(255) | text, 255 characters |  |  |  |
| CA-B-POSTCODE | CA-COMMERCIAL | X(8) | text, 8 characters |  |  |  |
| CA-B-LATITUDE | CA-COMMERCIAL | X(11) | text, 11 characters |  |  |  |
| CA-B-LONGITUDE | CA-COMMERCIAL | X(11) | text, 11 characters |  |  |  |
| CA-B-CUSTOMER | CA-COMMERCIAL | X(255) | text, 255 characters |  |  |  |
| CA-B-PROPTYPE | CA-COMMERCIAL | X(255) | text, 255 characters |  |  |  |
| CA-B-FIREPERIL | CA-COMMERCIAL | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| CA-B-FIREPREMIUM | CA-COMMERCIAL | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  |  |
| CA-B-CRIMEPERIL | CA-COMMERCIAL | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| CA-B-CRIMEPREMIUM | CA-COMMERCIAL | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  |  |
| CA-B-FLOODPERIL | CA-COMMERCIAL | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| CA-B-FLOODPREMIUM | CA-COMMERCIAL | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  |  |
| CA-B-WEATHERPERIL | CA-COMMERCIAL | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| CA-B-WEATHERPREMIUM | CA-COMMERCIAL | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  |  |
| CA-B-STATUS | CA-COMMERCIAL | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| CA-B-REJECTREASON | CA-COMMERCIAL | X(255) | text, 255 characters |  |  |  |
| CA-B-FILLER | CA-COMMERCIAL | X(31298) | text, 31298 characters |  |  |  |
| CA-CLAIM |  |  | group |  |  | redefines CA-POLICY-SPECIFIC |
| CA-C-NUM | CA-CLAIM | 9(10) | unsigned integer, 10 digits (zoned decimal) |  |  |  |
| CA-C-DATE | CA-CLAIM | X(10) | text, 10 characters |  |  |  |
| CA-C-PAID | CA-CLAIM | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  |  |
| CA-C-VALUE | CA-CLAIM | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  |  |
| CA-C-CAUSE | CA-CLAIM | X(255) | text, 255 characters |  |  |  |
| CA-C-OBSERVATIONS | CA-CLAIM | X(255) | text, 255 characters |  |  |  |
| CA-C-FILLER | CA-CLAIM | X(31854) | text, 31854 characters |  |  |  |


## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-035 | Replace stored customer record | business rule | WHEN a customer update reaches the customer file step, THE Customer Update SHALL read the customer's record in the customer file (KSDSCUST) by the 10-digit customer number and lock it for update, then replace the whole stored record with the 225 bytes of customer data from the request. | high | base/src/lgucvs01.cbl:50, base/src/lgucvs01.cbl:67-96, base/src/lgucvs01.cbl:104-120, base/src/lgucdb01.cbl:136-139 |
| CRCM-BR-036 | Customer update requires an existing record and fully replaces it | error handling | WHEN the customer record cannot be read for update for any reason, including the customer not being on the file, THE Customer Update SHALL set return code '81', write an error message with date, time, customer number and response codes to the error queue (via LGSTSQ), and end the task abnormally with code 'LGV1'. | high | base/src/lgucvs01.cbl:50, base/src/lgucvs01.cbl:67-96, base/src/lgucvs01.cbl:104-120, base/src/lgucdb01.cbl:136-139 |
| CRCM-BR-037 | Replace stored customer record | error handling | WHEN rewriting the locked customer record fails, THE Customer Update SHALL set return code '82', write an error message with date, time, customer number and response codes to the error queue (via LGSTSQ), and end the task abnormally with code 'LGV2'. | high | base/src/lgucvs01.cbl:50, base/src/lgucvs01.cbl:67-96, base/src/lgucvs01.cbl:104-120, base/src/lgucdb01.cbl:136-139 |

### Worked examples

- CRCM-BR-036: customer number = 0001000099; customer on file = no → Return code '81', error message logged, task abends with 'LGV1'; nothing is rewritten.
- CRCM-BR-037: customer number = 0001000042; rewrite result = failed → Return code '82', error message logged, task abends with 'LGV2'.

## Decision tables

#### Customer file record replacement

| Read for update | Rewrite | Result | Rule |
|---|---|---|---|
| Succeeds | Succeeds | Whole stored record replaced with the 225 bytes from the request | CRCM-BR-035 |
| Fails (including customer not on file) | - | Return code '81'; error logged; abend 'LGV1' | CRCM-BR-036 |
| Succeeds | Fails | Return code '82'; error logged; abend 'LGV2' | CRCM-BR-037 |


## Design notes

None.

## Open questions

- SME-088: When a customer's details are updated, the second copy of the customer record is always replaced afterwards. Should that copy be replaced only when the main database update succeeded, and not when the customer was not found or the update failed? (Data architect) On CRCM-BR-037.
- SME-089: A customer update writes to two stores. If the second write fails, the first is not undone. Should the two updates succeed or fail together? (Solution architect) On CRCM-BR-037.
- SME-090: When a customer update fails for a reason other than 'customer not found', what result code should the caller receive? (Business analyst, customer maintenance) On CRCM-BR-037.
- SME-091: A customer details update returns a number of policies set to '00'. What is this field for in the reply, and should it be kept? (Business analyst, customer maintenance) On CRCM-BR-037.
- DEF-020: Is this intended? The caller (LGUCDB01) links to this step even when its DB2 customer update found no customer (return code '01') or failed ('90'), so a DB2 failure can be followed by a VSAM update or an LGV1 abend. Also, the read failure logs the same ' Re-write KSDSCUST ' message text as a rewrite failure. (Subject-matter expert) On CRCM-BR-037.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
