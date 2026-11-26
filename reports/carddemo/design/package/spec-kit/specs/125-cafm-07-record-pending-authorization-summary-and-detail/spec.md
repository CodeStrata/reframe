# Feature specification: Record pending authorization summary and detail

**Feature:** CAFM-C07 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C07)

As a card issuer, I want every decided authorization for a known card recorded against the account's pending-authorization summary and as a detail record, so that approved and declined totals and balances are kept current for later matching and review.

Records every decided authorization for a known card against the account's pending-authorization summary and as a detail record, so approved and declined counts, totals and balances stay current for matching and fraud review. Approvals add to the approved count, approved total and credit balance. Each detail is stored with match status 'P' or 'D' and a blank fraud flag. A failure to save must be logged as a critical error ('I003' or 'I004').

**Acceptance scenarios:**

1. **Given** account: 00000000012; existing summary: none; decision: approved 200.00, **when** an authorization for a known card is recorded and the account has no pending-authorization summary yet, **then** A new summary is inserted with approved count 1, approved amount 200.00 and credit balance 200.00 (CAFM-C07-AC-01)
2. **Given** Account summary existed: Yes; Decision: approved, **when** a card in the cross-reference has had its authorization decided, **then** The existing summary for the account is replaced with the updated totals. (CAFM-C07-AC-02)
3. **Given** Account summary existed: No, **when** a card in the cross-reference has had its authorization decided, **then** A new summary for the account is inserted. (CAFM-C07-AC-03)
4. **Given** account credit limit: 5000.00; account cash credit limit: 1000.00; summary credit limit before: 4000.00, **when** an authorization for a known card is recorded, **then** Summary credit limit becomes 5000.00 and cash limit 1000.00 (CAFM-C07-AC-04)
5. **Given** credit balance: 1000.00; approved count: 3; approved amount total: 600.00; approved amount: 200.00, **when** the authorization is approved, **then** Approved count 4, approved total 800.00, credit balance 1200.00, cash balance 0 (CAFM-C07-AC-05)
6. **Given** declined count: 2; declined total: 300.00; current declined amount: 500.00; previous recorded request amount: 40.00, **when** the authorization is declined, **then** Declined count 3, declined total 340.00 (CAFM-C07-AC-06)
7. **Given** IMS status on summary update: not OK, **when** adding or replacing the summary fails, **then** Critical error 'I003' 'IMS UPDATE SUMRY FAILED' logged; the detail insert is still attempted (CAFM-C07-AC-07)
8. **Given** IMS status on summary save: II, **when** saving the pending authorization summary fails, **then** Error 'I003' 'IMS UPDATE SUMRY FAILED' is logged; no authorization detail is inserted and the task ends. (CAFM-C07-AC-08)
9. **Given** account: 00000000012; amount: 75.00; response: '00', **when** an authorization for a known card is recorded, **then** A detail with response '00', reason '0000' and approved amount 75.00 is inserted under the summary for account 00000000012 (CAFM-C07-AC-09)
10. **Given** decision: approved, **when** the authorization detail is recorded, **then** Match status 'P' (CAFM-C07-AC-10)
11. **Given** decision: declined, **when** the authorization detail is recorded, **then** Match status 'D' (CAFM-C07-AC-11)
12. **Given** decision: approved, **when** the authorization detail is recorded, **then** Fraud flag ' ', fraud report date blank (CAFM-C07-AC-12)
13. **Given** IMS status on detail insert: not OK, **when** inserting the authorization detail fails, **then** Critical error 'I004' 'IMS INSERT DETL FAILED' logged; the reply already sent is unchanged (CAFM-C07-AC-13)

## Requirements

### Functional requirements

