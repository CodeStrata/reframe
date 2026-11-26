# Design: Answer account inquiry requests from the queue (CAFM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A message service that answers account inquiry requests from other systems with the account's status, balances, limits and dates, so they never read the account file directly. Each request is answered on the account reply queue and matched to the request by its message and correlation ids. It must never answer a malformed or unknown-account request with account data, and it must never alter the stored values it reports.

Runs as online.

## Screens and components

No screens: it runs as online.

## Data models

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


## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-013 | Process inquiry requests until queue empty | design note | WHEN the account inquiry transaction (CDRA) is started by an MQ trigger, THE account inquiry service SHALL read requests from the queue named in the trigger message, send replies to the queue 'CARD.DEMO.REPLY.ACCT' and send error records to the queue 'CARD.DEMO.ERROR'. | high | app/app-vsam-mq/cbl/COACCT01.cbl:178-218, app/app-vsam-mq/cbl/COACCT01.cbl:222-253, app/app-vsam-mq/cbl/COACCT01.cbl:255-287, app/app-vsam-mq/cbl/COACCT01.cbl:289-322 |
| CAFM-BR-014 | Process inquiry requests until queue empty | business rule | THE account inquiry service SHALL take request messages one at a time, waiting up to 5 seconds for each, process and answer each one, and stop when no message arrives within 5 seconds (reason MQRC-NO-MSG-AVAILABLE), then close the queues it opened and end the task. | high | app/app-vsam-mq/cbl/COACCT01.cbl:178-218, app/app-vsam-mq/cbl/COACCT01.cbl:222-253, app/app-vsam-mq/cbl/COACCT01.cbl:255-287, app/app-vsam-mq/cbl/COACCT01.cbl:289-322 |
| CAFM-BR-015 | Queue-driven request processing loop with per-message commit | design note | THE account inquiry service SHALL take each request and put its reply as one unit of work, committed (CICS SYNCPOINT) before the next request is taken; the last request's unit of work is committed when the task ends. | high | app/app-vsam-mq/cbl/COACCT01.cbl:178-218, app/app-vsam-mq/cbl/COACCT01.cbl:222-253, app/app-vsam-mq/cbl/COACCT01.cbl:255-287, app/app-vsam-mq/cbl/COACCT01.cbl:289-322 |
| CAFM-BR-016 | Retrieve next inquiry request | design note | WHEN a request is taken successfully, THE account inquiry service SHALL keep its message id and correlation id for the reply and read the first 4 characters as the function code and the next 11 digits as the account number. | high | app/app-vsam-mq/cbl/COACCT01.cbl:178-218, app/app-vsam-mq/cbl/COACCT01.cbl:222-253, app/app-vsam-mq/cbl/COACCT01.cbl:255-287, app/app-vsam-mq/cbl/COACCT01.cbl:289-322 |
| CAFM-BR-017 | Queue-driven request processing loop with per-message commit | historical artifact | THE account inquiry service SHALL always send replies to 'CARD.DEMO.REPLY.ACCT' and SHALL NOT use the reply-to queue named in the request, although it saves that name (SAVE-REPLY2Q). | high | app/app-vsam-mq/cbl/COACCT01.cbl:178-218, app/app-vsam-mq/cbl/COACCT01.cbl:222-253, app/app-vsam-mq/cbl/COACCT01.cbl:255-287, app/app-vsam-mq/cbl/COACCT01.cbl:289-322 |
| CAFM-BR-018 | Send reply to requester | design note | WHEN a reply is ready for the current request, THE Inquiry Reply Delivery SHALL put the reply on the account reply queue carrying the request's message and correlation identifiers; on failure record 'MQPUT ERR', publish the error and end the run (physical store: `CARD.DEMO.REPLY.ACCT`) | medium | app/app-vsam-mq/cbl/COACCT01.cbl:462,467-471,473,475-477,479-486,488-499, app/app-vsam-mq/cbl/COACCT01.cbl:462-499 |
| CAFM-BR-019 | Reject invalid inquiry request | business rule | IF the function code is not 'INQA' or the account key is zero or less, THEN THE Account Inquiry SHALL send an 'INVALID REQUEST PARAMETERS' reply quoting the account ID and function code | medium | app/app-vsam-mq/cbl/COACCT01.cbl:448-457, app/app-vsam-mq/cbl/COACCT01.cbl:390-457 |
| CAFM-BR-020 | Reply with account details | business rule | WHEN the function code is not 'INQA' or the account number is zero, THE account inquiry service SHALL reply 'INVALID REQUEST PARAMETERS ACCT ID : ' with the account number, followed by 'FUNCTION : ' with the function code, without reading the account file. | high | app/app-vsam-mq/cbl/COACCT01.cbl:130-169, app/app-vsam-mq/cbl/COACCT01.cbl:390-457, app/app-vsam-mq/cbl/COACCT01.cbl:109-112, app/cpy/CVACT01Y.cpy:4-17 |
| CAFM-BR-021 | Reply with account details | business rule | WHEN a request has function code 'INQA' and an account number greater than zero, THE account inquiry service SHALL read that account from the account file (ACCTDAT). | high | app/app-vsam-mq/cbl/COACCT01.cbl:130-169, app/app-vsam-mq/cbl/COACCT01.cbl:390-457, app/app-vsam-mq/cbl/COACCT01.cbl:109-112, app/cpy/CVACT01Y.cpy:4-17 |
| CAFM-BR-022 | Reply with account details | formatting | WHEN the account is found, THE account inquiry service SHALL reply with 'ACCOUNT ID : ', 'ACCOUNT STATUS : ', 'BALANCE : ', 'CREDIT LIMIT : ', 'CASH LIMIT : ', 'OPEN DATE : ', 'EXPR DATE : ', 'REIS DATE : ', 'CREDIT BAL : ', 'DEBIT BAL : ' and 'GROUP ID : ', each followed by the stored value unchanged, the credit and debit balances being the current billing cycle's. | high | app/app-vsam-mq/cbl/COACCT01.cbl:130-169, app/app-vsam-mq/cbl/COACCT01.cbl:390-457, app/app-vsam-mq/cbl/COACCT01.cbl:109-112, app/cpy/CVACT01Y.cpy:4-17 |
| CAFM-BR-023 | Account inquiry lookup and reply content | formatting | THE account inquiry service SHALL show amounts in the reply as 12 digits with two implied decimal places, no decimal point and the sign carried in the last digit, exactly as stored. | high | app/app-vsam-mq/cbl/COACCT01.cbl:130-169, app/app-vsam-mq/cbl/COACCT01.cbl:390-457, app/app-vsam-mq/cbl/COACCT01.cbl:109-112, app/cpy/CVACT01Y.cpy:4-17 |
| CAFM-BR-024 | Reply account not found | business rule | WHEN the account is not on the account file, THE account inquiry service SHALL reply 'INVALID REQUEST PARAMETERS ACCT ID : ' followed by the 11-digit account number. | high | app/app-vsam-mq/cbl/COACCT01.cbl:130-169, app/app-vsam-mq/cbl/COACCT01.cbl:390-457, app/app-vsam-mq/cbl/COACCT01.cbl:109-112, app/cpy/CVACT01Y.cpy:4-17 |
| CAFM-BR-025 | Fatal error reporting to error queue and termination | error handling | WHEN reading the account file returns anything other than found or not found, THE account inquiry service SHALL put an error record on 'CARD.DEMO.ERROR' holding the message 'ERROR WHILE READING ACCTF' (cut to 25 characters), the file response and reason codes, and the input queue name. | medium | app/app-vsam-mq/cbl/COACCT01.cbl:58-67, app/app-vsam-mq/cbl/COACCT01.cbl:437-445, app/app-vsam-mq/cbl/COACCT01.cbl:501-536, app/app-vsam-mq/cbl/COACCT01.cbl:538-550 |
| CAFM-BR-026 | Fatal error reporting to error queue and termination | error handling | WHEN such an account file error occurs, THE account inquiry service SHALL send no reply to the requester, close the open queues and end the task, and the request just taken is committed as consumed when the task ends. | medium | app/app-vsam-mq/cbl/COACCT01.cbl:58-67, app/app-vsam-mq/cbl/COACCT01.cbl:437-445, app/app-vsam-mq/cbl/COACCT01.cbl:501-536, app/app-vsam-mq/cbl/COACCT01.cbl:538-550 |
| CAFM-BR-027 | Account inquiry lookup and reply content | error handling | WHEN reading the account file fails for any reason other than account not found, THE account inquiry service SHALL send no reply, put an error record on the error queue and end the task. | high | app/app-vsam-mq/cbl/COACCT01.cbl:130-169, app/app-vsam-mq/cbl/COACCT01.cbl:390-457, app/app-vsam-mq/cbl/COACCT01.cbl:109-112, app/cpy/CVACT01Y.cpy:4-17 |
| CAFM-BR-028 | Retrieve next inquiry request | error handling | WHEN taking a request fails for any reason other than no message being available, THE account inquiry service SHALL put an error record with 'INP MQGET ERR:', the condition and reason codes and the input queue name on the error queue, close the open queues and end the task. | high | app/app-vsam-mq/cbl/COACCT01.cbl:178-218, app/app-vsam-mq/cbl/COACCT01.cbl:222-253, app/app-vsam-mq/cbl/COACCT01.cbl:255-287, app/app-vsam-mq/cbl/COACCT01.cbl:289-322 |
| CAFM-BR-029 | Process inquiry requests until queue empty | error handling | WHEN the trigger data cannot be retrieved, or the input or reply queue cannot be opened, THE account inquiry service SHALL put an error record ('CICS RETREIVE' with the response codes, 'INP MQOPEN ERR' or 'OUT MQOPEN ERR' respectively) on the error queue and end the task. | high | app/app-vsam-mq/cbl/COACCT01.cbl:178-218, app/app-vsam-mq/cbl/COACCT01.cbl:222-253, app/app-vsam-mq/cbl/COACCT01.cbl:255-287, app/app-vsam-mq/cbl/COACCT01.cbl:289-322 |
| CAFM-BR-030 | Process inquiry requests until queue empty | error handling | WHEN the error queue 'CARD.DEMO.ERROR' cannot be opened, THE account inquiry service SHALL write 'ERR MQOPEN ERR' with the condition and reason codes to the job log and end the task. | high | app/app-vsam-mq/cbl/COACCT01.cbl:178-218, app/app-vsam-mq/cbl/COACCT01.cbl:222-253, app/app-vsam-mq/cbl/COACCT01.cbl:255-287, app/app-vsam-mq/cbl/COACCT01.cbl:289-322 |

