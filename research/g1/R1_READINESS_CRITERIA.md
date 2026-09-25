# R1 engineering criteria — defined before implementation, 2026-09-26

R1 means strong model-backed baselines can execute through the same scenario interfaces with inspected live usage, reproducible model/provider settings and effective resource limits. R2 additionally needs human adjudication and a signed study freeze. Offline mocks do not establish semantic competence or live provider enforcement.

| Gate | Objective acceptance evidence |
|---|---|
| G1 | Model-backed point support inference and semantic-neighbor implementation; inspect a tiny real-model fixture trace for basic competence without computing G1 statistics |
| G2 | Raw returned usage preserved; tested normalization of input/cache/output/reasoning and unknown fields; at least one live returned usage record |
| G3 | Reservation before network dispatch, reconciliation afterward, recorded failure/overrun, subsequent calls blocked; offline adversarial tests plus tiny live stopping check |
| G4 | Full versus cached recomputation uses identical evidence; cache identity includes model/prompt/settings/schema and logs physical versus reused work; local dependency-check time counted |
| G5 | Every published-method adaptation names deviations; no reproduction claim from a mock or store-only check |
| G6 | Classical support maintenance and model-inferred point support sets share PolicyView, ledger and source prefix; query-only and support-aware rollback threats available |
| G7 | Prompt allowlist tests exclude gold, future events, case names, masks and expected answers; no verifier gets hidden executable gold |
| G8 | Versioned prompts/configs, content-addressed immutable responses, raw usage, attempt/retry IDs, optional smoke runner; actual provider smoke inspectable |
| G9 | No human forms altered, no pilot runs, no proposed uncertainty controller, no fixture hypothesis statistics |

Any missing G1/G2/G3/G8 live evidence keeps overall readiness R0 even if offline engineering passes. Current credential/resource availability is checked without printing secrets. Unavailable live tests are explicitly SKIPPED; do not install large model weights or substitute a different model to manufacture completion. Final gate assessment will be recorded after validation.

## Final engineering assessment, 2026-09-26

| Gate | Status after this phase |
|---|---|
| G1 | PARTIAL — real provider/embedding implementations and point support baselines; no observed live competence |
| G2 | PARTIAL — raw parsing/normalization tested offline; no actual provider usage sample |
| G3 | PARTIAL — all requested cumulative caps tested before dispatch and after reconciliation; no live stop trace; revision-credit release unresolved |
| G4 | PARTIAL — deterministic incremental replay cache audited, dependency work counted, model response cache tested; live regeneration costs and final multi-arm cache parity not validated |
| G5 | PASS for explicit fidelity labeling and CUPMem/rollback inclusion decisions; no new published reproduction claimed |
| G6 | OFFLINE PASS — classical/model point policies share PolicyView/run/Ledger; B9 and current-only B10 executable; broader historical/readout integration remains |
| G7 | OFFLINE PASS — allowlist/poisoned-view tests; future importer/content review still required |
| G8 | PARTIAL — reproducible optional smoke, hashes/pins/raw artifacts; both live runs SKIPPED |
| G9 | PASS — no proposed method, human annotations unchanged, no real pilot or hypothesis statistics |

**Overall R0.** To reach R1: inspect a tiny competent real model/embedding trace; validate real returned usage and a no-dispatch exhausted-budget check; validate the intended Qwen deployment or explicitly narrow the supported engineering scope; resolve final resource-release/cache parity integration; make replay/readout scope scientifically adequate (model regeneration and historical audit where claimed); review and freeze development prompts/thresholds. Human adjudication is a separate R2 gate, not a reason to call the current engineering R1. Details and validation evidence are in [ENGINEERING_PHASE_REPORT.md](ENGINEERING_PHASE_REPORT.md).
