# Feature specification: View account and customer details for update

**Feature:** OATM-C02 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C02)

As an operator, I want the fetched or entered account and customer values shown with the right fields open for editing, so that I can see what is stored and change only what may be changed.

Shows the operator the stored account and customer details, or the values they have entered, with the right fields open for editing at each stage of the update. Only editable fields may be opened. Account number, customer number and country stay protected while editing, and every field is locked once changes are waiting for confirmation or saved. The screen must always show the current information and error messages.

**Acceptance scenarios:**

1. **Given** information message: 'Update account details presented above.'; return message: 'No change detected with respect to values fetched.', **when** Account Update screen runs, **then** Both messages appear on the screen (OATM-C02-AC-01)
2. **Given** update stage: 'S' (details shown), **when** the account update screen shows the original values, **then** Error highlights are cleared and the message reads 'Update account details presented above.' (OATM-C02-AC-02)
3. **Given** update stage: 'S', **when** the account update screen is shown after details were fetched and the stage is details shown ('S') or changes not OK ('E'), **then** Message 'Update account details presented above.' (OATM-C02-AC-03)
4. **Given** update stage: 'E', **when** the account update screen is shown after details were fetched and the stage is details shown ('S') or changes not OK ('E'), **then** Message 'Update account details presented above.' (OATM-C02-AC-04)
5. **Given** account found: yes; stored credit limit: 5000.00; stored open date: 2015-03-14, **when** the original values are shown and either the account or the customer was found, **then** Credit limit shows as a formatted 5,000.00 and the open date shows as year 2015, month 03, day 14 (OATM-C02-AC-05)
6. **Given** customer found: yes; stored SSN: 123456789; stored phone 1: (212)555-1234, **when** the original values are shown and the customer was found, **then** SSN shows as 123 / 45 / 6789 and phone 1 shows as 212 / 555 / 1234 (OATM-C02-AC-06)
7. **Given** account id: 00000000001, **when** the account update screen is shown on re-entry, **then** Account id 00000000001 is shown (OATM-C02-AC-07)
8. **Given** update stage: not fetched, **when** the screen is shown on re-entry and either no details have been fetched or the account id is zero, **then** All detail fields are blank (OATM-C02-AC-08)
9. **Given** update stage: 'S', **when** the screen is shown on re-entry with details shown ('S'), **then** Original stored values are shown (OATM-C02-AC-09)
10. **Given** update stage: 'E'; entered credit limit: 7000.00, **when** the screen is shown on re-entry with details shown ('S'), **then** The entered 7000.00 is shown again, so the operator can correct it (OATM-C02-AC-10)
11. **Given** Screen state: 'S'; Field: Credit limit, **when** account details are shown for editing (state 'S') or shown again with input errors (state 'E'), **then** The field can be typed in (OATM-C02-AC-11)
12. **Given** Screen state: 'E'; Field: Country, **when** account details are shown for editing (state 'S' or 'E'), **then** The field is protected (OATM-C02-AC-12)
13. **Given** Screen state: 'S'; Field: Customer number, **when** account details are shown for editing (state 'S' or 'E'), **then** The field is protected (OATM-C02-AC-13)
14. **Given** Screen state: 'N', **when** changes are waiting for confirmation (state 'N') or have been saved (state 'C'), **then** All fields are protected while the operator decides whether to press F5 to save (OATM-C02-AC-14)
15. **Given** Screen state: not fetched (blank), **when** changes are waiting for confirmation (state 'N') or have been saved (state 'C'), **then** Only the account number can be entered (OATM-C02-AC-15)

## Requirements

### Functional requirements

