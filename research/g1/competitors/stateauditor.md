# Stateauditor

## Exact Citation

Sun, Haofei, He, Lin. (2026). *When Memory Updates but Behavior Does Not: Repairing Implicit Stale Dependencies in Personalized Agent Responses*. [arXiv:2608.01619](https://arxiv.org/abs/2608.01619v1).

## Version Audited

Paper version: v1 for each paper above; latest located at the cutoff.

Repository: No attributable official repository located.

Commit/tag: Not available.

Dataset version: No independently versioned release located.

Date inspected: 2026-09-21; novelty cutoff: 2026-09-20. Later material is not novelty evidence. Source archives and supplementary files were inspected, not only abstracts.

## Evidence Pointers

[S paper](https://arxiv.org/html/2608.01619v1); [S supplement](https://arxiv.org/src/2608.01619v1/anc/supplementary.pdf), 16 pages. Main system/results/limitations; supplement §§1–2 scope/alignment, §13 exact prompts, §14 additional analyses and Table 12 claim–evidence ledger. Supplement pp.14–16 were also visually checked. Do not conflate scenario-joint, strict-query, external component and external full-pipeline experiments.

All section references below resolve through these versioned primary sources. “Not demonstrated” is bounded by the inspected material, not proof of global absence.

## Problem Definition

Find implicit stale premises in a personalized response even after stored memory has updated, then authorize and apply response repair. [S system]

## Unit of Persistent State

Structured dated memory entries are input; generated premises, transition paths, directives and a revised response are the audit objects. No persistent-store mutation established by the evaluated response pipeline. [S system; supplement algorithm sketch]

## Dependency Representation

LLM-inferred draft- and state-anchored premises plus old→new transition paths; deterministic quote/chronology checks verify entry provenance, not semantic entailment. [S system; supplement §14]

## Dependency Completeness Assumption

Hidden dependencies are inferred, not assumed fully logged. A missing premise/path or retrieval miss can evade the audit. [S supplement failure taxonomy]

## Missing Dependency Behavior

Retrieval and inferred-path misses explicitly analyzed: 52/145 joint-run failures retrieval-related, 33/145 no verified stale path. This is not a controlled persistent-store edge-deletion sweep. [S supplement §14]

## Spurious Dependency Behavior

Injected bad transition candidates are tested. Gate rejects chronology/quote defects but accepts all 290 semantically non-superseding, correctly dated candidates; semantic checking reduces over-correction. Not a persistent graph false-link sweep. [S supplement §14]

## Alternative Support

Compatible/coexisting valid values and over-correction traps are tested. General independent OR support-set preservation across source retractions is not isolated. [S hard confirmation, p.16]

## Conjunctive Support

Implicit multi-step premise paths and multi-attribute cases; no explicit general AND/OR support-set model with persistent repair. [S system; hard confirmation]

## Correlated / Copied Evidence

Quote provenance is not independent-source clustering; no copied-evidence uncertainty evaluation located. [S system]

## Fault Identity

No gold faulty ID is needed at runtime; the proposer infers stale premises. Offline gold-session alignment is evaluator-only. [S supplement §2]

## Scope Knowledge

Scenario-joint run pools SR/PR/IPA evidence, unlike isolated STALE queries; strict confirmation fixes this. HorizonBench store is constructed from gold from→to preference changes, limiting inference claims. [S supplement §§1,14]

## Repair Actions

Retrieve, audit VALID/STALE/UNKNOWN, propose/validate transitions, issue typed response-repair directives, regenerate/pass through or abstain. Semantic verifier is a measured extension. [S system; prompts]

## Persistent vs Query-Time Repair

Query/response repair. The word “persisted” in candidate telemetry means saved transition records, not proof that future agent memory is repaired. [S algorithm sketch and §14]

## Repeated Revisions

Cyclic A→B→A appears in the hard confirmation set. This is partial repeated-revision evidence, not a persistent-memory longitudinal repair frontier. [S p.16]

## Historical Queries

Temporal evidence and other memory benchmarks are considered; systematic retention of previously true records across persistent repair is not established. [S experiments]

## Domain Shift

HorizonBench full pipeline transfers, but incremental transition machinery versus matched no-transition control is non-significant (10:5 flips, p=.30). Hard cross-family lifecycle set shows no accuracy benefit. [S pp.15–16]

## Uncertainty

Lifecycle UNKNOWN and proposer abstention exist. Semantic verifier recall .819/specificity .885 are classifier performance, not probability calibration. Judge agreement is not lineage calibration. [S supplement §14]

## Cost Accounting

Strict matched evidence/adapter/call controls are a serious prior cost control. Additional semantic checks: 165 on hard confirmation. Reported latency is serving-stack dependent. [S main results; supplement §§9,14]

## Dataset

STALE 400 cases; strict independent-query confirmation; safety regimes; HorizonBench adapted stores; hard cross-family 120 cases, 20 each of six stress categories. Distinguish original histories from gold-structured store adaptations. [S experiments; supplement]

## Metrics

SR/PR/IPA correctness, false invalidation/repair triggers, current-value accuracy, stale reversion, judge/human agreement, paired flips and costs. [S metrics; supplement Table 12]

## Main Results

Author reports strict .736 versus matched .692; scenario-joint .879 is not official-protocol SOTA. Hard confirmation deterministic .533 versus .542 predecessor; semantic .600 versus .633. External full pipeline .458 versus .417 matched control, non-significant. [S results; supplement pp.15–16]

## Relevant Ablations

Provenance gate versus proposal/transition machinery, matched no-transition control, semantic gate, development ladders and cross-family judges. Hard semantic gate reduces trap repairs 18→6, preserves 57/58 true-supersession repairs, leaves deterministic accuracy .533. [S supplement §14]

## Failure Cases

Semantically compatible later events pass the provenance gate; hard-set world knowledge, binding and genuine ambiguity limit performance. Human VTA A/B raw agreement .700 with κ=.126 on 100 cells warns against treating judge labels as unquestionable. [S supplement Table 1, §14]

## Author-Stated Limitations

Quote/chronology validity does not imply semantic supersession; stronger claims do not transfer to the harder authored set. [S limitations; Table 12]

## Additional Limitations Observed From Code / Protocol

Supplement repeatedly names released scripts/JSON but no attributable executable archive/repository link was located in the accessed release/search. Exact prompts are inspectable; named filenames do not establish accessible code. No code performance reproduced.

## Exact Overlap With G1

Hidden dependency inference, uncertainty labels, response repair, semantic ambiguity, false invalidation and matched controls already exist. Kills “first implicit-dependency repair” and “first cost-controlled audit.”

## Exact Difference From G1

Persistent memory survival/recurrence and explicit uncertain support-set interventions remain different outcomes. Merely adding cyclic revisions or an UNKNOWN label is insufficient.

## Could This Paper Kill G1?

PARTIALLY. Strongest empirical warning: hard lifecycle gains vanish. It may make G1 practically uninteresting even if persistent-state outcomes differ.

## Missing Experiment That Would Most Threaten G1

Apply StateAuditor with a clearly declared persistent-write adapter, cost it fully, and test subsequent unsignaled reuse under missing/spurious support and independent versus copied alternatives. Compare with query-only StateAuditor on identical evidence; persistence must provide additional measured value.

## Reproduction Status

**could not reproduce: executable official release not located; paper/source inspection only**. No paper accuracy number in this audit is a new measurement. See [release and smoke ledger](../REPRODUCIBILITY.md).
