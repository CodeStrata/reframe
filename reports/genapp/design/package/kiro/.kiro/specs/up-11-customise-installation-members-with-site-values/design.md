# Design: Customise installation members with site values (UP-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Overview

Fills in the placeholders in the GenApp installation templates with the values the installer configured for their site, so the templates work in that environment. The placeholders stand for library names, region and system identifiers, database names and file paths. Every placeholder must get the value of its own setting and none may be left behind. '<WSIMLOG>', '<WSIMSTL>', '<PDSMACP>', '<PDSDBRM>' and '<PDSMSGS>' must take the simulator product qualifier, as they do today, not the library name they suggest.

Runs as service.

## Screens and components

No screens: it runs as service.

## Data models

None found in the source.

## Business rules

Classes: a *business rule* is kept exactly; *formatting* may be restyled; *error handling* keeps its messages; a *side effect* is kept; a *historical artifact* is carried only after asking the owner; a *design note* is for the build, below.

| ID | Name | Class | Rule | Confidence | Evidence |
|---|---|---|---|---|---|
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
| UP-BR-091 | Replace customer dataset placeholder throughout member | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<KSDSCUS>' in the member being customised with the customer data file name the installer set up (KSDSCUS). | medium | base/exec/mac1.rexx:14, base/exec/mac1.rexx:48, base/exec/cust1.rexx:55, base/exec/cust1.rexx:66 |
| UP-BR-092 | Substitute COBOL library qualifier placeholders | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<COBOLHLQ>' in the member being customised with the site's COBOL compiler library qualifier (COBOLHLQ). | medium | base/exec/mac1.rexx:9, base/exec/mac1.rexx:20, base/exec/cust1.rexx:12, base/exec/cust1.rexx:35 |
| UP-BR-093 | Replace WSIM qualifier placeholder throughout member | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<WSIMHLQ>' in the member being customised with the site's workload simulator library qualifier (WSIMHLQ). | medium | base/exec/mac1.rexx:12, base/exec/mac1.rexx:40, base/exec/cust1.rexx:21, base/exec/cust1.rexx:38 |
| UP-BR-094 | Replace user qualifier placeholders in member | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<USRHLQ>' in the member being customised with the installing user's data set qualifier (USRHLQ). | medium | base/exec/mac1.rexx:9, base/exec/mac1.rexx:19, base/exec/cust1.rexx:11, base/exec/cust1.rexx:35 |
| UP-BR-095 | Replace placeholder throughout edited member | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<WSIMWSX>' in the member being customised with the name of the GenApp workload simulator script library (WSIMWSX); a member without the placeholder is left as it is. | medium | base/exec/mac1.rexx:15, base/exec/mac1.rexx:53, base/exec/cust1.rexx:53, base/exec/cust1.rexx:61 |
| UP-BR-096 | Replace authorization identifier placeholders | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<SQLID>' in the member being customised with the Db2 SQL authorisation ID set for the installation (SQLID). | medium | base/exec/mac1.rexx:10, base/exec/mac1.rexx:25, base/exec/cust1.rexx:16, base/exec/cust1.rexx:36 |
| UP-BR-097 | Substitute management-component prefix placeholder | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<CPSMHLQ>' in the member being customised with the site's CICSPlex SM library qualifier (CPSMHLQ). | medium | base/exec/mac1.rexx:9, base/exec/mac1.rexx:17, base/exec/cust1.rexx:8, base/exec/cust1.rexx:35 |
| UP-BR-098 | Substitute character-set placeholder everywhere | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<DB2CCSID>' in the member being customised with the Db2 coded character set ID set for the installation (DB2CCSID). | medium | base/exec/mac1.rexx:10, base/exec/mac1.rexx:28, base/exec/cust1.rexx:19, base/exec/cust1.rexx:36 |
| UP-BR-099 | Replace plan placeholder throughout member | design note | THE installation customisation macro SHALL replace every occurrence of the placeholder '<DB2PLAN>' in the member being customised with the Db2 plan name set for the installation (DB2PLAN). | medium | base/exec/mac1.rexx:10, base/exec/mac1.rexx:29, base/exec/cust1.rexx:20, base/exec/cust1.rexx:36 |
| UP-BR-100 | Substitute placeholder with simulator qualifier | historical artifact | THE installation customisation macro SHALL replace every occurrence of the placeholder '<PDSMACP>' with the workload simulator library qualifier (WSIMHLQ), not with a map copybook library name; no supplied install member contains this placeholder, so the step changes nothing. | medium | base/exec/mac1.rexx:13, base/exec/mac1.rexx:42, base/exec/cust1.rexx:49, base/exec/cust1.rexx:65 |
| UP-BR-101 | Replace placeholder with installation qualifier | historical artifact | THE installation customisation macro SHALL replace every occurrence of the placeholder '<PDSDBRM>' with the workload simulator library qualifier (WSIMHLQ), not with the DBRM library name; no supplied install member contains this placeholder, so the step changes nothing. | medium | base/exec/mac1.rexx:13, base/exec/mac1.rexx:41, base/exec/cust1.rexx:48, base/exec/cust1.rexx:65 |
| UP-BR-102 | Replace simulator placeholder throughout member | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<WSIMSTL>' with the WSim product high-level qualifier (WSIMHLQ), not with the GenApp WSim data set name. | medium | base/exec/mac1.rexx:12-13, base/exec/mac1.rexx:46, base/exec/cust1.rexx:21, base/exec/cust1.rexx:53 |
| UP-BR-103 | Substitute application region name placeholder | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<AORAPPL>' with the configured application-owning region application name (AORAPPL). | medium | base/exec/mac1.rexx:11, base/exec/mac1.rexx:31, base/exec/cust1.rexx:24 |
| UP-BR-104 | Replace all placeholder tokens in member | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<WSIMLGX>' with the unquoted name of the GenApp WSim log data set (WSIMLGX). | medium | base/exec/mac1.rexx:15, base/exec/mac1.rexx:55, base/exec/cust1.rexx:52, base/exec/cust1.rexx:60 |
| UP-BR-105 | Substitute database qualifier placeholders in member | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<DB2HLQ>' with the configured Db2 high-level qualifier (DB2HLQ). | medium | base/exec/mac1.rexx:9, base/exec/mac1.rexx:21, base/exec/cust1.rexx:14 |
| UP-BR-106 | Substitute policy dataset placeholder in member | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<KSDSPOL>' with the name of the policy load data set (KSDSPOL). | medium | base/exec/mac1.rexx:14, base/exec/mac1.rexx:47, base/exec/cust1.rexx:56 |
| UP-BR-107 | Replace library placeholder with installation name | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<DBRMLIX>' with the unquoted name of the GenApp Db2 DBRM library (DBRMLIX). | medium | base/exec/mac1.rexx:14, base/exec/mac1.rexx:52, base/exec/cust1.rexx:48, base/exec/cust1.rexx:59 |
| UP-BR-108 | Substitute licence placeholder in member | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<CICSLIC>' with the configured name of the CICS licence data set (CICSLIC). | medium | base/exec/mac1.rexx:9, base/exec/mac1.rexx:18, base/exec/cust1.rexx:9 |
| UP-BR-109 | Replace CSD name placeholder | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<CSDNAME>' with the configured CICS system definition (CSD) data set name (CSDNAME). | medium | base/exec/mac1.rexx:10, base/exec/mac1.rexx:23, base/exec/cust1.rexx:10 |
| UP-BR-110 | Replace wui application placeholder | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<WUIAPPL>' with the configured CICSPlex SM web user interface application name (WUIAPPL). | medium | base/exec/mac1.rexx:12, base/exec/mac1.rexx:38, base/exec/cust1.rexx:31 |
| UP-BR-111 | Replace map copybook placeholder throughout member | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<MAPCOPX>' with the unquoted name of the GenApp map copybook library (MAPCOPX). | medium | base/exec/mac1.rexx:14, base/exec/mac1.rexx:51, base/exec/cust1.rexx:49, base/exec/cust1.rexx:58 |
| UP-BR-112 | Substitute cmas application name placeholder | design note | WHEN a GenApp installation member is customised, THE installation customisation macro SHALL replace every occurrence of the placeholder '<CMASAPPL>' with the configured CICSPlex SM address space (CMAS) application name (CMASAPPL). | medium | base/exec/mac1.rexx:12, base/exec/mac1.rexx:36, base/exec/cust1.rexx:29 |
| UP-BR-113 | Substitute data region system identifier | design note | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<DORSYSID>' with the data-owning region system identifier the installer set (DORSYSID, shipped as 'DOR1'). | medium | base/exec/mac1.rexx:11, base/exec/mac1.rexx:35, base/exec/mac1.rexx:58-62, base/exec/cust1.rexx:28 |
| UP-BR-114 | Substitute message library qualifier placeholder | historical artifact | WHEN an installation member is customised, THE installation customisation edit macro (MAC1) SHALL replace every occurrence of '<PDSMSGS>' with the Workload Simulator product qualifier (WSIMHLQ, shipped as 'PP.WSIM.V110'), not with the GenApp messages library name; no shipped member contains this placeholder. | medium | base/exec/mac1.rexx:13, base/exec/mac1.rexx:44, base/exec/cust1.rexx:21, base/exec/cust1.rexx:51 |

