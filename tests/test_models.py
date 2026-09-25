"""Offline engineering contracts; canned responses are not competence evidence."""

import json
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any

import pytest

from evomem.comparators import QueryAudit, SupportAwareRollback
from evomem.cost import Budget, BudgetExceededError, Ledger
from evomem.fixtures import fixture
from evomem.model import (
    InformationAccess,
    Memory,
    PolicyView,
    Snapshot,
    Status,
    Support,
)
from evomem.models.client import (
    AnthropicClient,
    ModelCallError,
    ModelIdentity,
    ModelRequest,
    ModelResponse,
    QwenVLLMClient,
    parse_response,
)
from evomem.models.embeddings import EmbeddingCache, SemanticClosure
from evomem.models.execution import ModelExecutor, cache_key
from evomem.models.inference import (
    FrozenInference,
    PointEstimatePolicy,
    SupportInference,
    parse_supports,
    request_for,
)
from evomem.models.pricing import estimate_usd
from evomem.policies import Baseline, RecordedInference
from evomem.replay import CachedReplay
from evomem.simulation import Corruption, project, run

IDENTITY = ModelIdentity("anthropic", "claude-sonnet-5", "claude-sonnet-5", "test-only")
REQUEST = ModelRequest(
    "system", "user", "{}", "test", max_output_tokens=20, input_reservation=30
)


def response(
    text: str = "{}", input_tokens: int | None = 10, output_tokens: int | None = 5
) -> ModelResponse:
    return ModelResponse(
        text,
        IDENTITY,
        "request-1",
        input_tokens,
        0,
        output_tokens,
        None,
        1.0,
        "end_turn",
        {"input_tokens": input_tokens, "output_tokens": output_tokens},
        {},
    )


@dataclass
class FakeClient:
    responses: list[ModelResponse | Exception]
    identity: ModelIdentity = IDENTITY
    requests: list[ModelRequest] = field(default_factory=list)

    def preflight(self, request: ModelRequest) -> None:
        pass

    def generate(self, request: ModelRequest) -> ModelResponse:
        self.requests.append(request)
        value = self.responses.pop(0)
        if isinstance(value, Exception):
            raise value
        return value


@dataclass
class FakeTransport:
    raw: dict[str, Any]
    bodies: list[dict[str, Any]] = field(default_factory=list)

    def post(
        self, url: str, headers: dict[str, str], body: dict[str, Any], timeout: float
    ) -> dict[str, Any]:
        self.bodies.append(body)
        return self.raw


def view(name: str = "alternative") -> PolicyView:
    scenario, _ = fixture(name)
    revision = scenario.revisions[0]
    items = tuple(
        replace(m, status=Status.SUPERSEDED, valid_until=1)
        if m.memory_id == revision.before
        else m
        for m in scenario.initial
    )
    return project(
        scenario,
        Snapshot(1, items + (revision.after,)),
        revision,
        (),
        InformationAccess(),
        Corruption(),
    )


def structured(v: PolicyView) -> str:
    return json.dumps(
        {
            "assessments": [
                {
                    "target_id": m.memory_id,
                    "decision": "specified",
                    "groups": [
                        {
                            "members": list(s.members),
                            "relation": s.relation.value,
                            "sufficient": s.sufficient,
                            "confidence": 0.9,
                        }
                        for s in v.lineage
                        if s.target == m.memory_id
                    ],
                }
                for m in v.items
                if m.kind != "source"
            ]
        }
    )


def test_native_parsing_and_serialization(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ANTHROPIC_API_KEY", "offline-dummy")
    raw = {
        "model": IDENTITY.model,
        "id": "a",
        "content": [{"type": "text", "text": "{}"}],
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 10,
            "output_tokens": 7,
            "cache_read_input_tokens": 3,
            "cache_creation_input_tokens": 2,
            "extra": "retained",
        },
    }
    transport = FakeTransport(raw)
    result = AnthropicClient(transport).generate(REQUEST)
    assert result.input_tokens == 15 and result.cached_input_tokens == 3
    assert result.raw_usage["extra"] == "retained"
    assert result.reasoning_tokens is None and result.raw_response == raw
    assert "temperature" not in transport.bodies[0]
    assert transport.bodies[0]["output_config"]["format"]["type"] == "json_schema"
    with pytest.raises(ValueError):
        AnthropicClient(transport).generate(replace(REQUEST, temperature=0))


