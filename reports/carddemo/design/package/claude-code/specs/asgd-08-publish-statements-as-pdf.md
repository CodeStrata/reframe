# Publish statements as PDF (ASGD-C08)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Customer Account Self-Service · Account Statement Generation and Delivery · runs as scheduled job · risk high

## Introduction

Once statements have been created, the text statements are converted to PDF so cardholders can view and keep them in a standard format. The PDF must contain exactly the statements from the completed run, and it must never be published from a failed or partial run.

**User story:** As a cardholder, I want my account statement delivered as a PDF, so that I can view and keep it in a standard format.

## Requirements

### Requirement 1: ASGD-REQ-F-039 (design note)

#### Acceptance criteria

1. When the statement creation job (CREASTMT) completes, the system shall run the text-to-PDF conversion (TXT2PDF, with BROWSE Y) on the account statement text file AWS.M2.CARDDEMO.STATEMNT.PS and write the statements as the PDF data set 'AWS.M2.CARDDEMO.STATEMNT.PS.PDF'. (rules ASGD-BR-039)
2. GIVEN statement text file: statements for 50 accounts produced by CREASTMT WHEN the statement creation job (CREASTMT) completes THEN The job converts the text file and writes 'AWS.M2.CARDDEMO.STATEMNT.PS.PDF' containing those statements. (ASGD-C08-AC-01; ASGD-BR-039)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ASGD-BR-039 | Convert account statements to PDF | design note | WHEN the statement creation job (CREASTMT) completes, THE Account Statement PDF Publication SHALL run the text-to-PDF conversion (TXT2PDF, with BROWSE Y) on the account statement text file AWS.M2.CARDDEMO.STATEMNT.PS and write the statements as the PDF data set 'AWS.M2.CARDDEMO.STATEMNT.PS.PDF'. | medium | app/jcl/TXT2PDF1.JCL:24-40, app/scheduler/CardDemo.ca7:470-495, app/jcl/CREASTMT.JCL:75 |

### Worked examples

- ASGD-BR-039: statement text file = statements for 50 accounts produced by CREASTMT → The job converts the text file and writes 'AWS.M2.CARDDEMO.STATEMNT.PS.PDF' containing those statements.

## Decision tables

None.

## Design notes

- ASGD-BR-039: A scheduled follow-on step that starts when statement creation completes. It renders the plain-text statement report to PDF and stores the result as the published statement document (legacy name AWS.M2.CARDDEMO.STATEMNT.PS.PDF), for example in document storage. Any text-to-PDF renderer works. The legacy job uses the TXT2PDF utility with BROWSE Y.

## Open questions

- SME-298: What should the modernized statement PDF output be called, and where should it be stored? Today it is known only by the legacy dataset name AWS.M2.CARDDEMO.STATEMNT.PS.PDF. (Statement operations team) On ASGD-BR-039.
- SME-299: The statement PDF conversion only runs if every earlier step ended with return code 0, yet it is the job's only business step. Which earlier steps does this cover, and should the modernized system keep this check? (Batch operations team) On ASGD-BR-039.
- SME-300: If the statement PDF conversion fails or is rerun, should a rerun overwrite the existing PDF, and is a partial PDF acceptable after a failure? (Batch operations team) On ASGD-BR-039.
- SME-301: The browse option (BROWSE Y) is described only as making the statement PDF viewable. Which PDF properties must the modernized conversion keep to meet this intent? (Statement operations team) On ASGD-BR-039.
- DEF-102: Is this intended? The step carries COND=(0,NE), which looks meant to skip conversion after a failure, but as the first and only step it has nothing to test, so the PDF is produced even if the statement job's output is incomplete. (Subject-matter expert) On ASGD-BR-039.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (1 in all).
