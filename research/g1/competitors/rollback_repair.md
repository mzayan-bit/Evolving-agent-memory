# Rollback Repair

## Exact Citation

Yu, Caili, Wang, Yiqi, Zhang, Jiaqi, Duan, Yiqun, Zheng, Mingkai, Wu, Zhangkai, Shi, Kaize, Cai, Taotao. (2026). *From Faulty Memories to Corrected Actions: Dependency-Guided Rollback Repair for Memory-Augmented Agents*. [arXiv:2608.10502](https://arxiv.org/abs/2608.10502v1).

## Version Audited

Paper version: v1 for each paper above; latest located at the cutoff.

Repository: No attributable official repository located.

Commit/tag: Not available.

Dataset version: No independently versioned release located.

Date inspected: 2026-09-21; novelty cutoff: 2026-09-20. Later material is not novelty evidence. Source archives and supplementary files were inspected, not only abstracts.

## Evidence Pointers

[R paper](https://arxiv.org/html/2608.10502v1): Method; Benchmark; Experiments; appendices Rollback Rules, Data Schema, Prompt, Baseline, Metrics, Fault Injection, Additional Results, Adapted LongMemEval-V2. Exact source paths in the arXiv source archive: `sections/03_method.tex`, `04_benchmark.tex`, `05_experiments.tex`, `appendix/rollback_rules.tex`, `appendix/adapted_lmev2.tex`.

All section references below resolve through these versioned primary sources. “Not demonstrated” is bounded by the inspected material, not proof of global absence.

## Problem Definition

Post-failure recovery given a failed execution and diagnosed faulty memories; recover both answer and reusable state while retaining unaffected work. [R Method]

## Unit of Persistent State

Typed memory, derived claim, action and trace nodes; persistent memory is deactivated and subsequent writes/replay can restore it. [R Method/Data Schema]

## Dependency Representation

Runtime provenance and explicit computational dependence, not an embedding-neighbor graph. Type-specific reachability determines candidate impact; independent trusted support can rescue candidates. [R Method/Rollback Rules]

## Dependency Completeness Assumption

Recorded runtime links define the candidate closure. Missing implicit semantic links are outside the claimed guarantee. This is narrower than assuming every real-world causal relation is logged. [R Method/limitations]

## Missing Dependency Behavior

An omitted true path can leave a contaminated descendant outside rollback; this is our inference from the traversal, not a measured error rate. No missing-edge sweep located. [R Rollback Rules]

## Spurious Dependency Behavior

A false path expands candidate scope; trusted-support checking may spare a candidate, otherwise extra invalidation/replay is possible. No controlled false-link sweep located. [R Rollback Rules]

## Alternative Support

YES: independent trusted support explicitly preserves candidates. G1 cannot claim the first alternative-support-aware rollback. Trust/support validity is supplied by the protocol rather than calibrated latent-support inference. [R Method; support-check ablation]

## Conjunctive Support

Multiple computational parents can be recorded. A general AND/OR justification algebra with alternative conjunctions is not separately established; do not mistake a multi-parent list for that algebra. [R Data Schema/Rollback Rules]

## Correlated / Copied Evidence

Provenance distinguishes origins at runtime; learned duplicate/correlated-source inference and shared-origin uncertainty are not evaluated. [R Method]

## Fault Identity

Diagnosed faulty IDs are given. Detecting the original fault is not the recovery task. [R problem definition/Fault Injection]

## Scope Knowledge

Graph closure plus answer relevance scopes replay. Gold injected fault and controlled trace construction make diagnosis and provenance substantially easier than raw-history deployment. [R Benchmark]

## Repair Actions

Deactivate unsupported memory, invalidate derived claims, retain independently supported/benign nodes, selectively replay affected answer-relevant steps, regenerate answer and memory writes. [R Rollback Rules]

## Persistent vs Query-Time Repair

Persistent repair AND answer/trace recovery; not merely a response editor. [R Method]

## Repeated Revisions

One diagnosed failure/recovery per evaluated case; no factorial longitudinal v1→v2→v3→v4 support-revision test located. Recurrence is measured but is not the same experiment. [R Benchmark/Metrics]

## Historical Queries

Trace preservation does not demonstrate time-indexed historical QA after repeated supersession. [R Metrics]

## Domain Shift

Three controlled domains and a trajectory-derived external adaptation; no held-out semantic lineage estimator transfer experiment. [R Benchmark/Adapted LongMemEval-V2]

## Uncertainty

No empirically calibrated posterior over missing/spurious support sets located. Trusted support is an operational rule. [R Method]

## Cost Accounting

Replay steps, total tokens and LLM-call overhead reported. Cost-breakdown table: 12,697.55 tokens/5.70 calls for rollback versus 28,175.28/9.80 for LLM-judge repair; thus the reported recovery gain is not simply purchased with more total compute in that comparison. Selective versus full replay is a meaningful cost comparison, but not a complete equal-token/evidence/verification frontier for uncertain support. [R Experiments/Baseline]

## Dataset

150 controlled cases across three tool-use domains and four failure types; injection retained when it caused a wrong answer and downstream acceptance. Additional 50 adapted LongMemEval-V2 trajectories. This is a selected recovery population. [R Benchmark/Fault Injection]

## Metrics

Recovery, faulty-memory removal, benign preservation, claim invalidation precision/recall/F1, replay/calls and recurrence. Reuse these distinctions rather than rename them as G1 metrics. [R Metrics]

## Main Results

Author reports: controlled recovery 85.3% versus 77.3% best competing recovery; benign preservation 100%; adapted recovery 68.0% versus 54.0%, invalidation F1 .669 versus .603. These are conditional on the selected cases and known faults. [R main results; adapted appendix]

## Relevant Ablations

Removing trusted-support checking raises recovery 85.3→88.0% while benign preservation falls 100→98.6%; replay/call overhead rises. This is already a repair–preservation tradeoff, not an unstudied concept. [R Additional Results]

## Failure Cases

Supplemental backbone table reports Gemini recovery .733 versus LLM-judge .740, so even recovery is not universally superior. Main GPT-4o recurrence is .266 versus .121 for LLM-judge, and claim-invalidation F1 .566 versus .946. Stale-fault subset recurrence is .781, despite .941 recovery. These are particularly important counterexamples to equating answer recovery with clean persistent state. Not uniformly best trace reconstruction; preserved alternative evidence can coexist with residual answer errors. Incomplete recorded provenance remains an untested failure mode. [R results/limitations]

## Author-Stated Limitations

Controlled injection, recorded provenance, diagnosed faults and limited domains constrain generalization. [R limitations]

## Additional Limitations Observed From Code / Protocol

No attributable executable repository from abs-page links, source archive, exact-title and GitHub repository searches. No runtime verification of support rescue possible here. Absence of code is a reproducibility limitation, not novelty evidence.

## Exact Overlap With G1

Closest single repair mechanism: selective persistent rollback, independent-support preservation and recovery cost are already present.

## Exact Difference From G1

The unresolved joint test is ambiguous/missing/spurious support with shared origins, repeated revisions and equal information plus equal verification/replay resources. Neither a graph nor alternative-support rescue alone distinguishes G1.

## Could This Paper Kill G1?

PARTIALLY. Kills broad method framing; could kill narrow G1 if its support check already achieves the same frontier under the proposed stressors.

## Missing Experiment That Would Most Threaten G1

Use identical initial memories and query schedules; corrupt only visible support links, preserve evaluator gold, add an independent alternative and a copied alternative, apply three revisions, and compare rollback+support-check against support-set truth maintenance and conservative reverify at identical budgets. Freeze fault/scope access. Report stale reuse and false invalidation jointly.

## Reproduction Status

**could not reproduce: executable official release not located; paper/source inspection only**. No paper accuracy number in this audit is a new measurement. See [release and smoke ledger](../REPRODUCIBILITY.md).
