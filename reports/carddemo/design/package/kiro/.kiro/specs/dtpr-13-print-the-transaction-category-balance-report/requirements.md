# Requirements: Print the transaction category balance report (DTPR-C13)

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

Customer Account Self-Service · Daily Transaction Processing and Reporting · runs as scheduled job · risk high

## Introduction

Produces a printed report of every transaction category balance so card operations analysts can review balances by account, transaction type and category. Each run takes a fresh snapshot of the category balances and lists them in ascending order of account id, then transaction type, then category code. It must never mix in a stale earlier report or keep a partial report when the run fails.

**User story:** As a card operations analyst, I want a sorted report of transaction category balances, so that I can review balances by account, transaction type and category.

## Requirements

### Requirement 1: DTPR-REQ-F-070 (design note)

#### Acceptance criteria

1. The system shall first delete any earlier category balance report (AWS.M2.CARDDEMO.TCATBALF.REPT), then copy the whole category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS) into a new generation of the category balance backup (AWS.M2.CARDDEMO.TCATBALF.BKUP) of 50-byte records. (rules DTPR-BR-077)
2. GIVEN existing report: AWS.M2.CARDDEMO.TCATBALF.REPT from yesterday; category balance file: 3 records WHEN Transaction Category Balance Print job runs THEN Yesterday's report is deleted and a new backup generation holding the 3 records is created. (DTPR-C13-AC-01; DTPR-BR-077)

### Requirement 2: DTPR-REQ-F-071 (formatting)

#### Acceptance criteria

1. The system shall write the category balance report (AWS.M2.CARDDEMO.TCATBALF.REPT) from the new backup generation, ordered ascending by account id, then transaction type, then category code, as one 40-byte line per record showing account id, type, category and balance edited as 'TTTTTTTTT.TT', separated by single blanks. (rules DTPR-BR-078)
2. GIVEN record A: account 00000000005, type 02, category 0003; record B: account 00000000005, type 01, category 0007 WHEN Transaction Category Balance Print job runs THEN Record B is printed before record A because type 01 comes before type 02. (DTPR-C13-AC-02; DTPR-BR-078)

### Requirement 3: DTPR-REQ-N-007 (error handling)

#### Acceptance criteria

1. When the report step completes normally, the system shall catalog the new category balance report. (rules DTPR-BR-079)
2. GIVEN sort step outcome: abends WHEN the report step completes normally THEN No AWS.M2.CARDDEMO.TCATBALF.REPT data set is kept. (DTPR-C13-AC-03; DTPR-BR-079)

### Requirement 4: DTPR-REQ-N-008 (error handling)

#### Acceptance criteria

1. If the report step fails, then the system shall delete the partial category balance report. (rules DTPR-BR-079)
2. GIVEN sort step outcome: abends WHEN the report step completes normally THEN No AWS.M2.CARDDEMO.TCATBALF.REPT data set is kept. (DTPR-C13-AC-03; DTPR-BR-079)
