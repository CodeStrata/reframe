# Design: List the CardDemo dataset catalog (UP-C10)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

An operator report of every CardDemo dataset that exists, with all its attributes, replacing the previous report each time it runs. It must list every CardDemo dataset and must never leave a half-written report behind when the run fails.

Runs as scheduled job.

## Screens and components

No screens: it runs as scheduled job.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-050 | List the CardDemo dataset catalog | formatting | WHEN the earlier step that deletes the previous catalog listing report ends with return code 0, THE catalog listing job SHALL list every catalog entry under the AWS.M2.CARDDEMO qualifier, with all attributes, into a new report (AWS.M2.CARDDEMO.LISTCAT) of fixed-length 133-byte print records, cataloging it on success and deleting it if the step fails. | medium | samples/jcl/LISTCAT.jcl:21-26, samples/jcl/LISTCAT.jcl:27-35 |

### Worked examples

- UP-BR-050: cleanup step return code = 0 → A new AWS.M2.CARDDEMO.LISTCAT report lists all AWS.M2.CARDDEMO catalog entries with all attributes.
- UP-BR-050: cleanup step return code = 8 → The listing step is skipped and no report is produced.

## Decision tables

None.

## Design notes

None.

## Open questions

None.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (2 in all).