# Cama

## Exact Citation

Lin, Chenchen, Yuan, Wenhao, Wang, Xuehe, Ngai, Edith Cheuk Han. (2026). *Beyond Memory Majority: Latent-Source Reasoning for Multi-Agent Memory Arbitration*. [arXiv:2608.19701](https://arxiv.org/abs/2608.19701v1).

## Version Audited

Paper version: v1 for each paper above; latest located at the cutoff.

Repository: No attributable official repository located.

Commit/tag: Not available.

Dataset version: No independently versioned release located.

Date inspected: 2026-09-21; novelty cutoff: 2026-09-20. Later material is not novelty evidence. Source archives and supplementary files were inspected, not only abstracts.

## Evidence Pointers

[C paper](https://arxiv.org/html/2608.19701v1): Methodology (Query-Conditioned Evidence Decoupling; Factor-Level Conflict Arbitration; Active Independent-Evidence Recovery; Evidence-Guided Recovery Optimization), Experiments, Algorithm, Detailed Dataset Descriptions, Ablation Study, Efficiency Analysis, Prompt Used. Source `Preprint.tex`; equation labels `eq:arbitration-posterior`, `eq:terminal-reward`, `eq:dependence-loss`.

All section references below resolve through these versioned primary sources. “Not demonstrated” is bounded by the inspected material, not proof of global absence.

## Problem Definition

Arbitrate correlated/conflicting multi-agent memories without counting many copies as independent votes; acquire missing independent evidence for a query. [C Methodology]

## Unit of Persistent State

Retrieved memories, provenance, latent query-conditioned source slots and factor-level hypotheses; no evaluated persistent support-retraction state machine. [C problem/inference algorithm]

## Dependency Representation

Neuro-symbolic soft memory-to-slot assignments with provenance priors plus set encoder; latent source dependence, not deterministic logged repair reachability. [C evidence decoupling]

## Dependency Completeness Assumption

Provenance is supporting evidence, not a hard dependency label. Hidden/query-dependent redundancy is explicitly inferred. Kills first latent-lineage/hidden-dependency claims. [C evidence decoupling]

## Missing Dependency Behavior

Missing independent evidence is recovered by Expand/Trace. This is not a controlled missing true-support edge sweep for future persistent descendants. [C recovery/dataset]

## Spurious Dependency Behavior

Correlation augmentation, dependence ablations and prior strength are tested; no explicit false causal-support link rate sweep for persistent repair. [C dataset/ablation]

## Alternative Support

Independent evidence groups support competing hypotheses. Independent evidence reasoning exists; preserving a persistent belief after retracting one of several sufficient justifications is not isolated. [C arbitration]

## Conjunctive Support

Factor-level hypothesis aggregation is not a demonstrated Boolean sufficient-support hypergraph for persistent derivations. [C equations/inference]

## Correlated / Copied Evidence

YES central contribution: latent source grouping, correlated copies and controlled paraphrase/summarization variants with shared-source provenance. [C dataset/decoupling]

## Fault Identity

Does not require a gold faulty ID at inference; provenance priors are input, latent sources inferred. Controlled correlation construction supplies training/evaluation origin supervision. [C optimization/dataset]

## Scope Knowledge

Query-retrieved memory slice and provenance define accessible evidence. Cannot compare with a baseline denied those traces. [C formulation]

## Repair Actions

Arbitrate, Expand, Trace, Stop, retrieve and answer. No persistent invalidate/quarantine/rewrite action established in the inference algorithm. [C Algorithm]

## Persistent vs Query-Time Repair

Query-conditioned evidence recovery/arbitration. Do not infer persistent-store repair from the word recovery. [C Algorithm]

## Repeated Revisions

Base benchmarks involve evolving interaction history; no isolated multi-revision persistent retraction stress with future recurrence located. [C datasets]

## Historical Queries

LongMemEval/LoCoMo contain historical reasoning; this is task-level evidence, not as-of preservation after repair. [C datasets]

## Domain Shift

Multiple benchmarks/backbones, but no held-out lineage corruption/domain-shift calibration evaluation located. [C experiments]

## Uncertainty

Soft assignments, reliability and hypothesis posteriors exist. No empirical probability calibration/reliability diagram/Brier audit located; scores are not automatically calibrated. [C equations/metrics]

## Cost Accounting

Cost-sensitive learned recovery and budget sensitivity; MemoryAgentBench DeepSeek-V4-Flash efficiency table reports 4.2 LLM calls, 14.6k tokens, 6.7 average latency units as specified by table. RAG 1 call/3.2k. Accuracy per token is not equal-cost comparison. [C Efficiency table]

## Dataset

MemoryAgentBench, LongMemEval, LoCoMo and author-constructed correlation-aware variants from shared sources; independently pinned derivative data release not located. [C Detailed Dataset Descriptions]

## Metrics

Task EM/F1/judge plus correlation metrics CMR, RS, IEG, ERR and resource accounting. None alone establishes stale-descendant repair or false invalidation of persistent state. [C Metric Descriptions]

## Main Results

Author overall-performance table reports MemoryAgentBench 67.3% for CAMA versus 63.4% MADAM-RAG and 51.3% RAG under DeepSeek-V4-Flash; Qwen3.6-27B values are 64.9%, 60.2% and 48.3%. Ablations degrade task/correlation outcomes after removing decoupling/prior/recovery. Do not translate these into persistent-repair improvements. Efficiency table explicitly shows more compute than RAG. [C results/efficiency]

## Relevant Ablations

Without decoupling/provenance prior/Expand/Trace/policy; K retrieved memories, J slots, prior strength and recovery budget. [C Ablation/Hyperparameter Sensitivity]

## Failure Cases

Latent grouping can fragment or merge evidence sources; set-encoder cost grows quadratically with memory slice size. These are representation/cost boundaries, not measured repair failures. [C inference complexity/sensitivity]

## Author-Stated Limitations

No separate limitations section was located. The authors’ formulation/complexity analysis bounds inference to a finite retrieved slice/latent slots and recovery resources; the evaluation constructs correlation variants. No separately identifiable claim of persistently correcting all downstream state. [C formulation/complexity]

## Additional Limitations Observed From Code / Protocol

No official code/dataset link found; source includes commented AAAI example links, which are template placeholders and not releases. Cannot inspect a trained checkpoint or reproduce the learned policy.

## Exact Overlap With G1

Uncertain latent sources, correlation-aware support, active verification/recovery and cost optimization already overlap heavily with any proposed uncertainty controller.

## Exact Difference From G1

The candidate difference is measured persistent-state repair after source revisions under explicit support uncertainty. A posterior plus controller by itself is not a credible contribution.

## Could This Paper Kill G1?

PARTIALLY. Strongest method-novelty threat alongside classical ATMS/provenance; composing it with rollback might be sufficient.

## Missing Experiment That Would Most Threaten G1

Give a CAMA-style evidence grouping baseline the same provenance and retrieval/verification budget, use its grouping to drive classical support retraction, and measure persistent stale reuse/valid retention over three revisions. If this simple composition matches the frontier, abandon a new controller.

## Reproduction Status

**could not reproduce: executable official release not located; paper/source inspection only**. No paper accuracy number in this audit is a new measurement. See [release and smoke ledger](../REPRODUCIBILITY.md).
