# Feature specification: Customer add, update and menu

**Feature:** UP2-C01 · Unassigned programs · Unassigned programs

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP2-C01)

As a customer service user, I want to add new customers and update existing customer details from the customer screen, so that customer records are created with a system-assigned number and kept current.

Lets customer service staff register new customers and change the details of existing ones from the customer screen; new customers always get their number from the system, never from the user. It must always normalise the postcode to upper case and record the highest customer number issued after every successful add, and it must roll back a failed add so no partial customer is left behind.

**Acceptance scenarios:**

1. **Given** option: 2; return code: 00; assigned customer number: 0000000011, **when** the add-customer request returns code 0, **then** The screen shows customer number 0000000011 and 'New Customer Inserted'. (UP2-C01-AC-01)
2. **Given** option: 2; return code: 90, **when** the add-customer request returns a code greater than 0, **then** The changes are rolled back and 'Error Adding Customer' is shown. (UP2-C01-AC-02)
3. **Given** option: 4; customer number: 0000000123, **when** the user chooses option '4', **then** The details of customer 0000000123 are shown for editing. (UP2-C01-AC-03)
4. **Given** option: 4; lookup return code: 01, **when** the user chooses option '4', **then** 'No data was returned.' is shown. (UP2-C01-AC-04)
5. **Given** update return code: 00, **when** the update returns code 0, **then** 'Customer details updated' is shown. (UP2-C01-AC-05)
6. **Given** update return code: 90, **when** the update returns code 0, **then** 'Error Updating Customer' is shown. (UP2-C01-AC-06)
7. **Given** option: 3; customer number: 0000000123, **when** the user enters an option other than '1' (inquire), '2' (add) or '4' (update), including blank or '3', **then** 'Please enter a valid option' is shown with the cursor on the option field. (UP2-C01-AC-07)
8. **Given** option: (blank), **when** the user enters an option other than '1' (inquire), '2' (add) or '4' (update), including blank or '3', **then** 'Please enter a valid option' is shown with the cursor on the option field. (UP2-C01-AC-08)
9. **Given** key pressed: PF3, **when** the user presses PF3, **then** 'Transaction ended' is shown and the menu ends. (UP2-C01-AC-09)
10. **Given** key pressed: CLEAR, **when** the user presses PF3, **then** An empty customer screen is shown. (UP2-C01-AC-10)
11. **Given** the customer screen with option '2' entered, a customer number field of any value, postcode 'ab1 2cd' and a first name field that contains a null character, **when** the user submits the screen, **then** one add-customer request '01ACUS' is sent to the customer add program (LGACUS01) with customer number 0, postcode 'AB1 2CD' and the null character in the first name replaced by a space; all other entered details are passed unchanged (UP2-C01-AC-11)
12. **Given** the control queue 'GENACNTL' holds the entries '**** GENAPP CNTL', 'LOW CUSTOMER=0000000001' and 'HIGH CUSTOMER=0000000005', **when** a new customer is added successfully and is assigned customer number 0000000006, **then** the queue is locked, the 'HIGH CUSTOMER' entry is rewritten as 'HIGH CUSTOMER=0000000006', the 'LOW CUSTOMER=0000000001' entry is unchanged, no entries are added, and the lock is released afterwards (UP2-C01-AC-12)
13. **Given** the control queue 'GENACNTL' does not exist, or exists without any 'HIGH CUSTOMER' entry, **when** a new customer is added successfully and is assigned customer number 0000000006, **then** three entries are written to 'GENACNTL': '**** GENAPP CNTL', 'LOW CUSTOMER=' and 'HIGH CUSTOMER=', each with customer number 0000000006 (UP2-C01-AC-13)
14. **Given** option '4' was entered for customer 0000000006, the lookup succeeded and the current details are displayed, **when** the user changes the postcode to 'ab1 2cd', leaves a null character in the house name field and presses Enter, **then** one update request '01UCUS' is sent to the customer update program (LGUCUS01) with customer number 0000000006 and every field from the screen, with postcode 'AB1 2CD' and the null character in the house name replaced by a space (UP2-C01-AC-14)

## Requirements

### Functional requirements

