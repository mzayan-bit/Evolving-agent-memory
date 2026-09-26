# Engineering phase report — 2026-09-26

**Final readiness: R0.** Stronger comparator interfaces and real-usage enforcement now exist and pass offline tests. No real model or embedding competence evidence was generated; neither engineering R1 nor pilot R2 is claimed. No proposed uncertainty-aware repair method, pilot run, synthetic human annotation, adjudication or hypothesis test was introduced.

## Requested deliverables

| # | Deliverable | Result |
|---|---|---|
| 1 | R1 criteria | Defined before implementation; objective G1–G9 and final assessment in R1_READINESS_CRITERIA.md |
| 2 | Adapters | Native Claude Sonnet 5 and one Qwen3.5-9B/vLLM backend; public identifier/revision verified; environment-only credentials |
| 3 | Live usage accounting | Raw metadata parsing, cache/input/output/reasoning handling and unknown semantics implemented; live validation SKIPPED |
| 4 | Actual budget enforcement | Pre-dispatch reservation, actual reconciliation, all requested cumulative caps, charged failures/retries and halt on unknown/overrun; tested offline |
| 5 | B4 | B4a lexical alias preserved; B4b pinned MiniLM semantic-neighbor closure and embedding cache; real backend unavailable here |
| 6 | B5 graph | Strict model point inference projected to pairwise arcs; fixed threshold; no adaptive use of confidence |
| 7 | B5 sets | Same proposals preserve AND/OR sets and drive deterministic classical maintenance |
| 8 | B7 | Honestly named simplified positive support maintenance; no full ATMS/JTMS claim; no unsupported new symbolic machinery |
| 9 | B8 | Dependency inspections counted on hits/misses; unaffected reuse and invalidation tested; model response caching separate; semantic regeneration remains absent |
| 10 | B9 | Visible-support rollback plus known-independent-root rescue; shared/unknown origins do not certify independence |
| 11 | Query-only | B10 current evidence audit, repeated verifier accounting, validated citations, no persistent mutation; historical audit not implemented |
| 12 | CUPMem | Keep prior unmodified native store reproduction external; direct G1 mapping rejected as scientifically lossy |
| 13 | Rollback | Internal B3/B9 analogues only; no official reproduction; complete/gold-lineage arms separately labeled oracles |
| 14 | Matrix | FAIR_COMPARATOR_MATRIX.md records mutation, model use, structure, history, resources and fidelity; shared no-external-evidence/no-ordinary-gold conditions explicit |
| 15 | Smoke | Claude SKIPPED; Qwen SKIPPED; embedding SKIPPED; optional five-dispatch/seven-target runner tested with offline doubles |
| 16 | Actual resources | Zero live model calls, zero live input/output tokens, zero real embedding calls; mock tokens are test data and not spending |
| 17 | Oracle leakage | Poisoned-view allowlist tests exclude hidden rules/lineage, future records, corruption kind, expected labels and benchmark metadata; no rules passed to model |
| 18 | Headroom gate | RESIDUAL_HEADROOM_PROTOCOL.md requires adjudicated data, strong-baseline residual harm and approved margins before any method phase |
| 19 | R0 blockers | Live competence/accounting/stopping; verified runtime deployment; final resource release/cache-parity integration; credible replay/readout scope; development freeze |
| 20 | Validation | 110 offline tests PASS, Ruff PASS, mypy PASS (25 source files); 70 deterministic runs completed (10 policies × 7 fixtures) |
| 21 | Commits | 7aab062 provider/accounting; e733273 comparators/tests; this report and protocol updates form the final research commit |
| 22 | Git | Human annotation paths unchanged versus fd7352d; final clean-tree and remote verification performed after documentation commit |
| 23 | Readiness | R0 retained honestly; R1 is not inferred from test counts |

## Evidence and limits

Committed `engineering_smoke/claude-skipped.json` and `qwen-skipped.json` record skipped attempts at code commit e733273, with uncommitted documentation explicitly marked dirty. `validation.json` records source hashes, test counts and the deterministic run manifest digest. Full local fixture artifacts remain in ignored `results/model-engineering-e733273/`. Final clean-checkout regression is run after the research commit; no raw private inputs or credentials are tracked.

The extra smoke-runner integration test exposed identical fixture prefixes causing response reuse. Smoke reuse was disabled, and a successful five-dispatch run now requires an exhausted-budget check to fail before a sixth dispatch. Some fixture text is identical while its authored formal rules differ: matching that hidden gold would be an oracle leak, not semantic competence. Unknown predictions are legitimate. The smoke validates mechanics; live inspection and development cases with genuinely observable semantics remain necessary for R1. No accuracy statistic is fabricated from the mocks.

Native JSON schema was checked against current provider documentation; unsupported numeric constraints are omitted from wire schema and enforced locally. Invalid usage subsets preserve the raw response, mark normalized usage unknown and halt. No full semantic model run, package installation, model download or substitute backend was attempted. Hardware suitability for Qwen is unassessed; lack of configured endpoint is the actual skip reason.

## Explicit research decisions

**Q1 — Single most dangerous comparator?** B5b point-estimate support-set inference plus classical maintenance. It directly supplies AND/OR repair logic once language inference is good. This is a structural assessment, not an empirical ranking; B8/B10 may dominate operationally.

**Q2 — Enough headroom after point support sets?** Unknown. No live competence or adjudicated held-out outcomes establish residual harm.

**Q3 — Does query-only auditing threaten persistent repair?** Yes conceptually. B10 now makes the threat executable for current queries, but superiority is unmeasured. Compare cumulative horizon cost, answers, remaining stale storage and later unaudited reuse.

**Q4 — Does cached replay make selective repair unnecessary?** Unknown. Symbolic fixtures verify cache correctness/reuse, not real regeneration cost or study dominance.

**Q5 — Are real costs/budgets pilot-ready?** Not yet. Offline enforcement is strong enough to test adapters safely, with explicit one-call overshoot and unknown billing. Live accounting/stopping, final release schedule and cache parity must be validated before scientific use.

**Q6 — Exactly what prevents R1?** Missing real provider/embedding competence trace (G1), real usage record (G2), live exhausted-budget stop (G3), credible model-backed replay/cost and arm-level cache accounting (G4), complete declared readout scope and runtime integration (G6/G8), and development prompt/threshold/deployment freeze. The Qwen endpoint/manifest and embedding runtime are unavailable. Human adjudication separately blocks R2; it is not the sole remaining obstacle.

**Q7 — Implement the proposed method now?** **NO.** Independently adjudicated gold and demonstrated residual baseline headroom are absent. Stop after this engineering phase.

## Subsequent live validation phase

The following report supersedes this phase's “embeddings unavailable” finding while preserving its historical record: [LIVE_RESOURCE_VALIDATION.md](LIVE_RESOURCE_VALIDATION.md). Pinned embeddings and Qwen tokenizer execution now pass. Model-backed readout/replay paths and 29 additional offline tests exist. Language generation is still unavailable and overall readiness remains R0. No human annotation status or research conclusion changed.
