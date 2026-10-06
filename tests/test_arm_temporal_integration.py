"""Only accounting, cache and temporal-boundary regressions; no model quality test."""

import json
from dataclasses import replace
from pathlib import Path

import pytest
from test_live_paths import ScriptClient
from test_models import FakeClient, FakeEmbedding, response

from evomem.arms import ARMS, SharedSupports, run_arms
from evomem.cost import Budget, BudgetExceededError, CostEvent, Ledger
from evomem.experiment.temporal_smoke import nonce_scenario
from evomem.model import InformationAccess, Memory, Snapshot, Support
from evomem.model_replay import Derivation
from evomem.models.client import ModelCallError, ModelRequest, ModelResponse
from evomem.models.embeddings import EmbeddingCache
from evomem.models.execution import ModelExecutor, cache_key
from evomem.models.inference import request_for
from evomem.readout import ReadoutProbe, TemporalModelReadout, assess_readout
from evomem.simulation import Corruption, project


class VisibleClient(ScriptClient):
    def generate(self, request: ModelRequest) -> ModelResponse:
        if request.schema_version.startswith("point-"):
            raw = json.loads(request.user)
            targets = [r for r in raw["records"] if r["kind"] != "source"]
            supports = [
                {
                    "target_id": r["id"],
                    "decision": "specified",
                    "groups": [
                        {
                            "members": list(r["source_ids"]),
                            "relation": "necessary",
                            "sufficient": True,
                            "confidence": 0.9,
                        }
                    ],
                }
                for r in targets
            ]
            self.requests.append(request)
            return ModelResponse(
                json.dumps({"assessments": supports}),
                self.identity,
                str(len(self.requests)),
                12,
                0,
                6,
                None,
                1,
                "stop",
                {"input_tokens": 12, "output_tokens": 6},
                {},
            )
        if request.schema_version.startswith(("readout", "query-audit")):
            raw = json.loads(request.user)
            source = next(
                r
                for r in raw["records"]
                if r["kind"] == "source"
                and r["status"] == "active"
                and (
                    r["id"] == "u"
                    if raw["target_id"] == "v"
                    else r["id"].startswith("s")
                )
            )
            text = {"answer": source["text"], "cited_ids": [source["id"]]}
            if request.schema_version.startswith("query-audit"):
                text = {
                    "answer": source["text"],
                    "verdict": "supported",
                    "evidence_ids": [source["id"]],
                }
            self.requests.append(request)
            return ModelResponse(
                json.dumps(text),
                self.identity,
                str(len(self.requests)),
                12,
                0,
                6,
                None,
                1,
                "stop",
                {"input_tokens": 12, "output_tokens": 6},
                {},
            )
        return super().generate(request)


SPECS = (
    Derivation("t", "State Zorvia's protocol.", ("s0",), "v1"),
    Derivation("v", "State Tovren's protocol.", ("u",), "v1"),
)


def test_all_arms_share_accounting_and_b8_commits_generated_text(
    tmp_path: Path,
) -> None:
    runs = run_arms(
        nonce_scenario(),
        ARMS,
        VisibleClient(),
        tmp_path / "arms",
        Budget(max_model_calls=10),
        embedding_backend=FakeEmbedding(),
        derivations=SPECS,
    )
    for name, result in runs.items():
        report = result.report()
        assert name in report["cache_namespace"]
        assert report["charged_usage"] == report["physical_usage"]
        assert report["physical_phase_latency_ms"] >= 0
    for name in ["B5a", "B5b", "B7", "B9"]:
        assert runs[name].report()["charged_usage"]["model_calls"] == 2
        assert runs[name].report()["charged_usage"]["dependency_checks"] > 0
    assert runs["B4b"].report()["charged_usage"]["embedding_calls"] > 0
    assert runs["B8"].trace.answer("t", 2) == "Project Zorvia uses protocol K29."
    assert runs["B8"].report()["charged_usage"]["model_calls"] == 3
    assert runs["B8"].report()["charged_usage"]["cache_hits"] == 1
    audit = runs["B10"].reader()
    before = runs["B10"].trace
    first = audit.answer(ReadoutProbe("t", 2))
    audit.answer(ReadoutProbe("t", 2))
    assert (
        runs["B10"].trace == before
        and before.answer("t", 2) == "Project Zorvia uses protocol K17."
    )
    assert runs["B10"].report()["charged_usage"]["verification_calls"] == 2
    outcome = assess_readout(
        first,
        expected_answer="Project Zorvia uses protocol K29.",
        memory_state_correct=False,
        required_retrieval=frozenset({"s2"}),
    )
    assert (
        outcome.answer_correct
        and outcome.retrieval_correct
        and not outcome.memory_state_correct
    )
    with pytest.raises(FileExistsError):
        run_arms(nonce_scenario(), ARMS, VisibleClient(), tmp_path / "arms", Budget())


