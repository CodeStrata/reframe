# Implementation plan: View a single transaction (OATM-C29)

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as online.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is final.

## Screens

### Transactions (S-TRANSACTION-LIST)

Browse transactions page by page from a chosen ID and open any one with a row action instead of typing S against it.

Prototype: `ui-reference/index.html#/S-TRANSACTION-LIST`. Replaces the legacy screens COTRN0A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|

### Transaction (S-TRANSACTION-VIEW)

Show one transaction's card, type, category, source, amount, dates and merchant together, opened from the list or looked up by ID.

Prototype: `ui-reference/index.html#/S-TRANSACTION-VIEW`. Replaces the legacy screens COTRN1A.

| Component | Type | Shows | Checks | Goes to | Requirements |
|---|---|---|---|---|---|
| Transaction ID | search | Pre-filled when opened from the list | Required: 'Tran ID can NOT be empty...'; must exist: 'Transaction ID NOT found...'. |  | OATM-REQ-F-229, OATM-REQ-F-233 |
| Look up | button |  |  |  | OATM-REQ-F-228 |
| Clear | button |  |  |  | OATM-REQ-F-235 |
| Lookup error | message | 'Unable to lookup Transaction...' when the file cannot be read |  |  | OATM-REQ-F-237 |
| Transaction ID | display |  |  |  | OATM-REQ-F-231 |
| Amount | display | Signed amount, +99999999.99 |  |  | OATM-REQ-F-232 |
| Back to transactions | link |  |  | S-TRANSACTION-LIST | OATM-REQ-F-236 |
| Back | link |  |  | S-APP-SHELL | OATM-REQ-F-234 |


## Data model

#### CVTRA05Y

File record of COTRN01C. Source: `app/cpy/CVTRA05Y.cpy`.

Record `TRAN-RECORD`:

| Field | In | PIC | Type | Code type | Column type | Values |
|---|---|---|---|---|---|---|
| TRAN-ID |  | X(16) | text, 16 characters |  |  |  |
| TRAN-TYPE-CD |  | X(02) | text, 2 characters |  |  |  |
| TRAN-CAT-CD |  | 9(04) | unsigned integer, 4 digits (zoned decimal) |  |  |  |
| TRAN-SOURCE |  | X(10) | text, 10 characters |  |  |  |
| TRAN-DESC |  | X(100) | text, 100 characters |  |  |  |
| TRAN-AMT |  | S9(09)V99 | signed decimal, 9 integer and 2 fraction digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-ID |  | 9(09) | unsigned integer, 9 digits (zoned decimal) |  |  |  |
| TRAN-MERCHANT-NAME |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-CITY |  | X(50) | text, 50 characters |  |  |  |
| TRAN-MERCHANT-ZIP |  | X(10) | text, 10 characters |  |  |  |
| TRAN-CARD-NUM |  | X(16) | text, 16 characters |  |  |  |
| TRAN-ORIG-TS |  | X(26) | text, 26 characters |  |  |  |
| TRAN-PROC-TS |  | X(26) | text, 26 characters |  |  |  |
| FILLER |  | X(20) | text, 20 characters |  |  |  |

- COCOM01Y (working storage of COTRN01C): see data-contracts.md.
- COTTL01Y (working storage of COTRN01C): see data-contracts.md.
- CSDAT01Y (working storage of COTRN01C): see data-contracts.md.
- CSMSG01Y (working storage of COTRN01C): see data-contracts.md.

## Design notes

None.

## Decision tables

#### Transaction View lookup outcome

| Transaction ID | Transaction file read result | Screen result | Rule |
|---|---|---|---|
| blank | not read | No lookup; message 'Tran ID can NOT be empty...' | OATM-BR-243 |
| entered | found | Show transaction and merchant details with signed amount | OATM-BR-244 |
| entered | not found | Message 'Transaction ID NOT found...', cursor on Transaction ID | OATM-BR-246 |
| entered | other failure | Log response and reason codes; message 'Unable to lookup Transaction...' | OATM-BR-247 |

#### Transaction View key handling

| Key pressed | Screen action | Rule |
|---|---|---|
| Enter | Read entered Transaction ID and look up the transaction | OATM-BR-241 |
| PF3 | Return to calling program, or main menu COMEN01C if none known | OATM-BR-248 |
| PF4 | Clear all fields and message, cursor on Transaction ID | OATM-BR-249 |
| PF5 | Go to transaction list COTRN00C | OATM-BR-250 |
| any other key | Message 'Invalid key pressed. Please see below...' | OATM-BR-251 |

