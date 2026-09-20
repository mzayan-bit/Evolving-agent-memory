# Independent annotation guide v0.1

## Task and units

Read only the scenario narrative, evidence sources, scope rules and the revision prefix visible at the current time. Hide `draft_gold`, `gold_*`, `required_support`, repair/change/survival suggestions and ambiguity commentary on the first independent pass. The proposed benchmark author knows later events; annotators and runtime models must not use them to resolve an earlier ambiguous event.

Annotate (1) each claim’s proposition/scope/time, (2) source-origin identity, (3) relation existence/type, (4) minimal sufficient support sets, (5) current usability and historical truth status after each revision, and (6) allowed repair actions. Trajectory is the sampling unit; relations and revision labels are nested units.

## Definitions

Support is evidence plus any declared rule sufficient to justify a proposition in a particular scope/time, or explicitly partial evidence when sufficiency is absent. Dependency means removing/changing that support changes justification under the stated rule; causal language is not required. Stale means a formerly usable assertion is still treated as current after its validity/support has ended. Invalid current use includes contradicted/superseded/unpermitted claims; label the subtype. Unknown means evidence is insufficient, not a synonym for false.

Previously true means supported at the requested earlier valid-time. A retracted fabricated result may never have been true, although the old belief/report existed. Independent support requires a separate evidential origin relevant to the failure mechanism, not a different URL, author or summary. Alternative supports each suffice; conjunctive members jointly suffice. Mere association shares topic but supplies no justification. Scope includes entity, environment, jurisdiction (if fictional rule supplied), version, task, action and authorization. Time includes occurrence/validity and recording/upload separately.

## Annotation steps

1. Normalize C/D into atomic propositions if they conflate fact and permission or exact value and threshold. Record all edits; do not silently simplify away a hard case.
2. List visible base sources with origins, authority and valid intervals. Mark independence known/partial/unknown with a reason.
3. Enumerate candidate relations including plausible negatives; mark support type using [ontology](../SUPPORT_ONTOLOGY.md). Distinguish missing candidate discovery from classification over a supplied candidate list.
4. Write sufficient support sets. A member is necessary only relative to the enumerated evidence universe. Preserve unknown alternatives explicitly.
5. At each revision mark C/D/U as usable, unusable or unresolved; state an acceptable current answer and an as-of answer. Supply the smallest valid repair and acceptable conservative alternatives. Content-preserving provenance updates are not false invalidation.
6. Mark confidence as human ordinal high/medium/low plus reason; never call it a calibrated probability. Record ambiguity about truth, scope, support type or origin separately.
7. Submit independently; only then expose the AI draft and the other human’s labels for adjudication.

## Positive and negative examples

For G1-13, compatibility AND security jointly authorize deployment; security alone cannot rescue it. For G1-14, independent valid Lab B rescues the threshold claim after A retracts. For G1-15, copied dashboards cannot rescue their withdrawn source. For G1-16, staging and production share words but have separate flags. For G1-18, consent withdrawal blocks use without making the temperature measurement false. For G1-07, a scorpion anecdote does not uniquely identify residence. For G1-29, preserve historical belief attribution without asserting the retracted finding as historical truth.

## Ambiguity procedure

Record at least two coherent interpretations and the missing clarification needed when relevant. If the evidence permits both travel and relocation, current residence is unresolved. Do not assume exclusive jobs, residences, affiliations or communication preferences. Do not force an AND/OR label when support is merely suggestive. Genuine unknowns remain in a dedicated abstention stratum; author mistakes that make the scenario incoherent are corrected transparently before freeze.

## Human agreement plan (not results)

Two independent humans annotate all 30; neither uses the other's answers or draft gold. An adjudicator resolves discrepancies after recording original labels, with reason and versioned edits. No person has completed this procedure yet.

Report raw agreement and confusion matrices for mutually exclusive status/type labels. Use Cohen’s κ only on paired single-label units with reported class marginals/prevalence; provide scenario-clustered uncertainty and do not interpret low κ without base rates. For missing/ordinal labels use the appropriate Krippendorff α distance and report missingness. Multi-label relation sets require per-type agreement and set/edge precision/recall/F1 against adjudication, including candidate-discovery misses; naive κ on strings is unsuitable. Support sets need semantic equivalence after normalization (member order ignored; redundant supersets removed only under accepted rules), not JSON text equality. Bootstrap entire scenarios, never independent edges.

Proposed gate: raw agreement at least .85 for usable/unusable/unknown and per-type relation F1 at least .80 on necessary/conjunctive/alternative/association after one rubric revision; disclose κ/α rather than replacing them with those thresholds. These are provisional engineering gates, not universal statistical standards. If disagreement persists across two fresh blinded passes or more than 20% of non-ambiguity cases cannot be adjudicated, stop benchmark expansion and narrow the ontology. Preserve the ambiguous stratum and report its size separately.
