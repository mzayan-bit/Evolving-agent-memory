"""Scientific invariants, including deliberately failing weak baseline behavior."""

import json
from dataclasses import FrozenInstanceError, asdict, replace
from pathlib import Path

import pytest

from evomem.cost import Budget, BudgetExceededError, CostEvent, Ledger
from evomem.data import load_adjudicated, validate
from evomem.evaluation import Gold, Probe, Rate, aggregate, score
from evomem.experiment.run import execute
from evomem.fixtures import FIXTURES, fixture
from evomem.model import (
    InformationAccess,
    Memory,
    Relation,
    Status,
    Support,
    grounded,
    independent_origins,
)
from evomem.policies import BASELINES, Baseline, RecordedInference
from evomem.simulation import Corruption, Trace, corrupt, project, run


def trajectory(
    name: str,
    policy: str = "B2",
    budget: Budget | None = None,
    corruption: Corruption | None = None,
) -> tuple[Trace, Gold, Ledger]:
    scenario, gold = fixture(name)
    ledger = Ledger(budget or Budget())
    trace = run(
        scenario,
        Baseline(policy, RecordedInference()),
        InformationAccess(),
        ledger,
        corruption,
    )
    return trace, gold, ledger


@pytest.mark.parametrize("name", FIXTURES)
def test_replay_recovers_all_fixture_current_and_historical_answers(name: str) -> None:
    scenario, _ = fixture(name)
    trace, gold, ledger = trajectory(name)
    validate(scenario, gold)
    for probe in gold.probes:
        assert (
            trace.answer(probe.item_id, probe.checkpoint, probe.view, probe.as_of)
            == probe.expected
        )
    assert ledger.totals()["model_calls"] == 0
    assert ledger.totals()["input_tokens"] == 0


@pytest.mark.parametrize("policy", BASELINES)
def test_snapshots_are_immutable_and_no_future_views(policy: str) -> None:
    scenario, _ = fixture("repeated")
    trace, _, _ = trajectory("repeated", policy)
    assert trace.snapshots[0].items == scenario.initial
    assert len(trace.snapshots) == 3
    assert trace.snapshots[1].items[0].valid_until == 1
    with pytest.raises(FrozenInstanceError):
        setattr(trace.snapshots[0].items[0], "content" + "", "changed")
    with pytest.raises(ValueError):
        trace.answer("b1", 1, "historical_then", 2)


def test_and_or_and_copies_not_confused() -> None:
    for name, active in [
        ("alternative", True),
        ("conjunction", False),
        ("copies", False),
    ]:
        trace, _, _ = trajectory(name, "B7")
        assert (trace.answer("b1", 1) is not None) is active
    assert independent_origins((frozenset({"x"}), frozenset({"y"})))
    assert not independent_origins((frozenset({"x"}), frozenset({"x"})))
    assert not independent_origins((frozenset(), frozenset({"x"})))


def test_no_repair_locality_and_source_only() -> None:
    for policy in ("B0", "B1"):
        trace, _, _ = trajectory("necessary", policy)
        assert trace.answer("b1", 1) == trace.answer("b1", 0)
        assert trace.snapshots[0].items[2:] == trace.snapshots[1].items[2:4]
    assert trajectory("necessary", "B0")[0].decisions[0].actions == ()
    assert trajectory("necessary", "B1")[0].decisions[0].actions


def test_missing_edges_not_magically_repaired_and_gold_unchanged() -> None:
    scenario, gold = fixture("necessary")
    hidden = replace(
        scenario, observed=tuple(s for s in scenario.observed if s.target != "b1")
    )
    ledger = Ledger(Budget())
    trace = run(
        hidden, Baseline("B3", RecordedInference()), InformationAccess(), ledger
    )
    metrics = score(gold, trace)
    assert metrics["stale_reuse"] == Rate(1, 1)
    assert len(gold.supports) == 2
    oracle = run(
        hidden,
        Baseline("B3", RecordedInference()),
        InformationAccess(gold_dependencies=True),
        Ledger(Budget()),
        oracle=gold.supports,
    )
    assert oracle.answer("b1", 1) is None


