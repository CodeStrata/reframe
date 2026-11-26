# Feature specification: Capture entered changes

**Feature:** OATM-C03 · Online Account and Transaction Management · Customer Account Self-Service

**Status: FINAL**, signed off by Sam (acceptance), 2026-11-25.

## User scenarios and testing

### User story (OATM-C03)

As an operator, I want the values I type to be captured as proposed changes, with blank or '*' entries treated as not supplied, so that the system knows exactly what I intend to change.

Takes what the operator typed on the update screen and turns it into proposed new values for the account and customer. A blank or '*' entry means 'not supplied', never a value to save. Amounts typed as currency (with '$', commas, sign or decimals) are converted to numbers with two decimal places. It must never confuse 'left blank' with a real value, and must never lose or round an entered amount wrongly.

**Acceptance scenarios:**

1. **Given** account group: '*', **when** the operator submits changes and the account group entry is '*' or blank, **then** Proposed group is not supplied (OATM-C03-AC-01)
2. **Given** account group: GOLD, **when** the operator submits changes and the account group entry is '*' or blank, **then** Proposed group is GOLD (OATM-C03-AC-02)
3. **Given** country code: (blank), **when** the operator submits changes and the country code entry is '*' or blank, **then** Country code not supplied, so the later required-field check fails (OATM-C03-AC-03)
4. **Given** country code: USA, **when** the operator submits changes and the country code entry is '*' or blank, **then** Proposed country code USA (OATM-C03-AC-04)
5. **Given** Account details shown: yes; Customer number entered: *, **when** account details are already on the update screen and the operator submits the customer number field as '*' or blank, **then** The proposed customer number is set to not supplied (low-values) (OATM-C03-AC-05)
6. **Given** Account details shown: yes; Customer number entered: 000000123, **when** account details are already on the update screen and the operator submits the customer number field as '*' or blank, **then** The proposed customer number is 000000123 (OATM-C03-AC-06)
7. **Given** Account details shown: no (only the account number was entered); Customer number entered: 000000123, **when** account details are already on the update screen and the operator submits the customer number field as '*' or blank, **then** The customer number is not staged; only the account number is read (OATM-C03-AC-07)
8. **Given** Account details shown: yes; Government ID entered: (blank), **when** account details are already on the update screen and the operator submits the government-issued ID field as '*' or blank, **then** The proposed government ID is set to not supplied (low-values) (OATM-C03-AC-08)
9. **Given** Credit limit entered: *, **when** the operator submits changes to a fetched account and any of the five amount fields (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit) is blank or '*', **then** Credit limit is treated as not supplied (OATM-C03-AC-09)
10. **Given** Cycle debit entered: (blank), **when** the operator submits changes to a fetched account and any of the five amount fields (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit) is blank or '*', **then** Cycle debit is treated as not supplied (OATM-C03-AC-10)
11. **Given** Credit limit entered: $5,000.00, **when** an entered amount reads as a valid currency number (an optional '$', thousands commas, a sign and decimals allowed), **then** Proposed credit limit is 5000.00 (OATM-C03-AC-11)
12. **Given** Current balance entered: -250.5, **when** an entered amount reads as a valid currency number (an optional '$', thousands commas, a sign and decimals allowed), **then** Proposed current balance is -250.50 (OATM-C03-AC-12)
13. **Given** Expiry month entry: 05, **when** the operator submits the account update screen after the account details are shown, **then** The expiry month is taken as 05. (OATM-C03-AC-13)
14. **Given** Date of birth year: *, **when** the operator enters a date of birth part as '*' or leaves it blank, **then** The year is treated as not supplied and fails the date check. (OATM-C03-AC-14)
15. **Given** Date of birth year: 1980; Month: 05; Day: 14, **when** the operator enters a date of birth part as '*' or leaves it blank, **then** 1980-05-14 is taken as the proposed date of birth. (OATM-C03-AC-15)

## Requirements

### Functional requirements

