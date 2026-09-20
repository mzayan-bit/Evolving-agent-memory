# Support ontology, version 0.1 (draft for human review)

The object is **justification of a scoped, time-indexed claim**, not semantic similarity and not truth in the universe. Represent an item as `(id, proposition, entity, scope, valid_from, valid_to, recorded_at, source_origin, authority, permission)`. Valid-time and recorded-time differ; intervals are half-open. Revisions close an interval and add a version. Historical truth and permission to disclose are separate labels.

| Relation | Operational meaning | Positive example | Negative / ambiguity boundary |
|---|---|---|---|
| Necessary support | Every admissible sufficient justification in the declared evidence universe contains A | Build approval requires the sole signed safety certificate | `A→C` in material implication does **not** mean A is necessary. Necessity is relative to enumerated justifications; unknown alternatives preclude certainty. |
| Conjunctive support | One sufficient justification requires all members | Deploy if load test AND security approval pass | Two agreeing reports are not automatically a conjunction. |
| Alternative sufficient support | Each alternative set independently suffices for the same scoped claim | Either of two independently run valid tests certifies the stated threshold | Two summaries copied from one test do not create independent alternatives. |
| Partial / contributing | Raises plausibility but is neither necessary nor sufficient | Small exploratory study supports a broad hypothesis | Do not turn association or weak evidence into logical entailment. |
| Copied / derived evidence | Content inherits an upstream origin | Dashboard copies a test report | Separate URLs/authors do not prove independent measurement. |
| Correlated support | Shared source or causal origin creates dependence | Two reports use the same instrument calibration | Correlation can be partial, not only exact duplication; unknown origin remains unknown. |
| Temporal dependency | Justification applies only during a specified interval | Capacity estimate used for a booking in June | A June revision need not invalidate the May historical answer. |
| Scope dependency | Relation holds only for specified entity/environment/version | Staging flag enables staging export | Production export is a related bystander unless its own flag changes. |
| Policy / authorization | Claim may remain true but action/use loses permission | Dataset is accurate but consent to reuse expires | Invalid permission does not prove the data false or require rewriting history as false. |
| Mere association | Related subject without evidential dependence | API documentation and billing address share a customer | Embedding proximity is not a reason to invalidate. |
| Contradiction | Claims cannot both hold under identical scope and time under declared constraints | Same exclusive deployment slot assigned two versions | Two offices, jobs or affiliations can coexist; do not impose exclusivity from stereotypes. |
| Unknown / ambiguous | Evidence does not determine relation, source independence or scope | Beach runs may be travel rather than relocation | Ask/reverify, retain competing interpretations or quarantine reliance; never manufacture a confident label. |

## Representation

For item i, `S_i = {{A,B},{C}}` denotes `(A AND B) OR C` sufficient justification. Store a justification identifier, members, validity/scope predicates and origin groups. Base observations and explicit domain rules must be visible evidence. Represent uncertain **existence/type** of a justification separately from uncertain truth of its members and uncertain source reliability.

The annotation file lists named relationships and `support_sets` per derived item. `unknown` sets are not silently converted to empty sets. Empty evidence means ungrounded/unknown, not false. A support set with no members may represent an axiom only if explicitly labeled; none is assumed by default.

## Repair semantics

At time t, retain a current claim if at least one admissible sufficient justification remains valid and permitted. Invalidate current reuse if every known justification fails and the evidence universe is closed for that claim. Under open-world uncertainty, mark unverified/quarantine current reliance until reverified; do not assert factual falsity. Repair can replace a value, update its support, close its current interval or regenerate a dependent artifact. A valid independently supported claim may need its provenance updated without its content being invalidated.

Historical answers use evidence valid at the requested past time, subject to present disclosure permission. A source later found fabricated may invalidate earlier belief attribution as truth while preserving the historical statement “the agent believed X”; a simple supersession does not retroactively make X false. Tag revision kind: correction, supersession, scope narrowing, withdrawal, permission revocation or reinstatement.

## Ambiguity and gold

These 30 files contain **AI-authored draft gold**, not human gold. Annotators see the scenario without draft decisions, independently label relation existence/type, support sets, origins and per-revision allowed state. Record alternative admissible interpretations. Cases with genuine indeterminacy are scored on appropriate uncertainty/abstention, not forced current facts. Preserve uncertain cases in a separate outcome stratum; do not remove them just to improve agreement.

## Formal model boundary

A possible future action set is retain/reverify/quarantine/repair/invalidate under budget B. A weighted objective over stale reuse, false invalidation, cost and recurrence is a decision-theoretic description, not a new algorithm. Predeclare weights or report Pareto curves. Logical support sets already follow [ATMS/provenance](CLASSICAL_PRIOR_ART.md); no controller is implemented or selected here.
