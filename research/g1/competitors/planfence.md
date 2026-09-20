# Planfence

## Exact Citation

Chen, Evan, Wang, Shiqiang, Brinton, Christopher G.. (2026). *Fresh Memory, Stale Plans: Dependency-Scoped Validation for Distributed LLM-Agent Memory*. [arXiv:2609.03340](https://arxiv.org/abs/2609.03340v1).

## Version Audited

Paper version: v1 for each paper above; latest located at the cutoff.

Repository: No attributable official repository located.

Commit/tag: Not available.

Dataset version: No independently versioned release located.

Date inspected: 2026-09-21; novelty cutoff: 2026-09-20. Later material is not novelty evidence. Source archives and supplementary files were inspected, not only abstracts.

## Evidence Pointers

[P paper/source](https://arxiv.org/html/2609.03340v1): problem/system model, PlanFence algorithm, evaluation and Appendix C dependency-completeness/over-approximation sensitivity. Source `main.tex`.

All section references below resolve through these versioned primary sources. “Not demonstrated” is bounded by the inspected material, not proof of global absence.

## Problem Definition

Prevent execution of plans derived from obsolete state although the local memory itself appears fresh. [P problem]

## Unit of Persistent State

Distributed memory records, per-owner versions, plans and dependent actions. [P system model]

## Dependency Representation

Explicit plan/action read sets D(a), owner heads and dependency versions; operational execution dependence, not semantic similarity. [P algorithm]

## Dependency Completeness Assumption

The safety guarantee needs relevant action dependencies covered and correct owner validation. Appendix C explicitly examines violated completeness/over-approximation. [P model; App.C]

## Missing Dependency Behavior

YES tested. At 50% omission, unsafe execution reaches 37.4% in the sensitivity experiment. This alone kills any first missing-edge test claim. [P App.C]

## Spurious Dependency Behavior

YES extra dependencies tested: checks increase from 4 to 36 in the reported over-approximation setting. Safety/cost tradeoff already studied for action validation. [P App.C]

## Alternative Support

An action read-set fence does not implement alternative sufficient justifications for a belief; a changed listed dependency prompts validation/replan even if another justification could suffice. [P algorithm]

## Conjunctive Support

All declared dependencies must be current for admission, an operational conjunction. This is not a general sufficient-support formula over alternative evidence. [P algorithm]

## Correlated / Copied Evidence

Versioned owner state, not inference of shared origins among duplicated natural-language evidence. [P model]

## Fault Identity

Does not need a diagnosed faulty memory: detects version mismatch. Owner versions and dependency identity are available. [P algorithm]

## Scope Knowledge

Action dependency set is declared by the tool/plan contract; stale version comparison is authoritative. [P model]

## Repair Actions

Validate, admit, replan once or block. Synchronization baselines update memory. No demonstrated persistent belief-support repair. [P algorithm]

## Persistent vs Query-Time Repair

Action-time validation/replanning, not query-text editing and not general persistent-memory invalidation. [P model]

## Repeated Revisions

Churn/replay evaluates changes over executions; not an explicit support-revision v1→v4 test with historical beliefs. [P evaluation]

## Historical Queries

Historical QA is outside the task. [P problem]

## Domain Shift

Three controlled workflows; no natural-language inferred-lineage domain shift experiment. [P evaluation]

## Uncertainty

Deterministic version checks; no calibrated distribution over support structures. [P model]

## Cost Accounting

Checks, communication/validation overhead and unsafe actions are evaluated under churn. Eager synchronization can be better at low churn. No LLM semantic-verification budget frontier. [P evaluation/App.C]

## Dataset

30 live controlled cases across three workflows, intentionally changing state after planning; replay experiment covers 32,700 actions. [P evaluation]

## Metrics

Unsafe/stale action execution, validation/check overhead and freshness-related behavior. [P evaluation]

## Main Results

Freshness-only misses all 30 designed live stale-plan cases while gate prevents their unsafe execution; this is a constructed stress-test result, not deployment prevalence. [P live evaluation]

## Relevant Ablations

Dependency omission, over-approximation, churn and synchronization alternatives. [P App.C/evaluation]

## Failure Cases

Omitted dependency defeats safety; over-approximation raises cost; low churn can favor eager synchronization. [P App.C]

## Author-Stated Limitations

Inferred dependencies, semantic conflict merging, Byzantine behavior and atomic check-to-act guarantees are outside the stated model. [P limitations]

## Additional Limitations Observed From Code / Protocol

No attributable executable release located in source/abs/exact-title and GitHub search. Third-party repositories mentioning PlanFence are not author code. Cannot run live tool-contract reproduction.

## Exact Overlap With G1

Lineage incompleteness/spurious links and cost already affect selective correction, at the action boundary.

## Exact Difference From G1

Persistent semantic support validity, independent alternative support, latent shared sources and calibrated repair remain outside the evaluated object.

## Could This Paper Kill G1?

PARTIALLY. Kills “noisy dependency graphs have never been tested.” If actions are our only useful endpoint, this may be the correct existing solution.

## Missing Experiment That Would Most Threaten G1

Compare declared versus inferred D(a) with AND/OR justifications and persistent stored descendants, while holding owner evidence and action costs fixed. Test whether persistent repair adds value over a fence on every action.

## Reproduction Status

**could not reproduce: executable official release not located; paper/source inspection only**. No paper accuracy number in this audit is a new measurement. See [release and smoke ledger](../REPRODUCIBILITY.md).
