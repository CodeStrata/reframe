# Requirements: Post a full-balance bill payment (OATM-C20)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Posts a confirmed bill payment as a new transaction for the full current balance, clears the account balance to zero, and gives the cardholder the new transaction ID as proof. The payment is numbered one above the highest existing transaction ID. As the legacy system behaves, the balance is still cleared even when the payment transaction could not be written, so the build team must decide explicitly whether to keep that.

**User story:** As a cardholder, I want my confirmed payment recorded as a transaction for the full balance and my account balance cleared, so that my account is paid off and I get a transaction ID as proof.

## Requirements

### Requirement 1: OATM-REQ-F-160 (business rule)

#### Acceptance criteria

1. When the user confirms a bill payment with 'Y' or 'y' and the account has a balance to pay, the system shall look up the card linked to the account and number the new payment transaction as the highest existing transaction ID plus 1. (rules OATM-BR-166)
2. GIVEN Confirm: Y; Highest transaction ID on file: 0000000000001234 WHEN the user confirms a bill payment with 'Y' or 'y' and the account has a balance to pay THEN The payment transaction is given ID 0000000000001235. (OATM-C20-AC-01; OATM-BR-166)

### Requirement 2: OATM-REQ-F-161 (design note)

#### Acceptance criteria

1. When a confirmed bill payment needs a new transaction number, the system shall position at the end of the transaction file, read the last transaction record and take its transaction ID as the latest existing number. (rules OATM-BR-167)
2. GIVEN Highest transaction ID on file: 0000000000001234; Confirm: Y WHEN a confirmed bill payment needs a new transaction number THEN The latest existing transaction ID is taken as 0000000000001234. (OATM-C20-AC-02; OATM-BR-167)

### Requirement 3: OATM-REQ-F-162 (business rule)

#### Acceptance criteria

1. When reading back from the end of the transaction file finds no transaction, the system shall treat the latest transaction ID as zero, so the payment is given transaction ID 1. (rules OATM-BR-168)
2. GIVEN Transaction file: empty; Confirm: Y WHEN reading back from the end of the transaction file finds no transaction (end of file) THEN The new payment transaction is numbered 0000000000000001. (OATM-C20-AC-03; OATM-BR-168)

### Requirement 4: OATM-REQ-F-163 (error handling)

#### Acceptance criteria

1. If a confirmed payment's lookup of the card linked to the account finds no card link, then the system shall show 'Account ID NOT found...', or 'Unable to lookup XREF AIX file...' on any other failure. (rules OATM-BR-169)
2. GIVEN Account ID: 00000000011; Confirm: Y; Card link for account: missing WHEN a confirmed payment looks up the card linked to the account THEN 'Account ID NOT found...' is shown (but see defect: posting still continues). (OATM-C20-AC-04; OATM-BR-169)

### Requirement 5: OATM-REQ-F-164 (business rule)

#### Acceptance criteria

1. When the user confirms a bill payment, the system shall record a payment for the full current account balance and reduce the account's current balance by that amount, leaving it at zero. (rules OATM-BR-170, OATM-BR-171)
2. GIVEN Confirm: Y; ACCT-CURR-BAL: 150.00; last TRAN-ID: 0000000000000041 WHEN a confirmed bill payment is posted THEN Transaction 0000000000000042 written with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', amount 150.00, merchant 999999999 'BILL PAYMENT' 'N/A' 'N/A', current timestamp; balance then becomes 0.00 (OATM-C20-AC-05; OATM-BR-170)
3. GIVEN Confirm: (blank); ACCT-CURR-BAL: 150.00 WHEN a confirmed bill payment is posted THEN No transaction written; screen shows 'Confirm to make a bill payment...' (OATM-C20-AC-06; OATM-BR-170)
4. GIVEN Account: 00000000011; Current balance: $1,250.75; Confirm: Y WHEN the user confirms a bill payment THEN A payment transaction of $1,250.75 is written and the account balance becomes $0.00. (OATM-C20-AC-07; OATM-BR-171)

### Requirement 6: OATM-REQ-F-165 (business rule)

#### Acceptance criteria

