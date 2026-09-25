# Baseline fidelity audit — 2026-09-25

Audited main `ae5949d` and the narrowly scoped fixes in this phase. **No B0–B7 implementation is a paper reproduction.** The runtime is ready for deterministic testing, not yet a faithful natural-language competitor comparison. See [reproduction evidence](COMPETITOR_REPRODUCTION.md).

## B0 — No repair

**Baseline ID:** B0

**Name:** No repair

**Scientific purpose:** Lower-bound persistence control

**Reference:** Internal control

**Implemented algorithm:** Accept common source ingestion; no derived mutations

**Information available:** Immutable current records, visible changed-source cue, projected past snapshots, observed lineage, explicit fixture domain rules, provenance/authority according to shared access flags. Rules are common executable evidence, not inferred natural-language truth.

**Hidden information unavailable:** Gold affected/valid masks, expected answers, future versions and corruption masks. Gold lineage/fault identity only in explicitly separate oracle runs.

**Budget behavior:** Zero maintenance model/verifier/replay operations; real local runtime recorded

**Persistent-state behavior:** Status changes commit to a new immutable snapshot; source ingestion is common to all arms. Fixed propositions only: no generated replacement text.

**Current/historical handling:** Current reads use persistent status; as-known-then uses archived snapshots; retrospective views apply observed corrections. Present permission applies to both historical views after the audit fix.

**Alternative-support behavior:** Does not evaluate alternatives

**Repeated-revision behavior:** Old derived state survives every revision

**Expected strength:** Cheap; may suffice if common reader finds fresh evidence

**Known simplifications:** Fixed identity reader cannot spontaneously repair an answer

**Difference from closest published method:** No paper method claimed

**Does the implementation unfairly weaken it?:** No for its control role; yes if presented as a realistic strong reader

**Fidelity level:** intentionally simple control

**Evidence:** [implementation](../../src/evomem/policies.py), [scientific tests](../../tests/test_harness.py), [prior-art audit](CLASSICAL_PRIOR_ART.md), and the method-specific primary reference below.

## B1 — Source only

**Baseline ID:** B1

**Name:** Source only

**Scientific purpose:** Isolate descendant propagation

**Reference:** Internal control

**Implemented algorithm:** Log direct old-source invalidation; leave descendants unchanged

**Information available:** Immutable current records, visible changed-source cue, projected past snapshots, observed lineage, explicit fixture domain rules, provenance/authority according to shared access flags. Rules are common executable evidence, not inferred natural-language truth.

**Hidden information unavailable:** Gold affected/valid masks, expected answers, future versions and corruption masks. Gold lineage/fault identity only in explicitly separate oracle runs.

**Budget behavior:** Same as B0

**Persistent-state behavior:** Status changes commit to a new immutable snapshot; source ingestion is common to all arms. Fixed propositions only: no generated replacement text.

**Current/historical handling:** Current reads use persistent status; as-known-then uses archived snapshots; retrospective views apply observed corrections. Present permission applies to both historical views after the audit fix.

**Alternative-support behavior:** No downstream rescue or invalidation

**Repeated-revision behavior:** Only source versions advance

**Expected strength:** Cheap local correction

**Known simplifications:** B0 already supersedes sources during common ingestion, making derived outcomes identical

**Difference from closest published method:** Not a distinct state-reconstruction competitor

**Does the implementation unfairly weaken it?:** Redundant outcomes in current fixtures; retain as ingestion/action-log control, never count as independent confirmation

**Fidelity level:** intentionally simple control

**Evidence:** [implementation](../../src/evomem/policies.py), [scientific tests](../../tests/test_harness.py), [prior-art audit](CLASSICAL_PRIOR_ART.md), and the method-specific primary reference below.

## B2 — Full recompute with archive

**Baseline ID:** B2

**Name:** Full recompute with archive

**Scientific purpose:** Strong correctness and cost threat

