# Feature specification: House policy add, delete and update

**Feature:** UP2-C04 · Unassigned programs · Unassigned programs

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP2-C04)

As a policy administrator, I want to add, delete and update house policies from the house policy screen, so that customers' property cover is recorded correctly.

Lets policy administrators add, delete and update a customer's house policy: property type, bedrooms, value, house name, number and postcode. Policies entered here always carry payment 0 and no broker, replacing whatever was stored before, and a failed add or delete must be rolled back. In the legacy screen a failed add resets the screen without showing 'Customer does not exist' or 'Error Adding House Policy'; the team must decide whether to keep that.

**Acceptance scenarios:**

1. **Given** Customer number: 0000000001; Property type: DETACHED; Bedrooms: 003; Value: 00250000; Option: 2, **when** option '2' is entered on the house policy screen, **then** A house policy is added for customer 0000000001 (UP2-C04-AC-01)
2. **Given** Request: 01UHOU; Stored broker id: 1234, **when** a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND), **then** The update is sent with broker id 0, payment 0 and a blank broker reference (UP2-C04-AC-02)
3. **Given** Request: 01AEND, **when** a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND), **then** The new endowment policy is sent with payment 0, broker id 0 and a blank broker reference (UP2-C04-AC-03)
4. **Given** Option: 2; Return code: 00, **when** the house policy add succeeds, **then** The assigned policy number and 'New House Policy Inserted' are shown (UP2-C04-AC-04)
5. **Given** Customer number: 0000000999; Return code: 70, **when** the house policy add returns a non-zero code, **then** The add is rolled back; the house screen is redisplayed without the 'Customer does not exist' message (UP2-C04-AC-05)
6. **Given** Customer number: 0000000001; Policy number: 0000000002; Option: 3; Return code: 00, **when** option '3' is entered on the house policy screen (transaction SSP3), **then** 'House Policy Deleted' is shown with the policy details blank (UP2-C04-AC-06)
7. **Given** Option: 3; Return code: 81, **when** the house policy delete returns a non-zero code, **then** The delete is rolled back and 'Error Deleting House Policy' is shown (UP2-C04-AC-07)
8. **Given** Policy number: 0000000002; Value: 00250000 edited to 00275000; Option: 4, **when** option '4' is entered on the house policy screen, **then** The update is sent with value 00275000 (UP2-C04-AC-08)
9. **Given** Return code: 00, **when** the house policy update succeeds, **then** 'House Policy Updated' is shown (UP2-C04-AC-09)
10. **Given** Return code: 02, **when** the house policy update succeeds, **then** 'Error Updating House Policy' is shown (UP2-C04-AC-10)

## Requirements

### Functional requirements

