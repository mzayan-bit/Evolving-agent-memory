# Benchmark matrix

33 named benchmarks, diagnostic suites or evaluation protocols. These are **not 33 independent standardized benchmark releases**. Original and adapted suites remain distinguished. Y=explicit coverage; P=partial/proxy; N=outside stated scope; ?=not verified. A dynamic fact in a supplied history is not necessarily a live external-world update. Counts/horizons are paper-specific; NR is unknown, not zero.

## Lifecycle coverage

| Benchmark | Multi-session | Dynamic facts | Supersession | Contradictions | Forgetting | Temporal QA | Long horizon | Distractors | Provenance | Memory ops evaluated | Cost |
|---|---|---|---|---|---|---|---|---|---|---|
| [LoCoMo](https://arxiv.org/abs/2402.17753) | Y | P | ? | P | ? | Y | Y | Y | P | recall/summary | ? |
| [LongMemEval](https://arxiv.org/abs/2410.10813) | Y | Y | Y | Y | P | Y | Y | Y | Y | QA/stages | P |
| [PersonaMem](https://arxiv.org/abs/2504.14225) | Y | Y | Y | Y | P | Y | Y | Y | P | personalization | ? |
| [MemoryAgentBench](https://arxiv.org/abs/2507.05257) | Y | Y | Y | Y | Y | P | Y | Y | P | incremental-use | Y |
| [MEMTRACK](https://arxiv.org/abs/2510.01353) | Y | Y | P | P | ? | Y | Y | Y | Y | tool-state | ? |
| [HaluMem](https://arxiv.org/abs/2511.03506) | Y | Y | Y | Y | P | P | Y | P | Y | extract/update/QA | P |
| [Evo-Memory](https://arxiv.org/abs/2511.20857) | Y | P | ? | ? | P | ? | Y | ? | ? | experience | P |
| [TAME](https://arxiv.org/abs/2602.03224) | Y | P | ? | ? | ? | ? | ? | ? | ? | trust-evolution | ? |
| [MemoryArena](https://arxiv.org/abs/2602.16313) | Y | P | ? | ? | ? | P | Y | Y | P | actions | Y |
| [Memora](https://arxiv.org/abs/2604.20006) | Y | Y | Y | Y | Y | Y | Y | P | Y | use/forget | N |
| [STALE](https://arxiv.org/abs/2605.06527) | Y | Y | Y | Y | Y | Y | Y | Y | Y | invalidation | Y |
| [LongMemEval-V2](https://arxiv.org/abs/2605.12493) | Y | Y | Y | P | P | Y | Y | Y | Y | gather/use | Y |
| [EvoMemBench](https://arxiv.org/abs/2605.18421) | Y | Y | Y | Y | Y | P | Y | Y | P | evolution | P |
| [SND / Misattribution Gap](https://arxiv.org/abs/2605.22842) | Y | P | ? | ? | ? | ? | P | Y | Y | poisoning | ? |
| [AgingBench](https://arxiv.org/abs/2605.26302) | Y | Y | Y | Y | Y | Y | Y | Y | Y | stages/maintenance | Y |
| [MemFail](https://arxiv.org/abs/2605.26667) | P | P | P | Y | ? | ? | P | Y | P | summary/store/retrieve | ? |
| [MemStrata synthetic suites](https://arxiv.org/abs/2606.26511) | P | Y | Y | Y | P | Y | P | Y | Y | supersession | Y |
| [MemSyco-Bench](https://arxiv.org/abs/2607.01071) | P | P | ? | Y | ? | ? | ? | Y | ? | sycophancy | ? |
| [GovMem-Bench](https://arxiv.org/abs/2607.02579) | P | Y | P | Y | P | P | P | Y | Y | promotion/review | Y |
| [MemOps](https://arxiv.org/abs/2607.12893) | Y | Y | Y | Y | Y | Y | Y | Y | Y | lifecycle-traces | ? |
| [MemTX conformance suite](https://arxiv.org/abs/2607.23929) | P | Y | Y | Y | Y | Y | N | Y | Y | commit/action | Y |
| [MemSecBench](https://arxiv.org/abs/2607.27080) | Y | P | P | Y | Y | ? | P | Y | Y | poison/repair | P |
| [ChronoMem post-exposure protocol](https://arxiv.org/abs/2607.27773) | Y | Y | Y | Y | Y | Y | Y | Y | Y | rollback | P |
| [StateAuditor evaluation](https://arxiv.org/abs/2608.01619) | Y | Y | Y | Y | P | Y | Y | Y | Y | audit/repair | Y |
| [AuthMem-Bench](https://arxiv.org/abs/2608.01679) | P | P | P | P | ? | P | P | Y | Y | authority/action | ? |
| [Rollback repair suite](https://arxiv.org/abs/2608.10502) | P | Y | Y | Y | Y | P | P | Y | Y | repair | Y |
| [Memory Commitment Boundary](https://arxiv.org/abs/2608.19564) | P | Y | P | Y | P | P | N | P | Y | decision/tool-choice | P |
| [StateMemBench](https://arxiv.org/abs/2608.19652) | Y | Y | Y | Y | Y | Y | Y | Y | Y | current-state | Y |
| [MemStrata software histories](https://arxiv.org/abs/2608.20685) | P | Y | Y | Y | P | Y | P | Y | Y | supersession | Y |
| [PersonaMem-v3](https://arxiv.org/abs/2608.21381) | Y | Y | Y | P | P | Y | Y | Y | Y | personalized-actions | P |
| [Memory Trust Gap](https://arxiv.org/abs/2609.01852) | N | Y | Y | Y | P | Y | N | Y | Y | evidence-use | P |
| [Execution-state unlearning tests](https://arxiv.org/abs/2609.04875) | P | P | P | P | Y | P | P | Y | Y | unlearning | Y |
| [Revocation enforcement study](https://arxiv.org/abs/2609.08258) | P | Y | Y | Y | Y | P | N | Y | Y | retrieve/action | ? |

## Construction, scale, outcomes and blind spots

### LoCoMo

- **Primary paper:** [LoCoMo](https://arxiv.org/abs/2402.17753); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Multi-session dialogue QA, summarization and generation; original paper averages ~300 turns/9K tokens, up to 35 sessions; common released evaluation uses 10 longer conversations.
- **Synthetic/natural:** LLM persona/event graph generation with human verification.
- **Lifecycle and world dynamics:** Temporal QA, multi-hop and adversarial/unanswerable questions.
- **Metrics/cost:** QA F1/judged correctness, summarization; cost not the original central target.
- **What it does not establish:** Do not mix original statistics with released 10-conversation subset; no executed lifecycle gold trace.

### LongMemEval

- **Primary paper:** [LongMemEval](https://arxiv.org/abs/2410.10813); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 500 questions; ~115K/1.5M-token tiers; five abilities.
- **Synthetic/natural:** Curated questions in scalable constructed chat histories.
- **Lifecycle and world dynamics:** Knowledge updates, temporal reasoning, abstention and multi-session reasoning; oracle evidence.
- **Metrics/cost:** QA accuracy; evidence recall/NDCG; indexing/retrieval/reading analysis.
- **What it does not establish:** Post-hoc QA does not expose every write/update operation; not a live evolving environment.

### PersonaMem

- **Primary paper:** [PersonaMem](https://arxiv.org/abs/2504.14225); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 20 personas, >180 histories; seven personalized query categories.
- **Synthetic/natural:** Synthetic evolving profiles/dialogue.
- **Lifecycle and world dynamics:** Latest preferences, full evolution, update reasons and transfer; historical/current distinction.
- **Metrics/cost:** Four-option accuracy; stale/irrelevant distractor options.
- **What it does not establish:** Multiple-choice selection differs from free-form personalized action.

### MemoryAgentBench

- **Primary paper:** [MemoryAgentBench](https://arxiv.org/abs/2507.05257); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Incremental chunk ingestion, retrieval/learning/understanding/selective-forgetting tasks; sizes depend on source.
- **Synthetic/natural:** Converted source datasets and synthetic fact-consolidation updates.
- **Lifecycle and world dynamics:** Replacement and multi-hop facts; long information streams; explicit selective forgetting.
- **Metrics/cost:** Task accuracy/F1, cost-performance; latest appendices include strict compute-matched comparisons.
- **What it does not establish:** v4 terminology differs from old Conflict Resolution split; costs/chunks need matching.

### MEMTRACK

- **Primary paper:** [MEMTRACK](https://arxiv.org/abs/2510.01353); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 47 dynamic multi-platform instances; sequential questions without future-query visibility.
- **Synthetic/natural:** Real GitHub issue grounding plus authored/LLM Slack/Linear/Git events.
- **Lifecycle and world dynamics:** Temporal cross-platform state and tool-accessible evolving environment.
- **Metrics/cost:** Task answer correctness and agent behavior; numerical horizons not uniformly extracted.
- **What it does not establish:** Small curated environments; full timeline is not directly given to agent.

### HaluMem

- **Primary paper:** [HaluMem](https://arxiv.org/abs/2511.03506); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Medium/long persona histories with extraction/update/QA annotations.
- **Synthetic/natural:** Generated and annotated memory histories.
- **Lifecycle and world dynamics:** Write omissions, hallucinations, update corruption and downstream answers.
- **Metrics/cost:** Integrity, omission, update accuracy and hallucination; API timing can confound.
- **What it does not establish:** Retrieval is excluded from the generative-hallucination definition, not shown harmless.

### Evo-Memory

- **Primary paper:** [Evo-Memory](https://arxiv.org/abs/2511.20857); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Sequential test-time learning tasks with self-evolving memory.
- **Synthetic/natural:** Task streams from existing evaluation sources.
- **Lifecycle and world dynamics:** Experience reuse and memory evolution across episodes.
- **Metrics/cost:** Task performance and evolution analysis; detailed budgets require matching.
- **What it does not establish:** Not interchangeable with dynamic factual supersession; exact per-stream sizes NR.

### TAME

- **Primary paper:** [TAME](https://arxiv.org/abs/2602.03224); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Trustworthy test-time memory evolution benchmark.
- **Synthetic/natural:** Screened abstract; construction details not fully reviewed.
- **Lifecycle and world dynamics:** Reliability-aware memory evolution.
- **Metrics/cost:** Reported trust/task metrics; exact definitions NR here.
- **What it does not establish:** Dimension coverage beyond explicit abstract claims remains uncertain.

### MemoryArena

- **Primary paper:** [MemoryArena](https://arxiv.org/abs/2602.16313); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Five domains: shopping, travel, progressive retrieval, mathematics, physics; interdependent multi-session subtasks.
- **Synthetic/natural:** Human-crafted, inspected agentic tasks.
- **Lifecycle and world dynamics:** Memory-action-environment loops; tool use and reuse of earlier feedback.
- **Metrics/cost:** Success, partial/task progress and latency; S3/S4.2/S4.5.
- **What it does not establish:** Task interdependence does not necessarily mean changing truth; no full lifecycle operator oracle.

### Memora

- **Primary paper:** [Memora](https://arxiv.org/abs/2604.20006); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Ten personas across weekly/monthly/quarterly sessions; remember/reason/recommend.
- **Synthetic/natural:** Simulated evolving personas with criteria.
- **Lifecycle and world dynamics:** Creation, mutation, deletion and forgetting-aware personalization.
- **Metrics/cost:** FAMA scores required and forbidden information; runtime efficiency not central.
- **What it does not establish:** Few personas; LLM judges; sampled errors are conditional, not population rates.

### STALE

- **Primary paper:** [STALE / CUPMem](https://arxiv.org/abs/2605.06527); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 400 scenarios, 1,200 queries, ~50 sessions, up to 150K tokens.
- **Synthetic/natural:** Synthetic, expert-validated conflicts.
- **Lifecycle and world dynamics:** Direct and dependency-mediated invalidation; stale query premises.
- **Metrics/cost:** SR, PR and IPA; appendix cost analysis.
- **What it does not establish:** One main conflict pair/scenario; no general natural provenance uncertainty.

### LongMemEval-V2

- **Primary paper:** [LongMemEval-V2](https://arxiv.org/abs/2605.12493); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 451 questions; 100/500-trajectory tiers with ~25M/115M tokens.
- **Synthetic/natural:** Manually curated questions over web-agent trajectories.
- **Lifecycle and world dynamics:** Static state, dynamic state, workflows, environment gotchas, premise awareness.
- **Metrics/cost:** Answer/context-gathering quality and latency; evidence trajectory labels.
- **What it does not establish:** Very large histories; context-gathering evaluation, not full autonomous-lifecycle replay.

### EvoMemBench

- **Primary paper:** [EvoMemBench](https://arxiv.org/abs/2605.18421); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Six suites: within-episode knowledge/execution and cross-episode knowledge/tool/web/embodied; CrossEp-Know 120 contexts/884 samples.
- **Synthetic/natural:** Reconstructed public tasks with human checking.
- **Lifecycle and world dynamics:** State revision, execution context, transferable experience, tool tasks.
- **Metrics/cost:** Suite task metrics; method-specific cost comparison needs protocol audit.
- **What it does not establish:** Heterogeneous subbenchmarks need separate reporting; aggregate is not one memory ability.

### SND / Misattribution Gap

- **Primary paper:** [Misattribution Gap](https://arxiv.org/abs/2605.22842); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 25 scenarios reported in abstract; persistent compositional poisoning.
- **Synthetic/natural:** Adversarial financial/healthcare-domain scenarios.
- **Lifecycle and world dynamics:** Temporal persistence, multi-agent composition and causal-entry localization.
- **Metrics/cost:** Counterfactual Composition Testing attribution; do not treat headline as replicated.
- **What it does not establish:** Abstract-level screen; safety/generalization and dataset scale need full verification.

### AgingBench

- **Primary paper:** [AgingBench](https://arxiv.org/abs/2605.26302); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 8–200 sessions; seven scenario families, 14 models, >400 runs.
- **Synthetic/natural:** Controlled temporal/dependency/distractor construction.
- **Lifecycle and world dynamics:** Compression, interference, revision, maintenance; oracle ladder.
- **Metrics/cost:** Version/forget/dependency/bystander scores, degradation slope and wall time.
- **What it does not establish:** Synthetic aging and diagnostic interventions are not complete causal identification.

### MemFail

- **Primary paper:** [MemFail](https://arxiv.org/abs/2605.26667); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Five datasets/four tasks: Conditional-Facts easy/hard, Coexisting-Facts, Persona-Retrieval, Long-Hop; 92 long-hop chains.
- **Synthetic/natural:** Controlled adversarial construction.
- **Lifecycle and world dynamics:** Lost qualifiers, compatible-fact overwrite, identity confusion and multi-hop retrieval.
- **Metrics/cost:** Task-specific answer correctness; failure-type comparison; S3–S6.
- **What it does not establish:** Designed isolation can still leave interactions; not a natural long-running deployment.

### MemStrata synthetic suites

- **Primary paper:** [MemStrata](https://arxiv.org/abs/2606.26511); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Six locally evaluated benchmarks; atomic old/new fact changes.
- **Synthetic/natural:** Controlled single-value fact updates.
- **Lifecycle and world dynamics:** Stale-fact reuse under forced answers, temporal supersession.
- **Metrics/cost:** Accuracy, stale-fact-error rate, retrieval latency.
- **What it does not establish:** Single-valued slot assumptions simplify ambiguous contradiction.

### MemSyco-Bench

- **Primary paper:** [MemSyco-Bench](https://arxiv.org/abs/2607.01071); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Memory-mediated sycophancy tasks.
- **Synthetic/natural:** Benchmark construction not deeply inspected.
- **Lifecycle and world dynamics:** Social pressure and persistent-memory distortion.
- **Metrics/cost:** Sycophancy/task outcomes; sizes NR here.
- **What it does not establish:** Sycophancy differs from factual falsity or expiry.

### GovMem-Bench

- **Primary paper:** [GovMem](https://arxiv.org/abs/2607.02579); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Synthetic stress cases; internal 120 candidates/79 traces; 35 held out; external selected 133 high-impact human-adjudicated candidates.
- **Synthetic/natural:** Synthetic plus internal and public agent traces.
- **Lifecycle and world dynamics:** Correlated support, stale/scope traps, evidence review burden.
- **Metrics/cost:** False promotion, precision/recall, review burden, AUPRC; downstream harm experiment not executed.
- **What it does not establish:** All external automatic positives rejected in selected final audit; not validated efficient writer.

### MemOps

- **Primary paper:** [MemOps](https://arxiv.org/abs/2607.12893); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 100 topics, 403 evidence conversations, 9,672 turns; 2,006 QA pairs evaluated twice =4,012 instances.
- **Synthetic/natural:** Controlled generation with exact dialogue evidence and verification.
- **Lifecycle and world dynamics:** Remember, forget, update, reflect, composed trajectories; six probe categories.
- **Metrics/cost:** Operation/target/evidence/state-order probes; forgetting includes over-removal.
- **What it does not establish:** Adjacent and long-context instances share underlying QA; do not count independent items twice.

### MemTX conformance suite

- **Primary paper:** [MemTX](https://arxiv.org/abs/2607.23929); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 90 base cases plus 56 harder cases; often 1–4 turns.
- **Synthetic/natural:** Controlled multi-agent conformance cases.
- **Lifecycle and world dynamics:** Lifecycle states, permissions, revocation and action safety.
- **Metrics/cost:** Harm, completion, violations, cost and formal-state checking.
- **What it does not establish:** Short horizon; formal guarantees scoped to modeled state/provenance.

### MemSecBench

- **Primary paper:** [MemSecBench](https://arxiv.org/abs/2607.27080); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 310 cases, 48 contexts; 24 harness/backend/model compositions.
- **Synthetic/natural:** Controlled memory poisoning and repair.
- **Lifecycle and world dynamics:** Persistence, exposure, adoption, consequence, removal and benign preservation.
- **Metrics/cost:** MPSR, E2E, conditional SRSR, repair/removal and benign retention.
- **What it does not establish:** Composition dependence; conditional and unconditional rates differ.

### ChronoMem post-exposure protocol

- **Primary paper:** [ChronoMem](https://arxiv.org/abs/2607.27773); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** LoCoMo/MAB adapted for historical global rollback after full exposure.
- **Synthetic/natural:** Adapted existing histories.
- **Lifecycle and world dynamics:** Version selection, rollback-consistent QA and summarization.
- **Metrics/cost:** Recall@k, temporal locality, QA F1, ROUGE.
- **What it does not establish:** MAB downstream scope restricted; global snapshot restore differs from selective repair.

### StateAuditor evaluation

- **Primary paper:** [StateAuditor](https://arxiv.org/abs/2608.01619); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** STALE plus HorizonBench and harder lifecycle transfer; strict vs joint-scenario settings.
- **Synthetic/natural:** Benchmark adaptation and authored controls.
- **Lifecycle and world dynamics:** Implicit stale premises and false invalidation; quote/time verification controls.
- **Metrics/cost:** Current preference/state accuracy, overcorrection, matched-budget comparisons.
- **What it does not establish:** Scope/judge dependence; external gains uneven and harder set shows no accuracy gain.

### AuthMem-Bench

- **Primary paper:** [AuthMem-Bench](https://arxiv.org/abs/2608.01679); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 50 base histories ×7 transitions =350 pairs; base-history splits.
- **Synthetic/natural:** Controlled authority transformations.
- **Lifecycle and world dynamics:** Authority preservation across consolidation and downstream actions.
- **Metrics/cost:** Authority upgrade/omission; prohibited actions and benign completion.
- **What it does not establish:** Prompted writer objectives are not complete native backend implementations.

### Rollback repair suite

- **Primary paper:** [Dependency-guided Rollback](https://arxiv.org/abs/2608.10502); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 150 selected injected failures; 50 adapted LME-V2 cases.
- **Synthetic/natural:** Controlled three-domain/four-fault setup.
- **Lifecycle and world dynamics:** Downstream repair, independent support and benign preservation.
- **Metrics/cost:** Recovery, preservation, recurrence and replay cost.
- **What it does not establish:** Fault IDs supplied; explicit recorded dependencies; selected successful attacks.

### Memory Commitment Boundary

- **Primary paper:** [Memory Commitment Boundary](https://arxiv.org/abs/2608.19564); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 140 primary cases:70 dev/70 test; separate70-item contrast set.
- **Synthetic/natural:** Rule-authored, independently relabeled held-out cases.
- **Lifecycle and world dynamics:** Persist/temporary/verify/clarify choices; structured tool selection.
- **Metrics/cost:** Accuracy, macro-F1, over/under-memory, verify/clarify recall and label-tool agreement.
- **What it does not establish:** Tool-call selection is not tool execution; isolated items not longitudinal drift.

### StateMemBench

- **Primary paper:** [StateMem](https://arxiv.org/abs/2608.19652); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 234 scenarios/322 probes; ~165 or599 turns, ~3K or7–15K tokens.
- **Synthetic/natural:** Synthetic explicit revisions/dependencies, checked labels.
- **Lifecycle and world dynamics:** Current versus superseded state; dependent constraints and drift attribution.
- **Metrics/cost:** Current-state accuracy, stale-state drift, other error; ingestion cost.
- **What it does not establish:** Explicit dependency utterances; many turns but comparatively modest tokens.

### MemStrata software histories

- **Primary paper:** [MemStrata Software Histories](https://arxiv.org/abs/2608.20685); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 130 clean atomic transitions extracted from707 GitHub issues.
- **Synthetic/natural:** SWE-bench Lite/Verified real fixes, transformed into marker-free statements.
- **Lifecycle and world dynamics:** Natural-source supersession and stale-answer frequency.
- **Metrics/cost:** Accuracy, stale-fact-error and latency.
- **What it does not establish:** Selection removes ambiguous/multi-fact changes; same team as synthetic study.

### PersonaMem-v3

- **Primary paper:** [PersonaMem-v3](https://arxiv.org/abs/2608.21381); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 200 resampled users, >1M engagement events;30-day substrate; six digital platforms.
- **Synthetic/natural:** Privacy-preserving real engagement substrate enriched by LLM synthesis.
- **Lifecycle and world dynamics:** Time-masked cross-platform understanding, recommendation, over-personalization and tool tasks.
- **Metrics/cost:** Open-ended universal/task rubrics; context and agent-harness modes.
- **What it does not establish:** Enriched worlds are not untouched real user logs; future evidence masked.

### Memory Trust Gap

- **Primary paper:** [Memory Trust Gap](https://arxiv.org/abs/2609.01852); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 300 base scenarios; four memory conditions;16-cell cue factorial; Qwen model-size series and external checks.
- **Synthetic/natural:** Controlled templates plus RGB/MisBench transfer.
- **Lifecycle and world dynamics:** Stale value versus authoritative evidence; provenance/recency/position interactions.
- **Metrics/cost:** Stale reliance, paired net harm, scenario-clustered intervals.
- **What it does not establish:** Consumption-time study; Benefit and Safety no-memory baselines mean different things.

### Execution-state unlearning tests

- **Primary paper:** [Execution-state Unlearning](https://arxiv.org/abs/2609.04875); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** 100 LME,100 ToolSandbox,80 AgentDojo controlled cases.
- **Synthetic/natural:** Adapted replayable tasks.
- **Lifecycle and world dynamics:** Forgetting influence from summaries/plans/cache as well as records.
- **Metrics/cost:** Leakage, counterfactual action distance, utility and recompute/latency.
- **What it does not establish:** Fixed observations and replay assumptions; no physical-world reversal.

### Revocation enforcement study

- **Primary paper:** [Revocation Enforcement](https://arxiv.org/abs/2609.08258); pinned version in [ledger](version_ledger.md).
- **Task and horizon:** Five memory systems, nine policy scenarios, nine models, six defenses.
- **Synthetic/natural:** Controlled revoked-policy and replacement pairs.
- **Lifecycle and world dynamics:** Whether revocation labels are actually enforced in retrieval/actions.
- **Metrics/cost:** Revoked retrieval and unsafe action frequency.
- **What it does not establish:** Small policy set; product versions and guard behavior must be pinned.

## Evaluation interpretation

The claim “memory benchmarks only test recall” is contradicted by LongMemEval, MemoryAgentBench, Memora, STALE, AgingBench, MemOps, StateMemBench and the security/repair suites above. A defensible new evaluation should isolate a missing **combination of assumptions**, not relabel an existing capability.

For the leading direction, extend existing data with controlled missing/spurious lineage, multiple valid support sets and repeated revisions. Score stale influence **and** damage to unaffected facts, with a human-adjudicated natural-language slice. Keep the original suite intact for comparability. Existing benign-preservation, stale-reuse and repair metrics must be credited rather than renamed as inventions.

Tool use is central in MemoryArena, MEMTRACK, LME-V2's source trajectories, EvoMemBench execution suites and PersonaMem-v3. Pure dialogue QA is not a substitute. Poisoning is central to AgentPoison-related studies, SND, MemSecBench and the rollback fault suite; ordinary distractors should not be labeled adversarial poisoning.

Consolidation is directly probed by HaluMem, AuthMem-Bench, MemOps Reflect, MemFail Conditional-Facts and GovMem promotion. Provenance means different things: gold evidence spans, source authority, generated lineage and real runtime dependencies are separate axes. No single Y mark means all are covered.
