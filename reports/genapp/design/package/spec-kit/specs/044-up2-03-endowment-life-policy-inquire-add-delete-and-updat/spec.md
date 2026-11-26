# Feature specification: Endowment (life) policy inquire, add, delete and update

**Feature:** UP2-C03 · Unassigned programs · Unassigned programs

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP2-C03)

As a policy administrator, I want to inquire on, add, delete and update endowment (life) policies from the endowment policy screen, so that customers' life cover is recorded correctly.

Lets policy administrators look up, add, delete and update a customer's endowment (life) policy: fund, term, sum assured, life assured and the with-profits, managed-fund and equities indicators. Policies entered here always carry payment 0 and no broker, a failed add must be rolled back, and every failure must clear the screen ready for the next attempt. In the legacy screen the add-failure message ('Customer does not exist' or 'Error Adding Life Policy') goes to the motor screen's message field, so the user never sees it; the team must decide whether to keep that behaviour on purpose.

**Acceptance scenarios:**

1. **Given** Option: 3; Customer number: 0000000001; Policy number: 0000000001, **when** endowment policy screen runs, **then** The delete program is called with request '01DEND'; on success 'Life Policy Deleted' is shown. (UP2-C03-AC-01)
2. **Given** Option: 7, **when** the operator presses Enter on the endowment policy screen with an option other than '1', '2', '3' or '4', **then** 'Please enter a valid option' is shown and the cursor sits on the option field. (UP2-C03-AC-02)
3. **Given** Option: (blank), **when** the operator presses Enter on the endowment policy screen with an option other than '1', '2', '3' or '4', **then** 'Please enter a valid option' is shown; nothing is inquired, added, deleted or updated. (UP2-C03-AC-03)
4. **Given** Key pressed: PF3, **when** the operator presses PF3, **then** The screen is erased and 'Transaction ended' is shown. (UP2-C03-AC-04)
5. **Given** Key pressed: CLEAR, **when** the operator presses PF3, **then** A blank endowment screen is shown. (UP2-C03-AC-05)
6. **Given** Option: 1; Customer number: 0000000001; Policy number: 0000000001; Return code: 0, **when** the operator chooses option '1' with a customer number and policy number, **then** The policy's dates, fund name, term, sum assured, life assured and fund flags are shown. (UP2-C03-AC-06)
7. **Given** Option: 1; Policy number: 0000009999 (not on file); Return code: 01, **when** the endowment policy inquiry returns a non-zero code, **then** 'No data was returned.' is shown. (UP2-C03-AC-07)
8. **Given** Option: 2; Customer number: 0000000001; Fund name: GROWTH; Term: 20; Sum assured: 100000, **when** the operator chooses option '2', **then** A new endowment policy is requested with payment 0 and no broker. (UP2-C03-AC-08)
9. **Given** Request: 01UHOU; Stored broker id: 1234, **when** a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND), **then** The update is sent with broker id 0, payment 0 and a blank broker reference (UP2-C03-AC-09)
10. **Given** Request: 01AEND, **when** a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND), **then** The new endowment policy is sent with payment 0, broker id 0 and a blank broker reference (UP2-C03-AC-10)
11. **Given** Option: 2; Return code: 0; New policy number: 0000000042, **when** adding the endowment policy succeeds, **then** Policy number 0000000042 and 'New Life Policy Inserted' are shown. (UP2-C03-AC-11)
12. **Given** Option: 2; Return code: 70, **when** adding the endowment policy returns a non-zero code, **then** The add is rolled back and the screen is reset. (UP2-C03-AC-12)
13. **Given** Option: 2; Customer number: 9999999999 (not on file); Back-end return code: 70, **when** adding an endowment policy fails because the customer is not on file (return code 70), **then** The add is rolled back and the endowment screen is shown again; the next Enter starts from a cleared screen. (UP2-C03-AC-13)
14. **Given** Option: 2; Back-end return code: 70, **when** adding an endowment policy fails, **then** 'Customer does not exist' is not shown; the endowment screen message line stays as it was. (UP2-C03-AC-14)
15. **Given** Option: 2; Back-end return code: 90, **when** adding an endowment policy fails, **then** 'Error Adding Life Policy' is not shown on the endowment screen. (UP2-C03-AC-15)
16. **Given** Option: 4; Customer number: 0000000001; Policy number: 0000000001; Term (changed): 20 to 25, **when** the operator chooses option '4', **then** The update is sent with term 25 and the other fields as shown on the screen. (UP2-C03-AC-16)
17. **Given** Option: 4; Update return code: 02, **when** the endowment policy update returns a non-zero code, **then** 'Error Updating Life Policy' is shown. (UP2-C03-AC-17)
18. **Given** Option: 4; Inquiry return code: 01, **when** the endowment policy update returns a non-zero code, **then** 'No data was returned.' is shown and no update is attempted. (UP2-C03-AC-18)
19. **Given** Option: 4; Update return code: 0, **when** the endowment policy update succeeds, **then** 'Life Policy Updated' is shown and the option field is blank. (UP2-C03-AC-19)
20. **Given** Option: 3; Delete return code: 01, **when** an inquiry, add, delete or update of an endowment policy fails, **then** 'Error Deleting Life Policy' is shown; the next Enter starts with empty conversation data. (UP2-C03-AC-20)
21. **Given** Option: 1; Inquiry return code: 01, **when** an inquiry, add, delete or update of an endowment policy fails, **then** 'No data was returned.' is shown and the conversation data is cleared. (UP2-C03-AC-21)