def test_shared_construction_is_allocated_to_every_recipient_and_capped(
    tmp_path: Path,
) -> None:
    scenario = nonce_scenario()
    reference = run_arms(
        scenario, ("B10",), VisibleClient(), tmp_path / "reference", Budget()
    )["B10"]
    recipients = frozenset({"B5a", "B5b", "B7", "B9"})
    maker = ModelExecutor(VisibleClient(), Ledger(Budget()))
    shared = {
        v.checkpoint: SharedSupports.construct(v, maker, recipients)
        for v in reference.session.frames
        if v.checkpoint
    }
    runs = run_arms(
        scenario,
        tuple(sorted(recipients)),
        VisibleClient(),
        tmp_path / "shared",
        Budget(max_model_calls=2),
        shared=shared,
        credit_schedule=((1, 1), (2, 1)),
    )
    for result in runs.values():
        report = result.report()
        assert report["charged_usage"]["model_calls"] == 2
        assert report["physical_usage"]["model_calls"] == 0
        assert report["charged_usage"]["input_tokens"] == 24
        assert len(report["shared_preprocessing_received"]) == 2
    blocked = run_arms(
        scenario,
        tuple(sorted(recipients)),
        VisibleClient(),
        tmp_path / "blocked",
        Budget(max_model_calls=0),
        shared=shared,
    )
    assert all(
        r.trace.decisions[0].completion == "budget_exhausted" for r in blocked.values()
    )
    with pytest.raises(ValueError, match="Every applicable"):
        run_arms(
            scenario,
            ("B7",),
            VisibleClient(),
            tmp_path / "wrong",
            Budget(),
            shared=shared,
        )
    with pytest.raises(ValueError, match="construction costs"):
        replace(shared[1], costs=())
    wrong = dict(shared)
    wrong[1] = replace(shared[1], prefix="different")
    with pytest.raises(ValueError, match="mismatch"):
        run_arms(
            scenario,
            tuple(sorted(recipients)),
            VisibleClient(),
            tmp_path / "wrong-prefix",
            Budget(),
            shared=wrong,
        )


def test_credit_release_carry_and_unused_token_reservation(tmp_path: Path) -> None:
    ledger = Ledger(
        Budget(max_model_calls=3, max_input_tokens=30, max_output_tokens=30),
        credit_schedule=((1, 1), (2, 1), (3, 1)),
    )
    client = FakeClient([response(), response(), response()])
    ex = ModelExecutor(client, ledger, tmp_path)
    request = replace(
        request_for(
            project(
                nonce_scenario(),
                Snapshot(0, nonce_scenario().initial),
                nonce_scenario().revisions[0],
                (),
                InformationAccess(),
                Corruption(),
            )
        ),
        input_reservation=20,
        max_output_tokens=10,
    )
    with pytest.raises(BudgetExceededError):
        ex.generate(request, 1, "test")
    ledger.release(1)
    ex.generate(request, 1, "test")
    used = ledger.totals().copy()
    ex.generate(request, 1, "test")  # cache hit at exhausted call credit
    assert ledger.totals()["model_calls"] == used["model_calls"] == 1
    assert ledger.totals()["input_tokens"] == used["input_tokens"]
    with pytest.raises(BudgetExceededError):
        ex.generate(replace(request, user="different"), 1, "test")
    ledger.release(2)
    ledger.release(3)  # carry unused second-revision credit
    ex.generate(replace(request, user="different"), 3, "test")
    assert len(client.requests) == 2
    assert ledger.totals()["input_tokens"] == 20  # actual 10, not reserved 20
    assert ledger.released_calls == 3
    with pytest.raises(ValueError):
        ledger.release(2)
    with pytest.raises(ValueError, match="Negative"):
        ledger.charge(CostEvent("refund", "test", 3, input_tokens=-10))


