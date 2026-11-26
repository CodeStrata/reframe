# Feature specification: Post daily transactions and record rejects

**Feature:** DTPR-C07 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C07)

As a card operations team, I want each day's card transactions posted to the transaction master and account records, with rejected transactions kept separately, so that balances reflect the day's activity and rejects can be investigated.

The scheduled daily posting job. It takes the day's card transactions, posts accepted ones to the transaction master, the account records and the category balances, and keeps rejected ones in a new daily rejects file of 430-byte records (the 350-byte transaction plus an 80-byte reason trailer). It serves the card operations team. It must never leave a partial rejects file behind when the job fails; the rejects file is kept only when the job ends normally.

**Acceptance scenarios:**

1. **Given** daily transaction file: 200 transactions for known cards, **when** Daily Transaction Posting job runs, **then** the transactions are written to the transaction master, and account balances and category balances are updated (DTPR-C07-AC-01)
2. **Given** rejected transactions: 3; step outcome: ends normally, **when** Daily Transaction Posting job runs, **then** a new DALYREJS generation with 3 records of 430 bytes is cataloged (DTPR-C07-AC-02)
3. **Given** step outcome: abends, **when** Daily Transaction Posting job runs, **then** the new DALYREJS generation is deleted (DTPR-C07-AC-03)

## Requirements

### Functional requirements

- **DTPR-REQ-F-057** (design note): The system shall run the posting program (CBTRN02C) to read the daily transaction file ('AWS.M2.CARDDEMO.DALYTRAN.PS') and the card cross-reference ('AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS'), write posted transactions to the transaction master ('AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS'), and update the account master ('AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS') and the transaction category balances ('AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS'). Rules: DTPR-BR-061.
- **DTPR-REQ-F-058** (side effect): The system shall write rejected transactions to a new generation of the daily rejects file ('AWS.M2.CARDDEMO.DALYREJS(+1)') in fixed 430-byte records made of the 350-byte transaction plus an 80-byte validation trailer. Rules: DTPR-BR-062.
- **DTPR-REQ-N-001** (side effect): If the posting step abends, then the system shall delete the new daily rejects generation, keeping it only when the step ends normally. Rules: DTPR-BR-062.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-061 | Post daily transactions and record rejects | design note | THE Daily Transaction Posting job SHALL run the posting program (CBTRN02C) to read the daily transaction file ('AWS.M2.CARDDEMO.DALYTRAN.PS') and the card cross-reference ('AWS.M2.CARDDEMO.CARDXREF.VSAM.KSDS'), write posted transactions to the transaction master ('AWS.M2.CARDDEMO.TRANSACT.VSAM.KSDS'), and update the account master ('AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS') and the transaction category balances ('AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS'). | medium | app/jcl/POSTTRAN.jcl:19-42, app/cbl/CBTRN02C.cbl:80-84, app/cbl/CBTRN02C.cbl:238, app/cbl/CBTRN02C.cbl:256 |
| DTPR-BR-062 | Post daily transactions and record rejects | side effect | THE Daily Transaction Posting job SHALL write rejected transactions to a new generation of the daily rejects file ('AWS.M2.CARDDEMO.DALYREJS(+1)'), in fixed 430-byte records (350-byte transaction plus an 80-byte validation trailer). The generation is kept if the step ends normally and deleted if the step abends. | medium | app/jcl/POSTTRAN.jcl:19-42, app/cbl/CBTRN02C.cbl:80-84, app/cbl/CBTRN02C.cbl:238, app/cbl/CBTRN02C.cbl:256 |

### Key entities

None found in the source.

### Needs clarification

- SME-039: How should the over-credit-limit check measure exposure? Today it uses cycle credits minus cycle debits plus the transaction amount, and because debits are stored as negative amounts this effectively adds payments. Is that intended, or should the check use the current balance plus the transaction amount? Should cash transactions also be checked against the cash credit limit? (Credit risk / card product owner) On DTPR-BR-062.

### Decision table gaps

None.