- **CAFM-REQ-F-071** (business rule): When an authorization for a known card is recorded and the account has no pending-authorization summary yet, the system shall start a new summary with all counts and amounts at zero, carrying the account and customer from the card cross-reference, and add it, and otherwise shall replace the existing summary. Rules: CAFM-BR-071, CAFM-BR-072.
- **CAFM-REQ-F-072** (business rule): When an authorization for a known card is recorded, the system shall set the summary credit limit and cash limit from the account record. Rules: CAFM-BR-073.
- **CAFM-REQ-F-073** (business rule): When the authorization is approved, the system shall add 1 to the approved count, add the approved amount to the approved total and to the credit balance, and set the cash balance to 0. Rules: CAFM-BR-074.
- **CAFM-REQ-F-074** (business rule): When the authorization is declined, the system shall add 1 to the declined count and add to the declined total the transaction amount from the previously recorded authorization detail, not the current request. Rules: CAFM-BR-075.
- **CAFM-REQ-F-075** (error handling): If adding or replacing the pending authorization summary fails, then the system shall log a critical error at location 'I003' with message 'IMS UPDATE SUMRY FAILED' and the IMS status. Rules: CAFM-BR-076, CAFM-BR-077.
- **CAFM-REQ-F-076** (design note): When an authorization for a known card is recorded, the system shall build an authorization detail from the request (original date and time, card, type, expiry, message type and source, processing code, amount, merchant details, transaction id) and the reply (authorization id code, response code, reason, approved amount), and insert it under the account's summary. Rules: CAFM-BR-078.
- **CAFM-REQ-F-077** (business rule): When the authorization detail is recorded, the system shall set match status 'P' (pending) for an approved authorization and 'D' (declined) for a declined one. Rules: CAFM-BR-079.
- **CAFM-REQ-F-078** (business rule): When the authorization detail is recorded, the system shall leave the fraud flag and the fraud report date blank. Rules: CAFM-BR-080.
- **CAFM-REQ-F-079** (error handling): If inserting the authorization detail fails, then the system shall log a critical error at location 'I004' with message 'IMS INSERT DETL FAILED' and the IMS status. Rules: CAFM-BR-081.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-071 | Accumulate pending authorization summary totals | business rule | WHEN an authorization for a known card is recorded and the account has no pending-authorization summary yet, THE summary maintenance SHALL start a new summary with all counts and amounts at zero, carrying the account and customer from the card cross-reference, and add it; otherwise it SHALL replace the existing summary. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-072 | Save pending authorization summary | design note | WHEN a card in the cross-reference has had its authorization decided, THE pending authorization summary maintenance SHALL replace the account's existing summary if one was found, or insert a new summary if none existed (physical store PAUTSUM0). | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:824-847, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:940-977, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:983-1023 |
| CAFM-BR-073 | Accumulate pending authorization summary totals | business rule | WHEN an authorization for a known card is recorded, THE summary maintenance SHALL set the summary credit limit and cash limit from the account record. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-074 | Accumulate pending authorization summary totals | business rule | WHEN the authorization is approved, THE summary maintenance SHALL add 1 to the approved count, add the approved amount to the approved total and to the credit balance, and set the cash balance to 0. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-075 | Accumulate pending authorization summary totals | business rule | WHEN the authorization is declined, THE summary maintenance SHALL add 1 to the declined count and add a transaction amount to the declined total, but the amount it adds is the one from the previously recorded authorization detail, not the current request. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-076 | Accumulate pending authorization summary totals | error handling | WHEN adding or replacing the summary fails, THE summary maintenance SHALL log a critical error at location 'I003' with message 'IMS UPDATE SUMRY FAILED' and the IMS status, and continue on to record the detail. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:798-848, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:854-885 |
| CAFM-BR-077 | Save pending authorization summary | error handling | WHEN saving the pending authorization summary fails, THE authorization processor SHALL log critical error 'I003' with message 'IMS UPDATE SUMRY FAILED' and the IMS status, and SHALL not record the authorization detail for that request. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:824-847, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:940-977, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:983-1023 |
| CAFM-BR-078 | Insert pending authorization detail record | design note | WHEN an authorization for a known card is recorded, THE detail recording SHALL build an authorization detail from the request (original date and time, card, type, expiry, message type and source, processing code, amount, merchant details, transaction id) and the reply (authorization id code, response code, reason, approved amount), and insert it under the account's summary. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:877-932, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:45-53 |
| CAFM-BR-079 | Insert pending authorization detail record | business rule | WHEN the authorization detail is recorded, THE detail recording SHALL set match status 'P' (pending) for an approved authorization and 'D' (declined) for a declined one. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:877-932, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:45-53 |
| CAFM-BR-080 | Insert pending authorization detail record | business rule | WHEN the authorization detail is recorded, THE detail recording SHALL leave the fraud flag and the fraud report date blank. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:877-932, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:45-53 |
| CAFM-BR-081 | Insert pending authorization detail record | error handling | WHEN inserting the authorization detail fails, THE detail recording SHALL log a critical error at location 'I004' with message 'IMS INSERT DETL FAILED' and the IMS status; the insert is attempted even if the summary update just failed. | high | app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:786-792, app/app-authorization-ims-db2-mq/cbl/COPAUA0C.cbl:877-932, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:45-53 |

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

- SME-131: The authorization reply expiry is given as 50 with no unit. What unit and timeout should the new messaging platform use? (Integration team) On CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-132: In the pending authorization summary, an approval sets the cash balance to zero instead of adding to it, and the declined-amount total may not use the current request's amount. Is each of these intended, or is it a defect? (Card authorization product owner) On CAFM-BR-074, CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-133: Decline reasons 4200 (card not active), 4300 (account closed), 5100 (card fraud) and 5200 (merchant fraud) are defined, but nothing triggers them. Should these checks be implemented, and what data should drive them? (Card authorization product owner / fraud management team) On CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-134: The authorization summary is saved before the authorization detail is recorded, so if recording the detail fails, the totals already include it. Must the summary update and the detail record succeed or fail together? (Card authorization business owner) On CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-135: When a lookup during authorization logs a critical error (C001, C002, C003, I002), should the decision, reply and recording still go ahead for that request? (Card authorization business owner) On CAFM-BR-076, CAFM-BR-081, CAFM-BR-077.
- SME-136: If the database fails after an authorization request has been taken off the queue and answered, the request is lost. Is that acceptable, or must such authorizations be reconciled? (Card authorization operations lead) On CAFM-BR-077.
- DEF-002: Is this intended? The declined total adds the transaction amount from the detail segment buffer. That buffer is filled for the current request only later, in 8500-INSERT-AUTH, so it adds the previous recorded request's amount (or zero or garbage for the first one). Also, every approval resets the summary cash balance to 0. (Subject-matter expert) On CAFM-BR-074, CAFM-BR-076.
- DEF-061: Is this intended? Summary and detail failures are only logged. The reply has already been sent, the detail insert goes ahead even after the summary update fails, and the SYNCPOINT at the end of each message commits whatever succeeded, so the summary and its details can fall out of step. (Subject-matter expert) On CAFM-BR-080, CAFM-BR-081.
- DEF-084: Is this intended? The reply to the merchant is sent (without syncpoint) before the summary and detail are written, so when the summary save fails with I003 the merchant has already received the decision (possibly an approval) while no pending authorization summary or detail is recorded for it. (Subject-matter expert) On CAFM-BR-077.

### Decision table gaps

- Pending authorization summary update: Rules disagree: R6 and R19 say the detail insert is still attempted, R21 says the detail is not recorded, and R22 says any critical error ends the task. Confirm whether the detail is recorded after a failed summary save.
- Pending authorization summary update: R5 adds the amount from the previously recorded authorization detail; no rule says which amount is used when there is no previous detail for a new summary.
