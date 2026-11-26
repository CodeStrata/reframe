# genapp, modernized

Build the modernized application from the specifications here. Each capability's specification is in `specs/`; the build tasks, each for a role, are in `tasks.md`; the prototype in `ui-reference/index.html` is the UI to build to; the data contracts are in `data-contracts.md`; `traceability.md` takes every ID back to the legacy source.

## Target stack

- Front end: [FILL IN: front end, for example React with TypeScript]
- Back end: [FILL IN: back end, for example Java 21 with Spring Boot]
- Data: [FILL IN: data store, for example PostgreSQL]

**Not given yet.** Give it with `reframe design --stack "<front end>; <back end>; <data>"` and write the package again, so the data contracts get the stack's types; Reframe never chooses a stack. Until then, build nothing that depends on it.

### Target architecture

- Versions: [FILL IN: language, framework and runtime versions]
- Build and dependencies: [FILL IN: build tool, package manager, repository layout]
- Testing: [FILL IN: unit, integration and end-to-end test frameworks, and the command that runs them]
- Hosting and deployment: [FILL IN: where it runs, environments, CI/CD]
- Security: [FILL IN: authentication, authorization, secrets handling]
- Integration: [FILL IN: the systems it calls or is called by, messaging, file transfers]
- Non-functional needs: [FILL IN: response times, volumes, availability, batch windows, retention]

Or put these in `target-architecture.md` in the design context folder and write the package again with `--context`.

## Conventions

- Keep every ID: name the requirement and rule IDs in a comment where they are implemented, and each acceptance criterion's ID in its test.
- A business rule is kept exactly; formatting may be restyled; error handling keeps its messages word for word; ask before carrying a historical artifact.
- The legacy source is read-only and only for reference. Use synthetic data only, never production or personal data.
- Build a draft capability only after the owner confirms it; build final ones first.
- Money is an exact decimal, never a float; keep each field's precision from the data contracts.
- The screens follow the prototype in the Claude Code form's ui-reference/ and the screen specifications; meet WCAG 2.2 AA.

## House conventions

