# Statemem Cupmem

## Exact Citation

Fan, Xinyi, Liu, Miri, Yang, Ruozhen, Ouyang, Siru, Han, Jiawei. (2026). *Can Agent Memory Systems Track Evolving State?*. [arXiv:2608.19652](https://arxiv.org/abs/2608.19652v1).

Chao, Hanxiang, Bai, Yihan, Sheng, Rui, Li, Tianle, Sun, Yushi. (2026). *STALE: Can LLM Agents Know When Their Memories Are No Longer Valid?*. [arXiv:2605.06527](https://arxiv.org/abs/2605.06527v1).

## Version Audited

Paper version: v1 for each paper above; latest located at the cutoff.

Repository: [STALE/CUPMem](https://github.com/icedreamc/STALE/tree/ea7d391103a151927cd29d2f01d87597a782bdcb); no attributable StateMem repository located.

Commit/tag: ea7d391103a151927cd29d2f01d87597a782bdcb.

Dataset version: [STALE](https://huggingface.co/datasets/STALEproj/STALE/tree/617c51dc200b5ab09970834144c7e51c77959af0), commit `617c51dc200b5ab09970834144c7e51c77959af0`; StateMemBench independently versioned release not located.

Date inspected: 2026-09-21; novelty cutoff: 2026-09-20. Later material is not novelty evidence. Source archives and supplementary files were inspected, not only abstracts.

## Evidence Pointers

[T StateMem paper](https://arxiv.org/html/2608.19652v1): StateMem method, StateMemBench construction, experimental results and appendix. Source `AnonymousSubmission2027.tex`.

[U STALE paper](https://arxiv.org/html/2605.06527v1), CUPMem method and Appendix A.7 release/license. [U code at audited commit](https://github.com/icedreamc/STALE/tree/ea7d391103a151927cd29d2f01d87597a782bdcb): `cup_mem/write/invalidation_lanes.py`, `invalidation_merge.py`, `invalidation_judge.py`, `writer.py`, `store_layer/transitions.py`, `memory/models.py`, `core/config.py`, `prompt_lib/templates.py`; generator `STALE/Generation/Step0_gen_funcs.py`, evaluator `STALE/Evaluation/run_target_model.py`, `full_eval_performance.py`, `judge_prompts.py`.

All section references below resolve through these versioned primary sources. “Not demonstrated” is bounded by the inspected material, not proof of global absence.

## Problem Definition

T: maintain evolving scoped state and dependent memories. U: detect implicit staleness from changed observations and prevent stale assumptions in downstream answers. [T method; U method]

## Unit of Persistent State

T: structured attribute/scope/source state entries with lifecycle and typed relations. U: ProfileItem, SessionDelta, InvalidationProposal, UnknownCurrent and StaleSupportLink; active store plus stale archive. [T method; U memory/models.py]

## Dependency Representation

T: LLM-extracted explicit derived/coupled dependencies with temporal/scope state. U: semantic proposal lanes infer latent invalidations; retrieved target candidates undergo LLM judgment, then deterministic store transitions. U is not dependent only on prelogged graph edges. [T method; U write/*]

## Dependency Completeness Assumption

T extracts structured state from utterances under benchmark construction assumptions. U handles inferred cross-attribute invalidation and uncertain current state, but candidate/top-k and bucket/track bounds may omit support. Neither establishes complete recovered real-world justifications. [T construction; U invalidation_judge.py]

## Missing Dependency Behavior

U inference/retrieval can miss an affected item. Selected target candidates restrict allowable invalidation IDs. No controlled gold support-edge recall sweep located in T/U evaluation. [U invalidation_judge.py; T/U experiments]

## Spurious Dependency Behavior

U false proposal can weaken/archive an unrelated still-valid item; LLM judge and target/temporal guards constrain it. No spurious-support incidence sweep with independently supported bystanders located. [U transitions.py; experiments]

## Alternative Support

U prompts assess whether old assumptions remain supported; active multiple items can coexist on multi tracks. No explicit general sufficient-support-set algebra or isolated OR-support preservation test located. T distinguishes hard/soft dependencies but this is not proof of arbitrary OR semantics. [T method; U models/prompts]

## Conjunctive Support

T derived/coupled relations and U semantic proposals can express dependence in text; neither inspected implementation formalizes arbitrary conjunctions of alternatives as support environments. [T method; U models.py]

## Correlated / Copied Evidence

U records source_delta_ids and evidence_chunk_ids; REFINE accumulates origins. Confidence max/thresholds do not establish independent-source treatment. No CAMA-like latent duplicate grouping demonstrated. [U transitions.py]

## Fault Identity

U receives chronological user sessions, infers delta and target, rather than a gold fault ID. T receives state-bearing conversation turns. [T encoder; U writer.py]

## Scope Knowledge

Fixed schema/buckets constrain candidate scope; evaluator old/new/explanation fields are privileged if supplied to runtime. Native STALE target evaluator should receive haystack and question; preserve this boundary. [U schema.py; evaluation scripts]

## Repair Actions

T supersede/deactivate, retain historical state, mark dependents needs-recheck. U ADD, REFINE, REPLACE, INDIRECT_INVALIDATE, WEAK_CHALLENGE, SET_UNKNOWN_CURRENT, NO_OP plus retrieval, premise verification and response grounding. [T method; U transitions.py/invalidation_judge.py]

## Persistent vs Query-Time Repair

BOTH persistent update and query-side handling. CUPMem archives invalidated active items and creates UNKNOWN_CURRENT. It is incorrect to describe it as query-only. [U transitions.py]

## Repeated Revisions

U store tracks revision_history and session chronology; this supports repeated writes mechanically. STALE isolates old/new conflicts, not the proposed multi-revision support uncertainty factorial. T evolving dialogues contain updates but do not isolate this joint variable. [T benchmark; U data/model]

## Historical Queries

T keeps superseded states; U stale_archive and timestamps preserve prior records. Storage support is not equivalent to demonstrated arbitrary as-of QA accuracy. [T method; U transitions.py]

## Domain Shift

T two backbones/short-long variants; U several models and ontology categories. No held-out support-inference calibration transfer demonstrated. [T/U experiments]

## Uncertainty

U confidence and thresholds (e.g. .45 explicit minimum, .55 strong support) are operational heuristics. WEAK_CHALLENGE/UNKNOWN_CURRENT explicitly represent uncertainty; no Brier/reliability calibration test located. [U core/config.py; transitions.py]

## Cost Accounting

T per-turn LLM encoding can mean 165–600 calls per conversation. U extraction/proposal/judge/embedding/retrieval must all be counted; a small final prompt omits write-side cost. No complete equal-budget support-repair frontier established. [T efficiency; U pipeline/config]

## Dataset

T StateMemBench: 234 scenarios, 322 probes, 190 short (~165 turns) and 44 long (~599 turns). U STALE: 400 scenarios, 1,200 probes, 50-session histories; direct Type I and propagated Type II, public CC BY 4.0. [T dataset; U release]

## Metrics

T evolving-state query accuracy; U SR (state resolution), PR (premise resistance), IPA (implicit policy adaptation). These do not by themselves measure all persistent descendants repaired. [T/U metrics]

## Main Results

T author reports DeepSeek .363 vs .205 RAG, Qwen .233 vs .224 GraphRAG. U audited README reports CUPMem overall 68.0%; Type II SR 89%, PR 75%, IPA 43%. Different protocols/backbones, not directly comparable. [T results; U README]

## Relevant Ablations

T memory structure/encoding/readout variants; U state/conflict handling comparisons. U config inspection reveals top-k and merge limits; sensitivity to missing/spurious support sets was not located. [T/U ablations; U config]

## Failure Cases

U may leave affected records outside candidate scope; semantic assumptions in Type II gold can be too strong (e.g. coastal routine need not imply permanent relocation). This audit treats such cases as ambiguous. [U invalidation_judge.py; dataset IDs in annotations]

## Author-Stated Limitations

T synthetic state-bearing dialogues, limited backbones; U implicit-conflict construction and long-context memory retrieval limit generalization. [T/U limitations]

## Additional Limitations Observed From Code / Protocol

U source store smoke passed 3 assertions (active removal, stale archive, unknown current). It bypasses inference and proves no benchmark accuracy. Full run needs local embedding checkpoint and API/local model; no such run performed. StateMem attributable code not located. U GitHub issues API returned empty at inspection.

## Exact Overlap With G1

Inferred persistent invalidation and uncertainty/lifecycle states already exist. This changes the earlier premise and makes U a mandatory strong baseline.

## Exact Difference From G1

No located joint calibration + independent/correlated support-set interventions + repeated persistent repair + equal-cost frontier. Absence of that joint test does not establish a new algorithm.

## Could This Paper Kill G1?

PARTIALLY, strongly. A straightforward CUPMem-style semantic judge plus classical support tracking may erase the proposed headroom.

## Missing Experiment That Would Most Threaten G1

Freeze the writer/extractor and its evidence; compare U-like point decisions, support-set truth maintenance and conservative reverify across missed/spurious supports, multi-source alternatives and three revisions. Count write-side and read-side costs; test future unannounced reuse.

## Reproduction Status

**partially worked: unmodified CUPMem store transitions exercised, 3 assertions passed; no end-to-end generation/evaluation**. No paper accuracy number in this audit is a new measurement. See [release and smoke ledger](../REPRODUCIBILITY.md).
