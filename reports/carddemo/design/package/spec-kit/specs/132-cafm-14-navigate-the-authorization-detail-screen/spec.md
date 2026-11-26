# Feature specification: Navigate the authorization detail screen

**Feature:** CAFM-C14 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C14)

As a card operations user, I want to use function keys on the authorization detail screen to move to the next authorization or return to the list, so that I can work through an account's pending authorizations.

Lets a card operations user move around the authorization detail screen: step to the next pending authorization of the same account, go back to the pending authorization list, or refresh the current one. It must stay within the same account when stepping forward and keep the current selection when there is nothing further. It must never show details from a failed read.

**Acceptance scenarios:**

1. **Given** transaction CPVD started directly: no commarea, **when** the detail program starts with no data passed from a calling screen, **then** Control passes to COPAUS0C. (CAFM-C14-AC-01)
2. **Given** key: PF3, **when** the user presses PF3 on the detail screen, **then** The pending authorization summary screen is shown. (CAFM-C14-AC-02)
3. **Given** account: 00000012345; selected authorization: K1; authorizations under account: K1, K2, **when** the user presses PF8, **then** K2 becomes the selected authorization and its details are shown. (CAFM-C14-AC-03)
4. **Given** key: PF8, **when** the user presses PF8 on the detail screen, **then** The next authorization of the account is displayed. (CAFM-C14-AC-04)
5. **Given** selected authorization: K2 (last); key: PF8, **when** the user presses PF8 and there is no further authorization for the account, **then** 'Already at the last Authorization...' is shown and K2 stays selected. (CAFM-C14-AC-05)
6. **Given** key pressed: PF7; selected authorization key: K1, **when** the user presses a key other than Enter, PF3, PF5 or PF8, **then** Authorization K1 is shown again with 'Invalid key pressed. Please see below...'. (CAFM-C14-AC-06)
7. **Given** key: PF7, **when** the user presses any key other than Enter, PF3, PF5 or PF8, **then** Details are redisplayed with 'Invalid key pressed. Please see below...'. (CAFM-C14-AC-07)
8. **Given** an authorization is selected on the detail screen and reading the next authorization of the account returns database status 'AJ' (not success, not found or end of data), **when** the user presses PF8, **then** an error is flagged, the message ' System error while reading next Auth: Code:' followed by AJ is shown, and the authorization detail fields are not filled in (CAFM-C14-AC-08)

## Requirements

### Functional requirements

- **CAFM-REQ-F-127** (design note): When the detail program starts with no data passed from a calling screen, the system shall transfer control to the authorization summary program (COPAUS0C). Rules: CAFM-BR-135.
- **CAFM-REQ-F-128** (business rule): When the user presses PF3 on the detail screen, the system shall return to the authorization summary list (COPAUS0C). Rules: CAFM-BR-136.
- **CAFM-REQ-F-129** (business rule): When the user presses PF8 on the detail screen, the system shall re-read the selected authorization of the account, fetch the next authorization under the same account, make it the selected authorization and display its details. Rules: CAFM-BR-137, CAFM-BR-138.
- **CAFM-REQ-F-130** (business rule): When the user presses PF8 and there is no further authorization for the account, the system shall keep the current selection and show 'Already at the last Authorization...' without erasing the screen. Rules: CAFM-BR-139.
- **CAFM-REQ-F-131** (error handling): If reading the next authorization fails with any database status other than success, not found or end of data, then the system shall flag an error, show ' System error while reading next Auth: Code:' followed by the status code, and not fill in the authorization details. Rules: CAFM-BR-140.
- **CAFM-REQ-F-132** (business rule): When the user presses any key other than Enter, PF3, PF5 or PF8, the system shall re-read and redisplay the selected authorization as for Enter, with the message 'Invalid key pressed. Please see below...'. Rules: CAFM-BR-141, CAFM-BR-142.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-135 | Authorization detail screen key handling and navigation | design note | WHEN the detail program starts with no data passed from a calling screen, THE Authorization Detail View SHALL transfer control to the authorization summary program (COPAUS0C). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-136 | Authorization detail screen key handling and navigation | business rule | WHEN the user presses PF3 on the detail screen, THE Authorization Detail View SHALL return to the authorization summary list (COPAUS0C). | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-137 | Show next authorization | business rule | WHEN the user presses PF8, THE Authorization Detail View SHALL re-read the selected authorization of the account, fetch the next authorization under the same account, make it the selected authorization and display its details. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:268-289, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:493-518, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:380-395 |
| CAFM-BR-138 | Route operator requests on re-entry | business rule | WHEN the user presses PF8 on the detail screen, THE Authorization Detail View SHALL show the next authorization of the same account. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |
| CAFM-BR-139 | Show next authorization | business rule | WHEN the user presses PF8 and there is no further authorization for the account, THE Authorization Detail View SHALL keep the current selection and show 'Already at the last Authorization...' without erasing the screen. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:268-289, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:493-518, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:380-395 |
| CAFM-BR-140 | Read next authorization detail | error handling | WHEN reading the next authorization fails with any database status other than success, not found or end of data, THE Authorization Detail View SHALL flag an error, show ' System error while reading next Auth: Code:' followed by the status code, and not fill in the authorization details. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:268-289, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:493-518, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:380-395 |
| CAFM-BR-141 | Authorization detail can only be shown for a numeric account and a selected authorization | business rule | WHEN the user presses a key other than Enter, PF3, PF5 or PF8, THE Authorization Detail View SHALL reload and show the selected authorization as for Enter, with the message 'Invalid key pressed. Please see below...'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:165-197, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:208-228, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:291-294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:431-491 |
| CAFM-BR-142 | Warn on invalid key | business rule | WHEN the user presses any key other than Enter, PF3, PF5 or PF8, THE Authorization Detail View SHALL re-read and redisplay the selected authorization with the message 'Invalid key pressed. Please see below...'. | high | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:157-206, app/cpy/CSMSG01Y.cpy:20-21, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:360-370 |

### Key entities

- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSMSG02Y (working storage)

### Needs clarification

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-139, CAFM-BR-140, CAFM-BR-138, CAFM-BR-142.
- DEF-026: Is this intended? When the summary or the selected detail is not found ('GE'/'GB'), the error flag stays off, so the screen is filled from whatever detail record is in memory, with no 'not found' message; and on a read error the screen is sent once inside the read routine and again by the main flow. (Subject-matter expert) On CAFM-BR-141.
- DEF-063: Is this intended? When a database read fails, the error paragraph sends the detail screen itself and then the main routine sends it a second time, so the screen is sent twice in one task. (Subject-matter expert) On CAFM-BR-139, CAFM-BR-140.

### Decision table gaps

None.
