# Data contracts

The copybooks the capabilities' programs copy, as typed records, read from the legacy source.

#### CCPAUERY

Source: `app/app-authorization-ims-db2-mq/cpy/CCPAUERY.cpy`.

Record `ERROR-LOG-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ERR-DATE |  | X(06) | text, 6 characters |  |  |  |
| ERR-TIME |  | X(06) | text, 6 characters |  |  |  |
| ERR-APPLICATION |  | X(08) | text, 8 characters |  |  |  |
| ERR-PROGRAM |  | X(08) | text, 8 characters |  |  |  |
| ERR-LOCATION |  | X(04) | text, 4 characters |  |  |  |
| ERR-LEVEL |  | X(01) | text, 1 character |  |  | ERR-LOG = L; ERR-INFO = I; ERR-WARNING = W; ERR-CRITICAL = C |
| ERR-SUBSYSTEM |  | X(01) | text, 1 character |  |  | ERR-APP = A; ERR-CICS = C; ERR-IMS = I; ERR-DB2 = D; ERR-MQ = M; ERR-FILE = F |
| ERR-CODE-1 |  | X(09) | text, 9 characters |  |  |  |
| ERR-CODE-2 |  | X(09) | text, 9 characters |  |  |  |
| ERR-MESSAGE |  | X(50) | text, 50 characters |  |  |  |
| ERR-EVENT-KEY |  | X(20) | text, 20 characters |  |  |  |

#### CCPAURLY

Source: `app/app-authorization-ims-db2-mq/cpy/CCPAURLY.cpy`.

Record `PA-RL-CARD-NUM`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RL-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |

Record `PA-RL-TRANSACTION-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RL-TRANSACTION-ID |  | X(15) | text, 15 characters |  |  |  |

Record `PA-RL-AUTH-ID-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RL-AUTH-ID-CODE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RL-AUTH-RESP-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RL-AUTH-RESP-CODE |  | X(02) | text, 2 characters |  |  |  |

Record `PA-RL-AUTH-RESP-REASON`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RL-AUTH-RESP-REASON |  | X(04) | text, 4 characters |  |  |  |

Record `PA-RL-APPROVED-AMT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RL-APPROVED-AMT |  | +9(10).99 | formatted text, 14 characters (a number shown with 12 digits) |  |  |  |

#### CCPAURQY

Source: `app/app-authorization-ims-db2-mq/cpy/CCPAURQY.cpy`.

Record `PA-RQ-AUTH-DATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-AUTH-DATE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RQ-AUTH-TIME`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-AUTH-TIME |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RQ-CARD-NUM`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |

Record `PA-RQ-AUTH-TYPE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-AUTH-TYPE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-RQ-CARD-EXPIRY-DATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-CARD-EXPIRY-DATE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-RQ-MESSAGE-TYPE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MESSAGE-TYPE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RQ-MESSAGE-SOURCE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MESSAGE-SOURCE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-RQ-PROCESSING-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-PROCESSING-CODE |  | 9(06) | unsigned integer, 6 digits (zoned decimal) |  |  |  |

Record `PA-RQ-TRANSACTION-AMT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-TRANSACTION-AMT |  | +9(10).99 | formatted text, 14 characters (a number shown with 12 digits) |  |  |  |

Record `PA-RQ-MERCHANT-CATAGORY-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-CATAGORY-CODE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-RQ-ACQR-COUNTRY-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-ACQR-COUNTRY-CODE |  | X(03) | text, 3 characters |  |  |  |

Record `PA-RQ-POS-ENTRY-MODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-POS-ENTRY-MODE |  | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |

Record `PA-RQ-MERCHANT-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-ID |  | X(15) | text, 15 characters |  |  |  |

Record `PA-RQ-MERCHANT-NAME`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-NAME |  | X(22) | text, 22 characters |  |  |  |

Record `PA-RQ-MERCHANT-CITY`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-CITY |  | X(13) | text, 13 characters |  |  |  |

Record `PA-RQ-MERCHANT-STATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-STATE |  | X(02) | text, 2 characters |  |  |  |

Record `PA-RQ-MERCHANT-ZIP`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-MERCHANT-ZIP |  | X(09) | text, 9 characters |  |  |  |

Record `PA-RQ-TRANSACTION-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-RQ-TRANSACTION-ID |  | X(15) | text, 15 characters |  |  |  |

#### CIPAUDTY

Source: `app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy`.

Record `PA-AUTHORIZATION-KEY`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-DATE-9C |  | S9(05) COMP-3 | signed integer, 5 digits (packed decimal) |  |  |  |
| PA-AUTH-TIME-9C |  | S9(09) COMP-3 | signed integer, 9 digits (packed decimal) |  |  |  |

Record `PA-AUTH-ORIG-DATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-ORIG-DATE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-AUTH-ORIG-TIME`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-ORIG-TIME |  | X(06) | text, 6 characters |  |  |  |

Record `PA-CARD-NUM`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |

Record `PA-AUTH-TYPE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-TYPE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-CARD-EXPIRY-DATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-CARD-EXPIRY-DATE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-MESSAGE-TYPE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MESSAGE-TYPE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-MESSAGE-SOURCE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MESSAGE-SOURCE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-AUTH-ID-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-ID-CODE |  | X(06) | text, 6 characters |  |  |  |

Record `PA-AUTH-RESP-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-RESP-CODE |  | X(02) | text, 2 characters |  |  | PA-AUTH-APPROVED = 00 |

Record `PA-AUTH-RESP-REASON`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-RESP-REASON |  | X(04) | text, 4 characters |  |  |  |

Record `PA-PROCESSING-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-PROCESSING-CODE |  | 9(06) | unsigned integer, 6 digits (zoned decimal) |  |  |  |

Record `PA-TRANSACTION-AMT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-TRANSACTION-AMT |  | S9(10)V99 COMP-3 | signed decimal, 10 integer and 2 fraction digits (packed decimal) |  |  |  |

Record `PA-APPROVED-AMT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-APPROVED-AMT |  | S9(10)V99 COMP-3 | signed decimal, 10 integer and 2 fraction digits (packed decimal) |  |  |  |

Record `PA-MERCHANT-CATAGORY-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MERCHANT-CATAGORY-CODE |  | X(04) | text, 4 characters |  |  |  |

Record `PA-ACQR-COUNTRY-CODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-ACQR-COUNTRY-CODE |  | X(03) | text, 3 characters |  |  |  |

Record `PA-POS-ENTRY-MODE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-POS-ENTRY-MODE |  | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |

Record `PA-MERCHANT-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MERCHANT-ID |  | X(15) | text, 15 characters |  |  |  |

Record `PA-MERCHANT-NAME`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MERCHANT-NAME |  | X(22) | text, 22 characters |  |  |  |

Record `PA-MERCHANT-CITY`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MERCHANT-CITY |  | X(13) | text, 13 characters |  |  |  |

Record `PA-MERCHANT-STATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MERCHANT-STATE |  | X(02) | text, 2 characters |  |  |  |

Record `PA-MERCHANT-ZIP`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MERCHANT-ZIP |  | X(09) | text, 9 characters |  |  |  |

