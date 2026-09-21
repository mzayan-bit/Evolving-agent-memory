#!/usr/bin/env python3
"""Deterministic human agreement analysis; no model calls or label inference."""

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

TRUTH = {
    "SUPPORTED",
    "CONTRADICTED",
    "INSUFFICIENT",
    "CONFLICTING",
    "UNKNOWN_AMBIGUOUS",
}
USE = {"USABLE", "NOT_USABLE", "UNKNOWN"}
ACTIONS = {"RETAIN", "REVERIFY", "INVALIDATE", "REDERIVE_OR_REPLAY", "UNCERTAIN"}
RELATIONS = {
    "necessary",
    "conjunctive",
    "alternative_sufficient",
    "partial_support",
    "copied_support",
    "correlated_support",
    "temporal_dependency",
    "scoped_dependency",
    "authorization_dependency",
    "association_only",
    "contradiction",
    "unknown_or_ambiguous",
}
BASIS = {"DIRECT", "DERIVED", "MIXED", "UNKNOWN"}
LABEL_FIELDS = [
    "belief_states_json",
    "relations_json",
    "support_sets_json",
    "affected_beliefs_json",
    "preserved_beliefs_json",
    "historical_valid_beliefs_json",
    "ambiguous_relationships_json",
]
OBSERVED_FIELDS = [
    "schema_version",
    "case_id",
    "checkpoint",
    "evidence_json",
    "claims_json",
    "tasks_json",
]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def ratio(numerator, denominator):
    return numerator / denominator if denominator else None


def categorical(pairs):
    """Unweighted Cohen kappa for paired, single categorical labels."""
    n = len(pairs)
    a = Counter(x for x, _ in pairs)
    b = Counter(y for _, y in pairs)
    matches = sum(x == y for x, y in pairs)
    observed = ratio(matches, n)
    expected = sum(a[k] * b[k] for k in a.keys() | b.keys()) / (n * n) if n else None
    kappa = (observed - expected) / (1 - expected) if n and expected < 1 else None
    return {
        "n": n,
        "matches": matches,
        "raw_agreement": observed,
        "kappa": kappa,
        "kappa_note": "undefined"
        if kappa is None
        else "descriptive; nested units are not independent",
        "marginals_A": dict(sorted(a.items())),
        "marginals_B": dict(sorted(b.items())),
        "confusion": {
            canonical([x, y]): count for (x, y), count in sorted(Counter(pairs).items())
        },
    }


def set_score(a, b):
    """Directional overlap, not accuracy against a gold reference."""
    overlap = len(a & b)
    return {
        "A_size": len(a),
        "B_size": len(b),
        "intersection": overlap,
        "B_precision_ref_A": ratio(overlap, len(b)),
        "B_recall_ref_A": ratio(overlap, len(a)),
        "symmetric_F1": ratio(2 * overlap, len(a) + len(b)),
        "exact": a == b,
    }


def summarize_sets(pairs):
    details = [set_score(a, b) for a, b in pairs]
    nonempty = [d["symmetric_F1"] for d in details if d["symmetric_F1"] is not None]
    total_a = sum(d["A_size"] for d in details)
    total_b = sum(d["B_size"] for d in details)
    intersection = sum(d["intersection"] for d in details)
    return {
        "units": len(details),
        "both_empty": sum(not a and not b for a, b in pairs),
        "exact_agreement": ratio(sum(d["exact"] for d in details), len(details)),
        "macro_F1_nonempty": ratio(sum(nonempty), len(nonempty)),
        "micro_F1": ratio(2 * intersection, total_a + total_b),
        "B_precision_ref_A": ratio(intersection, total_b),
        "B_recall_ref_A": ratio(intersection, total_a),
        "A_precision_ref_B": ratio(intersection, total_a),
        "A_recall_ref_B": ratio(intersection, total_b),
        "total_A": total_a,
        "total_B": total_b,
        "intersection": intersection,
    }


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_strings(values, allowed, name):
    require(isinstance(values, list), name + " must be a list")
    require(all(isinstance(x, str) for x in values), name + " must contain strings")
    require(len(set(values)) == len(values), name + " contains duplicates")
    require(set(values) <= allowed, name + " contains unknown IDs/labels")
    return set(values)


