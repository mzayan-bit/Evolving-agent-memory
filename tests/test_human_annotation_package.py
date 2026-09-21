"""Release-boundary and preservation checks, not human reliability estimates."""

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]
PACKAGE = ROOT / "research/human_annotation"
LABELS = [
    "belief_states_json",
    "relations_json",
    "support_sets_json",
    "affected_beliefs_json",
    "preserved_beliefs_json",
    "historical_valid_beliefs_json",
    "ambiguous_relationships_json",
    "notes",
]


def rows(path):
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def test_blank_forms_identical_except_identifier():
    a = rows(PACKAGE / "annotator_A.csv")
    b = rows(PACKAGE / "annotator_B.csv")
    assert len(a) == len(b) == 120
    assert len({r["case_id"] for r in a}) == 30
    for x, y in zip(a, b, strict=True):
        assert x.pop("annotator_id") == "A"
        assert y.pop("annotator_id") == "B"
        assert x == y
        assert all(x[field] == "" for field in LABELS)


def test_release_packets_are_prefix_only():
    for who in ["A", "B"]:
        masters = rows(PACKAGE / f"annotator_{who}.csv")
        order = None
        for stage in range(4):
            packet = rows(PACKAGE / "packets" / who / f"stage_{stage}.csv")
            assert len(packet) == 30
            assert packet == [r for r in masters if r["checkpoint"] == f"t{stage}"]
            ids = [r["case_id"] for r in packet]
            assert order is None or ids == order
            order = ids
            for row in packet:
                for record in json.loads(row["evidence_json"]):
                    assert record["observed_at"] <= f"t{stage}"
                    assert set(record) == {
                        "record_id",
                        "source_id",
                        "observed_at",
                        "text",
                    }
                for claim in json.loads(row["claims_json"]):
                    assert set(claim) == {"claim_id", "text"}
                assert "G1-" not in row["case_id"]
                assert "STALE" not in row["evidence_json"]


def test_authored_originals_unchanged_and_mapping_bijective():
    manifest = json.loads((PACKAGE / "coordinator_only/case_mapping.json").read_text())
    assert len(manifest["mapping"]) == 30
    assert len({m["case_id"] for m in manifest["mapping"]}) == 30
    for item in manifest["mapping"]:
        name = item["source_case"] + ".json"
        original = ROOT / "research/g1/annotations/scenarios" / name
        saved = PACKAGE / "coordinator_only/authored_originals" / name
        assert original.read_bytes() == saved.read_bytes()
        assert (
            hashlib.sha256(original.read_bytes()).hexdigest() == item["source_sha256"]
        )
        assert set(item["source_id_map"]) == {"A", "B"}
        assert set(item["claim_id_map"]) == {"C", "D", "U"}