Record `PA-TRANSACTION-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-TRANSACTION-ID |  | X(15) | text, 15 characters |  |  |  |

Record `PA-MATCH-STATUS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-MATCH-STATUS |  | X(01) | text, 1 character |  |  | PA-MATCH-PENDING = P; PA-MATCH-AUTH-DECLINED = D; PA-MATCH-PENDING-EXPIRED = E; PA-MATCHED-WITH-TRAN = M |

Record `PA-AUTH-FRAUD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-FRAUD |  | X(01) | text, 1 character |  |  | PA-FRAUD-CONFIRMED = F; PA-FRAUD-REMOVED = R |

Record `PA-FRAUD-RPT-DATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-FRAUD-RPT-DATE |  | X(08) | text, 8 characters |  |  |  |

Record `FILLER`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| FILLER |  | X(17) | text, 17 characters |  |  |  |

#### CIPAUSMY

Source: `app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy`.

Record `PA-ACCT-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-ACCT-ID |  | S9(11) COMP-3 | signed integer, 11 digits (packed decimal) |  |  |  |

Record `PA-CUST-ID`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |

Record `PA-AUTH-STATUS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-AUTH-STATUS |  | X(01) | text, 1 character |  |  |  |

Record `PA-ACCOUNT-STATUS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-ACCOUNT-STATUS |  | X(02) | text, 2 characters |  |  | occurs 5 |

Record `PA-CREDIT-LIMIT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-CREDIT-LIMIT |  | S9(09)V99 COMP-3 | signed decimal, 9 integer and 2 fraction digits (packed decimal) |  |  |  |

Record `PA-CASH-LIMIT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-CASH-LIMIT |  | S9(09)V99 COMP-3 | signed decimal, 9 integer and 2 fraction digits (packed decimal) |  |  |  |

Record `PA-CREDIT-BALANCE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-CREDIT-BALANCE |  | S9(09)V99 COMP-3 | signed decimal, 9 integer and 2 fraction digits (packed decimal) |  |  |  |

Record `PA-CASH-BALANCE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-CASH-BALANCE |  | S9(09)V99 COMP-3 | signed decimal, 9 integer and 2 fraction digits (packed decimal) |  |  |  |

Record `PA-APPROVED-AUTH-CNT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-APPROVED-AUTH-CNT |  | S9(04) COMP | signed integer, 4 digits (binary) |  |  |  |

Record `PA-DECLINED-AUTH-CNT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-DECLINED-AUTH-CNT |  | S9(04) COMP | signed integer, 4 digits (binary) |  |  |  |

Record `PA-APPROVED-AUTH-AMT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-APPROVED-AUTH-AMT |  | S9(09)V99 COMP-3 | signed decimal, 9 integer and 2 fraction digits (packed decimal) |  |  |  |

Record `PA-DECLINED-AUTH-AMT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PA-DECLINED-AUTH-AMT |  | S9(09)V99 COMP-3 | signed decimal, 9 integer and 2 fraction digits (packed decimal) |  |  |  |

Record `FILLER`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| FILLER |  | X(34) | text, 34 characters |  |  |  |

#### COADM02Y

Source: `app/cpy/COADM02Y.cpy`.

Record `CARDDEMO-ADMIN-MENU-OPTIONS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CDEMO-ADMIN-OPT-COUNT |  | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| CDEMO-ADMIN-OPTIONS-DATA |  |  | group |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-ADMIN-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| CDEMO-ADMIN-OPTIONS |  |  | group |  |  | redefines CDEMO-ADMIN-OPTIONS-DATA |
| CDEMO-ADMIN-OPT | CDEMO-ADMIN-OPTIONS |  | group |  |  | occurs 9 |
| CDEMO-ADMIN-OPT-NUM | CDEMO-ADMIN-OPTIONS/CDEMO-ADMIN-OPT | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| CDEMO-ADMIN-OPT-NAME | CDEMO-ADMIN-OPTIONS/CDEMO-ADMIN-OPT | X(35) | text, 35 characters |  |  |  |
| CDEMO-ADMIN-OPT-PGMNAME | CDEMO-ADMIN-OPTIONS/CDEMO-ADMIN-OPT | X(08) | text, 8 characters |  |  |  |

#### COCOM01Y

Source: `app/cpy/COCOM01Y.cpy`.

