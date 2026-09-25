"""Pinned, optional local embeddings. No download or installation at import time."""

import hashlib
import importlib
import importlib.metadata
import json
import math
import platform
from dataclasses import dataclass, field, replace
from pathlib import Path
from time import perf_counter
from typing import Protocol

from evomem.cost import CostEvent, Ledger
from evomem.model import Action, Decision, PolicyView, Status

MODEL = "sentence-transformers/all-MiniLM-L6-v2"
REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"


class EmbeddingBackend(Protocol):
    identity: str

    def encode(self, text: str) -> tuple[float, ...]: ...


class MiniLM:
    """Local files only, float32 CPU, pinned package/model; no implicit downloads."""

    def __init__(self) -> None:
        if importlib.metadata.version("sentence-transformers") != "6.1.0":
            raise ValueError("Requires sentence-transformers==6.1.0")
        module = importlib.import_module("sentence_transformers")
        torch = importlib.import_module("torch")
        torch.use_deterministic_algorithms(True)
        torch.set_num_threads(1)
        self.model = module.SentenceTransformer(
            MODEL, revision=REVISION, device="cpu", local_files_only=True
        )
        self.model.float()
        self.model.eval()
        self.model.max_seq_length = 256
        self.identity = json.dumps(
            {
                "model": MODEL,
                "revision": REVISION,
                "sentence_transformers": "6.1.0",
                "torch": torch.__version__,
                "transformers": importlib.metadata.version("transformers"),
                "dtype": "float32",
                "device": "cpu",
                "hardware": platform.machine(),
                "os": platform.platform(),
                "max_seq_length": 256,
                "normalization": True,
                "threads": 1,
            },
            sort_keys=True,
        )

    def encode(self, text: str) -> tuple[float, ...]:
        values = self.model.encode(
            text, normalize_embeddings=True, show_progress_bar=False
        )
        return tuple(float(x) for x in values)


def checked_vector(values: object) -> tuple[float, ...]:
    if not isinstance(values, (list, tuple)) or not values:
        raise ValueError("Empty embedding")
    if any(type(v) not in {int, float} or not math.isfinite(v) for v in values):
        raise ValueError("Invalid embedding")
    result = tuple(float(v) for v in values)
    if not any(result):
        raise ValueError("Zero embedding")
    return result


@dataclass
class EmbeddingCache:
    backend: EmbeddingBackend
    directory: Path

    def vector(self, text: str, ledger: Ledger, checkpoint: int) -> tuple[float, ...]:
        key = hashlib.sha256(
            json.dumps([self.backend.identity, text]).encode()
        ).hexdigest()
        path = self.directory / (key + ".json")
        start = perf_counter()
        hit = path.exists()
        if hit:
            raw = json.loads(path.read_text())
            if raw["key"] != key or raw["identity"] != self.backend.identity:
                raise ValueError("Embedding cache mismatch")
            result = checked_vector(raw["vector"])
        else:
            try:
                result = checked_vector(self.backend.encode(text))
            except Exception:
                ledger.charge(
                    CostEvent(
                        f"embedding:{len(ledger.events)}",
                        "embedding",
                        checkpoint,
                        embedding_calls=1,
                        status="failed",
                        model_id=self.backend.identity,
                        wall_latency_ms=(perf_counter() - start) * 1000,
                    )
                )
                raise
            self.directory.mkdir(parents=True, exist_ok=True)
            with path.open("x") as f:
                json.dump(
                    {"key": key, "identity": self.backend.identity, "vector": result}, f
                )
        ledger.charge(
            CostEvent(
                f"embedding:{len(ledger.events)}",
                "embedding",
                checkpoint,
                embedding_calls=int(not hit),
                cache_hits=int(hit),
                model_id=self.backend.identity,
                wall_latency_ms=(perf_counter() - start) * 1000,
            )
        )
        return result


def cosine(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    if len(a) != len(b):
        raise ValueError("Embedding dimension mismatch")
    return sum(x * y for x, y in zip(a, b, strict=True)) / math.sqrt(
        sum(x * x for x in a) * sum(y * y for y in b)
    )


@dataclass
class SemanticClosure:
    embeddings: EmbeddingCache
    threshold: float = 0.7  # Development candidate; never claimed tuned.
    name: str = field(default="B4b", init=False)

    def __post_init__(self) -> None:
        if not -1 <= self.threshold <= 1:
            raise ValueError("Invalid cosine threshold")

    def repair(self, view: PolicyView, ledger: Ledger) -> Decision:
        old = next(
            (m for m in view.items if m.memory_id == view.revision.fault_cue), None
        )
        if old is None:
            return Decision(view.items)
        vector = self.embeddings.vector(old.content, ledger, view.checkpoint)
        targets = {
            m.memory_id
            for m in view.items
            if m.kind != "source"
            and cosine(
                vector, self.embeddings.vector(m.content, ledger, view.checkpoint)
            )
            >= self.threshold
        }
        return Decision(
            tuple(
                replace(m, status=Status.INACTIVE) if m.memory_id in targets else m
                for m in view.items
            ),
            tuple((i, Action.INVALIDATE) for i in sorted(targets)),
        )
