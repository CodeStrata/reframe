# Design: Answer system date requests from the queue (CAFM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

A message-driven service that tells calling systems the host's current date and time. Each request gets one reply reading 'SYSTEM DATE : <mm-dd-yyyy>SYSTEM TIME : <time>' on the date reply queue, carrying the request's message and correlation identifiers. Every queue failure must be reported on the error queue, or on the console if the error queue itself is unavailable.

Runs as online.

## Screens and components

No screens: it runs as online.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-031 | Identify request queue from trigger | design note | WHEN the date inquiry transaction (CDRD) is started by a message arriving on its request queue, THE date inquiry service SHALL read the triggering queue's name, use it as the request queue, and always use 'CARD.DEMO.REPLY.DATE' as the reply queue. | high | app/app-vsam-mq/cbl/CODATE01.cbl:140-159, app/app-vsam-mq/cbl/CODATE01.cbl:312-322, app/app-vsam-mq/cbl/CODATE01.cbl:366-403, app/app-vsam-mq/cbl/CODATE01.cbl:243 |
| CAFM-BR-032 | Triggered drain-the-queue processing loop with per-message commit | design note | WHEN the date inquiry transaction starts, THE date inquiry service SHALL read and answer request messages one after another, committing each read-and-reply before reading the next, until no message arrives within 5 seconds, and then close its queues and end. | medium | app/app-vsam-mq/cbl/CODATE01.cbl:163-167, app/app-vsam-mq/cbl/CODATE01.cbl:274-337 |
| CAFM-BR-033 | Build system date and time reply | formatting | WHEN a date request message has been received, THE Date Reply Composition SHALL compose a reply reading 'SYSTEM DATE : <mm-dd-yyyy>SYSTEM TIME : <time>' from the current system clock and send it | medium | app/app-vsam-mq/cbl/CODATE01.cbl:339-340,343-345,347-353,355-364, app/app-vsam-mq/cbl/CODATE01.cbl:339-364 |
| CAFM-BR-034 | Send date reply to requester | design note | WHEN a date reply has been composed, THE date inquiry service SHALL put it on 'CARD.DEMO.REPLY.DATE' carrying the request's message ID and correlation ID, as a text-format message in the queue manager's code page, within the current unit of work; the requester's own reply-to queue is not used. | high | app/app-vsam-mq/cbl/CODATE01.cbl:140-159, app/app-vsam-mq/cbl/CODATE01.cbl:312-322, app/app-vsam-mq/cbl/CODATE01.cbl:366-403, app/app-vsam-mq/cbl/CODATE01.cbl:243 |
| CAFM-BR-035 | Queue open/close resource lifecycle at termination | design note | WHEN the date inquiry service ends, THE date inquiry service SHALL close each of the request, reply and error queues that it opened successfully, with no special close options, and then return control to CICS. | medium | app/app-vsam-mq/cbl/CODATE01.cbl:442-523, app/app-vsam-mq/cbl/CODATE01.cbl:194, app/app-vsam-mq/cbl/CODATE01.cbl:228, app/app-vsam-mq/cbl/CODATE01.cbl:263 |
| CAFM-BR-036 | Identify request queue from trigger | error handling | WHEN the trigger information cannot be retrieved at start-up, THE date inquiry service SHALL send an error record with location 'CICS RETRIEVE' and the CICS response codes to the error queue 'CARD.DEMO.ERROR', close any open queues and end. | high | app/app-vsam-mq/cbl/CODATE01.cbl:140-159, app/app-vsam-mq/cbl/CODATE01.cbl:312-322, app/app-vsam-mq/cbl/CODATE01.cbl:366-403, app/app-vsam-mq/cbl/CODATE01.cbl:243 |
| CAFM-BR-037 | Triggered drain-the-queue processing loop with per-message commit | error handling | WHEN reading a request fails for any reason other than no message being available, THE date inquiry service SHALL send an error record 'INP MQGET ERR:' with the condition and reason codes and the request queue name to 'CARD.DEMO.ERROR', close its queues and end. | medium | app/app-vsam-mq/cbl/CODATE01.cbl:163-167, app/app-vsam-mq/cbl/CODATE01.cbl:274-337 |
| CAFM-BR-038 | Send date reply to requester | error handling | WHEN putting the date reply fails, THE date inquiry service SHALL send an error record with message 'MQPUT ERR', the condition and reason codes and the reply queue name to 'CARD.DEMO.ERROR', close its open queues and end. | high | app/app-vsam-mq/cbl/CODATE01.cbl:140-159, app/app-vsam-mq/cbl/CODATE01.cbl:312-322, app/app-vsam-mq/cbl/CODATE01.cbl:366-403, app/app-vsam-mq/cbl/CODATE01.cbl:243 |
| CAFM-BR-039 | MQ failure reporting to error queue and termination | error handling | WHEN a queue operation fails, THE date inquiry service SHALL put an error record (failing step text, condition code, reason code and queue name) as a text message on 'CARD.DEMO.ERROR' within the unit of work, then close its open queues and end. | medium | app/app-vsam-mq/cbl/CODATE01.cbl:58-67, app/app-vsam-mq/cbl/CODATE01.cbl:264-270, app/app-vsam-mq/cbl/CODATE01.cbl:396-402, app/app-vsam-mq/cbl/CODATE01.cbl:405-440 |
| CAFM-BR-040 | MQ failure reporting to error queue and termination | error handling | WHEN the error queue itself cannot be opened or written to, THE date inquiry service SHALL write the error record to the system console ('ERR MQOPEN ERR' or 'MQPUT ERR') and end. | medium | app/app-vsam-mq/cbl/CODATE01.cbl:58-67, app/app-vsam-mq/cbl/CODATE01.cbl:264-270, app/app-vsam-mq/cbl/CODATE01.cbl:396-402, app/app-vsam-mq/cbl/CODATE01.cbl:405-440 |
| CAFM-BR-041 | Queue open/close resource lifecycle at termination | error handling | WHEN closing a queue fails, THE date inquiry service SHALL record 'MQCLOSE ERR' with the condition and reason codes and run termination again; only a failed error-queue close is also sent to 'CARD.DEMO.ERROR'. | medium | app/app-vsam-mq/cbl/CODATE01.cbl:442-523, app/app-vsam-mq/cbl/CODATE01.cbl:194, app/app-vsam-mq/cbl/CODATE01.cbl:228, app/app-vsam-mq/cbl/CODATE01.cbl:263 |

