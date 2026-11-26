# Requirements: Save confirmed account and customer changes (OATM-C13)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk high

## Introduction

Saves an operator's confirmed changes to an account and its customer as one unit of work: the account record first, then the customer record. It must never leave the two out of step. If either record cannot be locked, or either save fails, nothing is kept and the operator is told the changes were unsuccessful.

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
2. GIVEN An operator has validated changes to account 00000000001 (new status 'Y', current balance 1500.00, credit limit 5000.00, cash credit limit 1000.00, cycle credit 200.00, cycle debit 300.00, group 'GOLD', open date 2020-01-15, expiry date 2027-01-31, reissue date 2025-01-31), and both the account and the customer records are locked and unchanged by anyone else since they were shown WHEN The operator confirms with PF5 THEN The account master record for 00000000001 is rewritten with exactly those status, balance, limit, cycle credit and debit and group values, and its open, expiry and reissue dates are stored as '2020-01-15', '2027-01-31' and '2025-01-31' (YYYY-MM-DD) (OATM-C13-AC-07; OATM-BR-111)

### Requirement 4: OATM-REQ-F-110 (error handling)

#### Acceptance criteria

1. If the account rewrite fails, then the system shall not update the customer and shall show 'Update of record failed'. (rules OATM-BR-112)
2. GIVEN Account rewrite: fails WHEN the account rewrite fails THEN 'Update of record failed'; the customer record is not rewritten. (OATM-C13-AC-03; OATM-BR-112)

### Requirement 5: OATM-REQ-F-111 (business rule)

#### Acceptance criteria

1. When the account rewrite succeeds, the system shall rewrite the customer master (CUSTDAT) with the new name, address, phones formatted as '(aaa)bbb-cccc', SSN, government ID, date of birth as YYYY-MM-DD, EFT account, primary holder indicator and FICO score. (rules OATM-BR-113)
2. GIVEN The account rewrite for a confirmed change has succeeded, and the operator's changes to the linked customer include phone area 212, prefix 555, line 1234, date of birth 1985-03-07, plus new name, address, SSN, government ID, EFT account, primary holder indicator 'Y' and FICO score 720 WHEN The account update goes on to save the customer THEN The customer master record is rewritten with the new name, address, SSN, government ID, EFT account, primary holder indicator 'Y' and FICO score 720, the phone is stored as '(212)555-1234' and the date of birth as '1985-03-07' (OATM-C13-AC-08; OATM-BR-113)

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