def test_vllm_serialization_and_usage() -> None:
    identity = ModelIdentity("vllm", "Qwen/Qwen3.5-9B", "commit", "manifest")
    raw = {
        "model": identity.model,
        "id": "v",
        "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
        "usage": {
            "prompt_tokens": 20,
            "completion_tokens": 12,
            "completion_tokens_details": {"reasoning_tokens": 8},
        },
    }
    transport = FakeTransport(raw)
    client = QwenVLLMClient(transport, "http://localhost:8000", identity)
    result = client.generate(replace(REQUEST, seed=3))
    assert result.reasoning_tokens == 8 and result.cached_input_tokens is None
    assert transport.bodies[0]["structured_outputs"] == {"json": {}}
    assert transport.bodies[0]["seed"] == 3
    assert result.identity == identity


@pytest.mark.parametrize(
    "raw",
    [
        {"model": "wrong"},
        {"model": IDENTITY.model, "usage": [], "content": [None]},
        {"model": IDENTITY.model, "usage": {"input_tokens": -1}},
        {"model": IDENTITY.model, "content": {"not": "a list"}},
    ],
)
def test_malformed_provider_envelope(raw: dict[str, Any]) -> None:
    with pytest.raises(ModelCallError):
        parse_response(raw, IDENTITY, 1)


@pytest.mark.parametrize(
    "budget",
    [
        Budget(max_model_calls=0),
        Budget(max_input_tokens=29),
        Budget(max_output_tokens=19),
        Budget(max_total_tokens=49),
        Budget(max_verification_calls=0),
        Budget(max_replay_steps=0),
    ],
)
def test_reservation_blocks_before_dispatch(budget: Budget) -> None:
    client = FakeClient([response()])
    executor = ModelExecutor(client, Ledger(budget))
    with pytest.raises(BudgetExceededError):
        executor.generate(REQUEST, 1, "test", verification=True, replay=True)
    assert not client.requests and not executor.ledger.events


def test_reconcile_releases_unused_reservation() -> None:
    client = FakeClient([response(), response()])
    ledger = Ledger(Budget(max_total_tokens=65, max_model_calls=2))
    executor = ModelExecutor(client, ledger)
    executor.generate(REQUEST, 1, "test")
    executor.generate(REQUEST, 1, "test")
    assert ledger.totals()["input_tokens"] == 20
    with pytest.raises(BudgetExceededError):
        executor.generate(REQUEST, 1, "test")
    assert len(client.requests) == 2


@pytest.mark.parametrize(
    "result",
    [
        response(input_tokens=60),
        response(output_tokens=25),
        response(input_tokens=None),
        ModelCallError("timeout"),
    ],
)
def test_unknown_or_overshoot_remains_charged_and_halts(
    result: ModelResponse | Exception,
) -> None:
    client = FakeClient([result, response()])
    ledger = Ledger(Budget(max_total_tokens=60))
    executor = ModelExecutor(client, ledger)
    with pytest.raises((BudgetExceededError, ModelCallError)):
        executor.generate(REQUEST, 1, "test")
    assert ledger.totals()["model_calls"] == 1
    with pytest.raises(BudgetExceededError):
        executor.generate(REQUEST, 1, "test")
    assert len(client.requests) == 1


def test_missing_credential_is_not_physical_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    executor = ModelExecutor(AnthropicClient(FakeTransport({})), Ledger(Budget()))
    with pytest.raises(ValueError):
        executor.generate(REQUEST, 1, "test")
    assert not executor.ledger.events


def test_cache_is_config_and_version_specific(tmp_path: Path) -> None:
    client = FakeClient([response()])
    ledger = Ledger(Budget(max_model_calls=1))
    executor = ModelExecutor(client, ledger, tmp_path)
    first = executor.generate(REQUEST, 1, "test")
    assert executor.generate(REQUEST, 1, "test") == first
    assert len(client.requests) == 1 and ledger.totals()["cache_hits"] == 1
    for changed in [
        replace(REQUEST, user="new"),
        replace(REQUEST, system="new"),
        replace(REQUEST, schema_version="v2"),
        replace(REQUEST, seed=1),
        replace(REQUEST, max_output_tokens=19),
    ]:
        assert cache_key(client, changed) != cache_key(client, REQUEST)
    changed_client = FakeClient([], replace(IDENTITY, version="v2"))
    assert cache_key(changed_client, REQUEST) != cache_key(client, REQUEST)
    raw = json.loads(next(tmp_path.iterdir()).read_text())
    assert raw["response"]["raw_usage"]["input_tokens"] == 10


