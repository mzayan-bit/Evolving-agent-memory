# Comparator-arm resource integration

**ENGINEERING VALIDATION ONLY. No pilot or baseline ranking.** Implementation: `arms.py`, `cost.py`, `simulation.py`, and the existing comparator implementations. Starting remote main was verified as `859d4dd047e5f9351ed6951cdfdbcc2ee1e3e6f3`. The pre-existing R1 criteria are unchanged.

## One execution contract

`run_arms` runs B4b/B5a/B5b/B7/B8/B9/B10 serially from the same immutable Scenario, access flags and Budget. Each arm gets its own Ledger, ModelExecutor and create-only cache directory. A pre-existing run directory rejects rather than silently warming later arms. Both unrestricted (`None` caps) and matched (common explicit caps/release schedule) use this path. It is a comparator execution boundary, not a pilot launcher, dataset importer, parameter selector or scientific evaluator.

Scenario/source loading and the supplied initial memories are common immutable input, not an unrecorded model-generation step. No model creates those initial memories in this implementation. Model weights/runtime initialization may be common to the same backend; report startup separately from steady execution. No hidden upstream model-built representation is admitted as free input. A future pipeline that adds such construction must provide its original construction accounting under the shared-compute contract before it can be compared.

For all arms, `report()` exposes model calls, input/output/cache tokens, physical and allocated retries, embeddings, verification, dependency checks, replay steps/nodes, cache hits/misses, phase latency, trajectory runtime, shared proposal artifacts/original costs, arm-specific preprocessing and released credits. Unknown token usage stays unknown. Energy and local currency cost stay unavailable. Physical work and allocated shared work have separate totals; never sum allocated copies across arms as actual machine work. `charged_usage.wall_latency_ms` can contain nested runtime and phase events; it is not elapsed time. Use `trajectory_runtime_ms` for the maintenance trajectory and report later query phases separately.

| Arm | Model calls / tokens / retries | Embeddings / verification | Dependency work / regenerated nodes | Cache / preprocessing |
|---|---|---|---|---|
| B4b | No language calls; no invented language tokens | One encode per text-cache miss; no verifier | Embedding comparison time in local overhead; graph dependency checks not applicable | Arm-local text/model cache; all encodes and hits logged |
| B5a | Own pairwise inference per prefix, including any bounded protocol retry | None | Actual support-candidate examinations in descendant closure; no regeneration | Arm-local exact response cache; own pairwise construction |
| B5b | Own support-set inference per prefix and bounded retry | None | Positive-grounding candidate examinations; no regeneration | Arm-local exact response cache; own support-set construction |
| B7 | Own support-set inference in end-to-end mode; allocated original construction in policy isolation | None | Positive AND/OR fixed-point candidate examinations | No free supplied graph; same support construction contract as B5b |
| B8 | Each actual regeneration consumes a call and returned tokens; no generation retry | None | Dependency checks, hits/misses and staged regenerated IDs retained, including failed transactions | Arm-local generated-descendant cache; public task/provenance binding only |
| B9 | Own support-set inference in end-to-end mode; allocated construction in isolation | None | Descendant scan plus two grounding passes, all candidate checks counted | Same paid support construction; independent-origin rescue has no hidden verifier |
| B10 | No maintenance inference; each actual audit/readout call charged | One verification per audit; repeated queries pay again | Temporal projection/grounding checks and local time recorded; no persistent regeneration | Audit/readout response reuse disabled; persistent state unchanged |

A model-call counter is physical dispatch, not the sum of overlapping verification/replay purpose counters. One B8 generation records both one model call and one replay step, but consumes one released call credit. Cache misses in the top-level report mean non-reused physical model/embedding work; B8 additionally records logical lookup misses, which can include a subsequent predispatch denial. Retries allocated from a shared construction are distinguished from physical retries in that arm.

## Construction fairness and B8 access

End-to-end B5a, B5b, B7 and B9 each pay for their own support inference. B5a elicits pairs; B5b/B7/B9 elicit support sets. In policy isolation, SharedSupports.construct uses a real executor with response reuse disabled; its immutable proposal/cost bundle binds to the visible prefix. Every applicable receiving arm must be declared and receive the same bundle. Missing recipients, wrong prefixes and cost-free inferred bundles reject. A trial ledger checks the entire allocation before the artifact is used. Original construction costs remain inspectable even when an arm cannot afford the allocation. Derived status differences caused by prior maintenance are allowed; source status, content, scope, provenance and the prefix checkpoint must match. This is explicitly the common-proposal isolation experiment, not separately elicited pairwise B5a.

B8 does not receive an uncharged gold dependency graph. Its supplied task instructions are common experiment inputs, and its dependency IDs must equal the target's recorded `source_ids`, visible to the other arms under the same access flags. Public source-version replacements rebind those inputs; unknown provenance or an invented dependency fails instead of being guessed from gold. This is the existing explicit execution/provenance replay scope, not a claim of discovering arbitrary missing dependencies or replaying arbitrary tools/cycles. B8-generated content now survives the shared trajectory commit; non-visible metadata is restored as before.

## Common query and threshold configuration

Every supplied probe executes for every arm at its declared revision, before later revision credits are released. B10 uses its existing audit; the other arms use ordinary model readout. Historical evidence time does not change this dispatch schedule. A late attempt to replay an earlier dispatch checkpoint is rejected rather than borrowing newer credits. The boundary exposes existing threshold settings without selecting them; all recipients of shared proposals must use the same threshold. Defaults remain engineering defaults.

## Credits and reservations

The existing candidate two-credit-per-revision schedule is now expressible as `((1, 2), (2, 2), (3, 2))`, with a separate cumulative cap of six. This implements the candidate mechanism; it does not select that numeric budget for the scientific study. `Ledger.release` advances monotonically, is idempotent for the same checkpoint, and never removes past costs. Unused released credits carry. A call cannot borrow unreleased future credits. Historical queries spend against the current released ledger; evidence-time is not a budget reset.

Reservation is a non-mutating probe of the complete ledger, including release state. On completion, only actual returned usage is charged. A cache hit precedes reservation and spends no new model call/tokens; old charges remain. There is no negative refund event. Failed/unknown/overrun calls remain charged and stop subsequent dispatch as before. Post-operation local timing is retained even after exhaustion; recording it does not authorize new work. The supported driver is serial, with one executor per ledger; concurrent executors sharing a ledger remain unsupported.

## Validation

Focused tests in `test_arm_temporal_integration.py` execute all seven existing arms through this boundary with deterministic offline doubles: separate namespaces, paid B7/B9 construction, identical shared allocations, cap rejection before receiving a shared artifact, B8 content commit/unaffected reuse, repeated B10 cost, credit carryover, release of unused token reservation, no negative refunds, failure-cost preservation, temporal isolation and material cache invalidation. Existing response/derived-cache identity tests cover prompts, model/deployment, schema, settings, input, dependency version, scope and clock-sensitive changes.

The checked-in `integration/offline-arm-accounting.json` is an **offline accounting receipt**, not measured model performance. The separate four-call real Qwen temporal receipt validates the new historical boundary. Earlier real B5/B8/B10 traces remain in qwen_hardening and qwen_local; no new support sweep or semantic tuning was performed. Final results and the stop/readiness decision are in NON_HUMAN_PROTOCOL_SNAPSHOT.md.