def read_form(path):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames is not None, "missing header")
        require(
            len(reader.fieldnames) == len(set(reader.fieldnames)),
            "duplicate CSV columns",
        )
        require(
            set(OBSERVED_FIELDS + LABEL_FIELDS + ["annotator_id", "notes"])
            <= set(reader.fieldnames),
            "missing columns",
        )
        rows = {}
        for raw in reader:
            require(None not in raw, "extra CSV cells")
            key = (raw["case_id"], raw["checkpoint"])
            require(key not in rows, "duplicate case/checkpoint " + str(key))
            require(raw["checkpoint"] in {"t0", "t1", "t2", "t3"}, "invalid checkpoint")
            require(raw["schema_version"] == "1.0", "unsupported schema version")
            for field in ["evidence_json", "claims_json", "tasks_json"]:
                raw[field] = json.loads(raw[field])
            rows[key] = raw
    require(bool(rows), "empty form")
    require(len({r["annotator_id"] for r in rows.values()}) == 1, "mixed annotator IDs")
    return rows


def decode(row):
    """Reject malformed labels and unseen references; never fill blanks."""
    decoded = {f: json.loads(row[f]) for f in LABEL_FIELDS}
    claims = {x["claim_id"] for x in row["claims_json"]}
    evidence = {x["record_id"] for x in row["evidence_json"]}
    require(
        bool(claims) and len(claims) == len(row["claims_json"]),
        "empty/duplicate claim IDs",
    )
    require(len(evidence) == len(row["evidence_json"]), "duplicate evidence IDs")
    for item in row["evidence_json"]:
        if "observed_at" in item:
            require(
                item["observed_at"] <= row["checkpoint"], "future evidence in prefix"
            )
    refs = claims | evidence
    expected = {
        (c, view) for c in claims for view in row["tasks_json"]["permitted_time_views"]
    }
    states = {}
    for item in decoded["belief_states_json"]:
        key = (item["claim_id"], item["time_view"])
        require(
            key not in states and key in expected, "duplicate/unexpected belief state"
        )
        require(
            item["truth_status"] in TRUTH and item["use_status"] in USE,
            "invalid belief status",
        )
        require(
            item["action"] in ACTIONS
            if key[1] == "current"
            else item["action"] is None,
            "invalid action/time view",
        )
        states[key] = (item["truth_status"], item["use_status"], item["action"])
    require(set(states) == expected, "missing belief states")
    rels = {}
    for rel in decoded["relations_json"]:
        members = unique_strings(rel["members"], refs, "relation members")
        require(members and rel["target"] in claims, "invalid relation target/members")
        labels = unique_strings(rel["labels"], RELATIONS, "relation labels")
        require(bool(labels), "empty relation label list")
        key = (tuple(sorted(members)), rel["target"])
        require(key not in rels, "duplicate relation; combine its labels")
        rels[key] = frozenset(labels)
    supports = {}
    for item in decoded["support_sets_json"]:
        target = item["claim_id"]
        require(
            target in claims and target not in supports,
            "invalid/duplicate support target",
        )
        require(
            item["assessment"] in {"SPECIFIED", "NONE_SUFFICIENT", "UNKNOWN"},
            "invalid support assessment",
        )
        sets = {}
        for support in item["sets"]:
            members = unique_strings(support["members"], refs, "support members")
            require(
                bool(members) and support["basis"] in BASIS,
                "empty/invalid sufficient support",
            )
            key = tuple(sorted(members))
            require(key not in sets, "duplicate support set")
            sets[key] = support["basis"]
        require(
            bool(sets) == (item["assessment"] == "SPECIFIED"), "assessment/set mismatch"
        )
        supports[target] = (item["assessment"], sets)
    require(set(supports) == claims, "missing support targets")
    for name in [
        "affected_beliefs_json",
        "preserved_beliefs_json",
        "historical_valid_beliefs_json",
    ]:
        decoded[name] = unique_strings(decoded[name], claims, name)
    require(
        not (decoded["affected_beliefs_json"] & decoded["preserved_beliefs_json"]),
        "affected/preserved overlap",
    )
    if row["checkpoint"] == "t0":
        require(
            not any(
                decoded[f]
                for f in [
                    "affected_beliefs_json",
                    "preserved_beliefs_json",
                    "historical_valid_beliefs_json",
                ]
            ),
            "t0 revision lists must be []",
        )
    require(
        isinstance(decoded["ambiguous_relationships_json"], list),
        "ambiguity list required",
    )
    for item in decoded["ambiguous_relationships_json"]:
        unique_strings(item["members"], refs, "ambiguous members")
        require(
            item["target"] in claims
            and isinstance(item["reason"], str)
            and item["reason"].strip(),
            "invalid ambiguity entry",
        )
    return decoded | {"states": states, "relations": rels, "supports": supports}


