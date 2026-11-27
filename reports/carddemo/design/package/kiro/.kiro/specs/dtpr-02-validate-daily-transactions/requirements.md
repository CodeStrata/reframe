# Requirements: Validate daily transactions (DTPR-C02)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Checks each daily card transaction before it is posted. The card must be on the card cross-reference, its account must exist, the account must not go over its credit limit, and the transaction must not be dated after the account expires. It serves the card issuer and decides which transactions are posted and which are rejected. It must never post a transaction for an unknown card, a missing account, an over-limit cycle or an expired account, and it must assign the correct reason code (100, 101, 102 or 103), with expiry (103) taking precedence over over-limit (102).

**User story:** As a card issuer, I want each daily transaction checked against the card cross-reference and the linked account, so that only transactions for known cards on valid, in-limit, unexpired accounts are posted.

## Requirements

### Requirement 1: DTPR-REQ-F-013 (business rule)

#### Acceptance criteria

1. The system shall look up the transaction's card in the card cross-reference first and shall look up the linked account only when the card was found. (rules DTPR-BR-014, DTPR-BR-015, DTPR-BR-016)
2. GIVEN Card number: 4111000011112222 (not in cross-reference) WHEN daily posting batch runs THEN Rejected with reason 100 'INVALID CARD NUMBER FOUND'; the account is not looked up (DTPR-C02-AC-01; DTPR-BR-014)
3. GIVEN Card number: 4111000011112222 (in cross-reference, account 00000000012) WHEN daily posting batch runs THEN Account 00000000012 is looked up (DTPR-C02-AC-02; DTPR-BR-014)
4. GIVEN DALYTRAN-CARD-NUM: 4000000000000002; Card in cross-reference: no WHEN the transaction's card number is not found in the card cross-reference THEN WS-VALIDATION-FAIL-REASON is 100; the account lookup, credit limit and expiration checks are not made (DTPR-C02-AC-03; DTPR-BR-015)
5. GIVEN DALYTRAN-CARD-NUM: 4000000000000002; Card in cross-reference: yes; XREF-ACCT-ID: 00000000011 WHEN the transaction's card number is not found in the card cross-reference THEN Reason stays 0 and account 00000000011 is looked up for the credit limit and expiration checks (DTPR-C02-AC-04; DTPR-BR-015)
6. GIVEN DALYTRAN-CARD-NUM: 5500000000000004; Card in cross-reference: no WHEN the transaction's card number is not found in the card cross-reference THEN Reject record trailer holds reason 100 and 'INVALID CARD NUMBER FOUND'; reject count goes up by 1 and the job ends with return code 4 (DTPR-C02-AC-05; DTPR-BR-016)
7. GIVEN DALYTRAN-CARD-NUM: 5500000000000004; Card in cross-reference: yes WHEN the transaction's card number is not found in the card cross-reference THEN Reason stays 0 and the account lookup is made (DTPR-C02-AC-06; DTPR-BR-016)

### Requirement 2: DTPR-REQ-F-014 (business rule)

#### Acceptance criteria

1. If the transaction's card number is not found in the card cross-reference, then the system shall record failure reason 100 'INVALID CARD NUMBER FOUND' and skip the account checks. (rules DTPR-BR-015, DTPR-BR-016, DTPR-BR-017)
2. GIVEN DALYTRAN-CARD-NUM: 4000000000000002; Card in cross-reference: no WHEN the transaction's card number is not found in the card cross-reference THEN WS-VALIDATION-FAIL-REASON is 100; the account lookup, credit limit and expiration checks are not made (DTPR-C02-AC-03; DTPR-BR-015)
3. GIVEN DALYTRAN-CARD-NUM: 4000000000000002; Card in cross-reference: yes; XREF-ACCT-ID: 00000000011 WHEN the transaction's card number is not found in the card cross-reference THEN Reason stays 0 and account 00000000011 is looked up for the credit limit and expiration checks (DTPR-C02-AC-04; DTPR-BR-015)
4. GIVEN DALYTRAN-CARD-NUM: 5500000000000004; Card in cross-reference: no WHEN the transaction's card number is not found in the card cross-reference THEN Reject record trailer holds reason 100 and 'INVALID CARD NUMBER FOUND'; reject count goes up by 1 and the job ends with return code 4 (DTPR-C02-AC-05; DTPR-BR-016)
5. GIVEN DALYTRAN-CARD-NUM: 5500000000000004; Card in cross-reference: yes WHEN the transaction's card number is not found in the card cross-reference THEN Reason stays 0 and the account lookup is made (DTPR-C02-AC-06; DTPR-BR-016)
6. GIVEN DALYTRAN-CARD-NUM: 4111111111111111; Card in cross-reference: no WHEN the transaction's card number is not found in the card cross-reference THEN Failure reason is 100 (card not found); the transaction is written to the daily rejects file (DTPR-C02-AC-07; DTPR-BR-017)
7. GIVEN DALYTRAN-CARD-NUM: 4111111111111111; Card in cross-reference: yes WHEN the transaction's card number is not found in the card cross-reference THEN Failure reason stays 0 and validation goes on to the account checks (DTPR-C02-AC-08; DTPR-BR-017)

### Requirement 3: DTPR-REQ-F-015 (business rule)

#### Acceptance criteria

1. If the account linked to the card is not on the account master, then the system shall reject the transaction with reason 101 'ACCOUNT RECORD NOT FOUND' and shall not evaluate the credit-limit or expiration checks. (rules DTPR-BR-018)
2. GIVEN Card number: 4111000011112222; Linked account: 00000000099 (not on account master) WHEN the account linked to the card is not on the account master THEN Transaction rejected with reason 0101 'ACCOUNT RECORD NOT FOUND' and written to the daily rejects file (DTPR-C02-AC-09; DTPR-BR-018)

