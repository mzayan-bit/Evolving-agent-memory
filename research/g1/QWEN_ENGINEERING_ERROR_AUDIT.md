# Qwen model-inference engineering error audit

Live run: 2026-09-27. Report finalized: 2026-10-03.

**ENGINEERING FIXTURES — NOT RESEARCH EVALUATION.** No scientific pilot, human-label evaluation, significance test or proposed G1 method.

## Observed outcomes

31 new real Qwen generations; 22/22 support rows received model responses; 21/22 support rows schema-valid; 2 protocol-invalid attempts (both CONTRADICTORY_STRUCTURE; zero JSON-syntax/MALFORMED_OUTPUT failures); 12 schema-valid rows disagreed with their declared engineering structural reference. Counts are descriptive inventory outcomes, not estimates of model quality.

Exact usage: 28,266 input + 4,646 output tokens. Physical request latency sum 1572.165 s; ledger latency (also local replay preparation) 1572.167 s; suite elapsed 1576.306 s.

| Fixture | Arm | Pipeline | Format | Structural agreement | Category | Calls | Input | Output | Request seconds | Retries |
|---|---|---|---|---|---|---:|---:|---:|---:|---:|
| alternative@1 | B5a | True | True | False | VALID_WRONG_SEMANTICS | 1 | 996 | 95 | 36.912 | 0 |
| alternative@1 | B5b | True | True | False | VALID_WRONG_SEMANTICS | 1 | 938 | 89 | 35.654 | 0 |
| conjunction@1 | B5a | True | True | False | VALID_WRONG_SEMANTICS | 1 | 996 | 95 | 44.712 | 0 |
| conjunction@1 | B5b | True | True | False | VALID_WRONG_SEMANTICS | 1 | 938 | 89 | 33.969 | 0 |
| copies@1 | B5a | True | True | False | VALID_WRONG_SEMANTICS | 1 | 1007 | 163 | 53.414 | 0 |
| copies@1 | B5b | True | True | False | VALID_WRONG_SEMANTICS | 1 | 949 | 163 | 53.939 | 0 |
| correction@1 | B5a | True | True | True | VALID_CORRECT_FORMAT | 1 | 1076 | 163 | 54.806 | 0 |
| correction@1 | B5b | True | True | True | VALID_CORRECT_FORMAT | 1 | 1018 | 163 | 58.279 | 0 |
| necessary@1 | B5a | True | True | True | VALID_CORRECT_FORMAT | 1 | 996 | 95 | 28.858 | 0 |
| necessary@1 | B5b | True | True | True | VALID_CORRECT_FORMAT | 1 | 938 | 89 | 46.910 | 0 |
| observable-bystander | B5a | True | True | True | VALID_CORRECT_FORMAT | 1 | 1564 | 536 | 118.513 | 0 |
| observable-bystander | B5b | True | False | None | CONTRADICTORY_STRUCTURE | 2 | 3432 | 676 | 205.504 | 1 |
| repeated@1 | B5a | True | True | True | VALID_CORRECT_FORMAT | 1 | 1153 | 237 | 68.598 | 0 |
| repeated@1 | B5b | True | True | True | VALID_CORRECT_FORMAT | 1 | 1095 | 237 | 75.403 | 0 |
| repeated@2 | B5a | True | True | False | VALID_WRONG_SEMANTICS | 1 | 1225 | 237 | 67.592 | 0 |
| repeated@2 | B5b | True | True | False | VALID_WRONG_SEMANTICS | 1 | 1167 | 237 | 69.808 | 0 |
| semantic_bystander@1 | B5a | True | True | True | VALID_CORRECT_FORMAT | 1 | 1076 | 163 | 48.118 | 0 |
| semantic_bystander@1 | B5b | True | True | True | VALID_CORRECT_FORMAT | 1 | 1018 | 163 | 55.264 | 0 |
| short-ids | B5a | True | True | False | VALID_WRONG_SEMANTICS | 1 | 989 | 159 | 71.167 | 0 |
| short-ids | B5b | True | True | False | VALID_WRONG_SEMANTICS | 1 | 931 | 159 | 93.512 | 0 |
| similar-ids | B5a | True | True | False | VALID_WRONG_SEMANTICS | 1 | 1025 | 166 | 58.319 | 0 |
| similar-ids | B5b | True | True | False | VALID_WRONG_SEMANTICS | 1 | 967 | 166 | 57.007 | 0 |

