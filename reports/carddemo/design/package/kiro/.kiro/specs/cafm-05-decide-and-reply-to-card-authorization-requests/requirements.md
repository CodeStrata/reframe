# Requirements: Decide and reply to card authorization requests (CAFM-C05)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk high

## Introduction

The decision and reply step for card authorizations. It approves or declines each request against available credit (credit limit minus balance, taken from the pending summary when there is one, or else from the account) and sends the reply to the payment network in real time. It must never approve an amount strictly greater than the available credit, and a decline always carries response '05' with approved amount 0.

**User story:** As a card payment network, I want each authorization request approved or declined against the account's available credit and answered on my reply queue, so that the merchant transaction can proceed or be refused in real time.

## Requirements

### Requirement 1: CAFM-REQ-F-052 (business rule)

#### Acceptance criteria

1. When the account has a pending-authorization summary, the system shall compute available credit as the summary credit limit minus the summary credit balance and shall decline for insufficient funds when the requested amount is strictly greater than that available credit. (rules CAFM-BR-054)
2. GIVEN summary credit limit: 5000.00; summary credit balance: 4800.00; amount: 250.00 WHEN the account has a pending-authorization summary THEN Declined: response '05', reason '4100' (insufficient funds) (CAFM-C05-AC-01; CAFM-BR-054)
3. GIVEN summary credit limit: 5000.00; summary credit balance: 4800.00; amount: 200.00 WHEN the account has a pending-authorization summary THEN Approved: response '00', approved amount 200.00 (CAFM-C05-AC-02; CAFM-BR-054)

### Requirement 2: CAFM-REQ-F-053 (business rule)

#### Acceptance criteria

1. When the account has no pending-authorization summary but the account record was found, the system shall compute available credit as the account credit limit minus the account current balance and shall decline for insufficient funds when the amount is strictly greater. (rules CAFM-BR-055)
2. GIVEN summary: none; account credit limit: 3000.00; account current balance: 2900.00; amount: 150.00 WHEN the account has no pending-authorization summary but the account record was found THEN Declined: response '05', reason '4100' (CAFM-C05-AC-03; CAFM-BR-055)

### Requirement 3: CAFM-REQ-F-054 (business rule)

#### Acceptance criteria

1. When neither a pending-authorization summary nor the account record is found, the system shall decline the request without an insufficient-funds reason, the reply then carrying reason '3100' because the account is not found. (rules CAFM-BR-056)
2. GIVEN summary: none; account record: not found; amount: 10.00 WHEN neither a pending-authorization summary nor the account record is found THEN Declined: response '05', reason '3100', approved amount 0.00 (CAFM-C05-AC-04; CAFM-BR-056)

### Requirement 4: CAFM-REQ-F-055 (business rule)

#### Acceptance criteria

1. When the authorization decision is decline ('D'), the system shall set response code '05' with approved amount 0, and default the reason to '0000'. (rules CAFM-BR-057)
2. GIVEN Credit limit: 1000.00; Balance: 900.00; Transaction amount: 200.00 WHEN the authorization decision is decline ('D') or approve THEN Declined: response code '05', approved amount 0 (reason then set to '4100'). (CAFM-C05-AC-05; CAFM-BR-057)
3. GIVEN Credit limit: 1000.00; Balance: 100.00; Transaction amount: 200.00 WHEN the authorization decision is decline ('D') or approve THEN Approved: response code '00', approved amount 200.00, reason '0000'. (CAFM-C05-AC-06; CAFM-BR-057)

### Requirement 5: CAFM-REQ-F-056 (business rule)

#### Acceptance criteria

1. When the authorization decision is approve, the system shall set response code '00' with the full transaction amount as the approved amount, and default the reason to '0000'. (rules CAFM-BR-057)
2. GIVEN Credit limit: 1000.00; Balance: 900.00; Transaction amount: 200.00 WHEN the authorization decision is decline ('D') or approve THEN Declined: response code '05', approved amount 0 (reason then set to '4100'). (CAFM-C05-AC-05; CAFM-BR-057)
3. GIVEN Credit limit: 1000.00; Balance: 100.00; Transaction amount: 200.00 WHEN the authorization decision is decline ('D') or approve THEN Approved: response code '00', approved amount 200.00, reason '0000'. (CAFM-C05-AC-06; CAFM-BR-057)

### Requirement 6: CAFM-REQ-F-057 (business rule)

#### Acceptance criteria

1. The system shall carry the request's card number and transaction id in the authorization reply and shall use the request's authorization time as the authorization id code. (rules CAFM-BR-058)
2. GIVEN Card number: 4111111111111111; Transaction id: TX0001; Request auth time: 143015 WHEN authorization reply runs THEN The reply carries card 4111111111111111, transaction TX0001 and authorization id 143015. (CAFM-C05-AC-07; CAFM-BR-058)

### Requirement 7: CAFM-REQ-F-058 (formatting)

#### Acceptance criteria

1. The system shall format the authorization reply as comma-delimited text of card number, transaction id, authorization id, response code, reason code and approved amount (signed, two decimals), each followed by a comma. (rules CAFM-BR-059)
2. GIVEN An authorization decided for card number 4111111111111111, transaction id TXN0001 and authorization id 143005, with response code '00', reason code '0000' and approved amount 125.50 WHEN The authorization reply is formatted THEN The reply text is the card number, transaction id, authorization id, response code '00', reason code '0000' and the approved amount 125.50 written signed with two decimals, in that order, each followed by a comma (the message ends with a comma) (CAFM-C05-AC-09; CAFM-BR-059)

### Requirement 8: CAFM-REQ-F-059 (design note)

#### Acceptance criteria

1. When an authorization decision has been made, the system shall send the non-persistent reply with expiry 50 and the original correlation id through MQPUT1 to the requester's reply queue. (rules CAFM-BR-060)
2. GIVEN MQPUT1 completion code: not MQCC-OK WHEN an authorization decision has been made THEN Critical error logged at location 'M004' with message 'FAILED TO PUT ON REPLY MQ' to queue 'CSSL'; the program ends. (CAFM-C05-AC-08; CAFM-BR-060)

### Requirement 9: CAFM-REQ-F-060 (design note)

#### Acceptance criteria

1. If putting the authorization reply fails, then the system shall log critical error 'M004'. (rules CAFM-BR-060)
2. GIVEN MQPUT1 completion code: not MQCC-OK WHEN an authorization decision has been made THEN Critical error logged at location 'M004' with message 'FAILED TO PUT ON REPLY MQ' to queue 'CSSL'; the program ends. (CAFM-C05-AC-08; CAFM-BR-060)
