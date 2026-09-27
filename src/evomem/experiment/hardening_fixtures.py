"""Existing engineering fixtures plus two ID-only relabelings."""

from dataclasses import dataclass, replace

from evomem.fixtures import FIXTURES, fixture
from evomem.model import InformationAccess, PolicyView, Snapshot, Status, Support
from evomem.simulation import Corruption, project

from .observable_fixtures import support_view


@dataclass(frozen=True)
class Case:
    name: str
    view: PolicyView
    gold: tuple[Support, ...]
    targets: frozenset[str]
    note: str


def cases() -> tuple[Case, ...]:
    result = []
    for name in FIXTURES:
        scenario, gold = fixture(name)
        items = scenario.initial
        for revision in scenario.revisions:
            checkpoint = revision.checkpoint
            items = tuple(
                replace(m, status=Status.SUPERSEDED, valid_until=checkpoint)
                if m.memory_id == revision.before
                else m
                for m in items
            )
            items += (revision.after,)
            # Preserve the previous five-fixture smoke's exact projection.
            visible = tuple(
                m
                for m in items
                if m.memory_id != "b2"
                or name in {"semantic_bystander", "repeated", "correction"}
            )
            v = project(
                scenario,
                Snapshot(checkpoint, visible),
                revision,
                (),
                InformationAccess(),
                Corruption(),
            )
            v = replace(v, lineage=(), rules=(), history=())
            ids = {m.memory_id for m in visible}
            supports = tuple(
                s
                for s in gold.supports
                if s.target in ids
                and set(s.members) <= ids
                and s.valid_from <= checkpoint
                and (s.valid_until is None or checkpoint < s.valid_until)
            )
            result.append(
                Case(
                    f"{name}@{checkpoint}",
                    v,
                    supports,
                    frozenset(m.memory_id for m in visible if m.kind != "source"),
                    "Authored structural gold; some legacy text does not identify "
                    "AND/OR distinctions.",
                )
            )
    observed = support_view()
    result.append(
        Case(
            "observable-bystander",
            observed,
            (),
            frozenset({"assoc"}),
            "Partial semantic audit only: office paint does not justify protocol "
            "authorization. Other targets are not scored.",
        )
    )
    copies = next(c for c in result if c.name == "copies@1")
    for name, renamed_ids in [
        ("short-ids", ["0", "1", "2", "3"]),
        ("similar-ids", ["m1", "m10", "m100", "m01"]),
    ]:
        mapping = dict(
            zip((m.memory_id for m in copies.view.items), renamed_ids, strict=True)
        )
        renamed = tuple(
            replace(
                m,
                memory_id=mapping[m.memory_id],
                source_ids=tuple(mapping[i] for i in m.source_ids),
            )
            for m in copies.view.items
        )
        rev = copies.view.revision
        v = replace(
            copies.view,
            items=renamed,
            revision=replace(
                rev,
                before=mapping[rev.before],
                after=next(
                    m for m in renamed if m.memory_id == mapping[rev.after.memory_id]
                ),
                fault_cue=mapping[rev.fault_cue] if rev.fault_cue else None,
            ),
        )
        g = tuple(
            replace(
                s,
                target=mapping[s.target],
                members=tuple(mapping[i] for i in s.members),
            )
            for s in copies.gold
        )
        result.append(
            Case(
                name,
                v,
                g,
                frozenset(mapping[i] for i in copies.targets),
                "ID-only relabeling of existing copies evidence and evaluator gold.",
            )
        )
    return tuple(result)
