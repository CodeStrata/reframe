# Design: View authorization detail and mark fraud (CAFM-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

The Authorization details screen for fraud analysts. It shows a selected authorization with its response ('A' in green for '00', otherwise 'D' in red) and its reason as code and description. With PF5 the analyst reports the authorization as fraud or withdraws a fraud report. A toggle must always act on a freshly re-read record: 'F' becomes 'R' (remove fraud) and anything else becomes 'F' (report fraud), and the record goes to fraud processing with its account and customer number.

Runs as online. Journeys: J15.

## Screens and components

### Pending authorizations (S-PENDING-AUTHS)

Look up an account and see its customer, limits, balances and approved/declined totals together with a paged table of its pending authorizations; open any authorization from its row.

Prototype: `ui-reference/index.html#/S-PENDING-AUTHS`. Replaces the legacy screens COPAU0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Authorization details (S-AUTH-DETAIL)

Review one pending authorization — card, amount, response and reason, POS, merchant and fraud status — move to the account's next authorization, and mark or clear fraud on it.

Prototype: `ui-reference/index.html#/S-AUTH-DETAIL`. Replaces the legacy screens COPAU1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Response | display | 'Approved' (green) when response code is '00', otherwise 'Declined' (red); the word is always shown so colour is not the only cue |  |  | CAFM-REQ-F-113 |
| Reason | display | '<code>-<description>' from the decline reason table, or '9999-ERROR' when the code is not in the table |  |  | CAFM-REQ-F-112 |
| Mark as fraud / Remove fraud mark | button | Label follows the current state: 'Remove fraud mark' when flagged F, otherwise 'Mark as fraud'; opens a confirmation |  |  | CAFM-REQ-F-114 |


## Data models

- CIPAUDTY (working storage of COPAUS1C): see data-contracts.md.
- CIPAUSMY (working storage of COPAUS1C): see data-contracts.md.
- COCOM01Y (working storage of COPAUS1C): see data-contracts.md.
- COTTL01Y (working storage of COPAUS1C): see data-contracts.md.
- CSDAT01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG01Y (working storage of COPAUS1C): see data-contracts.md.
- CSMSG02Y (working storage of COPAUS1C): see data-contracts.md.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| CAFM-BR-118 | Look up decline reason description | formatting | WHEN authorization details are being populated, THE Authorization Detail View SHALL show the reason as '<code>-<description>' from the decline reason table, or as '9999-ERROR' when the code is not in the table | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:319-328, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:319-328 |
| CAFM-BR-119 | Classify authorization as approved or declined | formatting | WHEN the authorization detail screen shows an authorization, THE authorization detail screen SHALL show response 'A' in green when the response code is '00', otherwise 'D' in red. | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:294, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:311-317 |
| CAFM-BR-120 | Toggle authorization fraud mark | business rule | WHEN the user presses PF5 on the selected authorization, THE authorization detail screen SHALL re-read the authorization and, if its fraud flag is 'F', set it to 'R' with a remove-fraud action ('R'), otherwise set it to 'F' with a report-fraud action ('F'), and pass the record with account and customer number to the fraud processor (COPAUS2C). | medium | app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:230-252, app/app-authorization-ims-db2-mq/cbl/COPAUS1C.cbl:93-104, app/app-authorization-ims-db2-mq/cpy/CIPAUDTY.cpy:50-52 |

### Worked examples

- CAFM-BR-119: response code = 00 → 'A' shown in green.
- CAFM-BR-119: response code = 05 → 'D' shown in red.
- CAFM-BR-120: fraud flag = F → Flag becomes 'R' and the fraud processor is asked to remove the fraud report.
- CAFM-BR-120: fraud flag = blank → Flag becomes 'F' and the fraud processor is asked to report fraud.
- CAFM-BR-120: fraud flag = R → Flag becomes 'F' and the fraud processor is asked to report fraud.

## Decision tables

None.

## Design notes

None.

## Open questions

- SME-143: On the authorization detail screen, what should happen (a) when the screen is opened without any data from the screen that called it, and (b) when the user presses PF3 after the screen is already showing? (Authorization business analyst) On CAFM-BR-118, CAFM-BR-119.
- SME-144: When the request to mark or unmark an authorization as fraud does not complete normally, what should the operator see, and what state should the authorization be left in? (Authorization business analyst) On CAFM-BR-120.
- SME-145: When adding or updating a fraud record fails for any reason other than a duplicate record, what status and message should go back to the operator? (Fraud management team) On CAFM-BR-120.
- SME-146: The fraud update is written to the fraud store first, then to the authorization detail record. If the second write fails after the first has succeeded, nothing is rolled back. Must both updates succeed or fail together? (Architecture team) On CAFM-BR-120.
- SME-147: When an authorization's fraud flag is changed, which data stores must hold the new fraud flag and fraud report date: the authorization detail record, the fraud store, or both? (Data architect) On CAFM-BR-120.
- SME-148: If the fraud update reports success but the authorization's database status is neither blank nor 'FW', what message should the system show? (Business analyst) On CAFM-BR-120.
- SME-149: Please confirm: after the fraud flag is changed, the system sends a fraud update request with the updated authorization record, the account ID and the customer ID, to be recorded in the authorization fraud store (CARDDEMO.AUTHFRDS). (Business analyst) On CAFM-BR-120.
- DEF-137: Is this intended? If the LINK to the fraud processor fails, the change is rolled back with no message; and on any rollback the screen still shows the toggled fraud flag that was not saved. (Subject-matter expert) On CAFM-BR-120.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (6 in all).