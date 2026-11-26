# Implementation plan: Customise installation members with site values (UP-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

## Technical context

As in the constitution's *Technical context* (.specify/memory/constitution.md); the target stack is not given yet.

Runs as service.

## Constitution check

- The legacy source is read-only; data is synthetic only.
- Every requirement, rule and criterion keeps its ID in code and tests.
- This capability is draft.

## Screens

No screens: it runs as service.

## Data model

None found in the source.

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

## Decision tables

None.
