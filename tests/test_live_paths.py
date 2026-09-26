"""Offline boundary tests for opt-in validation, regeneration and readout."""

import json
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

import pytest

from evomem.cost import Budget, Ledger
from evomem.experiment.live_support import environment, manifest, remaining
from evomem.experiment.live_validation import provider, provider_checks
from evomem.experiment.observable_fixtures import nonce_view, support_view
from evomem.fixtures import fixture
from evomem.model import InformationAccess, Status
from evomem.model_replay import Derivation, ModelCachedReplay, ModelDeriver
from evomem.models.client import (
    ModelIdentity,
    ModelRequest,
    ModelResponse,
    parse_response,
)
from evomem.models.execution import ModelExecutor
from evomem.models.inference import (
    FrozenInference,
    PointEstimatePolicy,
    parse_supports,
    request_for,
)
from evomem.policies import Baseline, RecordedInference
from evomem.readout import (
    ModelReadout,
    ReadoutProbe,
    ReadoutResult,
    StructuredReadout,
    assess_readout,
)
from evomem.simulation import run

IDENTITY = ModelIdentity("anthropic", "claude-sonnet-5", "claude-sonnet-5", "offline")


@dataclass
class ScriptClient:
    identity: ModelIdentity = IDENTITY
    requests: list[ModelRequest] = field(default_factory=list)
    fail_on: int | None = None

    def preflight(self, request: ModelRequest) -> None:
        pass

    def generate(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        if self.fail_on == len(self.requests):
            text = "malformed"
        elif request.schema_version == "basic-v1":
            text = '{"ok":true}'
        elif request.schema_version.startswith("point-support"):
            raw = json.loads(request.user)
            text = json.dumps(
                {
                    "assessments": [
                        {"target_id": r["id"], "decision": "unknown", "groups": []}
                        for r in raw["records"]
                        if r["kind"] != "source"
                    ]
                }
            )
        elif request.schema_version.startswith("query-audit"):
            text = '{"verdict":"contradicted","answer":"K29","evidence_ids":["s"]}'
        elif request.schema_version.startswith("readout"):
            text = '{"answer":"K29","cited_ids":["s"]}'
        else:
            raw = json.loads(request.user.split("\nDependency validity:")[0])
            deps = raw["dependencies"]
            text = json.dumps(
                {
                    "content": deps[0]["content"] if deps else None,
                    "cited_ids": [deps[0]["memory_id"]] if deps else [],
                }
            )
        return ModelResponse(
            text,
            self.identity,
            "offline-id",
            12,
            0,
            6,
            None,
            1,
            "end_turn",
            {"input_tokens": 12, "output_tokens": 6},
            {},
        )


def replay_fixture() -> tuple[ModelCachedReplay, ScriptClient, Ledger]:
    client = ScriptClient()
    ledger = Ledger(Budget())
    return (
        ModelCachedReplay(ModelDeriver(ModelExecutor(client, ledger))),
        client,
        ledger,
    )


SPECS = (
    Derivation("t", "Restate Zorvia protocol.", ("s",), "v1"),
    Derivation("v", "Restate Tovren protocol.", ("u",), "v1"),
)


def test_b8_reuses_unaffected_and_regenerates_changed_content() -> None:
    replay, client, ledger = replay_fixture()
    first = replay.update(nonce_view(), SPECS)
    second = replay.update(nonce_view("K29"), SPECS)
    assert first.cache_misses == 2 and second.cache_hits == 1
    assert second.regenerated_nodes == ("t",) and len(client.requests) == 3
    assert next(m for m in second.items if m.memory_id == "t").content.endswith("K29.")
    assert ledger.totals()["model_calls"] == 3 and ledger.totals()["replay_steps"] == 3
    assert nonce_view().items[1].content.endswith("K17.")


@pytest.mark.parametrize(
    "change", ["model", "prompt", "schema", "generation", "dependency_version", "input"]
)
def test_replay_cache_material_identity(change: str) -> None:
    replay, client, _ = replay_fixture()
    view = nonce_view()
    specs: tuple[Derivation, ...] = SPECS
    replay.update(view, specs)
    if change == "model":
        client.identity = replace(client.identity, version="new")
    if change == "prompt":
        replay.deriver.system += " extra instruction"
    if change == "schema":
        replay.deriver.schema_version = "derivation-development-v2"
    if change == "generation":
        replay.deriver.max_output_tokens = 200
    if change == "dependency_version":
        specs = tuple(replace(s, version="v2") for s in specs)
    if change == "input":
        view = nonce_view("K31")
    result = replay.update(view, specs)
    assert result.cache_misses == (1 if change == "input" else 2)


def test_replay_transitive_change_and_cold_full_recompute() -> None:
    replay, client, _ = replay_fixture()
    specs = (SPECS[0], replace(SPECS[1], dependencies=("t",)))
    replay.update(nonce_view(), specs)
    changed = replay.update(nonce_view("K29"), specs)
    assert changed.regenerated_nodes == ("t", "v")
    full = replay.update(nonce_view("K29"), specs, reuse=False)
    assert (
        full.items == changed.items
        and full.cache_misses == 2
        and len(client.requests) == 6
    )


def test_replay_atomic_budget_or_validation_failure() -> None:
    for failure in ["budget", "parse"]:
        replay, client, ledger = replay_fixture()
        if failure == "budget":
            ledger.budget = Budget(max_model_calls=1)
        else:
            client.fail_on = 2
        original = nonce_view()
        result = replay.update(original, SPECS)
        assert result.items == original.items and not replay.cache
        assert result.completion == (
            "budget_exhausted" if failure == "budget" else "model_failed"
        )
        assert ledger.totals()["model_calls"] == (1 if failure == "budget" else 2)


def test_replay_cycles_rejected_before_dispatch() -> None:
    replay, client, _ = replay_fixture()
    with pytest.raises(ValueError, match="Cyclic"):
        replay.update(
            nonce_view(),
            (
                replace(SPECS[0], dependencies=("v",)),
                replace(SPECS[1], dependencies=("t",)),
            ),
        )
    assert not client.requests


def test_expired_dependency_invalidates_cache_and_is_not_generation_evidence() -> None:
    replay, client, _ = replay_fixture()
    v = nonce_view()
    replay.update(v, SPECS)
    expired = replace(
        v,
        items=tuple(
            replace(m, valid_until=1) if m.memory_id == "s" else m for m in v.items
        ),
    )
    result = replay.update(expired, SPECS)
    assert result.cache_misses == 1
    assert (
        next(m for m in result.items if m.memory_id == "t").status == Status.QUARANTINED
    )
    assert "Project Zorvia uses protocol K17." not in client.requests[-1].user


def test_readout_cannot_mask_state_failure() -> None:
    good_answer = ReadoutResult("K29", ("s",), ("s",))
    scored = assess_readout(
        good_answer,
        expected_answer="K29",
        memory_state_correct=False,
        required_retrieval=frozenset({"s"}),
    )
    assert (
        scored.answer_correct
        and scored.retrieval_correct
        and not scored.memory_state_correct
    )
    wrong = assess_readout(
        replace(good_answer, answer="K17"),
        expected_answer="K29",
        memory_state_correct=True,
        required_retrieval=frozenset({"missing"}),
    )
    assert (
        wrong.memory_state_correct
        and not wrong.answer_correct
        and not wrong.retrieval_correct
    )


def test_failed_abstention_is_not_correct_answer() -> None:
    result = ReadoutResult(None, (), (), "model_failed")
    score = assess_readout(
        result, expected_answer=None, memory_state_correct=None, required_retrieval=None
    )
    assert not score.answer_correct and score.memory_state_correct is None


def test_structured_readout_preserves_current_and_historical_views() -> None:
    scenario, gold = fixture("correction")
    trace = run(
        scenario,
        Baseline("B2", RecordedInference()),
        InformationAccess(),
        Ledger(Budget()),
    )
    reader = StructuredReadout(trace)
    for p in gold.probes:
        assert (
            reader.answer(
                ReadoutProbe(p.item_id, p.checkpoint, time_view=p.view, as_of=p.as_of)
            ).answer
            == p.expected
        )


def test_model_readout_is_label_free_and_does_not_mutate() -> None:
    client = ScriptClient()
    v = nonce_view("K29")
    reader = ModelReadout(ModelExecutor(client, Ledger(Budget())), v)
    answer = reader.answer(ReadoutProbe("t", 1, "Which protocol does Zorvia use?"))
    assert answer.answer == "K29" and v.items[1].content.endswith("K17.")
    assert set(json.loads(client.requests[0].user)) == {
        "records",
        "target_id",
        "question",
    }
    with pytest.raises(ValueError, match="current"):
        reader.answer(ReadoutProbe("t", 1, time_view="historical_then", as_of=0))


def test_nonce_counterfactual_replaces_evidence_not_labels() -> None:
    a, b = nonce_view("K17"), nonce_view("K29")
    assert a.items[0].content != b.items[0].content
    assert a.items[1:] == b.items[1:]
    assert "expected" not in request_for(a).user
    assert "expected" not in request_for(support_view()).user


def test_provider_adapters_share_support_schema() -> None:
    v = support_view()
    text = json.dumps(
        {
            "assessments": [
                {"target_id": m.memory_id, "decision": "unknown", "groups": []}
                for m in v.items
                if m.kind != "source"
            ]
        }
    )
    claude = parse_response(
        {
            "model": IDENTITY.model,
            "content": [{"type": "text", "text": text}],
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 4, "output_tokens": 8},
        },
        IDENTITY,
        1,
    )
    qwen_id = ModelIdentity("vllm", "Qwen/Qwen3.5-9B", "pinned", "offline")
    qwen = parse_response(
        {
            "model": qwen_id.model,
            "choices": [{"message": {"content": text}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 4, "completion_tokens": 8},
        },
        qwen_id,
        1,
    )
    assert parse_supports(claude.text, v) == parse_supports(qwen.text, v)


def test_point_confidence_is_discarded_after_fixed_selection() -> None:
    v = nonce_view()
    from evomem.model import Support

    proposal = Support("j", "t", ("s",), scope="lab")
    decisions = []
    for confidence in [0.71, 0.99]:
        ledger = Ledger(
            Budget(max_model_calls=0, max_verification_calls=0, max_replay_steps=0)
        )
        decisions.append(
            PointEstimatePolicy(
                FrozenInference(((proposal, confidence),)), "B5b", 0.7
            ).repair(v, ledger)
        )
        assert not ledger.events
    assert decisions[0] == decisions[1]


def test_provider_validation_complete_offline(tmp_path: Path) -> None:
    client = ScriptClient()
    result = provider_checks(tmp_path / "offline", client)
    assert result["status"] == "PASS", result["details"]
    assert len(client.requests) == 7
    assert result["details"]["call_stop"] and result["details"]["token_stop"]
    assert (
        result["usage"]["verification_calls"] == 2
        and result["usage"]["replay_steps"] == 2
    )
    assert result["usage"]["model_calls"] == 7
    assert len(result["attempts"]) == 9  # seven calls, one cache hit, one rejection
    assert "Return JSON" not in json.dumps(result)  # hashes, no prompt/source text


def test_live_gate_default_never_dispatches(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("EVOMEM_RUN_LIVE_TESTS", raising=False)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "never-used-offline-dummy")
    result = provider(tmp_path / "skip", "anthropic")
    assert result["status"] == "SKIPPED" and result["usage"]["model_calls"] == 0
    assert "never-used-offline-dummy" not in json.dumps(result)


def test_manifest_fields_and_remaining_budget(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HF_TOKEN", "never-print")
    import subprocess

    original = subprocess.check_output

    def command(args: list[str], **kwargs: Any) -> Any:
        if args[:3] == ["git", "status", "--porcelain"]:
            return " M changed.py"
        return original(args, **kwargs)

    monkeypatch.setattr(subprocess, "check_output", command)
    ledger = Ledger(Budget(max_model_calls=3, max_total_tokens=30))
    value = manifest(IDENTITY, ledger, "PASS", [], {})
    assert value["dirty"] is True
    assert {
        "git_commit",
        "timestamp",
        "provider",
        "model",
        "model_version",
        "runtime",
        "environment",
        "prompt_hashes",
        "generation_config",
        "usage",
        "budget",
        "cache_stats",
        "latency_ms",
        "status",
    } <= set(value)
    assert remaining(ledger)["max_total_tokens"] == 30
    assert environment()["credentials"]["HF_TOKEN"] == "configured"
    assert "never-print" not in json.dumps(value)


def test_qwen_token_id_shapes_and_not_character_estimates() -> None:
    from evomem.models.tokenization import token_ids

    assert (
        token_ids({"input_ids": [1, 200, 3]}) == token_ids([1, 200, 3]) == (1, 200, 3)
    )
    for bad in ["text", {"input_ids": [[1, 2]]}, [True], [-1], None]:
        with pytest.raises(ValueError):
            token_ids(bad)


def test_embedding_preflight_cap_blocks_backend(tmp_path: Path) -> None:
    from evomem.models.embeddings import EmbeddingCache

    class Backend:
        identity = "offline"
        calls = 0

        def encode(self, text: str) -> tuple[float, ...]:
            self.calls += 1
            return (1.0, 0.0)

    from evomem.cost import BudgetExceededError

    backend = Backend()
    ledger = Ledger(Budget(max_embedding_calls=1))
    cache = EmbeddingCache(backend, tmp_path)
    cache.vector("a", ledger, 1)
    with pytest.raises(BudgetExceededError):
        cache.vector("b", ledger, 1)
    cache.vector("a", ledger, 1)
    assert backend.calls == 1 and ledger.totals()["cache_hits"] == 1


def test_future_replay_target_rejected_before_dispatch() -> None:
    replay, client, _ = replay_fixture()
    v = nonce_view()
    v = replace(
        v,
        items=tuple(
            replace(m, created_at_checkpoint=9) if m.memory_id == "t" else m
            for m in v.items
        ),
    )
    with pytest.raises(ValueError):
        replay.update(v, SPECS)
    assert not client.requests


@pytest.mark.parametrize("code", [429, 500])
def test_http_failure_is_charged_once_no_free_retry(
    code: int, monkeypatch: pytest.MonkeyPatch
) -> None:
    import urllib.error
    import urllib.request

    from evomem.models.client import AnthropicClient, HTTPTransport, ModelCallError
    from evomem.models.inference import SupportInference

    monkeypatch.setenv("ANTHROPIC_API_KEY", "offline-dummy")
    calls = []

    def fail(*args: Any, **kwargs: Any) -> Any:
        calls.append(1)
        raise urllib.error.HTTPError("https://example.invalid", code, "error", {}, None)  # type: ignore[arg-type]

    monkeypatch.setattr(urllib.request, "urlopen", fail)
    ledger = Ledger(Budget())
    executor = ModelExecutor(AnthropicClient(HTTPTransport()), ledger)
    with pytest.raises(ModelCallError):
        SupportInference(executor).infer(support_view())
    assert calls == [1] and ledger.totals()["model_calls"] == 1
    assert ledger.totals()["input_tokens"] is None and executor.halted


def test_semantic_threshold_is_not_adapted_on_smoke_cases(tmp_path: Path) -> None:
    from evomem.models.embeddings import EmbeddingCache, SemanticClosure

    class Backend:
        identity = "offline-threshold-isolation"

        def encode(self, text: str) -> tuple[float, ...]:
            return (1.0, 0.0)

    policy = SemanticClosure(EmbeddingCache(Backend(), tmp_path), threshold=0.7)
    for value in ["K17", "K29"]:
        policy.repair(nonce_view(value), Ledger(Budget()))
        assert policy.threshold == 0.7


def test_replay_scope_and_declared_clock_are_cache_identity() -> None:
    replay, _, _ = replay_fixture()
    v = nonce_view()
    replay.update(v, SPECS)
    scoped = replace(
        v,
        items=tuple(
            replace(m, scope="other") if m.memory_id == "t" else m for m in v.items
        ),
    )
    assert replay.update(scoped, SPECS).cache_misses == 1
    clock_specs = tuple(replace(s, clock_sensitive=True) for s in SPECS)
    replay.update(v, clock_specs)
    assert replay.update(replace(v, checkpoint=2), clock_specs).cache_misses == 2


def test_transport_request_id_preferred_to_message_id() -> None:
    raw = {
        "model": IDENTITY.model,
        "id": "message-id",
        "_transport_request_id": "http-request-id",
        "content": [{"type": "text", "text": "{}"}],
        "usage": {"input_tokens": 1, "output_tokens": 2},
    }
    assert parse_response(raw, IDENTITY, 0).request_id == "http-request-id"
