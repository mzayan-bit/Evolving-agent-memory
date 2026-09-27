# Qwen local deployment — ENGINEERING VALIDATION

This deployment addresses only the missing local generative-model portion of R0.
It is **not scientific evidence**, a pilot, an evaluation of support quality, or
permission to implement G1. Research questions, annotation files, prompts,
thresholds and baseline semantics remain unchanged.

## Selection for the M4 / 16 GB MacBook Air

Use the official **llama.cpp b9222 arm64 release**, serving one local slot with a
4,096-token context. The installed build reports `9222 (9a532ae4b)`.
The repository's Qwen HTTP adapter now has an explicit `llama.cpp` dialect:
JSON-schema grammar via `response_format`, thinking disabled, temperature 0,
seed 0 and prompt-cache reuse disabled. The existing vLLM dialect remains usable.
The local client accepts loopback HTTP origins only and does not forward vLLM keys.

MLX-LM was considered first (mlx-lm 0.31.3, mlx / mlx-metal 0.32.2).
Importing `mlx.core` failed with:

> [metal::load_device] No Metal device available.

System Profiler identifies an M4 and Metal support; llama.cpp's device listing
also exposed no usable Metal device in this session. This is an execution-session
restriction, **not evidence that the Mac lacks a GPU or cannot run Qwen**.
The recorded deployment therefore uses CPU + Apple Accelerate (`--device none --n-gpu-layers 0`), four threads,
256-token batches, 128-token microbatches, one slot, no context shifting, no
speculative decoding and no vision projector. This keeps installation small and
permits real bounded engineering checks within the available access.

For faster use in a normal terminal with GPU access, the same pinned binary and
GGUF can use Metal (remove `--device none`, set `--n-gpu-layers 99`,
after checking `--list-devices`). That
configuration must be recorded as a separate deployment and revalidated; these
results must not be presented as Metal measurements. MLX-LM is also an appropriate
Apple Silicon route when Metal is accessible, but its conversion/runtime would
need its own identity and validation. vLLM is unnecessary for this one-user Mac.

## Exact representation and provenance

- Official selected model: `Qwen/Qwen3.5-9B`.
- Pinned source: `c202236235762e1c871ad0ccb60c8ee5ba337b9a`.
- Converter: `bartowski/Qwen_Qwen3.5-9B-GGUF`.
- Conversion revision: `182be2fd6c7bc44887d88a91cb03ff009cc9f549`.
- File: `Qwen_Qwen3.5-9B-Q4_K_M.gguf`, 6,169,341,984 bytes (5.75 GiB).
- SHA-256: `d784ce9eda1a5a7b51e8f705a9e6310844bf4f173654d115823c775fdea56d43`.
- Runtime archive SHA-256:
  `36862cb5ad4cd817df10e0b88d6d1512e126f6bf3a2c2de65bef641f99eb485b`;
  matches the official GitHub release asset digest.

The converter names the post-trained Qwen3.5-9B repository and llama.cpp b9222,
with importance-matrix calibration. Q4_K_M is a **lossy mixed quantization**, not
the original full-precision model: 125 Q4_K tensors, 16 Q5_K, 49 Q6_K, 20 Q8_0
and 232 F32 tensors in this file. It retains a multi-token prediction layer in
its 33-block GGUF; speculative/MTP inference is disabled. Vision is not loaded.
The source's complete multimodal BF16 weights total 19,306,216,416 bytes, already
larger than 16 GB before runtime allocations. That makes quantized text inference
the sensible deployment for this hardware. No fine-tuning or model substitution
was performed here; quantization may change outputs and scientific performance.

The converter does not attest an exact upstream commit. However, the official
repository still resolves to the selected pin, and all four source weight LFS
hashes match its initial weight-upload revision
`21eca8a083a2121a92fba681f4a7c72cf20ff1a7`. The GGUF chat-template bytes exactly
match the pinned official template (SHA-256
`a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715`).
All 248,070 official vocabulary entries and all 247,587 merge rules match
the GGUF; its 250 extra vocabulary slots are padding.
This documents the relationship without claiming an independent reconstruction
of quantized weights. The GGUF's `base_model ... 9B-Base` metadata names the
pretraining parent; the conversion card identifies the post-trained 9B source.
The deployment identity includes both source and conversion revisions plus the
weight checksum, so it cannot share EvoMem caches with full-precision vLLM.

## Reproduce

All commands below run from the repository root. Weights and runtime live in
sibling directories and are not committed. No new Python dependency is needed
by EvoMem's local adapter or runner.

Download and extract the official archive into `../g1-llama-b9222`:

