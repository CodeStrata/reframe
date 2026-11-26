# Requirements: Record pending authorization summary and detail (CAFM-C07)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

Records every decided authorization for a known card, both in the account's pending authorization summary (counts, totals, limits, balances) and as a detail record with match status 'P' or 'D' and a blank fraud flag. These records drive later matching, review and purging. They must stay consistent: approved counts and amounts must only reflect approved authorizations, and nothing is recorded for unknown cards.

**User story:** As a card issuer, I want every decided authorization for a known card recorded against the account's pending-authorization summary and as a detail record, so that approved and declined totals and balances are kept current for later matching and review.

## Requirements

### Requirement 1: CAFM-REQ-F-071 (business rule)

#### Acceptance criteria

1. When an authorization for a known card is recorded and the account has no pending-authorization summary yet, the system shall start a new summary with all counts and amounts at zero, carrying the account and customer from the card cross-reference, and add it, and otherwise shall replace the existing summary. (rules CAFM-BR-071, CAFM-BR-072)
2. GIVEN account: 00000000012; existing summary: none; decision: approved 200.00 WHEN an authorization for a known card is recorded and the account has no pending-authorization summary yet THEN A new summary is inserted with approved count 1, approved amount 200.00 and credit balance 200.00 (CAFM-C07-AC-01; CAFM-BR-071)
3. GIVEN Account summary existed: Yes; Decision: approved WHEN a card in the cross-reference has had its authorization decided THEN The existing summary for the account is replaced with the updated totals. (CAFM-C07-AC-02; CAFM-BR-072)
4. GIVEN Account summary existed: No WHEN a card in the cross-reference has had its authorization decided THEN A new summary for the account is inserted. (CAFM-C07-AC-03; CAFM-BR-072)

### Requirement 2: CAFM-REQ-F-072 (business rule)

#### Acceptance criteria

1. When an authorization for a known card is recorded, the system shall set the summary credit limit and cash limit from the account record. (rules CAFM-BR-073)
2. GIVEN account credit limit: 5000.00; account cash credit limit: 1000.00; summary credit limit before: 4000.00 WHEN an authorization for a known card is recorded THEN Summary credit limit becomes 5000.00 and cash limit 1000.00 (CAFM-C07-AC-04; CAFM-BR-073)

### Requirement 3: CAFM-REQ-F-073 (business rule)

#### Acceptance criteria

1. When the authorization is approved, the system shall add 1 to the approved count, add the approved amount to the approved total and to the credit balance, and set the cash balance to 0. (rules CAFM-BR-074)
2. GIVEN credit balance: 1000.00; approved count: 3; approved amount total: 600.00; approved amount: 200.00 WHEN the authorization is approved THEN Approved count 4, approved total 800.00, credit balance 1200.00, cash balance 0 (CAFM-C07-AC-05; CAFM-BR-074)

### Requirement 4: CAFM-REQ-F-074 (business rule)

#### Acceptance criteria

1. When the authorization is declined, the system shall add 1 to the declined count and add to the declined total the transaction amount from the previously recorded authorization detail, not the current request. (rules CAFM-BR-075)
2. GIVEN declined count: 2; declined total: 300.00; current declined amount: 500.00; previous recorded request amount: 40.00 WHEN the authorization is declined THEN Declined count 3, declined total 340.00 (CAFM-C07-AC-06; CAFM-BR-075)

### Requirement 5: CAFM-REQ-F-075 (error handling)

#### Acceptance criteria

1. If adding or replacing the pending authorization summary fails, then the system shall log a critical error at location 'I003' with message 'IMS UPDATE SUMRY FAILED' and the IMS status. (rules CAFM-BR-076, CAFM-BR-077)
2. GIVEN IMS status on summary update: not OK WHEN adding or replacing the summary fails THEN Critical error 'I003' 'IMS UPDATE SUMRY FAILED' logged; the detail insert is still attempted (CAFM-C07-AC-07; CAFM-BR-076)
3. GIVEN IMS status on summary save: II WHEN saving the pending authorization summary fails THEN Error 'I003' 'IMS UPDATE SUMRY FAILED' is logged; no authorization detail is inserted and the task ends. (CAFM-C07-AC-08; CAFM-BR-077)

### Requirement 6: CAFM-REQ-F-076 (design note)

#### Acceptance criteria

1. When an authorization for a known card is recorded, the system shall build an authorization detail from the request (original date and time, card, type, expiry, message type and source, processing code, amount, merchant details, transaction id) and the reply (authorization id code, response code, reason, approved amount), and insert it under the account's summary. (rules CAFM-BR-078)
2. GIVEN account: 00000000012; amount: 75.00; response: '00' WHEN an authorization for a known card is recorded THEN A detail with response '00', reason '0000' and approved amount 75.00 is inserted under the summary for account 00000000012 (CAFM-C07-AC-09; CAFM-BR-078)

### Requirement 7: CAFM-REQ-F-077 (business rule)

#### Acceptance criteria

1. When the authorization detail is recorded, the system shall set match status 'P' (pending) for an approved authorization and 'D' (declined) for a declined one. (rules CAFM-BR-079)
2. GIVEN decision: approved WHEN the authorization detail is recorded THEN Match status 'P' (CAFM-C07-AC-10; CAFM-BR-079)
3. GIVEN decision: declined WHEN the authorization detail is recorded THEN Match status 'D' (CAFM-C07-AC-11; CAFM-BR-079)

### Requirement 8: CAFM-REQ-F-078 (business rule)

#### Acceptance criteria

1. When the authorization detail is recorded, the system shall leave the fraud flag and the fraud report date blank. (rules CAFM-BR-080)
2. GIVEN decision: approved WHEN the authorization detail is recorded THEN Fraud flag ' ', fraud report date blank (CAFM-C07-AC-12; CAFM-BR-080)

### Requirement 9: CAFM-REQ-F-079 (error handling)

#### Acceptance criteria

1. If inserting the authorization detail fails, then the system shall log a critical error at location 'I004' with message 'IMS INSERT DETL FAILED' and the IMS status. (rules CAFM-BR-081)
2. GIVEN IMS status on detail insert: not OK WHEN inserting the authorization detail fails THEN Critical error 'I004' 'IMS INSERT DETL FAILED' logged; the reply already sent is unchanged (CAFM-C07-AC-13; CAFM-BR-081)
