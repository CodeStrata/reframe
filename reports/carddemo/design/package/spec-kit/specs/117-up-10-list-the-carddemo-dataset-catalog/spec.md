# Feature specification: List the CardDemo dataset catalog

**Feature:** UP-C10 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C10)

As a CardDemo operator, I want a report of every catalogued CardDemo dataset with its attributes, so that I can review what datasets exist.

An operator report of every CardDemo dataset that exists, with all its attributes, replacing the previous report each time it runs. It must list every CardDemo dataset and must never leave a half-written report behind when the run fails.

**Acceptance scenarios:**

1. **Given** cleanup step return code: 0, **when** the earlier step that deletes the previous catalog listing report ends with return code 0, **then** A new AWS.M2.CARDDEMO.LISTCAT report lists all AWS.M2.CARDDEMO catalog entries with all attributes. (UP-C10-AC-01)
2. **Given** cleanup step return code: 8, **when** the earlier step that deletes the previous catalog listing report ends with return code 0, **then** The listing step is skipped and no report is produced. (UP-C10-AC-02)

## Requirements

### Functional requirements

- **UP-REQ-F-047** (formatting): When the earlier step that deletes the previous catalog listing report ends with return code 0, the system shall list every catalog entry under the AWS.M2.CARDDEMO qualifier, with all attributes, into a new report (AWS.M2.CARDDEMO.LISTCAT) of fixed-length 133-byte print records, cataloging it on success and deleting it if the step fails. Rules: UP-BR-050.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-050 | List the CardDemo dataset catalog | formatting | WHEN the earlier step that deletes the previous catalog listing report ends with return code 0, THE catalog listing job SHALL list every catalog entry under the AWS.M2.CARDDEMO qualifier, with all attributes, into a new report (AWS.M2.CARDDEMO.LISTCAT) of fixed-length 133-byte print records, cataloging it on success and deleting it if the step fails. | medium | samples/jcl/LISTCAT.jcl:21-26, samples/jcl/LISTCAT.jcl:27-35 |

### Key entities

None found in the source.

### Needs clarification

None.

### Decision table gaps

None.