def analyze(file_a, file_b, allow_partial=False):
    a, b = read_form(file_a), read_form(file_b)
    require(set(a) == set(b), "A/B case/checkpoint coverage differs")
    require(
        {r["annotator_id"] for r in a.values()}
        != {r["annotator_id"] for r in b.values()},
        "annotator IDs must differ",
    )
    paired, excluded = [], []
    for key in sorted(a):
        require(
            all(a[key][f] == b[key][f] for f in OBSERVED_FIELDS),
            "observed case text differs: " + str(key),
        )
        missing = [
            side + ":" + f
            for side, row in [("A", a[key]), ("B", b[key])]
            for f in LABEL_FIELDS
            if not row[f].strip()
        ]
        if missing:
            excluded.append(
                {"case_id": key[0], "checkpoint": key[1], "missing": missing}
            )
            continue
        paired.append((key, decode(a[key]), decode(b[key])))
    require(
        allow_partial or not excluded,
        "incomplete annotations; --allow-partial is exploratory only",
    )
    pools = {
        x: []
        for x in [
            "truth",
            "current_truth",
            "historical_then_truth",
            "historical_now_truth",
            "use",
            "action",
            "relation_presence",
            "support_assessment",
            "support_basis",
        ]
    }
    sets = {
        x: []
        for x in [
            "support_edges",
            "support_sets",
            "affected",
            "preserved",
            "historical_valid",
            "relations",
        ]
    }
    per_label = {label: [] for label in RELATIONS}
    row_exact, scenario_exact = [], {}
    per_case = {}
    uncertainty = Counter()
    for (cid, checkpoint), x, y in paired:
        equal = True
        stats = per_case.setdefault(
            cid,
            {
                "truth_matches": 0,
                "truth_n": 0,
                "edge_pairs": [],
                "set_pairs": [],
                "row_matches": 0,
                "rows": 0,
            },
        )
        for key in sorted(x["states"]):
            sx, sy = x["states"][key], y["states"][key]
            pools["truth"].append((sx[0], sy[0]))
            pools[key[1] + "_truth"].append((sx[0], sy[0]))
            pools["use"].append((sx[1], sy[1]))
            if key[1] == "current":
                pools["action"].append((sx[2], sy[2]))
                for side, state in [("A", sx), ("B", sy)]:
                    uncertainty[side + "_uncertain_current"] += (
                        state[0] == "UNKNOWN_AMBIGUOUS"
                        or state[1] == "UNKNOWN"
                        or state[2] == "UNCERTAIN"
                    )
                uncertainty["current_units"] += 1
            stats["truth_matches"] += sx[0] == sy[0]
            stats["truth_n"] += 1
            equal &= sx == sy
        relkeys = x["relations"].keys() | y["relations"].keys()
        typed = []
        for obj in [x, y]:
            typed.append(
                {
                    (members, target, label)
                    for (members, target), labels in obj["relations"].items()
                    for label in labels
                }
            )
        sets["relations"].append(tuple(typed))
        equal &= typed[0] == typed[1]
        for key in sorted(relkeys):
            lx, ly = (
                x["relations"].get(key, frozenset()),
                y["relations"].get(key, frozenset()),
            )
            pools["relation_presence"].append(
                ("PRESENT" if lx else "ABSENT", "PRESENT" if ly else "ABSENT")
            )
            for label in RELATIONS:
                per_label[label].append(
                    ("YES" if label in lx else "NO", "YES" if label in ly else "NO")
                )
            uncertainty["relation_union_units"] += 1
            uncertainty["ambiguous_relation_union"] += (
                "unknown_or_ambiguous" in lx or "unknown_or_ambiguous" in ly
            )
        for target in sorted(x["supports"]):
            ax, ssx = x["supports"][target]
            ay, ssy = y["supports"][target]
            pools["support_assessment"].append((ax, ay))
            equal &= (ax, ssx) == (ay, ssy)
            if "UNKNOWN" in (ax, ay):
                uncertainty["unknown_support_targets"] += 1
                continue
            edges = (
                {(s, target) for members in ssx for s in members},
                {(s, target) for members in ssy for s in members},
            )
            spair = (set(ssx), set(ssy))
            sets["support_edges"].append(edges)
            sets["support_sets"].append(spair)
            stats["edge_pairs"].append(edges)
            stats["set_pairs"].append(spair)
            for members in ssx.keys() & ssy.keys():
                pools["support_basis"].append((ssx[members], ssy[members]))
        if checkpoint != "t0":
            for metric, field in [
                ("affected", "affected_beliefs_json"),
                ("preserved", "preserved_beliefs_json"),
                ("historical_valid", "historical_valid_beliefs_json"),
            ]:
                pair = (x[field], y[field])
                sets[metric].append(pair)
                equal &= pair[0] == pair[1]
        ux, uy = (
            bool(x["ambiguous_relationships_json"]),
            bool(y["ambiguous_relationships_json"]),
        )
        uncertainty["A_rows_with_ambiguity_notes"] += ux
        uncertainty["B_rows_with_ambiguity_notes"] += uy
        equal &= ux == uy
        row_exact.append(bool(equal))
        scenario_exact[cid] = scenario_exact.get(cid, True) and bool(equal)
        stats["row_matches"] += equal
        stats["rows"] += 1
    uncertainty["support_target_units"] = len(pools["support_assessment"])
    uncertainty["completed_rows"] = len(paired)
    case_report = {}
    for cid, stat in sorted(per_case.items()):
        case_report[cid] = {
            "truth_raw": ratio(stat["truth_matches"], stat["truth_n"]),
            "exact_rows": ratio(stat["row_matches"], stat["rows"]),
            "support_edges": summarize_sets(stat["edge_pairs"]),
            "support_sets": summarize_sets(stat["set_pairs"]),
        }

    def macro(metric):
        vals = [
            d[metric]["macro_F1_nonempty"]
            for d in case_report.values()
            if d[metric]["macro_F1_nonempty"] is not None
        ]
        return {"value": ratio(sum(vals), len(vals)), "eligible_cases": len(vals)}

    return {
        "plan_version": "1.0",
        "status": "EXPLORATORY_PARTIAL"
        if excluded
        else "COMPLETE_INPUTS_NOT_ADJUDICATED",
        "input_sha256": {
            "A": hashlib.sha256(Path(file_a).read_bytes()).hexdigest(),
            "B": hashlib.sha256(Path(file_b).read_bytes()).hexdigest(),
        },
        "paired_rows": len(paired),
        "design_coverage": {
            "cases": len({k[0] for k in a}),
            "checkpoints": dict(sorted(Counter(k[1] for k in a).items())),
            "all_30_cases_four_stages_complete": len({k[0] for k in a}) == 30
            and len(a) == 120
            and not excluded,
        },
        "excluded_rows": excluded,
        "raw_exact_row_agreement": ratio(sum(row_exact), len(row_exact)),
        "raw_exact_case_agreement": ratio(
            sum(scenario_exact.values()), len(scenario_exact)
        ),
        "categorical": {k: categorical(v) for k, v in pools.items()},
        "relation_label_binary_on_union": {
            k: categorical(v) for k, v in sorted(per_label.items())
        },
        "sets": {k: summarize_sets(v) for k, v in sets.items()},
        "scenario_macro_support_edges": macro("support_edges"),
        "scenario_macro_support_sets": macro("support_sets"),
        "scenario_macro_belief_state": ratio(
            sum(v["truth_raw"] for v in case_report.values()), len(case_report)
        ),
        "uncertainty_counts": dict(uncertainty),
        "uncertainty_rates": {
            "A_current": ratio(
                uncertainty["A_uncertain_current"], uncertainty["current_units"]
            ),
            "B_current": ratio(
                uncertainty["B_uncertain_current"], uncertainty["current_units"]
            ),
            "unknown_support_either": ratio(
                uncertainty["unknown_support_targets"],
                uncertainty["support_target_units"],
            ),
            "ambiguous_relation_either": ratio(
                uncertainty["ambiguous_relation_union"],
                uncertainty["relation_union_units"],
            ),
        },
        "disagreement_rates": {
            k: (1 - categorical(v)["raw_agreement"]) if v else None
            for k, v in pools.items()
        },
        "per_case": case_report,
        "gate_decision": (
            "NOT_AUTOMATED: inspect qualitative confusions, coverage, "
            "kappa applicability and preregistered gates; no gold inferred"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("annotator_a", type=Path)
    parser.add_argument("annotator_b", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    try:
        result = analyze(args.annotator_a, args.annotator_b, args.allow_partial)
        require(
            args.output.resolve()
            not in {args.annotator_a.resolve(), args.annotator_b.resolve()},
            "output must not overwrite raw input",
        )
        require(
            not args.output.exists(),
            "output already exists; choose a new analysis version",
        )
    except (ValueError, KeyError, TypeError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