Record `CARDDEMO-COMMAREA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CDEMO-GENERAL-INFO |  |  | group |  |  |  |
| CDEMO-FROM-TRANID | CDEMO-GENERAL-INFO | X(04) | text, 4 characters |  |  |  |
| CDEMO-FROM-PROGRAM | CDEMO-GENERAL-INFO | X(08) | text, 8 characters |  |  |  |
| CDEMO-TO-TRANID | CDEMO-GENERAL-INFO | X(04) | text, 4 characters |  |  |  |
| CDEMO-TO-PROGRAM | CDEMO-GENERAL-INFO | X(08) | text, 8 characters |  |  |  |
| CDEMO-USER-ID | CDEMO-GENERAL-INFO | X(08) | text, 8 characters |  |  |  |
| CDEMO-USER-TYPE | CDEMO-GENERAL-INFO | X(01) | text, 1 character |  |  | CDEMO-USRTYP-ADMIN = A; CDEMO-USRTYP-USER = U |
| CDEMO-PGM-CONTEXT | CDEMO-GENERAL-INFO | 9(01) | unsigned integer, 1 digit (zoned decimal) |  |  | CDEMO-PGM-ENTER = 0; CDEMO-PGM-REENTER = 1 |
| CDEMO-CUSTOMER-INFO |  |  | group |  |  |  |
| CDEMO-CUST-ID | CDEMO-CUSTOMER-INFO | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CDEMO-CUST-FNAME | CDEMO-CUSTOMER-INFO | X(25) | text, 25 characters |  |  |  |
| CDEMO-CUST-MNAME | CDEMO-CUSTOMER-INFO | X(25) | text, 25 characters |  |  |  |
| CDEMO-CUST-LNAME | CDEMO-CUSTOMER-INFO | X(25) | text, 25 characters |  |  |  |
| CDEMO-ACCOUNT-INFO |  |  | group |  |  |  |
| CDEMO-ACCT-ID | CDEMO-ACCOUNT-INFO | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| CDEMO-ACCT-STATUS | CDEMO-ACCOUNT-INFO | X(01) | text, 1 character |  |  |  |
| CDEMO-CARD-INFO |  |  | group |  |  |  |
| CDEMO-CARD-NUM | CDEMO-CARD-INFO | 9(16) | unsigned integer, 16 digits (zoned decimal) |  |  |  |
| CDEMO-MORE-INFO |  |  | group |  |  |  |
| CDEMO-LAST-MAP | CDEMO-MORE-INFO | X(7) | text, 7 characters |  |  |  |
| CDEMO-LAST-MAPSET | CDEMO-MORE-INFO | X(7) | text, 7 characters |  |  |  |

#### CODATECN

Source: `app/cpy/CODATECN.cpy`.

Record `CODATECN-REC`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CODATECN-IN-REC |  |  | group |  |  |  |
| CODATECN-TYPE | CODATECN-IN-REC | X | text, 1 character |  |  | YYYYMMDD-IN = 1; YYYY-MM-DD-IN = 2 |
| CODATECN-INP-DATE | CODATECN-IN-REC | X(20) | text, 20 characters |  |  |  |
| CODATECN-1INP | CODATECN-IN-REC |  | group |  |  | redefines CODATECN-INP-DATE |
| CODATECN-1YYYY | CODATECN-IN-REC/CODATECN-1INP | XXXX | text, 4 characters |  |  |  |
| CODATECN-1MM | CODATECN-IN-REC/CODATECN-1INP | XX | text, 2 characters |  |  |  |
| CODATECN-1DD | CODATECN-IN-REC/CODATECN-1INP | XX | text, 2 characters |  |  |  |
| CODATECN-1FIL | CODATECN-IN-REC/CODATECN-1INP | X(12) | text, 12 characters |  |  |  |
| CODATECN-2INP | CODATECN-IN-REC |  | group |  |  | redefines CODATECN-INP-DATE |
| CODATECN-1O-YYYY | CODATECN-IN-REC/CODATECN-2INP | XXXX | text, 4 characters |  |  |  |
| CODATECN-1I-S1 | CODATECN-IN-REC/CODATECN-2INP | X | text, 1 character |  |  |  |
| CODATECN-1MM | CODATECN-IN-REC/CODATECN-2INP | XX | text, 2 characters |  |  |  |
| CODATECN-1I-S2 | CODATECN-IN-REC/CODATECN-2INP | X | text, 1 character |  |  |  |
| CODATECN-2YY | CODATECN-IN-REC/CODATECN-2INP | XX | text, 2 characters |  |  |  |
| CODATECN-2FIL | CODATECN-IN-REC/CODATECN-2INP | X(10) | text, 10 characters |  |  |  |
| CODATECN-OUT-REC |  |  | group |  |  |  |
| CODATECN-OUTTYPE | CODATECN-OUT-REC | X | text, 1 character |  |  | YYYY-MM-DD-OP = 1; YYYYMMDD-OP = 2 |
| CODATECN-0UT-DATE | CODATECN-OUT-REC | X(20) | text, 20 characters |  |  |  |
| CODATECN-1OUT | CODATECN-OUT-REC |  | group |  |  | redefines CODATECN-0UT-DATE |
| CODATECN-1O-YYYY | CODATECN-OUT-REC/CODATECN-1OUT | XXXX | text, 4 characters |  |  |  |
| CODATECN-1O-S1 | CODATECN-OUT-REC/CODATECN-1OUT | X | text, 1 character |  |  |  |
| CODATECN-1O-MM | CODATECN-OUT-REC/CODATECN-1OUT | XX | text, 2 characters |  |  |  |
| CODATECN-1O-S2 | CODATECN-OUT-REC/CODATECN-1OUT | X | text, 1 character |  |  |  |
| CODATECN-1O-DD | CODATECN-OUT-REC/CODATECN-1OUT | XX | text, 2 characters |  |  |  |
| CODATECN-1OFIL | CODATECN-OUT-REC/CODATECN-1OUT | X(10) | text, 10 characters |  |  |  |
| CODATECN-2OUT | CODATECN-OUT-REC |  | group |  |  | redefines CODATECN-0UT-DATE |
| CODATECN-2O-YYYY | CODATECN-OUT-REC/CODATECN-2OUT | XXXX | text, 4 characters |  |  |  |
| CODATECN-2O-MM | CODATECN-OUT-REC/CODATECN-2OUT | XX | text, 2 characters |  |  |  |
| CODATECN-2O-DD | CODATECN-OUT-REC/CODATECN-2OUT | XX | text, 2 characters |  |  |  |
| CODATECN-2OFIL | CODATECN-OUT-REC/CODATECN-2OUT | X(12) | text, 12 characters |  |  |  |
| CODATECN-ERROR-MSG |  | X(38) | text, 38 characters |  |  |  |

#### COMEN02Y

Source: `app/cpy/COMEN02Y.cpy`.

Record `CARDDEMO-MAIN-MENU-OPTIONS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CDEMO-MENU-OPT-COUNT |  | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| CDEMO-MENU-OPTIONS-DATA |  |  | group |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(35) | text, 35 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(08) | text, 8 characters |  |  |  |
| FILLER | CDEMO-MENU-OPTIONS-DATA | X(01) | text, 1 character |  |  |  |
| CDEMO-MENU-OPTIONS |  |  | group |  |  | redefines CDEMO-MENU-OPTIONS-DATA |
| CDEMO-MENU-OPT | CDEMO-MENU-OPTIONS |  | group |  |  | occurs 12 |
| CDEMO-MENU-OPT-NUM | CDEMO-MENU-OPTIONS/CDEMO-MENU-OPT | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| CDEMO-MENU-OPT-NAME | CDEMO-MENU-OPTIONS/CDEMO-MENU-OPT | X(35) | text, 35 characters |  |  |  |
| CDEMO-MENU-OPT-PGMNAME | CDEMO-MENU-OPTIONS/CDEMO-MENU-OPT | X(08) | text, 8 characters |  |  |  |
| CDEMO-MENU-OPT-USRTYPE | CDEMO-MENU-OPTIONS/CDEMO-MENU-OPT | X(01) | text, 1 character |  |  |  |

#### COSTM01

Source: `app/cpy/COSTM01.CPY`.

Record `TRNX-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRNX-KEY |  |  | group |  |  |  |
| TRNX-CARD-NUM | TRNX-KEY | X(16) | text, 16 characters |  |  |  |
| TRNX-ID | TRNX-KEY | X(16) | text, 16 characters |  |  |  |
| TRNX-REST |  |  | group |  |  |  |
| TRNX-TYPE-CD | TRNX-REST | X(02) | text, 2 characters |  |  |  |
| TRNX-CAT-CD | TRNX-REST | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRNX-SOURCE | TRNX-REST | X(10) | text, 10 characters |  |  |  |
| TRNX-DESC | TRNX-REST | X(100) | text, 100 characters |  |  |  |
| TRNX-AMT | TRNX-REST | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRNX-MERCHANT-ID | TRNX-REST | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRNX-MERCHANT-NAME | TRNX-REST | X(50) | text, 50 characters |  |  |  |
| TRNX-MERCHANT-CITY | TRNX-REST | X(50) | text, 50 characters |  |  |  |
| TRNX-MERCHANT-ZIP | TRNX-REST | X(10) | text, 10 characters |  |  |  |
| TRNX-ORIG-TS | TRNX-REST | X(26) | text, 26 characters |  |  |  |
| TRNX-PROC-TS | TRNX-REST | X(26) | text, 26 characters |  |  |  |
| FILLER | TRNX-REST | X(20) | text, 20 characters |  |  |  |

#### COTTL01Y

Source: `app/cpy/COTTL01Y.cpy`.

Record `CCDA-SCREEN-TITLE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CCDA-TITLE01 |  | X(40) | text, 40 characters |  |  |  |
| CCDA-TITLE02 |  | X(40) | text, 40 characters |  |  |  |
| CCDA-THANK-YOU |  | X(40) | text, 40 characters |  |  |  |

