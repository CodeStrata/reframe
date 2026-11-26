# Requirements: Navigate the authorization detail screen (CAFM-C14)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Unclassified · Card Authorization and Fraud Management · runs as online · risk medium

## Introduction

Lets a card operations user move around the authorization detail screen: step to the next pending authorization of the same account, go back to the pending authorization list, or refresh the current one. It must stay within the same account when stepping forward and keep the current selection when there is nothing further. It must never show details from a failed read.

**User story:** As a card operations user, I want to use function keys on the authorization detail screen to move to the next authorization or return to the list, so that I can work through an account's pending authorizations.

## Requirements

### Requirement 1: CAFM-REQ-F-127 (design note)

#### Acceptance criteria

1. When the detail program starts with no data passed from a calling screen, the system shall transfer control to the authorization summary program (COPAUS0C). (rules CAFM-BR-135)
2. GIVEN transaction CPVD started directly: no commarea WHEN the detail program starts with no data passed from a calling screen THEN Control passes to COPAUS0C. (CAFM-C14-AC-01; CAFM-BR-135)

### Requirement 2: CAFM-REQ-F-128 (business rule)

#### Acceptance criteria

1. When the user presses PF3 on the detail screen, the system shall return to the authorization summary list (COPAUS0C). (rules CAFM-BR-136)
2. GIVEN key: PF3 WHEN the user presses PF3 on the detail screen THEN The pending authorization summary screen is shown. (CAFM-C14-AC-02; CAFM-BR-136)

### Requirement 3: CAFM-REQ-F-129 (business rule)

#### Acceptance criteria

1. When the user presses PF8 on the detail screen, the system shall re-read the selected authorization of the account, fetch the next authorization under the same account, make it the selected authorization and display its details. (rules CAFM-BR-137, CAFM-BR-138)
2. GIVEN account: 00000012345; selected authorization: K1; authorizations under account: K1, K2 WHEN the user presses PF8 THEN K2 becomes the selected authorization and its details are shown. (CAFM-C14-AC-03; CAFM-BR-137)
3. GIVEN key: PF8 WHEN the user presses PF8 on the detail screen THEN The next authorization of the account is displayed. (CAFM-C14-AC-04; CAFM-BR-138)

### Requirement 4: CAFM-REQ-F-130 (business rule)

#### Acceptance criteria

1. When the user presses PF8 and there is no further authorization for the account, the system shall keep the current selection and show 'Already at the last Authorization...' without erasing the screen. (rules CAFM-BR-139)
2. GIVEN selected authorization: K2 (last); key: PF8 WHEN the user presses PF8 and there is no further authorization for the account THEN 'Already at the last Authorization...' is shown and K2 stays selected. (CAFM-C14-AC-05; CAFM-BR-139)

### Requirement 5: CAFM-REQ-F-131 (error handling)

#### Acceptance criteria

1. If reading the next authorization fails with any database status other than success, not found or end of data, then the system shall flag an error, show ' System error while reading next Auth: Code:' followed by the status code, and not fill in the authorization details. (rules CAFM-BR-140)
2. GIVEN an authorization is selected on the detail screen and reading the next authorization of the account returns database status 'AJ' (not success, not found or end of data) WHEN the user presses PF8 THEN an error is flagged, the message ' System error while reading next Auth: Code:' followed by AJ is shown, and the authorization detail fields are not filled in (CAFM-C14-AC-08; CAFM-BR-140)

### Requirement 6: CAFM-REQ-F-132 (business rule)

#### Acceptance criteria

1. When the user presses any key other than Enter, PF3, PF5 or PF8, the system shall re-read and redisplay the selected authorization as for Enter, with the message 'Invalid key pressed. Please see below...'. (rules CAFM-BR-141, CAFM-BR-142)
2. GIVEN key pressed: PF7; selected authorization key: K1 WHEN the user presses a key other than Enter, PF3, PF5 or PF8 THEN Authorization K1 is shown again with 'Invalid key pressed. Please see below...'. (CAFM-C14-AC-06; CAFM-BR-141)
3. GIVEN key: PF7 WHEN the user presses any key other than Enter, PF3, PF5 or PF8 THEN Details are redisplayed with 'Invalid key pressed. Please see below...'. (CAFM-C14-AC-07; CAFM-BR-142)
