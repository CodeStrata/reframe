# Feature specification: Print the transaction category balance report

**Feature:** DTPR-C13 · Daily Transaction Processing and Reporting · Customer Account Self-Service

**Status: FINAL**, signed off by Pat (acceptance), 2026-11-25.

## User scenarios and testing

### User story (DTPR-C13)

As a card operations analyst, I want a sorted report of transaction category balances, so that I can review balances by account, transaction type and category.

Produces a printed report of every transaction category balance so card operations analysts can review balances by account, transaction type and category. Each run takes a fresh snapshot of the category balances and lists them in ascending order of account id, then transaction type, then category code. It must never mix in a stale earlier report or keep a partial report when the run fails.

**Acceptance scenarios:**

1. **Given** existing report: AWS.M2.CARDDEMO.TCATBALF.REPT from yesterday; category balance file: 3 records, **when** Transaction Category Balance Print job runs, **then** Yesterday's report is deleted and a new backup generation holding the 3 records is created. (DTPR-C13-AC-01)
2. **Given** record A: account 00000000005, type 02, category 0003; record B: account 00000000005, type 01, category 0007, **when** Transaction Category Balance Print job runs, **then** Record B is printed before record A because type 01 comes before type 02. (DTPR-C13-AC-02)
3. **Given** sort step outcome: abends, **when** the report step completes normally, **then** No AWS.M2.CARDDEMO.TCATBALF.REPT data set is kept. (DTPR-C13-AC-03)

## Requirements

### Functional requirements

- **DTPR-REQ-F-070** (design note): The system shall first delete any earlier category balance report (AWS.M2.CARDDEMO.TCATBALF.REPT), then copy the whole category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS) into a new generation of the category balance backup (AWS.M2.CARDDEMO.TCATBALF.BKUP) of 50-byte records. Rules: DTPR-BR-077.
- **DTPR-REQ-F-071** (formatting): The system shall write the category balance report (AWS.M2.CARDDEMO.TCATBALF.REPT) from the new backup generation, ordered ascending by account id, then transaction type, then category code, as one 40-byte line per record showing account id, type, category and balance edited as 'TTTTTTTTT.TT', separated by single blanks. Rules: DTPR-BR-078.
- **DTPR-REQ-N-007** (error handling): When the report step completes normally, the system shall catalog the new category balance report. Rules: DTPR-BR-079.
- **DTPR-REQ-N-008** (error handling): If the report step fails, then the system shall delete the partial category balance report. Rules: DTPR-BR-079.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| DTPR-BR-077 | Produce sorted category balance report | design note | THE Transaction Category Balance Print job SHALL first delete any earlier category balance report (AWS.M2.CARDDEMO.TCATBALF.REPT), then copy the whole category balance file (AWS.M2.CARDDEMO.TCATBALF.VSAM.KSDS) into a new generation of the category balance backup (AWS.M2.CARDDEMO.TCATBALF.BKUP) of 50-byte records. | medium | app/jcl/PRTCATBL.jcl:21-25, app/jcl/PRTCATBL.jcl:29-39, app/jcl/PRTCATBL.jcl:43-63, app/proc/REPROC.prc:21-28 |
| DTPR-BR-078 | Produce sorted category balance report | formatting | THE Transaction Category Balance Print job SHALL write the category balance report (AWS.M2.CARDDEMO.TCATBALF.REPT) from the new backup generation, ordered ascending by account id, then transaction type, then category code, one 40-byte line per record showing account id, type, category and balance edited as 'TTTTTTTTT.TT', separated by single blanks. | medium | app/jcl/PRTCATBL.jcl:21-25, app/jcl/PRTCATBL.jcl:29-39, app/jcl/PRTCATBL.jcl:43-63, app/proc/REPROC.prc:21-28 |
| DTPR-BR-079 | Produce sorted category balance report | error handling | WHEN the report step completes normally, THE Transaction Category Balance Print job SHALL catalog the new report, and WHEN the step fails it SHALL delete the partial report. | medium | app/jcl/PRTCATBL.jcl:21-25, app/jcl/PRTCATBL.jcl:29-39, app/jcl/PRTCATBL.jcl:43-63, app/proc/REPROC.prc:21-28 |

### Key entities

None found in the source.

### Needs clarification

- SME-273: Should the category balance report filter balances by a date parameter, as the job's comment says? If so, which date and which comparison apply? (Business reporting owner) On DTPR-BR-079.
- SME-274: The category balance report line adds up to 41 positions but the line is defined as 40 wide. Which element should be shortened, or should the line width change? (Business reporting owner) On DTPR-BR-079.
- SME-275: Must the category balance report show a sign for negative balances, and if so how? (Business reporting owner) On DTPR-BR-079.
- DEF-110: Is this intended? The balance is a signed field (S9(09)V99) but the edit mask 'TTTTTTTTT.TT' has no sign, so a negative category balance prints the same as a positive one; also the built line is 41 bytes (11+1+2+1+4+1+12+9) against a 40-byte report record, so the last pad byte is truncated (or the sort fails, depending on the site sort options). The step comment about filtering by parm date and sorting by card number does not match what the step does. (Subject-matter expert) On DTPR-BR-079.

### Decision table gaps

None.