#### CSDAT01Y

Source: `app/cpy/CSDAT01Y.cpy`.

Record `WS-DATE-TIME`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-CURDATE-DATA |  |  | group |  |  |  |
| WS-CURDATE | WS-CURDATE-DATA |  | group |  |  |  |
| WS-CURDATE-YEAR | WS-CURDATE-DATA/WS-CURDATE | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| WS-CURDATE-MONTH | WS-CURDATE-DATA/WS-CURDATE | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| WS-CURDATE-DAY | WS-CURDATE-DATA/WS-CURDATE | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| WS-CURDATE-N | WS-CURDATE-DATA | 9(08) | unsigned integer, 8 digits (zoned decimal) |  |  | redefines WS-CURDATE |
| WS-CURTIME | WS-CURDATE-DATA |  | group |  |  |  |
| WS-CURTIME-HOURS | WS-CURDATE-DATA/WS-CURTIME | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| WS-CURTIME-MINUTE | WS-CURDATE-DATA/WS-CURTIME | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| WS-CURTIME-SECOND | WS-CURDATE-DATA/WS-CURTIME | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| WS-CURTIME-MILSEC | WS-CURDATE-DATA/WS-CURTIME | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| WS-CURTIME-N | WS-CURDATE-DATA | 9(08) | unsigned integer, 8 digits (zoned decimal) |  |  | redefines WS-CURTIME |
| WS-CURDATE-MM-DD-YY |  |  | group |  |  |  |
| WS-CURDATE-MM | WS-CURDATE-MM-DD-YY | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-CURDATE-MM-DD-YY | X(01) | text, 1 character |  |  |  |
| WS-CURDATE-DD | WS-CURDATE-MM-DD-YY | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-CURDATE-MM-DD-YY | X(01) | text, 1 character |  |  |  |
| WS-CURDATE-YY | WS-CURDATE-MM-DD-YY | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| WS-CURTIME-HH-MM-SS |  |  | group |  |  |  |
| WS-CURTIME-HH | WS-CURTIME-HH-MM-SS | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-CURTIME-HH-MM-SS | X(01) | text, 1 character |  |  |  |
| WS-CURTIME-MM | WS-CURTIME-HH-MM-SS | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-CURTIME-HH-MM-SS | X(01) | text, 1 character |  |  |  |
| WS-CURTIME-SS | WS-CURTIME-HH-MM-SS | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| WS-TIMESTAMP |  |  | group |  |  |  |
| WS-TIMESTAMP-DT-YYYY | WS-TIMESTAMP | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| FILLER | WS-TIMESTAMP | X(01) | text, 1 character |  |  |  |
| WS-TIMESTAMP-DT-MM | WS-TIMESTAMP | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-TIMESTAMP | X(01) | text, 1 character |  |  |  |
| WS-TIMESTAMP-DT-DD | WS-TIMESTAMP | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-TIMESTAMP | X(01) | text, 1 character |  |  |  |
| WS-TIMESTAMP-TM-HH | WS-TIMESTAMP | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-TIMESTAMP | X(01) | text, 1 character |  |  |  |
| WS-TIMESTAMP-TM-MM | WS-TIMESTAMP | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-TIMESTAMP | X(01) | text, 1 character |  |  |  |
| WS-TIMESTAMP-TM-SS | WS-TIMESTAMP | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  |  |
| FILLER | WS-TIMESTAMP | X(01) | text, 1 character |  |  |  |
| WS-TIMESTAMP-TM-MS6 | WS-TIMESTAMP | 9(06) | unsigned integer, 6 digits (zoned decimal) |  |  |  |

#### CSDB2RPY

Source: `app/app-transaction-type-db2/cpy/CSDB2RPY.cpy`.

#### CSDB2RWY

Source: `app/app-transaction-type-db2/cpy/CSDB2RWY.cpy`.

Record `WS-DB2-COMMON-VARS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-DISP-SQLCODE |  | ----9 | formatted text, 5 characters (a number shown with 1 digit) |  |  |  |
| WS-DUMMY-DB2-INT |  | S9(4) COMP-3 | signed integer, 4 digits (packed decimal) |  |  |  |
| WS-DB2-PROCESSING-FLAG |  | X(1) | text, 1 character |  |  | WS-DB2-OK = 0; WS-DB2-ERROR = 1 |
| WS-DB2-CURRENT-ACTION |  | X(72) | text, 72 characters |  |  |  |

Record `WS-DSNTIAC-FORMATTED`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-DSNTIAC-MESG-LEN |  | S9(4) COMP | signed integer, 4 digits (binary) |  |  |  |
| WS-DSNTIAC-FMTD-TEXT |  |  | group |  |  |  |
| WS-DSNTIAC-FMTD-TEXT-LINE | WS-DSNTIAC-FMTD-TEXT | X(72) | text, 72 characters |  |  | occurs 10 |

Record `WS-DSNTIAC-LRECL`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-DSNTIAC-LRECL |  | S9(4) COMP | signed integer, 4 digits (binary) |  |  |  |

Record `WS-DSNTIAC-ERROR`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-DSNTIAC-ERR-MSG |  | X(10) | text, 10 characters |  |  |  |
| WS-DSNTIAC-ERR-CD-X |  | X(02) | text, 2 characters |  |  |  |
| WS-DSNTIAC-ERR-CD |  | 9(02) | unsigned integer, 2 digits (zoned decimal) |  |  | redefines WS-DSNTIAC-ERR-CD-X |

#### CSLKPCDY

Source: `app/cpy/CSLKPCDY.cpy`.

Record `WS-US-PHONE-AREA-CODE-TO-EDIT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-US-PHONE-AREA-CODE-TO-EDIT |  | XXX | text, 3 characters |  |  | VALID-PHONE-AREA-CODE = 201; VALID-GENERAL-PURP-CODE = 201; VALID-EASY-RECOG-AREA-CODE = 200 |

Record `US-STATE-CODE-TO-EDIT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| US-STATE-CODE-TO-EDIT |  | X(2) | text, 2 characters |  |  | VALID-US-STATE-CODE = AL |

Record `US-STATE-ZIPCODE-TO-EDIT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| US-STATE-AND-FIRST-ZIP2 |  | X(4) | text, 4 characters |  |  | VALID-US-STATE-ZIP-CD2-COMBO = AA34 |
| LAST-3-OF-ZIP |  | X(3) | text, 3 characters |  |  |  |

#### CSMSG01Y

Source: `app/cpy/CSMSG01Y.cpy`.

Record `CCDA-COMMON-MESSAGES`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CCDA-MSG-THANK-YOU |  | X(50) | text, 50 characters |  |  |  |
| CCDA-MSG-INVALID-KEY |  | X(50) | text, 50 characters |  |  |  |

#### CSMSG02Y

Source: `app/cpy/CSMSG02Y.cpy`.

