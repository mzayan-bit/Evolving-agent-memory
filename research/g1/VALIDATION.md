# Validation record

Inspection date 2026-09-21; literature novelty cutoff 2026-09-20. No proposed-method implementation, training, paid model calls or full pilot was performed.

## Completed checks

- Exactly 30 scenario JSON files; exactly 30 CSV rows, with unique matching IDs G1-01–G1-30.
- 12 public STALE adaptations, 18 original fictional scenarios; all adaptation UIDs and license notice present.
- CSV nested JSON round-trips exactly to canonical scenario fields.
- Both human annotator columns blank in every row/file; no fabricated agreement.
- All cases have three revisions, initial and per-revision draft status, current and prior-prefix historical answers, support sets, versioned source IDs, scope/ambiguity notes and unaffected U.
- All current-state labels belong to valid/invalid/unknown; valid C/D has a proposed sufficient support set; unknown gold is not forced into a binary repair label.
- All Markdown relative file links and heading anchors resolve. Directory links intentionally index scenario folders.
- All 48 distinct external Markdown URLs checked with HTTP GET; 45 returned 200, three publisher URLs returned 403. Publisher pages were independently verified through web search/open records; 403 is access restriction, not evidence of a fabricated citation.
- Exact primary paper titles/authors/versions cross-checked against arXiv metadata; six source-archive hashes and supplementary hash recorded.
- CUPMem store smoke: 3 assertions passed. MemTX targeted official tests: 22 passed. These are mechanics checks, not end-to-end reproductions.
- Upstream STALE and MemTX checkout `git status --short` empty after audit; no upstream changes.

## Restricted direct fetches

- https://www.sciencedirect.com/science/article/pii/0004370277900297 — HTTP 403; primary publisher metadata corroborated via web tool.
- https://www.sciencedirect.com/science/article/pii/0004370279900080 — HTTP 403; primary publisher metadata corroborated via web tool.
- https://www.sciencedirect.com/science/article/pii/000437028690072X — HTTP 403; primary publisher metadata corroborated via web tool.

The direct ACM policy initially returned 403 and subsequently returned 200; its publisher-indexed artifact-badging description was also inspected. COLM’s old site redirected through a landing page, so the citation was corrected to the official 2026 call. These web checks establish source accessibility/identity, not truth of every empirical claim.

## Remaining epistemic limits

Scientific case labels are still unadjudicated AI drafts. Mechanical schema/link checks do not validate human agreement, sufficiency of semantic support, real-world prevalence or model performance. Some cases intentionally contain initially unsupported memories; the metrics explicitly separate these from formerly justified stale descendants. Gold support sets may need revision after human annotation. Several official code releases could not be located despite bounded searches; no absence claim is global.

The two local smoke harness/environment logs remain in the audit workspace; only concise results are included in this research package. No upstream source or model weights are redistributed. Exact procedures and paths are in REPRODUCIBILITY.md.

## Created file inventory

```text
BASELINE_EXPECTATIONS.md
CLASSICAL_PRIOR_ART.md
CLOSEST_WORK_AUDIT.md
COST_ACCOUNTING_PROTOCOL.md
G1_CLAIM.md
G1_NON_CLAIMS.md
HOSTILE_REVIEW.md
INFORMATION_ACCESS.md
KILL_CRITERIA.md
PILOT_DESIGN.md
PREREGISTRATION_DRAFT.md
README.md
REPRODUCIBILITY.md
STATISTICAL_PLAN.md
SUPPORT_ONTOLOGY.md
VALIDATION.md
VARIABLES_AND_METRICS.md
VENUE_FIT.md
annotations/ANNOTATION_30.csv
annotations/ANNOTATION_GUIDE.md
annotations/README.md
annotations/STALE_LICENSE.txt
annotations/adaptation_manifest.json
annotations/scenarios/G1-01.json
annotations/scenarios/G1-02.json
annotations/scenarios/G1-03.json
annotations/scenarios/G1-04.json
annotations/scenarios/G1-05.json
annotations/scenarios/G1-06.json
annotations/scenarios/G1-07.json
annotations/scenarios/G1-08.json
annotations/scenarios/G1-09.json
annotations/scenarios/G1-10.json
annotations/scenarios/G1-11.json
annotations/scenarios/G1-12.json
annotations/scenarios/G1-13.json
annotations/scenarios/G1-14.json
annotations/scenarios/G1-15.json
annotations/scenarios/G1-16.json
annotations/scenarios/G1-17.json
annotations/scenarios/G1-18.json
annotations/scenarios/G1-19.json
annotations/scenarios/G1-20.json
annotations/scenarios/G1-21.json
annotations/scenarios/G1-22.json
annotations/scenarios/G1-23.json
annotations/scenarios/G1-24.json
annotations/scenarios/G1-25.json
annotations/scenarios/G1-26.json
annotations/scenarios/G1-27.json
annotations/scenarios/G1-28.json
annotations/scenarios/G1-29.json
annotations/scenarios/G1-30.json
competitors/cama.md
competitors/planfence.md
competitors/rollback_repair.md
competitors/stateauditor.md
competitors/statemem_cupmem.md
cupmem-smoke.txt
memtx-smoke.txt
source_manifest.json
```
