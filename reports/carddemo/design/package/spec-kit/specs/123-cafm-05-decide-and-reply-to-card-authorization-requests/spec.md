# Feature specification: Decide and reply to card authorization requests

**Feature:** CAFM-C05 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C05)

As a card payment network, I want each authorization request approved or declined against the account's available credit and answered on my reply queue, so that the merchant transaction can proceed or be refused in real time.

Approves or declines each card authorization request in real time against the account's available credit, and sends the answer back to the card payment network. Available credit is the credit limit minus the credit balance, taken from the pending-authorization summary when there is one and from the account otherwise. A request is declined only when the amount is strictly greater than that. A decline must always reply '05' with approved amount 0, and an approval '00' with the full amount.

**Acceptance scenarios:**

1. **Given** summary credit limit: 5000.00; summary credit balance: 4800.00; amount: 250.00, **when** the account has a pending-authorization summary, **then** Declined: response '05', reason '4100' (insufficient funds) (CAFM-C05-AC-01)
2. **Given** summary credit limit: 5000.00; summary credit balance: 4800.00; amount: 200.00, **when** the account has a pending-authorization summary, **then** Approved: response '00', approved amount 200.00 (CAFM-C05-AC-02)
3. **Given** summary: none; account credit limit: 3000.00; account current balance: 2900.00; amount: 150.00, **when** the account has no pending-authorization summary but the account record was found, **then** Declined: response '05', reason '4100' (CAFM-C05-AC-03)
4. **Given** summary: none; account record: not found; amount: 10.00, **when** neither a pending-authorization summary nor the account record is found, **then** Declined: response '05', reason '3100', approved amount 0.00 (CAFM-C05-AC-04)
5. **Given** Credit limit: 1000.00; Balance: 900.00; Transaction amount: 200.00, **when** the authorization decision is decline ('D') or approve, **then** Declined: response code '05', approved amount 0 (reason then set to '4100'). (CAFM-C05-AC-05)
6. **Given** Credit limit: 1000.00; Balance: 100.00; Transaction amount: 200.00, **when** the authorization decision is decline ('D') or approve, **then** Approved: response code '00', approved amount 200.00, reason '0000'. (CAFM-C05-AC-06)
7. **Given** Card number: 4111111111111111; Transaction id: TX0001; Request auth time: 143015, **when** authorization reply runs, **then** The reply carries card 4111111111111111, transaction TX0001 and authorization id 143015. (CAFM-C05-AC-07)
8. **Given** MQPUT1 completion code: not MQCC-OK, **when** an authorization decision has been made, **then** Critical error logged at location 'M004' with message 'FAILED TO PUT ON REPLY MQ' to queue 'CSSL'; the program ends. (CAFM-C05-AC-08)
9. **Given** An authorization for card 4111111111111111, transaction id TXN0001 and authorization id 123456, approved with response code '00', reason '0000' and approved amount 125.50, **when** The authorization reply is built, **then** The reply text is the card number, transaction id, authorization id, '00', '0000' and the approved amount with two decimals (125.50, signed), in that order, with a comma after each value, including the last. (CAFM-C05-AC-09)

## Requirements

### Functional requirements

