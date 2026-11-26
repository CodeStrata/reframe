# Design: Save customised installation members as copies (UP-C12)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Saves each customised installation member as a separate copy, so installers can re-run the customisation at any time. The member ONCICS is saved as '#ONCICS', and every other member as '@' followed by its name. The shipped templates must never be changed, and each re-run replaces the earlier customised copy.

Runs as service.

## Screens and components

No screens: it runs as service.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

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

### Worked examples

- UP-BR-116: member being edited = ONCICS → The customised text is saved as member #ONCICS
- UP-BR-118: member being edited = DB2CRE → The customised text is saved as member @DB2CRE
- UP-BR-120: member being edited = DB2CRE; member text = DSN=<DB2HLQ>.SDSNLOAD → DB2CRE still contains <DB2HLQ>; @DB2CRE contains the substituted value

## Decision tables

#### Name of the saved customised copy

| Member name | Name the customised copy is saved under | Rule |
|---|---|---|
| 'ONCICS' | '#ONCICS', replacing any existing member of that name | UP-BR-115 |
| Any other name | '@' followed by the original member name, replacing any existing member of that name | UP-BR-117 |


## Design notes

- UP-BR-115: When the template being customised is named 'ONCICS', its customised text is saved as a new output named '#ONCICS'.
- UP-BR-116: The whole customised text of 'ONCICS' is written as '#ONCICS' and overwrites any earlier output of that name, so the customisation can be re-run.
- UP-BR-117: Every template other than 'ONCICS' is saved as a new output named '@' followed by the template name.
- UP-BR-118: The whole customised text of every other template is written under the '@'-prefixed name and overwrites any earlier output of that name, so the customisation can be re-run.
- UP-BR-080: After '<LOADX>' has been replaced with the load library name, the result is saved only as the customised copy, never back into the template.
- UP-BR-081: After '<AORSYSID>' has been replaced with the application-owning region system identifier, the result is saved only as the customised copy, never back into the template.
- UP-BR-082: After '<DB2RUN>' has been replaced with the database run library value, the result is saved only as the customised copy, never back into the template.
- UP-BR-083: After '<TORAPPL>' has been replaced with the terminal-owning region application identifier, the result is saved only as the customised copy, never back into the template.
- UP-BR-084: After '<SOURCEX>' has been replaced with the source library name, the result is saved only as the customised copy, never back into the template.
- UP-BR-085: After '<TORSYSID>' has been replaced with the terminal-owning region system identifier, the result is saved only as the customised copy, never back into the template.
- UP-BR-086: After '<ZFSHOME>' has been replaced with the file-system home directory, the result is saved only as the customised copy, never back into the template.
- UP-BR-087: After '<DB2DBID>' has been replaced with the database name, the result is saved only as the customised copy, never back into the template.
- UP-BR-088: After '<WSIMMSX>' has been replaced with the message-text library name, the result is saved only as the customised copy, never back into the template.
- UP-BR-089: After '<DORAPPL>' has been replaced with the data-owning region application identifier, the result is saved only as the customised copy, never back into the template.
- UP-BR-090: After '<CICSHLQ>' has been replaced with the transaction-server library prefix, the result is saved only as the customised copy, never back into the template.
- UP-BR-119: The shipped template is never modified. Substitutions are made on a working copy, which is discarded once the customised output has been saved under its prefixed name.
- UP-BR-120: After the customised copy is saved, the working edits are discarded, so the original template stays exactly as shipped and can be customised again.

## Open questions

- DEF-042: Is this intended? MAC1 fetches the log data set name (WSIMLOG) from the pool, but it replaces '<WSIMLOG>' with WSIMHLQ instead. Lines 41-46 do the same for '<PDSDBRM>', '<PDSMACP>', '<PDSLOAD>', '<PDSMSGS>' and '<WSIMSTL>'. This looks like a copy-and-paste slip. It does no harm today because no member uses these placeholders. (Subject-matter expert) On UP-BR-079.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (3 in all).