# Preparation validation — no human results

- 30 original G1 files unchanged relative to the prior Git commit; coordinator copies are byte-identical and match their recorded SHA-256.
- Both master CSVs contain 120 blank rows (30 cases × four checkpoints), identical except anonymous annotator ID. Eight staged files contain 30 rows each, in the same randomized order.
- Prefix records expose no future checkpoint. Participant fields are whitelisted observable text/IDs/tasks and blank annotation columns. Titles, source benchmark membership, authored labels and intent are absent. Substantive provenance facts remain visible.
- Every original case has a coordinator-only wording/risk audit and exact proposed replacements. Two substantive missing-premise cases (G1-13, G1-20) remain unresolved; source labels are not certified gold. All 30 variants await coordinator review before freeze/distribution.
- 14 synthetic agreement-analysis tests, three package preservation/blinding tests and four existing smoke tests passed (21 total). These are software checks, not human agreement or baseline-harness runs.
- Ruff lint and format checks passed for the new analysis script and two test files.
- The analysis CLI refuses the actual blank forms with an explicit incomplete-annotation error and writes no results. No missing labels were imputed.
- Local Markdown links checked. No proposed method, baseline policy, harness fixture or provider inference was executed. No human labels/adjudications were supplied.

The release manifest hashes prepared files. It is not approval of semantic equivalence. Before recruitment, the coordinator must accept/version proposed variants, document residual blinding failures and prior participant exposure, and lock the distributed packet/guide/plan hashes. Public-repository availability makes packet-only distribution and no prior exposure essential; filesystem folder names are not access controls.