Record `ABEND-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ABEND-CODE |  | X(4) | text, 4 characters |  |  |  |
| ABEND-CULPRIT |  | X(8) | text, 8 characters |  |  |  |
| ABEND-REASON |  | X(50) | text, 50 characters |  |  |  |
| ABEND-MSG |  | X(72) | text, 72 characters |  |  |  |

#### CSSETATY

Source: `app/cpy/CSSETATY.cpy`.

#### CSSTRPFY

Source: `app/cpy/CSSTRPFY.cpy`.

#### CSUSR01Y

Source: `app/cpy/CSUSR01Y.cpy`.

Record `SEC-USER-DATA`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| SEC-USR-ID |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-FNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-LNAME |  | X(20) | text, 20 characters |  |  |  |
| SEC-USR-PWD |  | X(08) | text, 8 characters |  |  |  |
| SEC-USR-TYPE |  | X(01) | text, 1 character |  |  |  |
| SEC-USR-FILLER |  | X(23) | text, 23 characters |  |  |  |

#### CSUTLDPY

Source: `app/cpy/CSUTLDPY.cpy`.

#### CSUTLDWY

Source: `app/cpy/CSUTLDWY.cpy`.

Record `WS-EDIT-DATE-CCYYMMDD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-EDIT-DATE-CCYY |  |  | group |  |  |  |
| WS-EDIT-DATE-CC | WS-EDIT-DATE-CCYY | X(2) | text, 2 characters |  |  |  |
| WS-EDIT-DATE-CC-N | WS-EDIT-DATE-CCYY | 9(2) | unsigned integer, 2 digits (zoned decimal) |  |  | redefines WS-EDIT-DATE-CC; THIS-CENTURY = 20; LAST-CENTURY = 19 |
| WS-EDIT-DATE-YY | WS-EDIT-DATE-CCYY | X(2) | text, 2 characters |  |  |  |
| WS-EDIT-DATE-YY-N | WS-EDIT-DATE-CCYY | 9(2) | unsigned integer, 2 digits (zoned decimal) |  |  | redefines WS-EDIT-DATE-YY |
| WS-EDIT-DATE-CCYY-N |  | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  | redefines WS-EDIT-DATE-CCYY |
| WS-EDIT-DATE-MM |  | X(2) | text, 2 characters |  |  |  |
| WS-EDIT-DATE-MM-N |  | 9(2) | unsigned integer, 2 digits (zoned decimal) |  |  | redefines WS-EDIT-DATE-MM; WS-VALID-MONTH = 1; WS-31-DAY-MONTH = 1; WS-FEBRUARY = 2 |
| WS-EDIT-DATE-DD |  | X(2) | text, 2 characters |  |  |  |
| WS-EDIT-DATE-DD-N |  | 9(2) | unsigned integer, 2 digits (zoned decimal) |  |  | redefines WS-EDIT-DATE-DD; WS-VALID-DAY = 1; WS-DAY-31 = 31; WS-DAY-30 = 30; WS-DAY-29 = 29; WS-VALID-FEB-DAY = 1 |

Record `WS-EDIT-DATE-CCYYMMDD-N`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-EDIT-DATE-CCYYMMDD-N |  | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  | redefines WS-EDIT-DATE-CCYYMMDD |

Record `WS-EDIT-DATE-BINARY`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-EDIT-DATE-BINARY |  | S9(9) BINARY | signed integer, 9 digits (binary) |  |  |  |

Record `WS-CURRENT-DATE`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-CURRENT-DATE-YYYYMMDD |  | X(8) | text, 8 characters |  |  |  |
| WS-CURRENT-DATE-YYYYMMDD-N |  | 9(8) | unsigned integer, 8 digits (zoned decimal) |  |  | redefines WS-CURRENT-DATE-YYYYMMDD |
| WS-CURRENT-DATE-BINARY |  | S9(9) BINARY | signed integer, 9 digits (binary) |  |  |  |

Record `WS-EDIT-DATE-FLGS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-EDIT-YEAR-FLG |  | X(01) | text, 1 character |  |  | FLG-YEAR-ISVALID = ; FLG-YEAR-NOT-OK = 0; FLG-YEAR-BLANK = B |
| WS-EDIT-MONTH |  | X(01) | text, 1 character |  |  | FLG-MONTH-ISVALID = ; FLG-MONTH-NOT-OK = 0; FLG-MONTH-BLANK = B |
| WS-EDIT-DAY |  | X(01) | text, 1 character |  |  | FLG-DAY-ISVALID = ; FLG-DAY-NOT-OK = 0; FLG-DAY-BLANK = B |

Record `WS-DATE-FORMAT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-DATE-FORMAT |  | X(08) | text, 8 characters |  |  |  |

Record `WS-DATE-VALIDATION-RESULT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| WS-SEVERITY |  | X(04) | text, 4 characters |  |  |  |
| WS-SEVERITY-N |  | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  | redefines WS-SEVERITY |
| FILLER |  | X(11) | text, 11 characters |  |  |  |
| WS-MSG-NO |  | X(04) | text, 4 characters |  |  |  |
| WS-MSG-NO-N |  | 9(4) | unsigned integer, 4 digits (zoned decimal) |  |  | redefines WS-MSG-NO |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| WS-RESULT |  | X(15) | text, 15 characters |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| FILLER |  | X(09) | text, 9 characters |  |  |  |
| WS-DATE |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| FILLER |  | X(10) | text, 10 characters |  |  |  |
| WS-DATE-FMT |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| FILLER |  | X(03) | text, 3 characters |  |  |  |

#### CUSTREC

Source: `app/cpy/CUSTREC.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYYMMDD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

#### CVACT01Y

Source: `app/cpy/CVACT01Y.cpy`.

Record `ACCOUNT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| ACCT-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| ACCT-CURR-BAL |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CASH-CREDIT-LIMIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-OPEN-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-REISSUE-DATE |  | X(10) | text, 10 characters |  |  |  |
| ACCT-CURR-CYC-CREDIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-CURR-CYC-DEBIT |  | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| ACCT-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| ACCT-GROUP-ID |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(178) | text, 178 characters |  |  |  |

#### CVACT02Y

Source: `app/cpy/CVACT02Y.cpy`.

Record `CARD-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| CARD-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| CARD-CVV-CD |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| CARD-EMBOSSED-NAME |  | X(50) | text, 50 characters |  |  |  |
| CARD-EXPIRAION-DATE |  | X(10) | text, 10 characters |  |  |  |
| CARD-ACTIVE-STATUS |  | X(01) | text, 1 character |  |  |  |
| FILLER |  | X(59) | text, 59 characters |  |  |  |

#### CVACT03Y

Source: `app/cpy/CVACT03Y.cpy`.

