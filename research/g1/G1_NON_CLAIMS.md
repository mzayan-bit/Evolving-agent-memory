# Explicit non-claims

| Must not claim | Prior evidence that defeats the broad claim |
|---|---|
| First long-term agent memory | [Existing retained literature](../literature/master_paper_matrix.csv), including [Generative Agents](https://arxiv.org/abs/2304.03442) |
| First temporal memory or supersession | [StateMem/CUPMem audit](competitors/statemem_cupmem.md), methods and lifecycle storage |
| First dependency graph / provenance | [Classical provenance/TMS](CLASSICAL_PRIOR_ART.md); [Rollback](competitors/rollback_repair.md), runtime provenance |
| First dependency-aware repair or rollback | [Rollback](competitors/rollback_repair.md); [MemTX](https://arxiv.org/abs/2607.23929v2) |
| First hidden dependency inference | [StateAuditor](competitors/stateauditor.md), inferred premises; [CUPMem](competitors/statemem_cupmem.md), latent invalidation; [CAMA](competitors/cama.md), source slots |
| First memory uncertainty or UNKNOWN state | [CUPMem](competitors/statemem_cupmem.md), confidence/weak/unknown; [CAMA](competitors/cama.md), posterior scores |
| First stale-memory metric or lifecycle benchmark | [STALE/StateMemBench](competitors/statemem_cupmem.md), SR/PR/IPA and evolving state; [Rollback](competitors/rollback_repair.md), recurrence and benign preservation |
| First alternative evidence reasoning | [ATMS/provenance](CLASSICAL_PRIOR_ART.md); [Rollback support rescue](competitors/rollback_repair.md); [CAMA independent evidence](competitors/cama.md) |
| First AND/OR representation, hypergraph or support set | [ATMS, provenance semirings, factor graphs](CLASSICAL_PRIOR_ART.md) |
| First incomplete/spurious dependency evaluation | [PlanFence Appendix C](competitors/planfence.md) |
| First correlated-source handling | [CAMA](competitors/cama.md); [GovMem](https://arxiv.org/abs/2607.02579v1) |
| First matched-cost stale-premise repair | [StateAuditor matched controls](competitors/stateauditor.md) |
| First repeated revision or ambiguity cases | [StateAuditor hard confirmation](competitors/stateauditor.md), cyclic and ambiguous cases; [StateMem](competitors/statemem_cupmem.md), evolving state |
| Calibrated repair, now or by default | No calibration measurements in G1; classifier recall, LLM confidence and judge agreement are not posterior calibration. [Calibration definition](VARIABLES_AND_METRICS.md) |
| Novel method, SOTA, reliable human gold, publication readiness | No method implemented, no model evaluation, no human labels. The 30 cases are AI-authored annotation drafts. |

A conjunction of previously studied properties is not automatically a contribution. The missing experiment must expose a consequential assumption or a reproducible failure boundary, and beat an honest simple-baseline explanation.
