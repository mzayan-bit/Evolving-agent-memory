"""Explicitly opt-in engineering checks. No evaluation data and at most 8 API calls."""

import argparse
import importlib
import json
import os
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from time import perf_counter
from typing import Any

from evomem.comparators import QueryAudit
from evomem.cost import Budget, BudgetExceededError, CostEvent, Ledger
from evomem.experiment.live_support import digest, manifest, skipped, write_manifest
from evomem.experiment.model_smoke import QWEN_REVISION, configured_client
from evomem.experiment.observable_fixtures import nonce_view, support_view
from evomem.model_replay import Derivation, ModelCachedReplay, ModelDeriver
from evomem.models.client import (
    AnthropicClient,
    ModelClient,
    ModelIdentity,
    ModelRequest,
    QwenVLLMClient,
    Transport,
)
from evomem.models.embeddings import (
    MODEL,
    REVISION,
    EmbeddingCache,
    MiniLM,
    SemanticClosure,
    cosine,
)
from evomem.models.execution import ModelExecutor
from evomem.models.inference import (
    FrozenInference,
    PointEstimatePolicy,
    SupportInference,
)
from evomem.models.pricing import estimate_usd
from evomem.models.tokenization import token_ids
from evomem.readout import ModelReadout, ReadoutProbe


@dataclass
class CountingTransport:
    inner: Transport
    dispatched: int = 0

    def post(
        self, url: str, headers: dict[str, str], body: dict[str, Any], timeout: float
    ) -> dict[str, Any]:
        self.dispatched += 1
        return self.inner.post(url, headers, body, timeout)


@dataclass
class CountingEmbedding:
    model: MiniLM
    calls: int = 0

    identity: str = field(init=False)

    def __post_init__(self) -> None:
        self.identity = self.model.identity

    def encode(self, text: str) -> tuple[float, ...]:
        self.calls += 1
        return self.model.encode(text)


def enabled() -> bool:
    return os.environ.get("EVOMEM_RUN_LIVE_TESTS") == "1"


def embedding(output: Path) -> dict[str, Any]:
    if not enabled():
        return skipped(output, "EVOMEM_RUN_LIVE_TESTS is not 1")
    ledger = Ledger(Budget())
    start = perf_counter()
    details: dict[str, Any] = {}
    identity = ModelIdentity("local", MODEL, REVISION, "not loaded")
    status = "FAIL"
    try:
        model = MiniLM()
        identity = replace(identity, deployment=model.identity)
        details["load_latency_ms"] = (perf_counter() - start) * 1000
        cache = EmbeddingCache(model, output.parent / (output.name + "-vectors"))
        texts = (
            "Project Zorvia uses protocol K17.",
            "Zorvia operates with K17.",
            "Project Tovren paints its roof violet.",
        )
        first = cache.vector(texts[0], ledger, 1)
        cached = cache.vector(texts[0], ledger, 1)
        direct = model.encode(texts[0])
        ledger.charge(CostEvent("determinism", "embedding-smoke", 1, embedding_calls=1))
        batch = model.encode_batch(texts)
        ledger.charge(CostEvent("batch", "embedding-smoke", 1, embedding_calls=1))
        assert len(first) == 384 and first == cached and first == direct
        assert len(batch) == 3 and all(len(v) == 384 for v in batch)
        assert abs(sum(v * v for v in first) - 1) < 1e-5
        assert max(abs(a - b) for a, b in zip(first, batch[0], strict=True)) < 1e-5
        assert abs(cosine(first, first) - 1) < 1e-5
        SemanticClosure(cache, threshold=0.7).repair(nonce_view(), ledger)
        details.update(
            dimension=len(first),
            normalized=True,
            repeat_exact=True,
            batch_size=3,
            batch_matches_single=True,
            threshold=0.7,
            threshold_provenance="Existing untuned engineering default; unchanged",
            embedding_items=sum(e.embedding_calls for e in ledger.events) + 2,
            vector_hash=digest(first),
        )
        bounded = Ledger(Budget(max_embedding_calls=1))
        counted = CountingEmbedding(model)
        limited_cache = EmbeddingCache(
            counted, output.parent / (output.name + "-bounded")
        )
        limited_cache.vector("Nonce permit R41.", bounded, 1)
        try:
            limited_cache.vector("Nonce permit R42.", bounded, 1)
            raise AssertionError("Embedding cap did not stop dispatch")
        except BudgetExceededError:
            assert counted.calls == 1
        details["embedding_budget_stop"] = {
            "cap": 1,
            "actual_encodes": counted.calls,
            "second_encode_blocked": True,
        }
        for event in bounded.events:
            ledger.events.append(
                replace(event, operation_id="bounded:" + event.operation_id)
            )
        details["embedding_items"] = sum(e.embedding_calls for e in ledger.events) + 2
        status = "PASS"
    except Exception as error:
        details["error_type"] = type(error).__name__
        details["error"] = str(error)[:400]
    ledger.charge(
        CostEvent(
            "elapsed", "runtime", 1, wall_latency_ms=(perf_counter() - start) * 1000
        )
    )
    result = manifest(identity, ledger, status, [], details)
    write_manifest(output, result)
    return result


