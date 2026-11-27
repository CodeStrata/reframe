# Requirements: Post daily transactions and record rejects (DTPR-C07)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

The scheduled daily posting job. It takes the day's card transactions, posts accepted ones to the transaction master, the account records and the category balances, and keeps rejected ones in a new daily rejects file of 430-byte records (the 350-byte transaction plus an 80-byte reason trailer). It serves the card operations team. It must never leave a partial rejects file behind when the job fails; the rejects file is kept only when the job ends normally.

**User story:** As a card operations team, I want each day's card transactions posted to the transaction master and account records, with rejected transactions kept separately, so that balances reflect the day's activity and rejects can be investigated.

## Requirements

### Requirement 1: DTPR-REQ-F-057 (design note)

#### Acceptance criteria

1. The system shall run the posting program (CBTRN02C) to read the daily transaction file ('AWS.M2.CARDDEMO.DALYTRAN.PS') and the card cross-reference ('AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS'), write posted transactions to the transaction master ('AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS'), and update the account master ('AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS') and the transaction category balances ('AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS'). (rules DTPR-BR-061)
2. GIVEN daily transaction file: 200 transactions for known cards WHEN Daily Transaction Posting job runs THEN the transactions are written to the transaction master, and account balances and category balances are updated (DTPR-C07-AC-01; DTPR-BR-061)

### Requirement 2: DTPR-REQ-F-058 (side effect)

#### Acceptance criteria

1. The system shall write rejected transactions to a new generation of the daily rejects file ('AWS.M2.CARDDEMO.DALYREJS(+1)') in fixed 430-byte records made of the 350-byte transaction plus an 80-byte validation trailer. (rules DTPR-BR-062)
2. GIVEN rejected transactions: 3; step outcome: ends normally WHEN Daily Transaction Posting job runs THEN a new DALYREJS generation with 3 records of 430 bytes is cataloged (DTPR-C07-AC-02; DTPR-BR-062)
3. GIVEN step outcome: abends WHEN Daily Transaction Posting job runs THEN the new DALYREJS generation is deleted (DTPR-C07-AC-03; DTPR-BR-062)

### Requirement 3: DTPR-REQ-N-001 (side effect)

#### Acceptance criteria

1. If the posting step abends, then the system shall delete the new daily rejects generation, keeping it only when the step ends normally. (rules DTPR-BR-062)
2. GIVEN rejected transactions: 3; step outcome: ends normally WHEN Daily Transaction Posting job runs THEN a new DALYREJS generation with 3 records of 430 bytes is cataloged (DTPR-C07-AC-02; DTPR-BR-062)
3. GIVEN step outcome: abends WHEN Daily Transaction Posting job runs THEN the new DALYREJS generation is deleted (DTPR-C07-AC-03; DTPR-BR-062)