**Reference:** [Acar, Self-Adjusting Computation](https://www.cs.cmu.edu/~rwh/students/acar.pdf); full recomputation is an internal control

**Implemented algorithm:** Ground all visible explicit finite positive rules and reset each derived status

**Information available:** Immutable current records, visible changed-source cue, projected past snapshots, observed lineage, explicit fixture domain rules, provenance/authority according to shared access flags. Rules are common executable evidence, not inferred natural-language truth.

**Hidden information unavailable:** Gold affected/valid masks, expected answers, future versions and corruption masks. Gold lineage/fault identity only in explicitly separate oracle runs.

**Budget behavior:** One replay-output step per derived item; global fixed-point CPU work is included in wall time, not a model-call estimate. Atomic abort on cap

**Persistent-state behavior:** Status changes commit to a new immutable snapshot; source ingestion is common to all arms. Fixed propositions only: no generated replacement text.

**Current/historical handling:** Current reads use persistent status; as-known-then uses archived snapshots; retrospective views apply observed corrections. Present permission applies to both historical views after the audit fix.

**Alternative-support behavior:** OR rescue and AND requirements under explicit rules

**Repeated-revision behavior:** Recompute each prefix; preserve archive

**Expected strength:** Recovers all deterministic fixture states

**Known simplifications:** Does not replay an agent execution trace or regenerate content; repeated full graph work

**Difference from closest published method:** No implementation of Rollback selective answer-relevant tool replay

**Does the implementation unfairly weaken it?:** Potentially: output-step costs alone could make a comparison misleading. Add cached B8; require actual calls/tokens for model-backed claims

**Fidelity level:** protocol-level analogue

**Evidence:** [implementation](../../src/evomem/policies.py), [scientific tests](../../tests/test_harness.py), [prior-art audit](CLASSICAL_PRIOR_ART.md), and the method-specific primary reference below.

## B3 — Recorded graph closure

**Baseline ID:** B3

**Name:** Recorded graph closure

**Scientific purpose:** Measure omission and over-invalidation failure modes

**Reference:** [Rollback](https://arxiv.org/abs/2608.10502v1) is adjacent inspiration; exact graph closure is classical

**Implemented algorithm:** Reachability on recorded parent arcs; inactivate every descendant of the cue

**Information available:** Immutable current records, visible changed-source cue, projected past snapshots, observed lineage, explicit fixture domain rules, provenance/authority according to shared access flags. Rules are common executable evidence, not inferred natural-language truth.

**Hidden information unavailable:** Gold affected/valid masks, expected answers, future versions and corruption masks. Gold lineage/fault identity only in explicitly separate oracle runs.

**Budget behavior:** No verifier/model calls; deterministic graph time recorded

**Persistent-state behavior:** Status changes commit to a new immutable snapshot; source ingestion is common to all arms. Fixed propositions only: no generated replacement text.

**Current/historical handling:** Current reads use persistent status; as-known-then uses archived snapshots; retrospective views apply observed corrections. Present permission applies to both historical views after the audit fix.

**Alternative-support behavior:** Intentionally does not rescue independent support

**Repeated-revision behavior:** Traverses each revision; cannot rederive previously invalidated beliefs

**Expected strength:** Exact for visible traversal

**Known simplifications:** Drops AND/OR semantics and support rescue

**Difference from closest published method:** Rollback already rescues trusted independent support and selectively replays

**Does the implementation unfairly weaken it?:** Yes if called Rollback; no as an explicitly naive graph control

**Fidelity level:** intentionally simple control

**Evidence:** [implementation](../../src/evomem/policies.py), [scientific tests](../../tests/test_harness.py), [prior-art audit](CLASSICAL_PRIOR_ART.md), and the method-specific primary reference below.

## B4 — Lexical neighbor closure

**Baseline ID:** B4

**Name:** Lexical neighbor closure

**Scientific purpose:** Test broad over-invalidation control

**Reference:** Internal control; not CUPMem

**Implemented algorithm:** One-hop word-frequency cosine threshold .70

**Information available:** Immutable current records, visible changed-source cue, projected past snapshots, observed lineage, explicit fixture domain rules, provenance/authority according to shared access flags. Rules are common executable evidence, not inferred natural-language truth.

**Hidden information unavailable:** Gold affected/valid masks, expected answers, future versions and corruption masks. Gold lineage/fault identity only in explicitly separate oracle runs.

**Budget behavior:** No model/embedding API; local runtime only

**Persistent-state behavior:** Status changes commit to a new immutable snapshot; source ingestion is common to all arms. Fixed propositions only: no generated replacement text.

**Current/historical handling:** Current reads use persistent status; as-known-then uses archived snapshots; retrospective views apply observed corrections. Present permission applies to both historical views after the audit fix.

**Alternative-support behavior:** No support reasoning

**Repeated-revision behavior:** Repeat one-hop inactivation on cues; no semantic rederivation

**Expected strength:** May catch same-text dependencies

**Known simplifications:** Lexical similarity is not semantic inference; threshold unvalidated

**Difference from closest published method:** Published semantic systems use model proposals/judges and lifecycle handling

**Does the implementation unfairly weaken it?:** Yes as a strong semantic competitor. Keep lexical label; frozen embedding/model candidate selection is a pre-pilot gate

**Fidelity level:** intentionally simple control

**Evidence:** [implementation](../../src/evomem/policies.py), [scientific tests](../../tests/test_harness.py), [prior-art audit](CLASSICAL_PRIOR_ART.md), and the method-specific primary reference below.

## B5 — Thresholded point graph

**Baseline ID:** B5

**Name:** Thresholded point graph

**Scientific purpose:** Separate inference proposal from graph decision rule

**Reference:** [CUPMem](https://github.com/icedreamc/STALE) only motivates inference; graph policy is internal

**Implemented algorithm:** Threshold shared provider scores then collapse groups into parent arcs

**Information available:** Immutable current records, visible changed-source cue, projected past snapshots, observed lineage, explicit fixture domain rules, provenance/authority according to shared access flags. Rules are common executable evidence, not inferred natural-language truth.

**Hidden information unavailable:** Gold affected/valid masks, expected answers, future versions and corruption masks. Gold lineage/fault identity only in explicitly separate oracle runs.

**Budget behavior:** RecordedInference is zero-cost frozen input; future provider setup must be charged equally; arbitrary providers currently trusted

**Persistent-state behavior:** Status changes commit to a new immutable snapshot; source ingestion is common to all arms. Fixed propositions only: no generated replacement text.

**Current/historical handling:** Current reads use persistent status; as-known-then uses archived snapshots; retrospective views apply observed corrections. Present permission applies to both historical views after the audit fix.

**Alternative-support behavior:** Loses OR groups

**Repeated-revision behavior:** No rederivation; repeated invalidation only

**Expected strength:** Allows controlled inference × policy contrasts

**Known simplifications:** Default provider returns existing records at score one, not learned semantics

**Difference from closest published method:** CUPMem has multiple invalidation lanes, semantic target judges, weak challenges, UNKNOWN and query pipeline

**Does the implementation unfairly weaken it?:** Yes if called CUPMem. Retain point-graph label and require a common real inference adapter

**Fidelity level:** protocol-level analogue

**Evidence:** [implementation](../../src/evomem/policies.py), [scientific tests](../../tests/test_harness.py), [prior-art audit](CLASSICAL_PRIOR_ART.md), and the method-specific primary reference below.

## B6 — Conservative reverify

**Baseline ID:** B6

**Name:** Conservative reverify

**Scientific purpose:** Threat from cheap broad evidence checking

**Reference:** Internal task baseline; [StateAuditor](https://arxiv.org/abs/2608.01619v1) is query-side adjacent work

**Implemented algorithm:** Visit derived IDs lexically; verify using explicit finite rules; retain/inactivate/quarantine

**Information available:** Immutable current records, visible changed-source cue, projected past snapshots, observed lineage, explicit fixture domain rules, provenance/authority according to shared access flags. Rules are common executable evidence, not inferred natural-language truth.

**Hidden information unavailable:** Gold affected/valid masks, expected answers, future versions and corruption masks. Gold lineage/fault identity only in explicitly separate oracle runs.

**Budget behavior:** One verifier operation per output; unchecked records remain unchanged; global rule evaluation precedes output gating in this deterministic adapter

**Persistent-state behavior:** Status changes commit to a new immutable snapshot; source ingestion is common to all arms. Fixed propositions only: no generated replacement text.

**Current/historical handling:** Current reads use persistent status; as-known-then uses archived snapshots; retrospective views apply observed corrections. Present permission applies to both historical views after the audit fix.

**Alternative-support behavior:** Correct with common complete rule evidence

**Repeated-revision behavior:** Rechecks all derived records each prefix

**Expected strength:** Insensitive to corruption of separate observed lineage

**Known simplifications:** No LLM semantic verifier; fixture rules make verification unusually easy

**Difference from closest published method:** StateAuditor audits draft premises/dated transitions, not all persistent records

**Does the implementation unfairly weaken it?:** Yes if advertised as StateAuditor. Require common charged semantic verifier and matched query-only arm

**Fidelity level:** protocol-level analogue

**Evidence:** [implementation](../../src/evomem/policies.py), [scientific tests](../../tests/test_harness.py), [prior-art audit](CLASSICAL_PRIOR_ART.md), and the method-specific primary reference below.

## B7 — Positive support-set maintenance

**Baseline ID:** B7

**Name:** Positive support-set maintenance

**Scientific purpose:** Strong classical decision-policy threat

**Reference:** [de Kleer 1986](https://dekleer.org/Publications/An%20Assumption-Based%20TMS.pdf); [Green et al. 2007](https://web.cs.ucdavis.edu/~green/papers/pods07.pdf)

**Implemented algorithm:** Ground thresholded observed support sets by least fixed point: AND inside, OR across; missing justification quarantines

**Information available:** Immutable current records, visible changed-source cue, projected past snapshots, observed lineage, explicit fixture domain rules, provenance/authority according to shared access flags. Rules are common executable evidence, not inferred natural-language truth.

**Hidden information unavailable:** Gold affected/valid masks, expected answers, future versions and corruption masks. Gold lineage/fault identity only in explicitly separate oracle runs.

**Budget behavior:** No model calls for frozen proposal; deterministic inference CPU time recorded

**Persistent-state behavior:** Status changes commit to a new immutable snapshot; source ingestion is common to all arms. Fixed propositions only: no generated replacement text.

**Current/historical handling:** Current reads use persistent status; as-known-then uses archived snapshots; retrospective views apply observed corrections. Present permission applies to both historical views after the audit fix.

**Alternative-support behavior:** Preserves independent OR support; copied evidence requires explicit ancestry, not an origin-count shortcut

**Repeated-revision behavior:** Recomputes visible support admissibility, including reinstatement

**Expected strength:** Classical representation may eliminate all proposed policy headroom

**Known simplifications:** No minimal assumption environments, nogoods, disjunctive context switching or nonmonotonic defaults; absent failed support treated closed-world when a sufficient group is known

**Difference from closest published method:** Captures positive single-context support semantics, not full ATMS or complete JTMS

**Does the implementation unfairly weaken it?:** Not on the finite positive-rule slice; too weak to represent full ATMS claims or unknown natural-language sufficiency. Closed-world annotations must justify hard inactivation

**Fidelity level:** protocol-level analogue

**Evidence:** [implementation](../../src/evomem/policies.py), [scientific tests](../../tests/test_harness.py), [prior-art audit](CLASSICAL_PRIOR_ART.md), and the method-specific primary reference below.

## B8 addition and full replay challenge

B8 `CachedReplay` is an internal, memoized finite-rule recomputation baseline with `faithful_to_original=false`. It caches each output's complete ancestor slice, including source status/validity, visible rule identity and negative results. An input/rule/interval change causes a miss; unrelated outputs reuse cached status. Unsupported cycles still use grounded fixed points. Each miss costs a replay-output step; hits and actual total latency are reported. Ancestor discovery/key construction still has CPU cost and is not an asymptotically optimal incremental engine. Cache is trajectory-local and populated only after an atomic successful sweep; no gold/probe answers enter keys. Cold cache is charged; no warm-start from evaluator state.

It matches B2 snapshots on every existing fixture and saves one replay-output step on the repeated fixture. That is a software regression result, not economic evidence. B8 must appear alongside B2 in any cost claim; a future adapter must measure actual operations and allow the same provider/prompt caching for every arm. This is not DRed, self-adjusting computation, or Rollback reproduced.

## Is B7 just truth maintenance?

For complete finite positive rules, yes: Boolean support maintenance already solves this subproblem. de Kleer's original labels encode minimal consistent assumption environments and reject nogoods; B7 stores neither. Adding an ATMS arm on these fixtures would duplicate the current-context positive consequences, so do not manufacture B7b merely for table length. If adjudication introduces competing assumption contexts/nogoods, add a separately tested environment-maintenance arm before freeze. Do not call ordinary classifier confidence a new repair theory.

## Concrete audit fixes

Grounded inference previously ignored the target memory's own validity interval. That is fixed and regression-tested. Historical-as-known-then disclosure previously ignored present permission revocations; it now preserves the audit snapshot while withholding prohibited output. Existing fixture expectations did not change. The fixes do not add probabilistic decisions.

## 2026-09-26 engineering delta

The [fair comparator matrix](FAIR_COMPARATOR_MATRIX.md) is the current cross-arm inventory. Legacy B4 is now explicitly called B4a lexical closure; the old ID still works for regression reproducibility. B4b uses a pinned MiniLM embedding backend and immutable text/config cache, without treating similarity as support. B5a/B5b use strict model-inferred point groups, fixed thresholding and conventional downstream closure. B5a projects groups to arcs rather than independently eliciting pairs. B7 is renamed **simplified positive support maintenance** in the protocol; no ATMS reproduction is claimed. B9 performs affected closure plus known-independent-root rescue. B10 audits current queries without changing storage. All are internal implementations/adaptations.

B8 adds dependency inspection counts on both cache hits and misses. B2/B6/B8 still use executable rules and fixed proposition status; they do not regenerate text or replay original tool traces. ModelExecutor supplies separately tested model-response caching and replay-purpose accounting, but it does not make symbolic B8 into a live model replay implementation. Complete/gold lineage remains a separate oracle access condition, not a fair ordinary method arm.

Live semantic competence and model-cost fidelity are unvalidated. CUPMem/native comparison is excluded from direct ranking for the reasons in [the integration decision](CUPMEM_INTEGRATION_DECISION.md). Missing native fidelity is not fixed by renaming a method.
