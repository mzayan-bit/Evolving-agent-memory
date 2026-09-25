# Model prompt protocol — development candidate v1

**Not evaluation-frozen.** No prompt has been tuned on evaluation outcomes or human annotations. Code constants are the canonical exact text: `models/inference.py:SYSTEM,SCHEMA,request_for`; `comparators.py:AUDIT_SYSTEM,AUDIT_SCHEMA`. Their full text is hashed into every response-cache identity. Freeze their Git revision and SHA-256 after development review; do not substitute prose from this document for the executable prompt.

## Input and ontology

Explicit allowlist: checkpoint, visible memory ID/text/kind/scope/validity/status, visible source IDs and origins, permitted authority. No scenario/cluster name, gold support, hidden corruption, expected answer, masks, history or future-created record is serialized. Already-projected current records include historical source versions and their known status, allowing stale dependence to be inferred. IDs and source text themselves must not encode benchmark labels; the importer/data-review boundary is responsible for that. In-process prompt tests are not a sandbox against malicious adapters or prompt injection in documents.

Inference assesses every visible non-source target. Each assessment is `specified`, `none`, or `unknown`. Specified groups have nonempty unique visible members, relation, sufficiency and a finite confidence in [0,1]. Within a group members are AND; groups are OR. Relations use the existing enum: necessary, conjunctive, alternative, partial, copied, correlated, temporal, scope, policy, association, contradiction, unknown. Partial/association/contradiction/unknown cannot be sufficient. No separate invented ontology category replaces existing categories. None/unknown use empty groups. Scope is the target's scope; source and target time validity is evaluated by the deterministic engine. This first candidate has no model-predicted conditional rule intervals; richer temporal conditions remain a representational limitation.

Every object forbids extra fields. IDs, duplicate targets/groups, complete target coverage, sufficiency and numerical bounds are validated locally. Native provider schema avoids unsupported numeric minimum/maximum constraints and states bounds in the description; local validation enforces them. This follows the official [Claude structured-output limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs). No few-shot examples; no gold-assisted correction. Invalid support JSON gets at most one fixed schema reminder, never the expected answer; all attempts charged. Refusal/truncation receives no retry. Query audits receive no retry.

## Point-estimate contract

B5a projects the same inferred groups onto pairwise dependency arcs and runs conventional descendant closure; it is **not a separately optimized pairwise-only inference prompt**. B5b retains groups and runs positive least-fixed-point maintenance. Both use a fixed development candidate threshold .7, currently untuned. Once selected, no confidence changes evidence acquisition, replay, verification or actions. Missing justification follows the fixed classical unknown/quarantine rule; it is not a confidence-adaptive repair controller. The same FrozenInference object can be passed to both policies. Full pipeline PointEstimatePolicy uses the scenario's existing PolicyView and Ledger.

B7 remains an internal simplified positive support closure. It is neither full ATMS nor a claimed JTMS reproduction. Multiple sufficient sets and conjunctions are supported; nogoods, labeled minimal environments, defeasible priorities and contradictions-as-contexts are not. No full ATMS subsystem is justified by the present finite positive fixtures. Revisit if adjudication requires mutually inconsistent assumptions.

## Decoding, versions and resources

| Component | Development configuration |
|---|---|
| Native API | `claude-sonnet-5`, Messages API version 2023-06-01; non-streaming JSON schema output; no SDK retries |
| Sonnet sampling | Omit temperature/top_p/top_k/seed; model-default adaptive thinking and high effort; not deterministic; response cache records the realized output |
| Open model | Qwen/Qwen3.5-9B commit c202236235762e1c871ad0ccb60c8ee5ba337b9a; tokenizer same commit; vLLM 0.30.0 development candidate |
| Qwen decoding | temperature 0, seed omitted unless explicitly set in request; backend defaults otherwise recorded via pinned runtime/server manifest |
| Input/output | Per request input reservation 8192, max output 1024; 45-second HTTP timeout; these are engineering settings, not pilot budgets |
| Batching | One visible scenario-prefix per inference request; all its target assessments together; no cross-family batching |
| Retry | One malformed-support-schema retry; no transport/refusal/truncation retry; smoke max five physical calls including retry |
| Query | Current-time target ID; supported/contradicted/unknown, answer or null, active valid visible source citations; cache disabled |
| Embedding | all-MiniLM-L6-v2 commit 1110a243fdf4706b3f48f1d95db1a4f5529b4d41, sentence-transformers 6.1.0, float32 CPU, normalized, max sequence 256, one thread, deterministic algorithms requested |

Embedding truncation is real: long records can lose content. Report it and choose chunking on development before freezing if needed. B4b is semantic similarity, not logical entailment. Its .7 threshold is an untuned candidate. No evaluation search is authorized.

## Open model deployment

Only vLLM is prepared, not Transformers/llama.cpp alternatives. Use a separate environment, pin vLLM==0.30.0, model and tokenizer revisions, and archive exact launch command, context length, dtype, quantization, GPU/CPU model, driver/CUDA/torch versions and decoding defaults. `QWEN_DEPLOYMENT_MANIFEST` points to JSON containing model, revision, tokenizer_revision, vllm_version, dtype, quantization, hardware, context_length, server_command. Use the literal string `none` for no quantization. Additional runtime fields are retained in the cache identity. The launcher validates the core pins; it cannot attest that a remote server actually honors a user-supplied manifest. Reconcile with server logs before R1.

The official [Qwen card](https://huggingface.co/Qwen/Qwen3.5-9B) and [vLLM schema API](https://docs.vllm.ai/en/latest/features/structured_outputs/) were checked 2026-09-26. Public model commits and package release numbers were read from Hugging Face/PyPI metadata; no model weights or runtime were installed. No configured Qwen endpoint was found; hardware feasibility was not established. Do not claim an unsupported Mac conversion or exact cross-device determinism.

## Reproduction commands

After supplying an already authorized existing credential/endpoint, run one smoke command; never use CI secrets by default:

```sh
uv run python -m evomem.experiment.model_smoke --provider anthropic --output results/unique-claude-smoke
uv run python -m evomem.experiment.model_smoke --provider vllm --output results/unique-qwen-smoke
```

Outputs are create-only directories containing manifest, ledger and raw attempts. Smoke response reuse is disabled so five valid prefixes exercise five physical dispatches; production inference may use the separately tested immutable cache. Five canonical fixture prefixes retain seven target assessments: five primary claims, a semantic bystander and an intermediate copy. Fixture gold returned by the existing factory is discarded, never sent to the client. Some canonical fixtures deliberately reuse the same natural-language records with different authored formal rules. Those hidden rules are not inferable from identical text; unknown is legitimate. This set cannot measure dependency accuracy or establish competence by matching fixture gold. PASS means transport/schema/accounting completion only. Inspect semantic outputs manually; do not compute G1 statistics. Provider absence yields explicit SKIPPED. Full pytest uses offline doubles only.

Future evaluation freeze requires development competence inspection for both model families, reviewed temporal coverage, thresholds, context/output bounds, retry policy, complete deployment record, cache parity, and prompt checksums. No API guarantees exact repeated outputs, even at temperature zero.
