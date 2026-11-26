# Design: Purge expired pending authorizations (CAFM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A scheduled job for the card operations team that works through every account's pending authorization summary, deletes each authorization detail that has reached the expiry age, and reduces the account's approved or declined counts and totals for each deleted detail. It deletes a summary once its adjusted approved count is zero or below. It must never delete an authorization younger than the expiry days, and it must stop the run if a deletion fails instead of carrying on with the store half purged.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

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

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-001 | Load run date and purge parameters | design note | THE Purge Parameter Setup SHALL capture the current date, use the supplied expiry days (`P-EXPIRY-DAYS`) when numeric or else default to 5, and default the checkpoint frequency (`P-CHKP-FREQ`) to 5 when it is spaces, 0 or low-values | medium | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:183,187,189,196-203, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:196-209 |
| CAFM-BR-002 | Run the expired authorization purge program | design note | THE expired-authorization purge job SHALL run the purge program (CBPAUP0C) as an IMS batch message program (BMP) with program specification block PSBPAUTB, using the IMS PSB and DBD libraries. | medium | app/app-authorization-ims-db2-mq/jcl/CBPAUP0J.jcl:21-37, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:98-107, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:189-209, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:160-163 |
| CAFM-BR-003 | Run the expired authorization purge program | business rule | THE expired-authorization purge job SHALL pass the control values '00,00001,00001,Y', meaning: authorizations 0 or more days old count as expired, take a checkpoint after more than 1 authorization summary is processed, report every checkpoint, and turn debug messages on. | medium | app/app-authorization-ims-db2-mq/jcl/CBPAUP0J.jcl:21-37, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:98-107, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:189-209, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:160-163 |
| CAFM-BR-004 | Traverse summaries and purge expired details | design note | THE pending authorization purge SHALL read each account's pending authorization summary in turn until the end of the database, check every authorization detail under that summary for expiry, delete each detail that qualifies, and then move on to the next summary. | medium | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:136-167, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:216-241, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:248-271 |
| CAFM-BR-005 | Determine authorization detail expiry | business rule | THE pending authorization purge SHALL work out each authorization's date as 99999 minus its stored inverted date key (Julian YYDDD), and its age as today's Julian date (YYDDD) minus that date. | high | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:277-296, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:303-321, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:377-383, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:186-200 |
| CAFM-BR-006 | Determine authorization detail expiry | business rule | WHEN an authorization's age is at least the expiry days, THE pending authorization purge SHALL mark it as qualified for deletion; otherwise it SHALL mark it as not qualified and keep it. | high | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:277-296, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:303-321, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:377-383, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:186-200 |
| CAFM-BR-007 | Delete expired authorization detail | business rule | WHEN an authorization detail qualifies for deletion, THE pending authorization purge SHALL delete it from the pending authorization detail segment (PAUTDTL1) and add 1 to the details-deleted count. | high | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:277-296, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:303-321, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:377-383, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:186-200 |
| CAFM-BR-008 | Delete expired authorization detail | error handling | WHEN deleting an authorization detail fails, THE pending authorization purge SHALL display 'AUTH DETAIL DELETE FAILED :' with the status and 'AUTH APP ID :' with the account, then display 'CBPAUP0C ABENDING ...' and end the run with return code 16. | high | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:277-296, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:303-321, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:377-383, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:186-200 |
| CAFM-BR-009 | Reduce approved totals for expired detail | business rule | WHEN an authorization detail qualifies for purge and its response code is '00' (approved), THE pending authorization purge SHALL subtract 1 from the account summary's approved count and subtract the detail's approved amount from the summary's approved total, in its working copy of the summary only (the summary record is never rewritten). | high | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:284-296, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:156-158, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:27-30, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:30-35 |
| CAFM-BR-010 | Reduce declined totals for expired detail | business rule | WHEN an authorization detail qualifies for purge and its response code is anything other than '00', THE pending authorization purge SHALL subtract 1 from the account summary's declined count and subtract the detail's transaction amount from the summary's declined total, in its working copy of the summary only (the summary record is never rewritten). | high | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:284-296, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:156-158, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:27-30, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:30-35 |
| CAFM-BR-011 | Reverse summary totals for purged authorizations | business rule | WHEN all of an account summary's details have been checked, THE pending authorization purge SHALL use the adjusted approved count to decide whether to delete the summary, deleting it when the approved count is zero or less. | high | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:284-296, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:156-158, app/app-authorization-ims-db2-mq/cpy/CIPAUSMY.cpy:27-30, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:30-35 |
| CAFM-BR-012 | Delete summary with no remaining approvals | business rule | WHEN the approved authorization count (`PA-APPROVED-AUTH-CNT`) of the processed summary is zero or below, THE Pending Authorization Purge SHALL delete the pending authorization summary from the summary store (`DLI:PAUTSUM0`), and abend the run if the deletion fails | medium | app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:156-158,328,335-338,340,342,345-346, app/app-authorization-ims-db2-mq/cbl/CBPAUP0C.cbl:142-167 |

### Worked examples

