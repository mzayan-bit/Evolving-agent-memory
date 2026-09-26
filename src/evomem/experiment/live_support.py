"""Shared opt-in live validation artifacts; no secret values or human labels."""

import hashlib
import json
import os
import platform
import shutil
import subprocess
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from evomem.cost import Budget, Ledger
from evomem.models.client import ModelIdentity, ModelRequest
from evomem.models.execution import ModelExecutor


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def environment() -> dict[str, Any]:
    hardware: dict[str, Any] = {"machine": platform.machine()}
    if platform.system() == "Darwin":
        try:
            raw = json.loads(
                subprocess.check_output(
                    ["system_profiler", "SPHardwareDataType", "-json"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                )
            )["SPHardwareDataType"][0]
            hardware.update(
                {
                    k: raw.get(k)
                    for k in [
                        "machine_model",
                        "chip_type",
                        "number_processors",
                        "physical_memory",
                    ]
                }
            )
        except (subprocess.SubprocessError, ValueError, KeyError, IndexError):
            hardware["inspection"] = "unavailable"
    return {
        "os": platform.platform(),
        "python": platform.python_version(),
        "hardware": hardware,
        "disk_free_bytes": shutil.disk_usage(".").free,
        "credentials": {
            key: "configured" if os.environ.get(key) else "missing"
            for key in [
                "ANTHROPIC_API_KEY",
                "HF_TOKEN",
                "VLLM_BASE_URL",
                "QWEN_DEPLOYMENT_MANIFEST",
            ]
        },
    }


def remaining(ledger: Ledger) -> dict[str, int | float | None]:
    totals = ledger.totals()
    output: dict[str, int | float | None] = {}
    for name, cap in asdict(ledger.budget).items():
        if cap is None:
            output[name] = None
            continue
        resource = name.removeprefix("max_")
        if resource in {"tokens", "total_tokens"}:
            a, b = totals["input_tokens"], totals["output_tokens"]
            used = None if a is None or b is None else a + b
        else:
            used = totals[resource]
        output[name] = None if used is None else cap - used
    return output


def manifest(
    identity: ModelIdentity | None,
    ledger: Ledger,
    status: str,
    requests: list[ModelRequest],
    details: dict[str, Any],
    executor: ModelExecutor | None = None,
) -> dict[str, Any]:
    attempts = [] if executor is None else executor.attempts
    # Whitelist response metadata, never headers or raw generated/source text.
    sanitized = []
    for attempt in attempts:
        response = attempt.get("response")
        if isinstance(response, dict):
            sanitized.append(
                {
                    k: response.get(k)
                    for k in [
                        "identity",
                        "request_id",
                        "input_tokens",
                        "cached_input_tokens",
                        "output_tokens",
                        "reasoning_tokens",
                        "latency_ms",
                        "finish_reason",
                        "raw_usage",
                    ]
                }
                | {
                    "response_hash": digest(response),
                    "cache_hit": attempt.get("cache_hit"),
                    "reserved_input": attempt.get("reserved_input"),
                    "reserved_output": attempt.get("reserved_output"),
                }
            )
        else:
            sanitized.append(
                {
                    k: attempt.get(k)
                    for k in [
                        "operation_id",
                        "cache_hit",
                        "error",
                        "blocked_before_dispatch",
                    ]
                }
            )
    return {
        "label": "ENGINEERING SMOKE TEST ONLY",
        "status": status,
        "git_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True
        ).strip(),
        "dirty": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "timestamp": datetime.now(UTC).isoformat(),
        "environment": environment(),
        "provider": identity.provider if identity else None,
        "model": identity.model if identity else None,
        "model_version": identity.version if identity else None,
        "runtime": identity.deployment if identity else None,
        "prompt_hashes": [
            digest({"system": r.system, "user": r.user, "schema": r.schema_json})
            for r in requests
        ],
        "generation_config": [
            {
                "seed": r.seed,
                "temperature": r.temperature,
                "max_output_tokens": r.max_output_tokens,
                "schema_version": r.schema_version,
            }
            for r in requests
        ],
        "budget": asdict(ledger.budget),
        "usage": ledger.totals(),
        "remaining": remaining(ledger),
        "cache_stats": {
            "hits": ledger.totals()["cache_hits"],
            "physical_model_misses": ledger.totals()["model_calls"],
            "physical_embedding_encodes": ledger.totals()["embedding_calls"],
        },
        "latency_ms": sum(
            e.wall_latency_ms for e in ledger.events if e.phase == "runtime"
        )
        if any(e.phase == "runtime" for e in ledger.events)
        else ledger.totals()["wall_latency_ms"],
        "latency_semantics": "Runtime event or physical phase sum. "
        "usage.wall_latency_ms includes nested events and is not end-to-end time.",
        "attempts": sanitized,
        "events": [asdict(e) for e in ledger.events],
        "details": details,
    }


def write_manifest(output: Path, result: dict[str, Any]) -> None:
    output.mkdir(parents=True, exist_ok=False)
    (output / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")


def skipped(
    output: Path, reason: str, identity: ModelIdentity | None = None
) -> dict[str, Any]:
    value = manifest(identity, Ledger(Budget()), "SKIPPED", [], {"reason": reason})
    write_manifest(output, value)
    return value
