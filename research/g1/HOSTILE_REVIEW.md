# Simulated skeptical review

**Provisional assessment: not ready for a method submission.** The claimed ingredients largely exist. The remaining question may support an analysis, but neither its prevalence nor its annotation reliability is established. Thirty designed examples demonstrate that authors can construct a distinction, not that the distinction matters in agent workloads.

| Objection | Evidence required; no marketing rebuttal |
|---|---|
| This is truth maintenance with LLM names. | Compare ATMS-style support sets/rederive on identical inferred supports. State exactly which classical assumption fails and measure its consequence. A hypergraph diagram is insufficient. |
| Why not replay everything? | Full-history replay with archived historical state, real token/latency accounting and unavailable-source controls. If cheap replay dominates, stop. |
| Why not requery the source? | Requery baseline with the same evidence availability/cost; distinguish disappeared sources, expensive checks and ordinary cheap APIs. |
| Why persistent repair? | Delayed, unsignaled action/answer/summary reuse plus amortized horizon cost versus query-only StateAuditor or PlanFence-style action validation. |
| Semantic similarity may be sufficient. | Broad-neighbor invalidation at a tuned but frozen threshold; scope/bystander false invalidation and reconstruction cost on held-out domains. |
| Why probabilistic inference? | Show heterogeneous uncertainty and decision-relevant posterior quality beyond a point support-set estimate. If decisions are effectively binary and stable, probability machinery is needless. |
| Alternative supports look planted. | Independently collected/annotated naturalistic examples; prevalence is not estimated from deliberately balanced synthetic cases. |
| Synthetic assumptions encode the answer. | New human-authored held-out domains/templates, independent support annotation, construction audit and source-origin grouping. Do not train/test on generator labels that instantiate the proposed controller. |
| The gain is extra calls or a stronger model. | Matched evidence realization, model, tokens, retrieval and verifier/replay cap; charge preprocessing and failed calls. |
| “Calibrated” is unsupported. | Frozen event definition, held-out calibration split, Brier/reliability/risk–coverage with counts and uncertainty. LLM confidence and judge agreement do not suffice. |
| Domain shift will break semantic support. | Disjoint domains/entities/templates and both model families; show all regimes including failures. |
| Effect is too small to matter. | Predeclared practical margins, uncertainty and operational cost; no significance-only argument. |
| Oracles make comparisons unfair. | Runtime-field manifests and access matrix; gold fault/scope/support only in clearly separate upper bounds. |
| What is new over Rollback + StateAuditor + CAMA? | A controlled persistent-state experiment with equal evidence/resources and independent/correlated alternatives across revisions. A simple composition is a mandatory threat; if it matches, abandon a new controller claim. |
| Your support gold is not reliable. | Two independent humans, preserved disagreements, adjudication provenance and suitable relation/set agreement. The current AI drafts supply none of this evidence. |
| You changed benchmark labels to favor your ontology. | Publish source UID, original evidence, exact changes and competing interpretations; human reviewers must be free to reject the adaptation. Separate determinate and ambiguous strata. |
| A corrected answer is not repaired memory. | Inspect persistent state after repair and after later writes, score recurrence and historical truth, not only current QA. |
| Why should ACL/ICLR/NeurIPS/ICML care? | Either a generalizable language-support failure boundary, a rigorously validated evaluation protocol, or a method with independent evidence of improvement over strong classical/simple baselines. Presently none has been demonstrated. |

## Evidence currently available

Deep paper/source audit, CUPMem store mechanics, 22 MemTX unit tests, primary classical references, 30 unadjudicated draft cases and a prospective protocol. These justify investigating the question, not claiming empirical headroom. The StateAuditor hard-set null result makes baseline and generalization kills especially plausible.

## Decision logic

B for the question; no method implementation yet. If ontology survives but simple baselines solve the problem, choose C only if the failure-boundary analysis itself teaches something general and reproducible. Choose D if reliable annotation or practical signal fails. Do not rescue a dead method by adding complexity or renaming standard metrics.

## Round 2 — implemented harness audit, 2026-09-25

