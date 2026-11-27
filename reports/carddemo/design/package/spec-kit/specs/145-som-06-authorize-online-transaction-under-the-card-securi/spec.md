# Feature specification: Authorize online transaction under the card security profile

**Feature:** SOM-C06 · System Operations and Maintenance · User Access Control

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (SOM-C06)

As a security administrator, I want transaction CT02 added to the CARD transaction profile, so that access to it is controlled by the card security profile.

Is a security administration step that puts the CT02 online function under the CARD access profile, so only users granted that profile can run it. It is for security administrators. It must add CT02 to the CARD profile and record the result for audit, and must never leave CT02 reachable outside that profile.

**Acceptance scenarios:**

1. **Given** Profile: CARD in class GCICSTRN; Transaction: CT02, **when** security administration job (RACFCMDS) runs, **then** CT02 becomes a member of profile CARD, so users permitted to CARD are authorised for CT02; the command output is printed in the job listing. (SOM-C06-AC-01)

## Requirements

### Functional requirements

- **SOM-REQ-F-031** (business rule): The system shall add online transaction 'CT02' as a member of the transaction profile 'CARD' in the grouped CICS transaction class 'GCICSTRN', and print the command results to the job output. Rules: SOM-BR-035.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| SOM-BR-035 | Authorize transaction under card profile | business rule | THE security administration job (RACFCMDS) SHALL add online transaction 'CT02' as a member of the transaction profile 'CARD' in the grouped CICS transaction class 'GCICSTRN', and SHALL print the command results to the job output. | medium | samples/jcl/RACFCMDS.jcl:19-26 |

### Key entities

None found in the source.

### Needs clarification

- SME-276: The command connecting user AWSCODR to the application development group (M2APPDEV) sits after the job's end marker and may never run today. Should the modernized process apply this group connection, and should it run together with the CT02 profile update or separately? (Security administration team) On SOM-BR-035.

### Decision table gaps

None.
