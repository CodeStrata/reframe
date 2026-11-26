# Copy the new customer to the customer file (CRCM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Record Management · Customer Record Creation and Maintenance · runs as scheduled job · risk high

## Introduction

After a new customer is stored, writes a copy of the full customer record to the customer file, keyed by the 10-digit customer number, so every store holds the same details. If that write fails for any reason, including a customer number that already exists, it must return code '80', log the failure with the request data and stop. It must never leave the failure unrecorded.

**User story:** As a customer service user, I want each newly added customer to be written to the customer file as well, so that the customer details are held in every store.

## Requirements

### Requirement 1: CRCM-REQ-F-010 (design note)

#### Acceptance criteria

1. When a new-customer request has been inserted successfully, the system shall pass the full 225-byte request data, including the assigned customer number, to the customer copy step. (rules CRCM-BR-016)
2. GIVEN A new-customer request has passed validation and the customer row has been inserted successfully under the assigned customer number 0000001234 WHEN Customer registration continues to the customer copy step THEN The copy step receives the full 225-byte customer request data, and the customer number field in that data holds 0000001234 (CRCM-C03-AC-04; CRCM-BR-016)

### Requirement 2: CRCM-REQ-F-011 (design note)

#### Acceptance criteria

1. When a new customer has been added, the system shall write a 225-byte record to the customer file KSDSCUST, keyed by the 10-digit customer number, holding the customer number, first and last name, date of birth, house name, house number, postcode, number of policies, mobile phone, home phone and email address. (rules CRCM-BR-017)
2. GIVEN customer number: 0001000042; first name: Jane; last name: Smith; date of birth: 1980-05-14; postcode: SO21 2JN WHEN a new customer has been added THEN A 225-byte record with key 0001000042 is written to KSDSCUST (CRCM-C03-AC-01; CRCM-BR-017)

### Requirement 3: CRCM-REQ-F-012 (error handling)

#### Acceptance criteria

1. If the write to the customer file KSDSCUST does not complete normally for any reason (for example the customer number already exists), then the system shall set return code '80', log the failure with its response codes, and abend the task with code 'LGV0' without a dump. (rules CRCM-BR-018)
2. GIVEN customer number: 0001000042; KSDSCUST already holds key: 0001000042 WHEN the write to the customer file KSDSCUST does not complete normally for any reason (for example the customer number already exists) THEN Return code '80' is set, an error is logged, and the task abends with 'LGV0' (CRCM-C03-AC-02; CRCM-BR-018)

### Requirement 4: CRCM-REQ-F-013 (side effect)

#### Acceptance criteria

1. If writing a new customer to the customer file KSDSCUST fails, then the system shall log a message with the date (MMDDYYYY), time (HHMMSS), 'LGACVS01', the customer number, 'Write file KSDSCUST' and the response codes. (rules CRCM-BR-019)
2. GIVEN A new customer 0000001234 has been added, and the customer file KSDSCUST already holds a record under customer number 0000001234 WHEN The add-customer file step tries to write the new customer to KSDSCUST and the write fails THEN A log message is written that holds the current date in MMDDYYYY form, the time in HHMMSS form, 'LGACVS01', customer number 0000001234, 'Write file KSDSCUST' and the response codes of the failed write (CRCM-C03-AC-05; CRCM-BR-019)

### Requirement 5: CRCM-REQ-F-014 (side effect)

#### Acceptance criteria

1. When a customer file write failure is logged, if request data was received, then the system shall also log 'COMMAREA=' followed by the first 90 bytes of the request, or the whole request if it is shorter than 91 bytes. (rules CRCM-BR-020)
2. GIVEN request length: 225 bytes WHEN the failure is logged and request data was received THEN A second message 'COMMAREA=' plus the first 90 bytes of the request is logged (CRCM-C03-AC-03; CRCM-BR-020)

## Screens and components

No screens: it runs as scheduled job.

## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CRCM-BR-016 | Register customer and hand off to copy program | design note | WHEN a validated new-customer request has been inserted successfully, THE Customer Registration SHALL delegate to the customer copy program (`LGACVS01`) with the full 225-byte request data, including the assigned customer number | medium | base/src/lgacdb01.cbl:171-172,174-177, base/src/lgacdb01.cbl:174-177 |
| CRCM-BR-017 | Write new customer record | design note | WHEN a new customer has been added, THE add-customer file step SHALL write a 225-byte record to the customer file KSDSCUST, keyed by the 10-digit customer number, holding the customer number, first and last name, date of birth, house name, house number, postcode, number of policies, mobile phone, home phone and email address. | high | base/src/lgacvs01.cbl:49, base/src/lgacvs01.cbl:66-81, base/src/lgcmarea.cpy:10-25 |
| CRCM-BR-018 | Write new customer record | error handling | WHEN the write to the customer file KSDSCUST does not complete normally for any reason (for example the customer number already exists), THE add-customer file step SHALL set return code '80', log the failure with its response codes, and abend the task with code 'LGV0' without a dump. | high | base/src/lgacvs01.cbl:49, base/src/lgacvs01.cbl:66-81, base/src/lgcmarea.cpy:10-25 |
| CRCM-BR-019 | VSAM customer-file failures are recorded in an audit log with a timestamp and the request data | side effect | WHEN writing a new customer to the customer file KSDSCUST fails, THE add-customer file step SHALL log a message with the date (MMDDYYYY), time (HHMMSS), 'LGACVS01', the customer number, 'Write file KSDSCUST' and the response codes, through the shared logging program (LGSTSQ). | medium | base/src/lgacvs01.cbl:30-47, base/src/lgacvs01.cbl:89-120 |
| CRCM-BR-020 | VSAM customer-file failures are recorded in an audit log with a timestamp and the request data | side effect | WHEN the failure is logged and request data was received, THE add-customer file step SHALL also log 'COMMAREA=' followed by the first 90 bytes of the request, or the whole request if it is shorter than 91 bytes. | medium | base/src/lgacvs01.cbl:30-47, base/src/lgacvs01.cbl:89-120 |

### Worked examples

- CRCM-BR-017: customer number = 0001000042; first name = Jane; last name = Smith; date of birth = 1980-05-14; postcode = SO21 2JN → A 225-byte record with key 0001000042 is written to KSDSCUST
- CRCM-BR-018: customer number = 0001000042; KSDSCUST already holds key = 0001000042 → Return code '80' is set, an error is logged, and the task abends with 'LGV0'
- CRCM-BR-020: request length = 225 bytes → A second message 'COMMAREA=' plus the first 90 bytes of the request is logged

## Decision tables

None.

## Design notes

- CRCM-BR-016: Call the customer-file copy step only after the customer row is stored, and pass it the whole customer record including the newly assigned number. The step can be an in-process call or a message to the service that owns the customer file, but it must not run when the insert failed.
- CRCM-BR-017: The customer file needs a store keyed by the 10-digit customer number, with one record per customer holding the number, first and last name, date of birth, house name, house number, postcode, number of policies, mobile phone, home phone and email. Adding a customer is an insert-only write, so an existing key must make the write fail.

## Open questions

- SME-015: Every new customer gets the same fixed initial password. Is this shared default password meant to be used in production, and should the new system keep it or create a separate password for each customer? (Security team) On CRCM-BR-016, CRCM-BR-018.
- SME-024: When an add-customer request is shorter than the required 90 characters, the rules disagree: some say the return code is '98', and others say the request comes back with the default '00'. Which return code must the new system give for a short request? (Business analyst) On CRCM-BR-016, CRCM-BR-018.
- SME-025: After a new customer is inserted, the customer record is written to the VSAM customer file and a customer security record is created. In what order must these happen, and must both happen for every new customer? (Solution architect) On CRCM-BR-016, CRCM-BR-018.
- SME-026: Is the VSAM customer file still the main record for any process? If writing to the VSAM file or creating the security record fails after the customer has been inserted into the database, must the database insert be rolled back, and which store is the master copy after a partial failure? (Solution architect) On CRCM-BR-016, CRCM-BR-018.
- SME-027: When the counter is unavailable, the database generates the customer number instead. What format must customer numbers have, and how is it guaranteed that numbers from the two methods never clash, given that the VSAM customer key is 10 characters? (Data architect) On CRCM-BR-016, CRCM-BR-018.
- SME-028: Customer security requests with a request type other than '02ACUS' are passed to handling outside this process. Should the new system reject these requests, ignore them, or handle them somewhere else? (Business analyst) On CRCM-BR-016, CRCM-BR-018.
- DEF-011: Confirm this is deliberate: The return code '80' is set just before the task abends, and the CICS RETURN after the abend never runs, so the caller never sees the '80' code; the add then fails as an abend instead of a return code. (Subject-matter expert) On CRCM-BR-018.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (5 in all).
