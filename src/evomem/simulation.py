"""Chronology, access projection and synthetic observed-lineage perturbations."""

import random
from dataclasses import dataclass, replace
from time import perf_counter

from evomem.cost import CostEvent, Ledger
from evomem.model import (
    Decision,
    InformationAccess,
    Memory,
    PolicyView,
    Relation,
    Revision,
    Scenario,
    Snapshot,
    Status,
    Support,
    grounded,
)
from evomem.policies import RepairPolicy


@dataclass(frozen=True)
class Corruption:
    seed: int = 0
    drop_count: int = 0
    spurious: tuple[Support, ...] = ()
    change_type: bool = False
    hide_provenance: bool = False
    hide_fault: bool = False


def corrupt(lineage: tuple[Support, ...], config: Corruption) -> tuple[Support, ...]:
    rng = random.Random(config.seed)
    incidences = [(s.justification_id, m) for s in lineage for m in s.members]
    if not 0 <= config.drop_count <= len(incidences):
        raise ValueError("Invalid incidence drop count")
    removed = set(rng.sample(incidences, config.drop_count))
    result = []
    for s in lineage:
        members = tuple(m for m in s.members if (s.justification_id, m) not in removed)
        if members:
            result.append(replace(s, members=members))
    if config.change_type and result:
        index = rng.randrange(len(result))
        result[index] = replace(
            result[index], relation=Relation.ASSOCIATION, sufficient=False
        )
    return tuple(result) + config.spurious


def project(
    scenario: Scenario,
    snapshot: Snapshot,
    revision: Revision,
    history: tuple[Snapshot, ...],
    access: InformationAccess,
    corruption: Corruption,
    oracle: tuple[Support, ...] | None = None,
) -> PolicyView:
    if access.gold_dependencies and oracle is None:
        raise ValueError("Explicit oracle dependency bundle required")

    def redact(m: Memory) -> Memory:
        return replace(
            m,
            source_ids=m.source_ids
            if access.source_provenance and not corruption.hide_provenance
            else (),
            origin_ids=m.origin_ids
            if access.source_provenance and not corruption.hide_provenance
            else (),
            authority=m.authority if access.authority_labels else None,
        )

    items = tuple(redact(m) for m in snapshot.items)
    ids = {m.memory_id for m in items}
    lineage = (
        oracle if access.gold_dependencies else corrupt(scenario.observed, corruption)
    )
    assert lineage is not None

    def visible(s: Support) -> bool:
        return (
            s.target in ids
            and set(s.members) <= ids
            and s.valid_from <= snapshot.checkpoint
        )

    def redact_support(s: Support) -> Support:
        return replace(
            s,
            origin_ids=s.origin_ids
            if access.source_provenance and not corruption.hide_provenance
            else (),
        )

    cue = revision.before if access.gold_fault_identity else revision.fault_cue
    if corruption.hide_fault and not access.gold_fault_identity:
        cue = None
    return PolicyView(
        snapshot.checkpoint,
        items,
        replace(
            revision,
            before=revision.before if cue else "",
            after=redact(revision.after),
            fault_cue=cue,
        ),
        tuple(redact_support(s) for s in lineage if visible(s)),
        tuple(redact_support(s) for s in scenario.rules if visible(s)),
        tuple(
            Snapshot(h.checkpoint, tuple(redact(m) for m in h.items))
            for h in history
            if h.checkpoint <= snapshot.checkpoint
        )
        if access.full_history
        else (),
        access,
    )


@dataclass(frozen=True)
class Trace:
    snapshots: tuple[Snapshot, ...]
    decisions: tuple[Decision, ...]
    revisions: tuple[Revision, ...]
    rules: tuple[Support, ...]

    def answer(
        self,
        item_id: str,
        checkpoint: int,
        view: str = "current",
        as_of: int | None = None,
    ) -> str | None:
        if view not in {"current", "historical_then", "historical_now"}:
            raise ValueError("Unknown time view")
        when = checkpoint if view == "current" else as_of
        if when is None or when < 0 or when > checkpoint:
            raise ValueError("Invalid historical time")
        snap = next(s for s in self.snapshots if s.checkpoint == when)
        item = next(m for m in snap.items if m.memory_id == item_id)
        if view == "historical_now":
            revoked = {
                r.before
                for r in self.revisions
                if r.checkpoint <= checkpoint and r.kind in {"correction", "permission"}
            }
            if revoked:
                revised = tuple(
                    replace(m, status=Status.INACTIVE) if m.memory_id in revoked else m
                    for m in snap.items
                )
                if item_id not in grounded(revised, self.rules, when):
                    return None
        return item.content if item.status == Status.ACTIVE else None


def run(
    scenario: Scenario,
    policy: RepairPolicy,
    access: InformationAccess,
    ledger: Ledger,
    corruption: Corruption | None = None,
    oracle: tuple[Support, ...] | None = None,
) -> Trace:
    if access.external_evidence:
        raise ValueError("No external evidence adapter is installed")
    corruption = corruption or Corruption()
    history = [Snapshot(0, scenario.initial)]
    decisions = []
    start = perf_counter()
    for revision in scenario.revisions:
        old = history[-1]
        items = tuple(
            replace(m, status=Status.SUPERSEDED, valid_until=revision.checkpoint)
            if m.memory_id == revision.before
            else m
            for m in old.items
        )
        items += (revision.after,)
        snapshot = Snapshot(revision.checkpoint, items)
        view = project(
            scenario, snapshot, revision, tuple(history), access, corruption, oracle
        )
        decision = policy.repair(view, ledger)
        if {m.memory_id for m in decision.items} != {m.memory_id for m in items}:
            raise ValueError("Policy cannot invent or delete record IDs")
        # Restore non-visible metadata; policy mutations currently change only status.
        statuses = {m.memory_id: m.status for m in decision.items}
        committed = tuple(replace(m, status=statuses[m.memory_id]) for m in items)
        history.append(Snapshot(revision.checkpoint, committed))
        decisions.append(replace(decision, items=committed))
    ledger.charge(
        CostEvent(
            "trajectory-runtime",
            "runtime",
            len(decisions),
            wall_latency_ms=(perf_counter() - start) * 1000,
        )
    )
    return Trace(tuple(history), tuple(decisions), scenario.revisions, scenario.rules)
