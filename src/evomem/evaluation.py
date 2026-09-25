"""Evaluator-only labels and fixed-opportunity, trajectory-level metrics."""

from dataclasses import dataclass
from statistics import mean

from evomem.model import Status, Support
from evomem.simulation import Trace


@dataclass(frozen=True)
class Probe:
    probe_id: str
    checkpoint: int
    item_id: str
    expected: str | None
    view: str = "current"
    as_of: int | None = None


@dataclass(frozen=True)
class CheckpointGold:
    checkpoint: int
    affected: frozenset[str]
    valid: frozenset[str]
    independent: frozenset[str] = frozenset()
    unresolved: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        if (
            self.affected & self.valid
            or self.affected & self.unresolved
            or self.valid & self.unresolved
            or not self.independent <= self.valid
        ):
            raise ValueError("Invalid gold measurement sets")


@dataclass(frozen=True)
class Gold:
    supports: tuple[Support, ...]
    checkpoints: tuple[CheckpointGold, ...]
    probes: tuple[Probe, ...]


@dataclass(frozen=True)
class Rate:
    count: int
    eligible: int

    @property
    def rate(self) -> float | None:
        return self.count / self.eligible if self.eligible else None

    def json(self) -> dict[str, int | float | None]:
        return {"count": self.count, "eligible": self.eligible, "rate": self.rate}


def score(gold: Gold, trace: Trace) -> dict[str, Rate]:
    counts: dict[str, list[int]] = {
        name: [0, 0]
        for name in (
            "stale_reuse",
            "false_invalidation",
            "repair_precision",
            "repair_recall",
            "independent_support_retention",
            "recurrence",
            "current_correctness",
            "historical_correctness",
            "abstention",
            "reverify_coverage",
            "valid_quarantine",
            "valid_nonavailability",
            "unknown_abstention",
        )
    }

    def add(name: str, success: bool) -> None:
        counts[name][0] += int(success)
        counts[name][1] += 1

    labels = {g.checkpoint: g for g in gold.checkpoints}
    for p in gold.probes:
        answer = trace.answer(p.item_id, p.checkpoint, p.view, p.as_of)
        add(
            "current_correctness" if p.view == "current" else "historical_correctness",
            answer == p.expected,
        )
        add("abstention", answer is None)
        if p.view == "current" and p.item_id in labels[p.checkpoint].unresolved:
            add("unknown_abstention", answer is None)
        if p.view == "current" and p.item_id in labels[p.checkpoint].affected:
            # Fixtures use identity-preserving propositions; retrieval is not reliance.
            add("stale_reuse", answer is not None)
    for g in gold.checkpoints:
        now = {m.memory_id: m for m in trace.snapshots[g.checkpoint].items}
        before = {m.memory_id: m for m in trace.snapshots[g.checkpoint - 1].items}
        decision = trace.decisions[g.checkpoint - 1]
        for i in g.valid:
            add(
                "false_invalidation",
                now[i].status in {Status.INACTIVE, Status.SUPERSEDED},
            )
            add("valid_quarantine", now[i].status == Status.QUARANTINED)
            add("valid_nonavailability", now[i].status != Status.ACTIVE)
        for i in g.independent:
            add("independent_support_retention", now[i].status == Status.ACTIVE)
        for i in g.affected:
            add("repair_recall", now[i].status != Status.ACTIVE)
            later = [
                p
                for p in gold.probes
                if p.checkpoint > g.checkpoint
                and p.view == "current"
                and p.item_id == i
                and i in labels[p.checkpoint].affected
                and not any(
                    i in labels[t].valid
                    for t in range(g.checkpoint + 1, p.checkpoint + 1)
                )
            ]
            if now[i].status != Status.ACTIVE and later:
                add(
                    "recurrence",
                    any(trace.answer(i, p.checkpoint) is not None for p in later),
                )
        eligible = g.affected | g.valid | g.unresolved
        for i in eligible:
            add("reverify_coverage", i in decision.checked)
        for i in eligible:
            if before[i].status == Status.ACTIVE and now[i].status == Status.INACTIVE:
                add("repair_precision", i in g.affected)
    return {name: Rate(*values) for name, values in counts.items()}


def aggregate(
    rows: list[tuple[str, str, dict[str, Rate]]],
) -> dict[str, dict[str, float | int | None]]:
    """Average nested variants within base cluster, then equally across clusters."""
    if len({(cluster, variant) for cluster, variant, _ in rows}) != len(rows):
        raise ValueError("Duplicate scenario variant")
    result = {}
    names = rows[0][2] if rows else {}
    for name in names:
        clusters: dict[str, list[float]] = {}
        for cluster, _, metrics in rows:
            value = metrics[name].rate
            if value is not None:
                clusters.setdefault(cluster, []).append(value)
        result[name] = {
            "macro_rate": mean(mean(v) for v in clusters.values())
            if clusters
            else None,
            "eligible_clusters": len(clusters),
            "total_clusters": len({r[0] for r in rows}),
        }
    return result