- **OATM-REQ-F-015** (formatting): The system shall always show the current information message and the current error or return message in their message lines. Rules: OATM-BR-015.
- **OATM-REQ-F-016** (formatting): When the account update screen shows the original values, the system shall clear all field-error flags and set the information message to 'Update account details presented above.' Rules: OATM-BR-016.
- **OATM-REQ-F-017** (formatting): When the account update screen is shown after details were fetched and the stage is details shown ('S') or changes not OK ('E'), the system shall set the information message to 'Update account details presented above.' Rules: OATM-BR-017.
- **OATM-REQ-F-018** (formatting): When the original values are shown and either the account or the customer was found, the system shall show the stored account status, the current balance, credit limit, cash credit limit and cycle credit and debit as formatted amounts, the open, expiry and reissue dates as year, month and day, and the account group. Rules: OATM-BR-018.
- **OATM-REQ-F-019** (formatting): When the original values are shown and the customer was found, the system shall show the stored customer details, with the SSN split into 3-2-4 digits, both phone numbers split into area code, prefix and line number, and the date of birth split into year, month and day. Rules: OATM-BR-019.
- **OATM-REQ-F-020** (formatting): When the account update screen is shown on re-entry, the system shall show the entered account id, but leave it blank when the id is zero and the account search is valid. Rules: OATM-BR-020.
- **OATM-REQ-F-021** (formatting): When the screen is shown on re-entry and either no details have been fetched or the account id is zero, the system shall show all account and customer fields blank. Rules: OATM-BR-021.
- **OATM-REQ-F-022** (formatting): When the screen is shown on re-entry with details shown ('S'), the system shall show the original fetched values, and when changes have been made ('E', 'N', 'C', 'L', 'F'), the system shall show the values the operator entered. Rules: OATM-BR-022.
- **OATM-REQ-F-023** (formatting): While account details are shown for editing (state 'S') or shown again with input errors (state 'E'), the system shall let the operator change status, credit and cash limits, balance, cycle credit and debit, open, expiry and reissue dates, group, SSN, FICO score, date of birth, names, address lines, city, state, ZIP, both phones, government ID, EFT account and primary-holder flag. Rules: OATM-BR-023.
- **OATM-REQ-N-001** (formatting): While account details are shown for editing (state 'S' or 'E'), the system shall keep the account number, customer number and country protected so they cannot be changed. Rules: OATM-BR-024.
- **OATM-REQ-N-002** (formatting): While changes are waiting for confirmation (state 'N') or have been saved (state 'C'), the system shall protect every field. Rules: OATM-BR-025.
- **OATM-REQ-F-024** (formatting): While no account is fetched yet or the save failed, the system shall leave only the account number open for entry. Rules: OATM-BR-025.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-015 | Default to search prompt and show messages | formatting | THE Account Update screen SHALL always show the current information message and the current error or return message in their message lines. | medium | app/cbl/COACTUPC.cbl:2955-2982, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-016 | Display fetched original values | formatting | WHEN the account update screen shows the original values, THE Account Update screen SHALL clear all field-error flags (WS-NON-KEY-FLAGS) and set the information message to 'Update account details presented above.' | medium | app/cbl/COACTUPC.cbl:2785-2864, app/cbl/COACTUPC.cbl:2698-2725 |
| OATM-BR-017 | Prompt operator to edit shown details | formatting | WHEN the account update screen is shown after details were fetched and the stage is details shown ('S') or changes not OK ('E'), THE Account Update messaging SHALL set the information message to 'Update account details presented above.' | medium | app/cbl/COACTUPC.cbl:2962-2965, app/cbl/COACTUPC.cbl:470-471 |
| OATM-BR-018 | Display fetched original values | formatting | WHEN the original values are shown and either the account or the customer was found, THE Account Update screen SHALL show the stored account status, the current balance, credit limit, cash credit limit and cycle credit and debit as formatted amounts, the open, expiry and reissue dates as year, month and day, and the account group. | medium | app/cbl/COACTUPC.cbl:2785-2864, app/cbl/COACTUPC.cbl:2698-2725 |
| OATM-BR-019 | Display fetched original values | formatting | WHEN the original values are shown and the customer was found, THE Account Update screen SHALL show the stored customer details, with the SSN split into 3-2-4 digits, both phone numbers split into area code, prefix and line number, and the date of birth split into year, month and day. | medium | app/cbl/COACTUPC.cbl:2785-2864, app/cbl/COACTUPC.cbl:2698-2725 |
| OATM-BR-020 | Choose which account values to display | formatting | WHEN the account update screen is shown on re-entry, THE Account Update screen SHALL show the entered account id, but leave it blank when the id is zero and the account search is valid. | medium | app/cbl/COACTUPC.cbl:2698-2725, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-021 | Choose which account values to display | formatting | WHEN the screen is shown on re-entry and either no details have been fetched or the account id is zero, THE Account Update screen SHALL show all account and customer fields blank. | medium | app/cbl/COACTUPC.cbl:2698-2725, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-022 | Choose which account values to display | formatting | WHEN the screen is shown on re-entry with details shown ('S'), THE Account Update screen SHALL show the original fetched values; WHEN changes have been made ('E','N','C','L','F'), it SHALL show the values the operator entered. | medium | app/cbl/COACTUPC.cbl:2698-2725, app/cbl/COACTUPC.cbl:656-668 |
| OATM-BR-023 | Editable versus protected fields | formatting | WHEN account details are shown for editing (state 'S') or shown again with input errors (state 'E'), THE account update screen SHALL let the operator change status, credit and cash limits, balance, cycle credit and debit, open, expiry and reissue dates, group, SSN, FICO score, date of birth, names, address lines, city, state, ZIP, both phones, government ID, EFT account and primary-holder flag. | medium | app/cbl/COACTUPC.cbl:2986-3005, app/cbl/COACTUPC.cbl:3441-3495, app/cbl/COACTUPC.cbl:3500-3560, app/cbl/COACTUPC.cbl:654-668 |
| OATM-BR-024 | Editable versus protected fields | formatting | WHEN account details are shown for editing (state 'S' or 'E'), THE account update screen SHALL keep the account number, customer number and country protected so they cannot be changed. | medium | app/cbl/COACTUPC.cbl:2986-3005, app/cbl/COACTUPC.cbl:3441-3495, app/cbl/COACTUPC.cbl:3500-3560, app/cbl/COACTUPC.cbl:654-668 |
| OATM-BR-025 | Editable versus protected fields | formatting | WHEN changes are waiting for confirmation (state 'N') or have been saved (state 'C'), THE account update screen SHALL protect every field; WHEN no account is fetched yet or the save failed, it SHALL leave only the account number open for entry. | medium | app/cbl/COACTUPC.cbl:2986-3005, app/cbl/COACTUPC.cbl:3441-3495, app/cbl/COACTUPC.cbl:3500-3560, app/cbl/COACTUPC.cbl:654-668 |

### Key entities

- CSMSG02Y (file record)
- CVACT01Y (file record)
- CVACT03Y (file record)
- CVCUS01Y (file record)
- COCOM01Y (working storage)
- COTTL01Y (working storage)
- CSDAT01Y (working storage)
- CSLKPCDY (working storage)
- CSMSG01Y (working storage)
- CSSETATY (working storage)
- CSSTRPFY (working storage)
- CSUSR01Y (working storage)
- CSUTLDPY (working storage)
- CSUTLDWY (working storage)
- CVCRD01Y (working storage)

### Needs clarification

None.

### Decision table gaps

- Field protection by update stage: R31 lists stage 'L' among change stages, but no rule says which fields are open or protected in that stage.
