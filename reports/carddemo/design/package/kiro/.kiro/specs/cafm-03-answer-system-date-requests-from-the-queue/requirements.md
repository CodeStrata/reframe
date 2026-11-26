# Requirements: Answer system date requests from the queue (CAFM-C03)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk low

## Introduction

A message service that answers date requests from other systems with the host's current system date (mm-dd-yyyy) and time on the date reply queue. Each reply carries the request's message and correlation ids. It must never lose or double-answer a request, and it must report every queue failure to the error queue, or to the console if the error queue itself is unavailable.

**User story:** As a requesting system, I want to send a date request message and receive the system date and time on a reply queue, so that I can obtain the host system's current date and time.

## Requirements

### Requirement 1: CAFM-REQ-F-029 (design note)

#### Acceptance criteria

1. When the date inquiry transaction (CDRD) is started by a message arriving on its request queue, the system shall read the triggering queue's name, use it as the request queue, and always use 'CARD.DEMO.REPLY.DATE' as the reply queue. (rules CAFM-BR-031)
2. GIVEN triggering queue name: CARD.DEMO.REQUEST.DATE WHEN the date inquiry transaction (CDRD) is started by a message arriving on its request queue THEN Requests are read from CARD.DEMO.REQUEST.DATE and replies go to 'CARD.DEMO.REPLY.DATE' (CAFM-C03-AC-01; CAFM-BR-031)

### Requirement 2: CAFM-REQ-F-030 (design note)

#### Acceptance criteria

1. When the date inquiry transaction starts, the system shall read and answer request messages one after another, committing each read-and-reply before reading the next, until no message arrives within 5 seconds, and then close its queues and end. (rules CAFM-BR-032)
2. GIVEN requests waiting: 3 WHEN the date inquiry transaction starts THEN 3 replies are sent, each committed before the next read; after 5 seconds with no new message the transaction closes its queues and ends (CAFM-C03-AC-02; CAFM-BR-032)
3. GIVEN requests waiting: 0 WHEN the date inquiry transaction starts THEN The first read waits 5 seconds, finds nothing, and the transaction ends without sending a reply (CAFM-C03-AC-03; CAFM-BR-032)

### Requirement 3: CAFM-REQ-F-031 (formatting)

#### Acceptance criteria

1. When a date request message has been received, the system shall compose a reply reading 'SYSTEM DATE : <mm-dd-yyyy>SYSTEM TIME : <time>' from the current system clock and send it. (rules CAFM-BR-033)
2. GIVEN Input queue: empty (no message available) WHEN a date request message has been received THEN No reply is composed; the program stops reading and ends. (CAFM-C03-AC-04; CAFM-BR-033)

### Requirement 4: CAFM-REQ-F-032 (design note)

#### Acceptance criteria

1. When a date reply has been composed, the system shall put it on 'CARD.DEMO.REPLY.DATE' carrying the request's message ID and correlation ID, as a text-format message in the queue manager's code page, within the current unit of work, without using the requester's own reply-to queue. (rules CAFM-BR-034)
2. GIVEN request message ID: X; request correlation ID: Y; request reply-to queue: CLIENT.Q WHEN a date reply has been composed THEN Reply is put on CARD.DEMO.REPLY.DATE with message ID X and correlation ID Y; nothing goes to CLIENT.Q (CAFM-C03-AC-05; CAFM-BR-034)

### Requirement 5: CAFM-REQ-F-033 (design note)

#### Acceptance criteria

1. When the date inquiry service ends, the system shall close each of the request, reply and error queues that it opened successfully, with no special close options, and then return control to CICS. (rules CAFM-BR-035)
2. GIVEN queues opened: error, request and reply WHEN the date inquiry service ends THEN All three are closed and the transaction returns (CAFM-C03-AC-06; CAFM-BR-035)
3. GIVEN queues opened: error only (request queue open failed) WHEN the date inquiry service ends THEN Only the error queue is closed and the transaction returns (CAFM-C03-AC-07; CAFM-BR-035)

### Requirement 6: CAFM-REQ-F-034 (error handling)

#### Acceptance criteria

1. If the trigger information cannot be retrieved at start-up, then the system shall send an error record with location 'CICS RETRIEVE' and the CICS response codes to the error queue 'CARD.DEMO.ERROR', close any open queues and end. (rules CAFM-BR-036)
2. GIVEN CICS RETRIEVE response: not NORMAL WHEN the trigger information cannot be retrieved at start-up THEN Error record 'CICS RETRIEVE' 'RESP: ...END' is put on CARD.DEMO.ERROR and the transaction ends (CAFM-C03-AC-08; CAFM-BR-036)

### Requirement 7: CAFM-REQ-F-035 (error handling)

#### Acceptance criteria

1. If reading a request fails for any reason other than no message being available, then the system shall send an error record 'INP MQGET ERR:' with the condition and reason codes and the request queue name to 'CARD.DEMO.ERROR', close its queues and end. (rules CAFM-BR-037)
2. GIVEN read condition code: 2; reason code: 2009 WHEN reading a request fails for any reason other than no message being available THEN Error record 'INP MQGET ERR:' 02 02009 with the request queue name goes to CARD.DEMO.ERROR and the transaction ends (CAFM-C03-AC-09; CAFM-BR-037)

### Requirement 8: CAFM-REQ-F-036 (error handling)

#### Acceptance criteria

1. If putting the date reply fails, then the system shall send an error record with message 'MQPUT ERR', the condition and reason codes and the reply queue name to 'CARD.DEMO.ERROR', close its open queues and end. (rules CAFM-BR-038)
2. GIVEN reply put condition code: 2; reason code: 2053 WHEN putting the date reply fails THEN Error record 'MQPUT ERR' 02 02053 CARD.DEMO.REPLY.DATE goes to CARD.DEMO.ERROR and the transaction ends (CAFM-C03-AC-10; CAFM-BR-038)

### Requirement 9: CAFM-REQ-F-037 (error handling)

#### Acceptance criteria

1. If a queue operation fails, then the system shall put an error record (failing step text, condition code, reason code and queue name) as a text message on 'CARD.DEMO.ERROR' within the unit of work, then close its open queues and end. (rules CAFM-BR-039)
2. GIVEN failure: reply put; condition code: 2; reason code: 2053 WHEN a queue operation fails THEN Error record 'MQPUT ERR' 02 02053 CARD.DEMO.REPLY.DATE is put on CARD.DEMO.ERROR and the transaction ends (CAFM-C03-AC-11; CAFM-BR-039)

### Requirement 10: CAFM-REQ-F-038 (error handling)

#### Acceptance criteria

1. If the error queue itself cannot be opened or written to, then the system shall write the error record to the system console ('ERR MQOPEN ERR' or 'MQPUT ERR') and end. (rules CAFM-BR-040)
2. GIVEN error queue open condition code: 2 WHEN the error queue itself cannot be opened or written to THEN 'ERR MQOPEN ERR' with CARD.DEMO.ERROR is displayed on the console and the transaction ends (CAFM-C03-AC-12; CAFM-BR-040)

### Requirement 11: CAFM-REQ-F-039 (error handling)

#### Acceptance criteria

1. If closing a queue fails, then the system shall record 'MQCLOSE ERR' with the condition and reason codes and run termination again, sending only a failed error-queue close to 'CARD.DEMO.ERROR'. (rules CAFM-BR-041)
2. GIVEN error queue close condition code: 2 WHEN closing a queue fails THEN 'MQCLOSE ERR' with CARD.DEMO.ERROR is put to the error queue and termination is re-run (CAFM-C03-AC-13; CAFM-BR-041)