Record `CARD-XREF-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| XREF-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| XREF-CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| XREF-ACCT-ID |  | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |

#### CVCRD01Y

Source: `app/cpy/CVCRD01Y.cpy`.

Record `CC-WORK-AREAS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CC-WORK-AREA |  |  | group |  |  |  |
| CCARD-AID | CC-WORK-AREA | X(5) | text, 5 characters |  |  | CCARD-AID-ENTER = ENTER; CCARD-AID-CLEAR = CLEAR; CCARD-AID-PA1 = PA1 ; CCARD-AID-PA2 = PA2 ; CCARD-AID-PFK01 = PFK01; CCARD-AID-PFK02 = PFK02; CCARD-AID-PFK03 = PFK03; CCARD-AID-PFK04 = PFK04; CCARD-AID-PFK05 = PFK05; CCARD-AID-PFK06 = PFK06; CCARD-AID-PFK07 = PFK07; CCARD-AID-PFK08 = PFK08; CCARD-AID-PFK09 = PFK09; CCARD-AID-PFK10 = PFK10; CCARD-AID-PFK11 = PFK11; CCARD-AID-PFK12 = PFK12 |
| CCARD-NEXT-PROG | CC-WORK-AREA | X(8) | text, 8 characters |  |  |  |
| CCARD-NEXT-MAPSET | CC-WORK-AREA | X(7) | text, 7 characters |  |  |  |
| CCARD-NEXT-MAP | CC-WORK-AREA | X(7) | text, 7 characters |  |  |  |
| CCARD-ERROR-MSG | CC-WORK-AREA | X(75) | text, 75 characters |  |  |  |
| CCARD-RETURN-MSG | CC-WORK-AREA | X(75) | text, 75 characters |  |  | CCARD-RETURN-MSG-OFF = |
| CC-ACCT-ID | CC-WORK-AREA | X(11) | text, 11 characters |  |  |  |
| CC-ACCT-ID-N | CC-WORK-AREA | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  | redefines CC-ACCT-ID |
| CC-CARD-NUM | CC-WORK-AREA | X(16) | text, 16 characters |  |  |  |
| CC-CARD-NUM-N | CC-WORK-AREA | 9(16) | unsigned integer, 16 digits (zoned decimal) |  |  | redefines CC-CARD-NUM |
| CC-CUST-ID | CC-WORK-AREA | X(09) | text, 9 characters |  |  |  |
| CC-CUST-ID-N | CC-WORK-AREA | 9(9) | unsigned integer, 9 digits (zoned decimal) |  |  | redefines CC-CUST-ID |

#### CVCUS01Y

Source: `app/cpy/CVCUS01Y.cpy`.

Record `CUSTOMER-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| CUST-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-FIRST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-MIDDLE-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-LAST-NAME |  | X(25) | text, 25 characters |  |  |  |
| CUST-ADDR-LINE-1 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-2 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-LINE-3 |  | X(50) | text, 50 characters |  |  |  |
| CUST-ADDR-STATE-CD |  | X(02) | text, 2 characters |  |  |  |
| CUST-ADDR-COUNTRY-CD |  | X(03) | text, 3 characters |  |  |  |
| CUST-ADDR-ZIP |  | X(10) | text, 10 characters |  |  |  |
| CUST-PHONE-NUM-1 |  | X(15) | text, 15 characters |  |  |  |
| CUST-PHONE-NUM-2 |  | X(15) | text, 15 characters |  |  |  |
| CUST-SSN |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| CUST-GOVT-ISSUED-ID |  | X(20) | text, 20 characters |  |  |  |
| CUST-DOB-YYYY-MM-DD |  | X(10) | text, 10 characters |  |  |  |
| CUST-EFT-ACCOUNT-ID |  | X(10) | text, 10 characters |  |  |  |
| CUST-PRI-CARD-HOLDER-IND |  | X(01) | text, 1 character |  |  |  |
| CUST-FICO-CREDIT-SCORE |  | 9(03) | unsigned integer, 3 digits (zoned decimal) |  |  |  |
| FILLER |  | X(168) | text, 168 characters |  |  |  |

#### CVEXPORT

Source: `app/cpy/CVEXPORT.cpy`.

Record `EXPORT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| EXPORT-REC-TYPE |  | X(1) | text, 1 character |  |  |  |
| EXPORT-TIMESTAMP |  | X(26) | text, 26 characters |  |  |  |
| EXPORT-TIMESTAMP-R |  |  | group |  |  | redefines EXPORT-TIMESTAMP |
| EXPORT-DATE | EXPORT-TIMESTAMP-R | X(10) | text, 10 characters |  |  |  |
| EXPORT-DATE-TIME-SEP | EXPORT-TIMESTAMP-R | X(1) | text, 1 character |  |  |  |
| EXPORT-TIME | EXPORT-TIMESTAMP-R | X(15) | text, 15 characters |  |  |  |
| EXPORT-SEQUENCE-NUM |  | 9(9) COMP | unsigned integer, 9 digits (binary) |  |  |  |
| EXPORT-BRANCH-ID |  | X(4) | text, 4 characters |  |  |  |
| EXPORT-REGION-CODE |  | X(5) | text, 5 characters |  |  |  |
| EXPORT-RECORD-DATA |  | X(460) | text, 460 characters |  |  |  |
| EXPORT-CUSTOMER-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-CUST-ID | EXPORT-CUSTOMER-DATA | 9(09) COMP | unsigned integer, 9 digits (binary) |  |  |  |
| EXP-CUST-FIRST-NAME | EXPORT-CUSTOMER-DATA | X(25) | text, 25 characters |  |  |  |
| EXP-CUST-MIDDLE-NAME | EXPORT-CUSTOMER-DATA | X(25) | text, 25 characters |  |  |  |
| EXP-CUST-LAST-NAME | EXPORT-CUSTOMER-DATA | X(25) | text, 25 characters |  |  |  |
| EXP-CUST-ADDR-LINES | EXPORT-CUSTOMER-DATA |  | group |  |  | occurs 3 |
| EXP-CUST-ADDR-LINE | EXPORT-CUSTOMER-DATA/EXP-CUST-ADDR-LINES | X(50) | text, 50 characters |  |  |  |
| EXP-CUST-ADDR-STATE-CD | EXPORT-CUSTOMER-DATA | X(02) | text, 2 characters |  |  |  |
| EXP-CUST-ADDR-COUNTRY-CD | EXPORT-CUSTOMER-DATA | X(03) | text, 3 characters |  |  |  |
| EXP-CUST-ADDR-ZIP | EXPORT-CUSTOMER-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-CUST-PHONE-NUMS | EXPORT-CUSTOMER-DATA |  | group |  |  | occurs 2 |
| EXP-CUST-PHONE-NUM | EXPORT-CUSTOMER-DATA/EXP-CUST-PHONE-NUMS | X(15) | text, 15 characters |  |  |  |
| EXP-CUST-SSN | EXPORT-CUSTOMER-DATA | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| EXP-CUST-GOVT-ISSUED-ID | EXPORT-CUSTOMER-DATA | X(20) | text, 20 characters |  |  |  |
| EXP-CUST-DOB-YYYY-MM-DD | EXPORT-CUSTOMER-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-CUST-EFT-ACCOUNT-ID | EXPORT-CUSTOMER-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-CUST-PRI-CARD-HOLDER-IND | EXPORT-CUSTOMER-DATA | X(01) | text, 1 character |  |  |  |
| EXP-CUST-FICO-CREDIT-SCORE | EXPORT-CUSTOMER-DATA | 9(03) COMP-3 | unsigned integer, 3 digits (packed decimal) |  |  |  |
| FILLER | EXPORT-CUSTOMER-DATA | X(134) | text, 134 characters |  |  |  |
| EXPORT-ACCOUNT-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-ACCT-ID | EXPORT-ACCOUNT-DATA | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| EXP-ACCT-ACTIVE-STATUS | EXPORT-ACCOUNT-DATA | X(01) | text, 1 character |  |  |  |
| EXP-ACCT-CURR-BAL | EXPORT-ACCOUNT-DATA | S9(10)V99 COMP-3 | signed decimal, 10 integer and 2 fraction digits (packed decimal) |  |  |  |
| EXP-ACCT-CREDIT-LIMIT | EXPORT-ACCOUNT-DATA | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| EXP-ACCT-CASH-CREDIT-LIMIT | EXPORT-ACCOUNT-DATA | S9(10)V99 COMP-3 | signed decimal, 10 integer and 2 fraction digits (packed decimal) |  |  |  |
| EXP-ACCT-OPEN-DATE | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-ACCT-EXPIRAION-DATE | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-ACCT-REISSUE-DATE | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-ACCT-CURR-CYC-CREDIT | EXPORT-ACCOUNT-DATA | S9(10)V99 | signed decimal, 10 integer and 2 fraction digits (zoned decimal) |  |  |  |
| EXP-ACCT-CURR-CYC-DEBIT | EXPORT-ACCOUNT-DATA | S9(10)V99 COMP | signed decimal, 10 integer and 2 fraction digits (binary) |  |  |  |
| EXP-ACCT-ADDR-ZIP | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-ACCT-GROUP-ID | EXPORT-ACCOUNT-DATA | X(10) | text, 10 characters |  |  |  |
| FILLER | EXPORT-ACCOUNT-DATA | X(352) | text, 352 characters |  |  |  |
| EXPORT-TRANSACTION-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-TRAN-ID | EXPORT-TRANSACTION-DATA | X(16) | text, 16 characters |  |  |  |
| EXP-TRAN-TYPE-CD | EXPORT-TRANSACTION-DATA | X(02) | text, 2 characters |  |  |  |
| EXP-TRAN-CAT-CD | EXPORT-TRANSACTION-DATA | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| EXP-TRAN-SOURCE | EXPORT-TRANSACTION-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-TRAN-DESC | EXPORT-TRANSACTION-DATA | X(100) | text, 100 characters |  |  |  |
| EXP-TRAN-AMT | EXPORT-TRANSACTION-DATA | S9(09)V99 COMP-3 | signed decimal, 9 integer and 2 fraction digits (packed decimal) |  |  |  |
| EXP-TRAN-MERCHANT-ID | EXPORT-TRANSACTION-DATA | 9(09) COMP | unsigned integer, 9 digits (binary) |  |  |  |
| EXP-TRAN-MERCHANT-NAME | EXPORT-TRANSACTION-DATA | X(50) | text, 50 characters |  |  |  |
| EXP-TRAN-MERCHANT-CITY | EXPORT-TRANSACTION-DATA | X(50) | text, 50 characters |  |  |  |
| EXP-TRAN-MERCHANT-ZIP | EXPORT-TRANSACTION-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-TRAN-CARD-NUM | EXPORT-TRANSACTION-DATA | X(16) | text, 16 characters |  |  |  |
| EXP-TRAN-ORIG-TS | EXPORT-TRANSACTION-DATA | X(26) | text, 26 characters |  |  |  |
| EXP-TRAN-PROC-TS | EXPORT-TRANSACTION-DATA | X(26) | text, 26 characters |  |  |  |
| FILLER | EXPORT-TRANSACTION-DATA | X(140) | text, 140 characters |  |  |  |
| EXPORT-CARD-XREF-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-XREF-CARD-NUM | EXPORT-CARD-XREF-DATA | X(16) | text, 16 characters |  |  |  |
| EXP-XREF-CUST-ID | EXPORT-CARD-XREF-DATA | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| EXP-XREF-ACCT-ID | EXPORT-CARD-XREF-DATA | 9(11) COMP | unsigned integer, 11 digits (binary) |  |  |  |
| FILLER | EXPORT-CARD-XREF-DATA | X(427) | text, 427 characters |  |  |  |
| EXPORT-CARD-DATA |  |  | group |  |  | redefines EXPORT-RECORD-DATA |
| EXP-CARD-NUM | EXPORT-CARD-DATA | X(16) | text, 16 characters |  |  |  |
| EXP-CARD-ACCT-ID | EXPORT-CARD-DATA | 9(11) COMP | unsigned integer, 11 digits (binary) |  |  |  |
| EXP-CARD-CVV-CD | EXPORT-CARD-DATA | 9(03) COMP | unsigned integer, 3 digits (binary) |  |  |  |
| EXP-CARD-EMBOSSED-NAME | EXPORT-CARD-DATA | X(50) | text, 50 characters |  |  |  |
| EXP-CARD-EXPIRAION-DATE | EXPORT-CARD-DATA | X(10) | text, 10 characters |  |  |  |
| EXP-CARD-ACTIVE-STATUS | EXPORT-CARD-DATA | X(01) | text, 1 character |  |  |  |
| FILLER | EXPORT-CARD-DATA | X(373) | text, 373 characters |  |  |  |

