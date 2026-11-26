# Requirements: List the CardDemo dataset catalog (UP-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Programs not in a business function · Unassigned-Programs · runs as scheduled job · risk low

## Introduction

An operator report of every CardDemo dataset that exists, with all its attributes, replacing the previous report each time it runs. It must list every CardDemo dataset and must never leave a half-written report behind when the run fails.

**User story:** As a CardDemo operator, I want a report of every catalogued CardDemo dataset with its attributes, so that I can review what datasets exist.

## Requirements

### Requirement 1: UP-REQ-F-047 (formatting)

#### Acceptance criteria

1. When the earlier step that deletes the previous catalog listing report ends with return code 0, the system shall list every catalog entry under the AWS.M2.CARDDEMO qualifier, with all attributes, into a new report (AWS.M2.CARDDEMO.LISTCAT) of fixed-length 133-byte print records, cataloging it on success and deleting it if the step fails. (rules UP-BR-050)
2. GIVEN cleanup step return code: 0 WHEN the earlier step that deletes the previous catalog listing report ends with return code 0 THEN A new AWS.M2.CARDDEMO.LISTCAT report lists all AWS.M2.CARDDEMO catalog entries with all attributes. (UP-C10-AC-01; UP-BR-050)
3. GIVEN cleanup step return code: 8 WHEN the earlier step that deletes the previous catalog listing report ends with return code 0 THEN The listing step is skipped and no report is produced. (UP-C10-AC-02; UP-BR-050)
