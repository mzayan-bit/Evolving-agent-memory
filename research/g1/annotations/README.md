# Thirty-case annotation draft

Exactly **30 core scenarios: 12 STALE adaptations (6 Type I, 6 Type II) and 18 original fictional naturalistic cases**. These are AI-authored research drafts, not human annotations or empirical incidents. There are **zero completed human annotators**, no agreement statistic, and no model results. `annotator_A` and `annotator_B` are intentionally empty in both JSON and CSV.

Canonical definitions are [scenarios](scenarios/); [ANNOTATION_30.csv](ANNOTATION_30.csv) is the analysis view with nested objects serialized as JSON. [Ontology](../SUPPORT_ONTOLOGY.md) defines semantics; [guide](ANNOTATION_GUIDE.md) defines independent annotation. Do not show draft gold to annotators during their first pass. `source_versions_visible` in draft gold is a convenient evaluator snapshot, not an extra runtime oracle.

## Provenance and licensing

Adapted from **Hanxiang Chao, Yihan Bai, Rui Sheng, Tianle Li and Yushi Sun, STALE: Can LLM Agents Know When Their Memories Are No Longer Valid? (2026)**, [paper](https://arxiv.org/abs/2605.06527v1), [dataset release](https://huggingface.co/datasets/STALEproj/STALE/tree/617c51dc200b5ab09970834144c7e51c77959af0). Dataset revision `617c51dc200b5ab09970834144c7e51c77959af0`, CC BY 4.0; [license text](STALE_LICENSE.txt), [license explanation](https://creativecommons.org/licenses/by/4.0/). Adaptations are offered under CC BY 4.0 with this attribution; no endorsement by the source authors is implied.

[adaptation_manifest.json](adaptation_manifest.json) records each source UID/row and changes. We retained short old/new observations and added work context, persistent derived records, bystanders, support structures and two further revisions. We **changed** some interpretations to ambiguous or scope-specific; original explanations are not our gold. No LongMemEval haystack distractor text is redistributed. Original cases G1-13–30 contain fictional, project-authored evidence, not vendor/API/policy facts.

Selection is purposeful stress coverage, not a random representative sample. First six Type I and first six Type II release rows were inspected and adapted; this convenience selection cannot establish population prevalence. G1-07–12 particularly challenge overly strong cross-attribute inference. Expanded evaluation needs independent domains and human-authored evidence.

## Schema and status

Each file includes initial A/B evidence, derived C/D, unaffected U; typed support sets; three source revisions; visible source snapshots; current and historical draft outcomes; alternative/shared-origin support; missing and spurious candidates; fault-cue regime; repair/change/survival sets; ambiguity notes and independent annotation slots. Empty support sets mean no sufficient support supplied, not logical falsehood or an axiom.

`valid`, `invalid`, `unknown` refer to **current admissible reuse of the stored proposition**. `invalid` can mean contradicted, superseded or unsupported in an explicitly closed rule system; record the subtype during human annotation. `unknown` permits clarification/quarantine and must not be silently scored as false. Some intentionally bad initial memories test spurious inference; stratify them from formerly justified descendants when computing repair recall/stale-descendant reuse.

## Coverage map

- Missing support: G1-13, 16, 19, 21, 22, 23 and selectable links in other justified cases.
- Spurious association/bystander: U in all 30; especially G1-02, 03, 16 and 22.
- Alternative independent support: G1-01, 14, 17, 24; evolving alternative G1-26.
- Conjunction: G1-13, 18, 20, 23, 25.
- Copies/common cause: G1-15, 19, 20, 27, 29; ambiguous dependence in adaptations.
- Historical truth/revision: all; prospective G1-21 versus retroactive correction G1-29.
- Three successive revisions: all 30, including legitimate reinstatement G1-27.
- Scope and permission: G1-03, 06, 10, 16, 17, 18, 22, 23, 26, 30.
- Genuine ambiguity: G1-04, 07–12, 20, 28. Do not reduce it to random label noise.

These are ontology-development cases. They are not held-out confirmatory test cases, and no generalization estimate should be reported from them.