def test_schema_retry_is_bounded_and_billed() -> None:
    v = view()
    client = FakeClient([response("broken"), response(structured(v))])
    executor = ModelExecutor(client, Ledger(Budget(max_model_calls=2)))
    proposals = SupportInference(executor).infer(v)
    assert len(proposals) == 3
    assert executor.ledger.totals()["model_calls"] == 2
    assert executor.attempts[0]["structured_validation"] == "failed"
    assert client.requests[0] != client.requests[1]
    client = FakeClient([response("broken"), response("still broken")])
    with pytest.raises(ModelCallError):
        SupportInference(ModelExecutor(client, Ledger(Budget()))).infer(v)
    assert len(client.requests) == 2


@pytest.mark.parametrize(
    "mutation",
    ["missing", "unknown_id", "association", "extra", "duplicate", "confidence"],
)
def test_strict_support_validation(mutation: str) -> None:
    v = view()
    raw = json.loads(structured(v))
    group = raw["assessments"][0]["groups"][0]
    if mutation == "missing":
        raw["assessments"].pop()
    if mutation == "unknown_id":
        group["members"] = ["gold_hidden"]
    if mutation == "association":
        group["relation"] = "association"
    if mutation == "extra":
        group["oracle"] = True
    if mutation == "duplicate":
        group["members"] = ["s1", "s1"]
    if mutation == "confidence":
        group["confidence"] = float("nan")
    with pytest.raises(ValueError):
        parse_supports(json.dumps(raw), v)


def test_same_point_proposals_pairwise_vs_support_sets() -> None:
    v = view()
    frozen = FrozenInference(parse_supports(structured(v), v))
    graph = PointEstimatePolicy(frozen, "B5a").repair(v, Ledger(Budget()))
    sets = PointEstimatePolicy(frozen, "B5b").repair(v, Ledger(Budget()))
    assert next(m for m in graph.items if m.memory_id == "b1").status == Status.INACTIVE
    assert next(m for m in sets.items if m.memory_id == "b1").status == Status.ACTIVE
    # Confidence only determines fixed selection, never schedules another operation.
    ledger = Ledger(Budget(max_model_calls=0, max_verification_calls=0))
    PointEstimatePolicy(frozen, "B5b", threshold=0.95).repair(v, ledger)
    assert not ledger.events


def test_model_policy_uses_common_scenario_interface() -> None:
    scenario, _ = fixture("alternative")
    client = FakeClient([response(structured(view()))])
    ledger = Ledger(Budget())
    trace = run(
        scenario,
        PointEstimatePolicy(SupportInference(ModelExecutor(client, ledger))),
        InformationAccess(),
        ledger,
    )
    classical = run(
        scenario,
        Baseline("B7", RecordedInference()),
        InformationAccess(),
        Ledger(Budget()),
    )
    assert trace.snapshots == classical.snapshots


def test_prompt_allowlist_blocks_oracles_and_future() -> None:
    v = view()
    hidden = Support("GOLD_SUPPORT", "b1", ("s1",))
    future = Memory(
        "FUTURE_REVISION", "ADJUDICATED_ANSWER", "secret", created_at_checkpoint=99
    )
    poisoned = replace(
        v,
        lineage=(hidden,),
        rules=(hidden,),
        items=v.items + (future,),
        history=(Snapshot(99, (future,)),),
        revision=replace(v.revision, kind="GOLD_CORRUPTION"),
        access=InformationAccess(source_provenance=False, authority_labels=False),
    )
    prompt = request_for(poisoned).user
    for marker in [
        "GOLD_SUPPORT",
        "ADJUDICATED_ANSWER",
        "FUTURE_REVISION",
        "GOLD_CORRUPTION",
        "scenario_id",
        "cluster_id",
        "expected",
        "gold",
        "o1",
        "o2",
    ]:
        assert marker not in prompt
    assert (
        request_for(replace(poisoned, lineage=(), rules=(), history=())).user == prompt
    )