### Worked examples

- UP-BR-095: member text = no '<WSIMWSX>' present → Text is unchanged by this step
- UP-BR-102: member text = DSN=<WSIMSTL>; WSim high-level qualifier = PP.WSIM.V110 → The member text becomes DSN=PP.WSIM.V110
- UP-BR-103: member text = APPLID=<AORAPPL>; AOR application name = IYI0AOR1 → The member text becomes APPLID=IYI0AOR1
- UP-BR-104: member text = LOG=<WSIMLGX>; GenApp data set prefix = userid.GENAPP → The member text becomes LOG=userid.GENAPP.LOG
- UP-BR-105: member text = DSN=<DB2HLQ>.SDSNLOAD; Db2 high-level qualifier = SYS2.DB2.V12 → The member text becomes DSN=SYS2.DB2.V12.SDSNLOAD
- UP-BR-106: member text = DSN=<KSDSPOL>; GenApp data set prefix = userid.GENAPP → The member text becomes DSN=userid.GENAPP.KSDSPOLY.TXT
- UP-BR-107: member text = DSN=<DBRMLIX>; GenApp data set prefix = userid.GENAPP → The member text becomes DSN=userid.GENAPP.DBRMLIB
- UP-BR-108: member text = DSN=<CICSLIC>; CICS licence data set = CTS540.CICS710.LIC → The member text becomes DSN=CTS540.CICS710.LIC
- UP-BR-109: member text = DFHCSD DD DSN=<CSDNAME>; CSD data set name = userid.GENAPP.DFHCSD → The member text becomes DFHCSD DD DSN=userid.GENAPP.DFHCSD
- UP-BR-110: member text = APPLID=<WUIAPPL>; WUI application name = IYI0WUI → The member text becomes APPLID=IYI0WUI
- UP-BR-111: member text = SYSLIB DD DSN=<MAPCOPX>; GenApp data set prefix = userid.GENAPP → The member text becomes SYSLIB DD DSN=userid.GENAPP.MAPCOPY
- UP-BR-112: member text = APPLID=<CMASAPPL>; CMAS application name = IYI0CMAS → The member text becomes APPLID=IYI0CMAS
- UP-BR-113: member line = SYSIDNT=<DORSYSID>; DORSYSID = DOR1 → The customised copy of the member contains SYSIDNT=DOR1.
- UP-BR-114: member line = DSN=<PDSMSGS>; WSIMHLQ = PP.WSIM.V110 → The customised copy contains DSN=PP.WSIM.V110.

