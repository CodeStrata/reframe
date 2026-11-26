# Feature specification: Request a bill payment

**Feature:** OATM-C19 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C19)

As a cardholder, I want to enter my account, see the balance owed and confirm or decline paying it, so that I only pay when I mean to and there is something to pay.

Lets a signed-on cardholder enter an account, see the balance owed, and then confirm or decline paying it in full. It must never post a payment without an explicit 'Y' or 'y'. It must never accept a payment when the balance is zero or less, and it must never run without a signed-on session.

**Acceptance scenarios:**

1. **Given** Session data: none, **when** the Bill Payment transaction is started with no session data, **then** The user is sent to the sign-on screen. (OATM-C19-AC-01)
2. **Given** First entry: yes; Selected account passed: none, **when** the Bill Payment screen is entered for the first time from another screen, **then** An empty bill payment screen is shown with the cursor on the account ID. (OATM-C19-AC-02)
3. **Given** Selected account passed: 00000000011; Current balance: $1,250.75, **when** the Bill Payment screen is first entered and an account was already selected (CDEMO-CB00-TRN-SELECTED), **then** The account ID 00000000011 and balance are shown with the message 'Confirm to make a bill payment...'. (OATM-C19-AC-03)
4. **Given** Key: PF3; Calling program: blank, **when** the user presses PF3 on the Bill Payment screen, **then** The main menu COMEN01C is shown. (OATM-C19-AC-04)
5. **Given** Key: PF7, **when** Bill-pay screen navigation and session entry applies, **then** The message 'Invalid key pressed. Please see below...' is shown. (OATM-C19-AC-05)
6. **Given** Key: PF4, **when** Bill-pay screen navigation and session entry applies, **then** Account ID, balance and confirmation are cleared. (OATM-C19-AC-06)
7. **Given** Account ID: (blank), **when** the account ID is blank, **then** 'Acct ID can NOT be empty...' is shown; no payment is made. (OATM-C19-AC-07)
8. **Given** Account ID: 99999999999; Account on file: no, **when** the account is looked up (confirmation 'Y', 'y' or blank) and does not exist, **then** 'Account ID NOT found...' is shown; no payment is made. (OATM-C19-AC-08)
9. **Given** Account ID: 00000000011; Account file: unavailable, **when** the account is looked up (confirmation 'Y', 'y' or blank) and does not exist, **then** 'Unable to lookup Account...' is shown; no payment is made. (OATM-C19-AC-09)
10. **Given** Account ID: 00000000011; ACCT-CURR-BAL: 0.00, **when** no error has been flagged, WHEN the account balance (`ACCT-CURR-BAL`) is zero or less and an account ID was entered, **then** Error flagged; screen shows 'You have nothing to pay...' with cursor on Account ID (OATM-C19-AC-10)
11. **Given** Account ID: 00000000011; ACCT-CURR-BAL: -25.00, **when** no error has been flagged, WHEN the account balance (`ACCT-CURR-BAL`) is zero or less and an account ID was entered, **then** Error flagged; screen shows 'You have nothing to pay...' (OATM-C19-AC-11)
12. **Given** Account ID: 00000000011; ACCT-CURR-BAL: 150.00, **when** no error has been flagged, WHEN the account balance (`ACCT-CURR-BAL`) is zero or less and an account ID was entered, **then** No error; the payment can proceed to confirmation (OATM-C19-AC-12)
13. **Given** Account ID: 00000000011; Confirm: (blank); Current balance: $500.00, **when** an account ID is entered and the confirmation is blank, **then** Balance $500.00 is shown with 'Confirm to make a bill payment...'; no payment is posted. (OATM-C19-AC-13)
14. **Given** Account ID: 00000000011; Confirm: y; Current balance: $500.00, **when** an account ID is entered and the confirmation is 'Y' or 'y', **then** A bill payment of $500.00 is posted to the account. (OATM-C19-AC-14)
15. **Given** Account ID: 00000000011; Confirm: N, **when** the confirmation is 'N' or 'n', **then** All fields are cleared; no payment is posted. (OATM-C19-AC-15)
16. **Given** Account ID: 00000000011; Confirm: X, **when** the confirmation is anything other than 'Y', 'y', 'N', 'n' or blank, **then** 'Invalid value. Valid values are (Y/N)...' is shown; no payment is posted. (OATM-C19-AC-16)

## Requirements

### Functional requirements

