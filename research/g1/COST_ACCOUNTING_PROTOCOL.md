# Cost accounting and matching

Count **all phases**: initial memory construction, lineage extraction, maintenance, diagnosis, candidate retrieval, verification, repair, replay, answering and summary rewrites. Report setup and amortized per-query costs separately with an explicit query horizon. A shared frozen representation is charged equally to all arms in the policy-isolation experiment; end-to-end runs charge each arm its real construction costs.

Per-operation ledger: scenario/revision/policy/backbone/seed, phase, model/checkpoint/version, input/output/cached tokens, call count, embeddings (items/tokens), retrieval count and returned items, tool calls, verifier calls, replay steps, wall latency, errors/retries, provider pricing snapshot, monetary cost if applicable, local device/runtime and energy only if actually measured. Store no secrets. Count failed calls/retries and unsuccessful checks. Do not estimate local cost as zero.

## Two mandatory views

1. Unrestricted operation: each baseline runs its declared algorithm to completion; report resource use, quality and a Pareto plot. This reveals when full replay is cheap enough to dominate.
2. Matched resources: common verifier model, evidence pool, maximum input/output context, retrieval cap and per-trajectory verification/replay credit cap. Initial reference cap is **6 repair credits per three-revision trajectory** (two per revision, unused credits carry forward); a credit is one call to the common verifier OR one replay step with the common model and per-call token cap. Token caps are an additional binding constraint, not inferred from credit equality. Diagnose/extract calls consume the same cap unless supplied identically to every arm. Broader caps 0/3/12 are a later sensitivity plan.

A replay step can include several internal calls: charge each actual model call and step, never hide a sequence behind one credit. Tool/retrieval calls are capped and logged separately; equal verifier calls alone does not establish equal compute. Algorithms that cannot finish within the cap return their last admissible state and a budget-exhaustion status. Full replay is not silently exempt; report completed replay separately from truncated replay.

## Price, latency and evidence fairness

Dollar cost at execution time = sum over provider-specific input/output/cached token and tool charges using archived rates, plus separately reported local hardware time/cost model. Do not compare 2026 prices from memory. Freeze a pricing date and show token/call metrics so later repricing is possible. Latency: warm/cold start separately, same device/server mode, cap concurrency, randomize order, report median/P95 with queue/network conditions. Do not confuse parallel calls with lower total compute.

Every method receives the same accessible source text, provenance and authority labels. Equal evidence **opportunity** (same bounded source pool) and equal evidence **realization** (a precomputed common verification bundle) are separate experiments. The latter isolates decision policy; the former tests selection policy. If a method acquires extra evidence, charge it and give baselines the same access. Gold graph, gold affected scope and future facts never enter the main matched arm.

## Dominance and practical value

Publish quality at each realized cost and feasible operating point. A method dominates only if it is no worse on stale reuse, false invalidation and task completion at no greater resources, with uncertainty stated. Do not claim advantage from a stronger model, larger context or uncharged write pipeline. StateAuditor already has matched controls; CAMA’s accuracy-per-token table is useful but does not replace a matched experiment. [Competitor costs](CLOSEST_WORK_AUDIT.md).

## Implementation delta — 2026-09-26

See [REAL_RESOURCE_ENFORCEMENT.md](REAL_RESOURCE_ENFORCEMENT.md) for implemented cumulative input/output/total/call/verifier/replay reservations, actual usage reconciliation, unknown/overshoot stopping, retry charging and cache fairness. Versioned post-hoc prices are separate from policy logic. This replaces the prior “counters only” implementation limitation for model execution **offline**; live validation remains absent. The candidate revision-credit release schedule remains unimplemented and cannot be inferred from cumulative caps. B8 now reports dependency-check counts even on cache hits. Use trajectory wall latency once; phase latency is nested, not additive elapsed time.
