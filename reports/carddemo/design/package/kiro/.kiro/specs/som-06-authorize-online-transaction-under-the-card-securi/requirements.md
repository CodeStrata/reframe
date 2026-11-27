# Requirements: Authorize online transaction under the card security profile (SOM-C06)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

User Access Control · System Operations and Maintenance · runs as scheduled job · risk high

## Introduction

Is a security administration step that puts the CT02 online function under the CARD access profile, so only users granted that profile can run it. It is for security administrators. It must add CT02 to the CARD profile and record the result for audit, and must never leave CT02 reachable outside that profile.

**User story:** As a security administrator, I want transaction CT02 added to the CARD transaction profile, so that access to it is controlled by the card security profile.

## Requirements

### Requirement 1: SOM-REQ-F-031 (business rule)

#### Acceptance criteria

1. The system shall add online transaction 'CT02' as a member of the transaction profile 'CARD' in the grouped CICS transaction class 'GCICSTRN', and print the command results to the job output. (rules SOM-BR-035)
2. GIVEN Profile: CARD in class GCICSTRN; Transaction: CT02 WHEN security administration job (RACFCMDS) runs THEN CT02 becomes a member of profile CARD, so users permitted to CARD are authorised for CT02; the command output is printed in the job listing. (SOM-C06-AC-01; SOM-BR-035)
