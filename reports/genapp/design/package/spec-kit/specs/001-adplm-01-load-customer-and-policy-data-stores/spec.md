# Feature specification: Load customer and policy data stores

**Feature:** ADPLM-C01 · Application Deployment and Policy Lifecycle Management · Application Deployment Lifecycle Management

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (ADPLM-C01)

As an application administrator, I want the new customer and policy data stores filled from the supplied input data sets once they are defined, so that the online application starts with its customer and policy records in place.

Fills the new customer store and policy store with every record from the supplied customer and policy input files, so the online application starts with its existing records already in place. It is run by application administrators as part of setting up an environment. Each load runs only if its store was created successfully, and it must copy every record, with none dropped or changed.

**Acceptance scenarios:**

1. **Given** DEFINE2 return code: 0, **when** the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run, **then** all policy records are copied into KSDSPOLY (ADPLM-C01-AC-01)
2. **Given** DEFINE2 return code: 8, **when** the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run, **then** the policy load step is skipped (ADPLM-C01-AC-02)
3. **Given** DEFINE1 return code: 0, **when** the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run, **then** all customer records are copied into KSDSCUST (ADPLM-C01-AC-03)
4. **Given** DEFINE1 return code: 12, **when** the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run, **then** the customer load step is skipped (ADPLM-C01-AC-04)

## Requirements

### Functional requirements

- **ADPLM-REQ-F-001** (design note): When the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run, the system shall copy every record from the supplied policy input data set into the new policy data store (KSDSPOLY). Rules: ADPLM-BR-001.
- **ADPLM-REQ-F-002** (design note): If the step that defines the policy data store (DEFINE2) ends with a return code above 7, then the system shall skip the load of the policy data store. Rules: ADPLM-BR-001.
- **ADPLM-REQ-F-003** (design note): When the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run, the system shall copy every record from the supplied customer input data set into the new customer data store (KSDSCUST). Rules: ADPLM-BR-002.
- **ADPLM-REQ-F-004** (design note): If the step that defines the customer data store (DEFINE1) ends with a return code above 7, then the system shall skip the load of the customer data store. Rules: ADPLM-BR-002.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| ADPLM-BR-001 | Load second data store from input | design note | WHEN the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run, THE data store setup job SHALL copy every record from the supplied policy input data set into the new policy data store (KSDSPOLY); WHEN DEFINE2 ends above 7, it SHALL skip the load. | medium | base/cntl/adef121.jcl:37-52, base/cntl/adef121.jcl:65-73 |
| ADPLM-BR-002 | Load first data store from input | design note | WHEN the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run, THE data store setup job SHALL copy every record from the supplied customer input data set into the new customer data store (KSDSCUST); WHEN DEFINE1 ends above 7, it SHALL skip the load. | medium | base/cntl/adef121.jcl:12-27, base/cntl/adef121.jcl:55-63 |

### Key entities

None found in the source.

### Needs clarification

- SME-001: The two data loads are identified only by legacy labels. Which data stores are the input and the target for the first load and for the second load? (Application data owner) On ADPLM-BR-001, ADPLM-BR-002.
- SME-002: Each load copies every record into its target store. Is the target store empty before the load, or are existing records replaced, merged, or rejected as duplicates? (Application data owner) On ADPLM-BR-001, ADPLM-BR-002.
- SME-003: If a load stops partway through, should a rerun start again from the beginning, and must the target store be cleared first? (Batch operations) On ADPLM-BR-001, ADPLM-BR-002.

### Decision table gaps

None.
