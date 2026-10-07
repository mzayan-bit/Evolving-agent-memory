# Shared computation and cache policy

**Contract ready to freeze; scientific numeric budgets are not selected.** Identical work may be shared only when every relevant arm receives the same artifact under the same conditions.

## Allowed sharing

Scenario parsing, immutable source records, fixed metadata and the common declared task are identical inputs. Model/tokenizer weights may be loaded once on the same device, with startup reported separately. No model-built initial memory or inferred graph may masquerade as free supplied data.

The only implemented model-artifact sharing is explicit policy isolation: the same support proposal bundle goes to every selected applicable B5a/B5b/B7/B9 arm. Each is allocated the full original inference/retry/token cost and tested against its budget before use. A separate original physical construction ledger prevents counting duplicated allocations as repeated real inference. B5a here projects shared groups onto arcs; its separately elicited end-to-end pairwise mode is a different named comparison. Prefix binding rejects changed evidence; differences in prior arm-maintained belief status do not change the frozen common construction input.

End-to-end support inference, verification, query audits, replay generation and repair-specific inference remain arm-specific. Embedding artifacts are **not shared across arms** in this implementation, even if future work could distribute them fairly. Loading the same immutable embedding model is distinct from giving one arm free encoded inputs. Every relevant arm receives the same access opportunity; artifacts actually selected by an algorithm can differ, with their work charged.

## Cache inventory

| Cache | Material identity | Ownership / lifetime | Invalidation and accounting |
|---|---|---|---|
| Embedding | Complete backend identity (model/revision, packages, precision, normalization, truncation/device configuration) + exact text | Arm-local; checkpoint/revision-persistent within a run | Changed text/model identity misses. Unchanged text can legitimately reuse across IDs/times because metadata is not an input to the embedding function. Selection/scope decisions are recomputed. One physical encode per miss; local lookup/encode time recorded |
| Model response / support inference | Provider/model/version/deployment including quantization/runtime; exact system/user text, schema/version, temperature/seed/output/reservation settings | Arm-local, checkpoint/revision-persistent exact requests; new run must be cold | Checksum-verified immutable result; visible support requests include checkpoint and all material visible record fields. Invalid structured output is revalidated, not repaired. Retry cache disabled and paid |
| B8 descendant | Above request identity + dependency records/validity/version, target scope/time interval and explicit clock when clock-sensitive | Arm-local; checkpoint/revision-persistent within trajectory | Changed source version/content/validity, dependency version, scope or material time invalidates. Non-clock-relative unchanged descendants can reuse. Local checks are counted; failed transaction commits no partial state or cache |
| B10 audit | No response reuse | Every query independent; no query-persistent result cache | Every recurrence consumes verification/model calls and actual tokens |
| Shared ordinary model readout | No response reuse | Every query independent | Effective temporal prefix selected before generation; later query spends current ledger credits |

A checkpoint is material when it changes the function's input. Do not add meaningless clock values to a pure text-embedding key, and do not omit the clock for a time-relative derivation. Future source/support versions may not be borrowed for historical queries. Native llama.cpp prompt caching remains disabled in the pinned deployment; no hidden server warm-context advantage is claimed.

Cold namespaces eliminate order-dependent cross-arm response warming. Within-arm persistence is available consistently to the functions that legally support reuse. B8 reuses generated dependencies because that is its declared algorithm; it receives no free construction or privileged graph. Full replay uses identical evidence and bypasses descendant reuse, with every regeneration charged. B10's no-reuse rule is an explicit algorithm contract required to measure query recurrence, not an accidental implementation asymmetry. Physical work, allocated work, cache hits and cache misses remain separate.

No simultaneous writers or concurrent executors on one ledger are supported. A trusted caller must preserve archived immutable input/response files; checksums detect accidental mutation, not a malicious experimenter. Future changes to sharing or cache scope require an explicit protocol revision before evaluation, not an undocumented optimization.
