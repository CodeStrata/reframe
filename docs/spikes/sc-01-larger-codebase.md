# Spike SC-01: a larger codebase

**Question:** which public mainframe codebase, several times CardDemo's size and with a licence that allows it, should Reframe be proven on (SC-02)?

**Answer, for the owner to choose:** no public COBOL and CICS codebase several times CardDemo's size has a licence that allows it. The one large, real system is NAV's DSF, written in PL/I. Two paths are below, with a recommendation.

Read on 26 November 2026 from GitHub's metadata (languages, file trees, licences), with nothing cloned or downloaded.

## What was found

| Codebase | What it is | Size | Licence | Usable |
|---|---|---|---|---|
| [aws-samples/aws-mainframe-modernization-carddemo](https://github.com/aws-samples/aws-mainframe-modernization-carddemo) | The baseline: credit cards, CICS, batch, VSAM, with IMS, DB2 and MQ extensions | 44 COBOL programs, 62 copybooks, 55 JCL, 21 BMS maps; 2.2 MB of COBOL | Apache-2.0 | Yes (done) |
| [cicsdev/cics-genapp](https://github.com/cicsdev/cics-genapp) | IBM's general insurance sample, CICS and DB2 | 31 programs, 13 copybooks, 29 JCL, 1 BMS; 0.4 MB | EPL-2.0 | Yes (done) |
| [IBM/Bank-of-Z](https://github.com/IBM/Bank-of-Z) | A hybrid banking sample, CICS or IMS by customer, z/OS Connect | 45 programs, 96 copybooks, 17 assembler; 1.3 MB of COBOL | Apache-2.0 | Yes |
| [navikt/DSF](https://github.com/navikt/DSF) | *Det Sentrale Folketrygdsystemet*, Norway's national insurance system, in production for 51 years (1967 to 2018) | 1,473 PL/I files, 48 MB: about 20 times CardDemo's source | MIT | Yes, once Reframe reads PL/I |
| [RocketSoftwareCOBOLandMainframe/BankDemo](https://github.com/RocketSoftwareCOBOLandMainframe/BankDemo) | Rocket's banking demo, CICS, IMS, JCL | 82 programs, 83 copybooks | Internal demonstration with Rocket products only | No |
| [sentientsergio/COBOL-Legacy-Benchmark-Suite](https://github.com/sentientsergio/COBOL-Legacy-Benchmark-Suite) | A portfolio-management system written for benchmarking LLM translation | 42 programs | None stated | No |
| [etalab/taxe-fonciere](https://github.com/etalab/taxe-fonciere) | France's property-tax computation | 6 programs, 17 copybooks | CeCILL-2.1 | Yes, but small |

Every other public COBOL repository with stars is a course, a tool, a parser or a toy.

## Two paths

**A. Three COBOL applications as one codebase, now.** CardDemo, GenApp and Bank-of-Z together:
- **Size:** about 120 programs, 2.7 times CardDemo by programs and 1.8 times by source.
- **What it proves:** CICS, IMS, DB2, batch and three unrelated business domains in one run. Reframe reads all of it today.
- **What it does not prove:** a real system's size, or the cross-application flows a real estate has.
- **Licences:** all permissive (Apache-2.0, EPL-2.0 and Apache-2.0).

**B. DSF, after Reframe reads PL/I.** This is the real proof of scale, on a system that ran a country's national insurance for 51 years.
- **What Reframe needs first:**
  - The design's inventory, flow and data contracts read COBOL, BMS and copybooks; each needs a PL/I reader (`%INCLUDE`, `DECLARE`, the PL/I procedure structure).
  - Whether Claude's code-modernization plugin handles PL/I, and whether AWS Transform does, must be checked, each in a small spike.
- **Start with a slice:** a subsystem of about five times CardDemo, then all of it.

## What a run would cost

These are rough figures, scaled from CardDemo's recorded costs by source size. They are estimates to decide with, not quotes.

| Step | CardDemo (recorded) | Path A, about 2 to 3 times | A DSF slice, about 5 times |
|---|---|---|---|
| Claude assessment | about 9 million tokens, 2 hours, on the subscription | about 20 to 30 million tokens; needs a raised agent limit and may hit the subscription's limits (a stop and `reframe resume`) | about 45 million tokens; an API key or Bedrock is the practical sign-in |
| Reconciliation, at API prices | $30 to $70 | $70 to $210 | $150 to $350 |
| Design, at API prices | $35 to $60 | $80 to $180 | $175 to $300 |
| AWS Transform | the job and the run's resources, until teardown | the same, in the owner's own AWS account | the same, if AWS Transform reads PL/I |

## Recommendation

1. **Path A now** for SC-02, with Claude only, or with both tools once the owner's own AWS account is ready. It is cheap, it uses what Reframe reads today, and it shows Reframe across three domains.
2. **Then PL/I**, as its own stories: a spike on the plugin and AWS Transform, then the PL/I readers. After that, the DSF slice as the real scale proof. PL/I support matters beyond the proof too: many banks and insurers run PL/I.

**The owner decides:** the path, and a yes to each live run with its estimate. Bedrock waits for SC-03's clearance.