### Requirement 4: DTPR-REQ-F-016 (business rule)

#### Acceptance criteria

1. If the card's account is found and its credit limit is less than the cycle credit total minus the cycle debit total plus the transaction amount, then the system shall reject the transaction with reason 102 'OVERLIMIT TRANSACTION', passing a projection equal to the limit. (rules DTPR-BR-019)
2. GIVEN credit limit: $5,000.00; cycle credit: $4,800.00; cycle debit: $0.00; transaction amount: $250.00 WHEN the card's account is found and its credit limit is less than the cycle credit total minus the cycle debit total plus the transaction amount THEN The projection is $5,050.00, which is over the limit, so the transaction is rejected with 102 'OVERLIMIT TRANSACTION'. (DTPR-C02-AC-10; DTPR-BR-019)
3. GIVEN credit limit: $5,000.00; cycle credit: $4,800.00; cycle debit: $0.00; transaction amount: $200.00 WHEN the card's account is found and its credit limit is less than the cycle credit total minus the cycle debit total plus the transaction amount THEN The projection is exactly $5,000.00, so the transaction passes the limit check. (DTPR-C02-AC-11; DTPR-BR-019)

### Requirement 5: DTPR-REQ-F-017 (business rule)

#### Acceptance criteria

1. The system shall base the credit-limit check on the current billing cycle's credit and debit totals plus the new transaction, not on the account's current balance. (rules DTPR-BR-020)
2. GIVEN current balance: $4,900.00; credit limit: $5,000.00; cycle credit: $100.00; cycle debit: $0.00; transaction amount: $300.00 WHEN transaction validation runs THEN The projection is $400.00, so the transaction passes even though balance plus amount would be $5,200.00. (DTPR-C02-AC-12; DTPR-BR-020)

### Requirement 6: DTPR-REQ-F-018 (business rule)

#### Acceptance criteria

1. While the account linked to the card is found, when the account expiration date is earlier than the transaction's original date, the system shall record failure reason 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION'. (rules DTPR-BR-021, DTPR-BR-022, DTPR-BR-023)
2. GIVEN Card found in cross-reference: yes; Account found: yes; ACCT-EXPIRAION-DATE: 2024-12-31; DALYTRAN-ORIG-TS (date part): 2025-01-02 WHEN the account linked to the card is found, WHEN the account expiration date is earlier than the transaction date THEN Failure reason is 103 (transaction after account expiration); the transaction is rejected (DTPR-C02-AC-13; DTPR-BR-021)
3. GIVEN Account found: yes; ACCT-EXPIRAION-DATE: 2027-12-31; DALYTRAN-ORIG-TS (date part): 2025-01-02 WHEN the account linked to the card is found, WHEN the account expiration date is earlier than the transaction date THEN Failure reason is not set to 103; if no other check fails the transaction is posted (DTPR-C02-AC-14; DTPR-BR-021)
4. GIVEN Account found: no WHEN the account linked to the card is found, WHEN the account expiration date is earlier than the transaction date THEN The expiration check is not made; failure reason is 101 'ACCOUNT RECORD NOT FOUND' (DTPR-C02-AC-15; DTPR-BR-021)
5. GIVEN Account found: yes; ACCT-EXPIRAION-DATE: 2025-03-31; DALYTRAN-ORIG-TS: 2025-04-01-10.15.00.000000 WHEN the linked account was found, WHEN the account expiration date is earlier than the transaction's original date THEN Failure reason 103 with description 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION' is written in the reject record's trailer (DTPR-C02-AC-16; DTPR-BR-022)
6. GIVEN Account found: yes; Balance after transaction: over credit limit; ACCT-EXPIRAION-DATE: 2025-03-31; DALYTRAN-ORIG-TS: 2025-04-01-10.15.00.000000 WHEN the linked account was found, WHEN the account expiration date is earlier than the transaction's original date THEN The reason 102 'OVERLIMIT TRANSACTION' is replaced, and the reject shows 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION' (DTPR-C02-AC-17; DTPR-BR-022)
7. GIVEN ACCT-EXPIRAION-DATE: 2025-06-30; DALYTRAN-ORIG-TS (date part): 2025-07-15 WHEN the account is found and its expiration date is earlier than the transaction date THEN WS-VALIDATION-FAIL-REASON is set to 103; the transaction is written to the daily rejects file and not posted (DTPR-C02-AC-18; DTPR-BR-023)
8. GIVEN ACCT-EXPIRAION-DATE: 2025-06-30; DALYTRAN-ORIG-TS (date part): 2025-06-30 WHEN the account is found and its expiration date is earlier than the transaction date THEN No failure reason 103 is set (an expiry date equal to the transaction date is accepted) (DTPR-C02-AC-19; DTPR-BR-023)

### Requirement 7: DTPR-REQ-F-019 (business rule)

#### Acceptance criteria

1. When a transaction is both over the credit limit and dated after the account's expiration date, the system shall record only reason 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION'. (rules DTPR-BR-024)
2. GIVEN projection: over the credit limit; transaction date: after account expiration WHEN a transaction is both over the limit and dated after the account's expiration date THEN The reject record carries 103 'TRANSACTION RECEIVED AFTER ACCT EXPIRATION', not 102. (DTPR-C02-AC-20; DTPR-BR-024)
