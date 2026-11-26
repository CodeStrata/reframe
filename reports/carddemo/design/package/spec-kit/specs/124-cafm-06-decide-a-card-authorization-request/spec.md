# Feature specification: Decide a card authorization request

**Feature:** CAFM-C06 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C06)

As a card issuer, I want each incoming card authorization request approved or declined against the card, account and customer records, so that only transactions for known cards are approved and every request gets a reply with a clear reason.

The rules that decide each card authorization for the card issuer: look up the card, then its account, customer and pending summary, and approve or decline with a clear reason code. Only known cards may be approved. A card, account or customer that is not found always declines with reason '3100', which takes precedence over insufficient funds ('4100'). Every request gets a reply, even when the card is unknown.

**Acceptance scenarios:**

1. **Given** card number: 4000000000000002 (in cross-reference), **when** an authorization request is processed, **then** Account, customer and summary are read, then the decision is made (CAFM-C06-AC-01)
2. **Given** card number: 4000000000000099 (not in cross-reference), **when** an authorization request is processed, **then** No account, customer or summary is read; the decision is made directly (CAFM-C06-AC-02)
3. **Given** decision: declined; amount: 250.00, **when** the request is declined, **then** Response '05', approved amount 0.00 (CAFM-C06-AC-03)
4. **Given** decision: approved; amount: 75.00, **when** the request is declined, **then** Response '00', approved amount 75.00 (CAFM-C06-AC-04)
5. **Given** card number: 4000000000000099 (not in cross-reference); amount: 50.00, **when** the card is not in the card cross-reference, **then** Reply has response '05', reason '3100', approved amount 0.00 (CAFM-C06-AC-05)
6. **Given** card number: 4000000000000099 (not in cross-reference), **when** the card is not in the card cross-reference, **then** A reply is sent; nothing is written to the pending-authorization database (CAFM-C06-AC-06)
7. **Given** card number: 4000000000000099 (not in cross-reference), **when** the card is not in the card cross-reference, **then** Warning 'A001' 'CARD NOT FOUND IN XREF' logged with key 4000000000000099 (CAFM-C06-AC-07)
8. **Given** cross-reference file: unavailable, **when** reading the card cross-reference fails for any reason other than not found, **then** Critical error 'C001' 'FAILED TO READ XREF FILE' logged; account, customer and summary reads are still attempted and the authorization is recorded (CAFM-C06-AC-08)
9. **Given** decision: approved, **when** an authorization is approved, **then** Reason '0000' (CAFM-C06-AC-09)
10. **Given** card in cross-reference: no; decision: declined, **when** an authorization is declined and the card, **then** Reason '3100' (CAFM-C06-AC-10)
11. **Given** customer record: not found; decision: declined for insufficient funds, **when** an authorization is declined and the card, **then** Reason '3100', not '4100' (CAFM-C06-AC-11)
12. **Given** available credit: 200.00; amount: 250.00, **when** an authorization is declined for insufficient funds and the card, account and customer were all found, **then** Response '05', reason '4100' (CAFM-C06-AC-12)
13. **Given** card status: inactive, **when** reason assignment runs, **then** No '4200' decline is produced; the card is decided on credit only (CAFM-C06-AC-13)

## Requirements

### Functional requirements

