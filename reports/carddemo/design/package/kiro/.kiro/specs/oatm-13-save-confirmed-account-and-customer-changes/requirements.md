# Requirements: Save confirmed account and customer changes (OATM-C13)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Saves an operator's confirmed changes to an account and its customer as one unit of work: first the account record, then the customer record. It must never leave the two out of step. If either record cannot be locked, if someone else changed either one since it was shown, or if either save fails, nothing may be kept, and the operator must be told the update did not go through.

**User story:** As an operator, I want my confirmed changes saved to both the account and customer records together, so that the two records never end up out of step.

## Requirements

### Requirement 1: OATM-REQ-F-107 (error handling)

#### Acceptance criteria

1. When the operator presses PF5 to confirm validated changes, the system shall read the account record and then the customer record for update. (rules OATM-BR-110)
2. GIVEN Key: PF5; Account record: held by another user WHEN the operator presses PF5 to confirm validated changes THEN Nothing is saved; 'Could not lock account record for update' is shown and the screen reports a failure. (OATM-C13-AC-01; OATM-BR-110)
3. GIVEN Key: PF5; Customer record: cannot be read for update WHEN the operator presses PF5 to confirm validated changes THEN Nothing is saved; 'Could not lock customer record for update' is shown. (OATM-C13-AC-02; OATM-BR-110)

### Requirement 2: OATM-REQ-F-108 (error handling)

#### Acceptance criteria

1. If the account or customer record cannot be locked, then the system shall stop without saving and show 'Could not lock account record for update' or 'Could not lock customer record for update'. (rules OATM-BR-110)
2. GIVEN Key: PF5; Account record: held by another user WHEN the operator presses PF5 to confirm validated changes THEN Nothing is saved; 'Could not lock account record for update' is shown and the screen reports a failure. (OATM-C13-AC-01; OATM-BR-110)
3. GIVEN Key: PF5; Customer record: cannot be read for update WHEN the operator presses PF5 to confirm validated changes THEN Nothing is saved; 'Could not lock customer record for update' is shown. (OATM-C13-AC-02; OATM-BR-110)

### Requirement 3: OATM-REQ-F-109 (business rule)

#### Acceptance criteria

1. When both records are locked and neither was changed by someone else since it was shown, the system shall rewrite the account master (ACCTDAT) with the new status, balance, limits, cycle credit and debit, group and the open, expiry and reissue dates as YYYY-MM-DD. (rules OATM-BR-111)
2. GIVEN An operator has validated changes to account 00000012345 (status, current balance, credit limit, cash credit limit, cycle credit and debit, group, and open, expiry and reissue dates entered as year, month and day). Both the account and customer records are locked and neither has changed since they were shown WHEN The operator confirms with PF5 THEN The account record is saved with the new status, balance, limits, cycle credit and debit, group, and with the open, expiry and reissue dates stored as YYYY-MM-DD (for example 2025-03-01) (OATM-C13-AC-07; OATM-BR-111)

### Requirement 4: OATM-REQ-F-110 (error handling)

#### Acceptance criteria

1. If the account rewrite fails, then the system shall not update the customer and shall show 'Update of record failed'. (rules OATM-BR-112)
2. GIVEN Account rewrite: fails WHEN the account rewrite fails THEN 'Update of record failed'; the customer record is not rewritten. (OATM-C13-AC-03; OATM-BR-112)

### Requirement 5: OATM-REQ-F-111 (business rule)

#### Acceptance criteria

1. When the account rewrite succeeds, the system shall rewrite the customer master (CUSTDAT) with the new name, address, phones formatted as '(aaa)bbb-cccc', SSN, government ID, date of birth as YYYY-MM-DD, EFT account, primary holder indicator and FICO score. (rules OATM-BR-113)
2. GIVEN The account record of a confirmed update has just been saved, and the operator entered phone number 1 as area 212, prefix 555 and line 0100 and date of birth as 1980, 07, 15 WHEN The system saves the customer record THEN The customer record holds the new name, address, SSN, government ID, EFT account, primary holder indicator and FICO score, phone number 1 is stored as '(212)555-0100' and date of birth as '1980-07-15' (OATM-C13-AC-08; OATM-BR-113)

### Requirement 6: OATM-REQ-N-004 (error handling)

#### Acceptance criteria

1. If the customer rewrite fails, then the system shall roll back the account rewrite (SYNCPOINT ROLLBACK) and show 'Update of record failed'. (rules OATM-BR-114)
2. GIVEN Account rewrite: succeeds; Customer rewrite: fails WHEN the customer rewrite fails THEN Account change is rolled back; 'Update of record failed' is shown. (OATM-C13-AC-04; OATM-BR-114)

### Requirement 7: OATM-REQ-F-112 (formatting)

#### Acceptance criteria

1. When both rewrites succeed, the system shall mark the change as done and tell the operator the update succeeded. (rules OATM-BR-115)
2. GIVEN Account rewrite: succeeds; Customer rewrite: succeeds WHEN both rewrites succeed THEN Update confirmed as successful. (OATM-C13-AC-05; OATM-BR-115)

### Requirement 8: OATM-REQ-F-113 (error handling)

#### Acceptance criteria

1. If a save fails because the account could not be locked ('L') or the update failed ('F'), then the system shall show the message 'Changes unsuccessful. Please try again'. (rules OATM-BR-116)
2. GIVEN save outcome: account locked by another task WHEN a save fails because the account could not be locked ('L') or the update failed ('F') THEN State 'L'; message 'Changes unsuccessful. Please try again' (OATM-C13-AC-06; OATM-BR-116)
