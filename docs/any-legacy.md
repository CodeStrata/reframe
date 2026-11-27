# Reframe specification: any legacy codebase (release 1.1)

The owner's direction (27 November 2026): Reframe should not be only for mainframes. It should take any legacy codebase that the tools it drives support, and give the same result: reviewed requirements and business rules, checked against the source, and a package to build from.

Status: **agreed** (27 November 2026, #464). Its stories are in [the plan](plan.md), with an issue each under epic #472, and are built on a phase branch, as [CONTRIBUTING.md](../CONTRIBUTING.md) says. It builds on release 1.0 ([release-1.md](release-1.md)) and changes nothing in it.

## 1. Goal

Someone with a legacy application in any language can, with Claude only:

1. **assess it:** what it does, as business rules, each citing its source lines;
2. **reconcile it:** every rule checked against the source code, with the evidence checked by Reframe;
3. **design from it:** final specifications with acceptance criteria and data contracts, golden datasets, an AI-DLC package and a backlog;
4. **see the screens and flows** where the application has them, in a form that suits its stack.

Mainframe stays the strongest case: the only one with two independent assessments (AWS Transform and Claude) reconciled against each other, and with exact readers for screens, flows and copybooks.

## 2. What each tool supports

| | AWS Transform | Claude's code-modernization plugin |
|---|---|---|
| **Mainframe** (COBOL, PL/I, JCL, CICS, BMS) | An assessment with business functions, requirements and business rules: what pipeline 1 reads | Assessment, map and business rules |
| **Other stacks** | It transforms code (.NET Framework to modern .NET, Java upgrades, VMware, and custom transformations) but writes no requirements or business rules to reconcile | Assessment, map and business rules for any language. Tried by its authors on Java (Jetty, JSP, Spring), PHP, Perl, Python 2, AngularJS, Rails, .NET Framework and C |

So outside the mainframe, a run is **Claude only**, the release 1.0 mode in which every Claude rule is checked against the code. If AWS Transform later writes requirements for other stacks, a second assessment can be added the way pipeline 1 was.

## 3. What is tied to the mainframe today

| Area | Tied to the mainframe | What changes |
|---|---|---|
| Snapshot, run folder, resume, publish, teardown | No | Nothing |
| Pipeline 1 (AWS Transform) | Yes, by AWS's design | Offered only for a mainframe codebase (section 5.1) |
| Pipeline 2 (Claude's plugin) | Barely: a program's name is its file's stem in capitals, as COBOL members are named | Names from the stack profile (section 5.2) |
| Pipeline 3 (the reconciliation) | In its words: the prompts speak of readers who "do not read COBOL" and of following "a PERFORM, CALL or copybook"; the source files read are a list of mainframe suffixes | Words and suffixes from the stack profile (section 5.3) |
| Pipeline 4 (the design) | **Yes:** D1 reads BMS maps, D2 follows CICS transfers, the legacy screens are drawn as 3270, D6's data contracts come from COBOL copybooks, and "runs as" looks for CICS and JCL | Readers chosen by the stack profile, with a general reader for any stack (section 5.4) |
| Specifications, package, golden datasets, backlog | No | Their words only |

## 4. The stack profile (L1-01)

After the snapshot, Reframe works out what the codebase is, with no model, and records it in `stack-profile.json` in the run folder:

- **Languages,** counted by file: by extension, and by content where an extension is shared (`.inc`, `.h`, `.prc`).
- **Its family,** from the languages that carry most of the code:

  | Family | Recognised by | Readers in 1.1 |
  |---|---|---|
  | `mainframe` | COBOL, PL/I, JCL, BMS, HLASM, CICS CSD | The exact ones that exist (BMS, CICS flow, copybooks) |
  | `java` | Java, JSP, JSF, Groovy, Kotlin, Struts or Spring configuration | General |
  | `dotnet` | C#, VB.NET, ASP.NET (`.aspx`, `.cshtml`), `web.config` | General |
  | `web-script` | PHP, Perl, Ruby, Python, classic ASP | General |
  | `front-end` | JavaScript and TypeScript applications (AngularJS and the like) | General |
  | `native` | C, C++ | General |
  | `4gl` | RPG, Natural, Progress 4GL, PowerBuilder, VB6, Delphi, Oracle Forms | General, unproven |
  | `mixed` | No family carries most of the code | General |

- **What it has,** each with the files that show it:
  - **user interface:** screen definitions, views, templates or forms;
  - **routes:** HTTP endpoints, controllers, menu or transaction definitions;
  - **jobs:** JCL, cron entries, Quartz or Spring Batch jobs, Windows tasks, batch scripts;
  - **data:** SQL DDL, ORM mappings, entity or record definitions.
- **What it is told:** `reframe run --legacy <family>` overrides the family. The guided run shows the profile and asks only when no family carries most of the code; in autonomous mode Reframe takes `mixed`.

The profile is shown by `reframe status`, carried into the reports' About section, and read by every later stage. It records the language words each prompt uses: `COBOL`, or `Java and JSP`.

## 5. Changes by pipeline

### 5.1 Pipeline 1, AWS Transform (L1-02)

- `--tools both` and `--tools aws` are offered only when the profile's family is `mainframe`. For any other family, `reframe run` stops before anything is created, with the fix: run Claude only. The guided run does not offer AWS Transform.
- Nothing else in pipeline 1 changes.

### 5.2 Pipeline 2, Claude's plugin (L1-02)

- **A program's name** comes from the profile. For the mainframe it stays the member name; for other families it is the file's path within the source (`src/main/java/org/x/OrderService.java`), so two files of the same name in different folders stay apart.
- The plugin's own commands are unchanged: they already take any language.
- The estimate and the agent limit are unchanged.

### 5.3 Pipeline 3, the reconciliation (L1-03)

- **The prompts** take their words from the profile: readers "who do not read Java", and "follow a call, an include, an import or an inherited method" in place of "a PERFORM, CALL or copybook". The rules stay in the business form ("WHEN ..., THE ... SHALL ...").
- **The source files read** are those of the profile's languages, in place of the mainframe suffixes.
- **The evidence check** is unchanged: every cited line must exist in the snapshot.
- **The accuracy audit and the expert's pack** work as they are. The pack's guide names the stack.

### 5.4 Pipeline 4, the design (L1-04 to L1-07)

**Readers.** Each design stage that reads the legacy source goes through a reader chosen by the profile:

| Stage | Mainframe reader (exists) | General reader (new) |
|---|---|---|
| D1 Screens | BMS maps, with no model | The views, pages and forms the profile found. One model step per batch of files lists each screen's fields (label, kind, validation) and actions (buttons, links, submits), each citing its lines |
| D2 Flow | CICS transfers and the CSD, with no model, and a model step for what stays open | Routes and links: controllers and route tables, form targets, redirects, menu definitions. Read with no model where a pattern settles it (an `href`, an `action`, a `@RequestMapping`, a route table), and by a model step for the rest. Every link cites its lines |
| Legacy screens | Drawn as 3270 copies | A field list per screen, with a link to its source file. No rendering of the old page in 1.1 |
| D6 Data contracts | COBOL copybooks, with no model | SQL DDL (`CREATE TABLE`, with types, keys and constraints), with no model. Entity and record classes (JPA, Entity Framework, plain classes) by a model step that cites each field's line |
| "Runs as" | CICS transactions and JCL | **Online** where a capability's rules are reached from a screen or an HTTP route; **scheduled job** from cron, Quartz, Spring Batch, Windows tasks or JCL; **service** from routes with no screen; **library** otherwise |

**The same checks for every reader.** A general reader's answer is checked as the reconciliation checks its rules: every cited line exists, every screen names a file the profile found, and every link joins two things that exist. An answer that fails is asked again once with the reason; then it is kept as unresolved, never guessed. The design page says which reader made each part.

**A codebase with no screens** (a batch system, a service, a library) is designed without them. The journeys, modern screens and prototype are left out and the page says why. The final specifications, golden datasets, package and backlog are written as today.

**Journeys, modern screens and the prototype** work from the screens and flow the reader gives them, whatever made them. The modern screen mapping maps legacy fields, whether a BMS field or a form input.

### 5.5 What follows the design (L1-08)

- The package, golden datasets, backlog and reports change only their words: "the legacy source", not "the mainframe". START-HERE names the stack.
- The golden datasets' targets are unchanged: a screen, a job or a service.

## 6. Words, README and docs (L1-08)

- **The tagline** becomes: *From legacy source to reviewed requirements, business rules and a design to build from.* Mainframe is named as the deepest case: two assessments reconciled, with exact readers.
- **The README** says what each family gets, in one table: the tools, the readers, and what is proven.
- **The guide** gets a section per family worth one, starting with the mainframe as it is.
- **The words** "mainframe", "COBOL" and "copybook" stay where they mean exactly that.

## 7. Proving it (L1-09)

- **Offline:** small synthetic fixtures for each reader and for the profile: a Java web application, a .NET one, a PHP one and a batch-only one. They are written for the tests, with no code taken from anyone.
- **Live, on the owner's yes with an estimate before each run,** and run locally. Nothing from these codebases is committed or published (the owner's decision of 26 November 2026). Two candidates the plugin's authors have already run:
  - [dotnet-architecture/eShopModernizing](https://github.com/dotnet-architecture/eShopModernizing): .NET Framework web forms and MVC, MIT, archived;
  - [mybatis/jpetstore-6](https://github.com/mybatis/jpetstore-6): Java with Stripes and JSP, Apache-2.0.
- **Done when,** on each, from `reframe run --tools claude` to `reframe design` and `reframe export`, with no stop that needs a code fix:
  - the profile is right;
  - every rule's evidence exists;
  - the screens and flow cover every view the profile found, or say why not;
  - the data contracts come from the schema or the entities;
  - the package's checks pass.
- **Recorded in this document:** the time, agents and cost of each run, and what was found and fixed.

## 8. Not in 1.1

- **AWS Transform for other stacks.** It transforms code rather than documenting it, so there is nothing to reconcile yet. Revisit if AWS adds requirements for them.
- **Exact readers beyond the mainframe** (ASP.NET, JSP and Struts, Spring MVC). The general reader comes first; an exact one is added where the live runs show it pays.
- **PL/I exact readers and the DSF codebase** ([SC-01](spikes/sc-01-larger-codebase.md)): a story of their own. PL/I is a mainframe language, so it already gets the profile and the general readers.
- **Proving the `4gl` family.** It runs on the general readers, unproven, until a codebase with a licence that allows testing is found.
- **Rendering old web pages** beside the modern screens.

## 9. Decisions for the owner

| Decision | Proposed |
|---|---|
| Release | 1.1, after 1.0 is tagged |
| The two live codebases | eShopModernizing (.NET) and JPetStore 6 (Java), run locally only |
| General reader before exact readers | Yes: one reader for every stack first, checked as rules are |
| A codebase whose family is unclear | The guided run asks; autonomous mode takes `mixed` |
| The tagline | As in section 6 |

## 10. Stories

| Story | Title | Section | Done when |
|---|---|---|---|
| L1-01 | The stack profile | 4 | `stack-profile.json` names the languages, family, screens, routes, jobs and data with the files that show them, for each test fixture; `--legacy` overrides it; status and the reports show it |
| L1-02 | Pipelines 1 and 2 by profile | 5.1, 5.2 | AWS Transform is offered only for `mainframe`, and refused before anything is made otherwise; program names follow the profile |
| L1-03 | A reconciliation in the stack's words | 5.3 | The prompts and source files come from the profile; the evidence check, the audit and the expert's pack work on a non-mainframe fixture |
| L1-04 | A design without screens | 5.4 | A batch or service fixture gets its specifications, golden datasets, package and backlog, with journeys, screens and the prototype left out and the page saying why |
| L1-05 | Screens and flow from any stack | 5.4 | The general reader lists each view's fields and actions and the routes and links between them, each citing lines and checked; patterns that settle a link need no model; what fails twice is unresolved |
| L1-06 | Data contracts from any stack | 5.4 | SQL DDL is read with no model; entity classes by a checked model step; the target stack's types apply as today |
| L1-07 | "Runs as" for any stack | 5.4 | Online, scheduled job, service or library from screens, routes and job definitions, for each fixture |
| L1-08 | Words, README and docs | 5.5, 6 | The tagline, the README's table by family, the guide and every stage's words follow section 6 |
| L1-09 | Live acceptance on two codebases | 7 | Section 7's *done when* on eShopModernizing and JPetStore 6, run locally, nothing committed, the results recorded here |

**Estimate:** about two to three weeks of build. L1-05 is the largest part; L1-01 to L1-04 and L1-08 are small. The live runs' cost is estimated before each one.
