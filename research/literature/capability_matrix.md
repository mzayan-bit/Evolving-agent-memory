# Capability matrix

✅ explicitly described/tested; ◐ partial, restricted or proxy support; ❌ no positive evidence in inspected scope or explicit exclusion (not a universal impossibility); ? not established. Temporal metadata does not imply temporal QA; confidence scores do not imply calibration. Graph links do not imply logical dependencies. External retrieval means live outside knowledge/tool evidence, not reading the agent’s own store. Long horizon is benchmark-relative and is qualified in the benchmark matrix.

Rows are systems, not benchmark-only papers. Each row links to its pinned primary source and evidence note; column numbers below match the requested capability order.

## Formation and representation

| System / evidence | Selective Write | Importance Filtering | Episodic Memory | Semantic Memory | Graph Memory | Temporal Metadata | Memory Versioning |
|---|---|---|---|---|---|---|---|
| [Zep](https://arxiv.org/abs/2501.13956v1) | ? | ? | ✅ | ✅ | ✅ | ✅ | ✅ |
| [Mem0](https://arxiv.org/abs/2504.19413v1) | ✅ | ? | ◐ | ✅ | ◐ | ? | ? |
| [A-MEM](https://arxiv.org/abs/2502.12110v11) | ✅ | ? | ✅ | ✅ | ✅ | ✅ | ? |
| [Hindsight](https://arxiv.org/abs/2512.12818v1) | ? | ? | ✅ | ✅ | ✅ | ✅ | ◐ |
| [AgeMem](https://arxiv.org/abs/2601.01885v3) | ✅ | ◐ | ◐ | ✅ | ? | ? | ❌ |
| [Memory-R1](https://arxiv.org/abs/2508.19828v5) | ✅ | ◐ | ? | ✅ | ? | ? | ? |
| [Mem-alpha](https://arxiv.org/abs/2509.25911v1) | ✅ | ◐ | ✅ | ✅ | ? | ? | ? |
| [STALE / CUPMem](https://arxiv.org/abs/2605.06527v1) | ? | ? | ? | ✅ | ◐ | ◐ | ◐ |
| [MemTX](https://arxiv.org/abs/2607.23929v2) | ✅ | ? | ? | ? | ✅ | ✅ | ✅ |
| [PlanFence](https://arxiv.org/abs/2609.03340v1) | ? | ? | ? | ? | ? | ✅ | ✅ |
| [Dependency-guided Rollback](https://arxiv.org/abs/2608.10502v1) | ? | ? | ? | ? | ✅ | ? | ◐ |
| [StateAuditor](https://arxiv.org/abs/2608.01619v1) | ? | ? | ? | ? | ? | ✅ | ? |
| [Execution-state Unlearning](https://arxiv.org/abs/2609.04875v1) | ? | ? | ◐ | ? | ? | ✅ | ✅ |
| [OAS](https://arxiv.org/abs/2607.17545v2) | ◐ | ◐ | ? | ? | ? | ? | ❌ |
| [TRUSTMEM](https://arxiv.org/abs/2606.25161v1) | ✅ | ◐ | ✅ | ✅ | ? | ? | ? |
| [BeliefMem](https://arxiv.org/abs/2605.05583v2) | ? | ? | ? | ✅ | ? | ✅ | ✅ |
| [StateMem](https://arxiv.org/abs/2608.19652v1) | ◐ | ? | ? | ✅ | ✅ | ✅ | ✅ |
| [VerMem](https://arxiv.org/abs/2608.03137v1) | ✅ | ? | ✅ | ✅ | ? | ✅ | ✅ |
| [TierMem](https://arxiv.org/abs/2602.17913v1) | ? | ? | ✅ | ◐ | ? | ? | ? |
| [CAMA](https://arxiv.org/abs/2608.19701v1) | ? | ? | ? | ? | ✅ | ? | ❌ |
| [GovMem](https://arxiv.org/abs/2607.02579v1) | ✅ | ◐ | ? | ? | ◐ | ? | ? |
| [ChronoMem](https://arxiv.org/abs/2607.27773v2) | ? | ? | ✅ | ? | ? | ✅ | ✅ |
| [RD-Forget](https://arxiv.org/abs/2609.10263v1) | ? | ? | ✅ | ✅ | ? | ✅ | ◐ |
| [MemCon](https://arxiv.org/abs/2607.13591v1) | ◐ | ◐ | ◐ | ? | ? | ? | ❌ |
| [Self-RAG](https://arxiv.org/abs/2310.11511v1) | ? | ? | ? | ? | ? | ? | ? |
| [Corrective RAG](https://arxiv.org/abs/2401.15884v3) | ? | ? | ? | ? | ? | ? | ? |
| [Adaptive-RAG](https://arxiv.org/abs/2403.14403v2) | ? | ? | ? | ? | ? | ? | ? |
| [SkillZip Pro](https://arxiv.org/abs/2608.30785v1) | ? | ? | ? | ? | ✅ | ? | ◐ |

## Revision and evidence quality

| System / evidence | Update | Supersession | Contradiction Detection | Provenance | Uncertainty | Consolidation | Selective Forgetting |
|---|---|---|---|---|---|---|---|
| [Zep](https://arxiv.org/abs/2501.13956v1) | ✅ | ✅ | ✅ | ✅ | ? | ◐ | ? |
| [Mem0](https://arxiv.org/abs/2504.19413v1) | ✅ | ◐ | ✅ | ? | ? | ◐ | ✅ |
| [A-MEM](https://arxiv.org/abs/2502.12110v11) | ✅ | ? | ? | ? | ? | ✅ | ? |
| [Hindsight](https://arxiv.org/abs/2512.12818v1) | ✅ | ◐ | ✅ | ✅ | ✅ | ✅ | ❌ |
| [AgeMem](https://arxiv.org/abs/2601.01885v3) | ✅ | ? | ? | ? | ? | ✅ | ✅ |
| [Memory-R1](https://arxiv.org/abs/2508.19828v5) | ✅ | ◐ | ◐ | ? | ? | ◐ | ✅ |
| [Mem-alpha](https://arxiv.org/abs/2509.25911v1) | ✅ | ? | ? | ? | ? | ✅ | ✅ |
| [STALE / CUPMem](https://arxiv.org/abs/2605.06527v1) | ✅ | ✅ | ✅ | ◐ | ◐ | ◐ | ◐ |
| [MemTX](https://arxiv.org/abs/2607.23929v2) | ✅ | ✅ | ✅ | ✅ | ✅ | ◐ | ◐ |
| [PlanFence](https://arxiv.org/abs/2609.03340v1) | ✅ | ✅ | ? | ✅ | ? | ? | ◐ |
| [Dependency-guided Rollback](https://arxiv.org/abs/2608.10502v1) | ✅ | ✅ | ? | ✅ | ? | ◐ | ◐ |
| [StateAuditor](https://arxiv.org/abs/2608.01619v1) | ◐ | ✅ | ◐ | ✅ | ◐ | ? | ❌ |
| [Execution-state Unlearning](https://arxiv.org/abs/2609.04875v1) | ✅ | ? | ? | ✅ | ? | ◐ | ✅ |
| [OAS](https://arxiv.org/abs/2607.17545v2) | ? | ? | ? | ? | ? | ✅ | ◐ |
| [TRUSTMEM](https://arxiv.org/abs/2606.25161v1) | ✅ | ? | ? | ◐ | ? | ✅ | ✅ |
| [BeliefMem](https://arxiv.org/abs/2605.05583v2) | ✅ | ✅ | ✅ | ◐ | ✅ | ✅ | ◐ |
| [StateMem](https://arxiv.org/abs/2608.19652v1) | ✅ | ✅ | ✅ | ✅ | ◐ | ◐ | ◐ |
| [VerMem](https://arxiv.org/abs/2608.03137v1) | ✅ | ◐ | ? | ◐ | ? | ✅ | ✅ |
| [TierMem](https://arxiv.org/abs/2602.17913v1) | ? | ? | ? | ✅ | ? | ◐ | ❌ |
| [CAMA](https://arxiv.org/abs/2608.19701v1) | ? | ? | ◐ | ✅ | ✅ | ? | ? |
| [GovMem](https://arxiv.org/abs/2607.02579v1) | ? | ? | ✅ | ✅ | ✅ | ? | ? |
| [ChronoMem](https://arxiv.org/abs/2607.27773v2) | ✅ | ◐ | ? | ✅ | ? | ? | ◐ |
| [RD-Forget](https://arxiv.org/abs/2609.10263v1) | ✅ | ✅ | ✅ | ✅ | ? | ◐ | ◐ |
| [MemCon](https://arxiv.org/abs/2607.13591v1) | ? | ? | ? | ? | ? | ✅ | ✅ |
| [Self-RAG](https://arxiv.org/abs/2310.11511v1) | ? | ? | ? | ? | ◐ | ? | ? |
| [Corrective RAG](https://arxiv.org/abs/2401.15884v3) | ? | ? | ? | ? | ◐ | ? | ? |
| [Adaptive-RAG](https://arxiv.org/abs/2403.14403v2) | ? | ? | ? | ? | ? | ? | ? |
| [SkillZip Pro](https://arxiv.org/abs/2608.30785v1) | ✅ | ? | ? | ✅ | ? | ✅ | ❌ |

## Control and evaluation

| System / evidence | Learned Memory Policy | Adaptive Retrieval | External Retrieval | Multi-hop Retrieval | Dependency Propagation | Long-horizon Evaluation | Dynamic Knowledge Benchmark | Cost Evaluation |
|---|---|---|---|---|---|---|---|---|
| [Zep](https://arxiv.org/abs/2501.13956v1) | ? | ? | ? | ◐ | ❌ | ✅ | ✅ | ✅ |
| [Mem0](https://arxiv.org/abs/2504.19413v1) | ❌ | ? | ? | ? | ❌ | ✅ | ? | ✅ |
| [A-MEM](https://arxiv.org/abs/2502.12110v11) | ❌ | ? | ? | ◐ | ❌ | ✅ | ? | ✅ |
| [Hindsight](https://arxiv.org/abs/2512.12818v1) | ? | ◐ | ? | ✅ | ? | ✅ | ✅ | ? |
| [AgeMem](https://arxiv.org/abs/2601.01885v3) | ✅ | ✅ | ? | ❌ | ❌ | ? | ? | ✅ |
| [Memory-R1](https://arxiv.org/abs/2508.19828v5) | ✅ | ✅ | ? | ? | ❌ | ✅ | ◐ | ✅ |
| [Mem-alpha](https://arxiv.org/abs/2509.25911v1) | ✅ | ❌ | ? | ? | ❌ | ✅ | ? | ✅ |
| [STALE / CUPMem](https://arxiv.org/abs/2605.06527v1) | ❌ | ? | ? | ✅ | ✅ | ✅ | ✅ | ? |
| [MemTX](https://arxiv.org/abs/2607.23929v2) | ❌ | ? | ? | ✅ | ✅ | ❌ | ✅ | ✅ |
| [PlanFence](https://arxiv.org/abs/2609.03340v1) | ❌ | ? | ✅ | ? | ✅ | ◐ | ✅ | ✅ |
| [Dependency-guided Rollback](https://arxiv.org/abs/2608.10502v1) | ❌ | ? | ? | ? | ✅ | ◐ | ✅ | ✅ |
| [StateAuditor](https://arxiv.org/abs/2608.01619v1) | ◐ | ◐ | ? | ? | ◐ | ✅ | ✅ | ✅ |
| [Execution-state Unlearning](https://arxiv.org/abs/2609.04875v1) | ❌ | ? | ? | ? | ✅ | ◐ | ? | ✅ |
| [OAS](https://arxiv.org/abs/2607.17545v2) | ✅ | ? | ? | ? | ❌ | ◐ | ? | ✅ |
| [TRUSTMEM](https://arxiv.org/abs/2606.25161v1) | ✅ | ? | ? | ? | ❌ | ✅ | ? | ✅ |
| [BeliefMem](https://arxiv.org/abs/2605.05583v2) | ❌ | ? | ? | ? | ❌ | ✅ | ? | ? |
| [StateMem](https://arxiv.org/abs/2608.19652v1) | ❌ | ? | ? | ✅ | ✅ | ✅ | ✅ | ✅ |
| [VerMem](https://arxiv.org/abs/2608.03137v1) | ✅ | ✅ | ? | ? | ❌ | ❌ | ? | ✅ |
| [TierMem](https://arxiv.org/abs/2602.17913v1) | ✅ | ✅ | ? | ? | ? | ✅ | ? | ✅ |
| [CAMA](https://arxiv.org/abs/2608.19701v1) | ✅ | ✅ | ? | ✅ | ◐ | ✅ | ✅ | ✅ |
| [GovMem](https://arxiv.org/abs/2607.02579v1) | ? | ? | ? | ? | ◐ | ❌ | ? | ✅ |
| [ChronoMem](https://arxiv.org/abs/2607.27773v2) | ? | ? | ? | ? | ❌ | ✅ | ✅ | ? |
| [RD-Forget](https://arxiv.org/abs/2609.10263v1) | ❌ | ? | ? | ✅ | ? | ✅ | ✅ | ✅ |
| [MemCon](https://arxiv.org/abs/2607.13591v1) | ✅ | ✅ | ? | ? | ❌ | ✅ | ? | ✅ |
| [Self-RAG](https://arxiv.org/abs/2310.11511v1) | ✅ | ✅ | ✅ | ? | ❌ | ? | ? | ✅ |
| [Corrective RAG](https://arxiv.org/abs/2401.15884v3) | ◐ | ✅ | ✅ | ? | ❌ | ? | ? | ? |
| [Adaptive-RAG](https://arxiv.org/abs/2403.14403v2) | ✅ | ✅ | ✅ | ✅ | ❌ | ? | ? | ✅ |
| [SkillZip Pro](https://arxiv.org/abs/2608.30785v1) | ? | ? | ? | ? | ✅ | ? | ? | ✅ |

## Evidence and important qualifications

- **Zep**: [Deep read](deep_reads/2501.13956.md). S2 defines graph and temporal fields; S3 gives hybrid retrieval; S4 specifies datasets, compared models and results. Entity/edge extraction and contradiction adjudication remain fallible. Temporal conflict on a fact is not a proof that all derived beliefs or pending actions have been repaired. Benchmark comparisons use particular answerer/judge choices.
- **Mem0**: [Deep read](deep_reads/2504.19413.md). S2 algorithms; S3 evaluation; S4 Table 2 latency/cost; S5 discussion. Nearest-candidate selection can miss a contradictory record. A correct CRUD decision on visible candidates does not imply a globally consistent store. Historical retention is not a safety invariant of destructive updates.
- **A-MEM**: [Deep read](deep_reads/2502.12110.md). S3 note fields, linking and evolution; S4 component ablations and S4.6 scaling; S6 limitations. Rewriting neighboring context may spread an incorrect inference. There is no demonstrated invariant that updates retract precisely the logically dependent notes while preserving independent support.
- **Hindsight**: [Deep read](deep_reads/2512.12818.md). S3–S6 architecture; S7 experimental settings; S9 future directions; Appendix A confidence rules. Heuristic confidence reinforcement is not calibrated probability. The inspected evaluation contains an unresolved retrieval-budget placeholder and mixed external baseline reports, limiting reproducibility and leaderboard interpretation.
- **AgeMem**: [Deep read](deep_reads/2601.01885.md). S3 state/actions/rewards and curriculum; S4 results/ablations; limitations/discussion. ACL 2026 publication is independently indexed. Optimizing terminal task success can reward harmful memory shortcuts not exposed by the task. CRUD plus summarization is not a demonstrated safe supersession/rollback policy.
- **Memory-R1**: [Deep read](deep_reads/2508.19828.md). S3 training; S4 datasets and S4.4 ablations; Appendix D compute details. Question-level split sizes do not themselves demonstrate persona/history-disjoint generalization. Candidate retrieval coverage is a separate bottleneck. Reward does not certify contradiction or temporal correctness.
- **Mem-alpha**: [Deep read](deep_reads/2509.25911.md). S3 memory/rewards; S4 experimental setup; S5 limitations; Appendix C model behavior. A 4B policy is not automatically a small-compute project: rollout and optimization dominate. Fixed retrieval isolates one component but does not solve jointly calibrated lifecycle control.
- **STALE / CUPMem**: [Deep read](deep_reads/2605.06527.md). S3 conflict types/probes; S4.4 adoption analysis; S5 CUPMem; Appendix A scope and F design. Attention patterns are diagnostic, not causal proof. Typed schema and explicit benchmark construction can favor the proposed solution. Repeated updates with ambiguous, missing lineage remain a different test.
- **MemTX**: [Deep read](deep_reads/2607.23929.md). S3 states, gates and cascades; S4 cases; S5 results/formal checks; Appendices B and H implementation/horizon. Conflict detection uses structured assumptions; the action-safe existential gate is not action-specific proof. Complete recorded provenance is crucial. MemTX does not lead task success on GPT-5.5 in the main table (0.756 versus 0.778 for Cordon + revocation), so superiority is not uniform.
- **PlanFence**: [Deep read](deep_reads/2609.03340.md). S4 contract; S5 live/replay evaluation; S6 exclusions; Appendix C Figure 6 missing-edge sensitivity. The key novelty boundary is incomplete semantic lineage. Checking a perfect declared graph is already solved within this protocol. Extra edges can preserve safety by increasing checks, while missed edges undermine it.
- **Dependency-guided Rollback**: [Deep read](deep_reads/2608.10502.md). S3 assumptions/algorithm; S4 selection; S5 main/adapted results; Appendix F other backbones. Cases are selected where injection causes an error and downstream effects, so rates are conditional. Single temperature-zero runs do not remove stochastic or model-version uncertainty. Strong baseline for G1, not a novelty-free implementation template.
- **StateAuditor**: [Deep read](deep_reads/2608.01619.md). S3–S4 audit/gate; S5 scope controls; S6 external and semantic-gate tests; S7 limitations. An 80%-token quotation match and newer date verify provenance/order, not semantic supersession. The gate accepts semantically non-superseding transitions in a control, so calibrated semantic repair remains unresolved.
- **Execution-state Unlearning**: [Deep read](deep_reads/2609.04875.md). Method theorem and algorithm in Sx3; experiments Sx4; limitations Sx5. A non-significant difference from reset is not an equivalence proof. Selective branch repair needs trustworthy attribution; otherwise conservative suffix replay is necessary in the stated model.
- **OAS**: [Deep read](deep_reads/2607.17545.md). Sx3 formulation; Sx4 grouped experimental design; Appendix B.6 non-oracle results. Calibration is empirical and distribution-dependent, not a population safety certificate. Query-known compression does not test whether discarded evidence would be needed for an unknown later correction.
- **TRUSTMEM**: [Deep read](deep_reads/2606.25161.md). S3 verifier/reward; S4 data/results and ablations; limitations/conclusion. Verifier ranking is relative rather than a calibrated probability of edit correctness. Small hallucination rates judged by another LLM are not proof of zero false generalizations.
- **BeliefMem**: [Deep read](deep_reads/2605.05583.md). S3 candidate update; S4 tasks/ablations; Appendix A.1 confidence interpretation. Noisy-or-style combination risks overcounting dependent evidence. Top-1 convergence is not Brier score or calibration under shift. CAMA/GovMem directly challenge independence assumptions.
- **StateMem**: [Deep read](deep_reads/2608.19652.md). S3 error decomposition; S4 benchmark; S5 state model; S6 results/controls; Appendix H costs. Many turns do not imply a million-token horizon. Full transcript plus retrieved state can be an advantage unless context is matched. Explicit linguistic dependencies simplify the unknown-lineage problem.
- **VerMem**: [Deep read](deep_reads/2608.03137.md). S3 tools/verifiers; S4 episode-reset setup/results; S5 scope; Appendix A memory schema. Verifiers used in training are removed at inference; reward shaping does not create a runtime semantic safety contract. Episode resets sharply constrain claims about lifelong accumulation.
- **TierMem**: S2 immutable archive and provenance; S4 fixed answerer, online writeback disabled; S5 escalation/quality-cost; replay of same questions is not unseen lifelong learning.
- **CAMA**: Methodology evidence slots, soft dependency inference and Expand/Trace/Stop RL; experiments correlation-augmented MAB/LME/LoCoMo; Appendices A–C complexity and recovery.
- **GovMem**: S3 dependency-aware support and review; S4 controlled data; S5 internal held-out evidence; S6 external human rejection of every proposed automatic promotion in selected stress slice; S7 limitations.
- **ChronoMem**: S3 whole-memory snapshots and HEAD restore; S4 post-exposure protocol; S5 semantic version selection and QA; MAB downstream QA restricted to Accurate Retrieval.
- **RD-Forget**: S3 retained source H and query-conditioned budgeted view; S4.1 source-order subsets and same-family judge; S4.2 intent uses task metadata; S5–S6 component and historical-query tests.
- **MemCon**: S3 memory-control state/actions; S4 component ablations; Appendix A shared-interface reimplementations and single deployment runs; C discretization; D stationary bandit assumptions.
- **Self-RAG**: Evidence critique is not durable-memory version management. Screened at abstract level; positive flags only reflect explicit described actions, not independently validated performance.
- **Corrective RAG**: External retrieval routing is already prior art. Screened at abstract level; positive flags only reflect explicit described actions, not independently validated performance.
- **Adaptive-RAG**: Relevance/complexity routing is not evidence-freshness calibration. Screened at abstract level; positive flags only reflect explicit described actions, not independently validated performance.
- **SkillZip Pro**: S3 persistent versus transient storage accounting; S4.4 deletion witnesses; S4.5 faithfulness assumptions; S4.6 affected closure and repacking.
