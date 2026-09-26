# Live resource validation — 2026-09-26

**Readiness remains R0.** Real local embeddings and tokenizer checks passed. No live language-model generation was possible. This is engineering evidence only: no pilot, superiority claim, inferred G1 headroom or new repair controller.

## Outcomes

| Check | Outcome | Evidence |
|---|---|---|
| Claude basic / B5 | SKIPPED | ANTHROPIC_API_KEY missing; exact official identifier remains claude-sonnet-5 |
| Qwen generation / B5 | SKIPPED | No server/manifest; pinned weights alone exceed practical resident capacity on measured 16 GB host |
| Embedding / B4b | PASS | Pinned actual MiniLM load, 384 dimensions, normalized vectors, exact repeat, batch tolerance, cache and policy execution |
| Qwen tokenizer | PASS after two corrected setup/shape failures | Same pinned template/revision; 23 nonce prompt tokens, template IDs equal direct encode |
| Language-provider budget stop | SKIPPED | No real first call; offline counted-transport/call/token/overrun checks pass |
| Local embedding budget stop | PASS | One real encode allowed; distinct second input rejected before backend call |
| B8 real language-model replay | SKIPPED | End-to-end regeneration/cache path passes offline; no configured language model |
| B10 live audit | SKIPPED | Two-query, repeated-charge, unchanged-storage path passes offline only |
| Model natural-language readout | SKIPPED | Current-only reader implemented and tested offline; structured historical reader remains available |

All final local receipts identify runtime code commit **f50aa28** and correctly mark the tree dirty because documentation/test-suite artifacts were still being assembled. Source hashes in `live_validation/summary.json` permit verification. Earlier receipts remain preserved; they are not relabeled as clean or successful.

## Actual resources across this phase

| Resource | Measured total |
|---|---|
| Paid/API or local language-generation requests | 0 |
| Provider-reported input / cached / output tokens | 0 / 0 / 0 (no calls) |
| Provider reasoning tokens | Not exposed; no provider call |
| Provider failures / paid retries | 0 / 0 |
| Provider request latency | 0 ms (no calls) |
| Derived API spend | $0 under price table anthropic-sonnet5-2026-09-26-standard-usd |
| Real embedding forward calls | 14 across three local smoke runs |
| Embedding items encoded | 20, including the three-item batch in each run |
| Local hardware dollar/energy cost | Unknown; not assumed free |

The final embedding run uses five physical forward calls covering seven items; cache hits do not enter those counts. Three smoke runs were performed: initial load/shape/cache validation, addition of real preflight budget stopping, and confirmation at the committed runtime revision. `summary.json` provides exact elapsed milliseconds from each runtime event. Do not sum nested encode latency with total runtime. The first load included cold imports/setup; later warm runtimes are not a performance comparison.

Pinned Qwen tokenizer-only operations are not language-generation usage. Its 23-token fixture length is an exact local tokenizer result, **not** a server input count or a billable request. The first tokenizer run lacked config.json; the second exposed Transformers 5.17.0 returning BatchEncoding; the third and final runs passed after explicit token-ID normalization. Failed receipts are retained. A diagnostic tokenization used only the same public nonce prompt and no model weights.

## What changed

- Opt-in suite under `tests_live/`, excluded from default collection and requiring explicit environment gates. Paid checks require a second opt-in. Maximum eight provider dispatches, with separate one-call and seven-call phase budgets; no hidden retry grid.
- Actual embedding preflight cap. Provider rejected reservations now leave an auditable no-dispatch record. HTTP request-id is recorded when supplied; body message ID is a fallback.
- Exact Qwen tokenizer normalization for flat IDs or BatchEncoding; no character heuristics or fabricated provider usage.
- ModelCachedReplay and ModelDeriver regenerate changed DAG nodes, reuse unaffected derivations, track real-call costs, validate citations and commit state/cache atomically. Model/prompt/schema/config/dependency versions, scope, validity and declared clock sensitivity affect identity.
- Common bound-state Reader interface, with deterministic temporal readout and current-only model readout. State, retrieval coverage and answer correctness are evaluated separately; labels never enter prompts.
- Observable fictional five-relation evidence and nonce counterfactual controls, unchanged B5 threshold behavior, and development-only threshold-selection procedures.

Local raw language responses would be saved only in ignored output directories for manual inspection; committed manifests whitelist usage/config/identity and response hashes. No such real responses exist in this phase. Public local vector/token metadata is sanitized, with no credentials or hardware serials.

## R1 decision

| Gate | Status |
|---|---|
| G1 competent model-backed inference | PARTIAL — embedding live, language support inference blocked |
| G2 actual provider accounting | BLOCKED — no returned language-provider usage |
| G3 real budget stopping | PARTIAL — embedding stop live, language stop offline only |
| G4 credible cache/replay | PARTIAL — model path integrated, actual regeneration cost missing |
| G5 explicit fidelity | PASS |
| G6 common execution/readout scope | PARTIAL — integration tested, current-only model scope and final study driver unresolved |
| G7 oracle isolation | PASS at tested boundaries |
| G8 reproducible live evidence | PARTIAL — local receipts present, provider receipts skipped |
| G9 no pilot/method/human-label fabrication | PASS |

Primary blockers: Claude credential and an appropriate pinned Qwen deployment; real B5/usage/cap/B8/B10/readout validation then becomes executable. Remaining freeze work includes numeric threshold selection from independent development labels, server configuration verification, agreed readout/replay scope, final cache/construction accounting and resource-release schedule. Human adjudication separately blocks the pilot. No threshold was optimized or selected here.

Validation: **139 offline tests PASS**, Ruff PASS, strict mypy PASS (32 source files). Explicit `pytest tests_live` without opt-in: **4 SKIPPED**, proving its safe default. Deterministic fixture regression is rerun from the final committed tree. Human annotation files remain unchanged.

## Explicit answers

**Q1:** No real strong language-model support inference executed. B4b embeddings and Qwen tokenizer executed; neither substitutes for B5 generation.

**Q2:** Provider normalization is tested and follows current official usage semantics, but trustworthiness for a scientific run remains unvalidated against an actual response.

**Q3:** Yes for the real local embedding model: the second encode was prevented. No live language-provider stop was demonstrated; it is SKIPPED.

**Q4:** B8 now has a credible executable incremental-regeneration architecture for explicit acyclic dependencies. It is not yet an empirically validated real-cost comparator, nor arbitrary agent/tool-trace replay.

**Q5:** B10 is an executable current-time query-only alternative with repeated costs and non-mutation tested. Live behavior and broader historical scope remain unvalidated.

**Q6:** Missing credential/deployment prevents real language inference, provider usage reconciliation/stopping and live B8/B10/readout evidence; final matched-resource/cache and scope integration must also be resolved.

**Q7:** Some engineering contracts and threshold-selection procedures are READY TO FREEZE. The complete non-human protocol cannot freeze: live/provider/deployment evidence and development-dependent numerical settings remain unresolved. See DEVELOPMENT_FREEZE_CANDIDATE.md.

**Q8:** **NO.** Do not implement the proposed uncertainty-aware method without independently adjudicated evaluation and demonstrated residual strong-baseline headroom. Stop after this phase.
