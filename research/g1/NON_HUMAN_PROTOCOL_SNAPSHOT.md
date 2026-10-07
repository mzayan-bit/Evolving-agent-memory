# Non-human protocol snapshot

**ENGINEERING VALIDATION ONLY. No scientific pilot, evaluation claim or proposed uncertainty-aware G1 method.** This snapshot follows verified remote main 859d4dd. Implementation commits: 1633c2e (arm accounting and temporal binding) and 8459db1 (common checkpoint query scheduling and threshold configuration). Exact tracked artifact hashes are in integration/provenance.json. Historical engineering receipts remain intact.

## Contracts ready to freeze before annotations

- **Research question:** characterize support-inference versus repair-decision errors under revisions with equal evidence/resources, and determine whether strong classical/recompute/query-only baselines leave material residual headroom. No claim that uncertainty or an unimplemented method wins.
- **Non-claims:** tiny fixtures establish engineering behavior only; no accuracy estimate, significance, prevalence, scientific cost advantage, literature novelty or general model competence claim. B7/B8/B9/B10 are named internal adaptations, not paper reproductions.
- **Support ontology:** scoped/time-indexed justifications; AND within a support group, OR across groups, copied/correlated evidence not independent; necessary/conjunctive/alternative/partial/copied/correlated/temporal/scope/policy/association/contradiction/unknown retain existing meaning. Partial/association/contradiction/unknown cannot be sufficient. Positive grounding cannot create support from an ungrounded cycle.
- **Comparators:** B4b embedding closure; separately elicited B5a point links and B5b point sets; paid-construction B7 positive maintenance; explicit-provenance B8 regeneration/cache; paid-construction B9 support-aware rollback; B10 paid query-only audit. End-to-end and shared-proposal policy isolation remain distinct. No baseline added or removed to improve results.
- **Information:** same immutable sources, provenance, authority flags and declared task opportunity. Ordinary arms reject oracle flags. Runtime receives no Gold, expected answers, future checkpoint records, hidden rules or adjudication labels. The existing importer/reviewer boundary remains necessary; tests are not a sandbox against a malicious adapter or forged timestamps.
- **Model/runtime:** pinned Qwen3.5-9B source, Bartowski Q4_K_M and llama.cpp b9222 exactly as qwen_local/deployment.json. CPU+Accelerate on M4 16 GB; source/conversion provenance caveat retained. Pinned normalized MiniLM CPU backend unchanged. No model substitution or new dependency installation.
- **Prompt/schema procedures:** B5 v2 prompts and ontology unchanged. Literal IDs and strict schemas, immutable request identity, no semantic tuning. Existing current readout/audit prompts are applied only after temporal evidence binding; versions/hashes recorded. No few-shot examples or gold repair added.
- **Retry/failure:** one charged B5 protocol retry; no semantic retry. Transport/refusal/truncation and exhausted budgets remain explicit; malformed output is not a semantic error. A future/oracle contaminated prefix returns protocol_violation without generation, and cannot be scored correct. Failed/unknown usage is retained rather than converted to zero.
- **Resources:** the same serial Ledger contract for all seven arms, including support construction, embeddings, retries, audit/readout, regeneration and local dependency work. Staged credit release with carry and actual token reconciliation works. Common probes run at their declared revision, before later credits are released; replaying an earlier dispatch clock is rejected. Final numeric budgets remain unselected.
- **Shared compute:** identical artifacts only under identical conditions. Common raw inputs are supplied equally; shared model-built proposals have original costs allocated to every applicable recipient before use, with original physical work separately recorded. No free inferred graph or unrecorded upstream model construction. See SHARED_COMPUTE_POLICY.md.
- **Caching:** cold per-arm namespaces, exact material identity, counted hits/misses and local checks; B8 dependency reuse includes validity/config/version/scope/time when material; model readout and B10 reuse disabled. Scope exceptions are explicit, not order-dependent warming.
- **Result format:** raw responses/usage and attempt IDs, immutable hashes, physical and allocated costs, released credits, cache events, semantic/protocol outcomes and separate phase/runtime latency. Energy/local USD unavailable unless measured. No summed nested time masquerades as elapsed time.
- **Statistics/oracles:** independent source/scenario family; arm/backbone/revision/mask/seed/query repeats are nested measures. Existing macro outcomes/denominators, cluster inference and expansion/kill procedures remain prospective. Explicit oracle ladder is separate, never ordinary-arm input or ranking.

## Temporal/readout rules

TemporalModelReadout selects a saved immutable PolicyView, not a reconstruction from current status. `current` selects the dispatch checkpoint; `historical_then` selects `as_of` and excludes later factual changes/corrections; `historical_now` selects that same past frame but applies corrections known by dispatch time. Mere supersession does not rewrite the past. Present permission revocations constrain both historical modes outside the model prompt. As in the existing Trace semantics, a correction can invalidate an old justification and lead to abstention; it does not fabricate a replacement historical claim.

Filtering/grounding uses observed prefix supports, never Trace.rules or future inferred supports. Permission filtering is an access check, not permission to disclose later facts to the model. Future records/support versions, unavailable frames, duplicate archive checkpoints and oracle views are explicit protocol failures. All generations spend current dispatch credits even when their evidence time is earlier. The schema/reader never receives expected answers. `assess_readout` remains evaluator-only and separately exposes persistent-memory correctness, required-evidence coverage and answer correctness; a corrected answer cannot rewrite the memory score.

Scope remains the existing positive support and explicit acyclic derivation model. Unknown provenance, arbitrary agent/tool replay and inconsistent contexts are not silently promoted into supported capabilities. Those broader paper reproductions were already excluded; this snapshot does not change the research question.

## Tiny actual Qwen historical validation

