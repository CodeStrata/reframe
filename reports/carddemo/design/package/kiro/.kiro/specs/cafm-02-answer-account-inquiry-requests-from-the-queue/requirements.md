# Requirements: Answer account inquiry requests from the queue (CAFM-C02)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

A message-driven service for other systems. It answers an account inquiry request with the account's status, balances, limits and dates on the account reply queue, without the caller needing direct access to the account file. Each reply must carry the request's message and correlation identifiers and must show the stored values exactly as held. A bad request gets an 'INVALID REQUEST PARAMETERS' reply, never another account's data.

**User story:** As a requesting system, I want to send an account inquiry message and receive the account's details on a reply queue, so that I can see an account's status, balances and limits without direct file access.

## Requirements

### Requirement 1: CAFM-REQ-F-014 (design note)

#### Acceptance criteria

1. When the account inquiry transaction (CDRA) is started by an MQ trigger, the system shall read requests from the queue named in the trigger message, send replies to the queue 'CARD.DEMO.REPLY.ACCT' and send error records to the queue 'CARD.DEMO.ERROR'. (rules CAFM-BR-013)
2. GIVEN trigger message queue name: CARD.DEMO.REQUEST.ACCT WHEN the account inquiry transaction (CDRA) is started by an MQ trigger THEN Requests are read from CARD.DEMO.REQUEST.ACCT; replies go to 'CARD.DEMO.REPLY.ACCT'; errors go to 'CARD.DEMO.ERROR'. (CAFM-C02-AC-01; CAFM-BR-013)

### Requirement 2: CAFM-REQ-F-015 (business rule)

#### Acceptance criteria

1. The system shall take request messages one at a time, waiting up to 5 seconds for each, process and answer each one, and stop when no message arrives within 5 seconds, then close the queues it opened and end the task. (rules CAFM-BR-014)
2. GIVEN requests waiting: 3 WHEN account inquiry service runs THEN All 3 requests are answered; after a further 5 seconds with no message the queues are closed and the task ends. (CAFM-C02-AC-02; CAFM-BR-014)
3. GIVEN requests waiting: 0 WHEN account inquiry service runs THEN The service waits 5 seconds, finds nothing, closes the queues and ends without sending any reply. (CAFM-C02-AC-03; CAFM-BR-014)

### Requirement 3: CAFM-REQ-N-002 (design note)

#### Acceptance criteria

1. The system shall take each request and put its reply as one unit of work committed before the next request is taken, with the last request's unit of work committed when the task ends. (rules CAFM-BR-015)
2. GIVEN requests waiting: 2 WHEN account inquiry service runs THEN Request 1 and its reply are committed before request 2 is taken; request 2 and its reply are committed when the task ends. (CAFM-C02-AC-04; CAFM-BR-015)

### Requirement 4: CAFM-REQ-F-016 (design note)

#### Acceptance criteria

1. When a request is taken successfully, the system shall keep its message id and correlation id for the reply and read the first 4 characters as the function code and the next 11 digits as the account number. (rules CAFM-BR-016)
2. GIVEN request message: INQA00000012345 WHEN a request is taken successfully THEN Function code is 'INQA' and account number is 00000012345; the reply carries the request's message id and correlation id. (CAFM-C02-AC-05; CAFM-BR-016)

### Requirement 5: CAFM-REQ-F-017 (historical artifact)

#### Acceptance criteria

1. The system shall always send replies to 'CARD.DEMO.REPLY.ACCT' and shall not use the reply-to queue named in the request. (rules CAFM-BR-017)
2. GIVEN request reply-to queue: MY.REPLY.Q WHEN account inquiry service runs THEN The reply still goes to 'CARD.DEMO.REPLY.ACCT'. (CAFM-C02-AC-06; CAFM-BR-017)

### Requirement 6: CAFM-REQ-F-018 (design note)

#### Acceptance criteria

1. When a reply is ready for the current request, the system shall put the reply on the account reply queue carrying the request's message and correlation identifiers. (rules CAFM-BR-018)
2. GIVEN request message ID: MSG0001; request correlation ID: CORR0001; MQPUT result: OK WHEN a reply is ready for the current request THEN The reply is put on 'CARD.DEMO.REPLY.ACCT' with message ID MSG0001 and correlation ID CORR0001 (CAFM-C02-AC-07; CAFM-BR-018)
3. GIVEN reply queue: 'CARD.DEMO.REPLY.ACCT'; MQPUT result: failed (queue full) WHEN a reply is ready for the current request THEN 'MQPUT ERR' is recorded with the condition and reason codes, the error is sent to the error queue, and the queues are closed and the run ends (CAFM-C02-AC-08; CAFM-BR-018)