@pytest.mark.parametrize(
    "name,expected",
    [
        ("alternative", Status.ACTIVE),
        ("conjunction", Status.INACTIVE),
        ("copies", Status.INACTIVE),
    ],
)
def test_b9_rescue_and_copies(name: str, expected: Status) -> None:
    result = SupportAwareRollback().repair(view(name), Ledger(Budget()))
    assert next(m for m in result.items if m.memory_id == "b1").status == expected


def test_b9_unknown_or_shared_origin_cannot_claim_independence() -> None:
    v = view()
    for origins in [(), ("o1",)]:
        changed = replace(
            v,
            items=tuple(
                replace(m, origin_ids=origins) if m.memory_id == "s2" else m
                for m in v.items
            ),
        )
        result = SupportAwareRollback().repair(changed, Ledger(Budget()))
        assert (
            next(m for m in result.items if m.memory_id == "b1").status
            == Status.QUARANTINED
        )


def test_query_only_repeated_cost_and_nonmutation() -> None:
    v = view("necessary")
    raw = json.dumps(
        {
            "verdict": "contradicted",
            "answer": "production capacity eight",
            "evidence_ids": ["s3"],
        }
    )
    client = FakeClient([response(raw), response(raw)])
    ledger = Ledger(Budget(max_verification_calls=2))
    audit = QueryAudit(ModelExecutor(client, ledger))
    before = v.items
    assert audit.query(v, "b1").answer == "production capacity eight"
    assert audit.query(v, "b1").verdict == "contradicted"
    assert audit.query(v, "b1").completion == "budget_exhausted"
    assert (
        v.items == before
        and next(m for m in v.items if m.memory_id == "b1").status == Status.ACTIVE
    )
    assert ledger.totals()["verification_calls"] == 2
    assert ledger.totals()["model_calls"] == 2


@dataclass
class FakeEmbedding:
    identity: str = "offline-v1"
    calls: int = 0

    def encode(self, text: str) -> tuple[float, ...]:
        self.calls += 1
        return (1.0, 0.0) if "four" in text else (0.0, 1.0)


def test_embedding_cache_identity_and_simple_neighborhood(tmp_path: Path) -> None:
    backend = FakeEmbedding()
    cache = EmbeddingCache(backend, tmp_path)
    ledger = Ledger(Budget())
    result = SemanticClosure(cache).repair(view(), ledger)
    assert all(m.status == Status.INACTIVE for m in result.items if m.kind != "source")
    assert backend.calls == 1  # identical text content, including bystander
    cache.vector("production capacity four", ledger, 1)
    assert backend.calls == 1
    backend.identity = "offline-v2"
    cache.vector("production capacity four", ledger, 1)
    assert backend.calls == 2 and ledger.totals()["embedding_calls"] == 2


def test_b8_counts_dependency_work_on_hits_and_invalidates_changed_evidence() -> None:
    v = view()
    policy = CachedReplay()
    ledger = Ledger(Budget())
    policy.repair(v, ledger)
    before = ledger.totals()["dependency_checks"]
    policy.repair(v, ledger)
    assert ledger.totals()["cache_hits"] == 2
    assert ledger.totals()["dependency_checks"] > before  # type: ignore[operator]
    changed = replace(
        v,
        items=tuple(
            replace(m, status=Status.INACTIVE) if m.memory_id == "s2" else m
            for m in v.items
        ),
    )
    result = policy.repair(changed, ledger)
    assert (
        next(m for m in result.items if m.memory_id == "b1").status == Status.INACTIVE
    )
    assert ledger.totals()["replay_steps"] == 4


def test_price_is_posthoc_and_unknown_write_ttl_not_guessed() -> None:
    table = json.loads(
        Path("research/resources/pricing/anthropic-2026-09-26.json").read_text()
    )
    assert estimate_usd(response(), table) == pytest.approx(70 / 1_000_000)
    unknown = replace(
        response(),
        raw_usage={
            "input_tokens": 10,
            "output_tokens": 5,
            "cache_creation_input_tokens": 10,
        },
    )
    assert estimate_usd(unknown, table) is None