1. The system shall record each online payment with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', merchant ID 999999999, merchant name 'BILL PAYMENT', merchant city and ZIP 'N/A', the account's card number, and the current date and time as both origin and processing time. (rules OATM-BR-170, OATM-BR-172)
2. GIVEN Confirm: Y; ACCT-CURR-BAL: 150.00; last TRAN-ID: 0000000000000041 WHEN a confirmed bill payment is posted THEN Transaction 0000000000000042 written with type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE', amount 150.00, merchant 999999999 'BILL PAYMENT' 'N/A' 'N/A', current timestamp; balance then becomes 0.00 (OATM-C20-AC-05; OATM-BR-170)
3. GIVEN Confirm: (blank); ACCT-CURR-BAL: 150.00 WHEN a confirmed bill payment is posted THEN No transaction written; screen shows 'Confirm to make a bill payment...' (OATM-C20-AC-06; OATM-BR-170)
4. GIVEN Account card number: 4111111111111111; Payment time: 2026-11-25 10:15:00 WHEN Bill Payment screen runs THEN The transaction has type '02', category 2, source 'POS TERM', description 'BILL PAYMENT - ONLINE' and timestamps 2026-11-25 10:15:00. (OATM-C20-AC-08; OATM-BR-172)

### Requirement 7: OATM-REQ-F-166 (business rule)

#### Acceptance criteria

1. When a confirmed payment is posted, the system shall write a payment transaction for the full current balance, then subtract that amount from the account balance and save the account. (rules OATM-BR-173, OATM-BR-174)
2. GIVEN Current balance: $300.00; Confirm: Y WHEN a confirmed payment is posted THEN A transaction of $300.00 is written and the balance becomes $0.00. (OATM-C20-AC-09; OATM-BR-173)
3. GIVEN Balance before: $1,250.75; Payment: $1,250.75 WHEN the payment transaction has been written THEN The account is saved with current balance $0.00. (OATM-C20-AC-10; OATM-BR-174)

### Requirement 8: OATM-REQ-F-167 (formatting)

#### Acceptance criteria

1. When the bill payment transaction is written successfully, the system shall clear the account ID, balance and confirmation fields and show in green 'Payment successful. Your Transaction ID is <new ID>.'. (rules OATM-BR-175)
2. GIVEN A cardholder has confirmed a bill payment with 'Y' on account 00000000001 and the new payment transaction 0000000000000124 is written successfully WHEN The Bill Payment screen is shown again THEN The account ID, balance and confirmation fields are empty and the message 'Payment successful. Your Transaction ID is 0000000000000124.' is shown in green (OATM-C20-AC-15; OATM-BR-175)

### Requirement 9: OATM-REQ-F-168 (error handling)

#### Acceptance criteria

1. If the payment transaction ID already exists, then the system shall show 'Tran ID already exist...', and for any other write failure 'Unable to Add Bill pay Transaction...'. (rules OATM-BR-176)
2. GIVEN Write result: duplicate key WHEN the payment transaction ID already exists THEN The message 'Tran ID already exist...' is shown. (OATM-C20-AC-11; OATM-BR-176)

### Requirement 10: OATM-REQ-F-169 (error handling)

#### Acceptance criteria

1. If the payment transaction cannot be written or the card lookup fails, then the system shall still subtract the payment from the balance and save the account, so the balance is cleared without a payment on file. (rules OATM-BR-177)
2. GIVEN Current balance: $300.00; Confirm: Y; Transaction write: duplicate key WHEN the payment transaction cannot be written (message 'Tran ID already exist...' or 'Unable to Add Bill pay Transaction...') or the card lookup fails THEN 'Tran ID already exist...' is shown, yet the balance is saved as $0.00 with no payment transaction. (OATM-C20-AC-12; OATM-BR-177)

### Requirement 11: OATM-REQ-F-170 (error handling)

#### Acceptance criteria

1. If saving the updated account fails, then the system shall show 'Account ID NOT found...' if the account is not found, or 'Unable to Update Account...' for any other failure, with the cursor on the account ID. (rules OATM-BR-178)
2. GIVEN Account save result: not found WHEN saving the updated account fails THEN The message 'Account ID NOT found...' is shown. (OATM-C20-AC-13; OATM-BR-178)
3. GIVEN Account save result: other error WHEN saving the updated account fails THEN The message 'Unable to Update Account...' is shown. (OATM-C20-AC-14; OATM-BR-178)
