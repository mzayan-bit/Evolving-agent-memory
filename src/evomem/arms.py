"""One serial accounting/cache boundary for the existing seven comparator arms.

No dataset loading, parameter selection, scientific scoring or pilot dispatch.
Callers supply visible evidence and explicit derivations, never evaluator gold.
"""

import hashlib
import json
import math
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from time import perf_counter
from typing import Any

from evomem.comparators import SupportAwareRollback
from evomem.cost import Budget, BudgetExceededError, CostEvent, Ledger
from evomem.model import (
    Decision,
    InformationAccess,
    PolicyView,
    Revision,
    Scenario,
    Snapshot,
    Support,
)
from evomem.model_replay import Derivation, ModelCachedReplay, ModelDeriver
from evomem.models.client import ModelCallError, ModelClient
from evomem.models.embeddings import EmbeddingBackend, EmbeddingCache, SemanticClosure
from evomem.models.execution import ModelExecutor
from evomem.models.inference import (
    FrozenInference,
    PointEstimatePolicy,
    SupportInference,
    visible_payload,
)
from evomem.policies import Baseline
from evomem.readout import ReadoutProbe, TemporalModelReadout
from evomem.simulation import Corruption, Trace, project, run

ARMS = ("B4b", "B5a", "B5b", "B7", "B8", "B9", "B10")
SUPPORT_ARMS = frozenset({"B5a", "B5b", "B7", "B9"})


def prefix_key(view: PolicyView) -> str:
    payload = visible_payload(view)
    # Policy isolation intentionally supplies one proposal before arm decisions.
    # Derived status may differ after maintenance; immutable evidence may not.
    for record in payload["records"]:
        if record["kind"] != "source":
            record.pop("status")
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


@dataclass(frozen=True)
class SharedSupports:
    prefix: str
    proposals: tuple[tuple[Support, float], ...]
    costs: tuple[CostEvent, ...]
    recipients: frozenset[str]

    def __post_init__(self) -> None:
        if not self.costs or not any(e.model_calls for e in self.costs):
            raise ValueError("Shared inferred supports require construction costs")
        if not self.recipients or not self.recipients <= SUPPORT_ARMS:
            raise ValueError("Invalid shared-support recipients")

    @classmethod
    def construct(
        cls, view: PolicyView, executor: ModelExecutor, recipients: frozenset[str]
    ) -> "SharedSupports":
        if not recipients or not recipients <= SUPPORT_ARMS:
            raise ValueError("Invalid shared-support recipients")
        if view.access.gold_dependencies or view.access.gold_fault_identity:
            raise ValueError("Oracle construction is separate")
        start = len(executor.ledger.events)
        proposals = SupportInference(executor, use_cache=False).infer(view)
        return cls(
            prefix_key(view),
            proposals,
            tuple(executor.ledger.events[start:]),
            recipients,
        )


