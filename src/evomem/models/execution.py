"""Serialized reservation -> physical dispatch -> actual usage reconciliation."""

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from threading import RLock
from time import perf_counter

from evomem.cost import BudgetExceededError, CostEvent, Ledger
from evomem.models.client import (
    ModelCallError,
    ModelClient,
    ModelRequest,
    ModelResponse,
)


def cache_key(client: ModelClient, request: ModelRequest) -> str:
    blob = json.dumps(
        {"identity": asdict(client.identity), "request": asdict(request)},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(blob.encode()).hexdigest()


@dataclass
class ModelExecutor:
    client: ModelClient
    ledger: Ledger
    cache_dir: Path | None = None
    halted: bool = False
    attempts: list[dict[str, object]] = field(default_factory=list)
    _lock: RLock = field(default_factory=RLock)

    def generate(
        self,
        request: ModelRequest,
        checkpoint: int,
        phase: str,
        verification: bool = False,
        replay: bool = False,
        use_cache: bool = True,
    ) -> ModelResponse:
        with self._lock:
            if self.halted:
                raise BudgetExceededError(
                    "Executor halted after unknown usage or overrun"
                )
            key = cache_key(self.client, request)
            path = self.cache_dir / (key + ".json") if self.cache_dir else None
            op = f"model:{len(self.ledger.events)}"
            if path and use_cache and path.exists():
                raw = json.loads(path.read_text())
                identity = self.client.identity
                if raw["key"] != key or raw["identity"] != asdict(identity):
                    raise ValueError("Cache identity mismatch")
                checksum = hashlib.sha256(
                    json.dumps(raw["response"], sort_keys=True).encode()
                ).hexdigest()
                if raw.get("response_sha256") != checksum:
                    raise ValueError("Cache response checksum mismatch")
                response = ModelResponse(identity=identity, **raw["response"])
                self.ledger.charge(
                    CostEvent(
                        op,
                        phase,
                        checkpoint,
                        cache_hits=1,
                        model_id=identity.model,
                        provider=identity.provider,
                        model_version=identity.version,
                    )
                )
                self.attempts.append(
                    {
                        "operation_id": op,
                        "cache_key": key,
                        "cache_hit": True,
                        "original_usage": response.raw_usage,
                    }
                )
                return response
            reserve = CostEvent(
                op,
                phase,
                checkpoint,
                model_calls=1,
                input_tokens=request.input_reservation,
                output_tokens=request.max_output_tokens,
                verification_calls=int(verification),
                replay_steps=int(replay),
                usage_source="reservation",
            )
            # Probe a copied ledger: no physical event is charged before dispatch.
            Ledger(self.ledger.budget, list(self.ledger.events)).charge(reserve)
            self.client.preflight(request)
            start = perf_counter()
            try:
                response = self.client.generate(request)
            except (ModelCallError, ValueError) as error:
                event = CostEvent(
                    op,
                    phase,
                    checkpoint,
                    model_calls=1,
                    input_tokens=None,
                    output_tokens=None,
                    cached_input_tokens=None,
                    verification_calls=int(verification),
                    replay_steps=int(replay),
                    usage_source="unknown",
                    status="failed",
                    provider=self.client.identity.provider,
                    model_id=self.client.identity.model,
                    model_version=self.client.identity.version,
                    wall_latency_ms=(perf_counter() - start) * 1000,
                )
                self.ledger.events.append(
                    event
                )  # Physical attempts must never disappear.
                self.attempts.append(
                    {
                        "operation_id": op,
                        "cache_key": key,
                        "error": str(error),
                        "request": asdict(request),
                        "raw_response": error.raw_response
                        if isinstance(error, ModelCallError)
                        else None,
                        "cache_hit": False,
                    }
                )
                self.halted = True
                raise
            event = CostEvent(
                op,
                phase,
                checkpoint,
                model_calls=1,
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                cached_input_tokens=response.cached_input_tokens,
                reasoning_tokens=response.reasoning_tokens,
                reasoning_token_semantics="subset_of_output",
                verification_calls=int(verification),
                replay_steps=int(replay),
                wall_latency_ms=response.latency_ms,
                usage_source="provider_reported",
                provider=response.identity.provider,
                model_id=response.identity.model,
                model_version=response.identity.version,
                request_id=response.request_id,
            )
            audit: dict[str, object] = {
                "operation_id": op,
                "cache_key": key,
                "cache_hit": False,
                "request": asdict(request),
                "response": asdict(response),
                "reserved_input": request.input_reservation,
                "reserved_output": request.max_output_tokens,
            }
            self.attempts.append(audit)
            try:
                self.ledger.charge(event)
            except (BudgetExceededError, ValueError):
                self.ledger.events.append(event)
                audit["overrun"] = True
                self.halted = True
                raise BudgetExceededError(
                    "Actual usage exceeded reservation/cap; recorded"
                ) from None
            if response.input_tokens is None or response.output_tokens is None:
                self.halted = True
                audit["unknown_usage"] = True
            if (
                response.input_tokens is not None
                and response.input_tokens > request.input_reservation
                or response.output_tokens is not None
                and response.output_tokens > request.max_output_tokens
            ):
                audit["reservation_exceeded"] = True
                self.halted = True
                raise BudgetExceededError("Actual usage exceeded reservation; recorded")
            if (
                path
                and use_cache
                and not self.halted
                and response.finish_reason in {"end_turn", "stop"}
            ):
                path.parent.mkdir(parents=True, exist_ok=True)
                payload = asdict(response)
                payload.pop("identity")
                with path.open("x") as stream:
                    json.dump(
                        {
                            "key": key,
                            "identity": asdict(response.identity),
                            "response": payload,
                            "response_sha256": hashlib.sha256(
                                json.dumps(payload, sort_keys=True).encode()
                            ).hexdigest(),
                        },
                        stream,
                        sort_keys=True,
                    )
            return response
