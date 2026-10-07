# Non-human development freeze review

**No pilot freeze is signed.** READY_TO_FREEZE means the tested contract can be fixed before annotations; it does not assert model quality or select data-dependent values. The R1 criteria file is unchanged. See NON_HUMAN_PROTOCOL_SNAPSHOT.md for the complete gate assessment and stop decision.

| Component | Status | Frozen candidate / limit |
|---|---|---|
| Qwen source/revision | READY_TO_FREEZE | Qwen/Qwen3.5-9B c202236235762e1c871ad0ccb60c8ee5ba337b9a; actual generation and tokenizer checks |
| Q4_K_M conversion | READY_TO_FREEZE | Bartowski 182be2fd6c7bc44887d88a91cb03ff009cc9f549; weight SHA-256 d784ce9eda1a5a7b51e8f705a9e6310844bf4f173654d115823c775fdea56d43. Mixed imatrix K-quants; converter does not attest the exact source commit; no full-precision equivalence claim |
| llama.cpp revision | READY_TO_FREEZE | b9222 / 9a532ae4bab1b164052ce60a738f78538b421c66; launcher checks runtime and weight hashes |
| Generation deployment | READY_TO_FREEZE | CPU+Accelerate, M4 16 GB, 4096 context, one slot, four threads, f16 KV, batch 256/ubatch 128; temperature 0, seed 0, thinking/prompt cache off. Exact command in qwen_local/deployment.json |
| Study context/output/resource values | NEEDS_DEVELOPMENT_DATA | Deployment limits and smoke caps are not selected study budgets. Choose common feasible limits from development lengths/cost/completion data and obtain approval |
| Embedding model | READY_TO_FREEZE | all-MiniLM-L6-v2 1110a243fdf4706b3f48f1d95db1a4f5529b4d41; normalized CPU float32, 384 dimensions, max length 256; runtime snapshot retained |
| B4b selection procedure | READY_TO_FREEZE | Existing independently labeled neighborhood rubric/grid/F1/tie-break and disjoint validation contract; objective still subject to stated reviewer approval |
| B4b threshold value | NEEDS_DEVELOPMENT_DATA | .7 remains an engineering default, not selected or newly frozen |
| B5a prompt | READY_TO_FREEZE | point-pairwise-development-v2 singleton-link elicitation, unchanged b1d38c7 constants; named shared-proposal projection alternative only in isolation |
| B5b prompt | READY_TO_FREEZE | point-support-development-v2 AND/OR elicitation, unchanged b1d38c7 constants; no fixture-semantic prompt tuning |
| B5 structured schema | READY_TO_FREEZE | Literal visible-ID enums, complete targets, frozen relation ontology, confidence bounds and exact fields |
| Parser | READY_TO_FREEZE | Strict JSON/ID/structure checking; no guessed IDs, semantic repair or gold feedback. Existing self-support failure remains an explicit outcome |
| Retry policy | READY_TO_FREEZE | One paid protocol-invalid B5 retry; no semantic/transport/refusal/truncation retry; audit/readout have no retries |
| B5 thresholds and selection approval | NEEDS_DEVELOPMENT_DATA | Approve logical-support objective/grid/guardrails before selection; choose with adjudicated development support labels. Shared isolation recipients must use one identical threshold; .7 unselected |
| B7 semantics | READY_TO_FREEZE | Simplified positive AND/OR grounding, measured candidate checks, paid/allocated construction; no full ATMS/JTMS claim |
| B8 replay/cache semantics | READY_TO_FREEZE | Explicit acyclic public provenance tasks; public version rebinding; generated text committed; affected invalidation/unaffected reuse and atomic failure. No arbitrary tool/cyclic replay or privileged inferred graph |
| B9 rollback semantics | READY_TO_FREEZE | Paid/allocated support construction, affected closure and known-disjoint-origin rescue; unknown/copy origins never certify independence |
| B10 audit semantics | READY_TO_FREEZE | Query-only audit on selected current/historical prefix, paid every time, no storage mutation; same query schedule as other arms |
| Current model readout | READY_TO_FREEZE | Bound active visible records; strict citations/output; common per-checkpoint schedule and ledger |
| Historical model readout | READY_TO_FREEZE | Immutable known-time frame, no future records/supports; supersession preserves past; retrospective corrections and present permissions follow existing Trace semantics. Observed prefix support grounding, never gold rules |
| Accounting contract | READY_TO_FREEZE | One serial arm ledger/executor; non-mutating reservation; actual reconciliation; unknown/overrun retention; staged released calls with carry, no negative refunds or historical credit reset |
| Cache policy | READY_TO_FREEZE | Cold arm-local namespaces; material identity/invalidation; physical vs reused work; B8 legal reuse, B10/readout no response reuse |
| Shared-compute policy | READY_TO_FREEZE | Common immutable inputs; explicit same-artifact/same-condition proposal sharing, equal original-cost allocation and separate physical ledger; no free B7/B9 construction |
| Experiment manifests | READY_TO_FREEZE | Source/config/prompt/schema/runtime hashes, original usage/attempts, allocations, counters, cache scope, separate local/physical/runtime timing, current versus evidence clock, failure outcomes |
| Failure taxonomy | READY_TO_FREEZE | Protocol/semantic/transport/refusal/timeout/truncation/budget categories retained; future/oracle prefix rejection is protocol_violation and cannot score as success |
| Statistical unit/oracle boundaries | READY_TO_FREEZE | Source/scenario family; repeated revisions/queries/seeds are not independent units; explicit O-level diagnostics excluded from ordinary arms |
| Stress strength/practical margins/final horizon and study approval | NEEDS_DEVELOPMENT_DATA | Development/adjudication, resource feasibility and stakeholder approvals required; provisional constants are not promoted to selected values |
| Claude/two-backbone study execution | BLOCKED | Credentials/access and actual run unvalidated. External operational dependency for the proposed two-backbone study, not additional infrastructure needed before annotations; not an independent API-only R1 gate |

No unfinished code issue has been identified that needs work before independent annotation. READY_TO_FREEZE contracts should stop changing unless a concrete defect or adjudicated development finding requires it. Human signatures, final dataset/split/mask hashes and selected numerical parameters remain outside this non-human engineering snapshot. No Annotator A/B files were changed.
