"""Synthetic labels only; never fills the real annotation forms."""

import csv
import importlib.util
import json
from pathlib import Path

import pytest

SPEC = importlib.util.spec_from_file_location(
    "agreement", Path(__file__).parents[1] / "scripts/analyze_annotation_agreement.py"
)
agreement = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(agreement)


def dummy():
    return {
        "schema_version": "1.0",
        "annotator_id": "A",
        "case_id": "DUMMY",
        "checkpoint": "t0",
        "evidence_json": json.dumps(
            [
                {"record_id": "S1@0", "text": "Synthetic input one"},
                {"record_id": "S2@0", "text": "Synthetic input two"},
            ]
        ),
        "claims_json": json.dumps([{"claim_id": "B1", "text": "Dummy claim"}]),
        "tasks_json": json.dumps({"permitted_time_views": ["current"]}),
        "belief_states_json": json.dumps(
            [
                {
                    "claim_id": "B1",
                    "time_view": "current",
                    "truth_status": "SUPPORTED",
                    "use_status": "USABLE",
                    "action": "RETAIN",
                }
            ]
        ),
        "relations_json": json.dumps(
            [{"members": ["S1@0"], "target": "B1", "labels": ["necessary"]}]
        ),
        "support_sets_json": json.dumps(
            [
                {
                    "claim_id": "B1",
                    "assessment": "SPECIFIED",
                    "sets": [{"members": ["S1@0"], "basis": "DIRECT"}],
                }
            ]
        ),
        "affected_beliefs_json": "[]",
        "preserved_beliefs_json": "[]",
        "historical_valid_beliefs_json": "[]",
        "ambiguous_relationships_json": "[]",
        "notes": "Synthetic fixture, not human data",
    }


def save_pair(tmp_path, first=None, second=None):
    first = first or dummy()
    second = second or first.copy()
    second = second | {"annotator_id": "B"}
    paths = []
    for who, row in [("A", first), ("B", second)]:
        path = tmp_path / (who + ".csv")
        with path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(row), lineterminator="\n")
            writer.writeheader()
            writer.writerow(row)
        paths.append(path)
    return paths


def test_kappa_known_value():
    pairs = [("Y", "Y")] * 4 + [("N", "N")] * 4 + [("Y", "N"), ("N", "Y")]
    result = agreement.categorical(pairs)
    assert result["raw_agreement"] == 0.8
    assert result["kappa"] == pytest.approx(0.6)


def test_constant_kappa_is_undefined():
    assert agreement.categorical([("Y", "Y")])["kappa"] is None
    assert agreement.categorical([])["raw_agreement"] is None


def test_directional_overlap_and_empty():
    result = agreement.set_score({1, 2}, {2, 3, 4})
    assert result["B_precision_ref_A"] == pytest.approx(1 / 3)
    assert result["B_recall_ref_A"] == 0.5
    assert result["symmetric_F1"] == 0.4
    assert agreement.set_score(set(), set())["symmetric_F1"] is None
    assert agreement.set_score({1}, set())["symmetric_F1"] == 0


def test_complete_inputs_and_no_mutation(tmp_path):
    paths = save_pair(tmp_path)
    before = [p.read_bytes() for p in paths]
    result = agreement.analyze(*paths)
    assert result["raw_exact_row_agreement"] == 1
    assert result["scenario_macro_support_sets"]["value"] == 1
    assert [p.read_bytes() for p in paths] == before


def test_and_or_have_same_edges_different_sets(tmp_path):
    a, b = dummy(), dummy()
    a["support_sets_json"] = json.dumps(
        [
            {
                "claim_id": "B1",
                "assessment": "SPECIFIED",
                "sets": [{"members": ["S1@0", "S2@0"], "basis": "DIRECT"}],
            }
        ]
    )
    b["support_sets_json"] = json.dumps(
        [
            {
                "claim_id": "B1",
                "assessment": "SPECIFIED",
                "sets": [{"members": [s], "basis": "DIRECT"} for s in ["S1@0", "S2@0"]],
            }
        ]
    )
    result = agreement.analyze(*save_pair(tmp_path, a, b))
    assert result["sets"]["support_edges"]["micro_F1"] == 1
    assert result["sets"]["support_sets"]["micro_F1"] == 0
    assert result["raw_exact_row_agreement"] == 0