#### CVTRA01Y

Source: `app/cpy/CVTRA01Y.cpy`.

Record `TRAN-CAT-BAL-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-CAT-KEY |  |  | group |  |  |  |
| TRANCAT-ACCT-ID | TRAN-CAT-KEY | 9(11) | unsigned integer, 11 digits (zoned decimal) |  |  |  |
| TRANCAT-TYPE-CD | TRAN-CAT-KEY | X(02) | text, 2 characters |  |  |  |
| TRANCAT-CD | TRAN-CAT-KEY | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-CAT-BAL |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| FILLER |  | X(22) | text, 22 characters |  |  |  |

#### CVTRA02Y

Source: `app/cpy/CVTRA02Y.cpy`.

Record `DIS-GROUP-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| DIS-GROUP-KEY |  |  | group |  |  |  |
| DIS-ACCT-GROUP-ID | DIS-GROUP-KEY | X(10) | text, 10 characters |  |  |  |
| DIS-TRAN-TYPE-CD | DIS-GROUP-KEY | X(02) | text, 2 characters |  |  |  |
| DIS-TRAN-CAT-CD | DIS-GROUP-KEY | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| DIS-INT-RATE |  | S9(04)V99 | signed decimal, 4 integer and 2 fraction digits (zoned decimal) |  |  |  |
| FILLER |  | X(28) | text, 28 characters |  |  |  |

#### CVTRA03Y

Source: `app/cpy/CVTRA03Y.cpy`.

Record `TRAN-TYPE-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-TYPE |  | X(02) | text, 2 characters |  |  |  |
| TRAN-TYPE-DESC |  | X(50) | text, 50 characters |  |  |  |
| FILLER |  | X(08) | text, 8 characters |  |  |  |

#### CVTRA04Y

Source: `app/cpy/CVTRA04Y.cpy`.

Record `TRAN-CAT-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-CAT-KEY |  |  | group |  |  |  |
| TRAN-TYPE-CD | TRAN-CAT-KEY | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD | TRAN-CAT-KEY | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-CAT-TYPE-DESC |  | X(50) | text, 50 characters |  |  |  |
| FILLER |  | X(04) | text, 4 characters |  |  |  |

