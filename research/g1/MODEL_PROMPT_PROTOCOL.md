# Model prompt protocol — development candidate v2

> Current integration status: see the final update below and [NON_HUMAN_PROTOCOL_SNAPSHOT.md](NON_HUMAN_PROTOCOL_SNAPSHOT.md). Earlier dated limitations are retained as history.

**Not evaluation-frozen.** No prompt has been tuned on evaluation outcomes or human annotations. Code constants are the canonical exact text: `models/inference.py:SYSTEM,SCHEMA,request_for`; `comparators.py:AUDIT_SYSTEM,AUDIT_SCHEMA`. Their full text is hashed into every response-cache identity. Freeze their Git revision and SHA-256 after development review; do not substitute prose from this document for the executable prompt.

## Input and ontology

Explicit allowlist: checkpoint, visible memory ID/text/kind/scope/validity/status, visible source IDs and origins, permitted authority. No scenario/cluster name, gold support, hidden corruption, expected answer, masks, history or future-created record is serialized. Already-projected current records include historical source versions and their known status, allowing stale dependence to be inferred. IDs and source text themselves must not encode benchmark labels; the importer/data-review boundary is responsible for that. In-process prompt tests are not a sandbox against malicious adapters or prompt injection in documents.

Inference assesses every visible non-source target. Each assessment is `specified`, `none`, or `unknown`. Specified groups have nonempty unique visible members, relation, sufficiency and a finite confidence in [0,1]. Within a group members are AND; groups are OR. Relations use the existing enum: necessary, conjunctive, alternative, partial, copied, correlated, temporal, scope, policy, association, contradiction, unknown. Partial/association/contradiction/unknown cannot be sufficient. No separate invented ontology category replaces existing categories. None/unknown use empty groups. Scope is the target's scope; source and target time validity is evaluated by the deterministic engine. This first candidate has no model-predicted conditional rule intervals; richer temporal conditions remain a representational limitation.

