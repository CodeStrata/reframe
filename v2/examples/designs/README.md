# Sample designs (P1-06)

Synthetic canonical designs used to prove that the design site renderer works for any application, not one ([#235](https://github.com/sknampally/reframe/issues/235)). They are invented to exercise the format. Program, map and file names are made up, and none comes from a real application or client.

| File | Kind | Goal | What it exercises |
| --- | --- | --- | --- |
| `online-preserve.json` | CICS online journey, two 3270 maps | preserve | One page per map, Enter and PF3 keys, navigation, field rules, open findings |
| `online-modernize.json` | The same journey | modernize | One task page replacing both maps, with no field or rule lost |
| `batch-only.json` | Nightly batch job and a file hand-off | preserve | No screens and no invented endpoints; a contradicted rule |
| `message-exchange.json` | MQ intake plus one HTTP status call | modernize | Message, file and HTTP interactions, an OpenAPI reference, and a rule with no source |

Render one with `python -m reframe_v2.design_site <sample.json> <out-dir>`.
