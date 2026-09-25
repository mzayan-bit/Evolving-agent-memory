# Real resource enforcement — development implementation, 2026-09-26

Implemented in `src/evomem/models/client.py`, `execution.py` and `cost.py`. **Offline validated; live validation SKIPPED. Not yet pilot certified.** No tokens are estimated from character counts. No local tokenizer fallback is claimed: missing returned input/output counts stop further dispatch.

## Transaction semantics

Use one serialized ModelExecutor per shared trajectory Ledger. Before dispatch, probe a copy of the ledger with one model call, the declared input reservation, maximum output tokens, and the applicable verifier/replay counters. Reject before network access if any cumulative input, output, total, calls, verifier or replay cap cannot accommodate this reservation. Configuration validation also occurs before dispatch. The input reservation is a declared conservative allowance, **not an exact tokenizer measurement or guaranteed bound**. The smoke default is 8,192 input and 1,024 output tokens per request. Structured-output overhead is part of provider usage.

After dispatch, replace the reservation with actual usage: unused reservation becomes available. One successful HTTP attempt is one model call; verification and replay flags are overlapping purpose counters, not additional physical calls. A failed transport attempt is still counted, with unknown tokens; no claim that the provider necessarily billed it. Record actual overrun even if it exceeds the ledger cap. Halt the executor after an overrun or unknown input/output usage; do not conceal the one-call overshoot. A finite token cap rejects unknown reconciliation. Without a token cap the response may be inspected, but the executor still halts before another call. Invalid provider counters retain the raw envelope and mark usage unknown. Invalid subset metadata fails closed; the audit retains the returned event.

The implementation is synchronous, with an executor-local lock. Concurrent executors sharing one ledger and cross-process shared cache writes are unsupported. Do not use concurrency to bypass reservation. Per-revision credit release is not implemented; existing cumulative caps must not be presented as the candidate two-credit-per-revision schedule. Pilot integration must choose and freeze either cumulative caps or add and validate scheduled release first.

## Usage semantics

Claude input = uncached input + cache-read input + cache-creation input. Cached input is the cache-read subset; cache writes remain separately available in raw usage. Output includes any provider-billed reasoning; reasoning count stays null if absent. vLLM uses prompt/completion usage and reported cached/reasoning details; missing details remain null. Reasoning is a subset of output, never added twice. Returned model identity must match the requested model. Raw response, usage, request ID, latency and configured deployment identity are retained in attempts/cache.

Counters distinguish model calls, input/cache/output tokens, verification, replay, retrieval, embedding operations and dependency inspections. Embedding calls currently mean one text encode; a content hit costs zero new embedding calls. No embedding-token count or local dollar cost is invented. Local encode latency and identity are logged. B8 dependency_checks counts inspected rule candidates in ancestor expansion, including cache hits; this is an operation proxy, not FLOPs. Full end-to-end trajectory latency includes nested operation latency: **do not sum nested latency and trajectory-runtime as elapsed time**. Report runtime and phase latencies separately.

## Failures and retry policy

| Event | Action |
|---|---|
| Missing configuration / unsupported sampling settings | Preflight rejection, zero physical calls |
| Timeout/network error | One attempted call, unknown usage, halt; zero automatic retries |
| HTTP 429 rate/quota, 5xx transient, authentication/permission, context/invalid request | Sanitized error category, attempted call, unknown usage, halt; zero automatic retries |
| Malformed provider envelope / unexpected model | Preserve available raw envelope, unknown usage, halt |
| Refusal / truncated generation | Charge returned usage; semantic layer fails without retry or fallback |
| Valid envelope but malformed support JSON | Record raw response and failed validation; at most one fixed schema retry, separately reserved and charged |
| Bad query audit JSON / stale citation | Charge returned usage, return model_failed; zero retries |
| Budget cannot accommodate retry | No dispatch; return budget_exhausted |

No silent model substitution, SDK retry loop, external retrieval or hidden calls. Fixture smoke caps at five dispatches total, including schema retries. An all-success run attempts a sixth reservation to demonstrate pre-dispatch blocking, never a sixth network request. A transport error prevents this check and is a failed smoke, not a pass.

## Cache and fairness

Immutable create-only files keyed by SHA-256 of provider, model/version/deployment, exact prompts, generation parameters, schema/version and reservation configuration. Payload checksum detects accidental alteration; this is not a signed trust boundary. Cache hits log original usage separately from zero newly consumed model tokens. Refused/truncated/unknown-usage responses are not cached. A syntactically bad support result may be cached as a raw successful generation; it is always revalidated, and a retry uses a distinct fixed prompt with cache disabled. Never silently treat a cached malformed result as valid.

For policy isolation, generate a shared frozen proposal bundle once, attach its original construction ledger to every arm's accounting report, and compare deterministic decisions on that identical bundle. End-to-end runs use separate cold namespaces or explicitly account for original construction costs. Later arms must not receive free warm initialization unavailable to earlier arms. Query-only auditing disables response reuse by default to expose repeated verification costs. No current study runner automates a full multi-arm live budget experiment; this remains a freeze gate.

## Post-hoc money

`research/resources/pricing/anthropic-2026-09-26.json` is a dated standard-text USD snapshot from the official Sonnet 5 page. `models/pricing.py` reprices raw usage outside policy code. Cache-write TTL must be known when writes occur; otherwise cost is unknown. No batch, tool, tax or negotiated discounts are assumed. Local Qwen/embedding hardware costs are unknown, not free. Raw counts remain primary. The two live smoke manifests currently report SKIPPED and zero calls/tokens.
