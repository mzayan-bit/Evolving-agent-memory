"""Run fixture experiments only. Real pilot execution deliberately unavailable."""

import argparse
import hashlib
import json
import platform
import re
import subprocess
from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

from evomem.cost import Budget, CostEvent, Ledger
from evomem.data import validate
from evomem.evaluation import aggregate, score
from evomem.fixtures import FIXTURES, fixture
from evomem.model import InformationAccess
from evomem.policies import BASELINES, Baseline, RecordedInference
from evomem.simulation import Corruption, corrupt, run


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def execute(config: dict[str, Any]) -> Path:
    if config.get("mode") != "ENGINEERING_ONLY":
        raise ValueError(
            "Real pilot disabled: requires adjudication and protocol freeze"
        )
    identifier = config["experiment_id"]
    if not isinstance(identifier, str) or not re.fullmatch(
        r"[A-Za-z0-9_-]+", identifier
    ):
        raise ValueError("Unsafe experiment ID")
    dirty = bool(git("status", "--porcelain"))
    if dirty and not config.get("allow_dirty", False):
        raise ValueError("Dirty tree: commit first or explicitly allow_dirty")
    output = Path(config.get("output_root", "results")) / identifier
    output.mkdir(parents=True, exist_ok=False)
    (output / "logs").mkdir()
    access = InformationAccess(**config.get("information_access", {}))
    budget = Budget(**config.get("budget", {}))
    seed = config.get("seed", 0)
    corruption = Corruption(seed=seed, **config.get("corruption", {}))
    rows = []
    aggregates = {}
    for name in config.get("policies", BASELINES):
        nested = []
        for fixture_name in config.get("fixtures", FIXTURES):
            scenario, gold = fixture(fixture_name)
            validate(scenario, gold)
            ledger = Ledger(budget)
            trace = run(
                scenario,
                Baseline(name, RecordedInference()),
                access,
                ledger,
                corruption,
                gold.supports if access.gold_dependencies else None,
            )
            query_start = perf_counter()
            metrics = score(gold, trace)
            answers = [
                {
                    "probe_id": p.probe_id,
                    "answer": trace.answer(p.item_id, p.checkpoint, p.view, p.as_of),
                    "used_item_ids": [p.item_id]
                    if trace.answer(p.item_id, p.checkpoint, p.view, p.as_of)
                    is not None
                    else [],
                }
                for p in gold.probes
            ]
            ledger.charge(
                CostEvent(
                    "fixed-readout",
                    "readout-and-scoring",
                    len(scenario.revisions),
                    wall_latency_ms=(perf_counter() - query_start) * 1000,
                )
            )
            observed = corrupt(scenario.observed, corruption)
            true_incidences = {
                (s.justification_id, m, s.target)
                for s in gold.supports
                for m in s.members
            }
            visible_incidences = {
                (s.justification_id, m, s.target) for s in observed for m in s.members
            }

            nested.append((scenario.cluster_id, scenario.scenario_id, metrics))
            row = {
                "scenario": scenario.scenario_id,
                "cluster": scenario.cluster_id,
                "policy": name,
                "metrics": {k: v.json() for k, v in metrics.items()},
                "cost": ledger.totals(),
                "completion": [d.completion for d in trace.decisions],
            }
            rows.append(row)
            (output / "logs" / f"{name}-{fixture_name}.json").write_text(
                json.dumps(
                    {
                        "trace": asdict(trace),
                        "answers": answers,
                        "corruption_audit": {
                            "true_incidences": len(true_incidences),
                            "retained_incidences": len(
                                true_incidences & visible_incidences
                            ),
                            "spurious_incidences": len(
                                visible_incidences - true_incidences
                            ),
                            "removed": sorted(true_incidences - visible_incidences),
                            "inserted": sorted(visible_incidences - true_incidences),
                        },
                        "ledger": [asdict(e) for e in ledger.events],
                    },
                    indent=2,
                )
            )
        aggregates[name] = aggregate(nested)
    (output / "per_scenario.jsonl").write_text(
        "".join(json.dumps(r) + "\n" for r in rows)
    )
    (output / "aggregate.json").write_text(json.dumps(aggregates, indent=2))
    artifacts = {
        str(p.relative_to(output)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(output.rglob("*"))
        if p.is_file()
    }
    manifest = {
        "experiment_id": identifier,
        "git_commit": git("rev-parse", "HEAD"),
        "timestamp": datetime.now(UTC).isoformat(),
        "dirty": dirty,
        "scenario_version": "engineering-v1",
        "python_version": platform.python_version(),
        "policy_config": config,
        "model_identifiers": [],
        "seed": seed,
        "information_access": asdict(access),
        "budget": asdict(budget),
        "metrics": aggregates,
        "cost": [r["cost"] for r in rows],
        "artifacts": artifacts,
        "status": "ENGINEERING_ONLY_NO_RESEARCH_FINDINGS",
        "corruption_label": "synthetic perturbation",
        "oracle": access.gold_dependencies or access.gold_fault_identity,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    print(execute(json.loads(args.config.read_text())))


if __name__ == "__main__":
    main()
