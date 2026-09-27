"""Opt-in bounded ENGINEERING FIXTURES — NOT RESEARCH EVALUATION.

Gold comparisons run only after the complete model-backed fixture pass. No
comparison result changes a prompt, retry, threshold, cache or repair decision.
"""

import argparse
import json
import os
from dataclasses import asdict, replace
from pathlib import Path
from time import perf_counter
from typing import Any

from evomem.comparators import QueryAudit
from evomem.cost import Budget, Ledger
from evomem.experiment.hardening_fixtures import Case, cases
from evomem.experiment.inference_audit import compare
from evomem.experiment.live_support import digest, manifest, write_manifest
from evomem.experiment.observable_fixtures import nonce_view
from evomem.experiment.qwen_local import configured_local_client, token_audit
from evomem.model_replay import Derivation, ModelCachedReplay, ModelDeriver
from evomem.models.client import ModelClient, ModelRequest
from evomem.models.execution import ModelExecutor
from evomem.models.inference import (
    PointEstimatePolicy,
    SupportInference,
    visible_payload,
)
from evomem.models.llama_cpp import QwenLlamaCppClient


def executor(client: ModelClient, calls: int, path: Path) -> ModelExecutor:
    return ModelExecutor(
        client,
        Ledger(
            Budget(
                max_model_calls=calls,
                max_input_tokens=8192 * calls,
                max_output_tokens=1024 * calls,
                max_total_tokens=9216 * calls,
            )
        ),
        path / "responses",
    )


def receipt(
    path: Path, ex: ModelExecutor, status: str, details: dict[str, Any]
) -> dict[str, Any]:
    requests = []
    for attempt in ex.attempts:
        raw = attempt.get("request")
        if isinstance(raw, dict):
            requests.append(ModelRequest(**raw))
    value = manifest(ex.client.identity, ex.ledger, status, requests, details, ex)
    value.update(
        label="ENGINEERING FIXTURES — NOT RESEARCH EVALUATION",
        energy_joules=None,
        estimated_usd=None,
        currency_cost_reason="Local execution; energy and currency not measured",
        wire_request_hashes=[digest(ex.client.request_body(r)) for r in requests]
        if isinstance(ex.client, QwenLlamaCppClient)
        else [],
    )
    # Cache may already occupy this directory; write_manifest requires a new one.
    write_manifest(path / "receipt", value)
    (path / "attempts.json").write_text(json.dumps(ex.attempts, indent=2) + "\n")
    return value


def support_case(
    case: Case, variant: str, client: ModelClient, output: Path
) -> tuple[dict[str, Any], ModelExecutor, SupportInference]:
    ex = executor(client, 2, output)
    inference = SupportInference(ex, use_cache=True)
    started = perf_counter()
    decision = PointEstimatePolicy(inference, variant).repair(case.view, ex.ledger)
    details: dict[str, Any] = {
        "fixture": case.name,
        "variant": variant,
        "evidence_hash": digest(visible_payload(case.view)),
        "infrastructure_success": any("response" in a for a in ex.attempts),
        "schema_success": inference.last_proposals is not None,
        "semantic_correct": None,
        "category": inference.diagnostics[-1]["category"],
        "diagnostics": inference.diagnostics,
        "retry_count": max(0, int(ex.ledger.totals()["model_calls"] or 0) - 1),
        "threshold": 0.7,
        "decision": asdict(decision),
        "model_proposals": None
        if inference.last_proposals is None
        else [(asdict(s), c) for s, c in inference.last_proposals],
        "component_elapsed_ms": (perf_counter() - started) * 1000,
        "fixture_limit": case.note,
    }
    return details, ex, inference


def replay_checks(ex: ModelExecutor) -> dict[str, Any]:
    replay = ModelCachedReplay(ModelDeriver(ex))
    specs = (
        Derivation("t", "State which protocol Project Zorvia uses.", ("s",), "v1"),
        Derivation("v", "State which protocol Project Tovren uses.", ("u",), "v1"),
    )
    before = nonce_view()
    changed = nonce_view("K29")
    initial = replay.update(before, specs)
    warm = replay.update(before, specs)
    incremental = replay.update(changed, specs)
    full = replay.update(changed, specs, reuse=False)
    assert all(x.completion == "done" for x in [initial, warm, incremental, full])
    assert warm.cache_hits == 2 and incremental.cache_hits == 1
    assert incremental.regenerated_nodes == ("t",) and incremental.items == full.items
    assert (
        next(m for m in incremental.items if m.memory_id == "t").content.find("K29")
        >= 0
    )
    assert before == nonce_view()
    # Fail after one actual successful generation in a fresh transaction.
    # The second is denied before dispatch; neither partial state nor cache commits.
    ex.ledger.budget = replace(ex.ledger.budget, max_model_calls=6)
    atomic = ModelCachedReplay(ModelDeriver(ex))
    rejected = atomic.update(changed, specs)
    assert rejected.completion == "budget_exhausted"
    assert rejected.items == changed.items and atomic.cache == {}
    return {
        "initial": asdict(initial),
        "warm": asdict(warm),
        "incremental": asdict(incremental),
        "full": asdict(full),
        "atomic_budget_failure": asdict(rejected),
        "full_equals_incremental": True,
        "state_commit_atomic": True,
    }