## Gold and committed model structures

`target <- [members]`: singleton arcs for B5a; one AND group per bracket, alternatives as separate entries for B5b. Empty means no selected structure on the declared audit targets. Relation/confidence details and all unscored proposals are retained in [manifests](qwen_hardening/manifests.json) and [raw trace extracts](qwen_hardening/traces.json).

| Fixture / arm | Reference | Model | Audited targets |
|---|---|---|---|
| alternative@1 / B5a | b1 <- [s1]; b1 <- [s2] | b1 <- [s1] | b1 |
| alternative@1 / B5b | b1 <- [s1]; b1 <- [s2] | b1 <- [s1] | b1 |
| conjunction@1 / B5a | b1 <- [s1]; b1 <- [s2] | b1 <- [s1] | b1 |
| conjunction@1 / B5b | b1 <- [s1, s2] | b1 <- [s1] | b1 |
| copies@1 / B5a | b1 <- [s1]; b1 <- [s2]; s2 <- [s1] | b1 <- [s1]; s2 <- [s1] | b1, s2 |
| copies@1 / B5b | b1 <- [s1]; b1 <- [s2]; s2 <- [s1] | b1 <- [s1]; s2 <- [s1] | b1, s2 |
| correction@1 / B5a | b1 <- [s1]; b2 <- [s2] | b1 <- [s1]; b2 <- [s2] | b1, b2 |
| correction@1 / B5b | b1 <- [s1]; b2 <- [s2] | b1 <- [s1]; b2 <- [s2] | b1, b2 |
| necessary@1 / B5a | b1 <- [s1] | b1 <- [s1] | b1 |
| necessary@1 / B5b | b1 <- [s1] | b1 <- [s1] | b1 |
| observable-bystander / B5a | ∅ | ∅ | assoc |
| observable-bystander / B5b | ∅ | INFERENCE FAILED | assoc (not scored after failure) |
| repeated@1 / B5a | b1 <- [s1]; b2 <- [s2]; b3 <- [s3] | b1 <- [s1]; b2 <- [s2]; b3 <- [s3] | b1, b2, b3 |
| repeated@1 / B5b | b1 <- [s1]; b2 <- [s2]; b3 <- [s3] | b1 <- [s1]; b2 <- [s2]; b3 <- [s3] | b1, b2, b3 |
| repeated@2 / B5a | b1 <- [s1]; b1 <- [s4]; b2 <- [s2]; b3 <- [s3] | b1 <- [s1]; b2 <- [s2]; b3 <- [s3] | b1, b2, b3 |
| repeated@2 / B5b | b1 <- [s1]; b1 <- [s4]; b2 <- [s2]; b3 <- [s3] | ∅ | b1, b2, b3 |
| semantic_bystander@1 / B5a | b1 <- [s1]; b2 <- [s2] | b1 <- [s1]; b2 <- [s2] | b1, b2 |
| semantic_bystander@1 / B5b | b1 <- [s1]; b2 <- [s2] | b1 <- [s1]; b2 <- [s2] | b1, b2 |
| short-ids / B5a | 1 <- [0]; 2 <- [0]; 2 <- [1] | 1 <- [2]; 2 <- [3] | 1, 2 |
| short-ids / B5b | 1 <- [0]; 2 <- [0]; 2 <- [1] | 1 <- [0]; 2 <- [0] | 1, 2 |
| similar-ids / B5a | m10 <- [m1]; m100 <- [m1]; m100 <- [m10] | m10 <- [m1]; m100 <- [m1] | m10, m100 |
| similar-ids / B5b | m10 <- [m1]; m100 <- [m1]; m100 <- [m10] | m10 <- [m1]; m100 <- [m1] | m10, m100 |

## B8 and B10 real execution

B8 passed full/incremental equivalence and atomic commit checks. Cache misses include a lookup whose generation was subsequently blocked; they are not identical to physical calls. Request latency excludes the small separately charged local dependency preparation.

| B8 phase | Hits | Misses | Physical calls | Regenerated nodes | Input | Output | Request seconds |
|---|---:|---:|---:|---|---:|---:|---:|
| initial | 0 | 2 | 2 | t, v | 600 | 71 | 33.512 |
| warm | 2 | 0 | 0 | none | 0 | 0 | 0.000 |
| incremental | 1 | 1 | 1 | t | 301 | 36 | 14.755 |
| full | 0 | 2 | 2 | t, v | 600 | 71 | 28.476 |
| atomic_budget_failure | 0 | 2 | 1 | t | 301 | 36 | 14.888 |

