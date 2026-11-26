# Feature specification: Save confirmed account and customer changes

**Feature:** OATM-C13 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C13)

As an operator, I want my confirmed changes saved to both the account and customer records together, so that the two records never end up out of step.

Saves an operator's confirmed changes to an account and its customer as one unit of work: the account record first, then the customer record. It must never leave the two out of step. If either record cannot be locked, or either save fails, nothing is kept and the operator is told the changes were unsuccessful.

**Acceptance scenarios:**

1. **Given** Key: PF5; Account record: held by another user, **when** the operator presses PF5 to confirm validated changes, **then** Nothing is saved; 'Could not lock account record for update' is shown and the screen reports a failure. (OATM-C13-AC-01)
2. **Given** Key: PF5; Customer record: cannot be read for update, **when** the operator presses PF5 to confirm validated changes, **then** Nothing is saved; 'Could not lock customer record for update' is shown. (OATM-C13-AC-02)
3. **Given** Account rewrite: fails, **when** the account rewrite fails, **then** 'Update of record failed'; the customer record is not rewritten. (OATM-C13-AC-03)
4. **Given** Account rewrite: succeeds; Customer rewrite: fails, **when** the customer rewrite fails, **then** Account change is rolled back; 'Update of record failed' is shown. (OATM-C13-AC-04)
5. **Given** Account rewrite: succeeds; Customer rewrite: succeeds, **when** both rewrites succeed, **then** Update confirmed as successful. (OATM-C13-AC-05)
6. **Given** save outcome: account locked by another task, **when** a save fails because the account could not be locked ('L') or the update failed ('F'), **then** State 'L'; message 'Changes unsuccessful. Please try again' (OATM-C13-AC-06)
7. **Given** An operator has validated changes to account 00000000001 (new status 'Y', current balance 1500.00, credit limit 5000.00, cash credit limit 1000.00, cycle credit 200.00, cycle debit 300.00, group 'GOLD', open date 2020-01-15, expiry date 2027-01-31, reissue date 2025-01-31), and both the account and the customer records are locked and unchanged by anyone else since they were shown, **when** The operator confirms with PF5, **then** The account master record for 00000000001 is rewritten with exactly those status, balance, limit, cycle credit and debit and group values, and its open, expiry and reissue dates are stored as '2020-01-15', '2027-01-31' and '2025-01-31' (YYYY-MM-DD) (OATM-C13-AC-07)
8. **Given** The account rewrite for a confirmed change has succeeded, and the operator's changes to the linked customer include phone area 212, prefix 555, line 1234, date of birth 1985-03-07, plus new name, address, SSN, government ID, EFT account, primary holder indicator 'Y' and FICO score 720, **when** The account update goes on to save the customer, **then** The customer master record is rewritten with the new name, address, SSN, government ID, EFT account, primary holder indicator 'Y' and FICO score 720, the phone is stored as '(212)555-1234' and the date of birth as '1985-03-07' (OATM-C13-AC-08)

## Requirements

### Functional requirements