def audit_checks(ex: ModelExecutor) -> dict[str, Any]:
    view = nonce_view("K29")
    before = digest(asdict(view))
    results = [QueryAudit(ex).query(view, "t") for _ in range(2)]
    assert all(
        r.completion == "done"
        and r.verdict == "contradicted"
        and "K29" in (r.answer or "")
        for r in results
    )
    assert digest(asdict(view)) == before
    assert ex.ledger.totals()["verification_calls"] == 2
    assert ex.ledger.totals()["cache_hits"] == 0
    return {
        "queries": [asdict(r) for r in results],
        "persistent_state_unchanged": True,
        "state_still_contains_stale_claim": True,
        "answers_corrected": True,
        "recurrent_audits": 2,
        "cache_policy": "disabled; every query charged",
    }


def usage_sum(executors: list[ModelExecutor], resource: str) -> int | float | None:
    """An unreported physical cost makes the aggregate unknown, never zero."""
    values = [ex.ledger.totals()[resource] for ex in executors]
    if any(value is None for value in values):
        return None
    return sum(value for value in values if value is not None)


def run(output: Path, client: QwenLlamaCppClient) -> dict[str, Any]:
    output.mkdir(parents=True, exist_ok=False)
    started = perf_counter()
    completed = []
    outputs: list[dict[str, Any]] = []
    all_ex: list[ModelExecutor] = []
    fixture_cases = cases()
    # Freeze this complete input inventory before dispatch; never adapt it on scores.
    (output / "inventory.json").write_text(
        json.dumps(
            [
                {"fixture": c.name, "evidence_hash": digest(visible_payload(c.view))}
                for c in fixture_cases
            ],
            indent=2,
        )
        + "\n"
    )
    for case in fixture_cases:
        for variant in ["B5a", "B5b"]:
            path = output / (case.name.replace("@", "-") + "-" + variant)
            details, ex, inference = support_case(case, variant, client, path)
            path.mkdir(parents=True, exist_ok=True)
            (path / "attempts.json").write_text(
                json.dumps(ex.attempts, indent=2) + "\n"
            )
            completed.append((case, variant, path, details, ex, inference))
            all_ex.append(ex)
            print(
                json.dumps(
                    {
                        "fixture": case.name,
                        "variant": variant,
                        "schema": details["schema_success"],
                        "usage": ex.ledger.totals(),
                    }
                ),
                flush=True,
            )
    # Evaluator boundary: gold is consulted after ALL support-model calls.
    for case, variant, path, details, ex, inference in completed:
        if inference.last_proposals is not None:
            details.update(
                compare(inference.last_proposals, case.gold, variant, set(case.targets))
            )
        else:
            details["gold_structure"] = [asdict(s) for s in case.gold]
        value = receipt(path, ex, "RECORDED", details)
        outputs.append(value)
    # Independently bounded replay and query paths; a failure stays explicit.
    for name, fn, cap in [("B8", replay_checks, 6), ("B10", audit_checks, 2)]:
        path = output / name
        ex = executor(client, cap, path)
        try:
            details = fn(ex)
            status = "PASS"
        except Exception as error:
            status = "FAIL"
            details = {
                "component": name,
                "error_type": type(error).__name__,
                "error": str(error),
            }
        all_ex.append(ex)
        outputs.append(receipt(path, ex, status, details))
        print(
            json.dumps(
                {"component": name, "status": status, "usage": ex.ledger.totals()}
            ),
            flush=True,
        )
    # Independent exact token checks, no generation.
    audits = [r for ex in all_ex for r in token_audit(client, ex)]
    assert all(r["input_match"] and r["output_match"] for r in audits)
    result = {
        "label": "ENGINEERING FIXTURES — NOT RESEARCH EVALUATION",
        "support_rows": [v["details"] for v in outputs[: len(completed)]],
        "components": {
            v["details"].get("fixture", str(i)): v["status"]
            for i, v in enumerate(outputs)
        },
        "model_calls": sum(
            int(ex.ledger.totals()["model_calls"] or 0) for ex in all_ex
        ),
        "input_tokens": usage_sum(all_ex, "input_tokens"),
        "output_tokens": usage_sum(all_ex, "output_tokens"),
        "model_latency_ms": sum(
            float(ex.ledger.totals()["wall_latency_ms"] or 0) for ex in all_ex
        ),
        "wall_elapsed_ms": (perf_counter() - started) * 1000,
        "latency_semantics": "model_latency_ms includes charged local replay "
        "preparation; wall_elapsed_ms is the distinct suite elapsed time",
        "token_audits": audits,
        "energy_joules": None,
        "estimated_usd": None,
    }
    (output / "summary.json").write_text(json.dumps(result, indent=2) + "\n")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("EVOMEM_RUN_LIVE_TESTS") != "1":
        raise SystemExit("Explicit EVOMEM_RUN_LIVE_TESTS=1 required")
    run(args.output, configured_local_client())


if __name__ == "__main__":
    main()