def test_member_order_ignored(tmp_path):
    a, b = dummy(), dummy()
    for row, members in [(a, ["S1@0", "S2@0"]), (b, ["S2@0", "S1@0"])]:
        row["support_sets_json"] = json.dumps(
            [
                {
                    "claim_id": "B1",
                    "assessment": "SPECIFIED",
                    "sets": [{"members": members, "basis": "DIRECT"}],
                }
            ]
        )
    assert agreement.analyze(*save_pair(tmp_path, a, b))["raw_exact_row_agreement"] == 1


def test_unknown_is_not_imputed_as_empty_support(tmp_path):
    a, b = dummy(), dummy()
    b["support_sets_json"] = json.dumps(
        [{"claim_id": "B1", "assessment": "UNKNOWN", "sets": []}]
    )
    result = agreement.analyze(*save_pair(tmp_path, a, b))
    assert result["sets"]["support_sets"]["units"] == 0
    assert result["uncertainty_counts"]["unknown_support_targets"] == 1
    assert result["raw_exact_row_agreement"] == 0


def test_blank_rejected_and_partial_explicit(tmp_path):
    a = dummy()
    a["belief_states_json"] = ""
    paths = save_pair(tmp_path, a)
    with pytest.raises(ValueError, match="incomplete"):
        agreement.analyze(*paths)
    result = agreement.analyze(*paths, allow_partial=True)
    assert result["paired_rows"] == 0
    assert result["raw_exact_row_agreement"] is None
    assert result["status"] == "EXPLORATORY_PARTIAL"


def test_evidence_mismatch_rejected(tmp_path):
    a, b = dummy(), dummy()
    b["evidence_json"] = "[]"
    with pytest.raises(ValueError, match="observed case text differs"):
        agreement.analyze(*save_pair(tmp_path, a, b))


def test_duplicate_state_rejected(tmp_path):
    a = dummy()
    states = json.loads(a["belief_states_json"])
    a["belief_states_json"] = json.dumps(states + states)
    with pytest.raises(ValueError, match="duplicate"):
        agreement.analyze(*save_pair(tmp_path, a))


def test_future_reference_rejected(tmp_path):
    a = dummy()
    a["relations_json"] = json.dumps(
        [{"members": ["S1@3"], "target": "B1", "labels": ["necessary"]}]
    )
    with pytest.raises(ValueError, match="unknown IDs"):
        agreement.analyze(*save_pair(tmp_path, a))


def test_explicit_empty_vs_missing_distinguished(tmp_path):
    a, b = dummy(), dummy()
    b["relations_json"] = "[]"
    result = agreement.analyze(*save_pair(tmp_path, a, b))
    assert result["sets"]["relations"]["micro_F1"] == 0
    assert result["paired_rows"] == 1


def test_historical_status_and_revision_sets(tmp_path):
    a, b = dummy(), dummy()
    for row in [a, b]:
        row["checkpoint"] = "t1"
        row["tasks_json"] = json.dumps(
            {"permitted_time_views": ["current", "historical_then", "historical_now"]}
        )
        states = json.loads(row["belief_states_json"])
        states += [
            {
                "claim_id": "B1",
                "time_view": view,
                "truth_status": "SUPPORTED",
                "use_status": "USABLE",
                "action": None,
            }
            for view in ["historical_then", "historical_now"]
        ]
        row["belief_states_json"] = json.dumps(states)
        row["preserved_beliefs_json"] = '["B1"]'
        row["historical_valid_beliefs_json"] = '["B1"]'
    states = json.loads(b["belief_states_json"])
    states[-1]["truth_status"] = "CONTRADICTED"
    b["belief_states_json"] = json.dumps(states)
    b["historical_valid_beliefs_json"] = "[]"
    result = agreement.analyze(*save_pair(tmp_path, a, b))
    assert result["categorical"]["historical_then_truth"]["raw_agreement"] == 1
    assert result["categorical"]["historical_now_truth"]["raw_agreement"] == 0
    assert result["sets"]["historical_valid"]["micro_F1"] == 0
    assert result["sets"]["preserved"]["micro_F1"] == 1


def test_empty_sets_not_inflated_to_perfect_f1():
    result = agreement.summarize_sets([(set(), set()), ({1}, {2})])
    assert result["exact_agreement"] == 0.5
    assert result["both_empty"] == 1
    assert result["macro_F1_nonempty"] == 0