```sh
mkdir -p ../g1-llama-b9222 ../g1-qwen-gguf
curl -fL --retry 3 -o ../g1-llama-b9222/release.tar.gz \
  https://github.com/ggml-org/llama.cpp/releases/download/b9222/llama-b9222-bin-macos-arm64.tar.gz
shasum -a 256 ../g1-llama-b9222/release.tar.gz
# Check the exact archive checksum above before extracting.
tar -xzf ../g1-llama-b9222/release.tar.gz -C ../g1-llama-b9222
curl -fL --retry 3 -C - -o ../g1-qwen-gguf/Qwen_Qwen3.5-9B-Q4_K_M.gguf \
  https://huggingface.co/bartowski/Qwen_Qwen3.5-9B-GGUF/resolve/182be2fd6c7bc44887d88a91cb03ff009cc9f549/Qwen_Qwen3.5-9B-Q4_K_M.gguf
python3 scripts/start_qwen_local.py
```

The launcher checks the runtime version and full weight checksum before starting the exact command
in [deployment.json](qwen_local/deployment.json). Bind address is `127.0.0.1:8087`.
Debug verbosity 10 is used for these tiny fictional fixtures to return raw
sampled token IDs for accounting; logs/attempts can contain input and output
text and remain local under ignored `results/`. Stop the server with Ctrl-C to
release memory. Do not expose this unauthenticated local server to the network.

In another terminal:

```sh
export QWEN_DEPLOYMENT_MANIFEST=research/g1/qwen_local/deployment.json
export QWEN_LOCAL_URL=http://127.0.0.1:8087
EVOMEM_RUN_LIVE_TESTS=1 .venv/bin/python -m evomem.experiment.qwen_local \
  --output results/qwen-local-validation
.venv/bin/python -m evomem.experiment.model_smoke --provider llama.cpp \
  --output results/qwen-local-existing-fixtures
```

Use fresh output directories. The local validation runner has separate call caps
of 1 (trivial generation and second-call rejection), 2 (B5b, including at most one
existing schema retry), 2 (B8 cold/warm/changed source), and 1 (B10). The existing
five-fixture runner caps its phase at five calls. It can fail if a retry consumes
one of those calls; the cap is not raised automatically. No paid API is used.
All results remain engineering-only, even when every interface passes.

## Evidence

An initial adapter attempt sent the schema at the wrong nesting level. The
server ignored that field and returned unconstrained text; this consumed six
real generations, and B5b/B8/B10 correctly failed validation. The real one-call
stop and all six token-accounting checks passed. The failed receipt is retained
as [validation-initial-schema-error.json](qwen_local/validation-initial-schema-error.json).
Inspection of the pinned server parser identified the required
`response_format.json_schema.schema` nesting. The adapter and regression test
were corrected, without altering inference prompts, thresholds or model weights.
The corrected deployment identity includes a schema-protocol version.

A second bounded attempt enforced grammar and passed B8/B10, but B5b failed
target coverage. Its six generations and failed receipt are also retained.
llama.cpp does not show its grammar schema to the model, so the final adapter
serializes the existing `ModelRequest.schema_json` into the system message in
addition to grammar enforcement. This is a format-contract adaptation, with no
fixture-specific hints, new scientific prompt content, confidence-threshold
changes, or hidden labels. It is explicitly part of the deployment identity.

The final bounded validation passed with five physical generations:

| Check | Result | Input / output tokens | Client latency |
|---|---|---:|---:|
| Trivial JSON generation | PASS | 65 / 6 | 6.220 s |
| `max_model_calls=1` | First executes, second rejected before transport | No second inference | — |
| B5b observable support batch | Parsed six support proposals; deterministic B5b completed | 1,301 / 418 | 67.596 s |
| B8 cold generation | K17 result | 301 / 36 | 10.307 s |
| B8 unchanged / changed source | Unchanged cache hit; K29 regenerated | 301 / 36 for regeneration | 10.966 s |
| B10 query audit | `contradicted`, correction K29, citation `s`; no memory mutation | 485 / 46 | 17.348 s |

Total: 2,453 input tokens, 542 output tokens, 112.437 s of client-measured
request latency. All input counts matched the server tokenizer; all output
counts matched actual sampled IDs, including EOS. No character estimates were
used. Thinking is disabled; a separate reasoning-token count is unavailable,
not inferred as zero.

**Observed semantic limitation:** the B5b model incorrectly marked office-paint
evidence `e` as sufficient support for protocol authorization `assoc`. This is
a real model error preserved in the receipt. A successful transport/schema/
repair execution is not evidence of support-inference competence. No accuracy
score, threshold selection, scientific pilot, or headroom claim follows.

Deployment and
GGUF metadata are in [qwen_local](qwen_local). Full requests/responses are local,
ignored artifacts; tracked receipts contain sanitized accounting and fictional
fixture outputs only.

