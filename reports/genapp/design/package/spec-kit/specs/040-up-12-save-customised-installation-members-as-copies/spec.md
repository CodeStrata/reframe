# Feature specification: Save customised installation members as copies

**Feature:** UP-C12 · Unassigned-Programs · Programs not in a business function

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## User scenarios and testing

### User story (UP-C12)

As an installer, I want each customised member saved as a separate copy while the original template stays unchanged, so that I can re-run the customisation and keep the shipped templates intact.

Saves each customised installation member as a separate copy, so installers can re-run the customisation at any time. The member ONCICS is saved as '#ONCICS', and every other member as '@' followed by its name. The shipped templates must never be changed, and each re-run replaces the earlier customised copy.

**Acceptance scenarios:**

1. **Given** member being edited: ONCICS, **when** the customisation macro has made its substitutions in a member named ONCICS, **then** The customised text is saved as member #ONCICS (UP-C12-AC-01)
2. **Given** member being edited: DB2CRE, **when** the customisation macro has made its substitutions in any member other than ONCICS, **then** The customised text is saved as member @DB2CRE (UP-C12-AC-02)
3. **Given** member being edited: DB2CRE; member text: DSN=<DB2HLQ>.SDSNLOAD, **when** installation customisation macro runs, **then** DB2CRE still contains <DB2HLQ>; @DB2CRE contains the substituted value (UP-C12-AC-03)

## Requirements

### Functional requirements

- **UP-REQ-F-093** (design note): When the substitutions have been made in a member named 'ONCICS', the system shall save the whole customised text as a new member named '#ONCICS', replacing any existing member of that name. Rules: UP-BR-115, UP-BR-116.
- **UP-REQ-F-094** (historical artifact): When the substitutions have been made in a member with any name other than 'ONCICS', the system shall save the whole customised text as a member named '@' followed by the original member name, replacing any existing member of that name. Rules: UP-BR-117, UP-BR-118, UP-BR-079, UP-BR-080, UP-BR-081, UP-BR-082, UP-BR-083, UP-BR-084, UP-BR-085, UP-BR-086, UP-BR-087, UP-BR-088, UP-BR-089, UP-BR-090.
- **UP-REQ-F-095** (design note): The system shall leave the original template member unchanged, discarding the edit session after the customised copy has been saved under the prefixed name. Rules: UP-BR-119, UP-BR-120.

### Business rules

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
| UP-BR-115 | Derive prefixed backup member name | design note | WHEN the member being customised is named 'ONCICS', THE installation customisation macro SHALL save the customised text as a new member named '#ONCICS'. | medium | base/exec/mac1.rexx:58-62 |
| UP-BR-116 | Save full member content as copy | design note | WHEN the customisation macro has made its substitutions in a member named ONCICS, THE installation customisation macro SHALL save the whole customised text as a new member named '#ONCICS', replacing any existing member of that name. | medium | base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:110-122 |
| UP-BR-117 | Derive prefixed backup member name | design note | WHEN the member being customised has any name other than 'ONCICS', THE installation customisation macro SHALL save the customised text as a new member named '@' followed by the original member name. | medium | base/exec/mac1.rexx:58-62 |
| UP-BR-118 | Save full member content as copy | design note | WHEN the customisation macro has made its substitutions in any member other than ONCICS, THE installation customisation macro SHALL save the whole customised text under the member name prefixed with '@', replacing any existing member of that name. | medium | base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:110-122 |
| UP-BR-079 | Replace log placeholder with configured qualifier | historical artifact | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<WSIMLOG>' in each member it edits with the workload-simulator high-level qualifier (WSIMHLQ, e.g. 'PP.WSIM.V110'), not with the log data set name, and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:12-13, base/exec/mac1.rexx:45, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:21 |
| UP-BR-080 | Replace load library placeholder in member | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<LOADX>' in each member it edits with the GenApp load library name (LOADX, the installation qualifier followed by '.LOAD'), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:14, base/exec/mac1.rexx:50, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:41 |
| UP-BR-081 | Substitute application-region system identifier placeholders | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<AORSYSID>' in each member it edits with the application-owning region system identifier (AORSYSID), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:11, base/exec/mac1.rexx:34, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:27 |
| UP-BR-082 | Replace run placeholder with configured value | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<DB2RUN>' in each member it edits with the configured database run library value (DB2RUN), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:10, base/exec/mac1.rexx:24, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:15 |
| UP-BR-083 | Replace tor application placeholder in member | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<TORAPPL>' in each member it edits with the terminal-owning region application identifier (TORAPPL), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:11, base/exec/mac1.rexx:30, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:23 |
| UP-BR-084 | Replace source placeholder with environment name | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<SOURCEX>' in each member it edits with the GenApp source library name (SOURCEX, the installation qualifier followed by '.SRC'), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:14, base/exec/mac1.rexx:49, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:41 |
| UP-BR-085 | Substitute tor system identifier placeholders | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<TORSYSID>' in each member it edits with the terminal-owning region system identifier (TORSYSID), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:11, base/exec/mac1.rexx:33, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:26 |
| UP-BR-086 | Replace home directory placeholders | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<ZFSHOME>' in each member it edits with the configured file-system home directory (ZFSHOME), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:15, base/exec/mac1.rexx:56, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:22 |
| UP-BR-087 | Replace database id placeholders in member | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<DB2DBID>' in each member it edits with the configured database name (DB2DBID), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:10, base/exec/mac1.rexx:27, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:18 |
| UP-BR-088 | Replace placeholder with session value | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<WSIMMSX>' in each member it edits with the GenApp message-text library name (WSIMMSX, the installation qualifier followed by '.MSGTXT'), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:15, base/exec/mac1.rexx:54, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:51 |
| UP-BR-089 | Substitute data-owning region application name | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<DORAPPL>' in each member it edits with the data-owning region application identifier (DORAPPL), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:11, base/exec/mac1.rexx:32, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:25 |
| UP-BR-090 | Substitute transaction-server prefix placeholders | design note | THE installation customization edit macro (MAC1) SHALL replace every occurrence of the placeholder '<CICSHLQ>' in each member it edits with the configured transaction-server library prefix (CICSHLQ), and save the result as a customized copy of the member. | medium | base/exec/mac1.rexx:9, base/exec/mac1.rexx:16, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:7 |
| UP-BR-119 | Derive prefixed backup member name | design note | THE installation customisation macro SHALL leave the original member unchanged, discarding the edit session after the customised copy has been saved under the prefixed name. | medium | base/exec/mac1.rexx:58-62 |
| UP-BR-120 | Save full member content as copy | design note | THE installation customisation macro SHALL leave the original template member unchanged, discarding the edits after the customised copy has been saved. | medium | base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:110-122 |

### Key entities

None found in the source.

### Needs clarification

- DEF-042: Is this intended? MAC1 fetches the log data set name (WSIMLOG) from the pool, but it replaces '<WSIMLOG>' with WSIMHLQ instead. Lines 41-46 do the same for '<PDSDBRM>', '<PDSMACP>', '<PDSLOAD>', '<PDSMSGS>' and '<WSIMSTL>'. This looks like a copy-and-paste slip. It does no harm today because no member uses these placeholders. (Subject-matter expert) On UP-BR-079.

### Decision table gaps

None.