def tokenizer(output: Path) -> dict[str, Any]:
    if not enabled():
        return skipped(output, "EVOMEM_RUN_LIVE_TESTS is not 1")
    details: dict[str, Any] = {}
    identity = ModelIdentity(
        "local-tokenizer", "Qwen/Qwen3.5-9B", QWEN_REVISION, "tokenizer-only"
    )
    ledger = Ledger(Budget())
    start = perf_counter()
    status = "FAIL"
    try:
        module = importlib.import_module("transformers")
        tok = module.AutoTokenizer.from_pretrained(
            identity.model,
            revision=QWEN_REVISION,
            local_files_only=True,
            trust_remote_code=False,
        )
        messages = [{"role": "user", "content": "Project Zorvia uses protocol K17."}]
        rendered = tok.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True, enable_thinking=False
        )
        ids = tok.apply_chat_template(
            messages, tokenize=True, add_generation_prompt=True, enable_thinking=False
        )
        ids = token_ids(ids)
        assert ids == token_ids(tok.encode(rendered, add_special_tokens=False))
        assert len(ids) > 0
        details.update(
            token_count=len(ids),
            token_ids_hash=digest(ids),
            template_hash=digest(tok.chat_template),
            messages_hash=digest(messages),
            enable_thinking=False,
            add_generation_prompt=True,
            usage_source="exact_pinned_tokenizer_not_generation_usage",
            transformers=module.__version__,
            model_weights_loaded=False,
        )
        status = "PASS"
    except Exception as error:
        details.update(error_type=type(error).__name__, error=str(error)[:400])
    ledger.charge(
        CostEvent(
            "elapsed", "runtime", 0, wall_latency_ms=(perf_counter() - start) * 1000
        )
    )
    result = manifest(identity, ledger, status, [], details)
    write_manifest(output, result)
    return result


def provider(output: Path, family: str) -> dict[str, Any]:
    if not enabled() or os.environ.get("EVOMEM_RUN_PAID_TESTS") != "1":
        return skipped(
            output, "Requires EVOMEM_RUN_LIVE_TESTS=1 and EVOMEM_RUN_PAID_TESTS=1"
        )
    try:
        client, reason = configured_client(family)
    except (ValueError, OSError, KeyError, TypeError) as error:
        result = manifest(
            None,
            Ledger(Budget()),
            "FAIL",
            [],
            {
                "reason": "Invalid deployment configuration",
                "error_type": type(error).__name__,
            },
        )
        write_manifest(output, result)
        return result
    if client is None:
        intended = (
            ModelIdentity(
                "anthropic",
                "claude-sonnet-5",
                "claude-sonnet-5",
                "native-messages-2023-06-01",
            )
            if family == "anthropic"
            else ModelIdentity("vllm", "Qwen/Qwen3.5-9B", QWEN_REVISION, "unavailable")
        )
        return skipped(output, reason or "No configured client", intended)
    return provider_checks(output, client)