### Requirement 7: CAFM-REQ-F-019 (design note)

#### Acceptance criteria

1. If putting the reply fails, then the system shall record 'MQPUT ERR', publish the error and end the run. (rules CAFM-BR-018)
2. GIVEN request message ID: MSG0001; request correlation ID: CORR0001; MQPUT result: OK WHEN a reply is ready for the current request THEN The reply is put on 'CARD.DEMO.REPLY.ACCT' with message ID MSG0001 and correlation ID CORR0001 (CAFM-C02-AC-07; CAFM-BR-018)
3. GIVEN reply queue: 'CARD.DEMO.REPLY.ACCT'; MQPUT result: failed (queue full) WHEN a reply is ready for the current request THEN 'MQPUT ERR' is recorded with the condition and reason codes, the error is sent to the error queue, and the queues are closed and the run ends (CAFM-C02-AC-08; CAFM-BR-018)

### Requirement 8: CAFM-REQ-F-020 (business rule)

#### Acceptance criteria

1. If the function code is not 'INQA' or the account number is zero or less, then the system shall reply 'INVALID REQUEST PARAMETERS ACCT ID : ' with the account number, followed by 'FUNCTION : ' with the function code, without reading the account file. (rules CAFM-BR-019, CAFM-BR-020)
2. GIVEN function code: 'INQA'; account ID: 00000000001 WHEN the function code is not 'INQA' or the account key is zero or less THEN The request is accepted and the account file is read for account 00000000001 (CAFM-C02-AC-09; CAFM-BR-019)

### Requirement 9: CAFM-REQ-F-021 (business rule)

#### Acceptance criteria

1. When a request has function code 'INQA' and an account number greater than zero, the system shall read that account from the account file (ACCTDAT). (rules CAFM-BR-021)
2. GIVEN function code: INQA; account number: 00000012345 WHEN a request has function code 'INQA' and an account number greater than zero THEN Account 00000012345 is looked up in ACCTDAT. (CAFM-C02-AC-10; CAFM-BR-021)

### Requirement 10: CAFM-REQ-F-022 (formatting)

#### Acceptance criteria

1. When the account is found, the system shall reply with 'ACCOUNT ID : ', 'ACCOUNT STATUS : ', 'BALANCE : ', 'CREDIT LIMIT : ', 'CASH LIMIT : ', 'OPEN DATE : ', 'EXPR DATE : ', 'REIS DATE : ', 'CREDIT BAL : ', 'DEBIT BAL : ' and 'GROUP ID : ', each followed by the stored value unchanged, the credit and debit balances being the current billing cycle's. (rules CAFM-BR-022)
2. GIVEN Account 00000000001 is on the account file WHEN A request arrives with function code 'INQA' and account number 00000000001 THEN The reply holds 'ACCOUNT ID : ', 'ACCOUNT STATUS : ', 'BALANCE : ', 'CREDIT LIMIT : ', 'CASH LIMIT : ', 'OPEN DATE : ', 'EXPR DATE : ', 'REIS DATE : ', 'CREDIT BAL : ', 'DEBIT BAL : ' and 'GROUP ID : ', in that order, each followed by the account's stored value unchanged. 'CREDIT BAL : ' and 'DEBIT BAL : ' show the current billing cycle's credit and debit. (CAFM-C02-AC-18; CAFM-BR-022)

### Requirement 11: CAFM-REQ-F-023 (formatting)

#### Acceptance criteria

1. The system shall show amounts in the reply as 12 digits with two implied decimal places, no decimal point and the sign carried in the last digit, exactly as stored. (rules CAFM-BR-023)
2. GIVEN Account 00000000001 is on the account file with a stored current balance of 1234.56 WHEN An 'INQA' request for account 00000000001 is answered THEN The value after 'BALANCE : ' is 12 digits with two implied decimal places and no decimal point, with the sign carried in the last digit, exactly as stored (not shown as '1234.56'). Every other amount in the reply follows the same layout. (CAFM-C02-AC-19; CAFM-BR-023)

