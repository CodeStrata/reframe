# Requirements: Customer add, update and menu (UP2-C01)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unassigned programs · Unassigned programs · runs as online and scheduled job · risk medium

## Introduction

Lets customer service staff register new customers and change the details of existing ones from the customer screen; new customers always get their number from the system, never from the user. It must always normalise the postcode to upper case and record the highest customer number issued after every successful add, and it must roll back a failed add so no partial customer is left behind.

**User story:** As a customer service user, I want to add new customers and update existing customer details from the customer screen, so that customer records are created with a system-assigned number and kept current.

## Requirements

### Requirement 1: UP2-REQ-F-001 (business rule)

#### Acceptance criteria

1. When the user chooses option '2' on the customer screen, the system shall send an add-customer request ('01ACUS') to the customer add program (LGACUS01) with customer number 0 and the entered details, after turning any null characters into spaces and the postcode into upper case. (rules UP2-BR-001)
2. GIVEN the customer screen with option '2' entered, a customer number field of any value, postcode 'ab1 2cd' and a first name field that contains a null character WHEN the user submits the screen THEN one add-customer request '01ACUS' is sent to the customer add program (LGACUS01) with customer number 0, postcode 'AB1 2CD' and the null character in the first name replaced by a space; all other entered details are passed unchanged (UP2-C01-AC-11; UP2-BR-001)

### Requirement 2: UP2-REQ-F-002 (formatting)

#### Acceptance criteria

1. When the add-customer request returns code 0, the system shall update the customer-number control queue, show the assigned customer number, clear the option field and display 'New Customer Inserted'. (rules UP2-BR-002)
2. GIVEN option: 2; return code: 00; assigned customer number: 0000000011 WHEN the add-customer request returns code 0 THEN The screen shows customer number 0000000011 and 'New Customer Inserted'. (UP2-C01-AC-01; UP2-BR-002)

### Requirement 3: UP2-REQ-F-003 (side effect)

#### Acceptance criteria

1. When a new customer has been added successfully, the system shall lock the control queue 'GENACNTL', find its 'HIGH CUSTOMER' entry, rewrite that entry as 'HIGH CUSTOMER=' followed by the new customer number, leave the 'LOW CUSTOMER=' entry unchanged and then release the lock. (rules UP2-BR-003)
2. GIVEN the control queue 'GENACNTL' holds the entries '**** GENAPP CNTL', 'LOW CUSTOMER=0000000001' and 'HIGH CUSTOMER=0000000005' WHEN a new customer is added successfully and is assigned customer number 0000000006 THEN the queue is locked, the 'HIGH CUSTOMER' entry is rewritten as 'HIGH CUSTOMER=0000000006', the 'LOW CUSTOMER=0000000001' entry is unchanged, no entries are added, and the lock is released afterwards (UP2-C01-AC-12; UP2-BR-003)

### Requirement 4: UP2-REQ-F-004 (side effect)

#### Acceptance criteria

1. If the control queue 'GENACNTL' does not exist or has no 'HIGH CUSTOMER' entry, then the system shall write three entries to it: '**** GENAPP CNTL', 'LOW CUSTOMER=' and 'HIGH CUSTOMER=', each with the new customer number. (rules UP2-BR-004)
2. GIVEN the control queue 'GENACNTL' does not exist, or exists without any 'HIGH CUSTOMER' entry WHEN a new customer is added successfully and is assigned customer number 0000000006 THEN three entries are written to 'GENACNTL': '**** GENAPP CNTL', 'LOW CUSTOMER=' and 'HIGH CUSTOMER=', each with customer number 0000000006 (UP2-C01-AC-13; UP2-BR-004)

### Requirement 5: UP2-REQ-F-005 (error handling)

#### Acceptance criteria

1. If the add-customer request returns a code greater than 0, then the system shall roll back the unit of work, display 'Error Adding Customer' and clear the screen data. (rules UP2-BR-005)
2. GIVEN option: 2; return code: 90 WHEN the add-customer request returns a code greater than 0 THEN The changes are rolled back and 'Error Adding Customer' is shown. (UP2-C01-AC-02; UP2-BR-005)

### Requirement 6: UP2-REQ-F-006 (business rule)

#### Acceptance criteria

1. When the user chooses option '4', the system shall first look up the customer ('01ICUS', LGICUS01) and display the current details. (rules UP2-BR-006)
2. GIVEN option: 4; customer number: 0000000123 WHEN the user chooses option '4' THEN The details of customer 0000000123 are shown for editing. (UP2-C01-AC-03; UP2-BR-006)
3. GIVEN option: 4; lookup return code: 01 WHEN the user chooses option '4' THEN 'No data was returned.' is shown. (UP2-C01-AC-04; UP2-BR-006)