The incremental update regenerated `t` from K17 to K29 and reused unaffected `v`; full replay on identical evidence produced identical records. Across these checks: 3 derived-cache hits, 7 misses, 6 physical generations, 10 dependency checks. The final fresh transaction paid for `t`, blocked `v` before dispatch at the six-call cap, and committed neither partial state nor cache. The earlier literal one-call cap / second-call-no-dispatch receipt remains in [validation-final.json](qwen_local/validation-final.json).

B10 passed twice: each audit returned `contradicted`, corrected the answer to K29, and cited source `s`. Two physical verification calls, zero cache hits, 970 input / 92 output tokens, 44.275 seconds request latency. Persistent storage still contains K17; answer correctness and state correctness remain separate. Recurrent audit cost is explicit.

See [metrics](qwen_hardening/metrics.json), [memory](qwen_hardening/memory.json), [tokenizer audit](qwen_hardening/independent-tokenizer-audit.json), [immutable cache readback](qwen_hardening/cache-readback.json), and [code/artifact provenance](qwen_hardening/provenance.json).

## Interpretation and scope

All rows are **ENGINEERING FIXTURES — NOT RESEARCH EVALUATION**. They are a fixed inventory, not a sample from a research population. No significance, confidence intervals, ranking or residual-headroom estimate is warranted. The seven legacy fixture families include both repeated-revision checkpoints. Their gold is unchanged. Some legacy scenarios have identical language but different hidden authored AND/OR structures, so exact structural disagreement can reflect underidentification as well as model error. Two ID tests rename the existing copies fixture only. No examples or prompts were tuned after inspecting these new semantic results.

B5a and B5b receive identical allowlisted visible evidence per fixture (matching evidence hashes); each pays its own inference cost. B5a separately elicits singleton links, whereas B5b retains AND/OR support sets. The legacy FrozenInference shared-proposal projection remains available and is a distinct construction protocol. Both use unchanged provisional .7 point thresholding. Confidence does not trigger acquisition, replay, verification or adaptive repair. For B5a the audit compares committed arcs; for B5b it compares committed sufficient member sets. Full raw proposals retain relation, sufficiency and confidence. Exact agreement here is not an entailment oracle or an assessment of every relation enum.

The multi-target observable fixture executes all five existing target assessments. Its formal semantic comparison is deliberately limited to `assoc`: the office-paint statement does not authorize protocol M83. The other observable targets are retained for inspection, not silently scored correct. This limitation is part of every row's manifest. The v2 observable B5b response twice included its target `copy` in its own members and failed with CONTRADICTORY_STRUCTURE; no partial output was salvaged. Both raw responses and the exhausted retry remain recorded. The prior B5b `assoc <- e` sufficient-support error remains in qwen_local/validation-final.json and QWEN_STRUCTURED_OUTPUT_FAILURES.md as VALID_WRONG_SEMANTICS. It was neither repaired nor removed. One wrong fixture, old or new, is not scientific evidence.

The six valid B5b disagreements include `repeated@2`: its raw output omitted the newly active `s4` justification and marked all returned groups copied/insufficient at confidence .5, leaving no committed sufficient sets under the unchanged .7 threshold. This is a real point-baseline structural error under the authored reference, not a parser failure. It is not evidence that every legacy mismatch is a language-entailment mistake or that any threshold is calibrated. B5a had 5 exact agreements / 6 disagreements across 11 valid rows; B5b had 4 agreements / 6 disagreements across 10 valid rows, plus one unscored protocol failure.

## Protocol and failure boundary

The original copies failure used complete claim strings as target IDs despite visible literal IDs. The old schema only required strings and the prompt did not sufficiently emphasize literal ID use; the model violated target grounding. Native JSON-schema grammar was working syntactically. The strict parser correctly rejected the output. No serialization or target-visibility defect was found. Raw outputs, exact former schema, retries and costs are retained in [QWEN_STRUCTURED_OUTPUT_FAILURES.md](QWEN_STRUCTURED_OUTPUT_FAILURES.md).

