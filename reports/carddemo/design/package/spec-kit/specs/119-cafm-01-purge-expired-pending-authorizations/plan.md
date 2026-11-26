# Implementation plan: Purge expired pending authorizations (CAFM-C01)

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

#### CIPAUSMY

File record of CBPAUP0C. Source: `app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy`.

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

- CIPAUDTY (working storage of CBPAUP0C): see data-contracts.md.

## Design notes

- CAFM-BR-001: The job needs a parameter setup step at start-up: record today's date as the run date, take expiry days from the job parameters when numeric or else use 5, and set the checkpoint frequency to 5 when it is missing, blank or 0. Expose these as validated job configuration, not as positional text.
- CAFM-BR-002: Run the purge as a scheduled batch job with write access to the pending authorization store (summaries and their details). The legacy IMS batch program, PSB and DBD library setup becomes the job's scheduler entry and its database credentials and permissions.
- CAFM-BR-004: The job needs a full pass over all pending authorization summaries, one account at a time, with each summary's child details checked and expired ones deleted before it moves to the next summary. Commit progress at the configured checkpoint frequency so the job can restart after a failure without starting over.

## Decision tables

#### Purge outcome for an authorization detail

| Age at least expiry days | Response code is '00' | Purge action | Rule |
|---|---|---|---|
| Yes | Yes | Delete detail; subtract 1 from approved count and approved amount from approved total (working copy) | CAFM-BR-009 |
| Yes | No | Delete detail; subtract 1 from declined count and transaction amount from declined total (working copy) | CAFM-BR-010 |
| No | Any | Mark not qualified and keep the detail | CAFM-BR-006 |