### Worked examples

- CAFM-BR-013: trigger message queue name = CARD.DEMO.REQUEST.ACCT → Requests are read from CARD.DEMO.REQUEST.ACCT; replies go to 'CARD.DEMO.REPLY.ACCT'; errors go to 'CARD.DEMO.ERROR'.
- CAFM-BR-014: requests waiting = 3 → All 3 requests are answered; after a further 5 seconds with no message the queues are closed and the task ends.
- CAFM-BR-014: requests waiting = 0 → The service waits 5 seconds, finds nothing, closes the queues and ends without sending any reply.
- CAFM-BR-015: requests waiting = 2 → Request 1 and its reply are committed before request 2 is taken; request 2 and its reply are committed when the task ends.
- CAFM-BR-016: request message = INQA00000012345 → Function code is 'INQA' and account number is 00000012345; the reply carries the request's message id and correlation id.
- CAFM-BR-017: request reply-to queue = MY.REPLY.Q → The reply still goes to 'CARD.DEMO.REPLY.ACCT'.
- CAFM-BR-018: request message ID = MSG0001; request correlation ID = CORR0001; MQPUT result = OK → The reply is put on 'CARD.DEMO.REPLY.ACCT' with message ID MSG0001 and correlation ID CORR0001
- CAFM-BR-018: reply queue = 'CARD.DEMO.REPLY.ACCT'; MQPUT result = failed (queue full) → 'MQPUT ERR' is recorded with the condition and reason codes, the error is sent to the error queue, and the queues are closed and the run ends
- CAFM-BR-019: function code = 'INQA'; account ID = 00000000001 → The request is accepted and the account file is read for account 00000000001
- CAFM-BR-021: function code = INQA; account number = 00000012345 → Account 00000012345 is looked up in ACCTDAT.
- CAFM-BR-025: account file response = DISABLED (84) → Error record with 'ERROR WHILE READING ACCTF', condition 84 and the input queue name is put to 'CARD.DEMO.ERROR'.
- CAFM-BR-026: account file response = DISABLED (84); requests waiting = 2 → No reply is sent for the first request; the task ends and the second request stays on the queue for the next trigger.
- CAFM-BR-027: account file = disabled → No reply is sent; an error record goes to 'CARD.DEMO.ERROR' and the task ends.
- CAFM-BR-028: MQGET condition code = 2 (failed); reason code = 2016 (get inhibited) → Error record 'INP MQGET ERR:' with codes 02 and 02016 is put to 'CARD.DEMO.ERROR'; the task ends.
- CAFM-BR-029: input queue open = fails → Error record 'INP MQOPEN ERR' with the input queue name goes to 'CARD.DEMO.ERROR'; no requests are processed.
- CAFM-BR-029: reply queue open = fails → Error record 'OUT MQOPEN ERR' with queue 'CARD.DEMO.REPLY.ACCT' goes to 'CARD.DEMO.ERROR'; the task ends.
- CAFM-BR-030: error queue open = fails → 'ERR MQOPEN ERR' is written to the log and the task ends before any request is read.

