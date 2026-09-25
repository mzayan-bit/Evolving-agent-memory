"""Memoized finite-rule replay; internal baseline, not a paper reproduction."""

from dataclasses import dataclass, field, replace

from evomem.cost import BudgetExceededError, CostEvent, Ledger
from evomem.model import Action, Decision, PolicyView, Status, Support, grounded


@dataclass
class CachedReplay:
    """Cache per-output ancestor slices, including negative results and rule identity.

    Each cache key includes all currently visible ancestor records and active rules.
    Cycles are evaluated by the same grounded least fixed point as full replay.
    Cache is local to one trajectory; only fully committed sweeps populate it.
    """

    faithful_to_original: bool = field(default=False, init=False)
    cache: dict[str, tuple[str, Status]] = field(default_factory=dict)

    def repair(self, view: PolicyView, ledger: Ledger) -> Decision:
        pending = dict(self.cache)
        changes = {}
        actions = []
        rules = tuple(
            s
            for s in view.rules
            if s.valid_from <= view.checkpoint
            and (s.valid_until is None or view.checkpoint < s.valid_until)
        )
        for item in sorted(view.items, key=lambda m: m.memory_id):
            if item.kind == "source":
                continue
            ancestors = {item.memory_id}
            while True:
                added = {m for s in rules if s.target in ancestors for m in s.members}
                if added <= ancestors:
                    break
                ancestors |= added
            selected: tuple[Support, ...] = tuple(
                s for s in rules if s.target in ancestors
            )
            records = tuple(m for m in view.items if m.memory_id in ancestors)
            known = any(s.target == item.memory_id and s.sufficient for s in view.rules)
            # Derived statuses are outputs. Normalize clock predicates.
            key = repr(
                (
                    known,
                    tuple(
                        (
                            m.memory_id,
                            m.valid_from <= view.checkpoint
                            and (
                                m.valid_until is None or view.checkpoint < m.valid_until
                            ),
                        )
                        for m in records
                    ),
                    tuple(
                        replace(m, status=Status.INACTIVE)
                        if m.kind != "source"
                        else replace(
                            m,
                            status=Status.ACTIVE
                            if m.status == Status.ACTIVE
                            and m.valid_from <= view.checkpoint
                            and (
                                m.valid_until is None or view.checkpoint < m.valid_until
                            )
                            else Status.INACTIVE,
                        )
                        for m in records
                    ),
                    selected,
                )
            )
            hit = item.memory_id in self.cache and self.cache[item.memory_id][0] == key
            try:
                ledger.charge(
                    CostEvent(
                        f"{view.checkpoint}:B8:{item.memory_id}",
                        "cached-replay",
                        view.checkpoint,
                        replay_steps=int(not hit),
                        cache_hits=int(hit),
                    )
                )
            except BudgetExceededError:
                return Decision(view.items, completion="budget_exhausted")
            if hit:
                status = self.cache[item.memory_id][1]
            else:
                valid = grounded(records, selected, view.checkpoint)
                status = (
                    Status.ACTIVE
                    if item.memory_id in valid
                    else Status.INACTIVE
                    if known
                    else Status.QUARANTINED
                )
                pending[item.memory_id] = (key, status)
            changes[item.memory_id] = replace(item, status=status)
            actions.append((item.memory_id, Action.RETAIN if hit else Action.REPLAY))
        self.cache = pending
        return Decision(
            tuple(changes.get(m.memory_id, m) for m in view.items), tuple(actions)
        )
