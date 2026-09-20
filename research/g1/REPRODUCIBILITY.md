# Release and smoke audit

Inspected 2026-09-21; novelty cutoff 2026-09-20. All six primary papers are v1. The additional MemTX paper is v2 (2026-07-28). No post-cutoff paper revision was used. Citation metadata and arXiv source archives were checked against the existing literature ledger.

| Work | Accessible material | Runtime status |
|---|---|---|
| Rollback | v1 HTML, full LaTeX archive/appendices; no attributable code | could not reproduce: no executable release located |
| StateAuditor | v1 HTML/LaTeX and 16-page ancillary PDF with exact prompts | could not reproduce: named scripts not independently accessible |
| PlanFence | v1 full source/Appendix C | could not reproduce: no attributable code located |
| StateMem | v1 full source/appendices | could not reproduce: no attributable code located |
| STALE/CUPMem | [official repo](https://github.com/icedreamc/STALE/tree/ea7d391103a151927cd29d2f01d87597a782bdcb), HEAD `ea7d391103a151927cd29d2f01d87597a782bdcb` (2026-05-19) | partially worked: store-only smoke, three assertions passed |
| CAMA | v1 full source, algorithm, prompts, efficiency/ablations | could not reproduce: no attributable code/checkpoint located |
| MemTX | [official repo](https://github.com/lxy1134/MEMTX_/tree/4e1124ccd5fd384857463020e3497aa73ec93be6), HEAD `4e1124ccd5fd384857463020e3497aa73ec93be6` (2026-07-27) | worked: 22 targeted official tests; full benchmark not reproduced |

## What ran

Python 3.14 local isolated environment, pytest 9.1.1, pydantic 2.13.5. Initial bundled Python lacked pytest; initial PDF extractor lacked PyMuPDF. Installed small dependencies in the audit environment. These environment failures are not competitor failures.

MemTX command: `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q -p no:cacheprovider tests/test_dependency_graph.py tests/test_typed_rollback.py tests/test_validity_interval.py` from its checkout (equivalent paths were supplied from the audit root). **22 passed in 0.03s**. Tests cover reachability, typed cascade/compensation and time intervals. They do not establish benchmark scores or robustness to unrecorded support. No test files were edited.

CUPMem harness imported official `ProfileStore`, `SessionDelta`, `UpdateDecision`, `InvalidationProposal`; added a location item, then directly called `apply_invalidation(INDIRECT_INVALIDATE)` with a later session. Asserted active removal, one stale archive entry and UNKNOWN_CURRENT. **3 assertions passed**. It supplied the decision deliberately and therefore tests store mechanics only, not inferred invalidation correctness. Imports required the OpenAI client package; no client/API request was created. Transformer embeddings require a local checkpoint and have no lexical fallback (`retrieval/embedding.py`). Full CUPMem evaluation was not attempted without model/checkpoint provisioning. No paid model calls.

## Entrypoints and release boundaries

CUPMem: `cup_mem/run_cup_mem.py`; `cup_mem/core/sample_runner.py`; extraction/proposal/judge prompts in `prompt_lib/templates.py`; thresholds in `core/config.py`. STALE generation: `Generation/StepALL_IC_gen.py`; evaluation: `Evaluation/run_target_model.py` and `Evaluation/full_eval_performance.py`. Judge consumes reference explanation; that field must never become ordinary runtime evidence. Dataset format: uid, old/new observations, explanation, SR/PR/IPA queries, history sessions/timestamps and relevant-session indices.

MemTX tests and `src/memtx/dependency_graph.py` / `memtx_manager.py` inspected. The former is bidirectional parent-child adjacency plus transitive traversal; a set of parents is not a set of alternative sufficient justifications. Typed rollback tests explicitly expect every descendant revoked/invalidated/compensated; irreversible effects can remain leaked.

## Searches and uncertainty

Fresh abs links and all six arXiv source inventories inspected; exact paper/short-name web searches and GitHub repository search used. GitHub queries: StateAuditor (0 results), PlanFence (1 third-party result), StateMem (107 mostly unrelated results; no author-attributed release established), Dependency-Guided Rollback Repair (0), Correlation-Aware Memory (1 unrelated plugin). This is a bounded search, not proof that private or differently named code does not exist. CUPMem and MemTX issues endpoint each returned an empty list. Tags and releases APIs also each returned zero entries for both repositories, so the audited commits are the release pins. Exact-title GitHub follow-ups for CAMA, StateMem, Rollback and StateAuditor returned zero repository results. The ambiguous `jlwpony/statemem` name had no README accessible (404), so no author attribution was established. Do not treat unnamed supplement “released” files as independently verified code availability.

## Dataset pin and license

[STALE release](https://huggingface.co/datasets/STALEproj/STALE/tree/617c51dc200b5ab09970834144c7e51c77959af0), SHA `617c51dc200b5ab09970834144c7e51c77959af0`, last modified 2026-05-07. Source JSON LFS SHA-256 `5f3ec375179e20e2e94469e018189188f34e2e7e5f21cbecbd99fcfa648c1876`. The 305 MB haystack file was not downloaded. Dataset-server rows 0–11 and 200–205 were inspected; selected 0–5 and 200–205 are linked by UID in the adaptation manifest. API rows are a convenience view, not a separately pinned dataset; the repository metadata is pinned and release date checked. Only short old/new observations are adapted; no LongMemEval distractor text is redistributed. CC BY 4.0 attribution and changes are recorded in annotations.

## Reproduction limits

Paper tables are author-reported, not independently verified measurements. The audit did not train, evaluate an LLM, run the full pilot, instantiate a repair method, or alter upstream code. Smoke output and source hashes are retained in this package. An executable reproduction requires official releases for missing works and an approved model/checkpoint budget for end-to-end evaluation.