## Decision tables

#### Account inquiry reply

| Function code is 'INQA' | Account number greater than zero | Account file read result | Reply sent | Rule |
|---|---|---|---|---|
| No | Any | Not read | Reply 'INVALID REQUEST PARAMETERS ACCT ID : ' with account number and 'FUNCTION : ' with function code | CAFM-BR-020 |
| Yes | No | Not read | Reply 'INVALID REQUEST PARAMETERS ACCT ID : ' with account number and 'FUNCTION : ' with function code | CAFM-BR-019 |
| Yes | Yes | Found | Reply with account details | CAFM-BR-022 |
| Yes | Yes | Not found | Reply 'INVALID REQUEST PARAMETERS ACCT ID : ' with the 11-digit account number | CAFM-BR-024 |
| Yes | Yes | Other error | No reply; error record on 'CARD.DEMO.ERROR'; end task | CAFM-BR-027 |


## Design notes

- CAFM-BR-013: Run the service as a consumer started when messages arrive on the account inquiry request queue. Take the request queue from the start-up event or configuration, and send replies to the fixed queue 'CARD.DEMO.REPLY.ACCT' and error records to 'CARD.DEMO.ERROR'.
- CAFM-BR-015: Treat consuming one request and publishing its reply as one transaction, committed before the next request is taken. A failure then never loses a request or sends a reply twice, and the last request's transaction is committed when the consumer stops.
- CAFM-BR-016: Parse each request as fixed-position text: characters 1-4 are the function code and the next 11 digits are the account number. Keep the message id and correlation id so the reply can be matched to the request.
- CAFM-BR-018: Publish each reply to 'CARD.DEMO.REPLY.ACCT' with the request's message id and correlation id, so the requester can match it. If the publish fails, record 'MQPUT ERR', send the error to the error queue and stop the consumer.