- **OATM-REQ-F-107** (error handling): When the operator presses PF5 to confirm validated changes, the system shall read the account record and then the customer record for update. Rules: OATM-BR-110.
- **OATM-REQ-F-108** (error handling): If the account or customer record cannot be locked, then the system shall stop without saving and show 'Could not lock account record for update' or 'Could not lock customer record for update'. Rules: OATM-BR-110.
- **OATM-REQ-F-109** (business rule): When both records are locked and neither was changed by someone else since it was shown, the system shall rewrite the account master (ACCTDAT) with the new status, balance, limits, cycle credit and debit, group and the open, expiry and reissue dates as YYYY-MM-DD. Rules: OATM-BR-111.
- **OATM-REQ-F-110** (error handling): If the account rewrite fails, then the system shall not update the customer and shall show 'Update of record failed'. Rules: OATM-BR-112.
- **OATM-REQ-F-111** (business rule): When the account rewrite succeeds, the system shall rewrite the customer master (CUSTDAT) with the new name, address, phones formatted as '(aaa)bbb-cccc', SSN, government ID, date of birth as YYYY-MM-DD, EFT account, primary holder indicator and FICO score. Rules: OATM-BR-113.
- **OATM-REQ-N-004** (error handling): If the customer rewrite fails, then the system shall roll back the account rewrite (SYNCPOINT ROLLBACK) and show 'Update of record failed'. Rules: OATM-BR-114.
- **OATM-REQ-F-112** (formatting): When both rewrites succeed, the system shall mark the change as done and tell the operator the update succeeded. Rules: OATM-BR-115.
- **OATM-REQ-F-113** (error handling): If a save fails because the account could not be locked ('L') or the update failed ('F'), then the system shall show the message 'Changes unsuccessful. Please try again'. Rules: OATM-BR-116.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-110 | Atomic two-record update with locking and rollback | error handling | WHEN the operator presses PF5 to confirm validated changes, THE account update SHALL read the account record and then the customer record for update, and stop without saving if either cannot be locked, showing 'Could not lock account record for update' or 'Could not lock customer record for update'. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-111 | Rewrite account master with new values | business rule | WHEN both records are locked and neither was changed by someone else since it was shown, THE account update SHALL rewrite the account master (ACCTDAT) with the new status, balance, limits, cycle credit and debit, group and the open, expiry and reissue dates as YYYY-MM-DD. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-112 | Rewrite account master with new values | error handling | WHEN the account rewrite fails, THE account update SHALL not update the customer and SHALL show 'Update of record failed'. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-113 | Rewrite customer master with new values | business rule | WHEN the account rewrite succeeds, THE account update SHALL rewrite the customer master (CUSTDAT) with the new name, address, phones formatted as '(aaa)bbb-cccc', SSN, government ID, date of birth as YYYY-MM-DD, EFT account, primary holder indicator and FICO score. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-114 | Rewrite customer master with new values | error handling | WHEN the customer rewrite fails, THE account update SHALL roll back the account rewrite (SYNCPOINT ROLLBACK) and show 'Update of record failed'. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-115 | Atomic two-record update with locking and rollback | formatting | WHEN both rewrites succeed, THE account update SHALL mark the change as done and tell the operator the update succeeded. | high | app/cbl/COACTUPC.cbl:2602-2615, app/cbl/COACTUPC.cbl:3888-3953, app/cbl/COACTUPC.cbl:3954-4062, app/cbl/COACTUPC.cbl:4065-4104 |
| OATM-BR-116 | Inform operator of failed update | error handling | WHEN a save fails because the account could not be locked ('L') or the update failed ('F'), THE account update screen SHALL show the message 'Changes unsuccessful. Please try again'. | high | app/cbl/COACTUPC.cbl:654-668, app/cbl/COACTUPC.cbl:879-891, app/cbl/COACTUPC.cbl:904-915, app/cbl/COACTUPC.cbl:964-1002 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSLKPCDY (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDPY (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

- SME-066: When account update saves changes, the account record is written before the customer record. Must both be saved together, so that if the customer save fails the account change is rolled back? How critical is this, given it changes balances, limits and regulated customer data? (Account servicing SME / architecture team) On OATM-BR-112, OATM-BR-114, OATM-BR-115.
- DEF-057: Is this intended? A customer lock failure is not handled in the outcome EVALUATE, so it falls to WHEN OTHER and the change is marked done ('C') with an update-success prompt although nothing was saved; likewise if a message was already set, the lock-failure flag is never set and the outcome also falls to 'C'. (Subject-matter expert) On OATM-BR-112, OATM-BR-114, OATM-BR-115.
- DEF-074: Is this intended? The decision step has a branch that turns a committed save ('C') back into 'details shown' and clears the account and card number when there is no calling transaction, but it can never run: the main dispatch catches state 'C' first on the next interaction and resets the screen itself. The field edits also skip the 'C' state check for the same reason. (Subject-matter expert) On OATM-BR-116.

### Decision table gaps

- Two-record save outcome: No rule states what the operator sees or what happens when a record was changed by someone else since it was shown.