The v2 generic contract adds explicit candidate/required-ID lists and schema enums, complete target coverage and literal-ID instructions. B5a adds a singleton-membership constraint and separate pairwise elicitation. The ontology remains unchanged. The parser rejects arbitrary prose, duplicate JSON keys/targets/groups, missing fields, unknown IDs, self-membership and contradictory structures. It never guesses IDs or repairs logic. Exact text lives in models/inference.py at b1d38c7; all request/prompt/schema hashes and full request objects are retained.

One protocol-invalid output may receive one fixed reminder with its raw malformed response and original visible evidence. Every attempt is charged. Refusal, transport failure, timeout, truncation and exhausted budgets are explicit terminal categories. Schema-valid semantic mistakes are not retried. Runtime VALID_CORRECT_FORMAT means schema success only; the evaluator attaches VALID_WRONG_SEMANTICS after all support generations. Missing/failed inference remains explicit, never an invented empty correct result. Successful tiny checks do not guarantee arbitrary future outputs will parse.

## Resources and reproducibility

Same pinned Qwen3.5-9B source, Bartowski Q4_K_M conversion and llama.cpp b9222 as [QWEN_LOCAL_DEPLOYMENT.md](QWEN_LOCAL_DEPLOYMENT.md). Exact source/conversion/runtime commits, weight/archive hashes and launch command remain in qwen_local/deployment.json and each run's runtime identity. Mixed imatrix-calibrated quantization changes numerical weights. The converter names the official model but does not attest an exact upstream commit; do not claim independent full-weight equivalence.

M4 MacBook Air, 16 GB unified memory; CPU+Accelerate, four threads, one slot, 4096 context, f16 KV, batch 256 / ubatch 128, no context shift, no speculative decoding or vision projector. Metal was unavailable to this execution session. Temperature 0, seed 0, thinking disabled, server prompt cache disabled. B5 max output 1024, input reservation 8192 (ledger bound, not usable context); all tiny requests fit deployed context. Manifests retain per-request generation settings, hardware, OS, usage, attempts, retries, remaining budgets and response hashes. CPU scheduling and this fanless machine affect latency; no throughput claim follows from one run.

Input/output tokens and model calls are actual measured work. Raw returned usage is preserved; missing categories remain unknown. Token audits independently count rendered prompts and sampled output IDs, including terminating EOS. The official pinned tokenizer independently encodes exact server-rendered prompts and decodes sampled output. Client monotonic request latency is distinct from end-to-end suite elapsed time and small charged local dependency preparation. Server timing fields are retained but not substituted for client measurements. The peak RSS measurement covers the fresh inference server process; it is not whole-machine unified-memory usage or GPU allocation. Observed peak server RSS: **7,612,186,624 bytes (7.09 GiB)**, measured by Darwin `getrusage(RUSAGE_CHILDREN)` after a fresh server exited normally. All 31 input/output count checks and all 31 independent official-tokenizer checks matched. Energy and currency cost are unavailable, not zero.

The protocol implementation was committed as b1d38c7 before this run. Manifests can report dirty=true because documentation was being updated while inference ran; executable prompts and runner were unchanged during generation. Full local raw attempts and content-addressed cache files remain under results/qwen-hardening-v1. Checked-in trace extracts preserve every request, raw generated content, usage and original response hash while omitting redundant native verbose prompt/grammar text. No human material or credentials is included.

## R1 reassessment against unchanged criteria

The definition and previous assessments in [R1_READINESS_CRITERIA.md](R1_READINESS_CRITERIA.md) are unchanged. The gate table requires “at least one live returned usage record” (G2) and an inspectable actual-provider smoke (G8); it does **not** independently require a billed remote API or Claude specifically. A real local llama.cpp provider with returned token usage and inspected physical generation satisfies that local pathway requirement. This does not validate Claude or silently make both-family evaluation-freeze review optional. No credentials were obtained or invented.

