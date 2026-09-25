"""Opt-in five-fixture model plumbing smoke; never a scientific pilot."""

import argparse
import hashlib
import json
import os
import platform
import subprocess
from dataclasses import asdict, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from evomem.cost import Budget, BudgetExceededError, Ledger
from evomem.fixtures import fixture
from evomem.model import InformationAccess, Snapshot, Status
from evomem.models.client import (
    AnthropicClient,
    HTTPTransport,
    ModelCallError,
    ModelClient,
    ModelIdentity,
    QwenVLLMClient,
)
from evomem.models.execution import ModelExecutor
from evomem.models.inference import (
    FrozenInference,
    PointEstimatePolicy,
    SupportInference,
    request_for,
)
from evomem.simulation import Corruption, project

QWEN_REVISION = "c202236235762e1c871ad0ccb60c8ee5ba337b9a"
NAMES = ("necessary", "alternative", "conjunction", "semantic_bystander", "copies")


def configured_client(provider: str) -> tuple[ModelClient | None, str | None]:
    if provider == "anthropic":
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return None, "ANTHROPIC_API_KEY unavailable"
        return AnthropicClient(HTTPTransport()), None
    if not os.environ.get("VLLM_BASE_URL") or not os.environ.get(
        "QWEN_DEPLOYMENT_MANIFEST"
    ):
        return (
            None,
            "Qwen endpoint/deployment manifest unavailable; hardware not assessed",
        )
    manifest = json.loads(Path(os.environ["QWEN_DEPLOYMENT_MANIFEST"]).read_text())
    required = {
        "model",
        "revision",
        "tokenizer_revision",
        "vllm_version",
        "dtype",
        "quantization",
        "hardware",
        "context_length",
        "server_command",
    }
    if not required <= set(manifest) or any(
        manifest[k] in ("", None) for k in required
    ):
        raise ValueError("Incomplete Qwen deployment manifest")
    if (
        manifest["model"] != "Qwen/Qwen3.5-9B"
        or manifest["revision"] != QWEN_REVISION
        or manifest["tokenizer_revision"] != QWEN_REVISION
        or manifest["vllm_version"] != "0.30.0"
    ):
        raise ValueError("Deployment differs from pinned development candidate")
    identity = ModelIdentity(
        "vllm", manifest["model"], QWEN_REVISION, json.dumps(manifest, sort_keys=True)
    )
    return QwenVLLMClient(HTTPTransport(), os.environ["VLLM_BASE_URL"], identity), None


def execute(provider: str, output: Path) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=False)
    budget = Budget(
        max_model_calls=5,
        max_input_tokens=40960,
        max_output_tokens=5120,
        max_total_tokens=46080,
        max_verification_calls=5,
        max_replay_steps=5,
    )
    ledger = Ledger(budget)
    client, reason = configured_client(provider)
    manifest: dict[str, Any] = {
        "label": "ENGINEERING SMOKE TEST — NOT RESEARCH EVIDENCE",
        "timestamp": datetime.now(UTC).isoformat(),
        "provider": provider,
        "git": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "dirty": bool(
            subprocess.check_output(["git", "status", "--porcelain"], text=True)
        ),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "budget": asdict(budget),
        "fixtures": list(NAMES),
        "target_assessments": 7,  # Five main targets, one bystander, one copy
        "hypothesis_statistics": False,
        "status": "SKIPPED" if client is None else "ATTEMPTED",
        "reason": reason,
    }
    if client is not None:
        executor = ModelExecutor(client, ledger, output / "cache")
        manifest["identity"] = asdict(client.identity)
        results = []
        for name in NAMES:
            scenario, _unused_fixture_gold = fixture(name)
            revision = scenario.revisions[0]
            items = tuple(
                replace(m, status=Status.SUPERSEDED, valid_until=1)
                if m.memory_id == revision.before
                else m
                for m in scenario.initial
            )
            items = tuple(
                m for m in items if m.memory_id != "b2" or name == "semantic_bystander"
            )
            view = project(
                scenario,
                Snapshot(1, items + (revision.after,)),
                revision,
                (),
                InformationAccess(),
                Corruption(),
            )
            try:
                proposals = SupportInference(executor, use_cache=False).infer(view)
                frozen = FrozenInference(proposals)
                decisions = {
                    variant: asdict(
                        PointEstimatePolicy(frozen, variant).repair(view, ledger)
                    )
                    for variant in ("B5a", "B5b")
                }
                results.append(
                    {
                        "fixture": name,
                        "status": "PARSED",
                        "proposals": [
                            {"support": asdict(s), "confidence": p}
                            for s, p in proposals
                        ],
                        "decisions": decisions,
                    }
                )
            except (ModelCallError, BudgetExceededError, ValueError) as error:
                results.append(
                    {
                        "fixture": name,
                        "status": "FAILED",
                        "error_type": type(error).__name__,
                    }
                )
                break
        if len(results) == len(NAMES) and all(r["status"] == "PARSED" for r in results):
            try:
                executor.generate(
                    request_for(view), 1, "budget-stop-probe", use_cache=False
                )
            except BudgetExceededError:
                manifest["post_cap_dispatch_blocked"] = True
        manifest["results"] = results
        manifest["status"] = (
            "PASS"
            if len(results) == len(NAMES)
            and all(r["status"] == "PARSED" for r in results)
            and manifest.get("post_cap_dispatch_blocked") is True
            else "FAILED"
        )
        manifest["pass_scope"] = (
            "Transport/schema/accounting execution only; inspect competence manually"
        )
        (output / "attempts.json").write_text(json.dumps(executor.attempts, indent=2))
        manifest["attempts_sha256"] = hashlib.sha256(
            (output / "attempts.json").read_bytes()
        ).hexdigest()
    manifest["cost"] = ledger.totals()
    (output / "ledger.json").write_text(
        json.dumps([asdict(e) for e in ledger.events], indent=2)
    )
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", choices=["anthropic", "vllm"], required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = execute(args.provider, args.output)
    print(
        json.dumps(
            {
                "status": result["status"],
                "reason": result["reason"],
                "cost": result["cost"],
            }
        )
    )


if __name__ == "__main__":
    main()
