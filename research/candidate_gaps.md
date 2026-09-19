# Candidate directions after adversarial novelty checks

Cutoff: **19 September 2026**. These are hypotheses for research, not assertions of firstness. “Missing” means the reviewed primary evidence does not establish the specified combination of assumptions and outcomes. The search is broad but not exhaustive. No proposed method or benchmark generator has been implemented.

## G1 — Selective Memory Repair under Uncertain Dependency Lineage

### Research gap / problem

An agent may have several downstream beliefs, summaries and pending decisions that depend on a changed fact, but its recorded dependency graph can omit a prerequisite, invent a link or confuse copied evidence with independent support. We need to determine when selective repair remains useful under such uncertainty, instead of assuming perfect lineage or invalidating every possibly related record. The scientific target is a measured stale-error versus false-invalidation frontier under repeated updates and distribution shift.

### Evidence this problem exists

[PlanFence](https://arxiv.org/html/2609.03340v1#A3) explicitly tests sensitivity to missing dependencies, while its safety contract assumes complete dependencies. [Dependency-guided rollback repair](https://arxiv.org/html/2608.10502v1#S3) takes diagnosed faulty IDs and runtime-recorded edges, preserving independent trusted support. [StateAuditor](https://arxiv.org/html/2608.01619v1#S6) estimates implicit premises, but chronological/quotation validation does not prove semantic supersession, and harder transfer does not consistently improve accuracy. These are different, complementary boundaries, not evidence that dependency repair has never been studied.

### Closest papers / what they solve

- **Rollback repair:** selective post-failure recovery and benign preservation with explicit runtime dependencies.
- **PlanFence:** pre-action checking of exact dependency versions and bounded replan/block behavior.
- **StateMem and CUPMem:** dependent-state reconsideration and propagation-aware revision.
- **StateAuditor:** implicit stale-premise auditing and response repair.
- **CAMA:** learned latent evidence-dependence inference and adaptive recovery; “infer uncertain dependencies” alone is already taken.
- **GovMem:** dependency-aware write promotion, counterevidence and review burden; “risk-controlled memory evidence governance” alone is already taken.
- **MemTX, MemAudit and execution-state unlearning:** governance, diagnosis and counterfactual replay establish additional strong precedents.

### What remains missing / why this is not just an engineering feature

The candidate contribution is **not** adding a graph, confidence field or rollback button. It is a reproducible comparison of persistent-state repair under *measured lineage uncertainty*, including multiple alternative supports and repeated revisions, with an uncertainty-aware decision rule that improves an explicitly chosen risk/coverage/cost tradeoff. A negative result showing that plausible inference cannot outperform conservative replay under realistic lineage error could also be scientifically useful. If the contribution is merely existing rollback repair plus an LLM edge extractor with no controlled uncertainty analysis, reject it.

### Core research question and hypothesis

Can a selective repair rule lower stale descendant reuse relative to literal-edge traversal, while causing fewer false invalidations than broad semantic closure, at equal verification/replay budgets? Hypothesis: calibrated evidence for **support necessity and alternative sufficiency**, combined with an abstain/reverify option, yields a better frontier than a point-estimate graph. Calibration is empirical on held-out data; no distribution-free guarantee under arbitrary shift is claimed.

### Possible method / potential contribution

Use a frozen model or small classifier to score candidate support relationships and alternative support sets. Keep provenance and authority distinct from truth. Choose retain, quarantine/reverify or repair using validation-set thresholds and a measured cost model. Learn thresholds on disjoint domains/entities, evaluate under shifted update language and missing-edge patterns. This is a proposed method family, not a committed architecture. Existing retrieval, graph traversal and replay can remain unchanged.

### Minimum viable paper

A carefully audited extension of STALE/StateMemBench and the rollback protocol, a strong non-oracle dependency baseline, an uncertainty-aware selection rule, and a matched-budget analysis showing where selective repair succeeds and fails. Include one human-adjudicated natural-language slice and release annotation disagreements. A new metric is unnecessary: use existing stale reuse, recovery and benign-preservation concepts with precise denominators.

### Strong version

Demonstrate stable tradeoffs across two application domains, three dependency-error regimes, repeated multi-step revisions, and a second answerer family; quantify calibration degradation and selective-replay costs. Show that gains survive removing privileged fault IDs or gold scope annotations. Do not promise arbitrary natural-language truth maintenance.

### Experimental plan / required experiments

1. Freeze a support ontology distinguishing required conjunctions, alternative sufficient supports, scope changes and mere associations.
2. Start with known fault identity to isolate lineage inference; add a separate unknown-fault condition only later.
3. Compare complete, randomly missing, systematically missing and spurious lineage. Natural missingness must be included; random edge dropout alone is too easy.
4. Evaluate 1/3/10 revision events per stream, with unchanged-but-related bystanders and historical queries.
5. Keep reader, source information, retrieval candidates and total call/replay budget fixed. Report full-history and gold-dependency conditions only as upper bounds.
6. Split by source scenario/entity/template; bootstrap whole trajectories. Use at least three seeds for stochastic components and two model families for the final study.

### Strongest baselines

No repair; delete-source-only; full replay/reset; explicit-edge rollback repair; broad semantic-neighbor invalidation; StateAuditor-style audit/repair; CUPMem/StateMem dependent-state policy; inferred-edge point estimate; CAMA-style evidence grouping where applicable. A PlanFence-inspired pre-action gate is a complementary prevention baseline, not an exact substitute for post-failure repair.

### Metrics and required ablations

Report stale descendant reuse, answer/action correctness, false invalidation of unaffected items, independent-support retention, recurrence after later retrieval, coverage/abstention, calibration (Brier/reliability plots where labels are probabilistic), tokens, calls, replayed steps and p50/p95 latency. Ablate alternative-support preservation, uncertainty handling, calibration, source authority, dependency inference and repeated revision. Match budgets rather than letting more verifier calls explain gains.

### Data and compute feasibility

**Implementation complexity:** medium/high; annotation and faithful baseline adaptation dominate. **Experiment complexity:** medium/high. **Data:** existing public histories plus a few hundred audited support/revision cases; no benchmark generator in this phase. **GPU:** no required training GPU for API inference; optional 8B quantized inference or small classifier on accessible hardware. **API cost:** moderate pilot, potentially substantial full grid; estimate from measured calls before launch. A 60-case ×6-method ×2-backbone pilot is720 trajectories. At four calls of2K input/250 output tokens each, that is approximately5.76M input and0.72M output tokens, excluding ingestion/judging/retries. This is a planning assumption, not a price quote. Full grids must reuse immutable ingestion and cap verifier calls.

### Main novelty risk / papers that could invalidate it

**High overlap risk** with rollback repair, StateAuditor, CAMA, GovMem and PlanFence. If one already evaluates persistent repair under incomplete inferred lineage, alternative support and calibrated over-invalidation at matched cost, this candidate becomes replication/extension rather than a new method paper.

### Kill criterion and novelty confidence

**Medium, conditional.** Before implementation, inspect code/protocols of the five closest papers and manually adjudicate30 cases. Abandon the method claim if a simple conservative or point-estimate baseline already dominates the proposed frontier, if gold support is not reproducibly labelable, or if the closest work already runs the intended experiment.

## G2 — Revision-Preserving Memory Compression under a Total Storage Budget

### Research gap / problem

A compact answer context can conceal an unlimited raw archive, snapshots and provenance. The narrower question is how to allocate a *total persistent-state budget* when future corrections and historical queries are unknown at write time. What should survive compression so that a later retraction can be applied without retaining every original observation indefinitely?

### Evidence and closest work

[TierMem](https://arxiv.org/abs/2602.17913) escalates to an immutable raw archive. [RD-Forget](https://arxiv.org/html/2609.10263v1#S3) retains source history and budgets a query-conditioned view. [OAS](https://arxiv.org/abs/2607.17545) explicitly selects consolidation operators by budget and replacement harm, mainly using query-known evidence. [ChronoMem](https://arxiv.org/html/2607.27773v1#S3) snapshots entire memory for historical rollback. These already solve important parts of preservation, historical access and budgeted use.

[R3Mem](https://aclanthology.org/2025.findings-acl.235/) already studies learned reversible compression; [rate-distortion compaction](https://arxiv.org/abs/2607.08032) provides a theoretical/taxonomic formulation. [SkillZip-Tan](https://arxiv.org/abs/2608.05604), [SkillZip-Bai](https://arxiv.org/abs/2608.11079) and [SkillZip Pro](https://arxiv.org/html/2608.30785v1#S4) preserve procedural contracts, dependencies and deletion witnesses, including persistent storage accounting. Therefore neither reversible compression, dependency-preserving compression nor honest storage accounting alone is new.

### What remains missing / scientific distinction

The proposed test concerns **evolving factual support and later correction utility**, with every retained archive, witness, embedding and index counted against a budget, and no retrieval of discarded originals. Procedural bundle faithfulness and reconstruction are strong precedents but do not, in the inspected evidence, settle unknown future semantic revision after factual evidence has been discarded. This distinction must survive a direct comparison; changing the application label is insufficient.

### Core question and hypothesis

At a fixed total byte budget, can compact correction witnesses and support-aware retention outperform salience-only, recency-only and query-utility compression on future correction/historical tasks without unacceptable loss of ordinary recall? Hypothesis: a small allocation to revision-relevant distinctions provides a better accuracy–correction–storage frontier under declared query/update distributions.

### Possible method / contribution

A constrained retention policy choosing between raw evidence, compact support witnesses and a summary, trained or tuned on future correction utility. Include source identity, scope and minimal competing evidence where useful; charge their full storage. Use standard rate-distortion language with explicit task distribution. Do not claim lossless recovery of arbitrary unseen facts from a fixed-size state: that is impossible in general.

### Minimum viable paper / strong version

Minimum: a total-storage-controlled extension of existing histories, strong lossy and archive baselines, an evidence-retention rule and ablations separating recall from revision. Strong: an empirically validated lower-bound/feasibility analysis for specified update families, continual re-compression across100+ events and evaluation on real change histories. A result that archives are cheaper/more reliable under realistic storage prices would be valuable and could kill the practical method motivation.

### Evaluation, baselines and metrics

Use current/historical queries, delayed source retractions, qualifier changes and alternative supports. Compare fixed-size FIFO/LRU, lossless compression where applicable, raw reservoir, salience summaries, OAS-style operator selection, R3Mem where reproducible, TierMem/RD-Forget with explicitly charged/truncated archives, and a SkillZip-inspired witness-preserving adaptation. Preserve unmodified originals as upper bounds only.

Measure all bytes (including embeddings, graph/index overhead, snapshots and witnesses), current/historical accuracy, correction success, stale reuse, false invalidation, reconstruction fidelity, API tokens and latency. Report storage and context budgets separately. Ablate witness content, source links, future-query-aware training, archive rescue, and repeated compression. Hold code/model weights constant and account for learned per-user adapters if used.

### Data, compute and experimental conditions

**Implementation complexity:** medium/high. **Experiment complexity:** medium. **Data:** controlled revisions plus existing STALE/LME/StateMem and selected real software changes; avoid treating selected atomic code facts as fully natural conversation. **GPU:** none for main textual policy; R3Mem reproduction may require fine-tuning and should be optional initially. **API cost:** moderate-to-high due to re-compression. Initial grid:5 policies ×4 budgets ×3 revision delays ×2 answerer families =120 configuration cells before seeds, evaluated on shared streams. Stage this; do not launch the full grid at once.

### Biggest risk / kill criterion / novelty confidence

**Medium-low.** Closest threats are OAS, RD-Forget, R3Mem, SkillZip Pro, ChronoMem and any revision-aware bounded-memory extension. Kill the practical claim if total archive storage is negligible relative to inference cost for intended deployment, or if lossless compression plus ordinary indexed retention matches the method. Kill novelty if prior work already charges all retained evidence while evaluating delayed semantic corrections under unknown future queries.

## G3 — Budgeted Revalidation of Agent Memory under Unannounced World Changes

### Research gap / problem

When no update notification arrives, a stored claim can be obsolete even though nothing in the memory store contradicts it. The agent must choose whether to reuse it, check an authoritative source, ask the user or abstain. The candidate is a longitudinal **cost–freshness decision problem under missing notifications**, not another retrieval router.

### Evidence and competing solutions

[Corrective RAG](https://arxiv.org/abs/2401.15884), [Self-RAG](https://arxiv.org/abs/2310.11511) and [Adaptive-RAG](https://arxiv.org/abs/2403.14403) already make conditional retrieval decisions. [Right Pocket](https://arxiv.org/abs/2603.15658), [BudgetMem](https://arxiv.org/abs/2602.06025), [TierMem](https://arxiv.org/abs/2602.17913), [Router-Mem](https://arxiv.org/abs/2608.01285) and [MemCon](https://arxiv.org/abs/2607.13591) address store, budget, escalation or stopping choices. [PlanFence](https://arxiv.org/abs/2609.03340) checks version heads before actions. [MCB](https://arxiv.org/html/2608.19564v1#S3) directly tests verify-versus-clarify decisions but evaluates isolated action/tool selections, not downstream execution across an evolving source timeline. [Memory Trust Gap](https://arxiv.org/abs/2609.01852) shows stale notes can override authoritative tool evidence.

Classical cache refresh and age-of-information work are major adjacent precedents; [optimal freshness/refresh-cost tradeoffs](https://arxiv.org/abs/1008.0441) predate LLM agents. This older paper is an adjacent lead, not counted among the100 retained2023–26 works. We have not completed an exhaustive database/cache-control review, so confidence is lower than for G1.

### What remains missing / scientific distinction

In the inspected agent-memory evidence, an end-to-end comparison under **withheld change notifications, heterogeneous volatility, imperfect source checks and constrained verification budgets** is not established. The contribution would have to demonstrate why ordinary TTL/hazard-based refresh fails and what task/source-aware decision information improves the frontier. Merely implementing TTL or putting “verify” in a prompt is engineering, not novelty.

### Core question, hypothesis and method

Can a small calibrated policy allocate source checks better than fixed TTL, age-only hazard estimation and generic uncertainty-triggered RAG at the same stale-action rate? Hypothesis: task loss, source availability and observed change history improve risk-sensitive verification over age alone. Candidate actions: use memory, check source, ask user, abstain. Learn a small contextual policy from logged checks; include a missingness model and explicitly test drift in the change process. “Ask user” applies to private intent, not to public facts resolvable by a tool.

### Minimum viable paper / strong version

Minimum: a frozen time-indexed source replay protocol, strong cache/RAG baselines and a small policy with an interpretable cost–staleness analysis. Strong: realistic software/API or organizational-state change histories, missing-notification mechanisms, unavailable sources and delayed observation, with drift-robust calibration. The main outcome must be executed behavior after verification, not merely a correct action label.

### Experimental plan, baselines, metrics and ablations

Compare never-check, always-check, fixed TTL, learned age-only hazard, random budget allocation, uncertainty-triggered retrieval, MCB-style prompt rules, a MemCon-style bandit and an oracle change detector. Evaluate bursts, periodic changes and task-correlated changes at several notification-drop rates. Measure stale actions, valid completion, verification calls, total tokens, latency, abstention/clarification burden and missed checks. Ablate age, historical volatility, action loss, source reliability and calibration; include a held-out change process. Preserve historic source snapshots so answers are evaluated at the correct time without internet-future leakage.

### Data, compute and conditions

**Implementation complexity:** medium. **Experiment complexity:** high because realistic change processes and hidden information must be carefully controlled. **GPU:** optional small classifier; API or accessible local inference sufficient. **API cost:** moderate with cached source replay, potentially high with real browsing; begin offline. A first grid of6 policies ×3 change processes ×3 notification rates ×2 task-loss regimes =108 cells before seeds. Choose a small pilot subset before expanding. No live-web polling system is proposed in this literature phase.

### Biggest risk / kill criterion / novelty confidence

**Low; reserve direction.** Strong generic retrieval/control and classical refresh precedents may eliminate the methodological novelty. A new paper combining MCB’s verify/clarify actions with MemCon-style learning and time-indexed source changes could close most of the proposed boundary. Do not proceed unless a focused cache-control/age-of-information review and matched TTL pilot reveal headroom. If age-only refresh matches the proposed policy, retain only a diagnostic study if it establishes a meaningful failure mechanism.

## Qualitative paper potential

| Criterion | G1 uncertain-lineage repair | G2 total-storage revision | G3 unannounced-change revalidation |
|---|---|---|---|
| Importance | High: bad updates propagate into future decisions | Conditional on genuine storage constraints | High for volatile external facts |
| Novelty | Narrow, medium confidence; high competitor overlap | Conditional; compression precedents strong | Low pending adjacent-field audit |
| Experimental clarity | Good if support labels are reproducible | Good accounting; future-task distribution must be declared | Hidden changes and source access complicate interpretation |
| Baseline availability | Strong conceptual baselines; code availability uneven | Strong simple baselines; trained compression optional | Very strong simple/classical baselines |
| Benchmark opportunity | Extension with uncertain lineage, not first lifecycle benchmark | Charge total storage plus future corrections | Time-indexed missing-notification protocol |
| Method contribution | Uncertainty-aware repair with alternative support | Revision-utility retention | Small verification policy; easiest to reduce to existing control |
| Analysis potential | High: missing/spurious edges, recurrence, bystanders | High: compression/revision tradeoff | High: drift and source availability |
| Compute feasibility | Moderate, API/classifier feasible | Moderate, trained latent baseline optional | Moderate; offline source replay preferred |
| Reproducibility | Needs public support annotations and fixed model IDs | Needs byte-complete accounting and released histories | Needs released time-indexed source snapshots |
| Scooping risk | High: several close Aug–Sep2026 papers | High: rapidly moving compression literature | High and substantial older adjacent prior art |

**Recommendation:** prioritize G1's novelty and annotation audit. G2 is the backup if the target deployment truly has a total-storage constraint. G3 is a reserve hypothesis, not an equally validated investment recommendation. None warrants implementing a full EvoMem architecture yet.