## Open questions

- SME-048: For the account inquiry service, when should the work of reading a request and sending its reply be committed or rolled back: per request, at the end of the run, or on error? (Integration architecture team) On CAFM-BR-019, CAFM-BR-018, CAFM-BR-028, CAFM-BR-030, CAFM-BR-022, CAFM-BR-024.
- SME-049: What are the exact labels and layout for every field in the account inquiry reply? Only 'ACCOUNT ID : ' and 'BALANCE : ' are known. (Card authorization business analyst) On CAFM-BR-019, CAFM-BR-018, CAFM-BR-028, CAFM-BR-030, CAFM-BR-022, CAFM-BR-024.
- SME-050: Where do the function code and account number sit within an account inquiry request message, and how should a non-numeric account number be treated? (Integration architecture team) On CAFM-BR-019, CAFM-BR-018, CAFM-BR-028, CAFM-BR-030, CAFM-BR-022, CAFM-BR-024.
- SME-051: How should the account inquiry service handle an account file read failure other than 'not found', and failures opening or closing queues? What should the published error record contain? (Card authorization business analyst) On CAFM-BR-019, CAFM-BR-018, CAFM-BR-028, CAFM-BR-030, CAFM-BR-022, CAFM-BR-024.
- SME-052: How important is the account inquiry lookup and the content of its reply? Is it critical to the system's core purpose, or a rule that is costly if it goes wrong? (Business owner (account servicing)) On CAFM-BR-027.
- SME-053: Should account inquiry replies go to the reply queue the requester names, or always to the fixed queue CARD.DEMO.REPLY.ACCT for every consumer? (Integration architect) On CAFM-BR-018.
- DEF-069: Is this intended? When the trigger data cannot be retrieved, the code moves the RESP2 code onto itself instead of into its display field, so the error record always shows a RESP2 of 00000000. Also, 'CICS RETREIVE' is misspelled in the error record. (Subject-matter expert) On CAFM-BR-017, CAFM-BR-028, CAFM-BR-030.
- DEF-171: Is this intended? The error text 'ERROR WHILE READING ACCTFILE' (28 characters) is moved into a 25-character field, so the record says 'ERROR WHILE READING ACCTF'; the paragraph field is never filled on this path, and the request is consumed with no reply to the requester. (Subject-matter expert) On CAFM-BR-026.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (20 in all).