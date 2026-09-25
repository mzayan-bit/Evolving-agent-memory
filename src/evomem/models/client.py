"""Synchronous HTTP model clients with injectable transport for offline tests."""

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from time import perf_counter
from typing import Any, Protocol


@dataclass(frozen=True)
class ModelIdentity:
    provider: str
    model: str
    version: str
    deployment: (
        str  # Versioned server/runtime/tokenizer/hardware manifest JSON or hash.
    )


@dataclass(frozen=True)
class ModelRequest:
    system: str
    user: str
    schema_json: str
    schema_version: str
    max_output_tokens: int = 1024
    input_reservation: int = 8192
    temperature: float | None = None
    seed: int | None = None

    def __post_init__(self) -> None:
        if self.max_output_tokens <= 0 or self.input_reservation <= 0:
            raise ValueError("Positive token reservations required")


@dataclass(frozen=True)
class ModelResponse:
    text: str
    identity: ModelIdentity
    request_id: str | None
    input_tokens: int | None
    cached_input_tokens: int | None
    output_tokens: int | None
    reasoning_tokens: int | None
    latency_ms: float
    finish_reason: str | None
    raw_usage: dict[str, Any]
    raw_response: dict[str, Any]


class ModelCallError(RuntimeError):
    """No reliable usage received: attempted call remains charged, usage unknown."""

    raw_response: dict[str, Any] | None = None


class Transport(Protocol):
    def post(
        self, url: str, headers: dict[str, str], body: dict[str, Any], timeout: float
    ) -> dict[str, Any]: ...


class HTTPTransport:
    def post(
        self, url: str, headers: dict[str, str], body: dict[str, Any], timeout: float
    ) -> dict[str, Any]:
        request = urllib.request.Request(
            url, data=json.dumps(body).encode(), headers=headers, method="POST"
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                value = json.load(response)
            if not isinstance(value, dict):
                raise ModelCallError("malformed_provider_envelope")
            return value
        except urllib.error.HTTPError as error:
            # Never expose headers/keys/error bodies in exception strings.
            categories = {
                400: "invalid_request_or_context",
                401: "authentication",
                403: "permission",
                429: "rate_limit_or_quota",
                500: "server_error",
                502: "server_error",
                503: "server_error",
            }
            raise ModelCallError(categories.get(error.code, "http_error")) from None
        except (urllib.error.URLError, TimeoutError):
            raise ModelCallError("transport_or_timeout") from None
        except (ValueError, TypeError):
            raise ModelCallError("malformed_provider_envelope") from None


class ModelClient(Protocol):
    identity: ModelIdentity

    def preflight(self, request: ModelRequest) -> None: ...

    def generate(self, request: ModelRequest) -> ModelResponse: ...


def count(value: Any) -> int | None:
    if value is None:
        return None
    if type(value) is not int or value < 0:
        raise ModelCallError("invalid_usage_metadata")
    return int(value)


def _parse_response(
    raw: dict[str, Any], identity: ModelIdentity, latency_ms: float
) -> ModelResponse:
    if raw.get("model") != identity.model:
        raise ModelCallError("unexpected_returned_model")
    usage = raw.get("usage") or {}
    if identity.provider == "anthropic":
        text = "".join(
            b.get("text", "") for b in raw.get("content", []) if b.get("type") == "text"
        )
        base = count(usage.get("input_tokens"))
        read = count(usage.get("cache_read_input_tokens", 0))
        write = count(usage.get("cache_creation_input_tokens", 0))
        total = (
            None
            if base is None or read is None or write is None
            else base + read + write
        )
        output = count(usage.get("output_tokens"))
        reasoning = None  # No guessed reasoning allocation from content length.
        finish = raw.get("stop_reason")
    else:
        choice = raw.get("choices", [{}])[0]
        text = choice.get("message", {}).get("content") or ""
        total = count(usage.get("prompt_tokens"))
        read = count((usage.get("prompt_tokens_details") or {}).get("cached_tokens"))
        output = count(usage.get("completion_tokens"))
        reasoning = count(
            (usage.get("completion_tokens_details") or {}).get("reasoning_tokens")
        )
        finish = choice.get("finish_reason")
    if not isinstance(text, str):
        raise ModelCallError("invalid_text_content")
    return ModelResponse(
        text,
        identity,
        raw.get("id"),
        total,
        read,
        output,
        reasoning,
        latency_ms,
        finish,
        usage,
        raw,
    )


@dataclass
class AnthropicClient:
    transport: Transport
    identity: ModelIdentity = ModelIdentity(
        "anthropic", "claude-sonnet-5", "claude-sonnet-5", "native-messages-2023-06-01"
    )
    timeout: float = 45.0

    def preflight(self, request: ModelRequest) -> None:
        if request.temperature is not None or request.seed is not None:
            raise ValueError(
                "Sonnet 5 adapter omits unsupported sampling/seed settings"
            )
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY is not configured")

    def generate(self, request: ModelRequest) -> ModelResponse:
        self.preflight(request)
        key = os.environ["ANTHROPIC_API_KEY"]
        body = {
            "model": self.identity.model,
            "max_tokens": request.max_output_tokens,
            "system": request.system,
            "messages": [{"role": "user", "content": request.user}],
            "output_config": {
                "format": {
                    "type": "json_schema",
                    "schema": json.loads(request.schema_json),
                }
            },
        }
        start = perf_counter()
        raw = self.transport.post(
            "https://api.anthropic.com/v1/messages",
            {
                "x-api-key": key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            body,
            self.timeout,
        )
        return parse_response(raw, self.identity, (perf_counter() - start) * 1000)


@dataclass
class QwenVLLMClient:
    transport: Transport
    base_url: str
    identity: ModelIdentity
    timeout: float = 45.0

    def __post_init__(self) -> None:
        if (
            self.identity.provider != "vllm"
            or not self.identity.version
            or not self.identity.deployment
        ):
            raise ValueError("Pinned vLLM model and deployment metadata required")
        if not self.base_url.startswith(
            ("http://localhost:", "http://127.0.0.1:", "https://")
        ):
            raise ValueError("Use localhost or HTTPS; no implicit remote deployment")

    def preflight(self, request: ModelRequest) -> None:
        json.loads(request.schema_json)

    def generate(self, request: ModelRequest) -> ModelResponse:
        body: dict[str, Any] = {
            "model": self.identity.model,
            "messages": [
                {"role": "system", "content": request.system},
                {"role": "user", "content": request.user},
            ],
            "max_tokens": request.max_output_tokens,
            "temperature": request.temperature
            if request.temperature is not None
            else 0.0,
            "structured_outputs": {"json": json.loads(request.schema_json)},
        }
        if request.seed is not None:
            body["seed"] = request.seed
        headers = {"content-type": "application/json"}
        if os.environ.get("VLLM_API_KEY"):
            headers["authorization"] = "Bearer " + os.environ["VLLM_API_KEY"]
        start = perf_counter()
        raw = self.transport.post(
            self.base_url.rstrip("/") + "/v1/chat/completions",
            headers,
            body,
            self.timeout,
        )
        return parse_response(raw, self.identity, (perf_counter() - start) * 1000)


def parse_response(
    raw: dict[str, Any], identity: ModelIdentity, latency_ms: float
) -> ModelResponse:
    try:
        return _parse_response(raw, identity, latency_ms)
    except ModelCallError as error:
        error.raw_response = raw
        raise
    except (KeyError, IndexError, TypeError, AttributeError):
        malformed = ModelCallError("malformed_provider_envelope")
        malformed.raw_response = raw
        raise malformed from None
