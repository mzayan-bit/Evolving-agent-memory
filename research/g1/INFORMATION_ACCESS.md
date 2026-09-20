# Information access matrix

Main policy-isolation track freezes the initial memory, inferred support proposal, accessible evidence and source metadata for every arm. No gold affected descendants are exposed. A separate oracle track is an upper bound, never a fair main competitor. `Shared` means identical across arms; `Budgeted` means same opportunity with usage charged.

| Policy | Gold fault ID | Gold affected scope | Gold dependency sets | Future state | Full past history | Provenance | Authority | External evidence | Query oracle | Extra model calls |
|---|---|---|---|---|---|---|---|---|---|---|
| No repair | Changed-source cue only | No | No | No | Shared | Shared observed | Shared observed | Budgeted query access | No | No repair calls |
| Source-only | Changed-source cue only | No | No | No | Shared | Shared observed | Shared observed | Budgeted | No | Within cap |
| Full reset/replay | Changed-source cue only | No | No | No | Shared | Shared observed | Shared observed | Budgeted | No | Replay charged |
| Explicit-edge closure | Changed-source cue only | No | No; corrupted recorded graph | No | Shared | Shared observed | Shared observed | Budgeted | No | Within cap |
| Semantic-neighbor invalidation | Changed-source cue only | No | No | No | Shared | Shared observed | Shared observed | Budgeted | No | Similarity/extraction charged |
| Point inferred graph | Changed-source cue only | No | No; shared point estimate | No | Shared | Shared observed | Shared observed | Budgeted | No | Inference charged/shared |
| Conservative reverify/replay | Changed-source cue only | No | No | No | Shared | Shared observed | Shared observed | Budgeted | No | All checks charged |
| Point support-set TMS/rederive | Changed-source cue only | No | No; same inferred support sets | No | Shared | Shared observed | Shared observed | Budgeted | No | Inference/rederive charged |
| Future uncertain policy (not implemented) | Same cue | No | No | No | Shared | Shared observed | Shared observed | Budgeted | No | Same cap, no privileged verifier |
| Oracle support upper bound | Yes | Yes | Yes | No | Shared | Gold origin only if labeled | Gold only if labeled | Same pool | No | Report separately |

“Changed-source cue” identifies the new observation/source version, not a diagnosis that every sentence in it is false. Known-fault corruption experiments may supply a faulty ID to **all** arms; unknown-fault experiments supply none and charge diagnosis. Do not merge their scores. Scope predicates stated explicitly in source text are available; evaluator affected-item masks are not.

The full-history column refers to the same past history accessible via the common context/retrieval limits, not unlimited tokens for one arm. Point policies may choose not to read it but retain the same access opportunity. Classical oracle performance tests annotation/representation consistency, not deployable quality.

## Leakage guards

Strip source benchmark explanations, relevant-session indices, future versions, draft gold, suggested missing/spurious masks and annotator notes from runtime input. Keep runtime record IDs separate from gold semantic labels. Do not encode label in filenames or IDs. Corruption masks are evaluator-only; visible lineage shows the corrupted result without revealing which edges were removed. Human annotation views are also prefix-limited and hide draft decisions until independent submission.