def test_policy_view_has_no_gold_or_future_and_flags_redact_all_paths() -> None:
    scenario, gold = fixture("repeated")
    trace, _, _ = trajectory("repeated")
    access = InformationAccess(
        source_provenance=False, authority_labels=False, full_history=False
    )
    view = project(
        scenario,
        trace.snapshots[1],
        scenario.revisions[0],
        trace.snapshots,
        access,
        Corruption(hide_fault=True),
    )
    payload = json.dumps(asdict(view))
    assert not hasattr(view, "gold") and not hasattr(view, "affected")
    assert "s4" not in payload and "q9" not in payload
    assert view.revision.before == "" and view.revision.fault_cue is None
    assert view.history == ()
    assert all(
        not m.source_ids and not m.origin_ids and m.authority is None
        for m in view.items + (view.revision.after,)
    )
    changed_gold = replace(gold, supports=())
    assert changed_gold != gold
    assert (
        project(
            scenario,
            trace.snapshots[1],
            scenario.revisions[0],
            trace.snapshots,
            access,
            Corruption(hide_fault=True),
        )
        == view
    )
    with pytest.raises(ValueError, match="oracle"):
        project(
            scenario,
            trace.snapshots[1],
            scenario.revisions[0],
            (),
            InformationAccess(gold_dependencies=True),
            Corruption(),
        )


def test_spurious_edges_and_semantic_neighbors_damage_bystander() -> None:
    scenario, gold = fixture("semantic_bystander")
    injected = Support("false", "b2", ("s1",), scope="other")
    trace = run(
        scenario,
        Baseline("B3", RecordedInference()),
        InformationAccess(),
        Ledger(Budget()),
        Corruption(spurious=(injected,)),
    )
    assert score(gold, trace)["false_invalidation"] == Rate(1, 1)
    semantic, _, _ = trajectory("semantic_bystander", "B4")
    assert score(gold, semantic)["false_invalidation"] == Rate(1, 1)
    replay, _, _ = trajectory("semantic_bystander")
    assert replay.answer("b2", 1) is not None


def test_corruption_seeded_and_gold_not_mutated() -> None:
    scenario, gold = fixture("conjunction")
    config = Corruption(seed=7, drop_count=1, change_type=True)
    before = gold.supports
    assert corrupt(scenario.observed, config) == corrupt(scenario.observed, config)
    assert sum(len(s.members) for s in corrupt(scenario.observed, config)) == 2
    assert gold.supports == before
    assert any(
        s.relation == Relation.ASSOCIATION for s in corrupt(scenario.observed, config)
    )


def test_unsupported_cycles_and_empty_support_not_axioms() -> None:
    items = (Memory("a", "a", "demo"), Memory("b", "b", "demo"))
    rules = (Support("j1", "a", ("b",)), Support("j2", "b", ("a",)))
    assert grounded(items, rules, 0) == frozenset()
    with pytest.raises(ValueError):
        Support("j", "a", ())
    with pytest.raises(ValueError):
        Support("j", "a", ("b",), Relation.UNKNOWN)


def test_atomic_replay_exhaustion_and_unchecked_reverification() -> None:
    trace, _, ledger = trajectory("necessary", budget=Budget(max_replay_steps=1))
    assert trace.decisions[0].completion == "budget_exhausted"
    assert trace.answer("b1", 1) is not None
    assert ledger.totals()["replay_steps"] == 1
    trace, gold, ledger = trajectory(
        "necessary", "B6", Budget(max_verification_calls=1)
    )
    assert trace.decisions[0].completion == "budget_exhausted"
    assert trace.decisions[0].checked == ("b1",)
    assert score(gold, trace)["reverify_coverage"] == Rate(1, 2)
    assert trace.answer("b2", 1) is not None


