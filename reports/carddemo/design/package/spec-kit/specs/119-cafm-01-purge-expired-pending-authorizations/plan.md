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

- CAFM-BR-001: At start-up the job takes the run date from the system clock and reads two run parameters. Expiry days is used when numeric and defaults to 5 otherwise. Checkpoint frequency defaults to 5 when it is blank, zero or missing. Check both values before any data is touched.
- CAFM-BR-002: Run the purge as a scheduled batch job that has update access to the pending authorization store, both summaries and details. It runs alongside the online authorization service, so it must commit in small batches (see the checkpoint frequency) rather than locking the whole store.
- CAFM-BR-004: Read every account summary in turn and, for each one, all of its authorization details. Delete the details that qualify, then decide whether the summary goes too, before moving to the next account. A parent-child query or keyset cursor over summaries with their details is enough. Commit every checkpoint-frequency summaries so a restart can resume from the last committed account.

## Decision tables

#### Purge outcome for an authorization detail

| Age at least expiry days | Response code is '00' | Purge action | Rule |
|---|---|---|---|
| Yes | Yes | Delete detail; subtract 1 from approved count and approved amount from approved total (working copy) | CAFM-BR-009 |
| Yes | No | Delete detail; subtract 1 from declined count and transaction amount from declined total (working copy) | CAFM-BR-010 |
| No | Any | Mark not qualified and keep the detail | CAFM-BR-006 |

