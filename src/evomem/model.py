"""Immutable runtime records. Gold is deliberately defined in evaluation.py."""

from dataclasses import dataclass
from enum import StrEnum


class Status(StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    QUARANTINED = "quarantined"
    SUPERSEDED = "superseded"


class Relation(StrEnum):
    NECESSARY = "necessary"
    CONJUNCTIVE = "conjunctive"
    ALTERNATIVE = "alternative"
    PARTIAL = "partial"
    COPIED = "copied"
    CORRELATED = "correlated"
    TEMPORAL = "temporal"
    SCOPE = "scope"
    POLICY = "policy"
    ASSOCIATION = "association"
    CONTRADICTION = "contradiction"
    UNKNOWN = "unknown"


class Action(StrEnum):
    RETAIN = "retain"
    INVALIDATE = "invalidate"
    REPAIR = "repair"
    REVERIFY = "reverify"
    REPLAY = "replay"
    QUARANTINE = "quarantine"


@dataclass(frozen=True)
class Memory:
    memory_id: str
    content: str
    scope: str
    valid_from: int = 0
    valid_until: int | None = None
    status: Status = Status.ACTIVE
    source_ids: tuple[str, ...] = ()
    created_at_checkpoint: int = 0
    kind: str = "belief"
    origin_ids: tuple[str, ...] = ()
    authority: str | None = None


@dataclass(frozen=True)
class Support:
    justification_id: str
    target: str
    members: tuple[str, ...]
    relation: Relation = Relation.NECESSARY
    scope: str = "demo"
    valid_from: int = 0
    valid_until: int | None = None
    origin_ids: tuple[str, ...] = ()
    sufficient: bool = True

    def __post_init__(self) -> None:
        if not self.members or len(set(self.members)) != len(self.members):
            raise ValueError("Support members must be nonempty and unique")
        if (
            self.relation
            in {
                Relation.UNKNOWN,
                Relation.ASSOCIATION,
                Relation.PARTIAL,
                Relation.CONTRADICTION,
            }
            and self.sufficient
        ):
            raise ValueError("Non-sufficient relation cannot entail a claim")


@dataclass(frozen=True)
class Revision:
    checkpoint: int
    before: str
    after: Memory
    kind: str = "supersession"
    fault_cue: str | None = None


@dataclass(frozen=True)
class InformationAccess:
    gold_fault_identity: bool = False
    gold_dependencies: bool = False
    source_provenance: bool = True
    authority_labels: bool = True
    full_history: bool = True
    external_evidence: bool = False


@dataclass(frozen=True)
class Snapshot:
    checkpoint: int
    items: tuple[Memory, ...]


@dataclass(frozen=True)
class PolicyView:
    checkpoint: int
    items: tuple[Memory, ...]
    revision: Revision
    lineage: tuple[Support, ...]
    rules: tuple[Support, ...]  # Explicit executable evidence, never inferred gold.
    history: tuple[Snapshot, ...]
    access: InformationAccess


@dataclass(frozen=True)
class Decision:
    items: tuple[Memory, ...]
    actions: tuple[tuple[str, Action], ...] = ()
    completion: str = "done"
    checked: tuple[str, ...] = ()


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    cluster_id: str
    version: str
    initial: tuple[Memory, ...]
    revisions: tuple[Revision, ...]
    observed: tuple[Support, ...]
    rules: tuple[Support, ...]


def grounded(
    items: tuple[Memory, ...], supports: tuple[Support, ...], checkpoint: int
) -> frozenset[str]:
    """Least fixed point: ungrounded cycles cannot self-justify. AND/OR semantics."""
    lookup = {m.memory_id: m for m in items}
    active = {
        m.memory_id
        for m in items
        if m.kind == "source"
        and m.status == Status.ACTIVE
        and m.valid_from <= checkpoint
        and (m.valid_until is None or checkpoint < m.valid_until)
    }
    while True:
        added = {
            s.target
            for s in supports
            if s.sufficient
            and s.target in lookup
            and s.scope == lookup[s.target].scope
            and lookup[s.target].valid_from <= checkpoint
            and ((end := lookup[s.target].valid_until) is None or checkpoint < end)
            and s.valid_from <= checkpoint
            and (s.valid_until is None or checkpoint < s.valid_until)
            and set(s.members) <= active
        }
        if added <= active:
            return frozenset(active)
        active |= added


def independent_origins(groups: tuple[frozenset[str], ...]) -> bool:
    """Unknown/empty origins never establish independence; copies share an origin."""
    return any(
        a and b and a.isdisjoint(b)
        for i, a in enumerate(groups)
        for b in groups[i + 1 :]
    )