def test_ledger_exact_counts_retry_unknown_and_hard_caps() -> None:
    events = [
        CostEvent(
            "v",
            "verify",
            1,
            model_calls=1,
            input_tokens=100,
            output_tokens=20,
            cached_input_tokens=40,
            verification_calls=1,
            usage_source="synthetic",
        ),
        CostEvent(
            "r1",
            "replay",
            1,
            model_calls=1,
            input_tokens=50,
            output_tokens=10,
            replay_steps=1,
            usage_source="synthetic",
        ),
        CostEvent(
            "r2",
            "replay",
            1,
            model_calls=1,
            input_tokens=30,
            output_tokens=5,
            parent_operation_id="r1",
            usage_source="synthetic",
        ),
    ]
    ledger = Ledger(Budget())
    for event in events:
        ledger.charge(event)
    totals = ledger.totals()
    assert (
        totals["model_calls"],
        totals["input_tokens"],
        totals["output_tokens"],
        totals["cached_input_tokens"],
        totals["verification_calls"],
        totals["replay_steps"],
    ) == (3, 180, 35, 40, 1, 1)
    capped = Ledger(Budget(max_model_calls=2))
    for event in events[:2]:
        capped.charge(event)
    with pytest.raises(BudgetExceededError):
        capped.charge(events[2])
    assert len(capped.events) == 2
    ledger.charge(
        CostEvent(
            "failed",
            "verify",
            2,
            model_calls=1,
            input_tokens=None,
            output_tokens=None,
            usage_source="unknown",
            status="failed",
        )
    )
    ledger.charge(
        replace(events[0], operation_id="retry", parent_operation_id="failed")
    )
    assert ledger.totals()["model_calls"] == 5
    assert ledger.totals()["input_tokens"] is None
    with pytest.raises(BudgetExceededError):
        Ledger(Budget(max_tokens=119)).charge(events[0])
    with pytest.raises(ValueError):
        ledger.charge(events[0])


def test_denominators_do_not_depend_on_retrieval_or_zero_actions() -> None:
    trace, gold, _ = trajectory("necessary", "B0")
    doubled = replace(
        gold, probes=gold.probes + (replace(gold.probes[0], probe_id="extra"),)
    )
    assert score(doubled, trace)["stale_reuse"] == Rate(2, 2)
    assert score(gold, trace)["repair_precision"].rate is None
    trace, gold, _ = trajectory("alternative", "B7")
    assert score(gold, trace)["stale_reuse"].rate is None
    assert score(gold, trace)["independent_support_retention"] == Rate(1, 1)


def test_recurrence_detected_but_legitimate_reinstatement_excluded() -> None:
    trace, gold, _ = trajectory("repeated")
    assert score(gold, trace)["recurrence"] == Rate(0, 0)
    # Inject a later stale write into a separate synthetic continuation.
    old_label = gold.checkpoints[0]
    labels = (old_label, replace(old_label, checkpoint=2))
    altered = replace(gold, checkpoints=labels, probes=(Probe("later", 2, "b1", None),))
    assert score(altered, trace)["recurrence"] == Rate(1, 1)


def test_cluster_macro_does_not_count_variants_as_independent_samples() -> None:
    rows = [
        ("case1", "seed1", {"m": Rate(1, 1)}),
        ("case1", "seed2", {"m": Rate(1, 1)}),
        ("case2", "seed1", {"m": Rate(0, 1)}),
    ]
    result = aggregate(rows)["m"]
    assert result["macro_rate"] == 0.5 and result["eligible_clusters"] == 2
    with pytest.raises(ValueError, match="Duplicate"):
        aggregate(rows + rows[:1])


def test_importer_explicit_adjudication_and_roundtrip(tmp_path: Path) -> None:
    scenario, gold = fixture("necessary")

    def encode(value: object) -> object:
        if isinstance(value, frozenset):
            return sorted(value)
        raise TypeError()

    payload = {
        "schema_version": "g1-adjudicated-1",
        "status": "ADJUDICATED",
        "adjudication": {
            "reviewer": "SYNTHETIC_TEST",
            "agreement_report": "test",
            "protocol_version": "test",
        },
        "scenario": asdict(scenario),
        "gold": asdict(gold),
    }
    path = tmp_path / "synthetic.json"
    path.write_text(json.dumps(payload, default=encode))
    assert load_adjudicated(path) == (scenario, gold)
    payload["status"] = "PENDING"
    path.write_text(json.dumps(payload, default=encode))
    with pytest.raises(ValueError, match="adjudicated"):
        load_adjudicated(path)


