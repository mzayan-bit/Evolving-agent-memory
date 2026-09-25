"""Strict, separate adjudicated JSON interchange; never accepts annotator CSVs."""

import json
import types
from dataclasses import fields
from pathlib import Path
from typing import Any, get_args, get_origin, get_type_hints

from evomem.evaluation import CheckpointGold, Gold, Probe
from evomem.model import Memory, Relation, Revision, Scenario, Status, Support


def shape(value: Any, annotation: Any) -> bool:
    """Validate JSON types before dataclass construction (bool is not an int)."""
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin is types.UnionType:
        return any(shape(value, arg) for arg in args)
    if origin is tuple:
        return isinstance(value, list) and all(shape(v, args[0]) for v in value)
    if isinstance(annotation, type) and issubclass(annotation, (Status, Relation)):
        return isinstance(value, str) and value in list(annotation)
    if annotation in (str, int, bool, type(None)):
        return type(value) is annotation
    return True


def typed_fields(row: dict[str, Any], cls: type[Any]) -> None:
    exact(row, {f.name for f in fields(cls)})
    for name, annotation in get_type_hints(cls).items():
        if not shape(row[name], annotation):
            raise ValueError(f"Invalid field type or label: {name}")


def exact(
    row: dict[str, Any],
    required: set[str],
    optional: set[str] | frozenset[str] = frozenset(),
) -> None:
    if not required <= row.keys() or row.keys() - required - optional:
        raise ValueError("Missing or unexpected fields")


def memory(row: dict[str, Any]) -> Memory:
    typed_fields(row, Memory)
    row = row.copy()
    row["status"] = Status(row["status"])
    for key in ("source_ids", "origin_ids"):
        row[key] = tuple(row[key])
    return Memory(**row)


def support(row: dict[str, Any]) -> Support:
    typed_fields(row, Support)
    row = row.copy()
    row["relation"] = Relation(row["relation"])
    row["members"] = tuple(row["members"])
    row["origin_ids"] = tuple(row["origin_ids"])
    return Support(**row)


def validate(scenario: Scenario, gold: Gold) -> None:
    all_items = scenario.initial + tuple(r.after for r in scenario.revisions)
    lookup = {m.memory_id: m for m in all_items}
    if len(lookup) != len(all_items):
        raise ValueError("Duplicate memory IDs")
    if any(m.created_at_checkpoint != 0 for m in scenario.initial):
        raise ValueError("Initial record checkpoint must be zero")
    seen = {m.memory_id for m in scenario.initial}
    for index, r in enumerate(scenario.revisions, 1):
        if r.checkpoint != index or r.after.created_at_checkpoint != index:
            raise ValueError("Checkpoint ordering")
        if r.before not in seen or r.kind not in {
            "correction",
            "supersession",
            "withdrawal",
            "permission",
            "reinstatement",
        }:
            raise ValueError("Impossible revision reference or kind")
        seen.add(r.after.memory_id)
    for m in all_items:
        if (
            not m.memory_id
            or not m.content
            or not m.scope
            or m.valid_until is not None
            and m.valid_until <= m.valid_from
            or not set(m.source_ids) <= lookup.keys()
        ):
            raise ValueError("Invalid memory fields or references")
        if any(
            lookup[i].created_at_checkpoint > m.created_at_checkpoint
            for i in m.source_ids
        ):
            raise ValueError("Future provenance reference")
    for bundle in (scenario.observed, scenario.rules, gold.supports):
        if len({s.justification_id for s in bundle}) != len(bundle):
            raise ValueError("Duplicate justification ID")
        for s in bundle:
            if s.target not in lookup or not set(s.members) <= lookup.keys():
                raise ValueError("Impossible support reference")
            if any(lookup[i].created_at_checkpoint > s.valid_from for i in s.members):
                raise ValueError("Future support reference")
    if [g.checkpoint for g in gold.checkpoints] != list(
        range(1, len(scenario.revisions) + 1)
    ):
        raise ValueError("Gold checkpoint ordering")
    derived = {m.memory_id for m in all_items if m.kind != "source"}
    for g in gold.checkpoints:
        if not (g.affected | g.valid | g.unresolved) <= derived:
            raise ValueError("Gold sets must refer to derived records")
    if len({p.probe_id for p in gold.probes}) != len(gold.probes):
        raise ValueError("Duplicate probe IDs")
    for p in gold.probes:
        if p.item_id not in lookup or not 1 <= p.checkpoint <= len(scenario.revisions):
            raise ValueError("Impossible probe reference")
        if p.view not in {"current", "historical_then", "historical_now"}:
            raise ValueError("Unknown time view")
        when = p.checkpoint if p.view == "current" else p.as_of
        if (
            when is None
            or not 0 <= when <= p.checkpoint
            or lookup[p.item_id].created_at_checkpoint > when
            or p.view == "current"
            and p.as_of is not None
        ):
            raise ValueError("Invalid historical/current probe")


def load_adjudicated(path: Path) -> tuple[Scenario, Gold]:
    raw = json.loads(path.read_text())
    exact(raw, {"schema_version", "status", "adjudication", "scenario", "gold"})
    if raw["schema_version"] != "g1-adjudicated-1" or raw["status"] != "ADJUDICATED":
        raise ValueError("Only explicitly adjudicated interchange is accepted")
    exact(raw["adjudication"], {"reviewer", "agreement_report", "protocol_version"})
    if not all(isinstance(v, str) and v.strip() for v in raw["adjudication"].values()):
        raise ValueError("Missing adjudication provenance")
    s, g = raw["scenario"], raw["gold"]
    exact(s, {f.name for f in fields(Scenario)})
    exact(g, {"supports", "checkpoints", "probes"})
    revisions = []
    for r in s["revisions"]:
        typed_fields(r, Revision)
        revisions.append(
            Revision(
                r["checkpoint"],
                r["before"],
                memory(r["after"]),
                r["kind"],
                r["fault_cue"],
            )
        )
    scenario = Scenario(
        s["scenario_id"],
        s["cluster_id"],
        s["version"],
        tuple(memory(m) for m in s["initial"]),
        tuple(revisions),
        tuple(support(v) for v in s["observed"]),
        tuple(support(v) for v in s["rules"]),
    )
    checkpoints = []
    for row in g["checkpoints"]:
        typed_fields(row, CheckpointGold)
        for key in ("affected", "valid", "independent", "unresolved"):
            values = row[key]
            if (
                not isinstance(values, list)
                or any(not isinstance(v, str) for v in values)
                or len(set(values)) != len(values)
            ):
                raise ValueError("Invalid or duplicate measurement IDs")
        checkpoints.append(
            CheckpointGold(
                row["checkpoint"],
                frozenset(row["affected"]),
                frozenset(row["valid"]),
                frozenset(row["independent"]),
                frozenset(row["unresolved"]),
            )
        )
    probes = []
    for row in g["probes"]:
        typed_fields(row, Probe)
        probes.append(Probe(**row))
    gold = Gold(
        tuple(support(v) for v in g["supports"]), tuple(checkpoints), tuple(probes)
    )
    validate(scenario, gold)
    return scenario, gold