## Requirements

### Functional requirements

- **UP2-REQ-F-029** (business rule): The system shall treat endowment policy screen option '1' as inquire (LGIPOL01), '2' as add (LGAPOL01), '3' as delete (LGDPOL01) and '4' as inquire-then-update (LGIPOL01 then LGUPOL01). Rules: UP2-BR-023.
- **UP2-REQ-F-030** (business rule): If the operator presses Enter on the endowment policy screen with an option other than '1', '2', '3' or '4', then the system shall call no back-end program, show 'Please enter a valid option' with the cursor on the option field, and wait for the next input under transaction SSP2. Rules: UP2-BR-024.
- **UP2-REQ-F-031** (formatting): When the operator presses PF3 on the endowment policy screen, the system shall end the transaction with 'Transaction ended'. Rules: UP2-BR-025.
- **UP2-REQ-F-032** (formatting): When the operator presses CLEAR on the endowment policy screen, the system shall redisplay an empty endowment screen and continue under transaction SSP2. Rules: UP2-BR-025.
- **UP2-REQ-F-033** (business rule): When the operator chooses option '1' with a customer number and policy number, the system shall look up the policy (request '01IEND') and, on success, show its issue date, expiry date, fund name, term, sum assured, life assured, with-profits, managed fund and equities. Rules: UP2-BR-026.
- **UP2-REQ-F-034** (error handling): If the endowment policy inquiry returns a non-zero code, then the system shall show 'No data was returned.' and clear the screen and conversation data. Rules: UP2-BR-027.
- **UP2-REQ-F-035** (business rule): When the operator chooses option '2', the system shall send the customer number, issue and expiry dates, fund name, term, sum assured, life assured, with-profits, managed fund and equities for a new policy (request '01AEND'), with payment 0, broker 0 and a blank broker reference. Rules: UP2-BR-028, UP2-BR-029.
- **UP2-REQ-F-036** (formatting): When adding the endowment policy succeeds, the system shall show the customer number, the newly assigned policy number and the fund name, clear the option field and show 'New Life Policy Inserted'. Rules: UP2-BR-030.
- **UP2-REQ-F-037** (error handling): If adding the endowment policy returns a non-zero code, then the system shall roll back the unit of work and take the add-error path. Rules: UP2-BR-031.
- **UP2-REQ-F-038** (error handling): If adding an endowment policy fails because the customer is not on file (return code 70), then the system shall roll back the unit of work, redisplay the endowment screen and clear the screen and conversation data for the next attempt. Rules: UP2-BR-032.
- **UP2-REQ-F-039** (formatting): If adding an endowment policy fails, then the system shall put the message 'Customer does not exist' (return code 70) or 'Error Adding Life Policy' (any other code) in the message field of the motor policy screen (ERP1FLDO), so the message does not appear on the endowment screen. Rules: UP2-BR-033.
- **UP2-REQ-F-040** (business rule): When the operator chooses option '4', the system shall first show the current policy details (request '01IEND'), wait for the operator to change them and press Enter, then send the changed details for update (request '01UEND') with payment 0, broker 0 and a blank broker reference, whatever values the policy held before. Rules: UP2-BR-034, UP2-BR-029.
- **UP2-REQ-F-041** (error handling): If the first inquiry for option '4' fails, then the system shall show 'No data was returned.'. Rules: UP2-BR-035.
- **UP2-REQ-F-042** (formatting): When the endowment policy update succeeds, the system shall show the customer and policy numbers, clear the option field and show 'Life Policy Updated'. Rules: UP2-BR-036.
- **UP2-REQ-F-043** (error handling): If the endowment policy update returns a non-zero code, then the system shall show 'Error Updating Life Policy' and clear the screen and conversation data, without issuing a rollback. Rules: UP2-BR-035.
- **UP2-REQ-F-044** (error handling): If an inquiry, add, delete or update of an endowment policy fails, then the system shall redisplay the screen with the error message, then clear the screen data and conversation data and wait for the next input under transaction SSP2. Rules: UP2-BR-037.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-023 | Endowment (life) policy menu option dispatch and invalid-option guard | business rule | THE endowment policy screen SHALL treat option '1' as inquire (LGIPOL01), '2' as add (LGAPOL01), '3' as delete (LGDPOL01) and '4' as inquire-then-update (LGIPOL01 then LGUPOL01). | medium | base/src/lgtestp2.cbl:47-61, base/src/lgtestp2.cbl:125-153, base/src/lgtestp2.cbl:218-231, base/src/lgtestp2.cbl:239-266 |
| UP2-BR-024 | Endowment (life) policy menu option dispatch and invalid-option guard | business rule | WHEN the operator presses Enter on the endowment policy screen with an option other than '1', '2', '3' or '4', THE endowment policy screen SHALL call no back-end program, show 'Please enter a valid option' with the cursor on the option field, and wait for the next input under transaction SSP2. | medium | base/src/lgtestp2.cbl:47-61, base/src/lgtestp2.cbl:125-153, base/src/lgtestp2.cbl:218-231, base/src/lgtestp2.cbl:239-266 |
| UP2-BR-025 | Endowment (life) policy menu option dispatch and invalid-option guard | formatting | WHEN the operator presses PF3, THE endowment policy screen SHALL end the transaction with 'Transaction ended'; WHEN the operator presses CLEAR, it SHALL redisplay an empty endowment screen and continue under transaction SSP2. | medium | base/src/lgtestp2.cbl:47-61, base/src/lgtestp2.cbl:125-153, base/src/lgtestp2.cbl:218-231, base/src/lgtestp2.cbl:239-266 |
| UP2-BR-026 | Inquire policy by customer number and policy number | business rule | WHEN the operator chooses option '1' with a customer number and policy number, THE endowment policy screen SHALL look up the policy (request '01IEND') and, on success, show its issue date, expiry date, fund name, term, sum assured, life assured, with-profits, managed fund and equities. | medium | base/src/lgtestp2.cbl:63-88, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-027 | Inquire policy by customer number and policy number | error handling | WHEN the endowment policy inquiry returns a non-zero code, THE endowment policy screen SHALL show 'No data was returned.' and clear the screen and conversation data. | medium | base/src/lgtestp2.cbl:63-88, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-028 | Add endowment policy from terminal | business rule | WHEN the operator chooses option '2', THE endowment policy screen SHALL send the customer number, issue and expiry dates, fund name, term, sum assured, life assured, with-profits, managed fund and equities for a new policy (request '01AEND'), with payment 0, broker 0 and a blank broker reference. | medium | base/src/lgtestp2.cbl:90-123, base/src/lgtestp2.cbl:268-276 |
| UP2-BR-029 | Terminal-entered policies carry no broker and no payment | business rule | WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND), THE system SHALL always send payment 0, broker id 0 and a blank broker reference, whatever values the policy held before. | medium | base/src/lgtestp3.cbl:93-97, base/src/lgtestp3.cbl:183-187, base/src/lgtestp2.cbl:91-95, base/src/lgtestp2.cbl:184-188 |
| UP2-BR-030 | Add endowment policy from terminal | formatting | WHEN adding the endowment policy succeeds, THE endowment policy screen SHALL show the customer number, the newly assigned policy number and the fund name, clear the option field and show 'New Life Policy Inserted'. | medium | base/src/lgtestp2.cbl:90-123, base/src/lgtestp2.cbl:268-276 |
| UP2-BR-031 | Add endowment policy from terminal | error handling | WHEN adding the endowment policy returns a non-zero code, THE endowment policy screen SHALL roll back the unit of work and take the add-error path. | medium | base/src/lgtestp2.cbl:90-123, base/src/lgtestp2.cbl:268-276 |
| UP2-BR-032 | Adding a policy requires an existing customer | error handling | WHEN adding an endowment policy fails because the customer is not on file (return code 70), THE endowment policy screen SHALL roll back the unit of work, redisplay the endowment screen and clear the screen and conversation data for the next attempt. | medium | base/src/lgtestp2.cbl:105-112, base/src/lgtestp2.cbl:268-276, base/src/lgtestp2.cbl:290-300, base/src/ssmap.bms:230 |
| UP2-BR-033 | Adding a policy requires an existing customer | formatting | WHEN adding an endowment policy fails, THE endowment policy screen SHALL put the message 'Customer does not exist' (return code 70) or 'Error Adding Life Policy' (any other code) in the message field of the motor policy screen (ERP1FLDO), so the message does not appear on the endowment screen. | medium | base/src/lgtestp2.cbl:105-112, base/src/lgtestp2.cbl:268-276, base/src/lgtestp2.cbl:290-300, base/src/ssmap.bms:230 |
| UP2-BR-034 | Update endowment policy via inquire-then-update | business rule | WHEN the operator chooses option '4', THE endowment policy screen SHALL first show the current policy details (request '01IEND'), wait for the operator to change them and press Enter, then send the changed details for update (request '01UEND') with payment 0, broker 0 and a blank broker reference. | medium | base/src/lgtestp2.cbl:155-216, base/src/lgtestp2.cbl:278-280, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-035 | Update endowment policy via inquire-then-update | error handling | WHEN the endowment policy update returns a non-zero code, THE endowment policy screen SHALL show 'Error Updating Life Policy' and clear the screen and conversation data, without issuing a rollback; WHEN the first inquiry fails, it SHALL show 'No data was returned.' instead. | medium | base/src/lgtestp2.cbl:155-216, base/src/lgtestp2.cbl:278-280, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-036 | Update endowment policy via inquire-then-update | formatting | WHEN the endowment policy update succeeds, THE endowment policy screen SHALL show the customer and policy numbers, clear the option field and show 'Life Policy Updated'. | medium | base/src/lgtestp2.cbl:155-216, base/src/lgtestp2.cbl:278-280, base/src/lgtestp2.cbl:286-300 |
| UP2-BR-037 | Error path resets screen and conversation context | error handling | WHEN an inquiry, add, delete or update of an endowment policy fails, THE endowment policy screen SHALL redisplay the screen with the error message, then clear the screen data and conversation data and wait for the next input under transaction SSP2. | medium | base/src/lgtestp2.cbl:268-300, base/src/lgtestp2.cbl:239-243 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-085: When a policy is updated from a terminal, its broker id, broker reference and payment are reset to zero/blank. Is that intended, or should the stored values be kept? (Underwriting business owner) On UP2-BR-029.
- DEF-058: Is this intended? The add-failure messages are written to the motor policy map's message field (ERP1FLDO) instead of the endowment map's (ERP2FLDO), so an operator never sees 'Customer does not exist' or 'Error Adding Life Policy' on the endowment screen. It looks like a copy from LGTESTP1; every other error path in this program uses ERP2FLDO. (Subject-matter expert) On UP2-BR-033.
- DEF-063: Is this intended? For the update, the customer number is re-read from the screen but the policy number is not; the policy number left from the inquiry is used, so a policy number the operator changes on the screen is ignored. The update failure path also does not roll back, although add and delete do. (Subject-matter expert) On UP2-BR-036.

### Decision table gaps

- Endowment policy request outcome: No rule says what the endowment screen shows or clears after a successful delete.
- Endowment policy request outcome: No rule gives the error message text or whether a rollback is issued when an endowment delete fails.
