# Live environment and model verification — 2026-09-26

## Measured host

macOS 26.6.2, arm64, MacBook Air Mac16,12, Apple M4; 10 CPU cores (4 performance, 6 efficiency), 10-core integrated GPU, Metal supported, 16 GB unified memory. Initial free disk approximately 296 GiB. Hardware was inspected with system_profiler after the prior phase's failed sysctl probe; serial number/UUID fields are neither logged nor committed. Python 3.11.15. Torch reports CUDA unavailable, MPS built but MPS unavailable in this process; hardware Metal support alone does not establish usable acceleration here. The project environment initially had no torch, transformers, sentence-transformers or vLLM.

An isolated sibling `g1-live-env` was created and populated with sentence-transformers 6.1.0, torch 2.14.0, transformers 5.17.0 and dependencies. Exact installed versions are archived under `research/resources/runtime/`. The project default environment and dependency list remain lightweight. Model files are in a separate `g1-model-cache`, not Git. Anonymous public downloads were used with implicit Hugging Face token lookup disabled. Only MiniLM weights and Qwen tokenizer/config files were downloaded.

Credential presence: ANTHROPIC_API_KEY missing; HF_TOKEN missing; VLLM_BASE_URL missing; QWEN_DEPLOYMENT_MANIFEST missing. No credential values were printed, sought in unrelated files or committed.

## Current official checks

| Provider/model | Identifier/revision | Verified sources and scope |
|---|---|---|
| Anthropic | claude-sonnet-5 | [Official model overview](https://platform.claude.com/docs/en/models/sonnet-5/overview), [structured output](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), [usage/cache semantics](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), checked 2026-09-26 |
| Qwen | Qwen/Qwen3.5-9B, c202236235762e1c871ad0ccb60c8ee5ba337b9a | [Official model card](https://huggingface.co/Qwen/Qwen3.5-9B) and repository API/current revision, checked 2026-09-26; tokenizer and template from that same commit |
| Embedding | sentence-transformers/all-MiniLM-L6-v2, 1110a243fdf4706b3f48f1d95db1a4f5529b4d41 | [Official repository](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), repository API and actual pinned files, checked 2026-09-26 |

Claude is listed active; this does not establish account entitlement. Native JSON schema output is supported; numeric constraints are validated locally because the wire schema does not support them. Omit nondefault sampling parameters; adaptive thinking is default. Usage input categories distinguish uncached, cache creation and cache read; total input adds all three. Reasoning is not guessed when absent. Transport request-id is preserved when available, with body message ID as an explicitly documented fallback.

Qwen has native context 262,144. Use the pinned repository chat_template.jinja, not a hand-written imitation. The card documents vLLM serving and an enable_thinking chat-template option; structured outputs still require backend parsing/validation and cannot be assumed to fix truncation/refusal. The tokenizer smoke explicitly uses enable_thinking=False and add_generation_prompt=True. This is tokenizer validation only: the existing generation adapter uses its declared backend defaults, so these 23 tokens must not be substituted for a different server request's usage. Greedy temperature zero remains an engineering candidate, not a claim to follow every model-card sampling recommendation.

## Qwen deployment decision

Selected model: unchanged Qwen3.5-9B. Selected backend candidate: vLLM 0.30.0, not installed or executed. No configured alternative server is available. The pinned official model.safetensors.index.json reports total_size=19,306,216,416 bytes (about 18.0 GiB) for weights alone, exceeding practical resident capacity on this 16 GB host before OS, runtime and KV cache. We did not intentionally trigger memory exhaustion or download multi-GB weights merely to confirm this bound. This is a capacity assessment, not a measured load failure or claim that every quantized deployment is impossible.

Current [vLLM installation documentation](https://docs.vllm.ai/en/latest/getting_started/installation/) lists Apple support, including the [vLLM-Metal plugin](https://github.com/vllm-project/vllm-metal). Therefore “vLLM cannot run on Macs” would be false. The plugin uses a distinct MLX-based runtime; a quantized conversion plus plugin is a material deployment change requiring its own revision, quantization, template, schema and usage validation. No such change was made silently. A larger external GPU server serving the same pinned weights is the preferred way to preserve the current candidate, but none was configured or provisioned. No paid GPU service was launched.

The prior vLLM package pin is not proof of Qwen compatibility; the card's serving guidance and exact installed server must be reconciled on a real deployment. Qwen generation, actual tokenizer/server usage agreement, peak model memory and generation latency remain SKIPPED. Tokenizer-only execution now passes and cannot substitute for these gates.
