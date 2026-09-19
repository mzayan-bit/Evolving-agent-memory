# EvoMem Research Gap Analysis

**Literature cutoff:19 September 2026. Research phase only; no EvoMem implementation.**

## 1. Executive Summary

The broad project idea is **not novel as stated**. Temporal validity, historical versions, memory update/delete operations, dependency propagation, learned lifecycle control, consolidation-quality evaluation and stale-memory metrics all have close precedents. The strongest plausible contribution is narrower:

> **Selective repair of persistent agent memory when dependency lineage is incomplete or inferred, with explicit measurement of stale descendant reuse, false invalidation, independent-support preservation and verification/replay cost.**

This is a **medium-confidence research hypothesis**, not a firstness claim. [Dependency-guided rollback repair](https://arxiv.org/abs/2608.10502) already preserves unaffected work under recorded dependencies; [PlanFence](https://arxiv.org/abs/2609.03340) already validates exact plan dependencies; [StateAuditor](https://arxiv.org/abs/2608.01619) already audits implicit stale premises; [CAMA](https://arxiv.org/abs/2608.19701) already infers latent evidence dependence. We must beat or meaningfully extend those assumptions and experiments.

The review retains100 unique works from104 bibliographic records, including25 deep reads. First-public distribution:2023: 7;2024: 10;2025: 18;2026: 65. It maps33 benchmarks, diagnostic suites and adapted evaluation protocols—not33 independent standardized benchmark releases. Two backup directions are revision-preserving compression under a *total* storage budget and budgeted external revalidation under unannounced change. The latter has lower novelty confidence.

## 2. Scope and Search Methodology

The review covers formation, representation, retrieval, update, contradiction, temporal validity, forgetting, consolidation, dependencies, provenance, uncertainty, learned control, agentic RAG, evaluation and efficiency. It prioritizes2025–26 primary work while retaining2023–24 foundations. Surveys supplied maps; primary methods and experiments supplied gap evidence.

Sources include arXiv abstracts/HTML, official ACL Anthology publications, OpenReview leads and paper-associated repositories. A narrative search audit and recoverable exact adversarial queries are in [search_log.md](literature/search_log.md) and [adversarial_queries.json](literature/adversarial_queries.json). This is a broad iterative investigation, not an exhaustive systematic-review claim. Full source text is not redistributed; the [source manifest](literature/source_manifest.json) records inspected versions, section links and hashes.

The [master CSV](literature/master_paper_matrix.csv) separates deep reads, targeted primary inspections and bibliographic/abstract screens. NR means not established in this review. The [version ledger](literature/version_ledger.md) pins revisions, separates venue year from first-public year, groups the early MemOS treatment with its expanded work, and distinguishes two unrelated papers both called SkillZip. A conference link is not a claim that every difference from the inspected arXiv text was reconciled.

Major survey maps: [Memory Mechanism Survey](https://arxiv.org/abs/2404.13501), [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564), [From Storage to Experience](https://arxiv.org/abs/2605.06716), [Long-Term Memory Security Survey](https://arxiv.org/abs/2604.16548) and [Graph-Based Personalized Memory](https://arxiv.org/abs/2609.08599). The last is useful for recent discovery, not stronger empirical authority merely because it is newer.

## 3. Terminology and Taxonomy

**Memory** is persistent state that later influences an agent. **RAG** supplies retrieved evidence for a query; it can implement part of memory but need not decide how experience is written, revised or forgotten. **Working context** is what the current model invocation can see; a small context does not imply small persistent storage.

| Dimension | Questions and established mechanisms |
|---|---|
| A Formation/write | Unconditional logging; salience/importance; LLM extraction; trained CRUD; evidence-governed promotion |
| B Representation | Raw episodes, summaries, semantic facts, procedural skills, vectors, graphs, latent state and parametric/hybrid memory |
| C Retrieval | Sparse/dense/hybrid relevance, recency, importance, graph traversal, temporal filters and adaptive stopping |
| D Updating | Overwrite, append version, replace slot, preserve inactive historical state, revise confidence |
| E Contradiction | Same-scope conflict, source authority, competing beliefs, missing/current state and consistency checks |
| F Time | Event time versus ingestion time; validity intervals; current versus historical queries |
| G Forgetting | Capacity eviction, semantic invalidation, policy revocation, physical deletion and influence unlearning |
| H Consolidation | Summarization/reflection, clustering, abstraction, recurrence and learned operator selection |
| I Dependencies | Association, logical prerequisite, copied-source lineage and alternative support are different relations |
| J Provenance | Evidence origin, timestamps, source authority and transformation lineage |
| K Uncertainty | Heuristic confidence, competing candidates, abstention/review and measured calibration |
| L Learned management | Trained LM policies, small classifiers and online bandits; prompted LLM choice alone is not trained control |
| M Agentic RAG | Query planning, external retrieval, corrective evidence, store routing and stopping |
| N Evaluation | Recall, dynamic state, operations, action consequences, repair and long-horizon degradation |
| O Efficiency | All stored bytes, active tokens, ingestion/retrieval calls, latency, cost and useful completion |

These distinctions are grounded in [Zep](https://arxiv.org/abs/2501.13956), [MemTX](https://arxiv.org/abs/2607.23929), [BeliefMem](https://arxiv.org/abs/2605.05583), [AuthMem](https://arxiv.org/abs/2608.01679), [AgeMem](https://arxiv.org/abs/2601.01885) and the linked surveys. The detailed [failure taxonomy](literature/failure_taxonomy.md) defines false, historical, superseded, contradicted, uncertain, revoked and forgotten separately.

## 4. State of the Field

Early approaches already accumulated reflections, skills and long-lived conversations: [Reflexion](https://arxiv.org/abs/2303.11366), [Generative Agents](https://arxiv.org/abs/2304.03442), [Voyager](https://arxiv.org/abs/2305.16291), [MemoryBank](https://arxiv.org/abs/2305.10250), [ExpeL](https://arxiv.org/abs/2308.10144) and [MemGPT](https://arxiv.org/abs/2310.08560).2024 work broadened graph retrieval, latent updates and long-conversation evaluation through HippoRAG, AriGraph, MEMORYLLM, LoCoMo and LongMemEval.

By 2025, memory was already selectively extracted and updated ([Mem0](https://arxiv.org/abs/2504.19413)), dynamically linked ([A-MEM](https://arxiv.org/abs/2502.12110)), temporally versioned ([Zep](https://arxiv.org/abs/2501.13956)) and learned through RL ([Memory-R1](https://arxiv.org/abs/2508.19828), [Mem-alpha](https://arxiv.org/abs/2509.25911)). It is therefore wrong to characterize this period as uniformly static vector retrieval.

The 2026 literature directly addresses stale dependencies, lifecycle governance, operation diagnosis, evidence authority, bounded consolidation and post-failure recovery. This substantially narrows the opportunity. The research frontier suggested by the inspected evidence concerns **assumptions and tradeoffs**—incomplete lineage, changing evidence, calibration, information access and cost—not whether a memory store should have an UPDATE action.

## 5. Major Memory Architecture Families

| Family | Representative work | Benefit | Boundary to test |
|---|---|---|---|
| Raw/episodic retrieval | MemGPT, LoCoMo baselines | Auditability and exact evidence | Storage growth and retrieval/reader failures |
| Extracted facts and profiles | Mem0, MemoryBank | Compact reusable information | Missed qualifiers, overwrite and scope binding |
| Associative graphs | HippoRAG, A-MEM, AriGraph | Multi-hop/relational access | Association is not logical support |
| Temporal/state graphs | Zep, TOKI, MemStrata, StateMem | Current/historical state and supersession | Fallible extraction and ambiguous dependencies |
| Reflective/experiential/procedural | Reflexion, ExpeL, Voyager, Dynamic Cheatsheet | Reuse successful reasoning and skills | False generalization and changing applicability |
| Unified learned controllers | AgeMem, VerMem, MemCon | Adaptive operation choice | Training reward and benchmark coverage limit guarantees |
| Latent/parametric/hybrid | MEMORYLLM, R3Mem, MemOS, Dual-Layer | Alternative capacity/retention tradeoffs | Training/access cost and difficult provenance |
| Governed/recoverable state | MemTX, ChronoMem, rollback repair | Explicit authority, versioning and recovery | Completeness of lineage and replay assumptions |

The [capability matrix](literature/capability_matrix.md) has the requested22 dimensions with explicit/partial/unknown support and source pointers. Its flags describe stated capabilities; they are not a leaderboard or an assurance certificate.

## 6. Existing Benchmarks

The [benchmark matrix](literature/benchmark_matrix.md) covers33 named suites/protocols, their scale, provenance, dynamic behavior, operation coverage, metrics and limitations. The most consequential distinctions are:

- **Conversational recall and evolution:** LoCoMo, LongMemEval, PersonaMem and Memora.
- **Incremental learning and forgetting:** MemoryAgentBench, Evo-Memory and EvoMemBench.
- **State/action coupling:** MemoryArena, MEMTRACK, LongMemEval-V2 and PersonaMem-v3.
- **Stale state/dependency behavior:** STALE, StateMemBench, AgingBench and MemStrata evaluations.
- **Operation and consolidation diagnosis:** HaluMem, MemFail, MemOps and AuthMem-Bench.
- **Security, governance and recovery:** MemSecBench, GovMem, MemTX, ChronoMem, rollback repair and execution-state unlearning.

LongMemEval already tests updates and abstention; MAB's inspected v4 includes selective forgetting; MemOps represents gold lifecycle operations and their compositions. “First benchmark beyond recall” is untenable. LongMemEval-V2 reaches approximately25M/115M-token trajectory histories, while StateMemBench's hundreds of turns contain roughly3K/7–15K tokens. Neither session count nor token count alone defines difficulty. See [LME-V2 §3](https://arxiv.org/html/2605.12493v1#S3) and [StateMem §4](https://arxiv.org/html/2608.19652v1#S4).

## 7. What Current Systems Solve Well

Within controlled scopes, existing work provides useful temporal retention, compact fact extraction, associative retrieval, adaptive operation choice and selective recovery. Zep retains expired edges; Mem0 chooses CRUD actions; A-MEM evolves linked note context; AgeMem/VerMem learn unified memory/context operations; MemTX defines explicit lifecycle governance; PlanFence validates plan dependencies; rollback repair preserves independent support.

These are **existence counterexamples**, not claims of universal reliability. Uncertainty is already represented in BeliefMem/Hindsight, but representation is not calibration. Dependency graphs are already used, but extraction completeness is a separate question. A reader must distinguish a demonstrated controlled capability from a deployment-wide semantic guarantee. The25 [deep reads](literature/deep_reads/) record that boundary paper by paper.

## 8. Repeated Failure Modes

The synthesis identifies write omission, wrong entity/scope binding, retrieval omission, stale selection, incorrect overwrite, lost qualifiers, authority amplification, correlated evidence, incomplete propagation, over-invalidation, stale-plan execution and residual influence after deletion. These are supported across [HaluMem](https://arxiv.org/abs/2511.03506), [MemFail](https://arxiv.org/abs/2605.26667), [AuthMem](https://arxiv.org/abs/2608.01679), [CAMA](https://arxiv.org/abs/2608.19701), [PlanFence](https://arxiv.org/abs/2609.03340) and [execution-state unlearning](https://arxiv.org/abs/2609.04875).

Two recurring evaluation traps matter. First, a system can delete all memory and look safe on removal while destroying benign utility; MemSecBench measures both. Second, a method can reduce answer-context tokens while retaining an unlimited archive; TierMem and RD-Forget make that architecture explicit. We infer that total-state accounting and preservation controls are necessary for the proposed experiments—not that those papers misstate their own goals.

Conflicting findings should be retained. [LightMem reproduction](https://arxiv.org/abs/2607.29104) challenges general superiority over naive RAG. [MemoryLake's matched study](https://arxiv.org/abs/2608.13883) explicitly distinguishes system-level matching from cost matching. OAS's non-oracle appendix is less favorable than its primary oracle-evidence setting; StateAuditor does not improve every harder transfer set. These are reasons to prioritize controlled baselines over cross-paper SOTA rankings.

## 9. Candidate Research Gaps

Full templates, hypotheses, experiments, ablations, compute and kill criteria are in [candidate_gaps.md](candidate_gaps.md).

| ID | Narrow question | Closest competitors | Confidence |
|---|---|---|---|
| G1 | Can selective persistent repair remain reliable with incomplete/inferred lineage and alternative support? | Rollback repair, StateAuditor, PlanFence, StateMem/CUPMem, CAMA/GovMem | Medium, conditional |
| G2 | What evidence should survive a total-storage cap to support unknown future corrections and historical queries? | OAS, RD-Forget, TierMem, R3Mem, ChronoMem, SkillZip Pro | Medium-low |
| G3 | When should memory be revalidated if the world changes without notification, under a strict check budget? | MCB, MemCon, PlanFence, Router-Mem, adaptive/corrective RAG, classical refresh | Low; reserve |

These are relative shortlist choices, not three equally validated gaps. A complete new “lifecycle-aware architecture” combining all three would be too broad and would conceal prior art.

## 10. Adversarial Novelty Checks

The search deliberately removed attractive ideas. Temporal supersession found Zep/TOKI/MemStrata; lifecycle states found MemTX/CUPMem; dependent revision found StateMem/PlanFence/rollback repair; consolidation evaluation found HaluMem/TRUSTMEM/OAS/MemOps/MemFail. Correlation-aware confidence found GovMem/CAMA. Reversible compression found R3Mem, ChronoMem, RD-Forget and SkillZip variants. Generic causal diagnosis found MemAudit, CausalFlow, CAR and the Misattribution Gap.

For G1, the surviving difference is not inference or dependency repair separately: it is the measured behavior of **persistent repair under uncertain lineage**, repeated changes and alternative sufficient support. For G2, it is not reversible compression: it is **future semantic correction under a charged total factual-state budget**. For G3, it is not retrieval routing: it is **longitudinal executed revalidation under withheld changes**, and older cache-control prior art may still eliminate novelty. Search traces and decisions are recorded in the [search audit](literature/search_log.md).

## 11. Novelty Threat Matrix

The [full matrix](novelty_threat_matrix.md) evaluates the user's12 preliminary questions plus correlation and causal-diagnosis candidates. Most broad claims are invalidated; others require narrowing. In particular:

- Previously true versus false: already expressible through temporal validity and historical views.
- Explicit lifecycle states: already present under several vocabularies.
- Semantic forgetting, stale-reuse metrics and operation diagnosis: already studied directly.
- Unified learned management and efficiency optimization: already established research topics.
- Routing across *every* named memory/knowledge source is not verified here, but combining a longer list is not automatically novel.
- Bounded *active context* is well covered; bounded *total retained information* with future correction remains a conditional distinction.

Novelty risk is high for all finalists because the closest2026 papers are recent and directly adjacent. A medium confidence gap can coexist with high overlap/scooping risk.

## 12. Final 3–5 Directions

**1. Selective Memory Repair under Uncertain Dependency Lineage.** Minimum paper: an audited uncertain-lineage extension, strong explicit/inferred dependency baselines, a calibrated retain/reverify/repair rule and a matched-budget preservation analysis. Strong version: repeated revisions, natural-language support ambiguity and cross-domain transfer. Main risk: merely combining rollback repair with StateAuditor/CAMA. This is the lead.

**2. Revision-Preserving Memory Compression under a Total Storage Budget.** Minimum paper: total-byte accounting, future correction/history tasks and a support-retention policy beating simple compression/eviction baselines. Strong version: continual re-compression with declared limits and real change histories. Main risk: storage is practically cheap or SkillZip/R3Mem/OAS extensions already cover the distinction.

**3. Budgeted Revalidation under Unannounced World Changes.** Minimum paper: frozen time-indexed source replay, missing notifications, strong TTL/hazard/RAG baselines and executed check decisions. Strong version: drift-aware calibration and imperfect source availability. Main risk: classical refresh or MCB+MemCon already supplies the essential method. This remains a reserve until the adjacent review is completed.

Each direction's required data, full experiment plan, baselines, metrics and ablations are specified in [candidate_gaps.md](candidate_gaps.md), rather than being left as future planning work.

## 13. Leading Direction

**Select G1 for the next research audit, not immediate system development.** It has the clearest evidence-supported boundary: PlanFence assumes exact complete dependencies and shows missing-edge sensitivity; rollback repair follows recorded provenance; StateMem uses explicit dependencies; StateAuditor infers implicit premises but its semantic gate and transfer performance are limited. CAMA and GovMem prevent us from claiming that uncertainty or inferred evidence grouping itself is novel.

The plausible contribution is a **method-and-analysis result** showing when uncertain support information is sufficient for selective repair, and when revalidation or conservative replay is necessary. It must retain unaffected and independently supported knowledge while reducing stale reuse at matched cost. A useful negative finding could identify conditions under which selective repair is untrustworthy.

**The paper appearing tomorrow that would most threaten this direction:** a system that learns or calibrates incomplete semantic dependency/support sets, repairs persistent descendants through repeated updates, preserves alternative support, and demonstrates better stale-error/false-invalidation/cost tradeoffs than StateAuditor, CAMA-style inference and explicit-edge rollback on public plus naturalistic data. That would cover the intended contribution almost directly.

## 14. Proposed Initial Research Questions

- RQ1: How do missing versus spurious dependency edges change stale descendant reuse and false invalidation?
- RQ2: Does preserving alternative sufficient support improve repair beyond a single parent graph?
- RQ3: Can uncertainty-aware retain/reverify/repair improve the risk–coverage frontier over point-estimate inference at equal cost?
- RQ4: Do improvements survive repeated revisions, domain shift and removal of gold fault/scope information?
- RQ5: Which part of any gain comes from better dependency inference, more evidence, or a more conservative action policy?

These questions explicitly extend the assumptions of the closest work; they do not claim to invent truth maintenance. Classical belief revision, provenance and truth-maintenance systems remain conceptual prior art that must be acknowledged in a future paper.

## 15. Potential Hypotheses

H1: Missing edges primarily increase stale descendant reuse; spurious edges primarily increase unnecessary invalidation/cost. Test interactions rather than assume separability.

H2: Alternative-support preservation improves benign retention relative to broad closure without increasing stale risk when support validity is correctly assessed. Under misclassified support, it may instead preserve bad beliefs.

H3: Empirically calibrated uncertainty with a reverify option outperforms a point-estimate graph at fixed stale-risk targets on held-out in-domain cases; the advantage shrinks under shifted language/source distributions.

H4: More verifier calls alone explain part of apparent improvement. Matching calls and evidence access may remove the method advantage. Pre-register this as a potential disconfirming result.

No hypothesis has been experimentally tested in this review.

## 16. Minimum Experimental Design

**Stage0, before implementation:** manually annotate30 support/revision cases and reconcile disagreements; audit the closest five papers' code/protocols and exact revisions. Specify what counts as a logical prerequisite, copied evidence, alternative support and policy revocation. Stop if annotators cannot reproducibly label the target.

**Pilot:**60 cases ×6 baseline/policy conditions ×2 backbone families =720 trajectories, initially with one deterministic setting. Include explicit-edge repair, source-only deletion, broad closure, point-estimate inferred edges, audit/repair and conservative replay. The hypothetical uncertainty-aware method may first be evaluated as an offline decision table, without building an entire agent architecture.

**Full study only if pilot warrants it:** approximately300 source scenarios, eight policies, two backbones and three stochastic seeds =14,400 trajectories, with trajectory-clustered uncertainty intervals. Factor lineage missingness/spuriousness, alternative support, update count and source authority through balanced subsets rather than multiplying every axis blindly. Use held-out domain/template/entity splits and a manually audited natural-language slice.

Score current/historical accuracy, stale descendant reuse, false invalidation, support retention, recurrence, abstention/coverage, tokens, calls, replay steps and latency. Report macro and per-regime results, explicit denominators, failure cases and Pareto curves. Do not credit deleting everything, abstaining everywhere, gold future evidence or extra calls as a genuine method gain. Existing metrics are credited, not renamed.

## 17. Compute Feasibility

The recommended start uses API inference, embeddings and deterministic bookkeeping; a small classifier or quantized8B model is optional. It does not require pretraining or full RL. The pilot planning assumption of four2K-input/250-output calls per trajectory yields about5.76M input and0.72M output tokens for720 trajectories, **before ingestion, judge calls and retries**. Actual cost is:

`input_tokens × provider_input_rate + output_tokens × provider_output_rate + embeddings + retrieval infrastructure + retries`.

Price the measured pilot with current chosen model rates before spending. No API experiment has been launched and no provider-cost quote is asserted. Qualitatively, G1 is moderate pilot cost with potentially substantial full-grid cost; G2 adds repeated compression; G3 is moderate with offline replay but potentially high with live browsing.

Training replication can be much heavier: [Mem-alpha](https://arxiv.org/abs/2509.25911) reports32 H100 GPUs for approximately three days, and [Memory-R1](https://arxiv.org/abs/2508.19828) reports multiple H100s. Conversely [MemCon](https://arxiv.org/abs/2607.13591) uses a lightweight online controller, and StateAuditor reports a small QLoRA setting. Model parameter count alone is a poor compute estimate. The [learned-policy map](literature/learned_memory_policies.md) records states/actions/rewards/generalization/compute and missing details.

## 18. Key Papers to Reproduce / Use as Baselines

Priority1: dependency-guided rollback repair, StateAuditor, PlanFence, StateMem/CUPMem and CAMA. First establish whether their released code or a faithful reimplementation actually exposes the assumed uncertainty boundary. Keep prevention, query repair and persistent recovery tasks distinct.

Priority2: MemTX for governance/alternative support, MemAudit for diagnosis, and execution-state unlearning/ChronoMem as conservative recovery controls. MemSecBench supplies benign-preservation and recurrence evaluation ideas; MemOps/HaluMem help expose state corruption hidden by final answers.

Priority3: simple dense/lexical retrieval, explicit slot supersession, full-history or gold-state upper bounds, and no-memory/no-repair controls. A simple baseline winning is a useful result. Avoid reproducing every large RL system before establishing headroom. The [deep-read notes](literature/deep_reads/) explain exact scope and reproducibility risks.

## 19. What We Should NOT Claim

Do not claim first temporal memory, first lifecycle state machine, first dependency-aware update, first semantic forgetting, first learned memory policy, first beyond-recall benchmark, first stale-error metric, first consolidation-fidelity evaluation, first provenance-aware uncertainty or first reversible compression. The [threat matrix](novelty_threat_matrix.md) gives counterexamples.

Do not call confidence scores calibrated without calibration evidence. Do not treat association as entailment, newer as more authoritative, all sources as independent, or a revoked label as enforced. Do not compare oracle and non-oracle systems as peers, combine mismatched answerers/judges into a leaderboard, or describe100 screened works as100 full reproductions.

Do not claim exact unlearning for parameters or irreversible external actions from record deletion. Do not promise bounded storage with free archives. Do not imply that a broad conjunction of already known components is novel. Do not publish under “EvoMem” without checking name overlap with Evo-Memory and EvoMemBench.

## 20. Immediate Next Research Steps

1. Freeze G1's one-paragraph claim and explicit non-claims from this report.
2. Audit the exact code/version/protocols for rollback repair, StateAuditor, PlanFence, CAMA and StateMem/CUPMem; update the threat matrix with any missing capability.
3. Manually construct/adjudicate30 cases containing uncertain prerequisites, alternative support and repeated changes. This is a research annotation exercise, not a benchmark generator.
4. Draft a preregistered comparison specifying information access, cost, metrics, splits and kill criteria. Obtain a measured pilot cost estimate.
5. Only after the novelty and annotation gates survive, decide whether to implement a small experimental adapter. Do not build the full EvoMem system from the preliminary architecture intuition.

The practical answer is therefore: **we may contribute a defensible uncertainty-aware repair result and evaluation protocol, provided it beats existing repair/inference methods under explicitly incomplete lineage. We cannot plausibly contribute “evolving agent memory” as a new concept.**

## References

The complete verified metadata bibliography is [references.bib](literature/references.bib). The [human-readable matrix](literature/master_paper_matrix.md) and [CSV](literature/master_paper_matrix.csv) contain100 records with first-public dates, authors, inspected revisions, publication-status caveats and code/project links where verified. Important conclusions link primary papers inline;25 dedicated notes provide method/evaluation/appendix evidence rather than relying only on abstracts.