| Gate | Status | Evidence / remaining limitation |
|---|---|---|
| G1 | PASS | Actual separately elicited B5a/B5b traces plus prior real pinned MiniLM encode; inspectable basic source-dependent replay/audit competence. Semantic mistakes remain; no study-wide competence claim |
| G2 | PASS | New raw returned input/output/cache usage, exact token-ID checks and independent official tokenizer audit; offline normalization/unknown/reasoning tests. No invented local USD/energy |
| G3 | PARTIAL | Prior real one-call/second-no-dispatch check and new B8 paid-first/blocked-next atomic transaction; offline reservation/reconciliation/overrun tests. Pre-existing revision-credit release/final study-arm integration remains unresolved |
| G4 | PARTIAL | Same-evidence full versus incremental real regeneration, physical/reused counts, local dependency time and immutable response readback. Final multi-arm cache parity remains unvalidated |
| G5 | PASS | Pairwise-versus-shared-proposal deviation documented; B8/B9/B10 remain internal adaptations, no published reproduction claim |
| G6 | PARTIAL | Point policies use shared PolicyView/Ledger/source prefix; query-only B10 and support-aware rollback available. Historical model readout and final integrated arm scope still unresolved |
| G7 | PASS | Existing poisoned-view/allowlist tests plus retry tests exclude gold-assisted repair; evaluator compares only after model pass. This is the tested boundary, not proof against arbitrary malicious adapters |
| G8 | PASS | Versioned protocol/runtime, immutable content-addressed response checks, raw usage, request/attempt/retry records and actual local provider traces. Claude smoke remains unavailable |
| G9 | PASS | No human annotation edits, pilot, proposed controller or fixture hypothesis statistics |

**Overall R0 remains. The Qwen deployment/protocol blocker is cleared; overall readiness is not R1.** This is not caused by an invented API-only gate. The pre-existing final assessment explicitly requires “resolve final resource-release/cache parity integration,” adequate replay/readout scope “historical audit where claimed,” and development prompt/threshold review/freeze. Those requirements cannot be replaced by tiny local fixtures. Label-dependent threshold selection is also unfinished. Human adjudication itself remains the separate R2 gate, as originally written.

No changes to R1_READINESS_CRITERIA.md were made. Claude is unvalidated; the broader future evaluation-freeze language in MODEL_PROMPT_PROTOCOL.md calls for both model families and must be reviewed explicitly before a study freeze. This report does not waive it.

## Development freeze reassessment

See [DEVELOPMENT_FREEZE_CANDIDATE.md](DEVELOPMENT_FREEZE_CANDIDATE.md). Model/revision/quantization/runtime, generic ID protocol/schema, parser/retry, local accounting/cache contract, current-time B8/B10 semantics and result schema are READY TO FREEZE for their tested scope. Numeric B4/B5 thresholds NEED DEVELOPMENT DATA; .7 was not selected or newly frozen. Integrated construction/release/cache parity and historical model scope are BLOCKED. Claude remains unvalidated. No pilot freeze is signed.

## Engineering stop decision

**Yes, narrowly targeted remaining integration work can still change pilot validity.** Unequal inference-construction charges, incorrect revision-credit release, unfair cache reuse, or claiming unsupported historical answers can change baseline comparisons. The already-written criteria identify these specific outstanding checks. Therefore a blanket claim that infrastructure can no longer affect validity would be false.

**Stop general architecture expansion and fixture-driven semantic prompt tuning now.** Freeze the ready local contracts; wait for independent development annotations before choosing thresholds or measuring residual headroom. Limit any separately authorized pre-pilot engineering to final matched-arm resource/cache integration and agreed time/readout scope. Do not build extra abstractions or add tests merely to raise the count. No such extra implementation is performed in this phase. G1 must remain unimplemented until adjudicated data and residual-headroom evaluation exist.


## Final validation and code provenance

`uv run pytest`: **165 passed** (1.30 s); `uv run ruff check .`: clean; `uv run mypy src tests`: clean across 40 source files. `UV_CACHE_DIR=/private/tmp/evomem-uv-cache` was used. See [tests.json](qwen_hardening/tests.json).

Generation used committed protocol/runner b1d38c7. After generation, commit 5358ca5 fixed one summary-only accounting edge case: unavailable physical token usage now propagates as unknown instead of being summed as zero. Two focused tests cover input/output unknowns. All usage in this actual run was known, so no reported token total or model request changed; no extra generation was required. Original receipts are retained as generated, including their original `model_latency_ms` key; that key includes charged local replay preparation and is explicitly distinguished from physical request latency above.

The local endpoint was restarted after peak-RSS capture and returned healthy. This is a local process, not a newly installed persistent system service. No pilot, G1 implementation, human annotation changes, threshold selection or research-question changes were made. The R1 criteria remain byte-for-byte identical to 84ab65c; their hash is in provenance.json.
