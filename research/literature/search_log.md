# Search method and adversarial audit

**Review cutoff/search date:**19 September 2026. **Question:** what narrow, testable agent-memory contribution remains plausible after searching for counterexamples?

## Search progression

1. Survey-first map: memory mechanisms; forms/functions/dynamics; storage-to-experience; lifecycle security; graph-personalized memory. Surveys supplied terminology and primary-paper leads, not proof of novelty.
2. Subarea expansion: write/formation, episodic/semantic/procedural representation, retrieval, update/supersession, temporal validity, forgetting, consolidation, dependencies, provenance/uncertainty, learned policies, RAG routing, benchmarks, poisoning and efficiency.
3. Primary-source inspection: author/title/date/version metadata from arXiv; official ACL/other publication links when located; method/evaluation/limitations/appendix reading for25 priority papers and targeted inspection of close competitors. No experimental reproduction was performed.
4. Adversarial pass: search each candidate using synonyms, then retain papers that *weaken* the candidate. The final exact recoverable query list and primary result links are in [adversarial_queries.json](adversarial_queries.json). Earlier search families below are a narrative audit, not a fabricated complete query-by-query machine log.
5. Deduplicate arXiv/conference/workshop identities; pin latest inspected pre-cutoff revision; distinguish first-public year from venue year. Record exclusions and same-name collisions in [version_ledger.md](version_ledger.md).

## Sources and evidence hierarchy

Primary arXiv abstracts/HTML supplied the main corpus. Official ACL Anthology pages independently establish selected venues; OpenReview/workshop leads were used when surfaced. Official paper-linked code/project URLs are recorded without asserting that the current default branch matches the paper. Search snippets, aggregators, blogs and GitHub discovery lists are leads only; none establishes a finalist gap by itself. Abstract-only rows are explicitly marked, and unverified capability, compute and result fields are NR rather than guessed.

Strong survey maps: [Memory Mechanism Survey](https://arxiv.org/abs/2404.13501), [Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564), [Storage to Experience](https://arxiv.org/abs/2605.06716), [Memory Security Survey](https://arxiv.org/abs/2604.16548), [Graph-Based Personalized Memory](https://arxiv.org/abs/2609.08599). [Memory Mechanisms/Evaluation/Evolution](https://arxiv.org/abs/2509.18868) and [Rate-Distortion Compaction](https://arxiv.org/abs/2607.08032) added adjacent framing. Their coverage dates and evidential strength differ.

## Candidate-killing searches and consequences

| Proposed gap | Adversarial query themes | Primary counterexamples found | Decision |
|---|---|---|---|
| Temporal/historical memory | temporal supersession; versioned memory; bitemporal agent memory; historical state | Zep, TOKI, MemStrata, Kumiho, RD-Forget | Reject broad novelty |
| Explicit lifecycle management | lifecycle states; transactional memory; revocation; soft deletion | MemTX, CUPMem, VerMem | Reject new-state-name novelty |
| Dependency propagation | dependency-aware revision; stale plans; rollback repair; implicit stale dependencies | StateMem, CUPMem, PlanFence, rollback repair, StateAuditor | Narrow to incomplete/inferred lineage and measured false invalidation |
| Uncertainty from provenance | correlated traces; source independence; latent evidence memory; promotion | GovMem, CAMA, AuthMem, provenance laundering | Reject standalone correlation-aware confidence direction |
| Consolidation fidelity | memory hallucination; false generalization; operation selection; qualifier loss | HaluMem, TRUSTMEM, OAS, MemOps, MemFail | Reject first fidelity-evaluation claim |
| Bounded reversible memory | reversible compression; memory provenance compression retraction; historical forgetting budget | R3Mem, ChronoMem, RD-Forget, rate-distortion analysis, both SkillZip works, SkillZip Pro | Narrow to total factual-state budget and unknown future corrections |
| Failure attribution | causal failure attribution; oracle interventions; factorial fault injection; counterfactual attribution | CAR, CausalFlow, MemAudit, Misattribution Gap, AgingBench, MemOps/MemFail | Remove generic causal diagnosis finalist |
| Freshness-aware routing | external refresh policy; silent drift; freshness revalidation learned policy | CRAG/Adaptive-RAG, MCB, MemCon, PlanFence, Memory Trust Gap, classical refresh work | G3 survives only as low-confidence longitudinal/missing-notification hypothesis |

## Coverage and stopping rule

104 bibliographically identified source records were inspected at least at metadata level. Four were excluded/grouped, leaving100 unique retained works: 7 first public in2023,10 in2024,18 in2025 and65 in2026. These counts exclude unverified search snippets and the older adjacent refresh lead.25 papers received dedicated deep-read notes. The other rows retain their explicit evidence-depth labels; do not describe all100 as deeply reviewed.

Search stopped after each finalist had named direct competitors, explicit scope differences, a falsifiable pilot and a kill criterion. This is a research decision audit, **not an exhaustive systematic-review/PRISMA claim**. A new or missed preprint may invalidate a direction. G3 particularly needs an adjacent database/cache-control review before investment.

## Limitations of this review

- English and web-indexed/arXiv-accessible work dominates; coverage of closed publisher text and unindexed workshop papers is incomplete.
- Primary-source methods are not independently reproduced; many2026 results are preprints with limited external validation.
- Latest arXiv revision was read where available; a linked conference version may have formatting or substantive changes not fully reconciled. The ledger discloses this rather than claiming an exhaustive version diff.
- Public code links are verified as paper-associated when possible; repository licenses, dependency usability and exact reproduction commits were not audited.
- Absence of a result in inspected sections is not evidence that a capability is impossible or absent from all code.
- API model aliases, judge choices, cost boundaries, oracle access and benchmark variants can invalidate cross-paper rankings.
