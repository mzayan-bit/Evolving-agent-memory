# G1: pre-implementation claim freeze

Status: **B — survives conditionally as a scientific question; method novelty unestablished.** Inspection 2026-09-21, novelty cutoff 2026-09-20. This is an internal hypothesis, not an empirical result or publication-ready claim.

## Problem

A source changes while an agent retains summaries, derived beliefs and action assumptions. Some descendants lose all valid justification, others retain an independent sufficient justification, and some cannot be classified from available evidence. The repair decision must distinguish these states without silently using an evaluator's complete support structure.

## Exact Research Gap

The inspected evidence does not establish a joint, controlled evaluation of **persistent** repair under incomplete/spurious **semantic support structure**, alternative sufficient and correlated support, and repeated revisions, with future stale reuse and false invalidation measured under equal evidence and verification/replay resources. This is an evaluation gap bounded by the [audit](CLOSEST_WORK_AUDIT.md), not a claim that no such work exists.

## Narrow Scientific Claim

**We could characterize when uncertainty about semantic support changes the stale-reuse versus valid-retention frontier of persistent agent-memory repair under matched evidence and compute across repeated revisions.**

The eventual paper must either demonstrate that effect or publish a defensible null/negative analysis. It cannot presently claim that a new probabilistic controller improves anything.

## Why This Matters

A correct current response does not establish that future actions or summaries will stop reusing contaminated state. Conversely, broad invalidation can destroy useful independent knowledge. Persistence matters only if future unsignaled probes expose this difference at meaningful cost; otherwise query-time validation may suffice.

## Closest Prior Work

[Rollback](competitors/rollback_repair.md) is the closest single persistent repair mechanism. [CUPMem](competitors/statemem_cupmem.md) invalidates inferred dependencies persistently, contradicting the initial broad explicit-lineage premise. [StateAuditor](competitors/stateauditor.md) is the closest implicit stale-premise audit with matched controls. [CAMA](competitors/cama.md) already learns latent source dependence and cost-sensitive evidence recovery. [PlanFence](competitors/planfence.md) already tests omitted/excess dependencies at action time.

## What Prior Work Already Solves

Known-fault selective rollback and independent-support rescue; inferred implicit invalidation; UNKNOWN lifecycle states; temporal supersession; action freshness; latent source correlation; active recovery; and cost-controlled response audits all predate this proposal. Classical support environments, provenance expressions and incremental rederivation also predate LLMs. See [non-claims](G1_NON_CLAIMS.md) and [classical audit](CLASSICAL_PRIOR_ART.md).

## What Remains Unresolved

Whether natural semantic justifications can be annotated reliably; whether missing versus spurious support affects future reuse beyond task difficulty; whether simple replay/reverification dominates; and whether any additional decision policy helps after fixing inference quality, evidence and costs. No human agreement or pilot outcomes exist yet.

## Research Questions

1. How do missing versus spurious support relations affect persistent stale descendant reuse and false invalidation, holding textual evidence fixed?
2. Does representing alternative sufficient **support sets** improve decisions over a point graph, and does the gain survive shared-origin evidence? This tests the value of classical representation, not its novelty.
3. Is there headroom beyond point-estimate support-set truth maintenance and conservative reverify at the same verification/replay and token budgets? Only then ask whether uncertainty-aware decisions improve the frontier.
4. Do observed effects survive three revisions, then longer revision depth, and held-out domains/templates/entities?
5. How much change comes from lineage inference, extra evidence, additional computation or decision policy? Isolate them with frozen evidence and frozen inference.

## What changed during this audit

The original premise that dependency-aware repair generally assumes explicit lineage is too broad: CUPMem already infers and persistently invalidates; CAMA uses soft latent source assignments; StateAuditor infers implicit transitions. PlanFence already measures missing/spurious links. Rollback already preserves alternative support. The defensible object is therefore a controlled empirical boundary under joint stresses, not “uncertain dependencies are new.”

## Implementation decision

Do not implement the proposed method now. Obtain two independent human annotation passes, resolve licensing/provenance and ambiguous labels, and approve the baseline-only pilot after those gates. This phase authorizes protocol preparation only; it supplies no evidence that a new controller is needed.