### Requirement 7: UP2-REQ-F-007 (business rule)

#### Acceptance criteria

1. If the customer lookup for option '4' returns a code greater than 0, then the system shall display 'No data was returned.' and stop. (rules UP2-BR-006)
2. GIVEN option: 4; customer number: 0000000123 WHEN the user chooses option '4' THEN The details of customer 0000000123 are shown for editing. (UP2-C01-AC-03; UP2-BR-006)
3. GIVEN option: 4; lookup return code: 01 WHEN the user chooses option '4' THEN 'No data was returned.' is shown. (UP2-C01-AC-04; UP2-BR-006)

### Requirement 8: UP2-REQ-F-008 (business rule)

#### Acceptance criteria

1. When the user changes the displayed customer details and presses Enter, the system shall send an update request ('01UCUS') to the customer update program (LGUCUS01) with the customer number and all fields from the screen, after turning null characters into spaces and the postcode into upper case. (rules UP2-BR-007)
2. GIVEN option '4' was entered for customer 0000000006, the lookup succeeded and the current details are displayed WHEN the user changes the postcode to 'ab1 2cd', leaves a null character in the house name field and presses Enter THEN one update request '01UCUS' is sent to the customer update program (LGUCUS01) with customer number 0000000006 and every field from the screen, with postcode 'AB1 2CD' and the null character in the house name replaced by a space (UP2-C01-AC-14; UP2-BR-007)

### Requirement 9: UP2-REQ-F-009 (error handling)

#### Acceptance criteria

1. When the customer update returns code 0, the system shall display 'Customer details updated'. (rules UP2-BR-008)
2. GIVEN update return code: 00 WHEN the update returns code 0 THEN 'Customer details updated' is shown. (UP2-C01-AC-05; UP2-BR-008)
3. GIVEN update return code: 90 WHEN the update returns code 0 THEN 'Error Updating Customer' is shown. (UP2-C01-AC-06; UP2-BR-008)

### Requirement 10: UP2-REQ-F-010 (error handling)

#### Acceptance criteria

1. If the customer update returns a code greater than 0, then the system shall display 'Error Updating Customer' and clear the screen data, without a rollback. (rules UP2-BR-008)
2. GIVEN update return code: 00 WHEN the update returns code 0 THEN 'Customer details updated' is shown. (UP2-C01-AC-05; UP2-BR-008)
3. GIVEN update return code: 90 WHEN the update returns code 0 THEN 'Error Updating Customer' is shown. (UP2-C01-AC-06; UP2-BR-008)

### Requirement 11: UP2-REQ-F-011 (business rule)

#### Acceptance criteria

1. If the user enters an option other than '1' (inquire), '2' (add) or '4' (update), including blank or '3', then the system shall call no back-end program, display 'Please enter a valid option', place the cursor on the option field and wait for the next input under transaction 'SSC1'. (rules UP2-BR-009)
2. GIVEN option: 3; customer number: 0000000123 WHEN the user enters an option other than '1' (inquire), '2' (add) or '4' (update), including blank or '3' THEN 'Please enter a valid option' is shown with the cursor on the option field. (UP2-C01-AC-07; UP2-BR-009)
3. GIVEN option: (blank) WHEN the user enters an option other than '1' (inquire), '2' (add) or '4' (update), including blank or '3' THEN 'Please enter a valid option' is shown with the cursor on the option field. (UP2-C01-AC-08; UP2-BR-009)

### Requirement 12: UP2-REQ-F-012 (formatting)

#### Acceptance criteria

1. When the user presses PF3 on the customer screen, the system shall display 'Transaction ended' and end the conversation. (rules UP2-BR-010)
2. GIVEN key pressed: PF3 WHEN the user presses PF3 THEN 'Transaction ended' is shown and the menu ends. (UP2-C01-AC-09; UP2-BR-010)
3. GIVEN key pressed: CLEAR WHEN the user presses PF3 THEN An empty customer screen is shown. (UP2-C01-AC-10; UP2-BR-010)

### Requirement 13: UP2-REQ-F-013 (formatting)

#### Acceptance criteria

1. When the user presses CLEAR on the customer screen, the system shall redisplay an empty customer screen and continue under 'SSC1'. (rules UP2-BR-010)
2. GIVEN key pressed: PF3 WHEN the user presses PF3 THEN 'Transaction ended' is shown and the menu ends. (UP2-C01-AC-09; UP2-BR-010)
3. GIVEN key pressed: CLEAR WHEN the user presses PF3 THEN An empty customer screen is shown. (UP2-C01-AC-10; UP2-BR-010)