### Requirement 12: CAFM-REQ-F-024 (business rule)

#### Acceptance criteria

1. When the account is not on the account file, the system shall reply 'INVALID REQUEST PARAMETERS ACCT ID : ' followed by the 11-digit account number. (rules CAFM-BR-024)
2. GIVEN Account 00000000099 is not on the account file WHEN A request arrives with function code 'INQA' and account number 00000000099 THEN The reply is 'INVALID REQUEST PARAMETERS ACCT ID : ' followed by '00000000099', and no account details are returned. (CAFM-C02-AC-20; CAFM-BR-024)

### Requirement 13: CAFM-REQ-F-025 (error handling)

#### Acceptance criteria

1. If reading the account file returns anything other than found or not found, then the system shall put an error record on 'CARD.DEMO.ERROR' holding the message 'ERROR WHILE READING ACCTF' (cut to 25 characters), the file response and reason codes and the input queue name, send no reply, close the open queues and end the task, with the request just taken committed as consumed. (rules CAFM-BR-025, CAFM-BR-026, CAFM-BR-027)
2. GIVEN account file response: DISABLED (84) WHEN reading the account file returns anything other than found or not found THEN Error record with 'ERROR WHILE READING ACCTF', condition 84 and the input queue name is put to 'CARD.DEMO.ERROR'. (CAFM-C02-AC-11; CAFM-BR-025)
3. GIVEN account file response: DISABLED (84); requests waiting: 2 WHEN such an account file error occurs THEN No reply is sent for the first request; the task ends and the second request stays on the queue for the next trigger. (CAFM-C02-AC-12; CAFM-BR-026)
4. GIVEN account file: disabled WHEN reading the account file fails for any reason other than account not found THEN No reply is sent; an error record goes to 'CARD.DEMO.ERROR' and the task ends. (CAFM-C02-AC-13; CAFM-BR-027)

### Requirement 14: CAFM-REQ-F-026 (error handling)

#### Acceptance criteria

1. If taking a request fails for any reason other than no message being available, then the system shall put an error record with 'INP MQGET ERR:', the condition and reason codes and the input queue name on the error queue, close the open queues and end the task. (rules CAFM-BR-028)
2. GIVEN MQGET condition code: 2 (failed); reason code: 2016 (get inhibited) WHEN taking a request fails for any reason other than no message being available THEN Error record 'INP MQGET ERR:' with codes 02 and 02016 is put to 'CARD.DEMO.ERROR'; the task ends. (CAFM-C02-AC-14; CAFM-BR-028)

### Requirement 15: CAFM-REQ-F-027 (error handling)

#### Acceptance criteria

1. If the trigger data cannot be retrieved, or the input or reply queue cannot be opened, then the system shall put an error record ('CICS RETREIVE' with the response codes, 'INP MQOPEN ERR' or 'OUT MQOPEN ERR' respectively) on the error queue and end the task. (rules CAFM-BR-029)
2. GIVEN input queue open: fails WHEN the trigger data cannot be retrieved, or the input or reply queue cannot be opened THEN Error record 'INP MQOPEN ERR' with the input queue name goes to 'CARD.DEMO.ERROR'; no requests are processed. (CAFM-C02-AC-15; CAFM-BR-029)
3. GIVEN reply queue open: fails WHEN the trigger data cannot be retrieved, or the input or reply queue cannot be opened THEN Error record 'OUT MQOPEN ERR' with queue 'CARD.DEMO.REPLY.ACCT' goes to 'CARD.DEMO.ERROR'; the task ends. (CAFM-C02-AC-16; CAFM-BR-029)

### Requirement 16: CAFM-REQ-F-028 (error handling)

#### Acceptance criteria

1. If the error queue 'CARD.DEMO.ERROR' cannot be opened, then the system shall write 'ERR MQOPEN ERR' with the condition and reason codes to the job log and end the task. (rules CAFM-BR-030)
2. GIVEN error queue open: fails WHEN the error queue 'CARD.DEMO.ERROR' cannot be opened THEN 'ERR MQOPEN ERR' is written to the log and the task ends before any request is read. (CAFM-C02-AC-17; CAFM-BR-030)