@pytest.mark.parametrize("kind", ["supersession", "correction", "permission"])
def test_historical_binding_matches_existing_semantics_without_future_leak(
    tmp_path: Path, kind: str
) -> None:
    client = VisibleClient()
    result = run_arms(
        nonce_scenario(kind), ("B10",), client, tmp_path / kind, Budget()
    )["B10"]
    reader = result.reader(False)
    then = reader.answer(ReadoutProbe("t", 2, time_view="historical_then", as_of=1))
    now = reader.answer(ReadoutProbe("t", 2, time_view="historical_now", as_of=1))
    assert (then.answer is None) == (kind == "permission")
    assert (now.answer is None) == (kind != "supersession")
    other = reader.answer(ReadoutProbe("v", 2, time_view="historical_then", as_of=1))
    assert other.answer == "Project Tovren uses protocol M83."
    for request in client.requests:
        assert "K29" not in request.user and '"s2"' not in request.user
        assert "expected" not in request.user and "rules" not in request.user
    assert result.trace.snapshots[1].items == result.session.frames[1].items


def test_future_records_supports_and_oracle_prefixes_are_protocol_violations(
    tmp_path: Path,
) -> None:
    client = VisibleClient()
    result = run_arms(nonce_scenario(), ("B10",), client, tmp_path / "base", Budget())[
        "B10"
    ]
    old = result.session.frames[1]
    poisoned = [
        replace(
            old,
            items=old.items
            + (Memory("future", "LEAK", "lab", created_at_checkpoint=2),),
        ),
        replace(
            old, lineage=old.lineage + (Support("future", "t", ("s2",), valid_from=2),)
        ),
        replace(old, access=InformationAccess(gold_dependencies=True)),
    ]
    for bad in poisoned:
        frames = (result.session.frames[0], bad, result.session.frames[2])
        answer = TemporalModelReadout(
            result.session.executor, frames, result.trace.revisions
        ).answer(ReadoutProbe("t", 2, time_view="historical_then", as_of=1))
        assert answer.completion == "protocol_violation"
        assert not assess_readout(
            answer,
            expected_answer=None,
            memory_state_correct=True,
            required_retrieval=None,
        ).answer_correct
    assert not client.requests


def test_embedding_and_model_cache_identity_changes_are_material(
    tmp_path: Path,
) -> None:
    backend = FakeEmbedding()
    ledger = Ledger(Budget())
    cache = EmbeddingCache(backend, tmp_path / "embedding")
    cache.vector("K17", ledger, 1)
    cache.vector("K17", ledger, 2)
    cache.vector("K29", ledger, 2)
    backend.identity = "different-model-revision"
    cache.vector("K29", ledger, 2)
    assert (
        ledger.totals()["embedding_calls"] == 3 and ledger.totals()["cache_hits"] == 1
    )
    client = VisibleClient()
    request = ModelRequest("system", "input", "{}", "v1")
    key = cache_key(client, request)
    client.identity = replace(
        client.identity, deployment="different-quantization/runtime"
    )
    assert cache_key(client, request) != key


def test_transport_failure_cost_remains_in_arm_report(tmp_path: Path) -> None:
    result = run_arms(
        nonce_scenario(),
        ("B5b",),
        FakeClient([ModelCallError("model_timeout")]),
        tmp_path / "failed",
        Budget(max_input_tokens=20000),
    )["B5b"]
    report = result.report()
    assert report["charged_usage"]["input_tokens"] is None
    assert report["charged_usage"]["model_calls"] == 1
    assert result.trace.decisions[0].completion == "model_failed"


def test_b8_cannot_receive_an_uncharged_privileged_dependency(tmp_path: Path) -> None:
    client = VisibleClient()
    with pytest.raises(ValueError, match="visible provenance"):
        run_arms(
            nonce_scenario(),
            ("B8",),
            client,
            tmp_path / "hidden-graph",
            Budget(),
            derivations=(replace(SPECS[0], dependencies=("u",)),),
        )
    assert not client.requests
