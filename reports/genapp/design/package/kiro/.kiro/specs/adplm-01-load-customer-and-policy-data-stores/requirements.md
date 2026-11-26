# Requirements: Load customer and policy data stores (ADPLM-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Application Deployment Lifecycle Management · Application Deployment and Policy Lifecycle Management · runs as scheduled job · risk medium

## Introduction

Fills the new customer store and policy store with every record from the supplied customer and policy input files, so the online application starts with its existing records already in place. It is run by application administrators as part of setting up an environment. Each load runs only if its store was created successfully, and it must copy every record, with none dropped or changed.

**User story:** As an application administrator, I want the new customer and policy data stores filled from the supplied input data sets once they are defined, so that the online application starts with its customer and policy records in place.

## Requirements

### Requirement 1: ADPLM-REQ-F-001 (design note)

#### Acceptance criteria

1. When the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run, the system shall copy every record from the supplied policy input data set into the new policy data store (KSDSPOLY). (rules ADPLM-BR-001)
2. GIVEN DEFINE2 return code: 0 WHEN the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run THEN all policy records are copied into KSDSPOLY (ADPLM-C01-AC-01; ADPLM-BR-001)
3. GIVEN DEFINE2 return code: 8 WHEN the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run THEN the policy load step is skipped (ADPLM-C01-AC-02; ADPLM-BR-001)

### Requirement 2: ADPLM-REQ-F-002 (design note)

#### Acceptance criteria

1. If the step that defines the policy data store (DEFINE2) ends with a return code above 7, then the system shall skip the load of the policy data store. (rules ADPLM-BR-001)
2. GIVEN DEFINE2 return code: 0 WHEN the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run THEN all policy records are copied into KSDSPOLY (ADPLM-C01-AC-01; ADPLM-BR-001)
3. GIVEN DEFINE2 return code: 8 WHEN the step that defines the policy data store (DEFINE2) ends with a return code of 7 or less, or did not run THEN the policy load step is skipped (ADPLM-C01-AC-02; ADPLM-BR-001)

### Requirement 3: ADPLM-REQ-F-003 (design note)

#### Acceptance criteria

1. When the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run, the system shall copy every record from the supplied customer input data set into the new customer data store (KSDSCUST). (rules ADPLM-BR-002)
2. GIVEN DEFINE1 return code: 0 WHEN the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run THEN all customer records are copied into KSDSCUST (ADPLM-C01-AC-03; ADPLM-BR-002)
3. GIVEN DEFINE1 return code: 12 WHEN the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run THEN the customer load step is skipped (ADPLM-C01-AC-04; ADPLM-BR-002)

### Requirement 4: ADPLM-REQ-F-004 (design note)

#### Acceptance criteria

1. If the step that defines the customer data store (DEFINE1) ends with a return code above 7, then the system shall skip the load of the customer data store. (rules ADPLM-BR-002)
2. GIVEN DEFINE1 return code: 0 WHEN the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run THEN all customer records are copied into KSDSCUST (ADPLM-C01-AC-03; ADPLM-BR-002)
3. GIVEN DEFINE1 return code: 12 WHEN the step that defines the customer data store (DEFINE1) ends with a return code of 7 or less, or did not run THEN the customer load step is skipped (ADPLM-C01-AC-04; ADPLM-BR-002)
