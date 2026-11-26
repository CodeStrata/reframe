# Requirements: View authorization detail and mark fraud (CAFM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk medium

## Introduction

Shows a fraud analyst one authorization in full: approved 'A' in green or declined 'D' in red, with the decline reason as '<code>-<description>'. One key toggles its fraud mark, reporting the authorization as fraud ('F') or withdrawing the report ('R'), and passes it on to fraud processing. The toggle must always work from the freshly read record. An unknown reason code must show as '9999-ERROR', never blank.

**User story:** As a fraud analyst, I want to see an authorization's details with its decline reason and toggle its fraud mark, so that suspected fraud can be reported or withdrawn.

## Requirements

### Requirement 1: CAFM-REQ-F-112 (formatting)

#### Acceptance criteria

1. When authorization details are being populated, the system shall show the reason as '<code>-<description>' from the decline reason table, or as '9999-ERROR' when the code is not in the table. (rules CAFM-BR-118)
2. GIVEN One authorization with reason code '4100', which is in the decline reason table, and another with reason code '7777', which is not WHEN Each authorization's details are shown THEN The first shows its reason as '4100-' followed by that code's description from the decline reason table. The second shows '9999-ERROR'. (CAFM-C12-AC-06; CAFM-BR-118)

### Requirement 2: CAFM-REQ-F-113 (formatting)

#### Acceptance criteria

1. When the authorization detail screen shows an authorization, the system shall show response 'A' in green when the response code is '00', otherwise 'D' in red. (rules CAFM-BR-119)
2. GIVEN response code: 00 WHEN the authorization detail screen shows an authorization THEN 'A' shown in green. (CAFM-C12-AC-01; CAFM-BR-119)
3. GIVEN response code: 05 WHEN the authorization detail screen shows an authorization THEN 'D' shown in red. (CAFM-C12-AC-02; CAFM-BR-119)

### Requirement 3: CAFM-REQ-F-114 (business rule)

#### Acceptance criteria

1. When the user presses PF5 on the selected authorization, the system shall re-read the authorization and, if its fraud flag is 'F', set it to 'R' with a remove-fraud action 'R', otherwise set it to 'F' with a report-fraud action 'F', and pass the record with account and customer number to the fraud processor (COPAUS2C). (rules CAFM-BR-120)
2. GIVEN fraud flag: F WHEN the user presses PF5 on the selected authorization THEN Flag becomes 'R' and the fraud processor is asked to remove the fraud report. (CAFM-C12-AC-03; CAFM-BR-120)
3. GIVEN fraud flag: blank WHEN the user presses PF5 on the selected authorization THEN Flag becomes 'F' and the fraud processor is asked to report fraud. (CAFM-C12-AC-04; CAFM-BR-120)
4. GIVEN fraud flag: R WHEN the user presses PF5 on the selected authorization THEN Flag becomes 'F' and the fraud processor is asked to report fraud. (CAFM-C12-AC-05; CAFM-BR-120)