- **UP2-REQ-F-045** (business rule): When option '2' is entered on the house policy screen, the system shall add a house policy (request 01AHOU to LGAPOL01) from the entered customer number, dates, property type, bedrooms, value, house name, house number and postcode, with payment 0, broker id 0 and a blank broker reference. Rules: UP2-BR-038, UP2-BR-029.
- **UP2-REQ-F-046** (formatting): When the house policy add succeeds, the system shall show the customer number, the newly assigned policy number and 'New House Policy Inserted', and clear the option. Rules: UP2-BR-039.
- **UP2-REQ-F-047** (error handling): If the house policy add returns a non-zero code, then the system shall roll back the unit of work and reset the screen, without the intended message 'Customer does not exist' (code 70) or 'Error Adding House Policy' being shown on the house screen. Rules: UP2-BR-040.
- **UP2-REQ-F-048** (business rule): When option '3' is entered on the house policy screen (transaction SSP3), the system shall delete the house policy (request 01DHOU to LGDPOL01) and on success blank the dates and property details, clear the option and show 'House Policy Deleted'. Rules: UP2-BR-041.
- **UP2-REQ-F-049** (error handling): If the house policy delete returns a non-zero code, then the system shall roll back the unit of work, show 'Error Deleting House Policy' and reset the screen and request data. Rules: UP2-BR-042.
- **UP2-REQ-F-050** (business rule): When option '4' is entered on the house policy screen, the system shall first display the current house policy (request 01IHOU), then send the edited values as an update (request 01UHOU to LGUPOL01) with payment 0, broker id 0 and a blank broker reference, whatever values the policy held before. Rules: UP2-BR-043, UP2-BR-029.
- **UP2-REQ-F-051** (business rule): If the current house policy cannot be read for option '4', then the system shall show 'No data was returned.'. Rules: UP2-BR-043.
- **UP2-REQ-F-052** (error handling): When the house policy update succeeds, the system shall show 'House Policy Updated' and clear the option. Rules: UP2-BR-044.
- **UP2-REQ-F-053** (error handling): If the house policy update returns a non-zero code, then the system shall show 'Error Updating House Policy' and reset the screen, without a rollback. Rules: UP2-BR-044.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-038 | Add house policy from terminal | business rule | WHEN option '2' is entered on the house policy screen, THE system SHALL add a house policy (request 01AHOU to LGAPOL01) from the entered customer number, dates, property type, bedrooms, value, house name, house number and postcode. | medium | base/src/lgtestp3.cbl:92-123, base/src/lgtestp3.cbl:267-275, base/src/lgtestp3.cbl:289-293 |
| UP2-BR-029 | Terminal-entered policies carry no broker and no payment | business rule | WHEN a house or endowment policy is added or updated from the terminal screens (requests 01AHOU, 01UHOU, 01AEND, 01UEND), THE system SHALL always send payment 0, broker id 0 and a blank broker reference, whatever values the policy held before. | medium | base/src/lgtestp3.cbl:93-97, base/src/lgtestp3.cbl:183-187, base/src/lgtestp2.cbl:91-95, base/src/lgtestp2.cbl:184-188 |
| UP2-BR-039 | Add house policy from terminal | formatting | WHEN the house policy add succeeds, THE screen SHALL show the customer number, the newly assigned policy number and 'New House Policy Inserted', and clear the option. | medium | base/src/lgtestp3.cbl:92-123, base/src/lgtestp3.cbl:267-275, base/src/lgtestp3.cbl:289-293 |
| UP2-BR-040 | Add house policy from terminal | error handling | WHEN the house policy add returns a non-zero code, THE system SHALL roll back the unit of work and reset the screen; the intended message 'Customer does not exist' (code 70) or 'Error Adding House Policy' is not shown on the house screen. | medium | base/src/lgtestp3.cbl:92-123, base/src/lgtestp3.cbl:267-275, base/src/lgtestp3.cbl:289-293 |
| UP2-BR-041 | Delete policy with rollback on failure | business rule | WHEN option '3' is entered on the house policy screen (transaction SSP3), THE system SHALL delete the house policy (request 01DHOU to LGDPOL01) and on success blank the dates and property details, clear the option and show 'House Policy Deleted'. | medium | base/src/lgtestp3.cbl:125-153, base/src/lgtestp3.cbl:281-299 |
| UP2-BR-042 | Delete policy with rollback on failure | error handling | WHEN the house policy delete returns a non-zero code, THE system SHALL roll back the unit of work, show 'Error Deleting House Policy' and reset the screen and request data. | medium | base/src/lgtestp3.cbl:125-153, base/src/lgtestp3.cbl:281-299 |
| UP2-BR-043 | Update house policy via inquire-then-update | business rule | WHEN option '4' is entered on the house policy screen, THE system SHALL first display the current house policy (request 01IHOU), showing 'No data was returned.' if it cannot be read, then send the edited values as an update (request 01UHOU to LGUPOL01). | medium | base/src/lgtestp3.cbl:155-214, base/src/lgtestp3.cbl:277-299 |
| UP2-BR-044 | Update house policy via inquire-then-update | error handling | WHEN the house policy update succeeds, THE screen SHALL show 'House Policy Updated' and clear the option; WHEN it returns a non-zero code, it SHALL show 'Error Updating House Policy' and reset the screen, without a rollback. | medium | base/src/lgtestp3.cbl:155-214, base/src/lgtestp3.cbl:277-299 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-085: When a policy is updated from a terminal, its broker id, broker reference and payment are reset to zero/blank. Is that intended, or should the stored values be kept? (Underwriting business owner) On UP2-BR-029.
- DEF-064: Is this intended? The house add-error messages ('Customer does not exist', 'Error Adding House Policy') are moved to the motor screen's message field (ERP1FLDO) instead of the house screen's (ERP3FLDO), so the user sees no reason for the failed add. (Subject-matter expert) On UP2-BR-040.

### Decision table gaps

- House policy menu option handling: No rule says what a house policy inquiry (option '1') requests or displays.
- House policy menu option handling: No rule says how the house policy screen handles an invalid or blank option, or PF3 and CLEAR.