- **OATM-REQ-F-025** (design note): When the operator submits changes and the account group entry is '*' or blank, the system shall treat the group as not supplied, and otherwise take the entered group as the proposed group. Rules: OATM-BR-026.
- **OATM-REQ-F-026** (design note): When the operator submits changes and the country code entry is '*' or blank, the system shall treat the country code as not supplied, and otherwise take the entered value as the proposed country code. Rules: OATM-BR-027.
- **OATM-REQ-F-027** (design note): When account details are already on the update screen and the operator submits the customer number field as '*' or blank, the system shall treat the customer number as not supplied, and otherwise take the entered customer number as the proposed value to compare with the stored one and write to the customer record on save. Rules: OATM-BR-028.
- **OATM-REQ-F-028** (design note): When account details are already on the update screen and the operator submits the government-issued ID field as '*' or blank, the system shall treat the government ID as not supplied, and otherwise take the entered value as the proposed government ID to compare with the stored one and write to the customer record on save. Rules: OATM-BR-029.
- **OATM-REQ-F-029** (design note): When the operator submits changes to a fetched account and any of the credit limit, cash credit limit, current balance, current cycle credit or current cycle debit is blank or '*', the system shall treat that amount as not supplied. Rules: OATM-BR-030.
- **OATM-REQ-F-030** (design note): When an entered amount reads as a valid currency number (an optional '$', thousands commas, a sign and decimals allowed), the system shall convert it to the proposed new numeric amount with two decimal places. Rules: OATM-BR-031.
- **OATM-REQ-F-031** (design note): When the operator submits the account update screen after the account details are shown, the system shall treat each year, month or day part of the open, expiry and reissue dates entered as '*' or left blank as not supplied, and take any other entry as typed. Rules: OATM-BR-032.
- **OATM-REQ-F-032** (design note): When the operator enters a date of birth part (year, month or day) as '*' or leaves it blank, the system shall treat that part as not supplied, and otherwise take the entered part as the proposed value. Rules: OATM-BR-033.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| OATM-BR-026 | Stage entered account group | design note | WHEN the operator submits changes and the account group entry is '*' or blank, THE Account Update entry capture SHALL treat the group as not supplied (ACUP-NEW-GROUP-ID set to low-values); otherwise it SHALL take the entered group as the proposed group. | medium | app/cbl/COACTUPC.cbl:1211-1218, app/cbl/COACTUPC.cbl:1056-1062 |
| OATM-BR-027 | Stage country code entry | design note | WHEN the operator submits changes and the country code entry is '*' or blank, THE Account Update entry capture SHALL treat the country code as not supplied; otherwise it SHALL take the entered value as the proposed country code. | medium | app/cbl/COACTUPC.cbl:1343-1348 |
| OATM-BR-028 | Stage customer identifier entry | design note | WHEN account details are already on the update screen and the operator submits the customer number field as '*' or blank, THE account update screen SHALL treat the customer number as not supplied (low-values); otherwise it SHALL take the entered customer number as the proposed value, which is compared with the stored one and written to the customer record on save. | medium | app/cbl/COACTUPC.cbl:1220-1229, app/cbl/COACTUPC.cbl:1060-1062, app/cbl/COACTUPC.cbl:1708-1711, app/cbl/COACTUPC.cbl:4009 |
| OATM-BR-029 | Stage government identifier entry | design note | WHEN account details are already on the update screen and the operator submits the government-issued ID field as '*' or blank, THE account update screen SHALL treat the government ID as not supplied (low-values); otherwise it SHALL take the entered value as the proposed government ID, which is compared with the stored one and written to the customer record on save. | medium | app/cbl/COACTUPC.cbl:1399-1406, app/cbl/COACTUPC.cbl:1060-1062, app/cbl/COACTUPC.cbl:1755-1758, app/cbl/COACTUPC.cbl:4045-4046 |
| OATM-BR-030 | Stage entered credit limit amount | design note | WHEN the operator submits changes to a fetched account and any of the five amount fields (credit limit, cash credit limit, current balance, current cycle credit, current cycle debit) is blank or '*', THE Account Update screen SHALL treat that amount as not supplied. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-031 | Convert entered credit limit | design note | WHEN an entered amount reads as a valid currency number (an optional '$', thousands commas, a sign and decimals allowed), THE Account Update screen SHALL convert it to the proposed new numeric amount, with two decimal places. | high | app/cbl/COACTUPC.cbl:1072-1140, app/cbl/COACTUPC.cbl:1458-1470, app/cbl/COACTUPC.cbl:1472-1527, app/cbl/COACTUPC.cbl:2178-2224 |
| OATM-BR-032 | Stage entered account open date | design note | WHEN the operator submits the account update screen after the account details are shown, THE Account Update screen SHALL treat each year, month or day part of the open, expiry and reissue dates entered as '*' or left blank as not supplied, and take any other entry as typed. | high | app/cbl/COACTUPC.cbl:1144-1209, app/cbl/COACTUPC.cbl:1460-1543, app/cpy/CSUTLDPY.cpy:18-331, app/cpy/CSUTLDWY.cpy:4-63 |
| OATM-BR-033 | Stage date of birth parts | design note | WHEN the operator enters a date of birth part as '*' or leaves it blank, THE account update screen SHALL treat that part (year, month or day) as not supplied; otherwise it SHALL take the entered part as the proposed value. | high | app/cbl/COACTUPC.cbl:1254-1275, app/cbl/COACTUPC.cbl:1533-1543, app/cpy/CSUTLDPY.cpy:341-370 |

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

- SME-056: Can the customer identifier be changed on the account update screen, or should it be shown read-only? (Account servicing business owner) On OATM-BR-026, OATM-BR-027, OATM-BR-028, OATM-BR-029, OATM-BR-031, OATM-BR-032, OATM-BR-033.
- DEF-011: Confirm this is deliberate: The amount check accepts any signed currency number, so a negative or zero credit limit, cash credit limit or cycle amount passes validation and can be saved. (Subject-matter expert) On OATM-BR-031.
- DEF-036: Is this intended? When the date service returns a non-zero severity, the check jumps to the end of the final-check paragraph (EDIT-DATE-LE-EXIT). It then runs on into the statement that marks the whole date valid (WS-EDIT-DATE-IS-VALID). The rejected date's year, month and day flags are therefore reset to valid, the field is not marked as in error, and for Date of Birth the future-date check still runs. The input-error state and the message do stay set. (Subject-matter expert) On OATM-BR-032.
- DEF-037: Is this intended? A date of birth equal to today is rejected with a message saying it is in the future, which it is not. (Subject-matter expert) On OATM-BR-033.

### Decision table gaps

- Capture of each entered field: No rule says how '*' or blank entries are captured for these fields.
- Capture of each entered field: No rule says what proposed amount is held when the entry is not a valid currency number (validation rejects it, see R43).
