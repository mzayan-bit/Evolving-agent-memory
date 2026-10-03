# Development freeze candidate — local protocol hardening, 2026-09-27

**ENGINEERING VALIDATION, not a pilot freeze.** READY TO FREEZE means the engineering contract is concrete for its declared scope. It does not establish semantic quality, select label-dependent settings, or sign a study freeze. Readiness is assessed against the unchanged R1_READINESS_CRITERIA.md in QWEN_ENGINEERING_ERROR_AUDIT.md. No human annotations were accessed or changed.

| Component | Status | Candidate / outstanding evidence |
|---|---|---|
| Qwen revision | READY TO FREEZE | Qwen/Qwen3.5-9B c202236235762e1c871ad0ccb60c8ee5ba337b9a; real generation, exact tokenizer checks; source/conversion provenance retained |
| Quantization | READY TO FREEZE | Bartowski Q4_K_M conversion 182be2fd6c7bc44887d88a91cb03ff009cc9f549, weight SHA-256 in qwen_local/deployment.json; mixed imatrix-calibrated quantization changes weights, not a full-precision equivalence claim; converter does not attest exact source commit |
| llama.cpp runtime | READY TO FREEZE | b9222 / 9a532ae4bab1b164052ce60a738f78538b421c66, CPU+Accelerate on M4 16 GB, 4096 context, one slot; Metal unavailable in this session |
| B5 prompt | READY TO FREEZE | Generic ID-grounding v2 contract and distinct pairwise/support-set elicitation; exact constants at b1d38c7; freeze the protocol, not a claim of competent study-wide inference |
| B5 schema | READY TO FREEZE | Existing ontology, strict complete target assessments, per-view ID enums; B5a singleton links / B5b AND/OR sets; native grammar plus local semantic schema checks |
| Retry policy | READY TO FREEZE | At most one protocol-invalid retry using original evidence, fixed reminder and malformed output; every physical call/token/latency charged; no semantic/refusal/timeout/truncation retry |
| Parser | READY TO FREEZE | Strict JSON, exact fields, visible literal IDs, unique keys/targets/groups, finite confidence and consistent structures; no guessed IDs or logical repair |
| B5 threshold procedure | NEEDS DEVELOPMENT DATA | Review support-set loss/precision-recall objective and preservation guardrails before threshold search; deterministic grid/tie-break and disjoint validation required |
| B5 threshold value | NEEDS DEVELOPMENT DATA | .7 remains an untuned engineering candidate, not newly frozen; scores only commit a deterministic structure |
| B8 replay semantics | READY TO FREEZE | Explicit visible acyclic derivations, dependency/config/scope/time cache identity, charged local checks, staged atomic commit; only the tiny current-time contract is covered |
| B10 audit semantics | READY TO FREEZE | Current-time query-only audit, cache disabled, every recurrence charged, persistent state unchanged; distinct state versus answer outcomes |
| Embedding model/runtime | READY TO FREEZE | MiniLM 1110a243fdf4706b3f48f1d95db1a4f5529b4d41, normalized 384-dimensional CPU float32; prior actual load/encode/cache/cap evidence retained |
| B4 threshold procedure | READY TO FREEZE | Existing development-only rubric/grid/F1/tie-break and disjoint validation in SEMANTIC_BASELINE_PROTOCOL.md |
| B4 threshold value | NEEDS DEVELOPMENT DATA | .7 is provisional. No labeled development selection or new freeze occurred |
| Per-call accounting | READY TO FREEZE | Local returned input/output usage checked against actual token IDs; predispatch reservation, reconciliation, explicit unknowns/overruns, charged retry, real stopping evidence; no invented local USD/energy |
| Study-level accounting | BLOCKED | Final arm construction and revision-credit release scheduling remain unvalidated under matched study budgets |
| Response/derived caching | READY TO FREEZE | Immutable content-addressed responses, exact prompt/model/settings/schema identity; dependency-sensitive derived cache; tested physical versus reused work |
| Cache parity across study arms | BLOCKED | Final multi-arm construction/reuse policy and equal resource charging require integrated validation; tiny full/incremental equivalence does not establish this |
| Result/manifest schema | READY TO FREEZE | Commit/dirty/environment/runtime/settings, raw usage, prompt/wire hashes, attempts/retry IDs, failure categories, separate semantic audit, measured latency and unavailable cost fields |
| B7/B9 semantics | READY TO FREEZE | Simplified positive AND/OR maintenance and support-aware rollback; explicit fidelity limits remain, no ATMS reproduction claim |
| Structured readout | READY TO FREEZE | Existing immutable Trace interface with three time views and separate evaluator state/retrieval/answer outcomes |
| Historical model readout/replay coverage | BLOCKED | Current-time model checks do not validate historical natural-language outcomes; scope must be reviewed without silently narrowing the research question |
| Claude execution | BLOCKED | No credential obtained or invented. Claude remains unvalidated; the pre-existing R1 gate table does not independently require Claude/API-only accounting. MODEL_PROMPT_PROTOCOL.md's broader future evaluation-freeze review still calls for both model families |

No confidence drives evidence acquisition, verification, replay or repair scheduling. READY TO FREEZE entries should stop receiving generic architecture or semantic fixture-driven prompt changes. Reconsider only a concrete defect, agreed scope requirement, or development-data finding.

A pilot freeze additionally needs independent A/B/adjudication, approved comparator/access set, development thresholds, scope agreement, practical margins and statistical expansion/kill rules. Human adjudication remains an R2 condition, not a new retroactive R1 definition. The existing R1 assessment already requires resource/cache integration and development prompt/threshold review; these must not be erased merely because local inference now works.
