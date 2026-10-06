"""Four opt-in fictional historical calls; ENGINEERING VALIDATION ONLY."""

import argparse
import json
import os
from dataclasses import asdict
from pathlib import Path
from typing import Any

from evomem.arms import run_arms
from evomem.cost import Budget
from evomem.experiment.live_support import digest, manifest, write_manifest
from evomem.experiment.qwen_local import (
    LocalTransport,
    configured_local_client,
    token_audit,
)
from evomem.model import Memory, Revision, Scenario, Support
from evomem.models.client import ModelRequest
from evomem.readout import ReadoutProbe, assess_readout


def nonce_scenario(kind: str = "supersession") -> Scenario:
    source = Memory("s0", "Project Zorvia uses protocol K17.", "lab", kind="source")
    next_source = Memory(
        "s1",
        source.content,
        "lab",
        valid_from=1,
        created_at_checkpoint=1,
        kind="source",
    )
    changed = Memory(
        "s2",
        "Project Zorvia uses protocol K29.",
        "lab",
        valid_from=2,
        created_at_checkpoint=2,
        kind="source",
    )
    other = Memory("u", "Project Tovren uses protocol M83.", "lab", kind="source")
    target = Memory("t", source.content, "lab", source_ids=("s0",))
    unaffected = Memory("v", other.content, "lab", source_ids=("u",))
    supports = tuple(
        Support(f"j{i}", "t", (f"s{i}",), scope="lab", valid_from=i) for i in range(3)
    ) + (Support("ju", "v", ("u",), scope="lab"),)
    return Scenario(
        "temporal-engineering",
        "temporal-engineering",
        "v1",
        (source, target, other, unaffected),
        (
            Revision(1, "s0", next_source, fault_cue="s0"),
            Revision(2, "s1", changed, kind=kind, fault_cue="s1"),
        ),
        supports,
        (),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("EVOMEM_RUN_LIVE_TESTS") != "1":
        raise SystemExit(
            "Set EVOMEM_RUN_LIVE_TESTS=1 for the four-call engineering smoke"
        )
    client = configured_local_client()
    run = run_arms(
        nonce_scenario(),
        ("B10",),
        client,
        args.output / "arms",
        Budget(max_model_calls=4, max_input_tokens=32768, max_output_tokens=4096),
        credit_schedule=((1, 2), (2, 2)),
    )["B10"]
    before = digest(asdict(run.trace))
    probes = [
        ("current", ReadoutProbe("t", 2), True, "K29"),
        (
            "as-known",
            ReadoutProbe("t", 2, time_view="historical_then", as_of=1),
            True,
            "K17",
        ),
        (
            "unaffected",
            ReadoutProbe(
                "v", 2, "Which protocol does Project Tovren use?", "historical_then", 1
            ),
            False,
            "M83",
        ),
        (
            "retrospective-supersession",
            ReadoutProbe(
                "t", 2, "Which protocol did Project Zorvia use?", "historical_now", 1
            ),
            False,
            "K17",
        ),
    ]
    outcomes: list[dict[str, Any]] = []
    for label, probe, audit, expected in probes:
        subject = "Tovren" if label == "unaffected" else "Zorvia"
        result = run.reader(audit).answer(probe)
        outcomes.append(
            {
                "label": label,
                "probe": asdict(probe),
                "result": asdict(result),
                "expected_nonce": expected,
                "nonce_present": expected in (result.answer or ""),
                "assessment": asdict(
                    assess_readout(
                        result,
                        expected_answer=f"Project {subject} uses protocol {expected}.",
                        memory_state_correct=label != "current",
                        required_retrieval=frozenset(
                            {
                                "s2"
                                if label == "current"
                                else "u"
                                if label == "unaffected"
                                else "s1"
                            }
                        ),
                    )
                ),
            }
        )
    ex = run.session.executor
    stop = run.reader().answer(ReadoutProbe("t", 2))
    audits = token_audit(client, ex)
    assert isinstance(client.transport, LocalTransport)
    passed = (
        all(
            o["nonce_present"] and o["result"]["completion"] == "done" for o in outcomes
        )
        and all(a["input_match"] and a["output_match"] for a in audits)
        and digest(asdict(run.trace)) == before
        and stop.completion == "budget_exhausted"
        and client.transport.generations == 4
    )
    requests = [
        ModelRequest(**request)
        for a in ex.attempts
        if isinstance(request := a.get("request"), dict)
    ]
    value = manifest(
        client.identity,
        ex.ledger,
        "PASS" if passed else "FAIL",
        requests,
        {
            "label": "ENGINEERING VALIDATION ONLY",
            "outcomes": outcomes,
            "state_unchanged": digest(asdict(run.trace)) == before,
            "budget_stop": asdict(stop),
            "token_audits": audits,
            "arm_report": run.report(),
        },
        ex,
    )
    write_manifest(args.output / "receipt", value)
    (args.output / "attempts.json").write_text(json.dumps(ex.attempts, indent=2) + "\n")
    print(
        json.dumps(
            {"status": value["status"], "usage": value["usage"], "outcomes": outcomes},
            indent=2,
        )
    )
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
