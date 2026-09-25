"""Per-operation accounting, checked before deterministic operations execute."""

from dataclasses import asdict, dataclass, field


class BudgetExceededError(RuntimeError):
    pass


@dataclass(frozen=True)
class Budget:
    max_verification_calls: int | None = None
    max_replay_steps: int | None = None
    max_model_calls: int | None = None
    max_tokens: int | None = None
    max_retrieval_calls: int | None = None

    def __post_init__(self) -> None:
        if any(
            v is not None and (type(v) is not int or v < 0)
            for v in asdict(self).values()
        ):
            raise ValueError("Budget caps must be nonnegative integers")


@dataclass(frozen=True)
class CostEvent:
    operation_id: str
    phase: str
    checkpoint: int
    model_calls: int = 0
    input_tokens: int | None = 0
    output_tokens: int | None = 0
    cached_input_tokens: int | None = 0
    retrieval_calls: int = 0
    embedding_calls: int = 0
    verification_calls: int = 0
    replay_steps: int = 0
    tool_calls: int = 0
    wall_latency_ms: float = 0.0
    usage_source: str = "deterministic_no_model"
    status: str = "ok"
    parent_operation_id: str | None = None
    model_id: str | None = None


@dataclass
class Ledger:
    budget: Budget
    events: list[CostEvent] = field(default_factory=list)

    def totals(self) -> dict[str, int | float | None]:
        names = (
            "model_calls",
            "input_tokens",
            "output_tokens",
            "cached_input_tokens",
            "retrieval_calls",
            "embedding_calls",
            "verification_calls",
            "replay_steps",
            "tool_calls",
            "wall_latency_ms",
        )
        result: dict[str, int | float | None] = {}
        for name in names:
            values = [asdict(e)[name] for e in self.events]
            result[name] = None if None in values else sum(values)
        return result

    def charge(self, event: CostEvent) -> None:
        if event.operation_id in {e.operation_id for e in self.events}:
            raise ValueError("Duplicate physical operation ID")
        for value in self._values(event):
            if value is not None and value < 0:
                raise ValueError("Negative cost")
        if (
            event.cached_input_tokens is not None
            and event.input_tokens is not None
            and event.cached_input_tokens > event.input_tokens
        ):
            raise ValueError("Cached tokens must be a subset of input")
        if event.model_calls and event.usage_source == "deterministic_no_model":
            raise ValueError("Model usage needs measured/unknown/synthetic provenance")
        totals = self.totals()
        for resource in (
            "verification_calls",
            "replay_steps",
            "model_calls",
            "retrieval_calls",
        ):
            cap = getattr(self.budget, "max_" + resource)
            if cap is not None and totals[resource] + getattr(event, resource) > cap:
                raise BudgetExceededError(resource)
        if self.budget.max_tokens is not None:
            tokens = [
                totals["input_tokens"],
                totals["output_tokens"],
                event.input_tokens,
                event.output_tokens,
            ]
            if any(v is None for v in tokens):
                raise BudgetExceededError("Unknown usage cannot certify a token cap")
            if sum(v for v in tokens if v is not None) > self.budget.max_tokens:
                raise BudgetExceededError("tokens")
        self.events.append(event)

    @staticmethod
    def _values(event: CostEvent) -> tuple[int | float | None, ...]:
        return (
            event.model_calls,
            event.input_tokens,
            event.output_tokens,
            event.cached_input_tokens,
            event.retrieval_calls,
            event.embedding_calls,
            event.verification_calls,
            event.replay_steps,
            event.tool_calls,
            event.wall_latency_ms,
        )
