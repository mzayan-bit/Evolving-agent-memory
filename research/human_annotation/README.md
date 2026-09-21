# Blinded human annotation preparation

**Prepared, not executed. No human labels, agreement results, adjudication or model inference.** Original 30 G1 case files are unchanged. The canonical originals and authored labels are copied byte-for-byte under `coordinator_only/authored_originals`; SHA-256 and randomized ID/order maps are in `coordinator_only/case_mapping.json`.

## Distribution boundary

Do **not** send the repository, this coordinator README, root combined CSVs, blinding audit, mapping or author originals to annotators. `annotator_A.csv` and `annotator_B.csv` are identical blank 120-row master templates except annotator ID. Opening them reveals later events, so they are coordinator aggregation templates, not the staged participant distribution.

Send each annotator only ANNOTATION_GUIDE.md, the common NOTICE.md and their `packets/A/stage_0.csv` or `packets/B/stage_0.csv`. Each has the same 30 cases/order under opaque IDs and no answer fields. Receive and lock both stage submissions before releasing the corresponding stage_1, then stage_2, then stage_3. Each later packet contains the complete allowed prefix and no future events. Never distribute all stages together during the blinded exercise.

All 30 variants remove hidden labels/design provenance and document neutral wording proposals in [blinding audit](blinding_audit.md). **G1-13 lacks an explicit deployment conjunction rule; G1-20 lacks initial measurement values.** Neither can be treated as determinate-gold ready. They can be annotated as underdetermined without inventing missing premises. All designated bystanders lack independent corroboration, which may separate retention from factual support. The blinded versions are proposals awaiting coordinator review/freeze, not certified equivalent rewrites. See the audit before recruitment.

## Files and workflow

- `annotator_A.csv`, `annotator_B.csv`: blank master forms, 120 rows each.
- `packets/{A,B}/stage_{0,1,2,3}.csv`: progressive release forms, 30 rows each.
- [ANNOTATION_GUIDE.md](ANNOTATION_GUIDE.md): participant instructions and JSON schema.
- [AGREEMENT_PLAN.md](AGREEMENT_PLAN.md): pre-result metrics, project gates and qualitative vetoes.
- [ADJUDICATION_PROTOCOL.md](ADJUDICATION_PROTOCOL.md), [ADJUDICATION_TEMPLATE.csv](ADJUDICATION_TEMPLATE.csv): future human workflow; template header only.
- [blinding_audit.md](blinding_audit.md): per-case risks, exact original/proposed wording and unresolved failures.
- `coordinator_only/blinding_changes.json`: machine-readable edit ledger; `case_mapping.json`: frozen order/ID maps and source hashes; `authored_originals/`: 30 unmodified originals.
- [analysis script](../../scripts/analyze_annotation_agreement.py) and [synthetic tests](../../tests/test_annotation_agreement.py). Run only after receiving real labels: `python scripts/analyze_annotation_agreement.py completed_A.csv completed_B.csv --output analysis_v1.json`. The script refuses blanks by default, never invokes an LLM and does not overwrite raw inputs/output reports.
- [baseline interface specification](../pilot/BASELINE_IMPLEMENTATION_SPEC.md) and [harness sanity plan](../pilot/HARNESS_SANITY_PLAN.md): documentation only.

## Exact invitation for A

“You are Human Annotator A. Read ANNOTATION_GUIDE.md, then independently complete stage_0.csv using only its visible evidence. Do not use an LLM, web search, the other annotator, the repository or future stage files. Stored claims may be wrong; UNKNOWN/UNCERTAIN is legitimate. Leave the fixed input columns unchanged and complete all required annotation columns. Submit the file to the coordinator, who will lock it before providing stage 1. Repeat through stage 3. Do not overwrite a submitted file; send a dated addendum if needed. Do not discuss labels until both independent passes are locked.”

## Exact invitation for B

“You are Human Annotator B. Read ANNOTATION_GUIDE.md, then independently complete stage_0.csv using only its visible evidence. Do not use an LLM, web search, the other annotator, the repository or future stage files. Stored claims may be wrong; UNKNOWN/UNCERTAIN is legitimate. Leave the fixed input columns unchanged and complete all required annotation columns. Submit the file to the coordinator, who will lock it before providing stage 1. Repeat through stage 3. Do not overwrite a submitted file; send a dated addendum if needed. Do not discuss labels until both independent passes are locked.”

[Validation record](VALIDATION.md) and `coordinator_only/release_manifest.json` record preparation checks and hashes.
