"""Bounded local Qwen ENGINEERING VALIDATION, never scientific evidence."""

import argparse
import json
import os
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any

from evomem.comparators import QueryAudit
from evomem.cost import Budget, BudgetExceededError, Ledger
from evomem.experiment.live_support import digest, manifest, write_manifest
from evomem.experiment.model_smoke import QWEN_REVISION
from evomem.experiment.observable_fixtures import nonce_view, support_view
from evomem.model_replay import Derivation, ModelCachedReplay, ModelDeriver
from evomem.models.client import HTTPTransport, ModelIdentity, ModelRequest, Transport
from evomem.models.execution import ModelExecutor
from evomem.models.inference import (
    FrozenInference,
    PointEstimatePolicy,
    SupportInference,
)
from evomem.models.llama_cpp import QwenLlamaCppClient
from evomem.models.tokenization import token_ids


@dataclass
class LocalTransport:
    inner: Transport = field(default_factory=HTTPTransport)
    generations: int = 0

    def post(
        self, url: str, headers: dict[str, str], body: dict[str, Any], timeout: float
    ) -> dict[str, Any]:
        if url.endswith("/v1/chat/completions"):
            self.generations += 1
        return self.inner.post(url, headers, body, timeout)


def configured_local_client() -> QwenLlamaCppClient:
    data = json.loads(Path(os.environ["QWEN_DEPLOYMENT_MANIFEST"]).read_text())
    required = {
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
    }
    if not required <= data.keys() or any(data[k] in ("", None) for k in required):
        raise ValueError("Incomplete local Qwen deployment manifest")
    if data["model"] != "Qwen/Qwen3.5-9B" or data["source_revision"] != QWEN_REVISION:
        raise ValueError("Local deployment differs from pinned Qwen source")
    return QwenLlamaCppClient(
        LocalTransport(),
        os.environ.get("QWEN_LOCAL_URL", "http://127.0.0.1:8087"),
        ModelIdentity(
            "llama.cpp", data["model"], QWEN_REVISION, json.dumps(data, sort_keys=True)
        ),
    )


def token_audit(
    client: QwenLlamaCppClient, executor: ModelExecutor
) -> list[dict[str, Any]]:
    """Independently tokenize rendered prompts and inspect generated token IDs.

    These metadata endpoints do not execute model inference. llama.cpp verbose
    output exposes sampled IDs including its terminating EOS token.
    """
    records = []
    for attempt in executor.attempts:
        if attempt.get("cache_hit") or "response" not in attempt:
            continue
        raw_request = attempt["request"]
        response = attempt["response"]
        assert isinstance(raw_request, dict) and isinstance(response, dict)
        req = ModelRequest(**raw_request)

        def post(route: str, body: dict[str, Any]) -> dict[str, Any]:
            return client.transport.post(
                client.base_url + route, {"content-type": "application/json"}, body, 60
            )

        rendered = post("/apply-template", client.request_body(req))["prompt"]
        ids = token_ids(
            post("/tokenize", {"content": rendered, "add_special": True})["tokens"]
        )
        raw = response["raw_response"]
        native = raw["__verbose"]
        generated = token_ids(native["tokens"])
        decoded = post("/detokenize", {"tokens": list(generated)})["content"]
        record = {
            "request_id": response["request_id"],
            "input_ids_count": len(ids),
            "input_ids_hash": digest(ids),
            "reported_input": response["input_tokens"],
            "generated_ids_count": len(generated),
            "generated_ids_hash": digest(generated),
            "reported_output": response["output_tokens"],
            "native_stop_type": native["stop_type"],
            "native_tokens_evaluated": native["tokens_evaluated"],
            "native_tokens_predicted": native["tokens_predicted"],
            "decoded_output_hash": digest(decoded),
        }
        record["input_match"] = len(ids) == response["input_tokens"]
        record["output_match"] = len(generated) == response["output_tokens"]
        records.append(record)
    return records