## Legacy fixtures, resource observations, and readiness

The unchanged five-fixture suite parsed `necessary`, `alternative`,
`conjunction`, and `semantic_bystander`. The last of those needed its existing
schema retry, consuming the fifth call. The suite therefore **FAILED its overall
completion criterion**: `copies` was blocked before dispatch by the five-call
budget. That cap was preserved. A separate two-call `copies` follow-up then
executed the actual model and its one existing retry; both responses used claim
text as `target_id` instead of record IDs. EvoMem rejected both with
`structured_output_invalid`. The legacy suite is **not fully passing**. No
baseline/parser relaxation, fixture rewrite or target-specific prompt tuning
was performed to hide the failure. The follow-up constructs the same projected
`copies` view as `model_smoke.execute`, then calls existing `SupportInference`
and `PointEstimatePolicy` under the separate recorded budget.

Receipts:

- [Final bounded checks](qwen_local/validation-final.json): PASS.
- [Original five-call legacy phase](qwen_local/existing-fixtures.json): FAILED
  overall, four parsed fixtures, fifth blocked before dispatch.
- [Isolated copies follow-up](qwen_local/copies-followup.json): FAIL after two
  actual generations; incorrect target IDs.
- [Independent token accounting](qwen_local/token-accounting.json): every input
  count matches the pinned Hugging Face tokenizer; every output count matches
  raw sampled IDs and those IDs decode to the returned native content.
- [Measured process memory](qwen_local/memory.json): maximum resident set
  **8,133,689,344 bytes (7.58 GiB)** via Darwin `getrusage(RUSAGE_CHILDREN)`,
  including model loading and the validation runs. This is process RSS, not
  total system memory or a Metal allocation estimate. A simple `ps` inspection
  was unavailable in the execution sandbox. CPU inference ran within the
  observed 16 GB hardware capacity.

Across all attempts, including the two unsuccessful adapter protocols and the
legacy follow-up: **24 actual generations, 14,106 input tokens, 4,266 output
tokens**. The final deployment's runs account for 12 generations (five bounded
checks, five calls in the original suite, two isolated copies calls). The
previous two protocols account for the other 12. No calls or failed usage were
discarded from the accounting record. Tokenizer auditing itself performs no
inference.

The final bounded check's latencies are client `time.perf_counter` durations.
The legacy phase used 180.192 s across five calls; the copies follow-up used
88.348 s across two calls. Internal llama.cpp timing counters sometimes diverged
substantially from client durations during the second protocol attempt; both
are retained in the accounting receipt. Their cause was not established, so
these observations must not be used as a controlled throughput benchmark.
The process elapsed-time field includes idle time and is not generation latency.

The temporary MLX probe environment and abandoned download cache were removed.
The standalone llama.cpp runtime and verified GGUF remain installed outside the
repository. The server was restarted after collecting peak memory and is
configured at `http://127.0.0.1:8087`; the launcher reproduces that deployment.
It is not installed as a system startup service.

Validation of the final code: **147 pytest tests passed**, `ruff check .` passed,
and `mypy src tests scripts/start_qwen_local.py` passed (36 checked files).
No human annotation file, research question, G1 method or scientific pilot was
changed/run. Runtime and weights are excluded from Git; only code, configuration,
provenance and small engineering receipts are committed.

**R0 decision:** the specific Qwen blocker “tokenizer only, no actual local LLM”
is **cleared**. Actual Qwen generation is connected to the existing adapter,
and tiny B5b, B8 and B10 execute against it with exact usage and a demonstrated
pre-inference call-budget stop. This does **not** clear broader scientific or
support-inference quality readiness: the legacy copies failure and false
bystander support remain explicitly unresolved.

## Primary sources

- [Official pinned Qwen model](https://huggingface.co/Qwen/Qwen3.5-9B/tree/c202236235762e1c871ad0ccb60c8ee5ba337b9a).
- [Pinned conversion card](https://huggingface.co/bartowski/Qwen_Qwen3.5-9B-GGUF/blob/182be2fd6c7bc44887d88a91cb03ff009cc9f549/README.md).
- [Official llama.cpp b9222 release](https://github.com/ggml-org/llama.cpp/releases/tag/b9222).
- [Pinned server API documentation](https://github.com/ggml-org/llama.cpp/blob/b9222/tools/server/README.md).
- [Official MLX-LM project](https://github.com/ml-explore/mlx-lm).

The server parser, rather than the inconsistent README example, defines the
wire format: [b9222 response-format handling](https://github.com/ggml-org/llama.cpp/blob/b9222/tools/server/server-common.cpp#L945).
