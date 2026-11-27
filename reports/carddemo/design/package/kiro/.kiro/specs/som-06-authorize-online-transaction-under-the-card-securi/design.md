# Design: Authorize online transaction under the card security profile (SOM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Is a security administration step that puts the CT02 online function under the CARD access profile, so only users granted that profile can run it. It is for security administrators. It must add CT02 to the CARD profile and record the result for audit, and must never leave CT02 reachable outside that profile.

Runs as scheduled job.

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