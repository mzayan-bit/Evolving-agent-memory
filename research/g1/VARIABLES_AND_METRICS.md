# Variables and metrics: draft operational definitions

## Independent variables

Manipulate observed lineage separately from source text and evaluator gold. Use edge **member incidences** `(source, justification, target)` so deleting one member of an AND set differs from deleting an OR alternative. Initially test completeness 100% versus 70% and spurious incidence 0 versus .30 per true incidence; these are stress contrasts, not claims about real deployment. Reserve 90%/50% and other rates for a later sensitivity study. Report achieved rather than rounded target rates on tiny graphs; sample exactly with published masks. Stratify corruption by necessary/alternative/conjunctive/shared-origin relations. Include matched random omissions and plausible semantic omissions only as separately labeled regimes.

Spurious rate = inserted false member incidences / true gold incidences before corruption. Also report precision of visible lineage, because that denominator differs. Unknown relationships are not counted as gold true/false corruption opportunities. Explicitly scope false links to bystander, wrong-time, wrong-entity and copied-as-independent types. Correlation is a separate source-origin manipulation, not just an extra edge.

Revision depth: primary three revisions; one-revision prefix provides an internal comparison, ten-revision expansion only after gates. Domain/template/entity shift: held-out combinations, with all paraphrases/copies of a base scenario in one split. Known-source cue versus unknown fault discovery are distinct tracks. Authority: trusted explicit record, lower-authority report or unknown; source availability: requeryable, delayed or unavailable. Budget includes verifier/replay calls and tokens, not only repair actions. Avoid a combinatorial full factorial before pilot variance/cost are known.

## Measurement sets and attribution

Let s be a scenario, t a revision, i a stored derived proposition, and q a predeclared subsequent probe. Gold is human-adjudicated and time/scope specific. Define `A_st` as formerly usable derived items whose current reuse must stop/change after t; exclude changed base sources themselves and initially ungrounded claims. `V_st` are still-valid derived items and unaffected bystanders. `I_st ⊆ V_st` have at least one valid independent sufficient alternative after a source fails. `U_st` are genuinely unresolved items. Keep these disjoint for the primary metrics.

A probe has fixed item-level opportunities determined by the scenario, regardless of what the policy retrieves. Reliance means the answer, proposed action or new memory uses the stale proposition as a premise; retrieval alone is a separate exposure measure. Require structured used-item IDs and verify against text/actions, with blinded human adjudication for unmarked implicit reliance. A policy cannot improve its denominator by deleting everything or avoiding retrieval.

## Primary outcome and guardrails

**Trajectory-macro stale descendant reuse rate (SDRR)** under a fixed repair resource cap:

`SDRR_s = Σ_(t,i∈A_st,q∈Q_sti) 1[stale i relied upon at q] / Σ_(t,i∈A_st) |Q_sti|`.

Report the macro mean across eligible scenarios, with denominator/eligible-scenario count. `Q_sti` is fixed before any run. If a scenario has no affected descendants, its SDRR is NA, not zero; it contributes to valid-state preservation and accuracy. Report conditional results separately for natural ambiguity and initially bad memories. False invalidation and task accuracy are mandatory guardrails, not optional favorable secondary metrics.

**False invalidation rate:** `FIR_s = Σ_(t,i∈V_st) 1[valid content wrongly deleted/deactivated/blocked as invalid] / Σ_t |V_st|`. Also report valid-item quarantine burden separately and a combined nonavailability rate, so a policy cannot hide over-invalidation by renaming it quarantine. A provenance-only edit preserving use is not false invalidation.

**Independent-support retention:** `ISR_s = Σ_(t,i∈I_st) 1[valid claim remains usable] / Σ_t |I_st|`. Publish number of opportunities and reason for any loss. Unknown origin is outside this denominator and inside the uncertainty stratum.

## Secondary outcomes

| Measure | Definition / denominator |
|---|---|
| Repair recall | Correctly repaired/deactivated items in `A_st` / all items in `A_st`, aggregated by trajectory. Wrong replacement is not successful repair. |
| Repair precision | Items actually requiring the chosen content-changing repair among all such repairs. Provenance-only valid edits are separately tagged, not treated as false repairs. Zero actions: precision NA; recall remains defined when affected items exist. |
| Recurrence | Among stale propositions verified absent/unusable immediately after repair, fraction that later reappear as current in a write/answer/action before legitimate reinstatement. Report count of repaired propositions eligible for later probes. Never count legitimate A→B→A reversion as recurrence. |
| Current-state accuracy | Correct current structured answers / fixed current probes, with abstention incorrect when gold is determined and correct when gold requires uncertainty. Include no-answer/failed runs. |
| Historical-state accuracy | Correct time-indexed answers / fixed historical probes; require distinction between formerly true and formerly believed. Present disclosure rules still apply. |
| Action correctness | Correct admissible action or required stop / fixed action opportunities. Never execute real external actions in this study. |
| Abstention coverage | Abstained probes / all fixed probes, stratified by gold known/unknown. Pair with error among answered probes; report zero-answer case as undefined risk, not perfect performance. |
| Reverification coverage | Unique item-revision pairs reverified / eligible item-revision pairs. Repeated checks also count separately as cost. |
| Quarantine burden | Valid/unresolved/invalid item-revision pairs quarantined, separately by gold state and duration until next opportunity. |
| Exposure | Stale retrievals / fixed retrieval opportunities; not interchangeable with reliance. |

Rollback already measures benign preservation, invalidation precision/recall and recurrence; STALE supplies SR/PR/IPA; StateAuditor measures false repair/current-value accuracy. [Audit](CLOSEST_WORK_AUDIT.md). SDRR is an operational persistent-reuse definition, not a claim to invent stale-state measurement.

## Calibration: define the event first

If a future model outputs probability `p_i`, freeze its event, e.g. “item i has no currently valid permissible sufficient support among available evidence.” Do not mix edge existence, source reliability, supersession and invalidation probabilities. Genuine unknown gold has no forced binary target and is reported separately or with adjudicated bounds. Calibrate only on a disjoint calibration split; never calibrate on test labels or future revisions.

For determinate binary events, Brier = `mean((p-y)^2)`. Reliability diagram bins and ECE binning must be frozen (e.g. 10 equal-width bins, with counts and uncertainty); ECE = `Σ_b n_b/n * |mean(p_b)-mean(y_b)|`. Report Brier and plots because ECE is bin-sensitive. Small pilot bins are descriptive only. Risk–coverage plots rank uncertainty and show error on answered/retained items as coverage changes, with scenario-clustered intervals and coverage floor. A safety benefit from abstention is meaningful only alongside task completion/preservation.

[Guo et al. (2017), On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a.html) supplies a standard calibration reference; [Geifman and El-Yaniv (2017), Selective Classification for Deep Neural Networks](https://arxiv.org/abs/1705.08500) motivates risk–coverage. Neither LLM self-confidence nor a judge’s agreement is automatically a calibrated probability.