- **OATM-REQ-N-006** (business rule): When the Bill Payment transaction is started with no session data, the system shall transfer to the sign-on program (COSGN00C). Rules: OATM-BR-154.
- **OATM-REQ-F-149** (formatting): When the Bill Payment screen is entered for the first time from another screen, the system shall mark the session as re-entered, start with a blank screen with the cursor on the account ID, and display it. Rules: OATM-BR-155.
- **OATM-REQ-F-150** (business rule): When the Bill Payment screen is first entered and an account was already selected, the system shall fill in that account ID and process it as if Enter were pressed, before showing the screen. Rules: OATM-BR-156.
- **OATM-REQ-F-151** (formatting): When the user presses PF3 on the Bill Payment screen, the system shall return to the screen it was called from, or to the main menu (COMEN01C) when no caller is recorded. Rules: OATM-BR-157.
- **OATM-REQ-F-152** (formatting): When the user presses Enter the system shall process the payment request, when PF4 it shall clear all fields, and when any other key it shall show 'Invalid key pressed. Please see below...'. Rules: OATM-BR-158.
- **OATM-REQ-F-153** (business rule): If the account ID is blank, then the system shall show 'Acct ID can NOT be empty...', place the cursor on the account ID and make no payment. Rules: OATM-BR-159.
- **OATM-REQ-F-154** (business rule): If the account is looked up (confirmation 'Y', 'y' or blank) and does not exist, then the system shall show 'Account ID NOT found...' and make no payment, and on any other lookup failure show 'Unable to lookup Account...' and make no payment. Rules: OATM-BR-160.
- **OATM-REQ-F-155** (business rule): While no error has been flagged, when the account balance is zero or less and an account ID was entered, the system shall flag an error and show 'You have nothing to pay...'. Rules: OATM-BR-161.
- **OATM-REQ-F-156** (business rule): When an account ID is entered and the confirmation is blank, the system shall look up the account, show its current balance and the message 'Confirm to make a bill payment...', and post nothing (provided the balance is above zero). Rules: OATM-BR-162.
- **OATM-REQ-F-157** (business rule): When an account ID is entered and the confirmation is 'Y' or 'y', the system shall look up the account for update, show its balance and go on to post a payment for the full current balance. Rules: OATM-BR-163.
- **OATM-REQ-F-158** (business rule): When the confirmation is 'N' or 'n', the system shall clear the account ID, balance and confirmation fields, redisplay the empty screen and post nothing. Rules: OATM-BR-164.
- **OATM-REQ-F-159** (business rule): If the confirmation is anything other than 'Y', 'y', 'N', 'n' or blank, then the system shall show 'Invalid value. Valid values are (Y/N)...', place the cursor on the confirmation field and post nothing. Rules: OATM-BR-165.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-154 | Bill-pay screen navigation and session entry | business rule | WHEN the Bill Payment transaction is started with no session data, THE Bill Payment screen SHALL transfer to the sign-on program (COSGN00C). | medium | app/cbl/COBIL00C.cbl:107-144, app/cbl/COBIL00C.cbl:273-284, app/cbl/COBIL00C.cbl:552-566, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-155 | Start bill payment on first entry | formatting | WHEN the Bill Payment screen is entered for the first time from another screen, THE Bill Payment screen SHALL mark the session as re-entered, start with a blank screen with the cursor on the account ID, and display it. | medium | app/cbl/COBIL00C.cbl:107-122, app/cbl/COBIL00C.cbl:154-244 |
| OATM-BR-156 | Start bill payment on first entry | business rule | WHEN the Bill Payment screen is first entered and an account was already selected (CDEMO-CB00-TRN-SELECTED), THE Bill Payment screen SHALL fill in that account ID and process it as if Enter were pressed, before showing the screen. | medium | app/cbl/COBIL00C.cbl:107-122, app/cbl/COBIL00C.cbl:154-244 |
| OATM-BR-157 | Bill-pay screen navigation and session entry | formatting | WHEN the user presses PF3 on the Bill Payment screen, THE Bill Payment screen SHALL return to the screen it was called from, or to the main menu (COMEN01C) when no caller is recorded. | medium | app/cbl/COBIL00C.cbl:107-144, app/cbl/COBIL00C.cbl:273-284, app/cbl/COBIL00C.cbl:552-566, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-158 | Bill-pay screen navigation and session entry | formatting | WHEN the user presses Enter the screen SHALL process the payment request, WHEN PF4 it SHALL clear all fields, and WHEN any other key it SHALL show 'Invalid key pressed. Please see below...'. | medium | app/cbl/COBIL00C.cbl:107-144, app/cbl/COBIL00C.cbl:273-284, app/cbl/COBIL00C.cbl:552-566, app/cpy/CSMSG01Y.cpy:20-21 |
| OATM-BR-159 | Require account ID for payment | business rule | WHEN the account ID is blank, THE Bill Payment screen SHALL show 'Acct ID can NOT be empty...', place the cursor on the account ID and make no payment. | high | app/cbl/COBIL00C.cbl:158-167, app/cbl/COBIL00C.cbl:173-184, app/cbl/COBIL00C.cbl:343-372, app/cbl/COBIL00C.cbl:208-235 |
| OATM-BR-160 | Retrieve account for payment | business rule | WHEN the account is looked up (confirmation 'Y', 'y' or blank) and does not exist, THE Bill Payment screen SHALL show 'Account ID NOT found...' and make no payment; on any other lookup failure it SHALL show 'Unable to lookup Account...' and make no payment. | high | app/cbl/COBIL00C.cbl:158-167, app/cbl/COBIL00C.cbl:173-184, app/cbl/COBIL00C.cbl:343-372, app/cbl/COBIL00C.cbl:208-235 |
| OATM-BR-161 | Reject payment when nothing owed | business rule | WHILE no error has been flagged, WHEN the account balance (`ACCT-CURR-BAL`) is zero or less and an account ID was entered, THE Bill Payment Validation SHALL flag an error and show 'You have nothing to pay...' | medium | app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:197-206 |
| OATM-BR-162 | Look up account without confirmation | business rule | WHEN an account ID is entered and the confirmation is blank, THE Bill Payment screen SHALL look up the account, show its current balance and the message 'Confirm to make a bill payment...', and SHALL post nothing (provided the balance is above zero). | high | app/cbl/COBIL00C.cbl:154-195, app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:208-244, app/cbl/COBIL00C.cbl:552-566 |
| OATM-BR-163 | Accept confirmed payment and show balance | business rule | WHEN an account ID is entered and the confirmation is 'Y' or 'y', THE Bill Payment screen SHALL look up the account for update, show its balance and go on to post a payment for the full current balance. | high | app/cbl/COBIL00C.cbl:154-195, app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:208-244, app/cbl/COBIL00C.cbl:552-566 |
| OATM-BR-164 | Cancel payment on declined confirmation | business rule | WHEN the confirmation is 'N' or 'n', THE Bill Payment screen SHALL clear the account ID, balance and confirmation fields, redisplay the empty screen and post nothing. | high | app/cbl/COBIL00C.cbl:154-195, app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:208-244, app/cbl/COBIL00C.cbl:552-566 |
| OATM-BR-165 | Reject invalid confirmation value | business rule | WHEN the confirmation is anything other than 'Y', 'y', 'N', 'n' or blank, THE Bill Payment screen SHALL show 'Invalid value. Valid values are (Y/N)...', place the cursor on the confirmation field and post nothing. | high | app/cbl/COBIL00C.cbl:154-195, app/cbl/COBIL00C.cbl:197-206, app/cbl/COBIL00C.cbl:208-244, app/cbl/COBIL00C.cbl:552-566 |

