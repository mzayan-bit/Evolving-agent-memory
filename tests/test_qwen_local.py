"""Local dialect, strict origin, and real-dispatch budget boundary (offline)."""

import json
from dataclasses import dataclass, field
from typing import Any

import pytest

from evomem.cost import Budget, BudgetExceededError, Ledger
from evomem.experiment.qwen_local import LocalTransport, configured_local_client
from evomem.models.client import ModelIdentity, ModelRequest
from evomem.models.execution import ModelExecutor
from evomem.models.llama_cpp import QwenLlamaCppClient

IDENTITY = ModelIdentity("llama.cpp", "Qwen/Qwen3.5-9B", "source-pin", "conversion-pin")


@dataclass
class Endpoint:
    bodies: list[dict[str, Any]] = field(default_factory=list)
    headers: list[dict[str, str]] = field(default_factory=list)

    def post(
        self, url: str, headers: dict[str, str], body: dict[str, Any], timeout: float
    ) -> dict[str, Any]:
        self.bodies.append(body)
        self.headers.append(headers)
        return {
            "model": IDENTITY.model,
            "id": "local-1",
            "choices": [
                {"message": {"content": '{"ok":true}'}, "finish_reason": "stop"}
            ],
            "usage": {
                "prompt_tokens": 15,
                "completion_tokens": 6,
                "prompt_tokens_details": {"cached_tokens": 0},
            },
        }


def test_local_schema_accounting_and_predispatch_stop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("VLLM_API_KEY", "must-not-be-forwarded")
    endpoint = Endpoint()
    transport = LocalTransport(endpoint)
    client = QwenLlamaCppClient(transport, "http://127.0.0.1:8087", IDENTITY)
    ledger = Ledger(Budget(max_model_calls=1))
    executor = ModelExecutor(client, ledger)
    req = ModelRequest("system", "user", '{"type":"object"}', "test")
    response = executor.generate(req, 0, "first", use_cache=False)
    assert response.input_tokens == 15 and response.output_tokens == 6
    assert response.cached_input_tokens == 0 and response.reasoning_tokens is None
    body = endpoint.bodies[0]
    assert body["response_format"] == {
        "type": "json_schema",
        "json_schema": {"name": "evomem", "strict": True, "schema": {"type": "object"}},
    }
    assert body["messages"][0]["content"] == (
        'system\n\nRequired output JSON Schema:\n{"type": "object"}'
    )
    assert "structured_outputs" not in body
    assert body["chat_template_kwargs"] == {"enable_thinking": False}
    assert body["temperature"] == 0 and body["seed"] == 0
    assert body["cache_prompt"] is False
    assert "authorization" not in endpoint.headers[0]
    with pytest.raises(BudgetExceededError):
        executor.generate(req, 0, "second", use_cache=False)
    assert transport.generations == 1 and len(endpoint.bodies) == 1
    assert executor.attempts[-1]["blocked_before_dispatch"] is True


@pytest.mark.parametrize(
    "url",
    [
        "https://example.com",
        "http://localhost.evil:8087",
        "http://user:password@localhost:8087",
        "http://127.0.0.1:8087/v1",
        "http://127.0.0.1:8087?x=1",
    ],
)
def test_local_origin_restriction(url: str) -> None:
    with pytest.raises(ValueError, match="local HTTP origin"):
        QwenLlamaCppClient(Endpoint(), url, IDENTITY)


def test_local_manifest_requires_source_pin(
    tmp_path: Any, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "deployment.json"
    data = dict.fromkeys(
        [
            "model",
            "source_revision",
            "conversion_repo",
            "conversion_revision",
            "gguf_sha256",
            "quantization",
            "backend_revision",
            "context_length",
            "hardware",
            "server_command",
        ],
        "wrong",
    )
    path.write_text(json.dumps(data))
    monkeypatch.setenv("QWEN_DEPLOYMENT_MANIFEST", str(path))
    with pytest.raises(ValueError, match="pinned Qwen source"):
        configured_local_client()


def test_token_audit_compares_ids_instead_of_estimating_text() -> None:
    from dataclasses import asdict

    from evomem.experiment.qwen_local import token_audit

    @dataclass
    class TokenEndpoint(Endpoint):
        def post(
            self,
            url: str,
            headers: dict[str, str],
            body: dict[str, Any],
            timeout: float,
        ) -> dict[str, Any]:
            if url.endswith("/apply-template"):
                return {"prompt": "rendered prompt"}
            if url.endswith("/tokenize"):
                return {"tokens": [10, 20, 30]}
            return {"content": '{"ok":true}'}

    client = QwenLlamaCppClient(TokenEndpoint(), "http://localhost:8087", IDENTITY)
    executor = ModelExecutor(client, Ledger(Budget()))
    executor.attempts.append(
        {
            "request": asdict(ModelRequest("system", "user", "{}", "test")),
            "response": {
                "request_id": "test",
                "input_tokens": 3,
                "output_tokens": 2,
                "raw_response": {
                    "__verbose": {
                        "tokens": [40, 248046],
                        "stop_type": "eos",
                        "tokens_evaluated": 3,
                        "tokens_predicted": 2,
                    }
                },
            },
        }
    )
    row = token_audit(client, executor)[0]
    assert row["input_match"] and row["output_match"]
    response = executor.attempts[0]["response"]
    assert isinstance(response, dict)
    response["output_tokens"] = 3
    assert token_audit(client, executor)[0]["output_match"] is False