- **CAFM-REQ-F-061** (business rule): When an authorization request is processed, the system shall start from an approve decision and look up the card in the card cross-reference, and only when the card is found shall it read the account, the customer and the account's pending-authorization summary before deciding. Rules: CAFM-BR-061.
- **CAFM-REQ-F-062** (business rule): When the request is declined, the system shall reply with response code '05' and approved amount 0, and otherwise shall reply '00' with the full requested amount approved. Rules: CAFM-BR-062.
- **CAFM-REQ-F-063** (business rule): When the card is not in the card cross-reference, the system shall treat the card and its account as not found and decline the request with response '05', reason '3100' and approved amount 0. Rules: CAFM-BR-063.
- **CAFM-REQ-F-064** (business rule): When the card is not in the card cross-reference, the system shall still decide and send a reply but shall not update the pending-authorization summary or record an authorization detail. Rules: CAFM-BR-064.
- **CAFM-REQ-F-065** (side effect): When the card is not in the card cross-reference, the system shall log a warning at location 'A001' with message 'CARD NOT FOUND IN XREF' and the card number as the key. Rules: CAFM-BR-065.
- **CAFM-REQ-F-066** (error handling): If reading the card cross-reference fails for any reason other than not found, then the system shall log a critical error at location 'C001' with message 'FAILED TO READ XREF FILE' and the response codes, and carry on processing the request as if the card had been found. Rules: CAFM-BR-066.
- **CAFM-REQ-F-067** (business rule): When an authorization is approved, the system shall reply with reason code '0000'. Rules: CAFM-BR-067.
- **CAFM-REQ-F-068** (business rule): When an authorization is declined and the card, the account or the customer was not found, the system shall reply with reason code '3100', taking precedence over every other reason. Rules: CAFM-BR-068.
- **CAFM-REQ-F-069** (business rule): When an authorization is declined for insufficient funds and the card, account and customer were all found, the system shall reply with reason code '4100'. Rules: CAFM-BR-069.
- **CAFM-REQ-F-070** (historical artifact): Where a decline is for card not active, account closed, card fraud, merchant fraud or any other cause, the system shall assign reason '4200', '4300', '5100', '5200' or '9000' respectively, although nothing sets these conditions today so these codes are not produced. Rules: CAFM-BR-070.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-061 | Orchestrate single authorization request | business rule | WHEN an authorization request is processed, THE authorization processor SHALL start from an approve decision and look up the card in the card cross-reference; only when the card is found SHALL it read the account, the customer and the account's pending-authorization summary before deciding. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-062 | Available credit check (insufficient funds decline) | business rule | WHEN the request is declined, THE authorization decision SHALL reply with response code '05' and approved amount 0; otherwise it SHALL reply '00' with the full requested amount approved. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:664-696, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-706 |
| CAFM-BR-063 | Look up card in cross-reference | business rule | WHEN the card is not in the card cross-reference, THE authorization processor SHALL treat the card and its account as not found, so the request is declined with response '05', reason '3100' and approved amount 0. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-064 | Orchestrate single authorization request | business rule | WHEN the card is not in the card cross-reference, THE authorization processor SHALL still decide and send a reply, but SHALL NOT update the pending-authorization summary or record an authorization detail. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-065 | Look up card in cross-reference | side effect | WHEN the card is not in the card cross-reference, THE authorization processor SHALL log a warning at location 'A001' with message 'CARD NOT FOUND IN XREF' and the card number as the key. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-066 | Look up card in cross-reference | error handling | WHEN reading the card cross-reference fails for any reason other than not found, THE authorization processor SHALL log a critical error at location 'C001' with message 'FAILED TO READ XREF FILE' and the response codes, and carry on processing the request as if the card had been found. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:438-465, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:472-513, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:672-688, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:699-704 |
| CAFM-BR-067 | Assign decline reason code | business rule | WHEN an authorization is approved, THE authorization reply SHALL carry reason code '0000'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-718, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:140-145, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:665-683 |
| CAFM-BR-068 | Assign decline reason code | business rule | WHEN an authorization is declined and the card, the account or the customer was not found, THE authorization reply SHALL carry reason code '3100'; this takes precedence over every other reason. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-718, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:140-145, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:665-683 |
| CAFM-BR-069 | Assign decline reason code | business rule | WHEN an authorization is declined for insufficient funds and the card, account and customer were all found, THE authorization reply SHALL carry reason code '4100'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-718, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:140-145, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:665-683 |
| CAFM-BR-070 | Assign decline reason code | historical artifact | THE reason assignment SHALL map card not active to '4200', account closed to '4300', card fraud to '5100', merchant fraud to '5200' and any other decline to '9000', but nothing in the program ever sets these conditions, so these codes are not produced today. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:698-718, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:140-145, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:665-683 |

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

- SME-131: The authorization reply expiry is given as 50 with no unit. What unit and timeout should the new messaging platform use? (Integration team) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-070.
- SME-132: In the pending authorization summary, an approval sets the cash balance to zero instead of adding to it, and the declined-amount total may not use the current request's amount. Is each of these intended, or is it a defect? (Card authorization product owner) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-070.
- SME-133: Decline reasons 4200 (card not active), 4300 (account closed), 5100 (card fraud) and 5200 (merchant fraud) are defined, but nothing triggers them. Should these checks be implemented, and what data should drive them? (Card authorization product owner / fraud management team) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-068, CAFM-BR-070.
- SME-134: The authorization summary is saved before the authorization detail is recorded, so if recording the detail fails, the totals already include it. Must the summary update and the detail record succeed or fail together? (Card authorization business owner) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-070.
- SME-135: When a lookup during authorization logs a critical error (C001, C002, C003, I002), should the decision, reply and recording still go ahead for that request? (Card authorization business owner) On CAFM-BR-064, CAFM-BR-066, CAFM-BR-070.
- DEF-001: Is this intended? The summary-found flag and the decline-reason flag are never reset between messages. When the summary read fails with an IMS error (I002), or the card is unknown, the check uses the summary flag and the limit and balance left over from the previous request in the same run. (Subject-matter expert) On CAFM-BR-062.
- DEF-022: Is this intended? The summary-found flag is not reset for each message. For an unknown card, the decision uses the summary-found flag and the limit and balance left over from an earlier request in the same run of up to 500 messages, so an unknown card can be approved. A cross-reference read error (C001) also leaves the card marked as found, and processing goes on with whatever cross-reference data is in memory. (Subject-matter expert) On CAFM-BR-064, CAFM-BR-065, CAFM-BR-066.
- DEF-023: Is this intended? A missing customer record does not cause a decline, but it takes precedence over the reason. A request declined for insufficient funds on an account whose customer is missing is reported as '3100' instead of '4100'. The flags are also never reset between messages. (Subject-matter expert) On CAFM-BR-068, CAFM-BR-070.

### Decision table gaps

- Authorization response and reason code: The rules name an available credit check but do not state how insufficient funds is determined (which balance and limit are compared).
- Authorization response and reason code: R11 carries on as if the card were found, but no rule says what decision or reason results when the account and customer data were not actually read.