### Worked examples

- CAFM-BR-031: triggering queue name = CARD.DEMO.REQUEST.DATE → Requests are read from CARD.DEMO.REQUEST.DATE and replies go to 'CARD.DEMO.REPLY.DATE'
- CAFM-BR-032: requests waiting = 3 → 3 replies are sent, each committed before the next read; after 5 seconds with no new message the transaction closes its queues and ends
- CAFM-BR-032: requests waiting = 0 → The first read waits 5 seconds, finds nothing, and the transaction ends without sending a reply
- CAFM-BR-033: Input queue = empty (no message available) → No reply is composed; the program stops reading and ends.
- CAFM-BR-034: request message ID = X; request correlation ID = Y; request reply-to queue = CLIENT.Q → Reply is put on CARD.DEMO.REPLY.DATE with message ID X and correlation ID Y; nothing goes to CLIENT.Q
- CAFM-BR-035: queues opened = error, request and reply → All three are closed and the transaction returns
- CAFM-BR-035: queues opened = error only (request queue open failed) → Only the error queue is closed and the transaction returns
- CAFM-BR-036: CICS RETRIEVE response = not NORMAL → Error record 'CICS RETRIEVE' 'RESP: ...END' is put on CARD.DEMO.ERROR and the transaction ends
- CAFM-BR-037: read condition code = 2; reason code = 2009 → Error record 'INP MQGET ERR:' 02 02009 with the request queue name goes to CARD.DEMO.ERROR and the transaction ends
- CAFM-BR-038: reply put condition code = 2; reason code = 2053 → Error record 'MQPUT ERR' 02 02053 CARD.DEMO.REPLY.DATE goes to CARD.DEMO.ERROR and the transaction ends
- CAFM-BR-039: failure = reply put; condition code = 2; reason code = 2053 → Error record 'MQPUT ERR' 02 02053 CARD.DEMO.REPLY.DATE is put on CARD.DEMO.ERROR and the transaction ends
- CAFM-BR-040: error queue open condition code = 2 → 'ERR MQOPEN ERR' with CARD.DEMO.ERROR is displayed on the console and the transaction ends
- CAFM-BR-041: error queue close condition code = 2 → 'MQCLOSE ERR' with CARD.DEMO.ERROR is put to the error queue and termination is re-run

