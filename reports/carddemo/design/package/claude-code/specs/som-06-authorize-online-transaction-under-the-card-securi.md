# Authorize online transaction under the card security profile (SOM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as scheduled job · risk high

## Introduction

Security administration adds transaction CT02 to the CARD access profile, so only users allowed under that profile can run it. The result of the change must be recorded in the job output for audit. The change must never miss CT02, never put it in the wrong profile, and never go unrecorded.

**User story:** As a security administrator, I want transaction CT02 added to the CARD transaction profile, so that access to it is controlled by the card security profile.

## Requirements

### Requirement 1: SOM-REQ-F-031 (business rule)

#### Acceptance criteria

1. The system shall add online transaction 'CT02' as a member of the transaction profile 'CARD' in the grouped CICS transaction class 'GCICSTRN', and print the command results to the job output. (rules SOM-BR-035)
2. GIVEN Profile: CARD in class GCICSTRN; Transaction: CT02 WHEN security administration job (RACFCMDS) runs THEN CT02 becomes a member of profile CARD, so users permitted to CARD are authorised for CT02; the command output is printed in the job listing. (SOM-C06-AC-01; SOM-BR-035)

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-035 | Authorize transaction under card profile | business rule | THE security administration job (RACFCMDS) SHALL add online transaction 'CT02' as a member of the transaction profile 'CARD' in the grouped CICS transaction class 'GCICSTRN', and SHALL print the command results to the job output. | medium | samples/jcl/RACFCMDS.jcl:19-26 |

### Worked examples

- SOM-BR-035: Profile = CARD in class GCICSTRN; Transaction = CT02 → CT02 becomes a member of profile CARD, so users permitted to CARD are authorised for CT02; the command output is printed in the job listing.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-276: The command connecting user AWSCODR to the application development group (M2APPDEV) sits after the job's end marker and may never run today. Should the modernized process apply this group connection, and should it run together with the CT02 profile update or separately? (Security administration team) On SOM-BR-035.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (1 in all).
