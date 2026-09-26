# Development freeze candidate — live validation phase, 2026-09-26

**Not a pilot freeze. Overall R0.** READY TO FREEZE means the engineering contract is concrete and tested for its stated scope, not that a signed freeze exists or semantic quality is established. Procedures can be fixed now; label-dependent settings cannot. No human annotations were accessed for model selection.

| Component | Status | Candidate / outstanding evidence |
|---|---|---|
| Embedding model/runtime | READY TO FREEZE | MiniLM pinned revision, 384 dimensions, normalized CPU float32, package snapshot; real load/encode/cache tests passed |
| Semantic threshold procedure | READY TO FREEZE | Development-only neighborhood rubric/grid/F1/tie-break and disjoint validation in SEMANTIC_BASELINE_PROTOCOL.md |
| Semantic threshold value | NEEDS HUMAN DATA | Existing .7 is engineering-only; no labeled development selection occurred |
| Claude model ID | NEEDS MORE ENGINEERING | Official claude-sonnet-5 reverified, native schema/usage rules checked; no credential/account execution |
| Qwen revision | NEEDS MORE ENGINEERING | c202236235762e1c871ad0ccb60c8ee5ba337b9a, tokenizer/template executed; model generation/deployment unvalidated |
| B5 system prompt | NEEDS MORE ENGINEERING | Existing development-v1 prompt, now observable five-relation smoke; real inference missing |
| B5 output schema | READY TO FREEZE | Strict shared groups/assessments, complete targets and visible IDs, local confidence bounds; identical provider normalization tested |
| B5 threshold logic | READY TO FREEZE | Fixed preselected threshold creates structure; downstream decisions receive no confidence-driven scheduling; above-threshold score invariance tested |
| B5 threshold value | NEEDS HUMAN DATA | .7 remains provisional; select on independent development support labels before evaluation |
| B7 semantics | READY TO FREEZE | Positive single-context AND/OR closure; no full ATMS/nogoods claim; richer task semantics require separate review |
| B8 cache/replay | NEEDS MORE ENGINEERING | Real ModelDeriver/ModelCachedReplay path, DAG/version/config cache and atomic commit tested; no live language-model regeneration trace |
| B9 repair semantics | READY TO FREEZE | Visible support closure plus grounded disjoint-origin rescue; shared/unknown origins never certify independence |
| B10 query audit | NEEDS MORE ENGINEERING | Current-time path with paid-per-query audit and non-mutation; no live audit; historical model audit unsupported |
| Budget accounting | NEEDS MORE ENGINEERING | Cumulative preflight/reconcile/overshoot contracts tested; actual embedding stop passed; language-provider usage/stop unvalidated; release schedule not implemented |
| Retry policy | READY TO FREEZE | One malformed B5 schema retry, charged; no transport/refusal/truncation retry; 429/500/timeout/overrun tested without paid waste |
| Structured readout | READY TO FREEZE | Three time views from immutable Trace, separate evaluator state/retrieval/answer outcomes |
| Natural-language readout | NEEDS MORE ENGINEERING | Current-only model reader, exact fixture scoring and source citations; live execution unvalidated |
| Result/manifest schema | READY TO FREEZE | Commit/dirty/hardware/config hashes, original phase budgets, raw usage categories, cache/latency/status; secret whitelist |
| Cache parity across study arms | NEEDS MORE ENGINEERING | Cold/warm and full/cached integration tests; shared proposal construction must still be charged consistently in final study runner |

B5 selection procedure: approve a development-only support-set loss/precision-recall objective and preservation guardrails before examining model outputs; use fixed threshold candidates with deterministic tie-break; freeze against a separate development validation partition. Do not import the embedding-neighborhood F1 label into logical support inference. No calibration claim is made from LLM confidence.

A pilot freeze additionally needs the existing independent A/B/adjudication gates, final comparator/access set, scope agreement, practical margins and statistical expansion/kill rules. Historical model generation cannot be reported under the current reader contract; either implement and validate it or explicitly restrict model outcomes while retaining deterministic historical outcomes. Do not silently narrow the research question to fit code.
