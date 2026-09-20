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
