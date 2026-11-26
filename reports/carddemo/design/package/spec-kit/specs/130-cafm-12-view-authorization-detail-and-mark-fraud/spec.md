# Feature specification: View authorization detail and mark fraud

**Feature:** CAFM-C12 · Card Authorization and Fraud Management · Unclassified

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (CAFM-C12)

As a fraud analyst, I want to see an authorization's details with its decline reason and toggle its fraud mark, so that suspected fraud can be reported or withdrawn.

The Authorization details screen for fraud analysts. It shows a selected authorization with its response ('A' in green for '00', otherwise 'D' in red) and its reason as code and description. With PF5 the analyst reports the authorization as fraud or withdraws a fraud report. A toggle must always act on a freshly re-read record: 'F' becomes 'R' (remove fraud) and anything else becomes 'F' (report fraud), and the record goes to fraud processing with its account and customer number.

**Acceptance scenarios:**

1. **Given** response code: 00, **when** the authorization detail screen shows an authorization, **then** 'A' shown in green. (CAFM-C12-AC-01)
2. **Given** response code: 05, **when** the authorization detail screen shows an authorization, **then** 'D' shown in red. (CAFM-C12-AC-02)
3. **Given** fraud flag: F, **when** the user presses PF5 on the selected authorization, **then** Flag becomes 'R' and the fraud processor is asked to remove the fraud report. (CAFM-C12-AC-03)
4. **Given** fraud flag: blank, **when** the user presses PF5 on the selected authorization, **then** Flag becomes 'F' and the fraud processor is asked to report fraud. (CAFM-C12-AC-04)
5. **Given** fraud flag: R, **when** the user presses PF5 on the selected authorization, **then** Flag becomes 'F' and the fraud processor is asked to report fraud. (CAFM-C12-AC-05)
6. **Given** One selected authorization with reason code '3100', which is in the decline reason table as 'INVALID CARD', and another with reason code '7777', which is not in the table, **when** Each is shown on the Authorization details screen, **then** The first shows reason '3100-INVALID CARD' and the second shows reason '9999-ERROR' (CAFM-C12-AC-06)

## Requirements

### Functional requirements

- **CAFM-REQ-F-112** (formatting): When authorization details are being populated, the system shall show the reason as '<code>-<description>' from the decline reason table, or as '9999-ERROR' when the code is not in the table. Rules: CAFM-BR-118.
- **CAFM-REQ-F-113** (formatting): When the authorization detail screen shows an authorization, the system shall show response 'A' in green when the response code is '00', otherwise 'D' in red. Rules: CAFM-BR-119.
- **CAFM-REQ-F-114** (business rule): When the user presses PF5 on the selected authorization, the system shall re-read the authorization and, if its fraud flag is 'F', set it to 'R' with a remove-fraud action 'R', otherwise set it to 'F' with a report-fraud action 'F', and pass the record with account and customer number to the fraud processor (COPAUS2C). Rules: CAFM-BR-120.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-118 | Look up decline reason description | formatting | WHEN authorization details are being populated, THE Authorization Detail View SHALL show the reason as '<code>-<description>' from the decline reason table, or as '9999-ERROR' when the code is not in the table | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:319-328, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:319-328 |
| CAFM-BR-119 | Classify authorization as approved or declined | formatting | WHEN the authorization detail screen shows an authorization, THE authorization detail screen SHALL show response 'A' in green when the response code is '00', otherwise 'D' in red. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:311-317 |
| CAFM-BR-120 | Toggle authorization fraud mark | business rule | WHEN the user presses PF5 on the selected authorization, THE authorization detail screen SHALL re-read the authorization and, if its fraud flag is 'F', set it to 'R' with a remove-fraud action ('R'), otherwise set it to 'F' with a report-fraud action ('F'), and pass the record with account and customer number to the fraud processor (COPAUS2C). | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-252, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:93-104, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-52 |

### Key entities

- CIPAUDTY (working storage)
- CIPAUSMY (working storage)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSMSG01Y (working storage)
- CSMSG02Y (working storage)

### Needs clarification

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-118, CAFM-BR-119.
- SME-144: When the request to mark or unmark an authorization as fraud does not complete normally, what should the operator see, and what state should the authorization be left in? (Authorization business analyst) On CAFM-BR-120.
- SME-145: When adding or updating a fraud record fails for any reason other than a duplicate record, what status and message should go back to the operator? (Fraud management team) On CAFM-BR-120.
- SME-146: The fraud update is written to the fraud store first, then to the authorization detail record. If the second write fails after the first has succeeded, nothing is rolled back. Must both updates succeed or fail together? (Architecture team) On CAFM-BR-120.
- SME-147: When an authorization's fraud flag is changed, which data stores must hold the new fraud flag and fraud report date: the authorization detail record, the fraud store, or both? (Data architect) On CAFM-BR-120.
- SME-148: If the fraud update reports success but the authorization's database status is neither blank nor 'FW', what message should the system show? (Business analyst) On CAFM-BR-120.
- SME-149: Please confirm: after the fraud flag is changed, the system sends a fraud update request with the updated authorization record, the account ID and the customer ID, to be recorded in the authorization fraud store (CARDDEMO.AUTHFRDS). (Business analyst) On CAFM-BR-120.
- DEF-137: Is this intended? If the LINK to the fraud processor fails, the change is rolled back with no message; and on any rollback the screen still shows the toggled fraud flag that was not saved. (Subject-matter expert) On CAFM-BR-120.

### Decision table gaps

None.
