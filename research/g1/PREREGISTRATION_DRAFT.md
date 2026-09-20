# G1 preregistration draft — not registered, not final

Version 0.1, prepared after literature/code audit and before model experiments. The 30 AI-authored cases have been inspected and are development data. There are no human labels or experimental outcomes. Human agreement, case corrections and cost dry-run must precede a final frozen protocol. Any post-outcome changes become exploratory and are logged.

## Motivation and questions

Determine whether support uncertainty materially affects persistent memory repair beyond classical support maintenance and simple replay. RQ1–5 are frozen in [claim](G1_CLAIM.md): missing/spurious effects, alternative support, budgeted headroom, repeated revisions/shift and causal attribution to inference/evidence/policy.

## Hypotheses

H1: corrupting support increases stale reuse or false invalidation for at least some deterministic point policies. H2: support-set semantics preserve independently supported claims better than naive closure on relevant cases. H2 is a classical prediction, not method novelty. H3: under equal evidence/resources, strong simple baselines leave practically meaningful residual headroom. H3 is uncertain and may be false. H4: any effect is not confined to templates or one backbone. No hypothesis claims an unimplemented uncertainty method wins.

## Outcomes

Primary: scenario-macro SDRR at the frozen resource cap and paired stress contrast. Guardrails: FIR, valid quarantine/nonavailability, current and historical accuracy. Secondary: independent-support retention, repair precision/recall, recurrence, action correctness, coverage and resource ledger. Definitions and NA conventions in [metrics](VARIABLES_AND_METRICS.md). No arbitrary new metric family replaces the joint tradeoff.

## Data and splits

Exactly 30 current development scenarios (12 attributed STALE adaptations, 18 original). Independent human review/adjudication required. Planned baseline pilot: 12 new human-reviewed cases, eight development/calibration and four held-out domain/template cases, 384 trajectories under the [pilot](PILOT_DESIGN.md). This small held-out slice is exploratory. Confirmatory expansion uses new source scenarios and frozen sample size from variance/cost; no test-driven selection. Group by source/origin/template across splits.

## Baselines and information

No repair, source-only, full reset/replay with archive, recorded closure, semantic-neighbor invalidation, point inferred graph, conservative reverify/replay, and point support-set TMS/rederive. All receive the [same permitted information](INFORMATION_ACCESS.md). Separate gold-support upper bound. No future facts/gold affected scope. Known-source and unknown-diagnosis tracks remain separate.

## Cost matching

Unrestricted and matched-resource reports. Initial planned matched cap six credits per three-revision trajectory plus common per-call/token/retrieval caps; exact token/dollar caps frozen after dry run, before comparative pilot outputs. All write, infer, verify, retrieval and replay stages charged. Shared evidence realization is the policy-isolation condition. [Cost protocol](COST_ACCOUNTING_PROTOCOL.md).

## Statistical unit, intervals and comparisons

Scenario clusters, paired repeated measures; bootstrap whole scenarios with all dependent outputs retained. One primary stress contrast, predeclared strong baseline comparisons; Holm only for a confirmatory multi-test family. Report macro/micro distinctions and per-backbone/regime results. [Statistical plan](STATISTICAL_PLAN.md). Pilot p-values are not grounds for a broad positive or null claim.

## Seeds and execution freeze

One paired seed in initial pilot, later three if expansion warranted. Freeze model IDs/checkpoint hashes, prompts, generators (if any), corruption masks, scoring rubric, environment, retry/timeout caps and run manifest. Document nondeterministic providers. No model training in this phase.

## Exclusion rules

Before freeze only: duplicate scenario, inaccessible licensed evidence, incoherent scope/time or non-adjudicable intended-determinate gold. Preserve genuine ambiguous cases in their own stratum. After freeze: infrastructure failure rules only, with all attempts/costs and sensitivity bounds retained. Wrong outputs, parse failures, high cost, poor performance and ambiguity are not post-hoc exclusion grounds.

## Leakage and judges

Development-only public adaptations; independent human-authored held-out scenarios; no same-family generation/evaluation/judging loop. Prefix-only runtime, hidden gold/provenance masks, blinded semantic equivalence judge, deterministic state/action checks, human review and disjoint-family rejudging. [Detailed safeguards](PILOT_DESIGN.md).

## Failure and stopping/expansion

Apply [kill criteria](KILL_CRITERIA.md). Stop for unreliable ontology, no meaningful uncertainty signal, simple-baseline dominance, disappearance under matching, failed shift or negligible practical value. Expand only if signal/headroom and cost justify it. Do not start an uncertainty-method implementation merely because the audit failed to find the exact joint experiment.
