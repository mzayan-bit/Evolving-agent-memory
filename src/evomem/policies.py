"""Eight deterministic protocol analogues; no learned repair controller."""

import math
import re
from collections import Counter
from dataclasses import dataclass, replace
from typing import Protocol

from evomem.cost import BudgetExceededError, CostEvent, Ledger
from evomem.model import Action, Decision, PolicyView, Status, Support, grounded


class InferenceProvider(Protocol):
    def infer(self, view: PolicyView) -> tuple[tuple[Support, float], ...]: ...


class RecordedInference:
    """Frozen observed proposal, unit confidence; no claim of semantic inference."""

    def infer(self, view: PolicyView) -> tuple[tuple[Support, float], ...]:
        return tuple((s, 1.0) for s in view.lineage)


class RepairPolicy(Protocol):
    def repair(self, view: PolicyView, ledger: Ledger) -> Decision: ...


def similarity(left: str, right: str) -> float:
    a, b = (Counter(re.findall(r"\w+", text.lower())) for text in (left, right))
    norm = math.sqrt(sum(v * v for v in a.values()) * sum(v * v for v in b.values()))
    return sum(v * b[k] for k, v in a.items()) / norm if norm else 0.0


@dataclass
class Baseline:
    name: str
    inference: InferenceProvider
    threshold: float = 0.7

    def __post_init__(self) -> None:
        if self.name not in BASELINES or not 0 <= self.threshold <= 1:
            raise ValueError("Invalid baseline or threshold")

    def repair(self, view: PolicyView, ledger: Ledger) -> Decision:
        if self.name == "B0":
            return Decision(view.items)
        if self.name == "B1":
            return Decision(
                view.items,
                ((view.revision.before, Action.INVALIDATE),)
                if view.revision.before
                else (),
            )
        derived = sorted(
            (m for m in view.items if m.kind != "source"), key=lambda m: m.memory_id
        )
        targets: set[str] = set()
        supports = view.lineage
        if self.name in {"B5", "B7"}:
            supports = tuple(
                s for s, score in self.inference.infer(view) if score >= self.threshold
            )
        if self.name in {"B3", "B5"}:
            reached = {view.revision.fault_cue} if view.revision.fault_cue else set()
            while True:
                added = {s.target for s in supports if reached.intersection(s.members)}
                if added <= reached:
                    break
                reached |= added
            targets = {m.memory_id for m in derived if m.memory_id in reached}
        elif self.name == "B4" and view.revision.fault_cue:
            old = next(m for m in view.items if m.memory_id == view.revision.fault_cue)
            targets = {
                m.memory_id
                for m in derived
                if similarity(old.content, m.content) >= self.threshold
            }
        if self.name in {"B3", "B4", "B5"}:
            return Decision(
                tuple(
                    replace(m, status=Status.INACTIVE) if m.memory_id in targets else m
                    for m in view.items
                ),
                tuple((i, Action.INVALIDATE) for i in sorted(targets)),
            )
        valid = grounded(
            view.items, supports if self.name == "B7" else view.rules, view.checkpoint
        )
        known = {
            s.target
            for s in (supports if self.name == "B7" else view.rules)
            if s.sufficient
        }
        changes = {}
        actions: list[tuple[str, Action]] = []
        checked: list[str] = []
        completion = "done"
        for m in derived:
            try:
                if self.name in {"B2", "B6"}:
                    ledger.charge(
                        CostEvent(
                            f"{view.checkpoint}:{self.name}:{m.memory_id}",
                            "maintenance",
                            view.checkpoint,
                            verification_calls=int(self.name == "B6"),
                            replay_steps=int(self.name == "B2"),
                        )
                    )
                    checked.append(m.memory_id)
            except BudgetExceededError:
                completion = "budget_exhausted"
                if self.name == "B2":
                    return Decision(view.items, completion=completion)
                break
            status = (
                Status.ACTIVE
                if m.memory_id in valid
                else Status.INACTIVE
                if m.memory_id in known
                else Status.QUARANTINED
            )
            changes[m.memory_id] = replace(m, status=status)
            action = (
                Action.REPLAY
                if self.name == "B2"
                else Action.REVERIFY
                if self.name == "B6"
                else Action.RETAIN
                if status == Status.ACTIVE
                else Action.QUARANTINE
                if status == Status.QUARANTINED
                else Action.INVALIDATE
            )
            actions.append((m.memory_id, action))
        return Decision(
            tuple(changes.get(m.memory_id, m) for m in view.items),
            tuple(actions),
            completion,
            tuple(checked) if self.name == "B6" else (),
        )


BASELINES = ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7")
