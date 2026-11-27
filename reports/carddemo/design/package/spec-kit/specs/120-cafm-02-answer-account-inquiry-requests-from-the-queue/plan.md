# Implementation plan: Answer account inquiry requests from the queue (CAFM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as online.

## Data model

#### CVACT01Y

File record of COACCT01. Source: `app/cpy/CVACT01Y.cpy`.

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


## Design notes

- CAFM-BR-013: Run the account inquiry as a consumer on the account inquiry request queue, started when messages arrive. It replies on the fixed account reply queue ('CARD.DEMO.REPLY.ACCT') and reports failures to a shared error queue ('CARD.DEMO.ERROR'). Queue names come from configuration, and the request queue is whichever one triggered the consumer.
- CAFM-BR-015: Take a request and send its reply in one transaction, so that a request counts as consumed only when its reply is sent. Commit before taking the next request, and commit the final request's transaction when the consumer stops.
- CAFM-BR-016: Keep each request's message id and correlation id for its reply. Read the request body as fixed positions: characters 1–4 are the function code and the next 11 digits are the account number. Validate the account number as numeric before looking it up.
- CAFM-BR-018: Publish the reply to the account reply queue with the request's message and correlation identifiers, so the caller can match it to its request. If publishing fails, send an 'MQPUT ERR' record to the error queue and stop the consumer.

## Decision tables

#### Account inquiry reply

| Function code is 'INQA' | Account number greater than zero | Account file read result | Reply sent | Rule |
|---|---|---|---|---|
| No | Any | Not read | Reply 'INVALID REQUEST PARAMETERS ACCT ID : ' with account number and 'FUNCTION : ' with function code | CAFM-BR-020 |
| Yes | No | Not read | Reply 'INVALID REQUEST PARAMETERS ACCT ID : ' with account number and 'FUNCTION : ' with function code | CAFM-BR-019 |
| Yes | Yes | Found | Reply with account details | CAFM-BR-022 |
| Yes | Yes | Not found | Reply 'INVALID REQUEST PARAMETERS ACCT ID : ' with the 11-digit account number | CAFM-BR-024 |
| Yes | Yes | Other error | No reply; error record on 'CARD.DEMO.ERROR'; end task | CAFM-BR-027 |