- **UP2-REQ-F-001** (business rule): When the user chooses option '2' on the customer screen, the system shall send an add-customer request ('01ACUS') to the customer add program (LGACUS01) with customer number 0 and the entered details, after turning any null characters into spaces and the postcode into upper case. Rules: UP2-BR-001.
- **UP2-REQ-F-002** (formatting): When the add-customer request returns code 0, the system shall update the customer-number control queue, show the assigned customer number, clear the option field and display 'New Customer Inserted'. Rules: UP2-BR-002.
- **UP2-REQ-F-003** (side effect): When a new customer has been added successfully, the system shall lock the control queue 'GENACNTL', find its 'HIGH CUSTOMER' entry, rewrite that entry as 'HIGH CUSTOMER=' followed by the new customer number, leave the 'LOW CUSTOMER=' entry unchanged and then release the lock. Rules: UP2-BR-003.
- **UP2-REQ-F-004** (side effect): If the control queue 'GENACNTL' does not exist or has no 'HIGH CUSTOMER' entry, then the system shall write three entries to it: '**** GENAPP CNTL', 'LOW CUSTOMER=' and 'HIGH CUSTOMER=', each with the new customer number. Rules: UP2-BR-004.
- **UP2-REQ-F-005** (error handling): If the add-customer request returns a code greater than 0, then the system shall roll back the unit of work, display 'Error Adding Customer' and clear the screen data. Rules: UP2-BR-005.
- **UP2-REQ-F-006** (business rule): When the user chooses option '4', the system shall first look up the customer ('01ICUS', LGICUS01) and display the current details. Rules: UP2-BR-006.
- **UP2-REQ-F-007** (business rule): If the customer lookup for option '4' returns a code greater than 0, then the system shall display 'No data was returned.' and stop. Rules: UP2-BR-006.
- **UP2-REQ-F-008** (business rule): When the user changes the displayed customer details and presses Enter, the system shall send an update request ('01UCUS') to the customer update program (LGUCUS01) with the customer number and all fields from the screen, after turning null characters into spaces and the postcode into upper case. Rules: UP2-BR-007.
- **UP2-REQ-F-009** (error handling): When the customer update returns code 0, the system shall display 'Customer details updated'. Rules: UP2-BR-008.
- **UP2-REQ-F-010** (error handling): If the customer update returns a code greater than 0, then the system shall display 'Error Updating Customer' and clear the screen data, without a rollback. Rules: UP2-BR-008.
- **UP2-REQ-F-011** (business rule): If the user enters an option other than '1' (inquire), '2' (add) or '4' (update), including blank or '3', then the system shall call no back-end program, display 'Please enter a valid option', place the cursor on the option field and wait for the next input under transaction 'SSC1'. Rules: UP2-BR-009.
- **UP2-REQ-F-012** (formatting): When the user presses PF3 on the customer screen, the system shall display 'Transaction ended' and end the conversation. Rules: UP2-BR-010.
- **UP2-REQ-F-013** (formatting): When the user presses CLEAR on the customer screen, the system shall redisplay an empty customer screen and continue under 'SSC1'. Rules: UP2-BR-010.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP2-BR-001 | New customer registration with system-assigned number and normalised postcode | business rule | WHEN the user chooses option '2' on the customer screen, THE Customer Menu SHALL send an add-customer request ('01ACUS') to the customer add program (LGACUS01) with customer number 0 and the entered details, after turning any null characters into spaces and the postcode into upper case. | medium | base/src/lgtestc1.cbl:113-146, base/src/lgtestc1.cbl:263-281, base/src/lgcmarea.cpy:11-12 |
| UP2-BR-002 | New customer registration with system-assigned number and normalised postcode | formatting | WHEN the add-customer request returns code 0, THE Customer Menu SHALL update the customer-number control queue, show the assigned customer number, clear the option field and display 'New Customer Inserted'. | medium | base/src/lgtestc1.cbl:113-146, base/src/lgtestc1.cbl:263-281, base/src/lgcmarea.cpy:11-12 |
| UP2-BR-003 | Customer number low/high control record maintenance | side effect | WHEN a new customer has been added successfully, THE Customer Menu SHALL lock the control queue 'GENACNTL', find its 'HIGH CUSTOMER' entry and rewrite that entry as 'HIGH CUSTOMER=' followed by the new customer number, leaving the 'LOW CUSTOMER=' entry unchanged, then release the lock. | medium | base/src/lgtestc1.cbl:21-38, base/src/lgtestc1.cbl:137, base/src/lgtestc1.cbl:283-347 |
| UP2-BR-004 | Customer number low/high control record maintenance | side effect | WHEN the control queue 'GENACNTL' does not exist or has no 'HIGH CUSTOMER' entry, THE Customer Menu SHALL write three entries to it: '**** GENAPP CNTL', 'LOW CUSTOMER=' and 'HIGH CUSTOMER=', each with the new customer number. | medium | base/src/lgtestc1.cbl:21-38, base/src/lgtestc1.cbl:137, base/src/lgtestc1.cbl:283-347 |
| UP2-BR-005 | New customer registration with system-assigned number and normalised postcode | error handling | WHEN the add-customer request returns a code greater than 0, THE Customer Menu SHALL roll back the unit of work, display 'Error Adding Customer' and clear the screen data. | medium | base/src/lgtestc1.cbl:113-146, base/src/lgtestc1.cbl:263-281, base/src/lgcmarea.cpy:11-12 |
| UP2-BR-006 | Customer update is a read-then-write two-step | business rule | WHEN the user chooses option '4', THE Customer Menu SHALL first look up the customer ('01ICUS', LGICUS01) and display the current details; if the lookup returns a code greater than 0 it SHALL display 'No data was returned.' and stop. | medium | base/src/lgtestc1.cbl:148-207, base/src/lgtestc1.cbl:259-281 |
| UP2-BR-007 | Customer update is a read-then-write two-step | business rule | WHEN the user then changes the displayed details and presses Enter, THE Customer Menu SHALL send an update request ('01UCUS') to the customer update program (LGUCUS01) with the customer number and all fields from the screen, after turning null characters into spaces and the postcode into upper case. | medium | base/src/lgtestc1.cbl:148-207, base/src/lgtestc1.cbl:259-281 |
| UP2-BR-008 | Customer update is a read-then-write two-step | error handling | WHEN the update returns code 0, THE Customer Menu SHALL display 'Customer details updated'; WHEN it returns a code greater than 0, it SHALL display 'Error Updating Customer' and clear the screen data, without a rollback. | medium | base/src/lgtestc1.cbl:148-207, base/src/lgtestc1.cbl:259-281 |
| UP2-BR-009 | Customer menu permits only Inquire, Add and Update actions | business rule | WHEN the user enters an option other than '1' (inquire), '2' (add) or '4' (update), including blank or '3', THE Customer Menu SHALL call no back-end program, display 'Please enter a valid option', place the cursor on the option field and wait for the next input under transaction 'SSC1'. | medium | base/src/lgtestc1.cbl:70-81, base/src/lgtestc1.cbl:84-86, base/src/lgtestc1.cbl:113, base/src/lgtestc1.cbl:148 |
| UP2-BR-010 | Customer menu permits only Inquire, Add and Update actions | formatting | WHEN the user presses PF3, THE Customer Menu SHALL display 'Transaction ended' and end the conversation; WHEN the user presses CLEAR, it SHALL redisplay an empty customer screen and continue under 'SSC1'. | medium | base/src/lgtestc1.cbl:70-81, base/src/lgtestc1.cbl:84-86, base/src/lgtestc1.cbl:113, base/src/lgtestc1.cbl:148 |

### Key entities

- LGCMAREA (working storage)

### Needs clarification

- SME-081: Is the recorded low/high customer number range the official range that other processes (such as workload generators) rely on, and should the high value only ever go up? (Application owner) On UP2-BR-004.
- SME-082: New customer registration assigns the customer number automatically and normalises the postcode. Is this rule critical to the business, or costly if it were wrong, so that it must be preserved exactly? (Customer services business owner) On UP2-BR-005.
- DEF-052: Is this intended? When the queue exists but has no 'HIGH CUSTOMER' entry, the header and both LOW and HIGH entries are appended after the existing items, which can leave a second header and LOW entry in the queue. The HIGH entry is also overwritten with whatever number was just assigned, without checking that it is higher than the current one. (Subject-matter expert) On UP2-BR-004.
- DEF-061: Is this intended? The update takes the customer number from the screen after the edit, not the number that was looked up, so a user who changes the customer number field updates a different customer. The task also holds the terminal open (conversationally) while the user edits. (Subject-matter expert) On UP2-BR-008.

### Decision table gaps

- Customer menu option handling: Option '1' (inquire) is accepted as valid, but no rule says what the customer inquiry does or displays.
