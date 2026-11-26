# Requirements: Publish statements as PDF (ASGD-C08)

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