**R0 for the proposed model-backed study.** Deterministic tests passing is narrower than scientifically adequate baselines. Human labels alone cannot make this executable study ready.

| Attack | Audit finding and disposition |
|---|---|
| Is B7 too weak? | It is positive single-context least-fixed-point support maintenance, not full ATMS. It covers current fixture consequence semantics; nogoods/minimal environments are absent. Require explicit closed-world annotations and a common semantic verifier. Add environment reasoning only if the adjudicated task requires it; do not claim a new TMS. |
| Is full replay artificially expensive? | A replay step is currently an output refresh, not a physical LLM call. Full graph computation is repeated. Added B8 ancestor-slice memoization, cold-cache charging and hit logging; actual model/CPU measurements still required. |
| Is semantic closure unrealistic? | Yes: B4 is lexical cosine, not a strong semantic baseline. Preserve its control label; require a development-tuned frozen embedding/model-neighbor comparator before a method claim. |
| Are baselines faithful enough? | No published-method reproduction exists in B0–B7. CUPMem component checks are real but do not validate pipeline fidelity. Rollback support rescue and query-only audit remain required threats. |
| Can oracle information leak? | Frozen views omit gold masks, but explicit fixture rules make semantics easy. O1 currently identifies a changed source, not independently adjudicated fault. O2/O3 share a bundle flag and need stricter projection before general adapters. Trusted in-process adapters are not adversarially sandboxed. |
| Are budgets comparable? | Only deterministic counters are enforced. Shared evidence access is not matched realized context/compute. Provider reservation/reconciliation, released credits, real inference/verifier costs and cache parity remain gates. |
| Could stronger models remove the problem? | Yes. Require within-family effects on the current API candidate plus open model, and stronger-model sensitivity before generalization. Weak-backbone-only effects cannot support a general controller claim. |
| Is dependency uncertainty ordinary classification uncertainty? | Often yes. Freeze inference and compare thresholded B5/B7 to any future decision rule; gains that disappear with identical proposals are inference gains, not a new repair policy. |
| Are support sets artificial? | Fixtures are explicit finite rules and planted alternatives. Independent human annotation and new naturalistic families must establish usable semantics; random corruption cannot estimate natural prevalence. |
| Is G1 a TMS with noisy edges? | On the formal slice, yes. Scientific value would be a measured language-derived support failure boundary under persistence and resources, or residual policy advantage after classical threats. Neither exists yet. |
| Why specifically modern LLM agents? | Potentially implicit language entailment, stochastic inference/replay, lossy summaries and long-lived reuse. These properties must be demonstrated in observed workloads; renaming deterministic records as agents proves nothing. |
| Are history semantics sound? | Audit found target validity intervals ignored by grounding and current permissions omitted from historical-then disclosure. Both fixed with tests; existing fixture expectations unchanged. Broader retroactive semantic changes still need adjudicated evidence adapters. |
| Was the protocol tuned after outcomes? | Only engineering fixtures have run. Candidate splits now keep all new pilot families out of tuning; thresholds and budgets must be chosen on development before a signed freeze. |

See [fidelity audit](BASELINE_FIDELITY_AUDIT.md), [missing threats](MISSING_BASELINE_AUDIT.md), [reproduction evidence](COMPETITOR_REPRODUCTION.md) and [candidate protocol](PILOT_PROTOCOL_CANDIDATE.md). No positive method result is currently supportable. Do not implement the proposed uncertainty policy before adjudication and strong-baseline evaluation.

## Round 3 — model interfaces and stronger comparator engineering, 2026-09-26

**R0 retained.** Offline execution contracts now exist, but no live provider, local Qwen or embedding competence run has passed. More code does not establish research headroom.