- **CAFM-REQ-F-052** (business rule): When the account has a pending-authorization summary, the system shall compute available credit as the summary credit limit minus the summary credit balance and shall decline for insufficient funds when the requested amount is strictly greater than that available credit. Rules: CAFM-BR-054.
- **CAFM-REQ-F-053** (business rule): When the account has no pending-authorization summary but the account record was found, the system shall compute available credit as the account credit limit minus the account current balance and shall decline for insufficient funds when the amount is strictly greater. Rules: CAFM-BR-055.
- **CAFM-REQ-F-054** (business rule): When neither a pending-authorization summary nor the account record is found, the system shall decline the request without an insufficient-funds reason, the reply then carrying reason '3100' because the account is not found. Rules: CAFM-BR-056.
- **CAFM-REQ-F-055** (business rule): When the authorization decision is decline ('D'), the system shall set response code '05' with approved amount 0, and default the reason to '0000'. Rules: CAFM-BR-057.
- **CAFM-REQ-F-056** (business rule): When the authorization decision is approve, the system shall set response code '00' with the full transaction amount as the approved amount, and default the reason to '0000'. Rules: CAFM-BR-057.
- **CAFM-REQ-F-057** (business rule): The system shall carry the request's card number and transaction id in the authorization reply and shall use the request's authorization time as the authorization id code. Rules: CAFM-BR-058.
- **CAFM-REQ-F-058** (formatting): The system shall format the authorization reply as comma-delimited text of card number, transaction id, authorization id, response code, reason code and approved amount (signed, two decimals), each followed by a comma. Rules: CAFM-BR-059.
- **CAFM-REQ-F-059** (design note): When an authorization decision has been made, the system shall send the non-persistent reply with expiry 50 and the original correlation id through MQPUT1 to the requester's reply queue. Rules: CAFM-BR-060.
- **CAFM-REQ-F-060** (design note): If putting the authorization reply fails, then the system shall log critical error 'M004'. Rules: CAFM-BR-060.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-054 | Check available credit for authorization | business rule | WHEN the account has a pending-authorization summary, THE authorization decision SHALL compute available credit as the summary credit limit minus the summary credit balance, and SHALL decline for insufficient funds when the requested amount is strictly greater than that available credit. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:664-696, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-706 |
| CAFM-BR-055 | Check available credit for authorization | business rule | WHEN the account has no pending-authorization summary but the account record was found, THE authorization decision SHALL compute available credit as the account credit limit minus the account current balance, and SHALL decline for insufficient funds when the amount is strictly greater. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:664-696, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-706 |
| CAFM-BR-056 | Check available credit for authorization | business rule | WHEN neither a pending-authorization summary nor the account record is found, THE authorization decision SHALL decline the request without an insufficient-funds reason (the reply then carries reason '3100' because the account is not found). | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:664-696, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-706 |
| CAFM-BR-057 | Set approve or decline response | business rule | WHEN the authorization decision is decline ('D') or approve, THE Authorization Credit Decision SHALL set response code '05' with approved amount 0 for a decline, or '00' with the full transaction amount for an approval, and default the reason to '0000' | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:685-686,688-696,698, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:685-696 |
| CAFM-BR-058 | Assemble comma-delimited reply content | business rule | THE authorization reply SHALL carry the request's card number and transaction id, and SHALL use the request's authorization time as the authorization id code. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:657-662, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:720-731, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:66, app/app-authorization-ims-db2-mq/cpy/CCPAURLY.cpy:21 |
| CAFM-BR-059 | Assemble comma-delimited reply content | formatting | THE authorization reply SHALL be comma-delimited text of card number, transaction id, authorization id, response code, reason code and approved amount (signed, two decimals), each followed by a comma. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:657-662, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:720-731, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:66, app/app-authorization-ims-db2-mq/cpy/CCPAURLY.cpy:21 |
| CAFM-BR-060 | Send authorization reply message | design note | WHEN an authorization decision has been made, THE Authorization Reply SHALL send the non-persistent reply with expiry 50 and the original correlation id through MQPUT1 to the requester's reply queue, logging critical error 'M004' if the put fails | medium | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:738,741-742,744-751,753-754,756,758-779, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:738-766 |

### Key entities

- CCPAUERY (file record)
- CCPAURQY (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- CCPAURLY (working storage)
- CIPAUDTY (working storage)
- CIPAUSMY (working storage)

### Needs clarification

- SME-131: The authorization reply expiry is given as 50 with no unit. What unit and timeout should the new messaging platform use? (Integration team) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- SME-132: In the pending authorization summary, an approval sets the cash balance to zero instead of adding to it, and the declined-amount total may not use the current request's amount. Is each of these intended, or is it a defect? (Card authorization product owner) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- SME-133: Decline reasons 4200 (card not active), 4300 (account closed), 5100 (card fraud) and 5200 (merchant fraud) are defined, but nothing triggers them. Should these checks be implemented, and what data should drive them? (Card authorization product owner / fraud management team) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- SME-134: The authorization summary is saved before the authorization detail is recorded, so if recording the detail fails, the totals already include it. Must the summary update and the detail record succeed or fail together? (Card authorization business owner) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- SME-135: When a lookup during authorization logs a critical error (C001, C002, C003, I002), should the decision, reply and recording still go ahead for that request? (Card authorization business owner) On CAFM-BR-060, CAFM-BR-057, CAFM-BR-059, CAFM-BR-056.
- DEF-001: Is this intended? The summary-found flag and the decline-reason flag are never reset between messages. When the summary read fails with an IMS error (I002), or the card is unknown, the check uses the summary flag and the limit and balance left over from the previous request in the same run. (Subject-matter expert) On CAFM-BR-055, CAFM-BR-056.
- DEF-139: Is this intended? The STRING pointer for the reply (WS-RESP-LENGTH) starts at 1 and is never reset between messages, so from the second request in a task each reply is appended after the previous replies in the 200-byte buffer and sent with them; after about three replies the buffer overflows. The sent length is also one byte longer than the text. (Subject-matter expert) On CAFM-BR-059.

### Decision table gaps

- Available credit check: R58 decides on the summary alone; the rules do not say whether reason '3100' (account not found) also applies when the summary is found but the account record is not.