def test_validation_rejects_impossible_references_and_views() -> None:
    scenario, gold = fixture("necessary")
    with pytest.raises(ValueError, match="Duplicate memory"):
        validate(replace(scenario, initial=scenario.initial * 2), gold)
    with pytest.raises(ValueError, match="reference"):
        validate(replace(scenario, observed=(Support("bad", "b1", ("absent",)),)), gold)
    with pytest.raises(ValueError, match="ordering"):
        validate(
            replace(
                scenario, revisions=(replace(scenario.revisions[0], checkpoint=3),)
            ),
            gold,
        )
    with pytest.raises(ValueError, match="historical"):
        validate(
            scenario,
            replace(gold, probes=(Probe("bad", 1, "b1", None, "historical_then", 2),)),
        )


def test_cli_artifacts_and_pilot_gate(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Real pilot disabled"):
        execute({"mode": "PILOT"})
    output = execute(
        {
            "mode": "ENGINEERING_ONLY",
            "experiment_id": "test-run",
            "allow_dirty": True,
            "output_root": str(tmp_path),
            "policies": ["B2"],
            "fixtures": ["necessary"],
        }
    )
    manifest = json.loads((output / "manifest.json").read_text())
    assert manifest["model_identifiers"] == []
    assert manifest["status"] == "ENGINEERING_ONLY_NO_RESEARCH_FINDINGS"
    assert (output / "per_scenario.jsonl").exists()
    assert len(manifest["artifacts"]) == 3


def test_unknown_relation_is_quarantined_not_declared_false() -> None:
    scenario, gold = fixture("necessary")
    unknown = Support("unknown", "b1", ("s1",), Relation.UNKNOWN, sufficient=False)
    scenario = replace(scenario, observed=(unknown, scenario.observed[1]))
    trace = run(
        scenario,
        Baseline("B7", RecordedInference()),
        InformationAccess(),
        Ledger(Budget()),
    )
    assert trace.snapshots[1].items[2].status == Status.QUARANTINED
    assert score(gold, trace)["repair_precision"].rate is None


def test_retrospective_correction_rescues_independent_alternative() -> None:
    scenario, _ = fixture("alternative")
    scenario = replace(
        scenario, revisions=(replace(scenario.revisions[0], kind="correction"),)
    )
    trace = run(
        scenario,
        Baseline("B2", RecordedInference()),
        InformationAccess(),
        Ledger(Budget()),
    )
    assert trace.answer("b1", 1, "historical_now", 0) == "production capacity four"
    correction, _, _ = trajectory("correction")
    assert correction.answer("b1", 1, "historical_then", 0) is not None
    assert correction.answer("b1", 1, "historical_now", 0) is None


@pytest.mark.parametrize(
    "resource", ["verification_calls", "replay_steps", "model_calls", "retrieval_calls"]
)
def test_each_resource_cap_is_binding(resource: str) -> None:
    budget = Budget(**{"max_" + resource: 0})
    event = CostEvent(
        "op",
        "test",
        1,
        usage_source="synthetic",
        verification_calls=int(resource == "verification_calls"),
        replay_steps=int(resource == "replay_steps"),
        model_calls=int(resource == "model_calls"),
        retrieval_calls=int(resource == "retrieval_calls"),
    )
    with pytest.raises(BudgetExceededError):
        Ledger(budget).charge(event)


def test_inference_provider_can_be_crossed_with_graph_and_support_policy() -> None:
    class EmptyInference:
        def infer(self, view: object) -> tuple[tuple[Support, float], ...]:
            return ()

    scenario, _ = fixture("necessary")
    graph = run(
        scenario,
        Baseline("B5", EmptyInference()),
        InformationAccess(),
        Ledger(Budget()),
    )
    sets = run(
        scenario,
        Baseline("B7", EmptyInference()),
        InformationAccess(),
        Ledger(Budget()),
    )
    assert graph.answer("b1", 1) is not None
    assert sets.snapshots[1].items[2].status == Status.QUARANTINED