def provider_checks(output: Path, client: ModelClient) -> dict[str, Any]:
    """Called by gated runner; injectable client permits offline integration tests."""
    counter = None
    if isinstance(client, (AnthropicClient, QwenVLLMClient)):
        counter = CountingTransport(client.transport)
        client.transport = counter
    basic = Ledger(
        Budget(
            max_model_calls=1,
            max_input_tokens=8192,
            max_output_tokens=256,
            max_total_tokens=8448,
        )
    )
    executor = ModelExecutor(
        client, basic, output.parent / (output.name + "-responses")
    )
    request = ModelRequest(
        "Return JSON only.",
        'Return {"ok":true}.',
        '{"type":"object","properties":{"ok":{"type":"boolean"}},"required":["ok"],"additionalProperties":false}',
        "basic-v1",
        max_output_tokens=256,
    )
    details: dict[str, Any] = {"components": {}, "max_phase_dispatches": 8}
    status = "FAIL"
    try:
        basic_response = executor.generate(request, 0, "basic")
        assert basic_response.finish_reason in {"stop", "end_turn"} and json.loads(
            basic_response.text
        ) == {"ok": True}
        assert (
            basic_response.input_tokens is not None
            and basic_response.output_tokens is not None
        )
        assert basic_response.request_id
        assert executor.generate(request, 0, "cache-check") == basic_response
        dispatched = counter.dispatched if counter else basic.totals()["model_calls"]
        try:
            executor.generate(request, 0, "call-stop", use_cache=False)
            raise AssertionError("Call budget failed to stop")
        except BudgetExceededError:
            assert (
                counter.dispatched if counter else basic.totals()["model_calls"]
            ) == dispatched
        # A separate zero-token ledger tests token rejection without another dispatch.
        token_executor = ModelExecutor(client, Ledger(Budget(max_input_tokens=0)))
        try:
            token_executor.generate(request, 0, "token-stop", use_cache=False)
            raise AssertionError("Token budget failed to stop")
        except BudgetExceededError:
            assert (
                counter.dispatched if counter else basic.totals()["model_calls"]
            ) == dispatched
        details.update(
            call_stop=True,
            token_stop=True,
            basic_usage=basic.totals(),
            basic_remaining=manifest(client.identity, basic, "PASS", [request], {})[
                "remaining"
            ],
            token_stop_attempts=token_executor.attempts,
        )
        details["components"]["basic"] = "PASS"
        details["components"]["budget_stop"] = "PASS"
        # Explicit second phase: at most seven further calls.
        phase = Ledger(
            Budget(
                max_model_calls=7,
                max_input_tokens=57344,
                max_output_tokens=7168,
                max_total_tokens=64512,
                max_verification_calls=2,
                max_replay_steps=2,
            )
        )
        follow = ModelExecutor(client, phase)
        try:
            v = support_view()
            frozen = FrozenInference(SupportInference(follow, use_cache=False).infer(v))
            for variant in ("B5a", "B5b"):
                PointEstimatePolicy(frozen, variant).repair(v, phase)
            details["components"]["support_inference"] = "PASS"
            # No correctness scores: only schema/proposal execution.
            details["proposal_hash"] = digest(
                [(asdict(s), c) for s, c in frozen.proposals]
            )
            current = nonce_view("K29")
            before = current.items
            audit = QueryAudit(follow)
            for _ in range(2):
                assert audit.query(current, "t").completion == "done"
            assert current.items == before and phase.totals()["verification_calls"] == 2
            details["components"]["query_audit"] = "PASS"
            replay = ModelCachedReplay(ModelDeriver(follow))
            spec = (
                Derivation(
                    "t", "State which protocol Project Zorvia uses.", ("s",), "v1"
                ),
            )
            cold = replay.update(nonce_view(), spec)
            warm = replay.update(nonce_view(), spec)
            changed = replay.update(current, spec)
            assert cold.completion == changed.completion == "done"
            assert warm.cache_hits == 1 and changed.cache_misses == 1
            details["components"]["model_replay"] = "PASS"
            details["replay"] = {
                "cold_regenerated": cold.regenerated_nodes,
                "warm_hits": warm.cache_hits,
                "changed_regenerated": changed.regenerated_nodes,
            }
            answer = ModelReadout(follow, current).answer(
                ReadoutProbe("t", 1, "Which protocol does Zorvia use?")
            )
            assert answer.completion == "done" and current.items == before
            details["components"]["model_readout"] = "PASS"
            status = "PASS"
        finally:
            details["phase_budget"] = asdict(phase.budget)
            details["phase_remaining"] = manifest(
                client.identity, phase, "RECORDED", [], {}
            )["remaining"]
            # Reporting aggregate only; original phase caps remain in details.
            for event in phase.events:
                basic.events.append(
                    replace(event, operation_id="phase2:" + event.operation_id)
                )
            executor.attempts.extend(follow.attempts)
    except Exception as error:
        details.update(error_type=type(error).__name__, error=str(error)[:300])
    if counter:
        details["transport_dispatches"] = counter.dispatched
    requests = []
    for attempt in executor.attempts:
        raw_request = attempt.get("request")
        if isinstance(raw_request, dict):
            requests.append(ModelRequest(**raw_request))
    original_budget = asdict(basic.budget)
    basic.budget = Budget()  # Report aggregation, not an executable budget extension.
    details["basic_budget"] = original_budget
    details["budget_scope"] = "Two separately enforced phases: 1 plus 7 calls"
    result = manifest(client.identity, basic, status, requests, details, executor)
    # Pricing is post-hoc. Raw provider categories remain in the attempt records.
    prices = json.loads(
        Path("research/resources/pricing/anthropic-2026-09-26.json").read_text()
    )
    from evomem.models.client import ModelResponse

    costs = []
    for attempt in executor.attempts:
        raw = attempt.get("response")
        if isinstance(raw, dict) and client.identity.provider == "anthropic":
            value = dict(raw)
            value.pop("identity")
            costs.append(
                estimate_usd(ModelResponse(identity=client.identity, **value), prices)
            )
    result["derived_usd"] = (
        None
        if not costs
        or any(c is None for c in costs)
        or basic.totals()["input_tokens"] is None
        or basic.totals()["output_tokens"] is None
        else sum(c for c in costs if c is not None)
    )
    result["price_table_version"] = prices["version"]
    local_responses = [a["response"] for a in executor.attempts if "response" in a]
    result["local_responses_sha256"] = digest(local_responses)
    write_manifest(output, result)
    (output / "responses.json").write_text(json.dumps(local_responses, indent=2) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--component",
        choices=["embedding", "tokenizer", "anthropic", "vllm"],
        required=True,
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    value = (
        embedding(args.output)
        if args.component == "embedding"
        else tokenizer(args.output)
        if args.component == "tokenizer"
        else provider(args.output, args.component)
    )
    print(
        json.dumps(
            {
                "component": args.component,
                "status": value["status"],
                "usage": value["usage"],
            }
        )
    )


if __name__ == "__main__":
    main()