## Decision tables

None.

## Design notes

- UP-BR-080: Template substitution: every '<LOADX>' is replaced with the GenApp load library name, which is the installation qualifier followed by '.LOAD'. Derive the value from the one qualifier setting rather than asking for it separately.
- UP-BR-081: Template substitution: every '<AORSYSID>' is replaced with the application-owning region system identifier from the site configuration.
- UP-BR-082: Template substitution: every '<DB2RUN>' is replaced with the configured database run library value from the site configuration.
- UP-BR-083: Template substitution: every '<TORAPPL>' is replaced with the terminal-owning region application identifier from the site configuration.
- UP-BR-084: Template substitution: every '<SOURCEX>' is replaced with the GenApp source library name, which is the installation qualifier followed by '.SRC'. Derive the value from the qualifier setting.
- UP-BR-085: Template substitution: every '<TORSYSID>' is replaced with the terminal-owning region system identifier from the site configuration.
- UP-BR-086: Template substitution: every '<ZFSHOME>' is replaced with the configured file-system home directory.
- UP-BR-087: Template substitution: every '<DB2DBID>' is replaced with the configured database name.
- UP-BR-088: Template substitution: every '<WSIMMSX>' is replaced with the GenApp message-text library name, which is the installation qualifier followed by '.MSGTXT'. Derive the value from the qualifier setting.
- UP-BR-089: Template substitution: every '<DORAPPL>' is replaced with the data-owning region application identifier from the site configuration.
- UP-BR-090: Template substitution: every '<CICSHLQ>' is replaced with the configured transaction-server library prefix.
- UP-BR-091: Template substitution: every '<KSDSCUS>' is replaced with the customer data file name the installer set up.
- UP-BR-092: Template substitution: every '<COBOLHLQ>' is replaced with the site's COBOL compiler library qualifier.
- UP-BR-093: Template substitution: every '<WSIMHLQ>' is replaced with the site's workload simulator library qualifier (shipped as 'PP.WSIM.V110'). Several other placeholders reuse this same value.
- UP-BR-094: Template substitution: every '<USRHLQ>' is replaced with the installing user's data set qualifier.
- UP-BR-095: Template substitution: every '<WSIMWSX>' is replaced with the name of the GenApp workload simulator script library. A template without the placeholder passes through unchanged.
- UP-BR-096: Template substitution: every '<SQLID>' is replaced with the database SQL authorisation ID set for the installation.
- UP-BR-097: Template substitution: every '<CPSMHLQ>' is replaced with the site's CICSPlex SM library qualifier.
- UP-BR-098: Template substitution: every '<DB2CCSID>' is replaced with the database coded character set ID set for the installation.
- UP-BR-099: Template substitution: every '<DB2PLAN>' is replaced with the database plan name set for the installation.
- UP-BR-102: Template substitution: every '<WSIMSTL>' is replaced with the WSim product high-level qualifier (WSIMHLQ), not with the GenApp WSim data set name. Keep that mapping unless the owner decides otherwise.
- UP-BR-103: Template substitution: every '<AORAPPL>' is replaced with the configured application-owning region application name.
- UP-BR-104: Template substitution: every '<WSIMLGX>' is replaced with the name of the GenApp WSim log data set, written without quotes.
- UP-BR-105: Template substitution: every '<DB2HLQ>' is replaced with the configured database high-level qualifier.
- UP-BR-106: Template substitution: every '<KSDSPOL>' is replaced with the name of the policy load data set.
- UP-BR-107: Template substitution: every '<DBRMLIX>' is replaced with the name of the GenApp database request module library, written without quotes.
- UP-BR-108: Template substitution: every '<CICSLIC>' is replaced with the configured name of the CICS licence data set.
- UP-BR-109: Template substitution: every '<CSDNAME>' is replaced with the configured CICS system definition data set name.
- UP-BR-110: Template substitution: every '<WUIAPPL>' is replaced with the configured CICSPlex SM web user interface application name.
- UP-BR-111: Template substitution: every '<MAPCOPX>' is replaced with the name of the GenApp map copybook library, written without quotes.
- UP-BR-112: Template substitution: every '<CMASAPPL>' is replaced with the configured CICSPlex SM address space (CMAS) application name.
- UP-BR-113: Template substitution: every '<DORSYSID>' is replaced with the data-owning region system identifier the installer set (shipped default 'DOR1'). As with every placeholder, build it as one entry in a placeholder-to-setting table read from the site configuration, and report a missing setting instead of leaving the placeholder in place.