Four real generations, **2,053 input / 134 output tokens**, zero cache hits, two verification calls and two ordinary readouts. Physical request latency **56.595 seconds**; ledger latency **56.611 seconds**, including small local work/runtime. All four rendered-prompt/output token-ID checks matched. No new peak-memory or energy measurement is claimed.

| Query at checkpoint 2 | Visible evidence time | Actual answer | Persistent-state assessment | Answer assessment |
|---|---:|---|---|---|
| Current B10 audit | 2 | Project Zorvia uses protocol K29. | Wrong/stale K17 | Correct |
| As-known-at-1 B10 audit | 1 | Project Zorvia uses protocol K17. | Correct for past | Correct |
| Unaffected historical ordinary readout | 1 | Project Tovren uses protocol M83. | Correct for past | Correct |
| Retrospective ordinary readout, supersession | 1 | Project Zorvia uses protocol K17. | Correct for past | Correct |

All three historical wire payloads exclude K29 and source s2. Storage hash is unchanged. A fifth requested call was blocked before dispatch at the four-call cap. Retrospective correction and present-permission cases use focused offline tests of the same binding function; no additional live cases or support sweep was needed.

The actual smoke recorded HEAD 1633c2e and `dirty: true`; that original provenance is preserved, not rewritten as a clean-checkout run. The later common-query scheduling/current-clock guard and threshold parameter plumbing were validated offline at 8459db1; the real smoke's four probes all used the correct current dispatch clock and unchanged default thresholds. No model settings, B5 prompts, fixture gold or recorded responses changed. See integration/qwen-temporal-manifest.json, qwen-temporal-traces.json and checks.json. Seven-arm and shared-allocation receipts are explicitly offline scripted accounting checks, not real Claude/Qwen comparisons.

## R1 against the unchanged pre-existing criteria

| Gate | Status | Direct evidence |
|---|---|---|
| G1 | PASS | Prior real Qwen B5a/B5b and MiniLM execution; new real temporal/readout evidence. Semantic errors remain visible, no quality ranking |
| G2 | PASS | Preserved actual usage and token-ID checks, unknown propagation and prior independent tokenizer audit |
| G3 | PASS | Shared arm ledger, tested credit release/carry/reservation reconciliation; prior live one-call stop and new four-call/fifth-no-dispatch stop; offline unknown/overrun/failure retention |
| G4 | PASS | Cold arm namespaces, equal allocated construction, material cache identity/invalidation, prior real full/incremental equivalence, new integrated B8 text commit/unaffected reuse and counted local work |
| G5 | PASS | All adaptations, shared-projection exception and explicit replay/provenance limits named; no reproduction claim |
| G6 | PASS | Seven arms through common source/access/Ledger/query schedule; B7/B9 pay construction; model-backed current and both historical modes available; B10 does not mutate storage |
| G7 | PASS | Allowlist, future-prefix/oracle rejection, permission/correction tests and inspected historical wire payloads without later source facts; no evaluator feedback |
| G8 | PASS | Committed code/config, pinned runtime, request/response/usage hashes, actual four-call trace, cache/attempt/blocked-dispatch records |
| G9 | PASS | No human A/B edits, pilot, G1 implementation, fixture-gold changes or scientific statistics |

**Overall remains R0 under the full already-written freeze requirement.** The objective engineering gates G1–G9 now have acceptance evidence. However, the pre-existing final R1 assessment additionally requires review/freeze of development prompts/thresholds. The threshold values/selection approval and final study settings are not complete. Calling this R1 by dropping that written requirement would move the goalposts. The criteria file remains byte-for-byte identical to 859d4dd.

No remaining infrastructure defect has been identified that must be addressed before annotations. Outstanding choices require development data, adjudication and study-owner approval. Claude execution remains an external operational blocker for the proposed two-backbone evaluation; the R1 table does not impose a separate billed-API gate, and this snapshot does not waive the existing two-backbone plan. Human adjudication remains the separate R2 requirement, not a newly invented R1 gate.

## UNRESOLVED — REQUIRES HUMAN/DEVELOPMENT DATA

B4b cosine threshold; B5a/B5b logical commit thresholds and approved objective/grid/guardrails; common shared-construction threshold; stress-mask strengths; feasible context/token/credit/retrieval limits and query horizon; practical margins, ambiguity/eligibility decisions and final study signatures. Existing .7 values, .7/.3 stress and 5 pp/2 pp margins remain provisional. Exact procedures/approval points are listed in DEVELOPMENT_DATA_REQUIREMENTS.md. No final evaluation outcomes may choose them.

Independent human A/B work, agreement and adjudication have not been completed by this engineering phase. Strong-baseline evaluation and residual-headroom analysis remain future, gated work. Neither engineering success nor preserved model errors authorizes a new G1 controller.

## Checks

`uv run pytest`: **176 passed**. `uv run ruff check .`: clean. `uv run mypy src tests`: clean, 43 source files. No broad new fixture sweep. Existing tests now distinguish deterministic dependency-inspection events from forbidden confidence-triggered model/verification/replay work. All other prior offline behavior remains covered.

# STOP GENERAL ENGINEERING

**No additional infrastructure engineering is justified before the independent human annotations are completed.** The three authorized gaps are addressed for the existing declared scope. Stop architecture expansion, optional cache optimization, new baselines and fixture-driven semantic tuning. The next project action is **independent human annotation**, followed by agreement review/adjudication, development-only selection and a signed study freeze. External model access can be arranged as an operational prerequisite before the planned two-backbone evaluation; it does not justify more repository engineering now.

**Do not implement the proposed uncertainty-aware G1 method.** First require human annotation, adjudication, strong-baseline evaluation and residual-headroom analysis that justifies it.
