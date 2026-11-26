# Tasks: Customise installation members with site values (UP-C11)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] UP-C11-T1 [business-rules] Implement the business rules. Requirements: UP-REQ-F-057, UP-REQ-F-078, UP-REQ-F-079, UP-REQ-F-092. Rules: UP-BR-079, UP-BR-100, UP-BR-101, UP-BR-114.
  - Keep each business rule exactly as specified.
  - Ask the owner before carrying the historical artifacts: UP-BR-079, UP-BR-100, UP-BR-101, UP-BR-114.
- [ ] UP-C11-T2 [api] Build the service. Requirements: UP-REQ-F-058, UP-REQ-F-059, UP-REQ-F-060, UP-REQ-F-061, UP-REQ-F-062, UP-REQ-F-063, UP-REQ-F-064, UP-REQ-F-065, UP-REQ-F-066, UP-REQ-F-067, UP-REQ-F-068, UP-REQ-F-069, UP-REQ-F-070, UP-REQ-F-071, UP-REQ-F-072, UP-REQ-F-073, UP-REQ-F-074, UP-REQ-F-075, UP-REQ-F-076, UP-REQ-F-077, UP-REQ-F-080, UP-REQ-F-081, UP-REQ-F-082, UP-REQ-F-083, UP-REQ-F-084, UP-REQ-F-085, UP-REQ-F-086, UP-REQ-F-087, UP-REQ-F-088, UP-REQ-F-089, UP-REQ-F-090, UP-REQ-F-091. Rules: UP-BR-080, UP-BR-081, UP-BR-082, UP-BR-083, UP-BR-084, UP-BR-085, UP-BR-086, UP-BR-087, UP-BR-088, UP-BR-089, UP-BR-090, UP-BR-091, UP-BR-092, UP-BR-093, UP-BR-094, UP-BR-095, UP-BR-096, UP-BR-097, UP-BR-098, UP-BR-099, UP-BR-102, UP-BR-103, UP-BR-104, UP-BR-105, UP-BR-106, UP-BR-107, UP-BR-108, UP-BR-109, UP-BR-110, UP-BR-111, UP-BR-112, UP-BR-113. After: UP-C11-T1.
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
- [ ] UP-C11-T3 [test-generation] Write a test for every acceptance criterion. Requirements: UP-REQ-F-057, UP-REQ-F-058, UP-REQ-F-059, UP-REQ-F-060, UP-REQ-F-061, UP-REQ-F-062, UP-REQ-F-063, UP-REQ-F-064, UP-REQ-F-065, UP-REQ-F-066, UP-REQ-F-067, UP-REQ-F-068, UP-REQ-F-069, UP-REQ-F-070, UP-REQ-F-071, UP-REQ-F-072, UP-REQ-F-073, UP-REQ-F-074, UP-REQ-F-075, UP-REQ-F-076, UP-REQ-F-077, UP-REQ-F-078, UP-REQ-F-079, UP-REQ-F-080, UP-REQ-F-081, UP-REQ-F-082, UP-REQ-F-083, UP-REQ-F-084, UP-REQ-F-085, UP-REQ-F-086, UP-REQ-F-087, UP-REQ-F-088, UP-REQ-F-089, UP-REQ-F-090, UP-REQ-F-091, UP-REQ-F-092. Criteria: UP-C11-AC-01, UP-C11-AC-02, UP-C11-AC-03, UP-C11-AC-04, UP-C11-AC-05, UP-C11-AC-06, UP-C11-AC-07, UP-C11-AC-08, UP-C11-AC-09, UP-C11-AC-10, UP-C11-AC-11, UP-C11-AC-12, UP-C11-AC-13, UP-C11-AC-14, UP-C11-AC-15, UP-C11-AC-16, UP-C11-AC-17, UP-C11-AC-18, UP-C11-AC-19, UP-C11-AC-20, UP-C11-AC-21, UP-C11-AC-22, UP-C11-AC-23, UP-C11-AC-24, UP-C11-AC-25, UP-C11-AC-26, UP-C11-AC-27, UP-C11-AC-28, UP-C11-AC-29, UP-C11-AC-30, UP-C11-AC-31, UP-C11-AC-32, UP-C11-AC-33, UP-C11-AC-34, UP-C11-AC-35, UP-C11-AC-36, UP-C11-AC-37, UP-C11-AC-38. After: UP-C11-T1, UP-C11-T2.
  - 38 acceptance criteria, each a test named by its ID.
- [ ] UP-C11-T4 [compliance] Review the handling of security. Requirements: UP-REQ-F-057, UP-REQ-F-058, UP-REQ-F-059, UP-REQ-F-060, UP-REQ-F-061, UP-REQ-F-062, UP-REQ-F-063, UP-REQ-F-064, UP-REQ-F-065, UP-REQ-F-066, UP-REQ-F-067, UP-REQ-F-068, UP-REQ-F-069, UP-REQ-F-070, UP-REQ-F-071, UP-REQ-F-072, UP-REQ-F-073, UP-REQ-F-074, UP-REQ-F-075, UP-REQ-F-076, UP-REQ-F-077, UP-REQ-F-078, UP-REQ-F-079, UP-REQ-F-080, UP-REQ-F-081, UP-REQ-F-082, UP-REQ-F-083, UP-REQ-F-084, UP-REQ-F-085, UP-REQ-F-086, UP-REQ-F-087, UP-REQ-F-088, UP-REQ-F-089, UP-REQ-F-090, UP-REQ-F-091, UP-REQ-F-092. After: UP-C11-T1, UP-C11-T2.
  - Check storage, logs, screens and audit against the rules.