- Coding standards: [FILL IN: style guide, linters and formatters]
- Naming: [FILL IN: packages, modules, classes, endpoints, tables]
- Error handling and logging: [FILL IN: exception policy, log format, what is never logged (card numbers, personal data)]
- Style reference: [FILL IN: path or link to the house's example screens and code, or its design system]
- Branching and review: [FILL IN: branch naming, pull request rules, who reviews]
- Definition of done: [FILL IN: the checks a task must pass: tests, coverage, review, security scan]

## Skills

In `.claude/skills/`: `build-capability`, `write-acceptance-tests`, `model-data-contract`, `build-screen`. Fill in their placeholders first; START-HERE.md says how.

## Capabilities

- [ADPLM-C01 Load customer and policy data stores](specs/adplm-01-load-customer-and-policy-data-stores.md): draft, scheduled job
- [ADPLM-C02 Define online files and transactions](specs/adplm-02-define-online-files-and-transactions.md): draft, scheduled job
- [ADPLM-C03 Provision the insurance database](specs/adplm-03-provision-the-insurance-database.md): draft, scheduled job
- [ADPLM-C04 Remove dependent records on deletion](specs/adplm-04-remove-dependent-records-on-deletion.md): draft, scheduled job
- [ADPLM-C05 Load sample insurance data](specs/adplm-05-load-sample-insurance-data.md): draft, scheduled job
- [ADPLM-C06 Prepare monitoring and workload simulation](specs/adplm-06-prepare-monitoring-and-workload-simulation.md): draft, scheduled job
- [ADPLM-C07 Validate and register a new policy](specs/adplm-07-validate-and-register-a-new-policy.md): draft, scheduled job
- [ADPLM-C08 Store product details for a new policy](specs/adplm-08-store-product-details-for-a-new-policy.md): draft, scheduled job
- [ADPLM-C09 Log policy add errors](specs/adplm-09-log-policy-add-errors.md): draft, scheduled job
- [ADPLM-C10 Add a policy to the policy database](specs/adplm-10-add-a-policy-to-the-policy-database.md): draft, scheduled job
- [ADPLM-C11 Record a new policy in the policy file](specs/adplm-11-record-a-new-policy-in-the-policy-file.md): draft, scheduled job
- [ADPLM-C12 Record the first application start](specs/adplm-12-record-the-first-application-start.md): draft, scheduled job
- [ADPLM-C13 Count transactions by request type and outcome](specs/adplm-13-count-transactions-by-request-type-and-outcome.md): draft, scheduled job
- [ADPLM-C14 Delete a policy](specs/adplm-14-delete-a-policy.md): draft, scheduled job
- [ADPLM-C15 Remove a deleted policy from the policy file](specs/adplm-15-remove-a-deleted-policy-from-the-policy-file.md): draft, scheduled job
- [ADPLM-C16 Pick a customer number within the control range](specs/adplm-16-pick-a-customer-number-within-the-control-range.md): draft, scheduled job
- [ADPLM-C17 Look up a customer's policy by type](specs/adplm-17-look-up-a-customer-s-policy-by-type.md): draft, scheduled job
- [ADPLM-C18 Reset the application environment](specs/adplm-18-reset-the-application-environment.md): draft, scheduled job
- [ADPLM-C19 Accept and check a policy update request](specs/adplm-19-accept-and-check-a-policy-update-request.md): draft, scheduled job
- [ADPLM-C20 Update a policy in the database with a timestamp check](specs/adplm-20-update-a-policy-in-the-database-with-a-timestamp-c.md): draft, scheduled job
- [ADPLM-C21 Synchronise the policy file after an update](specs/adplm-21-synchronise-the-policy-file-after-an-update.md): draft, scheduled job
- [CRCM-C01 Accept and check an add-customer request](specs/crcm-01-accept-and-check-an-add-customer-request.md): draft, scheduled job
- [CRCM-C02 Assign a customer number and store the new customer](specs/crcm-02-assign-a-customer-number-and-store-the-new-custome.md): draft, scheduled job
- [CRCM-C03 Copy the new customer to the customer file](specs/crcm-03-copy-the-new-customer-to-the-customer-file.md): draft, scheduled job
- [CRCM-C04 Create the new customer's security record](specs/crcm-04-create-the-new-customer-s-security-record.md): draft, scheduled job
- [CRCM-C05 Accept a customer update request](specs/crcm-05-accept-a-customer-update-request.md): draft, scheduled job
- [CRCM-C06 Update the customer's personal and contact details](specs/crcm-06-update-the-customer-s-personal-and-contact-details.md): draft, scheduled job
- [CRCM-C07 Replace the customer's record in the customer file](specs/crcm-07-replace-the-customer-s-record-in-the-customer-file.md): draft, service
- [UP-C01 Produce the simulator log listing](specs/up-01-produce-the-simulator-log-listing.md): draft, scheduled job
- [UP-C02 Translate workload simulator scripts](specs/up-02-translate-workload-simulator-scripts.md): draft, scheduled job
- [UP-C03 Look up customer details](specs/up-03-look-up-customer-details.md): draft, scheduled job
- [UP-C04 Route policy inquiries by request type](specs/up-04-route-policy-inquiries-by-request-type.md): draft, scheduled job
- [UP-C05 Report policy lookup outcomes](specs/up-05-report-policy-lookup-outcomes.md): draft, scheduled job
- [UP-C06 Return policy details](specs/up-06-return-policy-details.md): draft, scheduled job
- [UP-C07 Look up a single commercial policy](specs/up-07-look-up-a-single-commercial-policy.md): draft, scheduled job
- [UP-C08 List commercial policies by customer or postcode](specs/up-08-list-commercial-policies-by-customer-or-postcode.md): draft, scheduled job
- [UP-C09 Look up house and motor policy details](specs/up-09-look-up-house-and-motor-policy-details.md): draft, scheduled job
- [UP-C10 Accept and route policy inquiries](specs/up-10-accept-and-route-policy-inquiries.md): draft, scheduled job
- [UP-C11 Customise installation members with site values](specs/up-11-customise-installation-members-with-site-values.md): draft, service
- [UP-C12 Save customised installation members as copies](specs/up-12-save-customised-installation-members-as-copies.md): draft, service
- [UP-C13 Customise installation members with site values](specs/up-13-customise-installation-members-with-site-values.md): draft, service
- [UP2-C01 Customer add, update and menu](specs/up2-01-customer-add-update-and-menu.md): draft, online and scheduled job
- [UP2-C02 Motor policy inquire, add, delete and update](specs/up2-02-motor-policy-inquire-add-delete-and-update.md): draft, online and scheduled job
- [UP2-C03 Endowment (life) policy inquire, add, delete and update](specs/up2-03-endowment-life-policy-inquire-add-delete-and-updat.md): draft, online and scheduled job
- [UP2-C04 House policy add, delete and update](specs/up2-04-house-policy-add-delete-and-update.md): draft, online and scheduled job
- [UP2-C05 Commercial property policy inquire, add and delete](specs/up2-05-commercial-property-policy-inquire-add-and-delete.md): draft, online and scheduled job
- [DEML-C01 Accept log requests from programs and terminals](specs/deml-01-accept-log-requests-from-programs-and-terminals.md): draft, scheduled job
- [DEML-C02 Record log messages to the standard and error queues](specs/deml-02-record-log-messages-to-the-standard-and-error-queu.md): draft, service
- [TSM-C01 Self-scheduled statistics refresh](specs/tsm-01-self-scheduled-statistics-refresh.md): draft, scheduled job
- [TSM-C02 Total transaction counters by outcome and type](specs/tsm-02-total-transaction-counters-by-outcome-and-type.md): draft, scheduled job
- [TSM-C03 Publish statistics to shared queues](specs/tsm-03-publish-statistics-to-shared-queues.md): draft, scheduled job
- [TSM-C04 Business-monitor symbol list (not delivered)](specs/tsm-04-business-monitor-symbol-list-not-delivered.md): draft, scheduled job
- [WSIG-C01 Publish customer operations as web services](specs/wsig-01-publish-customer-operations-as-web-services.md): draft, scheduled job
- [WSIG-C02 Publish policy add as web services by policy type](specs/wsig-02-publish-policy-add-as-web-services-by-policy-type.md): draft, scheduled job
- [WSIG-C03 Publish policy inquiry as web services](specs/wsig-03-publish-policy-inquiry-as-web-services.md): draft, scheduled job
- [WSIG-C04 Publish policy update as web services by policy type](specs/wsig-04-publish-policy-update-as-web-services-by-policy-ty.md): draft, scheduled job
- [WSIG-C05 Publish policy number lookup as a web service](specs/wsig-05-publish-policy-number-lookup-as-a-web-service.md): draft, scheduled job
