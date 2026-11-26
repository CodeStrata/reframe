# Requirements: Validate and look up an account for viewing (OATM-C16)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

Customer Account Self-Service · Online Account and Transaction Management · runs as online · risk medium

## Introduction

Checks the 11-digit account number a user enters on the Account View screen. It then finds the account's linked card and customer, the account itself and the customer's profile. It must never show details for an invalid or unknown number, and every lookup that fails must give a clear message naming which record could not be found or read.

**User story:** As a user, I want the account number I enter to be checked and the account and its customer looked up, so that I see the right account or a clear reason why it could not be shown.

## Requirements

### Requirement 1: OATM-REQ-F-123 (business rule)

#### Acceptance criteria

1. When the account number entered on the Account View screen is '*' or blank, the system shall treat the account number as not supplied. (rules OATM-BR-126)
2. GIVEN Account number: '*' WHEN the account number entered on the Account View screen is '*' or blank THEN Handled exactly like a blank account number (OATM-C16-AC-01; OATM-BR-126)

### Requirement 2: OATM-REQ-F-124 (business rule)

#### Acceptance criteria

1. If no account number is supplied, then the system shall reject the request as an input error without reading any file, set the session account to zero, show 'No input received', and redisplay the account field as '*' in red. (rules OATM-BR-127)
2. GIVEN Account number: blank WHEN no account number is supplied THEN Message 'No input received'; the account field shows '*' in red; no file is read (OATM-C16-AC-02; OATM-BR-127)

### Requirement 3: OATM-REQ-F-125 (business rule)

#### Acceptance criteria

1. If the account number supplied is not all digits (including one shorter than 11 digits) or is all zeros, then the system shall reject it as an input error without reading any file, set the session account to zero, show the account field in red and show 'Account Filter must be a non-zero 11 digit number'. (rules OATM-BR-128)
2. GIVEN Account number: ABC12345678 WHEN the account number supplied is not all digits (including one shorter than 11 digits) or is all zeros THEN Message 'Account Filter must be a non-zero 11 digit number' (OATM-C16-AC-03; OATM-BR-128)
3. GIVEN Account number: 00000000000 WHEN the account number supplied is not all digits (including one shorter than 11 digits) or is all zeros THEN Message 'Account Filter must be a non-zero 11 digit number' (OATM-C16-AC-04; OATM-BR-128)

### Requirement 4: OATM-REQ-F-126 (business rule)

#### Acceptance criteria

1. When the account number is 11 digits and not all zeros, the system shall accept it as the session account and go on to the account lookup. (rules OATM-BR-129)
2. GIVEN Account number: 00000012345 WHEN the account number is 11 digits and not all zeros THEN Accepted; the card cross-reference is read for account 00000012345 (OATM-C16-AC-05; OATM-BR-129)

### Requirement 5: OATM-REQ-F-127 (design note)

#### Acceptance criteria

1. When an account number passes validation, the system shall look the account up in the card cross-reference by account number (CXACAIX) and, when it is found, keep that account's customer number and card number for the rest of the session. (rules OATM-BR-130)
2. GIVEN Account number: 00000012345; Cross-reference entry: customer 000000123, card 4111111111111111 WHEN an account number passes validation on the Account View screen THEN Customer 000000123 and card 4111111111111111 are kept for the session and the account master is read next (OATM-C16-AC-06; OATM-BR-130)

### Requirement 6: OATM-REQ-F-128 (business rule)

#### Acceptance criteria

1. If the account is not in the card cross-reference, then the system shall stop the lookup, treat it as an input error, show the account number in red and show 'Account:<account number> not found in Cross ref file. Resp:<code> Reas:<code>'. (rules OATM-BR-131)
2. GIVEN Account number 00000012345 passes validation but has no entry in the card cross-reference by account WHEN The user submits the Account View screen THEN The lookup stops without reading the account or customer, the request is treated as an input error, the account number is shown in red, and the message 'Account:00000012345 not found in Cross ref file. Resp:<code> Reas:<code>' is shown with the response and reason codes from the failed read (OATM-C16-AC-12; OATM-BR-131)

### Requirement 7: OATM-REQ-F-129 (error handling)

#### Acceptance criteria

1. If reading the card cross-reference fails for any reason other than 'not found', then the system shall stop the lookup, treat it as an input error and show 'File Error: READ on CXACAIX returned RESP <code>,RESP2 <code>'. (rules OATM-BR-132)
2. GIVEN Account number 00000012345 passes validation and reading the card cross-reference fails for a reason other than not found WHEN The user submits the Account View screen THEN The lookup stops, the request is treated as an input error, and the message 'File Error: READ on CXACAIX returned RESP <code>,RESP2 <code>' is shown with the codes from the failed read (OATM-C16-AC-13; OATM-BR-132)

### Requirement 8: OATM-REQ-F-130 (design note)

#### Acceptance criteria

