# Agreement analysis preregistration — project protocol v1.0

Frozen before any human results. This is an internal preregistration, not an external registry entry. No humans have annotated and no agreement results exist. The user-requested gates below supersede the earlier Stage-0 provisional .85 raw/.80 relation gate for this annotation exercise. Do not tune thresholds to completed labels. Protocol/variant approval and file hashes must be frozen before recruitment; later changes require a new version and fresh independent annotation, not a retroactive improved score.

## Units and denominators

30 independent case families; four nested checkpoints per case; three candidate claims per checkpoint. At t0 each has current view; later checkpoints add historical_then/historical_now. Thus a complete pass contains 120 rows and 900 belief-state units. Relations/support sets are nested, variable-sized annotations. Report complete-case coverage, explicit unknowns and missing work; never substitute an LLM or author label. Two blank forms are not agreement.

The script requires identical observable inputs and paired row coverage. Blank required cells reject analysis by default. `--allow-partial` yields an explicitly exploratory complete-paired-row analysis and lists exclusions; it cannot pass project gates. Explicit `[]` is a completed empty set. Missing and uncertain are different. Unknown support assessments are excluded from determinate set/edge overlap, with their counts/coverage reported; high exclusions can invalidate an aggregate pass.

## Metrics frozen in advance

1. **Raw exact row agreement:** fraction of complete paired rows with identical closed belief truth/use/actions, typed relation sets, support assessments/sets/basis, revision ID selections and presence/absence of ambiguity notes. Ignore member ordering and optional free-text rationale; do not call this literal prose agreement. Exact whole-case agreement requires every included checkpoint to match, and is confirmatory only with all four checkpoints present.
2. **Belief-state agreement:** matched truth labels / paired claim-time-view units; report current, historical_then, historical_now separately, plus use and action agreement. Primary raw summary is equal-weight mean of case-level truth agreement, with pooled unit rate secondary. Report confusion matrices and marginals.
3. **Relation-label agreement:** union of relations identified by either annotator, keyed by sorted member group and target; typed set exact/F1, presence disagreement and per-label binary agreement. Do not manufacture a huge set of unannotated true negatives. Labels may co-occur: no single multiclass kappa over serialized label lists.
4. **Support-edge overlap:** expand specified sufficient sets to unique (member,target) pairs. For A reference/B prediction, precision = intersection/|B|, recall = intersection/|A|; reverse roles too. These are agreement measures, not accuracy against human gold.
5. **Support-set agreement:** exact matching of member sets per target after sorting/deduplication checks. AND `{X,Y}` does not match OR `{X},{Y}`, even if edge F1 is 1. Symmetric F1 = 2×intersection/(|A|+|B|). No semantic LLM alignment, subset credit or post-hoc normalization. Basis agreement is reported separately on shared sets. Annotators may explain logically equivalent decompositions; manual adjudication can align them later without altering the raw score.
6. **Affected-descendant, preserved-belief and historical-valid agreement:** set exact match plus directional overlap and symmetric F1 over the named candidate claims at t1–t3. These are annotator selections, not transitive-closure predictions.
7. **Uncertainty/disagreement:** count current units with UNKNOWN_AMBIGUOUS truth, UNKNOWN usability or UNCERTAIN action; report each annotator’s count/denominator, support-UNKNOWN target count, rows with ambiguity notes, and union-relation ambiguity count. Report categorical disagreement as 1−raw agreement and affected/preserved disagreements. Manual critical-confusion review is mandatory.
8. **Cohen kappa:** unweighted kappa `(p_o−p_e)/(1−p_e)` on fixed paired single-label truth/use/action units; `p_e` from observed marginals. Constant-class/empty cases are undefined, not perfect. Per-label binary relation kappa is descriptive and prevalence-sensitive. Do not gate on it as if relations were independent.

Set conventions: both empty yields exact agreement=true, F1 undefined (not 1); one empty/one nonempty gives F1=0. Report both-empty counts and macro F1 over eligible nonempty comparisons plus pooled micro F1. Primary support gates use equal-weight mean of within-case macro F1, with eligible-case count; cases without eligible comparisons are NA. Complete high agreement dominated by empties is insufficient evidence.

## Project gates — not universal standards

- All 30 cases/four stages complete for both annotators; raw source forms locked and version matched.
- Scenario-macro belief truth agreement ≥ .80, and pooled current/historical_then/historical_now truth agreement each ≥ .80.
- Pooled truth kappa ≥ .70 **when applicable**: at least two observed categories in both annotators, expected agreement <1, at least 30 paired units, and each annotator’s least frequent observed category has ≥5 units. If not applicable, mark the gate unassessable; do not replace kappa with zero or declare a pass.
- Scenario-macro support-edge F1 and support-set F1 both ≥ .80, with at least 20 eligible cases and at least 70% of all paired target-checkpoint assessments determinate for both annotators. The 70% is an analysis-coverage requirement, not an annotation quota; never discourage UNKNOWN to meet it.
- Report affected/preserved/historical-valid F1 and exact agreement; values <.80 trigger review even if other gates pass.

## Qualitative vetoes

Before looking at outcomes, define systematic critical disagreement as either (a) the same central confusion in at least three distinct cases, or (b) at least 20% of relevant eligible candidate relations across at least two cases. Review association versus dependency, copied versus independent evidence, necessary versus alternative support, and current versus historical truth. The coordinator codes confusion categories after both raw passes are locked; record denominator, examples and alternative explanations. Multiple relation labels can legitimately coexist: a label mismatch alone is not automatically a conceptual error. A documented inability to apply a central distinction reliably vetoes expansion even when aggregate scores clear numeric gates.

Missing-rule or underdetermined cases are not failures merely because both humans mark uncertainty. If uncertainty prevents studying the intended distinctions, the cases/ontology fail their scientific purpose. Do not adjudicate them into a determinate claim without new visible evidence and fresh annotation. More than two missing/unusable stages per case or exclusion of a central family blocks a complete-package conclusion.

## Uncertainty and reporting

The deterministic script reports descriptive metrics, case-level values and counts; it does not compute significance or auto-authorize a gate pass. Thirty clusters are the inferential sample, not 900 independent observations. If intervals are later added, resample whole cases retaining all stages/claims/relations; lock seed and method before results. No t-test over individual edges. No significance testing is required for these engineering reliability gates.

Analyze pre-adjudication forms first. Publish raw agreement, missingness, unknowns and critical disagreements even if adjudication produces a convenient final gold. If gates fail, allow one documented guide/variant revision and a fresh blinded pass (prefer new annotators or explicitly report carryover). Persistent central disagreement stops benchmark expansion and the G1 method direction; do not adjust thresholds after seeing scores.