def test_native_schema_avoids_unsupported_numeric_constraints() -> None:
    schema = request_for(view()).schema_json
    assert "minimum" not in schema and "maximum" not in schema
    assert "Finite number from 0 to 1" in schema


def test_cache_payload_tampering_detected(tmp_path: Path) -> None:
    executor = ModelExecutor(FakeClient([response()]), Ledger(Budget()), tmp_path)
    executor.generate(REQUEST, 1, "test")
    path = next(tmp_path.iterdir())
    raw = json.loads(path.read_text())
    raw["response"]["text"] = "tampered"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match="checksum"):
        executor.generate(REQUEST, 1, "test")
    assert executor.ledger.totals()["model_calls"] == 1


def test_query_rejects_stale_citation() -> None:
    raw = json.dumps({"verdict": "supported", "answer": "four", "evidence_ids": ["s1"]})
    executor = ModelExecutor(FakeClient([response(raw)]), Ledger(Budget()))
    assert QueryAudit(executor).query(view(), "b1").completion == "model_failed"
    assert executor.ledger.totals()["model_calls"] == 1


def test_smoke_skips_without_secrets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from evomem.experiment.model_smoke import execute

    for key in ["ANTHROPIC_API_KEY", "VLLM_BASE_URL", "QWEN_DEPLOYMENT_MANIFEST"]:
        monkeypatch.delenv(key, raising=False)
    for provider in ["anthropic", "vllm"]:
        result = execute(provider, tmp_path / provider)
        assert result["status"] == "SKIPPED"
        assert result["cost"]["model_calls"] == 0
        assert result["target_assessments"] == 7


@dataclass
class EmptySupportClient:
    identity: ModelIdentity = IDENTITY
    calls: int = 0

    def preflight(self, request: ModelRequest) -> None:
        pass

    def generate(self, request: ModelRequest) -> ModelResponse:
        self.calls += 1
        rows = json.loads(request.user)["records"]
        return response(
            json.dumps(
                {
                    "assessments": [
                        {"target_id": r["id"], "decision": "unknown", "groups": []}
                        for r in rows
                        if r["kind"] != "source"
                    ]
                }
            )
        )


def test_smoke_runner_five_attempts_then_real_dispatch_block(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from evomem.experiment import model_smoke

    client = EmptySupportClient()
    monkeypatch.setattr(
        model_smoke, "configured_client", lambda provider: (client, None)
    )
    result = model_smoke.execute("anthropic", tmp_path / "offline-canned")
    assert result["status"] == "PASS"  # Mechanical completion, not semantic accuracy.
    assert result["post_cap_dispatch_blocked"] is True
    assert client.calls == 5 and result["cost"]["model_calls"] == 5
    assert len(result["results"]) == 5 and not result["hypothesis_statistics"]


@pytest.mark.parametrize("finish", ["refusal", "max_tokens"])
def test_refusal_or_truncation_charged_without_retry(finish: str) -> None:
    client = FakeClient([replace(response(), finish_reason=finish)])
    executor = ModelExecutor(client, Ledger(Budget()))
    with pytest.raises(ModelCallError, match="refusal_or_truncation"):
        SupportInference(executor).infer(view())
    assert len(client.requests) == 1 and executor.ledger.totals()["output_tokens"] == 5


def test_retry_cannot_bypass_call_cap() -> None:
    client = FakeClient([response("broken")])
    ledger = Ledger(Budget(max_model_calls=1))
    decision = PointEstimatePolicy(
        SupportInference(ModelExecutor(client, ledger))
    ).repair(view(), ledger)
    assert decision.completion == "budget_exhausted"
    assert len(client.requests) == 1


def test_invalid_usage_subsets_fail_closed_preserving_raw_attempt() -> None:
    invalid = replace(response(), cached_input_tokens=100)
    executor = ModelExecutor(FakeClient([invalid]), Ledger(Budget()))
    with pytest.raises(ModelCallError, match="invalid_usage"):
        executor.generate(REQUEST, 1, "test")
    assert executor.halted and executor.ledger.totals()["input_tokens"] is None
    assert executor.ledger.totals()["model_calls"] == 1
    assert executor.attempts[0]["response"] == asdict(invalid)