## Open questions

- DEF-042: Is this intended? MAC1 fetches the log data set name (WSIMLOG) from the pool, but it replaces '<WSIMLOG>' with WSIMHLQ instead. Lines 41-46 do the same for '<PDSDBRM>', '<PDSMACP>', '<PDSLOAD>', '<PDSMSGS>' and '<WSIMSTL>'. This looks like a copy-and-paste slip. It does no harm today because no member uses these placeholders. (Subject-matter expert) On UP-BR-079.
- DEF-045: Is this intended? Lines 41-46 replace the library placeholders '<PDSDBRM>', '<PDSMACP>', '<PDSLOAD>', '<PDSMSGS>', '<WSIMLOG>' and '<WSIMSTL>' with the simulator qualifier (WSIMHLQ) rather than with their own library names, which are fetched at line 13 but never used. CUST1 also misspells PDSMAPC as PDSMACP when it pools the value. No template uses these placeholders today, so nothing goes wrong now, but any template that used them would get the wrong library. (Subject-matter expert) On UP-BR-100.
- DEF-046: Is this intended? '<PDSDBRM>' is replaced with the simulator qualifier (WSIMHLQ) instead of the DBRM library name that CUST1 pools under PDSDBRM. This is part of the same copy-paste pattern as lines 41-46. No template uses the placeholder today. (Subject-matter expert) On UP-BR-101.
- DEF-047: Is this intended? The placeholders '<PDSDBRM>', '<PDSMACP>', '<PDSLOAD>', '<PDSMSGS>', '<WSIMLOG>' and '<WSIMSTL>' are all replaced with the WSim product qualifier (WSIMHLQ), even though their own values are retrieved on line 13 and set in CUST1. This looks like a copy-and-paste slip, so any member that uses these placeholders gets the wrong data set name. (Subject-matter expert) On UP-BR-102.
- DEF-048: Is this intended? MAC1 replaces the placeholders '<PDSDBRM>', '<PDSMACP>', '<PDSLOAD>', '<PDSMSGS>', '<WSIMLOG>' and '<WSIMSTL>' with the Workload Simulator qualifier WSIMHLQ. It ignores the GenApp library names that CUST1 builds and passes for these same variables, and that MAC1 itself reads in. No shipped member uses these placeholders, so nothing goes wrong today, but any member that did would get the wrong data set name. (Subject-matter expert) On UP-BR-114.

## Testing

Every acceptance criterion in requirements.md is a test named by its ID (38 in all).