@dataclass
class ArmSession:
    name: str
    executor: ModelExecutor
    embeddings: EmbeddingCache | None = None
    derivations: tuple[Derivation, ...] = ()
    shared: dict[int, SharedSupports] | None = None
    threshold: float = 0.7
    frames: list[PolicyView] = field(default_factory=list)
    replay: ModelCachedReplay = field(init=False)
    allocated: set[str] = field(default_factory=set)
    replay_events: list[dict[str, Any]] = field(default_factory=list)
    source_versions: dict[str, str] = field(default_factory=dict)
    probes: tuple[ReadoutProbe, ...] = ()
    revisions: tuple[Revision, ...] = ()
    query_results: list[dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.replay = ModelCachedReplay(ModelDeriver(self.executor))

    def repair(self, view: PolicyView, ledger: Ledger) -> Decision:
        if ledger is not self.executor.ledger:
            raise ValueError("Arm must use one trajectory ledger")
        if view.access.gold_dependencies or view.access.gold_fault_identity:
            raise ValueError("Oracle arm cannot enter ordinary integration")
        started = perf_counter()
        event_start = len(ledger.events)
        view = replace(view, rules=())
        self.source_versions[view.revision.before] = view.revision.after.memory_id
        completion = "done"
        try:
            if self.name in SUPPORT_ARMS:
                if self.shared is not None:
                    bundle = self.shared[view.checkpoint]
                    if (
                        self.name not in bundle.recipients
                        or prefix_key(view) != bundle.prefix
                    ):
                        raise ValueError("Shared proposal evidence/recipient mismatch")
                    if bundle.prefix not in self.allocated:
                        # Atomic allocation: inability to afford construction cannot
                        # yield an otherwise free shared representation.
                        trial = replace(ledger, events=list(ledger.events))
                        allocated = [
                            replace(
                                e,
                                operation_id=f"shared:{bundle.prefix}:{i}",
                                status="shared_allocation",
                            )
                            for i, e in enumerate(bundle.costs)
                        ]
                        for event in allocated:
                            trial.charge(event)
                        ledger.events.extend(allocated)
                        self.allocated.add(bundle.prefix)
                    proposals = bundle.proposals
                else:
                    inference = SupportInference(self.executor)
                    proposals = inference.infer(view, pairwise=self.name == "B5a")
                selected = tuple(
                    s for s, confidence in proposals if confidence >= self.threshold
                )
                view = replace(view, lineage=selected)
                if self.name in {"B5a", "B5b"}:
                    decision = PointEstimatePolicy(
                        FrozenInference(proposals), self.name, self.threshold
                    ).repair(view, ledger)
                elif self.name == "B7":
                    decision = Baseline(
                        "B7", FrozenInference(proposals), self.threshold
                    ).repair(view, ledger)
                else:
                    decision = SupportAwareRollback().repair(view, ledger)
            elif self.name == "B4b":
                if self.embeddings is None:
                    raise ValueError("B4b requires an embedding backend")
                decision = SemanticClosure(self.embeddings, self.threshold).repair(
                    view, ledger
                )
            elif self.name == "B8":
                if not self.derivations:
                    raise ValueError("B8 requires explicit visible derivations")
                lookup = {m.memory_id: m for m in view.items}

                def latest(source: str) -> str:
                    seen: set[str] = set()
                    while source in self.source_versions:
                        if source in seen:
                            raise ValueError("Cyclic source-version mapping")
                        seen.add(source)
                        source = self.source_versions[source]
                    return source

                if any(
                    s.target_id not in lookup
                    or set(s.dependencies) != set(lookup[s.target_id].source_ids)
                    for s in self.derivations
                ):
                    raise ValueError(
                        "B8 dependencies must be shared visible provenance"
                    )
                specs = tuple(
                    replace(s, dependencies=tuple(latest(i) for i in s.dependencies))
                    for s in self.derivations
                )
                result = self.replay.update(view, specs)
                self.replay_events.append(
                    {
                        "checkpoint": view.checkpoint,
                        "cache_hits": result.cache_hits,
                        "cache_misses": result.cache_misses,
                        "regenerated_nodes": result.regenerated_nodes,
                        "completion": result.completion,
                    }
                )
                decision = Decision(result.items, completion=result.completion)
            elif self.name == "B10":
                decision = Decision(view.items)
            else:
                raise ValueError("Unknown comparator")
        except BudgetExceededError:
            completion = "budget_exhausted"
        except ModelCallError:
            completion = "model_failed"
        if completion != "done":
            decision = Decision(view.items, completion=completion)
        # Non-overlapping local overhead excludes already measured physical work
        # and allocated work performed elsewhere. Runtime stays a separate view.
        measured = sum(
            e.wall_latency_ms
            for e in ledger.events[event_start:]
            if e.status != "shared_allocation"
        )
        ledger.events.append(
            CostEvent(
                f"arm-local:{len(ledger.events)}",
                "arm-local",
                view.checkpoint,
                wall_latency_ms=max(0.0, (perf_counter() - started) * 1000 - measured),
            )
        )
        self.frames.append(replace(view, items=decision.items))
        reader = TemporalModelReadout(
            self.executor, tuple(self.frames), self.revisions, self.name == "B10"
        )
        for probe in self.probes:
            if probe.checkpoint == view.checkpoint:
                query_result = reader.answer(probe)
                self.query_results.append(
                    {"probe": asdict(probe), "result": asdict(query_result)}
                )
        return decision


@dataclass
class ArmRun:
    session: ArmSession
    trace: Trace

    def reader(self, audit: bool | None = None) -> TemporalModelReadout:
        return TemporalModelReadout(
            self.session.executor,
            tuple(self.session.frames),
            self.trace.revisions,
            self.session.name == "B10" if audit is None else audit,
        )

    def report(self) -> dict[str, Any]:
        ex = self.session.executor
        physical = [e for e in ex.ledger.events if e.status != "shared_allocation"]
        local = [e for e in physical if e.phase != "runtime"]
        physical_retries = sum(
            "protocol_retry" in json.loads(str(request["user"]))
            for a in ex.attempts
            if isinstance(request := a.get("request"), dict)
            and str(request.get("schema_version", "")).startswith("point-")
        )
        shared_retries = sum(
            max(0, sum(e.model_calls for e in b.costs) - 1)
            for b in (self.session.shared or {}).values()
            if b.prefix in self.session.allocated
        )
        return {
            "arm": self.session.name,
            "threshold": self.session.threshold,
            "mode": "policy_isolation"
            if self.session.shared is not None
            else "end_to_end",
            "charged_usage": ex.ledger.totals(),
            "physical_usage": Ledger(Budget(), physical).totals(),
            "physical_phase_latency_ms": sum(e.wall_latency_ms for e in local),
            "trajectory_runtime_ms": sum(
                e.wall_latency_ms for e in physical if e.phase == "runtime"
            ),
            "cache_namespace": str(ex.cache_dir),
            "cache_misses": sum(
                not a.get("cache_hit", False)
                and not a.get("blocked_before_dispatch", False)
                for a in ex.attempts
            )
            + sum(e.embedding_calls for e in physical),
            "support_retries": physical_retries + shared_retries,
            "physical_support_retries": physical_retries,
            "shared_preprocessing_received": sorted(self.session.allocated),
            "shared_original_costs": {
                b.prefix: [asdict(e) for e in b.costs]
                for b in (self.session.shared or {}).values()
            },
            "common_input": "same immutable input bundle; no model construction",
            "replay_events": self.session.replay_events,
            "query_results": self.session.query_results,
            "arm_specific_preprocessing": "own embeddings/support inference; ledgered",
            "credit_schedule": ex.ledger.credit_schedule,
            "released_model_calls": ex.ledger.released_calls,
            "events": [asdict(e) for e in ex.ledger.events],
            "energy_joules": None,
            "estimated_usd": None,
        }


def run_arms(
    scenario: Scenario,
    names: tuple[str, ...],
    client: ModelClient,
    output: Path,
    budget: Budget,
    *,
    embedding_backend: EmbeddingBackend | None = None,
    credit_schedule: tuple[tuple[int, int], ...] = (),
    derivations: tuple[Derivation, ...] = (),
    shared: dict[int, SharedSupports] | None = None,
    access: InformationAccess | None = None,
    probes: tuple[ReadoutProbe, ...] = (),
    thresholds: dict[str, float] | None = None,
) -> dict[str, ArmRun]:
    """Create cold arm-local caches and dispatch existing policies serially."""
    access = access or InformationAccess()
    if any(
        p.checkpoint not in {r.checkpoint for r in scenario.revisions} for p in probes
    ):
        raise ValueError("Query schedule must use declared revision checkpoints")
    if not names or len(set(names)) != len(names) or not set(names) <= set(ARMS):
        raise ValueError("Invalid arm inventory")
    if (
        access.gold_dependencies
        or access.gold_fault_identity
        or access.external_evidence
    ):
        raise ValueError("Ordinary arms require non-oracle local evidence")
    thresholds = thresholds or {}
    if not set(thresholds) <= SUPPORT_ARMS | {"B4b"} or any(
        not math.isfinite(value) or not 0 <= value <= 1 for value in thresholds.values()
    ):
        raise ValueError("Invalid development threshold configuration")
    recipients = frozenset(names) & SUPPORT_ARMS
    if shared is not None and len({thresholds.get(n, 0.7) for n in recipients}) > 1:
        raise ValueError("Shared point construction needs one common threshold")
    if shared is not None and (
        set(shared) != {r.checkpoint for r in scenario.revisions}
        or any(b.recipients != recipients for b in shared.values())
    ):
        raise ValueError(
            "Every applicable arm must receive the same shared construction"
        )
    output.mkdir(parents=True, exist_ok=False)
    results = {}
    for name in names:
        directory = output / name
        directory.mkdir()
        ledger = Ledger(budget, credit_schedule=credit_schedule)
        ex = ModelExecutor(client, ledger, directory / "model")
        session = ArmSession(
            name,
            ex,
            EmbeddingCache(embedding_backend, directory / "embedding")
            if embedding_backend
            else None,
            derivations,
            shared if name in SUPPORT_ARMS else None,
            threshold=thresholds.get(name, 0.7),
            probes=probes,
            revisions=scenario.revisions,
        )
        if scenario.revisions:
            initial = project(
                scenario,
                Snapshot(0, scenario.initial),
                scenario.revisions[0],
                (),
                access,
                Corruption(),
            )
            session.frames.append(replace(initial, rules=(), history=()))
        trace = run(scenario, session, access, ledger)
        results[name] = ArmRun(session, trace)
    return results