### Key entities

- CVACT01Y (file record)
- CVACT03Y (file record)
- CVTRA05Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)

### Needs clarification

- SME-080: What should the bill payment screen do when it is opened without any information from the screen that called it? (Business analyst) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-081: What format and length must a new bill payment transaction ID have? It is currently the last ID plus 1. (Data architect) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-082: The bill payment transaction is saved before the account balance is reduced. If the account update then fails, what should happen to the saved transaction? Should the two be one all-or-nothing step? (Business analyst / architecture team) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-083: How must the system make sure that two bill payments made at the same time never get the same transaction ID? (Architecture team) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-084: If saving the bill payment transaction fails, what message should the user see and how should the failure be handled? (Business analyst) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-085: During a bill payment, should a failed card cross-reference lookup or a failed account update stop the remaining payment steps? (Business analyst) On OATM-BR-161, OATM-BR-156, OATM-BR-159, OATM-BR-160, OATM-BR-162, OATM-BR-163, OATM-BR-164, OATM-BR-165.
- SME-086: Please confirm the full rule for checking the account ID on bill payment: it is required, it must exist, and which error message goes with each case. (Legacy application SME) On OATM-BR-160.
- SME-087: If the user enters 'Y' on the first submission, the bill payment is posted straight away without first showing the balance. Should the balance always be shown before a payment can be confirmed? (Payments business owner) On OATM-BR-165.
- DEF-046: Is this intended? A failed card cross-reference lookup sets an error message but does not stop the posting: the transaction is still written (with whatever card number is in the cross-reference record) and the balance is still reduced and saved. (Subject-matter expert) On OATM-BR-159, OATM-BR-160.
- DEF-112: Is this intended? When a selected account is passed on first entry, the Enter processing already sends the screen and the first-entry logic then sends it again, so the screen is sent twice in one interaction. (Subject-matter expert) On OATM-BR-156.

### Decision table gaps

None.
