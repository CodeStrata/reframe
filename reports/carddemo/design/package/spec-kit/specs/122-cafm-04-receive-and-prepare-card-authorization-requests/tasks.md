# Tasks: Receive and prepare card authorization requests (CAFM-C04)

**Status: DRAFT**: the function is not signed off yet. Confirm with the owner before building to it.

Each task names the role that does it; the role files are in .claude/agents/.

- [ ] CAFM-C04-T1 [data] Model the data the capability reads and writes. Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051.
  - File records: CCPAUERY, CCPAURQY, CVACT01Y, CVACT03Y, CVCUS01Y (see data-contracts.md).
  - Working records it passes or builds: CCPAURLY, CIPAUDTY, CIPAUSMY.
- [ ] CAFM-C04-T2 [business-rules] Implement error handling and messages. Requirements: CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-050. Rules: CAFM-BR-046, CAFM-BR-047, CAFM-BR-049, CAFM-BR-050, CAFM-BR-052. After: CAFM-C04-T1.
  - Show every message word for word; formatting rules may be restyled to the design system.
- [ ] CAFM-C04-T3 [api] Build the services behind the screens. Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-046, CAFM-REQ-F-049, CAFM-REQ-F-051. Rules: CAFM-BR-042, CAFM-BR-043, CAFM-BR-044, CAFM-BR-045, CAFM-BR-048, CAFM-BR-051, CAFM-BR-053. After: CAFM-C04-T1, CAFM-C04-T2.
  - CAFM-BR-042: Each consumer run handles at most 501 messages (the limit of 500 is tested as 'more than'), committing after each message. Leave the remaining messages on the queue for the next start-up so one run cannot hold the queue indefinitely.
  - CAFM-BR-043: Read the request queue with a 5-second wait, and end the run when no message arrives in that time.
  - CAFM-BR-044: Provide a parser that splits the comma-delimited request into named fields and converts the amount text to an exact decimal (not floating point) transaction amount.
  - CAFM-BR-045: Look up the account record by the account id taken from the card cross-reference, and return found or not found as a flag for the decision step.
  - CAFM-BR-048: Look up the customer record by the customer id taken from the card cross-reference, and return found or not found as a flag for the decision step.
  - CAFM-BR-051: Look up the account's pending authorization summary by account id, with three outcomes: found, not found, or error. Only an error ends the task (critical 'I002'). The legacy IMS statuses blank/'FW' mean found and 'GE' means not found.
  - CAFM-BR-053: Authorization details must be read newest first. The legacy store did this with an inverted key: date = 99999 minus the YYDDD value, time = 999999999 minus (time x 1000 + milliseconds). The new store can use a descending index on the authorization timestamp, but any shared or migrated keys must keep this formula, because the purge works out an authorization's age from the inverted date.
- [ ] CAFM-C04-T4 [test-generation] Write a test for every acceptance criterion. Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051. Criteria: CAFM-C04-AC-01, CAFM-C04-AC-02, CAFM-C04-AC-03, CAFM-C04-AC-04, CAFM-C04-AC-05, CAFM-C04-AC-06, CAFM-C04-AC-07, CAFM-C04-AC-08, CAFM-C04-AC-09, CAFM-C04-AC-10, CAFM-C04-AC-11, CAFM-C04-AC-12, CAFM-C04-AC-13, CAFM-C04-AC-14, CAFM-C04-AC-15. After: CAFM-C04-T1, CAFM-C04-T2, CAFM-C04-T3.
  - 15 acceptance criteria, each a test named by its ID.
- [ ] CAFM-C04-T5 [compliance] Review the handling of card data, personal data. Requirements: CAFM-REQ-F-040, CAFM-REQ-F-041, CAFM-REQ-F-042, CAFM-REQ-F-043, CAFM-REQ-F-044, CAFM-REQ-F-045, CAFM-REQ-F-046, CAFM-REQ-F-047, CAFM-REQ-F-048, CAFM-REQ-F-049, CAFM-REQ-F-050, CAFM-REQ-F-051. After: CAFM-C04-T1, CAFM-C04-T2, CAFM-C04-T3.
  - Check storage, logs, screens and audit against the rules.