1. When the account is found in the cross-reference, the system shall read the account master (ACCTDAT) by account number and, on success, mark the account as found so that its details are displayed. (rules OATM-BR-133)
2. GIVEN Account number: 00000012345; Account master: record exists WHEN the account is found in the cross-reference THEN The account is marked as found and its status, balances, limits and dates are displayed (OATM-C16-AC-07; OATM-BR-133)

### Requirement 9: OATM-REQ-F-131 (error handling)

#### Acceptance criteria

1. If the account is not in the account master, then the system shall treat it as an input error, show the account number in red and show 'Account:<account number> not found in Acct Master file.Resp:<code> Reas:<code>', and for any other read failure show 'File Error: READ on ACCTDAT returned RESP <code>,RESP2 <code>'. (rules OATM-BR-134)
2. GIVEN Account 00000012345 is found in the card cross-reference but is not in the account master WHEN The user submits the Account View screen THEN The request is treated as an input error, the account number is shown in red and the message 'Account:00000012345 not found in Acct Master file.Resp:<code> Reas:<code>' is shown (OATM-C16-AC-14; OATM-BR-134)
3. GIVEN Account 00000012345 is found in the card cross-reference and reading the account master fails for a reason other than not found WHEN The user submits the Account View screen THEN The message 'File Error: READ on ACCTDAT returned RESP <code>,RESP2 <code>' is shown with the codes from the failed read (OATM-C16-AC-15; OATM-BR-134)

### Requirement 10: OATM-REQ-F-132 (error handling)

#### Acceptance criteria

1. If reading the account master does not succeed, then the system shall still go on to read the customer master, because the stop check after the account read never triggers. (rules OATM-BR-135)
2. GIVEN Account master: no record for 00000012345; Customer master: customer 000000123 exists WHEN reading the account master does not succeed THEN The customer is still read and shown, the account fields are shown from an empty record, and the account 'not found' message is still shown (OATM-C16-AC-08; OATM-BR-135)

### Requirement 11: OATM-REQ-F-133 (design note)

#### Acceptance criteria

1. The system shall read the customer master (CUSTDAT) using the customer number taken from the card cross-reference and, on success, mark the customer as found so that the customer details are displayed. (rules OATM-BR-136)
2. GIVEN Cross-reference customer: 000000123; Customer master: record exists WHEN account view runs THEN The customer's name, address, phones, SSN and FICO score are displayed (OATM-C16-AC-09; OATM-BR-136)

### Requirement 12: OATM-REQ-F-134 (error handling)

#### Acceptance criteria

1. If the customer is not in the customer master, then the system shall treat it as an input error and show 'CustId:<customer number> not found in customer master.Resp: <code> REAS:<code>', unless an earlier message is already set. (rules OATM-BR-137)
2. GIVEN Account 00000012345 is found in the cross-reference and the account master, its cross-reference gives customer number 000000099, no message has been set yet, and that customer is not in the customer master WHEN The user submits the Account View screen THEN The request is treated as an input error and the message 'CustId:000000099 not found in customer master.Resp: <code> REAS:<code>' is shown (OATM-C16-AC-16; OATM-BR-137)
3. GIVEN An earlier lookup step has already set a message, and the customer is then not found in the customer master WHEN The user submits the Account View screen THEN The earlier message is kept and the customer-not-found message is not shown (OATM-C16-AC-17; OATM-BR-137)

### Requirement 13: OATM-REQ-F-135 (error handling)

#### Acceptance criteria

1. If reading the customer master fails for any reason other than 'not found', then the system shall treat it as an input error and show 'File Error: READ on CUSTDAT returned RESP <code>,RESP2 <code>', replacing any earlier message. (rules OATM-BR-138)
2. GIVEN An earlier message is already set, and reading the customer master fails for a reason other than not found WHEN The user submits the Account View screen THEN The request is treated as an input error and the earlier message is replaced by 'File Error: READ on CUSTDAT returned RESP <code>,RESP2 <code>' (OATM-C16-AC-18; OATM-BR-138)

### Requirement 14: OATM-REQ-F-136 (business rule)

#### Acceptance criteria

1. While the program context is re-entry (1), when PF3 was not pressed, the system shall read and validate the entered account number, redisplay the screen with the error on an input error, and otherwise look up the card cross-reference, account master and customer master in turn (stopping at the first not found) and display the screen. (rules OATM-BR-139)
2. GIVEN program context: 1; account number: 00000000000 WHEN PF3 was not pressed and the program context is re-entry (1) THEN Screen redisplayed with 'Account number must be a non zero 11 digit number' (OATM-C16-AC-10; OATM-BR-139)
3. GIVEN program context: 1; account number: 00000012345; cross-reference, account, customer: all found WHEN PF3 was not pressed and the program context is re-entry (1) THEN Screen shows account and customer details (OATM-C16-AC-11; OATM-BR-139)
