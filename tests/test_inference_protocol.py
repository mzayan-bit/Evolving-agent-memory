"""Protocol, accounting and information-boundary regressions."""

import json
from dataclasses import replace

import pytest
from test_models import FakeClient, response

from evomem.cost import Budget, BudgetExceededError, Ledger
from evomem.experiment.inference_audit import compare
from evomem.experiment.observable_fixtures import nonce_view
from evomem.model import Relation, Support
from evomem.models.client import ModelCallError, ModelResponse
from evomem.models.execution import ModelExecutor
from evomem.models.failures import InferenceCategory as C
from evomem.models.failures import InferenceError, ProtocolError
from evomem.models.inference import (
    PointEstimatePolicy,
    SupportInference,
    parse_supports,
    request_for,
)


def valid() -> dict[str, object]:
    return {
        "assessments": [
            {
                "target_id": i,
                "decision": "specified",
                "groups": [
                    {
                        "members": [s],
                        "relation": "necessary",
                        "sufficient": True,
                        "confidence": 0.9,
                    }
                ],
            }
            for i, s in [("t", "s"), ("v", "u")]
        ]
    }


@pytest.mark.parametrize(
    "mutation,category",
    [
        ("text_id", C.UNKNOWN_TARGET_ID),
        ("missing", C.MISSING_REQUIRED_FIELD),
        ("coverage", C.MISSING_TARGET),
        ("duplicate", C.DUPLICATE_RELATION),
        ("contradiction", C.CONTRADICTORY_STRUCTURE),
        ("json", C.MALFORMED_OUTPUT),
    ],
)
def test_categories_are_strict(mutation: str, category: C) -> None:
    raw = json.loads(json.dumps(valid()))
    row = raw["assessments"][0]
    if mutation == "text_id":
        row["target_id"] = "Project Zorvia uses protocol K17."
    elif mutation == "missing":
        del row["decision"]
    elif mutation == "coverage":
        raw["assessments"].pop()
    elif mutation == "duplicate":
        row["groups"].append(row["groups"][0])
    elif mutation == "contradiction":
        row["groups"][0]["relation"] = "association"
    text = "not json" if mutation == "json" else json.dumps(raw)
    with pytest.raises(ProtocolError) as caught:
        parse_supports(text, nonce_view())
    assert caught.value.category == category


def test_retry_uses_only_contract_evidence_and_raw_failure_and_is_billed() -> None:
    client = FakeClient([response("malformed"), response(json.dumps(valid()))])
    ledger = Ledger(Budget(max_model_calls=2))
    executor = ModelExecutor(client, ledger)
    inference = SupportInference(executor, use_cache=False)
    inference.infer(nonce_view())
    assert ledger.totals()["model_calls"] == 2
    assert ledger.totals()["input_tokens"] == 20
    assert ledger.totals()["output_tokens"] == 10
    assert ledger.totals()["wall_latency_ms"] == 2
    retry = json.loads(client.requests[1].user)
    assert retry["protocol_retry"]["previous_output"] == "malformed"
    assert inference.diagnostics[1]["parent_request_id"] == "request-1"
    retry.pop("protocol_retry")
    assert retry == json.loads(client.requests[0].user)
    poisoned = replace(nonce_view(), rules=(Support("GOLD", "t", ("u",)),))
    assert request_for(poisoned) == request_for(nonce_view())
    client = FakeClient([response("bad"), response("bad")])
    with pytest.raises(InferenceError):
        SupportInference(ModelExecutor(client, Ledger(Budget()))).infer(poisoned)
    assert len(client.requests) == 2


def test_retry_cannot_cross_budget_and_semantic_error_does_not_retry() -> None:
    ledger = Ledger(Budget(max_model_calls=1))
    client = FakeClient([response("bad")])
    inference = SupportInference(ModelExecutor(client, ledger))
    with pytest.raises(BudgetExceededError):
        inference.infer(nonce_view())
    assert len(client.requests) == 1
    assert inference.diagnostics[-1]["category"] == C.BUDGET_EXHAUSTED
    # Wrong but protocol-valid edge is retained without repair or another call.
    raw = json.loads(json.dumps(valid()))
    raw["assessments"][0]["groups"][0]["members"] = ["u"]
    client = FakeClient([response(json.dumps(raw))])
    inference = SupportInference(ModelExecutor(client, Ledger(Budget())))
    proposals = inference.infer(nonce_view())
    assert proposals[0][0].members == ("u",) and len(client.requests) == 1
    result = compare(proposals, (Support("gold", "t", ("s",)),), "B5b", {"t"})
    assert result["category"] == C.VALID_WRONG_SEMANTICS
    assert inference.diagnostics[-1]["category"] == C.VALID_CORRECT_FORMAT