## Decision tables

None.

## Design notes

- CAFM-BR-031: Run the date inquiry as a consumer on the queue whose arrival started it. It always replies on the fixed date reply queue ('CARD.DEMO.REPLY.DATE') and ignores any reply-to queue the requester names.
- CAFM-BR-032: Process requests one at a time until the queue is empty: wait up to 5 seconds for each, and stop when none arrives. Take a request and send its reply in one transaction, committed before the next request is taken.
- CAFM-BR-034: Send the reply as a text message in the broker's standard character set, carrying the request's message ID and correlation ID, inside the same transaction that consumed the request.
- CAFM-BR-035: On shutdown, normal or after an error, release every queue connection that was opened (request, reply and error). Release only the ones that opened successfully, then end the task.

## Open questions

- SME-117: The date/time service's error messages contain old-platform texts such as 'CICS RETRIEVE' and 'MQPUT ERR'. Do downstream consumers of the error queue rely on these exact texts, or can they be replaced with neutral wording? (Operations / integration team) On CAFM-BR-033, CAFM-BR-036, CAFM-BR-038.
- SME-118: What exact time format must the date/time service's reply contain (separators, precision)? (Integration team) On CAFM-BR-033, CAFM-BR-036, CAFM-BR-038.
- SME-119: The date/time reply is built in a fixed-size buffer. Do consumers depend on a maximum reply length? (Integration team) On CAFM-BR-033, CAFM-BR-036, CAFM-BR-038.
- SME-120: The date/time reply service is filed under 'Card Authorization and Fraud Management'. Should it be moved to a different business function? (Business analyst) On CAFM-BR-033, CAFM-BR-036, CAFM-BR-038.
- SME-121: Is the content of the system date/time reply critical to the system's core purpose, or costly if wrong, so that it must be matched exactly? (Business owner) On CAFM-BR-033.
- SME-122: Should date/time replies go to the reply queue named by the requester instead of the fixed queue CARD.DEMO.REPLY.DATE, and should replies be matched to requests by the request's message ID instead of its correlation ID? (Integration architect) On CAFM-BR-034.
- SME-123: If the date/time service fails midway, should the request be put back on the queue to retry, instead of being consumed with no reply as today? (Operations / support lead) On CAFM-BR-040.
- SME-124: In the date/time service, is the 'reply queue open' flag (which actually tracks the input queue) only a naming quirk? And if closing a queue fails, should the transaction end without trying to close it again? (Technical lead / MQ administrator) On CAFM-BR-041.
- DEF-087: Is this intended? On a CICS RETRIEVE failure the second response code is moved onto itself instead of into its display field, so the error record always shows RESP2 as zero; also the requester's reply-to queue is saved but ignored, so all replies go to the fixed queue. (Subject-matter expert) On CAFM-BR-036, CAFM-BR-034, CAFM-BR-038.
- DEF-166: Is this intended? A close failure re-performs termination while the open flags are still set, so it retries the same close recursively. A failed reply-queue close is labelled with the request queue name, and request/reply close failures are never sent to the error queue. (Subject-matter expert) On CAFM-BR-041.
- DEF-172: Is this intended? The error-location field is set only for the trigger-retrieve failure, so for every queue failure the record's location is blank and the step can only be read from the message text. (Subject-matter expert) On CAFM-BR-040.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (13 in all).