Every object forbids extra fields. IDs, duplicate targets/groups, complete target coverage, sufficiency and numerical bounds are validated locally. Native provider schema avoids unsupported numeric minimum/maximum constraints and states bounds in the description; local validation enforces them. This follows the official [Claude structured-output limitations](https://platform.claude.com/docs/en/build-with-claude/structured-outputs). No few-shot examples; no gold-assisted correction. Invalid support JSON gets at most one fixed schema reminder, never the expected answer; all attempts charged. Refusal/truncation receives no retry. Query audits receive no retry.

## Point-estimate contract

The v2 real-model B5a path separately elicits singleton pairwise links and runs conventional descendant closure. B5b separately elicits AND/OR support sets and runs positive least-fixed-point maintenance. Both consume identical allowlisted visible evidence; prompt/schema differences express the declared representation. Historical FrozenInference comparisons still project the same supplied groups onto arcs. These are different construction protocols and must not be conflated or shared for free in a study ledger. Both use a fixed development candidate threshold .7, currently untuned. Once selected, no confidence changes evidence acquisition, replay, verification or actions. Missing justification follows the fixed classical unknown/quarantine rule; it is not a confidence-adaptive repair controller. The same FrozenInference object can be passed to both policies. Full pipeline PointEstimatePolicy uses the scenario's existing PolicyView and Ledger.

B7 remains an internal simplified positive support closure. It is neither full ATMS nor a claimed JTMS reproduction. Multiple sufficient sets and conjunctions are supported; nogoods, labeled minimal environments, defeasible priorities and contradictions-as-contexts are not. No full ATMS subsystem is justified by the present finite positive fixtures. Revisit if adjudication requires mutually inconsistent assumptions.

## Decoding, versions and resources

| Component | Development configuration |
|---|---|
| Native API | `claude-sonnet-5`, Messages API version 2023-06-01; non-streaming JSON schema output; no SDK retries |
| Sonnet sampling | Omit temperature/top_p/top_k/seed; model-default adaptive thinking and high effort; not deterministic; response cache records the realized output |
| Open model | Qwen/Qwen3.5-9B commit c202236235762e1c871ad0ccb60c8ee5ba337b9a; tokenizer same commit; llama.cpp b9222 local deployment, Q4_K_M conversion (exact provenance in QWEN_LOCAL_DEPLOYMENT.md) |
| Qwen decoding | temperature 0, seed 0, thinking disabled, prompt cache disabled; exact settings in qwen_local/deployment.json |
| Input/output | Per support request input reservation 8192, max output 1024; local adapter timeout 600 seconds; these are engineering settings, not pilot budgets |
| Batching | One visible scenario-prefix per inference request; all its target assessments together; no cross-family batching |
| Retry | One malformed-support-schema retry; no transport/refusal/truncation retry; v2 regression cap two physical calls per support fixture/variant; independent B8 cap six and B10 cap two |
| Query | Current-time target ID; supported/contradicted/unknown, answer or null, active valid visible source citations; cache disabled |
| Embedding | all-MiniLM-L6-v2 commit 1110a243fdf4706b3f48f1d95db1a4f5529b4d41, sentence-transformers 6.1.0, float32 CPU, normalized, max sequence 256, one thread, deterministic algorithms requested |

Embedding truncation is real: long records can lose content. Report it and choose chunking on development before freezing if needed. B4b is semantic similarity, not logical entailment. Its .7 threshold is an untuned candidate. No evaluation search is authorized.

## Historical initial deployment candidate (superseded locally)

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

## Live validation phase additions — 2026-09-26

An opt-in runner now uses `experiment/observable_fixtures.py`: five public fictional support cases whose distinctions are actually stated in visible evidence. It does not pass hidden canonical rules to a model. The prior ambiguous canonical smoke remains historical engineering infrastructure; neither set yields research accuracy claims. B5's prompt/schema/threshold are unchanged and not tuned on these fixtures.

Exact new prompts/schema constants: `readout.py:READOUT_SYSTEM,READOUT_SCHEMA` and `model_replay.py:REPLAY_SYSTEM,REPLAY_SCHEMA`. The bound-state Reader interface takes only ReadoutProbe; evaluator labels remain outside. Generative replay takes explicit visible Derivation instructions/dependencies/version, never gold. Model response cache identity includes exact prompt/schema/generation settings; derived-state cache additionally includes dependency validity, target scope/time bounds, dependency version and an explicit clock when clock_sensitive=True. Clock-relative tasks must declare this flag. Acyclic dependency graphs are required; cycles reject before dispatch.

Live suite defaults and commands are in `tests_live/README.md`. Provider validation requires two opt-ins and caps dispatches at 1 basic + 7 further calls including schema retries. Full provider execution is still unavailable. The local pinned embedding and Qwen tokenizer checks passed; the tokenizer uses an explicitly recorded non-thinking template setting and is not a substitute for server usage counts. No numeric threshold has been selected or newly frozen.

## Local v2 protocol hardening — 2026-09-27

The local deployment in `qwen_local/deployment.json` supersedes the historical vLLM-only setup above. Qwen3.5-9B Q4_K_M runs through llama.cpp b9222, CPU+Accelerate, one slot, 4096 context, four threads. The 8192 input reservation is a ledger ceiling, not a promise of 8192 model context. Exact requests must fit the deployed context including output; these tiny fixtures do. Native JSON-schema grammar is supplied on every request. No cross-device determinism claim is made.

Exact changes are `models/inference.py:ID_CONTRACT,PAIRWISE_CONTRACT,RETRY_REMINDER,request_for` at commit b1d38c7. The original ontology and SYSTEM text remain. Added instructions require literal MEMORY IDs, complete non-source target coverage (including copied beliefs), candidate-only members and JSON only. Every request derives explicit `candidate_memory_ids` / `required_target_ids` lists and schema enums from the same visible view. B5a adds singleton membership and pairwise elicitation instructions; B5b retains AND/OR sets. No tailored examples, expected answers, hidden rules or semantic corrections are added.

Versions: `point-pairwise-development-v2` and `point-support-development-v2`. Dynamic enums constrain syntax/reference grounding, not truth. The strict parser rejects duplicate JSON keys, missing/extra fields, unknown IDs, duplicate targets/relations, self-membership, conflicting group structures and invalid ontology/sufficiency. It does not extract prose, normalize claim text to IDs, guess missing IDs or repair logic. JSON's ordinary whitespace is accepted.

Only protocol-invalid output gets one retry. It contains the original allowlisted payload plus a fixed reminder and the exact malformed response as untrusted data. Both requests, raw responses, usage, latency, category, attempt index and parent request ID are retained. Refusal, timeout, transport failure, truncation and budget exhaustion receive no automatic retry. A schema-valid wrong dependency remains unchanged and receives no semantic retry. Runtime VALID_CORRECT_FORMAT means format only; evaluator-only VALID_WRONG_SEMANTICS is attached after all fixture generations.

The .7 B5 threshold is an unchanged engineering candidate, not a newly selected or evaluation-frozen value. Scores only select a deterministic structure; no confidence-driven acquisition, replay, audit or quarantine is implemented. Full gold/model structures and declared audit targets are retained. Some legacy natural-language evidence underidentifies its authored formal structure; disagreement there is an engineering comparison, not an accuracy estimate.

Run the fixed tiny regression with `EVOMEM_RUN_LIVE_TESTS=1 QWEN_DEPLOYMENT_MANIFEST=research/g1/qwen_local/deployment.json uv run python -m evomem.experiment.qwen_hardening --output results/unique-hardening-run`. Output directories are create-only. All seven legacy fixture families (both repeated checkpoints), the existing multi-target observable view, and two ID-only copies relabelings are included for each B5 variant. B8 compares initial/warm/changed/full regeneration and an atomic budget failure; B10 audits the same query twice. See QWEN_ENGINEERING_ERROR_AUDIT.md for actual outcomes and limits. No scientific pilot was run.
## Final non-human integration update

B5a/B5b v2 prompts, schema and retry rules are unchanged in this integration phase. Current readout and B10 prompt procedures now receive a temporally bound immutable prefix through TemporalModelReadout; requested evidence time and actual dispatch/budget time are separate. No gold, future support graph or expected answer is introduced. Historical raw requests are retained in integration/qwen-temporal-traces.json.

See [ARM_RESOURCE_INTEGRATION.md](ARM_RESOURCE_INTEGRATION.md), [SHARED_COMPUTE_POLICY.md](SHARED_COMPUTE_POLICY.md) and [NON_HUMAN_PROTOCOL_SNAPSHOT.md](NON_HUMAN_PROTOCOL_SNAPSHOT.md) for the contract, evidence and unchanged-criteria readiness assessment. **ENGINEERING VALIDATION ONLY.**