@pytest.mark.parametrize("variant", ["B5a", "B5b"])
def test_live_policy_interface_uses_distinct_elicitation_same_evidence(
    variant: str,
) -> None:
    client = FakeClient([response(json.dumps(valid()))])
    ledger = Ledger(Budget())
    inference = SupportInference(ModelExecutor(client, ledger))
    assert (
        PointEstimatePolicy(inference, variant).repair(nonce_view(), ledger).completion
        == "done"
    )
    req = client.requests[0]
    assert json.loads(req.user) == json.loads(request_for(nonce_view()).user)
    members = json.loads(req.schema_json)["properties"]["assessments"]["items"][
        "properties"
    ]["groups"]["items"]["properties"]["members"]
    assert (members.get("maxItems") == 1) == (variant == "B5a")
    assert ledger.totals()["verification_calls"] == ledger.totals()["replay_steps"] == 0


def test_id_enums_come_only_from_visible_records_and_duplicate_json_fails() -> None:
    view = nonce_view()
    req = request_for(view)
    payload = json.loads(req.user)
    assert payload["candidate_memory_ids"] == ["s", "t", "u", "v"]
    assert payload["required_target_ids"] == ["t", "v"]
    with pytest.raises(ProtocolError):
        parse_supports('{"assessments":[],"assessments":[]}', view)


def test_refusal_timeout_and_truncation_never_trigger_schema_retry() -> None:
    cases: list[tuple[ModelResponse | Exception, C]] = [
        (replace(response(), finish_reason="refusal"), C.MODEL_REFUSAL),
        (replace(response(), finish_reason="length"), C.TRUNCATED_OUTPUT),
        (ModelCallError("model_timeout"), C.MODEL_TIMEOUT),
    ]
    for result, category in cases:
        client = FakeClient([result])
        inference = SupportInference(ModelExecutor(client, Ledger(Budget())))
        with pytest.raises(InferenceError) as caught:
            inference.infer(nonce_view())
        assert caught.value.category == category and len(client.requests) == 1


def test_conflicting_same_members_remain_structural_failure() -> None:
    raw = json.loads(json.dumps(valid()))
    group = raw["assessments"][0]["groups"][0]
    raw["assessments"][0]["groups"].append(dict(group, relation=Relation.COPIED.value))
    with pytest.raises(ProtocolError) as caught:
        parse_supports(json.dumps(raw), nonce_view())
    assert caught.value.category == C.CONTRADICTORY_STRUCTURE


def test_replay_and_repeat_audit_runner_contracts() -> None:
    from test_live_paths import ScriptClient

    from evomem.experiment.qwen_hardening import audit_checks, replay_checks

    client = ScriptClient()
    replay = ModelExecutor(client, Ledger(Budget(max_model_calls=6)))
    result = replay_checks(replay)
    assert result["full_equals_incremental"] and result["state_commit_atomic"]
    assert replay.ledger.totals()["model_calls"] == 6
    assert replay.ledger.totals()["cache_hits"] == 3
    assert any(
        e.phase == "dependency-check" and e.wall_latency_ms > 0
        for e in replay.ledger.events
    )
    audit = ModelExecutor(ScriptClient(), Ledger(Budget(max_model_calls=2)))
    result = audit_checks(audit)
    assert result["persistent_state_unchanged"]
    assert audit.ledger.totals()["verification_calls"] == 2


def test_historical_semantic_error_stays_in_receipt() -> None:
    from pathlib import Path

    historical = json.loads(
        Path("research/g1/qwen_local/validation-final.json").read_text()
    )
    proposals = historical["details"]["support"]["proposals"]
    wrong = next(s for s, _ in proposals if s["target"] == "assoc")
    assert wrong["members"] == ["e"] and wrong["sufficient"] is True


def test_http_timeout_is_not_mislabeled_as_schema_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import urllib.request

    from evomem.models.client import HTTPTransport

    def timeout(*args: object, **kwargs: object) -> None:
        raise TimeoutError()

    monkeypatch.setattr(urllib.request, "urlopen", timeout)
    with pytest.raises(ModelCallError, match="model_timeout"):
        HTTPTransport().post("http://127.0.0.1:8087", {}, {}, 1)
