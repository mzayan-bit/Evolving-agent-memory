# Independent annotation guide — version 1.0

Work independently, without an LLM, web search, the other annotator, the repository, author labels or later release files. All situations are fictional research material. Judge evidence, not what you think the author intended. `UNCERTAIN` is a legitimate action; unknown support is a legitimate conclusion. No reward is attached to matching an intended answer.

## Release sequence

You receive stage_0.csv first: 30 cases in a fixed randomized order. Complete and submit it before receiving stage_1.csv. Repeat through stage_3.csv. Each stage includes only the evidence prefix available at its checkpoint. Earlier submissions are locked; later corrections require a separate dated addendum, never an overwritten file. A coordinator retains the combined master forms and mapping; do not open them during annotation. Do not compare cases to public benchmarks or infer design families.

## What the form contains

The first seven columns are fixed: schema version, anonymous annotator ID, case ID, checkpoint, evidence records, candidate stored claims, and tasks. Source identifiers and version suffixes preserve observable identity/time; they do not certify truth. B1/B2/B3 are stored assertions to evaluate, not gold facts. The same claim ID can name an action recommendation rather than a factual statement; explain any needed atomic decomposition in notes without changing its ID. Unchanged wording is not proof of truth. A record’s upload time need not be its valid time.

Fill all seven JSON annotation columns plus optional notes. Empty cell means **missing work**; `[]` means you intentionally found no entries. Do not edit fixed columns or use spreadsheet auto-formatting on IDs/JSON. JSON uses double quotes and `null`, not Python syntax. Save UTF-8 CSV with proper CSV quoting. You may use an ordinary editor/spreadsheet, but no automated label inference.

## Belief states

`belief_states_json` is a list with one object per claim and required time view:

```json
{"claim_id":"B1","time_view":"current","truth_status":"INSUFFICIENT","use_status":"UNKNOWN","action":"UNCERTAIN"}
```

This is a syntax example, not a suggested answer. Optional free-text keys `normalized_claim`, `scope`, `valid_time` and `rationale` may record your interpretation. Those free-text fields are retained but not string-matched for agreement. All three claims must have each required time view. At t0: `current` only. At t1–t3: `current`, `historical_then`, `historical_now`.

- `current`: assess the claim for the present checkpoint using its visible prefix.
- `historical_then`: assess it at the immediately preceding checkpoint using only evidence available then.
- `historical_now`: assess the same past-time claim using all evidence visible now. Later retraction may undermine a past factual assertion without changing the fact that somebody once believed it.

Truth labels: `SUPPORTED` (justified by visible evidence/rules), `CONTRADICTED` (visible evidence establishes incompatibility in the same scope/time), `INSUFFICIENT` (no adequate basis), `CONFLICTING` (unresolved competing evidence), `UNKNOWN_AMBIGUOUS` (interpretation/scope prevents a determinate judgment). These are epistemic labels, not access to world truth. Permission can lapse while a factual assertion remains supported.

Use labels: `USABLE`, `NOT_USABLE`, `UNKNOWN`. Use refers to the proposition’s stated task/scope. Historical use is evidential usability for an as-of answer, with current disclosure constraints noted separately if relevant.

Actions, for current view only: `RETAIN` (no substantive current-state change needed), `REVERIFY` (seek a specified missing check/source), `INVALIDATE` (stop current reliance; preserve archival record), `REDERIVE_OR_REPLAY` (recompute a derived claim/artifact with updated inputs), `UNCERTAIN` (cannot choose a justified action). Historical views have `action: null`. Retain can be justified operationally even when factual certainty is incomplete: record that distinction rather than forcing matching truth/use/action labels.

## Relations and support

`relations_json` is a list such as:

```json
[{"members":["S1@0","S2@0"],"target":"B1","labels":["conjunctive","scoped_dependency"]}]
```

Use only record IDs actually visible in your row, or candidate claim IDs for derived support. A group of members is one relation candidate; multiple labels may apply. Annotate meaningful positive and negative relationships, including association/contradiction and uncertainty; you need not enumerate every irrelevant cross-product. Missing candidate discovery is analyzed separately from label agreement on jointly identified relations.

| Label | Meaning |
|---|---|
| necessary | Every sufficient justification available in the declared evidence universe requires this member. A sole observed support does not prove no unknown alternatives exist. |
| conjunctive | Members jointly justify the target; individual members do not suffice under the stated rule. |
| alternative_sufficient | This justification is one of multiple sufficient alternatives for the same claim/scope/time. Independence is a separate source-origin question. |
| partial_support | Contributes evidence but is neither necessary nor sufficient alone. |
| copied_support | Repeats/derives from another record without adding a new observation. |
| correlated_support | Shares an upstream observation, measurement or failure source. Distinct source names alone do not prove independence. |
| temporal_dependency | Justification depends on a particular validity interval. |
| scoped_dependency | Justification depends on entity, environment, version or other context. |
| authorization_dependency | Use/action depends on permission even if the proposition remains factually supported. |
| association_only | Related topic, but no evidential justification established. |
| contradiction | Incompatible in the same scope/time under an established constraint. Do not assume exclusive roles or residences. |
| unknown_or_ambiguous | Available evidence cannot determine the relationship; record what clarification is missing. |

`support_sets_json` contains one entry per claim:

```json
[{"claim_id":"B1","assessment":"SPECIFIED","sets":[{"members":["S1@0"],"basis":"DIRECT"},{"members":["S2@0"],"basis":"DIRECT"}]}]
```

Two singleton sets mean either suffices. One set with `members: ["S1@0","S2@0"]` means they jointly suffice. Never flatten these into the same representation. `basis` is `DIRECT` for base evidence/rules, `DERIVED` for prior inferred claims, `MIXED` for both, `UNKNOWN` when origin is unresolved. List minimal sufficient sets; do not include redundant supersets or an empty axiom. Repeated copies are not extra independent observations. When alternatives exist, also record in notes whether their origins are independent, shared or unknown and why; use copied_support/correlated_support relations where warranted. Alternative sufficiency alone is not evidence of source independence. Use `assessment: NONE_SUFFICIENT` and `sets: []` if no sufficient justification is established; use `assessment: UNKNOWN` and `sets: []` if adequacy itself is ambiguous. Put partial/candidate uncertain supports in relations/notes, not as asserted sufficient sets.

## Revision-level selections

At t1–t3, fill arrays of claim IDs:

- `affected_beliefs_json`: current content, admissible use or provenance needs substantive reconsideration because of this revision. This is not automatically a set to delete.
- `preserved_beliefs_json`: current content/use/justification should remain substantively unchanged. Do not overlap with affected; unresolved cases may be in neither.
- `historical_valid_beliefs_json`: claims supported at the immediately previous checkpoint **retrospectively**, using current evidence. Match the historical_now perspective, not merely that they were once asserted.

At t0 use `[]` for these three fields (there was no revision). `ambiguous_relationships_json` is a list of `{members:[...], target:"B1", reason:"..."}`; use `[]` if none. Notes record alternative interpretations, missing policies, unobservable source independence or statements needing splitting. Do not repair the case by inventing a premise.

## Submission

Preserve an untouched copy of each input and your submitted version. Submit your stage file to the coordinator only. Do not discuss answers with the other annotator until both passes are locked and adjudication is explicitly opened. If wording appears to give away an answer, flag it in notes and explain your own evidential judgment anyway.