- CAFM-BR-001: SYSIN = 00,00001,00001,Y → Expiry days is 0 (numeric, so used as given) and checkpoint frequency stays '00001'.
- CAFM-BR-001: P-EXPIRY-DAYS = 'AB'; P-CHKP-FREQ = spaces → Expiry days defaults to 5 and checkpoint frequency defaults to 5.
- CAFM-BR-001: P-EXPIRY-DAYS = 30; P-CHKP-FREQ = 00000 → Expiry days is 30 and checkpoint frequency is set to 5.
- CAFM-BR-002: Job = CBPAUP0J → Step STEP01 runs DFSRRC00 with PARM 'BMP,CBPAUP0C,PSBPAUTB'.
- CAFM-BR-003: Control values = 00,00001,00001,Y; Authorization age = 0 days (made today) → The authorization qualifies for deletion, because its age is not less than 0 expiry days.
- CAFM-BR-003: Control values = 00,00001,00001,Y → Debug lines such as 'DEBUG: AUTH SMRY READ : ' are printed and 'CHKP SUCCESS: AUTH COUNT - ' is shown after every checkpoint.
- CAFM-BR-004: Summaries in database = 2; Details under first summary = 3, of which 1 expired → All 3 details of the first summary are checked and 1 is deleted before the second summary is read; the run stops when the summary read returns end of database.
- CAFM-BR-005: Stored date key = 74964; Today (YYDDD) = 25040 → Authorization date is 25035 and age is 5 days.
- CAFM-BR-006: Expiry days = 5; Age = 5 → Qualified for deletion.
- CAFM-BR-006: Expiry days = 5; Age = 4 → Kept.
- CAFM-BR-007: Qualified for deletion = Yes; Delete status = blank (success) → Detail removed and '# DETAILS REC DELETED' count increases by 1.
- CAFM-BR-008: Delete status = any non-blank code → Messages 'AUTH DETAIL DELETE FAILED :' and 'CBPAUP0C ABENDING ...' are shown and the job ends with return code 16.
- CAFM-BR-009: Summary approved count = 3; Summary approved total = $450.00; Detail response code = '00'; Detail approved amount = $120.00 → Approved count becomes 2 and approved total becomes $330.00 in the run's working copy; the stored summary is unchanged.
- CAFM-BR-011: Approved count after purge = 0; Declined count after purge = 2 → The summary is deleted even though declined authorizations remain.
- CAFM-BR-012: PA-APPROVED-AUTH-CNT = 0; DIBSTAT = spaces → The summary segment is deleted and '# SUMMARY REC DELETED :' at end of run counts it.
- CAFM-BR-012: PA-APPROVED-AUTH-CNT = 2 → The summary is kept.
- CAFM-BR-012: PA-APPROVED-AUTH-CNT = 0; DIBSTAT = GE → 'AUTH SUMMARY DELETE FAILED :' is displayed with the account id, then 'CBPAUP0C ABENDING ...' and the run ends with return code 16.

## Decision tables

#### Purge outcome for an authorization detail

| Age at least expiry days | Response code is '00' | Purge action | Rule |
|---|---|---|---|
| Yes | Yes | Delete detail; subtract 1 from approved count and approved amount from approved total (working copy) | CAFM-BR-009 |
| Yes | No | Delete detail; subtract 1 from declined count and transaction amount from declined total (working copy) | CAFM-BR-010 |
| No | Any | Mark not qualified and keep the detail | CAFM-BR-006 |


## Design notes

- CAFM-BR-001: The job needs a parameter setup step at start-up: record today's date as the run date, take expiry days from the job parameters when numeric or else use 5, and set the checkpoint frequency to 5 when it is missing, blank or 0. Expose these as validated job configuration, not as positional text.
- CAFM-BR-002: Run the purge as a scheduled batch job with write access to the pending authorization store (summaries and their details). The legacy IMS batch program, PSB and DBD library setup becomes the job's scheduler entry and its database credentials and permissions.
- CAFM-BR-004: The job needs a full pass over all pending authorization summaries, one account at a time, with each summary's child details checked and expired ones deleted before it moves to the next summary. Commit progress at the configured checkpoint frequency so the job can restart after a failure without starting over.

## Open questions

- SME-028: The authorization purge job receives the parameters '00,00001,00001,Y'. What does each value mean (for example expiry days or checkpoint frequency), and would '00' mean authorizations expire after zero days? (Card authorization operations) On CAFM-BR-001, CAFM-BR-012, CAFM-BR-003, CAFM-BR-004, CAFM-BR-009, CAFM-BR-010, CAFM-BR-006, CAFM-BR-008.
- SME-029: When should a pending-authorization summary be deleted: only when both the approved and declined counts are zero and no unexpired details remain under it? (Today the code checks the approved count twice.) (Card authorization business analyst) On CAFM-BR-001, CAFM-BR-012, CAFM-BR-003, CAFM-BR-004, CAFM-BR-009, CAFM-BR-010, CAFM-BR-006, CAFM-BR-008.
- DEF-004: Is this intended? The summary-delete test checks the approved count twice ('PA-APPROVED-AUTH-CNT <= 0 AND PA-APPROVED-AUTH-CNT <= 0'), so a summary is deleted when no approved authorizations remain even if declined ones do; the declined count was almost certainly meant for the second test. (Subject-matter expert) On CAFM-BR-009, CAFM-BR-010, CAFM-BR-011.
- DEF-081: Is this intended? The age is a plain subtraction of YYDDD values, so across a year end it is wrong: an authorization dated 25365 checked on 26001 gets an age of 636 days and is purged after one day. Also, the shipped job passes '00' as expiry days, which is numeric, so the default of 5 is skipped and every detail is purged on every run. (Subject-matter expert) On CAFM-BR-006, CAFM-BR-007, CAFM-BR-008.
- DEF-140: Is this intended? The job passes 00 expiry days, which CBPAUP0C accepts as numeric, so every authorization (including ones made today) qualifies for deletion instead of the program default of 5 days. (Subject-matter expert) On CAFM-BR-003.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (18 in all).