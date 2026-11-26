# aws-carddemo, modernized

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

- [ASGD-C01 Re-sequence transactions by card number](specs/asgd-01-re-sequence-transactions-by-card-number.md): draft, scheduled job
- [ASGD-C02 Load and group card-ordered transactions](specs/asgd-02-load-and-group-card-ordered-transactions.md): draft, scheduled job
- [ASGD-C03 Produce one statement per card](specs/asgd-03-produce-one-statement-per-card.md): draft, scheduled job
- [ASGD-C04 Show statement header and holder details](specs/asgd-04-show-statement-header-and-holder-details.md): draft, scheduled job
- [ASGD-C05 List card transactions and total](specs/asgd-05-list-card-transactions-and-total.md): draft, scheduled job
- [ASGD-C06 Stop the statement run on file errors](specs/asgd-06-stop-the-statement-run-on-file-errors.md): draft, scheduled job
- [ASGD-C07 Read-only statement data access](specs/asgd-07-read-only-statement-data-access.md): draft, scheduled job
- [ASGD-C08 Publish statements as PDF](specs/asgd-08-publish-statements-as-pdf.md): draft, scheduled job
- [DTPR-C01 Extract account data to output files](specs/dtpr-01-extract-account-data-to-output-files.md): final, scheduled job
- [DTPR-C02 Validate daily transactions](specs/dtpr-02-validate-daily-transactions.md): final, scheduled job
- [DTPR-C03 Post validated transactions](specs/dtpr-03-post-validated-transactions.md): final, scheduled job
- [DTPR-C04 Run daily posting and handle rejects](specs/dtpr-04-run-daily-posting-and-handle-rejects.md): final, scheduled job
- [DTPR-C05 Calculate and post monthly interest](specs/dtpr-05-calculate-and-post-monthly-interest.md): final, scheduled job
- [DTPR-C06 Produce daily transaction report](specs/dtpr-06-produce-daily-transaction-report.md): final, online and scheduled job
- [DTPR-C07 Post daily transactions and record rejects](specs/dtpr-07-post-daily-transactions-and-record-rejects.md): final, scheduled job
- [DTPR-C08 Calculate monthly interest as system transactions](specs/dtpr-08-calculate-monthly-interest-as-system-transactions.md): final, scheduled job
- [DTPR-C09 Consolidate transactions into the transaction master](specs/dtpr-09-consolidate-transactions-into-the-transaction-mast.md): final, scheduled job
- [DTPR-C10 Back up the transaction master](specs/dtpr-10-back-up-the-transaction-master.md): final, scheduled job
- [DTPR-C11 Set up the transaction master and its timestamp index](specs/dtpr-11-set-up-the-transaction-master-and-its-timestamp-in.md): final, scheduled job
- [DTPR-C12 Load disclosure group and category balance masters](specs/dtpr-12-load-disclosure-group-and-category-balance-masters.md): final, scheduled job
- [DTPR-C13 Print the transaction category balance report](specs/dtpr-13-print-the-transaction-category-balance-report.md): final, scheduled job
- [DTPR-C14 Produce account extracts from the account master](specs/dtpr-14-produce-account-extracts-from-the-account-master.md): final, scheduled job
- [DTPR-C15 Extract transactions for a reporting period](specs/dtpr-15-extract-transactions-for-a-reporting-period.md): final, scheduled job
- [DTPR-C16 Run the transaction report job](specs/dtpr-16-run-the-transaction-report-job.md): final, scheduled job
- [DTPR-C17 Print the daily transaction report with totals](specs/dtpr-17-print-the-daily-transaction-report-with-totals.md): final, scheduled job
- [OATM-C01 Find the account to update](specs/oatm-01-find-the-account-to-update.md): final, online
- [OATM-C02 View account and customer details for update](specs/oatm-02-view-account-and-customer-details-for-update.md): final, online
- [OATM-C03 Capture entered changes](specs/oatm-03-capture-entered-changes.md): final, online
- [OATM-C04 Validate changed account and customer fields](specs/oatm-04-validate-changed-account-and-customer-fields.md): final, online
- [OATM-C05 Validate account and customer dates](specs/oatm-05-validate-account-and-customer-dates.md): final, online
- [OATM-C06 Confirm and save the account update](specs/oatm-06-confirm-and-save-the-account-update.md): final, online
- [OATM-C07 Select an account to update](specs/oatm-07-select-an-account-to-update.md): final, online
- [OATM-C08 Detect changes before validating](specs/oatm-08-detect-changes-before-validating.md): final, online
- [OATM-C09 Validate customer name and address](specs/oatm-09-validate-customer-name-and-address.md): final, online
- [OATM-C10 Validate customer phone numbers](specs/oatm-10-validate-customer-phone-numbers.md): final, online
- [OATM-C11 Validate identity and credit details](specs/oatm-11-validate-identity-and-credit-details.md): final, online
- [OATM-C12 Validate account flags and EFT account](specs/oatm-12-validate-account-flags-and-eft-account.md): final, online
- [OATM-C13 Save confirmed account and customer changes](specs/oatm-13-save-confirmed-account-and-customer-changes.md): final, online
- [OATM-C14 Navigate the account update screen](specs/oatm-14-navigate-the-account-update-screen.md): final, online
- [OATM-C15 Update account details with validation and confirmation](specs/oatm-15-update-account-details-with-validation-and-confirm.md): final, online
- [OATM-C16 Validate and look up an account for viewing](specs/oatm-16-validate-and-look-up-an-account-for-viewing.md): final, online
- [OATM-C17 Display account and customer details](specs/oatm-17-display-account-and-customer-details.md): final, online
- [OATM-C18 Navigate the account view screen](specs/oatm-18-navigate-the-account-view-screen.md): final, online
- [OATM-C19 Request a bill payment](specs/oatm-19-request-a-bill-payment.md): final, online
- [OATM-C20 Post a full-balance bill payment](specs/oatm-20-post-a-full-balance-bill-payment.md): final, online
- [OATM-C21 Set report period for transaction reports](specs/oatm-21-set-report-period-for-transaction-reports.md): final, online
- [OATM-C22 Reach and move around the transaction report screen](specs/oatm-22-reach-and-move-around-the-transaction-report-scree.md): final, online
- [OATM-C23 Choose a report type and a valid custom period](specs/oatm-23-choose-a-report-type-and-a-valid-custom-period.md): final, online
- [OATM-C24 Confirm and submit a transaction report for printing](specs/oatm-24-confirm-and-submit-a-transaction-report-for-printi.md): final, online
- [OATM-C25 Browse and page through the transaction list](specs/oatm-25-browse-and-page-through-the-transaction-list.md): final, online
- [OATM-C26 Select a transaction from the list to view its details](specs/oatm-26-select-a-transaction-from-the-list-to-view-its-det.md): final, online
- [OATM-C27 Transaction list access and session handling](specs/oatm-27-transaction-list-access-and-session-handling.md): final, online
- [OATM-C28 Look up a single transaction](specs/oatm-28-look-up-a-single-transaction.md): final, online
- [OATM-C29 View a single transaction](specs/oatm-29-view-a-single-transaction.md): final, online
- [OATM-C30 Open and navigate the Add Transaction screen](specs/oatm-30-open-and-navigate-the-add-transaction-screen.md): final, online
- [OATM-C31 Identify the account and card for a new transaction](specs/oatm-31-identify-the-account-and-card-for-a-new-transactio.md): final, online
- [OATM-C32 Validate new transaction details](specs/oatm-32-validate-new-transaction-details.md): final, online
- [OATM-C33 Record a confirmed new transaction](specs/oatm-33-record-a-confirmed-new-transaction.md): final, online
- [OATM-C34 Confirm a transaction before it is added](specs/oatm-34-confirm-a-transaction-before-it-is-added.md): final, online
- [OATM-C35 Validate a date against a format mask](specs/oatm-35-validate-a-date-against-a-format-mask.md): final, service
- [CCLDV-C01 Browse and page the card list](specs/ccldv-01-browse-and-page-the-card-list.md): draft, online
- [CCLDV-C02 Filter the card list by account and card number](specs/ccldv-02-filter-the-card-list-by-account-and-card-number.md): draft, online
- [CCLDV-C03 Select a card to view or update](specs/ccldv-03-select-a-card-to-view-or-update.md): draft, online
- [CCLDV-C04 Search and view card details](specs/ccldv-04-search-and-view-card-details.md): draft, online
- [CCLDV-C05 Enter and leave the card detail screen](specs/ccldv-05-enter-and-leave-the-card-detail-screen.md): draft, online
- [CCLDV-C06 Detect unchanged card details on update](specs/ccldv-06-detect-unchanged-card-details-on-update.md): draft, online
- [CCLDV-C07 Find and show a card for update](specs/ccldv-07-find-and-show-a-card-for-update.md): draft, online
- [CCLDV-C08 Edit and validate card details](specs/ccldv-08-edit-and-validate-card-details.md): draft, online
- [CCLDV-C09 Confirm and save card changes](specs/ccldv-09-confirm-and-save-card-changes.md): draft, online
- [CCLDV-C10 Leave or restart card update](specs/ccldv-10-leave-or-restart-card-update.md): draft, online
- [CCLDV-C11 Save card changes](specs/ccldv-11-save-card-changes.md): draft, online
- [CPBM-C01 Export complete customer profiles for branch migration](specs/cpbm-01-export-complete-customer-profiles-for-branch-migra.md): draft, scheduled job
- [CPBM-C02 Carry sensitive customer and card data in the export](specs/cpbm-02-carry-sensitive-customer-and-card-data-in-the-expo.md): draft, scheduled job
- [CPBM-C03 Report export reconciliation counts](specs/cpbm-03-report-export-reconciliation-counts.md): draft, service
- [CPBM-C04 Stop the export on any file error](specs/cpbm-04-stop-the-export-on-any-file-error.md): draft, scheduled job
- [CPBM-C05 Import and split the migration file into target files](specs/cpbm-05-import-and-split-the-migration-file-into-target-fi.md): draft, scheduled job
- [CPBM-C06 Log unknown record types during import](specs/cpbm-06-log-unknown-record-types-during-import.md): draft, scheduled job
- [CPBM-C07 Report import run statistics](specs/cpbm-07-report-import-run-statistics.md): draft, scheduled job
- [CPBM-C08 Abort the import on any file failure](specs/cpbm-08-abort-the-import-on-any-file-failure.md): draft, scheduled job
- [MDFI-C01 Load account master](specs/mdfi-01-load-account-master.md): draft, scheduled job
- [MDFI-C02 Load card master and its account index](specs/mdfi-02-load-card-master-and-its-account-index.md): draft, scheduled job
- [MDFI-C03 Refresh customer master](specs/mdfi-03-refresh-customer-master.md): draft, scheduled job
- [MDFI-C04 Load card cross-reference master and its account index](specs/mdfi-04-load-card-cross-reference-master-and-its-account-i.md): draft, scheduled job
- [TTRDM-C01 Batch maintenance of transaction types](specs/ttrdm-01-batch-maintenance-of-transaction-types.md): draft, scheduled job
- [TTRDM-C02 Enter and leave the transaction type list](specs/ttrdm-02-enter-and-leave-the-transaction-type-list.md): draft, online
- [TTRDM-C03 Page through transaction types](specs/ttrdm-03-page-through-transaction-types.md): draft, online
- [TTRDM-C04 Filter the transaction type list](specs/ttrdm-04-filter-the-transaction-type-list.md): draft, online
- [TTRDM-C05 Update transaction type descriptions from the list](specs/ttrdm-05-update-transaction-type-descriptions-from-the-list.md): draft, online
- [TTRDM-C06 Access to transaction type maintenance](specs/ttrdm-06-access-to-transaction-type-maintenance.md): draft, online
- [TTRDM-C07 Filter the transaction type list](specs/ttrdm-07-filter-the-transaction-type-list.md): draft, online
- [TTRDM-C08 Mark a list row for update or delete](specs/ttrdm-08-mark-a-list-row-for-update-or-delete.md): draft, online
- [TTRDM-C09 Confirm and apply a list update or delete](specs/ttrdm-09-confirm-and-apply-a-list-update-or-delete.md): draft, online
- [TTRDM-C10 Navigate from the transaction type list](specs/ttrdm-10-navigate-from-the-transaction-type-list.md): draft, online
- [TTRDM-C11 Look up a transaction type to maintain](specs/ttrdm-11-look-up-a-transaction-type-to-maintain.md): draft, online
- [TTRDM-C12 Show maintenance screen values and messages](specs/ttrdm-12-show-maintenance-screen-values-and-messages.md): draft, online
- [TTRDM-C13 Detect changes to a fetched transaction type](specs/ttrdm-13-detect-changes-to-a-fetched-transaction-type.md): draft, online
- [TTRDM-C14 Cancel a pending maintenance change](specs/ttrdm-14-cancel-a-pending-maintenance-change.md): draft, online
- [TTRDM-C15 Exit the maintenance screen](specs/ttrdm-15-exit-the-maintenance-screen.md): draft, online
- [TTRDM-C16 Find a transaction type to maintain](specs/ttrdm-16-find-a-transaction-type-to-maintain.md): draft, online
- [TTRDM-C17 Change a transaction type description](specs/ttrdm-17-change-a-transaction-type-description.md): draft, online
- [TTRDM-C18 Add a new transaction type](specs/ttrdm-18-add-a-new-transaction-type.md): draft, online
- [TTRDM-C19 Delete a transaction type](specs/ttrdm-19-delete-a-transaction-type.md): draft, online
- [TTRDM-C20 Control maintenance screen keys and flow](specs/ttrdm-20-control-maintenance-screen-keys-and-flow.md): draft, online
- [TTRDM-C21 Maintain transaction types in batch](specs/ttrdm-21-maintain-transaction-types-in-batch.md): draft, scheduled job
- [TTRDM-C22 Set up reference data backups](specs/ttrdm-22-set-up-reference-data-backups.md): draft, scheduled job
- [TTRDM-C23 Extract transaction types and categories to files](specs/ttrdm-23-extract-transaction-types-and-categories-to-files.md): draft, scheduled job
- [TTRDM-C24 Load reference data into keyed files](specs/ttrdm-24-load-reference-data-into-keyed-files.md): draft, scheduled job
- [UP-C01 Build screen map copybooks](specs/up-01-build-screen-map-copybooks.md): draft, scheduled job
- [UP-C02 List card master records](specs/up-02-list-card-master-records.md): draft, scheduled job
- [UP-C03 List card cross-reference records](specs/up-03-list-card-cross-reference-records.md): draft, scheduled job
- [UP-C04 List customer records](specs/up-04-list-customer-records.md): draft, scheduled job
- [UP-C05 Verify daily transaction cards and accounts](specs/up-05-verify-daily-transaction-cards-and-accounts.md): draft, service
- [UP-C06 Build and deploy online programs](specs/up-06-build-and-deploy-online-programs.md): draft, scheduled job
- [UP-C07 Convert date formats](specs/up-07-convert-date-formats.md): draft, scheduled job
- [UP-C08 Pause a batch job](specs/up-08-pause-a-batch-job.md): draft, scheduled job
- [UP-C09 Retain dataset generations](specs/up-09-retain-dataset-generations.md): draft, scheduled job
- [UP-C10 List the CardDemo dataset catalog](specs/up-10-list-the-carddemo-dataset-catalog.md): draft, scheduled job
- [UP-C11 Read transactions by processed timestamp](specs/up-11-read-transactions-by-processed-timestamp.md): draft, scheduled job
- [CAFM-C01 Purge expired pending authorizations](specs/cafm-01-purge-expired-pending-authorizations.md): draft, scheduled job
- [CAFM-C02 Answer account inquiry requests from the queue](specs/cafm-02-answer-account-inquiry-requests-from-the-queue.md): draft, online
- [CAFM-C03 Answer system date requests from the queue](specs/cafm-03-answer-system-date-requests-from-the-queue.md): draft, online
- [CAFM-C04 Receive and prepare card authorization requests](specs/cafm-04-receive-and-prepare-card-authorization-requests.md): draft, online
- [CAFM-C05 Decide and reply to card authorization requests](specs/cafm-05-decide-and-reply-to-card-authorization-requests.md): draft, online
- [CAFM-C06 Decide a card authorization request](specs/cafm-06-decide-a-card-authorization-request.md): draft, online
- [CAFM-C07 Record pending authorization summary and detail](specs/cafm-07-record-pending-authorization-summary-and-detail.md): draft, online
- [CAFM-C08 Log errors and stop on critical failures](specs/cafm-08-log-errors-and-stop-on-critical-failures.md): draft, online
- [CAFM-C09 Inquire on an account's pending authorizations](specs/cafm-09-inquire-on-an-account-s-pending-authorizations.md): draft, online
- [CAFM-C10 Page through an account's pending authorizations](specs/cafm-10-page-through-an-account-s-pending-authorizations.md): draft, online
- [CAFM-C11 Select an authorization for detail](specs/cafm-11-select-an-authorization-for-detail.md): draft, online
- [CAFM-C12 View authorization detail and mark fraud](specs/cafm-12-view-authorization-detail-and-mark-fraud.md): draft, online
- [CAFM-C13 View pending authorization details](specs/cafm-13-view-pending-authorization-details.md): draft, online
- [CAFM-C14 Navigate the authorization detail screen](specs/cafm-14-navigate-the-authorization-detail-screen.md): draft, online
- [CAFM-C15 Mark or unmark an authorization as fraud](specs/cafm-15-mark-or-unmark-an-authorization-as-fraud.md): draft, online
- [CAFM-C16 Record fraud action in the fraud register](specs/cafm-16-record-fraud-action-in-the-fraud-register.md): draft, online
- [CAFM-C17 Unload the pending authorization database](specs/cafm-17-unload-the-pending-authorization-database.md): draft, scheduled job
- [CAFM-C18 Load pending authorizations into the database](specs/cafm-18-load-pending-authorizations-into-the-database.md): draft, scheduled job
- [CAFM-C19 Load pending authorization summaries](specs/cafm-19-load-pending-authorization-summaries.md): draft, scheduled job
- [CAFM-C20 Unload all pending authorizations](specs/cafm-20-unload-all-pending-authorizations.md): draft, scheduled job
- [CAFM-C21 Run the unload jobs and manage unload files](specs/cafm-21-run-the-unload-jobs-and-manage-unload-files.md): draft, scheduled job
- [SOM-C01 Register online CardDemo programs and transactions](specs/som-01-register-online-carddemo-programs-and-transactions.md): draft, scheduled job
- [SOM-C02 Navigate the Admin Menu](specs/som-02-navigate-the-admin-menu.md): draft, online
- [SOM-C03 Navigate the Main Menu with access control](specs/som-03-navigate-the-main-menu-with-access-control.md): draft, online
- [SOM-C04 Send the CardDemo test file by FTP](specs/som-04-send-the-carddemo-test-file-by-ftp.md): draft, scheduled job
- [SOM-C05 Back up and distribute the FTP test file](specs/som-05-back-up-and-distribute-the-ftp-test-file.md): draft, scheduled job
- [SOM-C06 Authorize online transaction under the card security profile](specs/som-06-authorize-online-transaction-under-the-card-securi.md): draft, scheduled job
- [USPM-C01 Sign on to CardDemo](specs/uspm-01-sign-on-to-carddemo.md): draft, online
- [USPM-C02 Browse the user list](specs/uspm-02-browse-the-user-list.md): draft, online
- [USPM-C03 Select a user to update or delete](specs/uspm-03-select-a-user-to-update-or-delete.md): draft, online
- [USPM-C04 Add a new user](specs/uspm-04-add-a-new-user.md): draft, online
- [USPM-C05 Look up and update a user](specs/uspm-05-look-up-and-update-a-user.md): draft, online
- [USPM-C06 Open the User Update screen and look up a user](specs/uspm-06-open-the-user-update-screen-and-look-up-a-user.md): draft, online
- [USPM-C07 Save changes to a user profile](specs/uspm-07-save-changes-to-a-user-profile.md): draft, online
- [USPM-C08 Delete a user](specs/uspm-08-delete-a-user.md): draft, online
- [USPM-C09 Seed and load the user security file](specs/uspm-09-seed-and-load-the-user-security-file.md): draft, scheduled job