def validate(output: Path, client: QwenLlamaCppClient) -> dict[str, Any]:
    if output.exists():
        raise ValueError("Use a fresh output directory")
    counter = client.transport
    if not isinstance(counter, LocalTransport):
        counter = LocalTransport(counter)
        client.transport = counter
    basic = Ledger(
        Budget(
            max_model_calls=1,
            max_input_tokens=8192,
            max_output_tokens=256,
            max_total_tokens=8448,
        )
    )
    first = ModelExecutor(client, basic)
    details: dict[str, Any] = {"components": {}, "hypothesis_statistics": False}
    request = ModelRequest(
        "Return JSON only.",
        'Return {"ok":true}.',
        '{"type":"object","properties":{"ok":{"type":"boolean"}},'
        '"required":["ok"],"additionalProperties":false}',
        "basic-v1",
        max_output_tokens=256,
    )
    all_executors = [first]
    try:
        response = first.generate(request, 0, "trivial", use_cache=False)
        assert (
            json.loads(response.text) == {"ok": True}
            and response.finish_reason == "stop"
        )
        details["components"]["trivial_generation"] = "PASS"
        before = counter.generations
        try:
            first.generate(request, 0, "budget-stop", use_cache=False)
            raise AssertionError("Second generation was not blocked")
        except BudgetExceededError:
            assert counter.generations == before == 1
        details["budget_stop"] = {
            "cap": 1,
            "actual_generations": before,
            "after_second_request": counter.generations,
            "blocked_before_dispatch": True,
        }
        details["components"]["budget_stop"] = "PASS"
    except Exception as error:
        details["basic_error"] = {
            "type": type(error).__name__,
            "message": str(error)[:300],
        }
    # Each requested path has a separate small cap; one failure cannot hide others.
    for name, calls in [("B5b", 2), ("B8", 2), ("B10", 1)]:
        ledger = Ledger(
            Budget(
                max_model_calls=calls,
                max_input_tokens=8192 * calls,
                max_output_tokens=1024 * calls,
                max_total_tokens=9216 * calls,
            )
        )
        executor = ModelExecutor(client, ledger)
        all_executors.append(executor)
        try:
            if name == "B5b":
                view = support_view()
                proposals = SupportInference(executor, use_cache=False).infer(view)
                decision = PointEstimatePolicy(
                    FrozenInference(proposals), "B5b"
                ).repair(view, ledger)
                details["support"] = {
                    "proposals": [(asdict(s), c) for s, c in proposals],
                    "decision": asdict(decision),
                    "scope": "Existing five-relation observable smoke batch; "
                    "no accuracy score",
                }
            elif name == "B8":
                replay = ModelCachedReplay(ModelDeriver(executor))
                spec = (
                    Derivation(
                        "t", "State which protocol Project Zorvia uses.", ("s",), "v1"
                    ),
                )
                cold = replay.update(nonce_view(), spec)
                warm = replay.update(nonce_view(), spec)
                changed = replay.update(nonce_view("K29"), spec)
                assert (
                    cold.completion == warm.completion == changed.completion == "done"
                )
                assert warm.cache_hits == 1 and changed.cache_misses == 1
                old_text = next(m.content for m in cold.items if m.memory_id == "t")
                new_text = next(m.content for m in changed.items if m.memory_id == "t")
                assert "K17" in old_text and "K29" in new_text and old_text != new_text
                details["replay"] = {
                    "cold": old_text,
                    "changed": new_text,
                    "warm_cache_hits": warm.cache_hits,
                    "changed_regenerated_nodes": changed.regenerated_nodes,
                }
            else:
                view = nonce_view("K29")
                original = view.items
                audit_result = QueryAudit(executor).query(view, "t")
                assert audit_result.completion == "done" and view.items == original
                details["query_audit"] = asdict(audit_result)
            details["components"][name] = "PASS"
        except Exception as error:
            details["components"][name] = "FAIL"
            details[name + "_error"] = {
                "type": type(error).__name__,
                "message": str(error)[:300],
            }
    accounting = []
    try:
        for executor in all_executors:
            accounting.extend(token_audit(client, executor))
        assert accounting and all(
            r["input_match"] and r["output_match"] for r in accounting
        )
        details["components"]["token_accounting"] = "PASS"
    except Exception as error:
        details["components"]["token_accounting"] = "FAIL"
        details["accounting_error"] = {
            "type": type(error).__name__,
            "message": str(error)[:300],
        }
    details["token_accounting"] = accounting
    details["generation_dispatches"] = counter.generations
    details["phase_budgets"] = [asdict(e.ledger.budget) for e in all_executors]
    aggregate = ModelExecutor(client, Ledger(Budget()))
    for index, executor in enumerate(all_executors):
        aggregate.ledger.events.extend(
            replace(e, operation_id=f"{index}:{e.operation_id}")
            for e in executor.ledger.events
        )
        aggregate.attempts.extend(executor.attempts)
    status = (
        "PASS"
        if all(
            details["components"].get(c) == "PASS"
            for c in [
                "trivial_generation",
                "budget_stop",
                "B5b",
                "B8",
                "B10",
                "token_accounting",
            ]
        )
        else "FAIL"
    )
    requests = []
    for attempt in aggregate.attempts:
        raw_request = attempt.get("request")
        if isinstance(raw_request, dict):
            requests.append(ModelRequest(**raw_request))
    result = manifest(
        client.identity, aggregate.ledger, status, requests, details, aggregate
    )
    result["label"] = "ENGINEERING VALIDATION — NOT SCIENTIFIC EVIDENCE"
    write_manifest(output, result)
    (output / "attempts.json").write_text(
        json.dumps(aggregate.attempts, indent=2) + "\n"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("EVOMEM_RUN_LIVE_TESTS") != "1":
        raise SystemExit("Requires EVOMEM_RUN_LIVE_TESTS=1; no paid API flag needed")
    result = validate(args.output, configured_local_client())
    print(json.dumps({"status": result["status"], "details": result["details"]}))
    raise SystemExit(0 if result["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
