# Implementation plan: Copy the new customer to the customer file (CRCM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as scheduled job.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as scheduled job.

## Data model

#### LGCMAREA

File record of LGACDB01, LGACVS01. Source: `base/src/lgcmarea.cpy`.

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

- LGPOLICY (working storage of LGACDB01): see data-contracts.md.

## Design notes

- CRCM-BR-016: Call the customer-file copy step only after the customer row is stored, and pass it the whole customer record including the newly assigned number. The step can be an in-process call or a message to the service that owns the customer file, but it must not run when the insert failed.
- CRCM-BR-017: The customer file needs a store keyed by the 10-digit customer number, with one record per customer holding the number, first and last name, date of birth, house name, house number, postcode, number of policies, mobile phone, home phone and email. Adding a customer is an insert-only write, so an existing key must make the write fail.

## Decision tables

None.