#### CVTRA05Y

Source: `app/cpy/CVTRA05Y.cpy`.

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

#### CVTRA06Y

Source: `app/cpy/CVTRA06Y.cpy`.

Record `DALYTRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| DALYTRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| DALYTRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| DALYTRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| DALYTRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| DALYTRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| DALYTRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| DALYTRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| DALYTRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| DALYTRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| DALYTRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| DALYTRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| DALYTRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| DALYTRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

#### CVTRA07Y

Source: `app/cpy/CVTRA07Y.cpy`.

Record `REPORT-NAME-HEADER`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| REPT-SHORT-NAME |  | X(38) | text, 38 characters |  |  |  |
| REPT-LONG-NAME |  | X(41) | text, 41 characters |  |  |  |
| REPT-DATE-HEADER |  | X(12) | text, 12 characters |  |  |  |
| REPT-START-DATE |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(04) | text, 4 characters |  |  |  |
| REPT-END-DATE |  | X(10) | text, 10 characters |  |  |  |

Record `TRANSACTION-DETAIL-REPORT`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-REPORT-TRANS-ID |  | X(16) | text, 16 characters |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| TRAN-REPORT-ACCOUNT-ID |  | X(11) | text, 11 characters |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| TRAN-REPORT-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| TRAN-REPORT-TYPE-DESC |  | X(15) | text, 15 characters |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| TRAN-REPORT-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| TRAN-REPORT-CAT-DESC |  | X(29) | text, 29 characters |  |  |  |
| FILLER |  | X(01) | text, 1 character |  |  |  |
| TRAN-REPORT-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| FILLER |  | X(04) | text, 4 characters |  |  |  |
| TRAN-REPORT-AMT |  | -ZZZ,ZZZ,ZZZ.ZZ | formatted text, 15 characters (a number shown with 11 digits) |  |  |  |
| FILLER |  | X(02) | text, 2 characters |  |  |  |

Record `TRANSACTION-HEADER-1`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| FILLER |  | X(17) | text, 17 characters |  |  |  |
| FILLER |  | X(12) | text, 12 characters |  |  |  |
| FILLER |  | X(19) | text, 19 characters |  |  |  |
| FILLER |  | X(35) | text, 35 characters |  |  |  |
| FILLER |  | X(14) | text, 14 characters |  |  |  |
| FILLER |  | X | text, 1 character |  |  |  |
| FILLER |  | X(16) | text, 16 characters |  |  |  |

Record `TRANSACTION-HEADER-2`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRANSACTION-HEADER-2 |  | X(133) | text, 133 characters |  |  |  |

Record `REPORT-PAGE-TOTALS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| FILLER |  | X(11) | text, 11 characters |  |  |  |
| FILLER |  | X(86) | text, 86 characters |  |  |  |
| REPT-PAGE-TOTAL |  | +ZZZ,ZZZ,ZZZ.ZZ | formatted text, 15 characters (a number shown with 11 digits) |  |  |  |

Record `REPORT-ACCOUNT-TOTALS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| FILLER |  | X(13) | text, 13 characters |  |  |  |
| FILLER |  | X(84) | text, 84 characters |  |  |  |
| REPT-ACCOUNT-TOTAL |  | +ZZZ,ZZZ,ZZZ.ZZ | formatted text, 15 characters (a number shown with 11 digits) |  |  |  |

Record `REPORT-GRAND-TOTALS`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| FILLER |  | X(11) | text, 11 characters |  |  |  |
| FILLER |  | X(86) | text, 86 characters |  |  |  |
| REPT-GRAND-TOTAL |  | +ZZZ,ZZZ,ZZZ.ZZ | formatted text, 15 characters (a number shown with 11 digits) |  |  |  |

#### IMSFUNCS

Source: `app/app-authorization-ims-db2-mq/cpy/IMSFUNCS.cpy`.

Record `FUNC-CODES`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| FUNC-GU |  | X(04) | text, 4 characters |  |  |  |
| FUNC-GHU |  | X(04) | text, 4 characters |  |  |  |
| FUNC-GN |  | X(04) | text, 4 characters |  |  |  |
| FUNC-GHN |  | X(04) | text, 4 characters |  |  |  |
| FUNC-GNP |  | X(04) | text, 4 characters |  |  |  |
| FUNC-GHNP |  | X(04) | text, 4 characters |  |  |  |
| FUNC-REPL |  | X(04) | text, 4 characters |  |  |  |
| FUNC-ISRT |  | X(04) | text, 4 characters |  |  |  |
| FUNC-DLET |  | X(04) | text, 4 characters |  |  |  |
| PARMCOUNT |  | S9(05) COMP-5 | signed integer, 5 digits (native binary) |  |  |  |

#### PADFLPCB

Source: `app/app-authorization-ims-db2-mq/cpy/PADFLPCB.CPY`.

Record `PADFLPCB`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PADFL-DBDNAME |  | X(08) | text, 8 characters |  |  |  |
| PADFL-SEG-LEVEL |  | X(02) | text, 2 characters |  |  |  |
| PADFL-PCB-STATUS |  | X(02) | text, 2 characters |  |  |  |
| PADFL-PCB-PROCOPT |  | X(04) | text, 4 characters |  |  |  |
| FILLER |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PADFL-SEG-NAME |  | X(08) | text, 8 characters |  |  |  |
| PADFL-KEYFB-NAME |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PADFL-NUM-SENSEGS |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PADFL-KEYFB |  | X(255) | text, 255 characters |  |  |  |

#### PASFLPCB

Source: `app/app-authorization-ims-db2-mq/cpy/PASFLPCB.CPY`.

Record `PASFLPCB`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PASFL-DBDNAME |  | X(08) | text, 8 characters |  |  |  |
| PASFL-SEG-LEVEL |  | X(02) | text, 2 characters |  |  |  |
| PASFL-PCB-STATUS |  | X(02) | text, 2 characters |  |  |  |
| PASFL-PCB-PROCOPT |  | X(04) | text, 4 characters |  |  |  |
| FILLER |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PASFL-SEG-NAME |  | X(08) | text, 8 characters |  |  |  |
| PASFL-KEYFB-NAME |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PASFL-NUM-SENSEGS |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PASFL-KEYFB |  | X(100) | text, 100 characters |  |  |  |

#### PAUTBPCB

Source: `app/app-authorization-ims-db2-mq/cpy/PAUTBPCB.CPY`.

Record `PAUTBPCB`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| PAUT-DBDNAME |  | X(08) | text, 8 characters |  |  |  |
| PAUT-SEG-LEVEL |  | X(02) | text, 2 characters |  |  |  |
| PAUT-PCB-STATUS |  | X(02) | text, 2 characters |  |  |  |
| PAUT-PCB-PROCOPT |  | X(04) | text, 4 characters |  |  |  |
| FILLER |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PAUT-SEG-NAME |  | X(08) | text, 8 characters |  |  |  |
| PAUT-KEYFB-NAME |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PAUT-NUM-SENSEGS |  | S9(05) COMP | signed integer, 5 digits (binary) |  |  |  |
| PAUT-KEYFB |  | X(255) | text, 255 characters |  |  |  |
