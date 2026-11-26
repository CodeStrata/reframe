# Print the transaction category balance report (DTPR-C13)

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

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-077 | Produce sorted category balance report | design note | THE Transaction Category Balance Print job SHALL first delete any earlier category balance report (AWS.M2.CARDDEMO.TCATBALF.REPT), then copy the whole category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS) into a new generation of the category balance backup (AWS.M2.CARDDEMO.TCATBALF.BKUP) of 50-byte records. | medium | app/jcl/PRTCATBL.jcl:21-25, app/jcl/PRTCATBL.jcl:29-39, app/jcl/PRTCATBL.jcl:43-63, app/proc/REPROC.prc:21-28 |
| DTPR-BR-078 | Produce sorted category balance report | formatting | THE Transaction Category Balance Print job SHALL write the category balance report (AWS.M2.CARDDEMO.TCATBALF.REPT) from the new backup generation, ordered ascending by account id, then transaction type, then category code, one 40-byte line per record showing account id, type, category and balance edited as 'TTTTTTTTT.TT', separated by single blanks. | medium | app/jcl/PRTCATBL.jcl:21-25, app/jcl/PRTCATBL.jcl:29-39, app/jcl/PRTCATBL.jcl:43-63, app/proc/REPROC.prc:21-28 |
| DTPR-BR-079 | Produce sorted category balance report | error handling | WHEN the report step completes normally, THE Transaction Category Balance Print job SHALL catalog the new report, and WHEN the step fails it SHALL delete the partial report. | medium | app/jcl/PRTCATBL.jcl:21-25, app/jcl/PRTCATBL.jcl:29-39, app/jcl/PRTCATBL.jcl:43-63, app/proc/REPROC.prc:21-28 |

### Worked examples

- DTPR-BR-077: existing report = AWS.M2.CARDDEMO.TCATBALF.REPT from yesterday; category balance file = 3 records → Yesterday's report is deleted and a new backup generation holding the 3 records is created.
- DTPR-BR-078: record A = account 00000000005, type 02, category 0003; record B = account 00000000005, type 01, category 0007 → Record B is printed before record A because type 01 comes before type 02.
- DTPR-BR-079: sort step outcome = abends → No AWS.M2.CARDDEMO.TCATBALF.REPT data set is kept.

## Decision tables

None.

## Design notes

- DTPR-BR-077: Before reporting, remove the previous category balance report and take a complete point-in-time snapshot of all category balance records as a new numbered backup version. The report is then built from that snapshot, not from the live balances, so it reflects one consistent moment.

## Open questions

- SME-273: Should the category balance report filter balances by a date parameter, as the job's comment says? If so, which date and which comparison apply? (Business reporting owner) On DTPR-BR-079.
- SME-274: The category balance report line adds up to 41 positions but the line is defined as 40 wide. Which element should be shortened, or should the line width change? (Business reporting owner) On DTPR-BR-079.
- SME-275: Must the category balance report show a sign for negative balances, and if so how? (Business reporting owner) On DTPR-BR-079.
- DEF-110: Is this intended? The balance is a signed field (S9(09)V99) but the edit mask 'TTTTTTTTT.TT' has no sign, so a negative category balance prints the same as a positive one; also the built line is 41 bytes (11+1+2+1+4+1+12+9) against a 40-byte report record, so the last pad byte is truncated (or the sort fails, depending on the site sort options). The step comment about filtering by parm date and sorting by card number does not match what the step does. (Subject-matter expert) On DTPR-BR-079.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).