| Attack | Evidence and current disposition |
|---|---|
| Can Sonnet/Qwen infer almost all dependencies correctly? | Unknown. Adapters and strict output validation exist; live smoke is SKIPPED. No inferred accuracy from canned fixtures. Strong models may erase the problem. |
| Does point support-set inference eliminate the gap? | B5b now composes a fixed model proposal with classical AND/OR maintenance, using the same proposals as B5a. It is the most dangerous structural comparator. Need adjudicated held-out outcomes, not authored alternatives. |
| Does query-only audit dominate persistent repair? | B10 corrects/withholds answers without state writes and pays on repeated queries. Need time-horizon costs, future unaudited reuse and historical scope before claiming persistence value. Current-time plumbing is not dominance evidence. |
| Does incremental replay dominate selective repair? | B8 preserves unchanged derivations and now reports dependency inspections even on hits. It still evaluates explicit rules, not model/tool regeneration. Do not turn symbolic steps into a cost victory. |
| Does ATMS already supply the logic once inference is good? | Positive support closure already supplies AND/OR propagation here. No new logic contribution is shown. Full minimal-environment/nogood machinery is absent and presently unnecessary for the fixtures. |
| Is novelty just confidence instead of threshold? | No uncertainty controller was implemented. Such novelty would be weak without independently established residual decision-relevant uncertainty after B5b/B8/B10. Current method decision remains NO. |
| Are independence and copies handled honestly? | B9 requires known source origins disjoint from the changed origin and currently grounded support. Unknown or shared origins cannot be called independent rescue; still-grounded but unverified independence is quarantined under a fixed rule. Incorrect inferred provenance remains a failure mode. |
| Are prices driving scientific decisions? | No. Raw resource caps are separate from a dated post-hoc price snapshot. Local model dollar cost remains unknown. |
| Are budgets actually safe? | Offline preflight, reconciliation and overrun tests pass. Estimated input reservations can overshoot once; failed calls may have unknown billing. Single executor only. Live accounting/stopping and final release schedule remain gates. |
| Is the prompt leaking formal fixture answers? | Explicit allowlist excludes rules/lineage/gold/future/labels and metadata; provenance is permitted visible evidence. Content or IDs can still contain label-like information if a future data adapter is careless, so independent construction review remains necessary. |
| Is the embedding comparator competent? | A pinned real backend exists but was not installed/run. Tests use synthetic vectors to verify mechanics only. Sequence truncation and the untuned threshold need development inspection. |
| Are adaptations being sold as reproductions? | No. CUPMem stays an external unmodified-store check; B9/B10 are internal analogues. Neither official Rollback nor StateAuditor performance is reproduced. |

Human gold and residual baseline headroom still do not exist in this execution context. Do not implement the proposed method or infer a paper result from the passing engineering tests.

## Round 4 — local live evidence and remaining language-model gap

Real MiniLM vectors and a pinned Qwen tokenizer now execute; neither proves competent support inference. The tokenizer initially failed because required config metadata was absent, then because current Transformers returned BatchEncoding instead of the assumed flat list. Both failures are preserved; the corrected exact-ID normalization passes. This is a useful engineering finding, not a model-quality result.

Could the current Reader mask memory failure? It can produce a correct answer from corrected evidence while stale storage survives, so evaluator fields remain separate and tests explicitly preserve that counterexample. Nonce/counterfactual prompts reduce easy pretraining shortcuts but do not guarantee grounding. Citation membership is a schema/evidence-availability check, not an entailment proof.

Could B8's previous weak cost model manufacture headroom? The new generated-content DAG path uses actual model-call accounting and invalidates keys for model/prompt/config/dependency/scope/clock changes, but only mocks have generated text here. Therefore its real cost remains unknown; do not compare symbolic or mock costs against a future proposed method. Unknown dependency structure and unsupported cyclic generative tasks remain limitations.

Could confidence leak the proposed contribution into B5? Tests show selected proposals with .71 and .99 yield identical decisions and no verifier/replay operations at the fixed .7 cutoff. Below-threshold omission changes the point structure only; no adaptive uncertainty controller exists.

Can R1 be awarded from one real embedding budget stop? No. It is evidence of local B4 execution and preflight enforcement only. Missing API credentials and a suitable pinned Qwen deployment still prevent real support, usage, language-budget stop, replay and query-audit validation. R0 retained. The research question and no-method decision remain unchanged.
