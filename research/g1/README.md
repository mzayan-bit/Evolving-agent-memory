# G1 scientific validation package

**Decision B — survives conditionally as a research question. No method novelty or performance is established; do not implement an uncertainty controller yet.** Cutoff 2026-09-20; inspected 2026-09-21.

Start with [claim](G1_CLAIM.md), [closest-work audit](CLOSEST_WORK_AUDIT.md), [classical prior art](CLASSICAL_PRIOR_ART.md), and [kill criteria](KILL_CRITERIA.md). The audit materially narrows the earlier explicit-lineage premise: CUPMem already performs inferred persistent invalidation; Rollback already preserves independent support; PlanFence already tests omitted/excess dependencies; StateAuditor already has matched controls and hard lifecycle null results; CAMA already models latent source correlation.

## Artifact index

- Claim boundaries: [G1_CLAIM](G1_CLAIM.md), [G1_NON_CLAIMS](G1_NON_CLAIMS.md).
- Evidence: [CLOSEST_WORK_AUDIT](CLOSEST_WORK_AUDIT.md), [CLASSICAL_PRIOR_ART](CLASSICAL_PRIOR_ART.md), [REPRODUCIBILITY](REPRODUCIBILITY.md), [source manifest](source_manifest.json); [Rollback](competitors/rollback_repair.md), [StateAuditor](competitors/stateauditor.md), [PlanFence](competitors/planfence.md), [StateMem/CUPMem](competitors/statemem_cupmem.md), [CAMA](competitors/cama.md).
- Representation: [SUPPORT_ONTOLOGY](SUPPORT_ONTOLOGY.md).
- Cases: [annotation README](annotations/README.md), [guide](annotations/ANNOTATION_GUIDE.md), [CSV](annotations/ANNOTATION_30.csv), [30 JSON scenarios](annotations/scenarios/), [adaptation manifest](annotations/adaptation_manifest.json), [STALE license](annotations/STALE_LICENSE.txt).
- Controls: [BASELINE_EXPECTATIONS](BASELINE_EXPECTATIONS.md), [VARIABLES_AND_METRICS](VARIABLES_AND_METRICS.md), [COST_ACCOUNTING_PROTOCOL](COST_ACCOUNTING_PROTOCOL.md), [INFORMATION_ACCESS](INFORMATION_ACCESS.md).
- Prospective study: [KILL_CRITERIA](KILL_CRITERIA.md), [PREREGISTRATION_DRAFT](PREREGISTRATION_DRAFT.md), [PILOT_DESIGN](PILOT_DESIGN.md), [STATISTICAL_PLAN](STATISTICAL_PLAN.md).
- Critique/positioning: [HOSTILE_REVIEW](HOSTILE_REVIEW.md), [VENUE_FIT](VENUE_FIT.md).
- Actual smoke output: [MemTX](memtx-smoke.txt), [CUPMem](cupmem-smoke.txt). These are mechanics tests, not paper reproductions.

## Five decisions

Q1: We could characterize when uncertainty about semantic support changes the stale-reuse versus valid-retention frontier of persistent agent-memory repair under matched evidence and compute across repeated revisions.

Q2: Dependency-Guided Rollback Repair is the closest single persistent repair paper; CUPMem and StateAuditor narrow its difference, and CAMA plus classical TMS is the strongest composition threat.

Q3: Freeze evidence/inference, corrupt visible support, distinguish independent alternatives from copies, run three revisions with delayed reuse and historical probes, and compare existing rollback, support-set truth maintenance and conservative verification at identical resource caps.

Q4: Abandon a new method if a simple support-set/replay/reverify baseline covers the frontier within practical margins; abandon the direction if ontology or practical uncertainty signal fails. A small inconclusive pilot is not a null result.

Q5: No proposed-method implementation now. Human annotation and a cost-capped baseline-only pilot are the next gates. Planned initial pilot is 384 trajectories; none ran in this phase.

[Validation record and complete file inventory](VALIDATION.md) documents checks and remaining limitations.

## Baseline fidelity phase (2026-09-25)

Start with [baseline fidelity audit](BASELINE_FIDELITY_AUDIT.md), [missing-baseline decisions](MISSING_BASELINE_AUDIT.md), and [official artifact/component reproduction ledger](COMPETITOR_REPRODUCTION.md). The [candidate protocol](PILOT_PROTOCOL_CANDIDATE.md) is **not frozen**. It links the oracle, noise, model, hyperparameter and sample-size plans. [Planned outputs](PLANNED_TABLES_AND_FIGURES.md), [negative-result commitments](NEGATIVE_RESULT_PLAN.md), [error decomposition](ERROR_DECOMPOSITION.md) and [release checklist](REPRODUCIBILITY_CHECKLIST.md) precede any pilot outcomes. Round 2 of HOSTILE_REVIEW records remaining R0 model-backed study gates.
