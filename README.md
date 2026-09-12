# Evolving Agent Memory (EvoMem)

> **A research project investigating continual memory management for LLM agents operating under evolving knowledge.**

---

## 1. Motivation

Autonomous LLM agents deployed over extended operational horizons interact with dynamic, non-stationary environments. Throughout continuous execution, an agent routinely encounters:

- **Updated facts** requiring existing internal representations to be modified.
- **Stale memories** that reflect outdated environmental states.
- **Direct contradictions** between past experiences and recent observations.
- **Superseded information** where newer evidence invalidates historical premises.
- **Irrelevant accumulated memories** that saturate context windows and degrade inference quality.
- **Uncertain or unverified information** requiring probabilistic or conditional retention.

Standard retrieval approaches (such as naive semantic-similarity lookup over static vector stores) treat memory as static key-value stores. They do not model temporal dynamics, validity windows, or belief revision, often retrieving obsolete or contradictory contexts.

---

## 2. Broad Research Question

> **How should an autonomous LLM agent decide what to remember, retrieve, update, consolidate, invalidate, and forget as its knowledge evolves over time?**

---

## 3. Tentative Research Areas

> [!NOTE]
> **Exploratory Scope Notice**: The areas listed below represent tentative research directions under active investigation during literature review, **not** implemented features or proven claims.

- **Continual Agent Memory**: Architectures that maintain coherent internal representations across unbounded interactions without catastrophic forgetting or memory bloat.
- **Episodic vs. Semantic Memory**: Mechanisms for transforming concrete interaction traces (episodic) into generalized, structured knowledge (semantic).
- **Temporal Validity & Decay**: Explicit modeling of time, validity intervals, and recency-weighted relevance.
- **Stale-Memory Handling & Invalidation**: Systematic detection and invalidation of out-of-date records.
- **Contradiction Resolution & Belief Revision**: Formal policies for adjudicating conflicting pieces of evidence gathered at different timestamps.
- **Memory Consolidation**: Periodic offline or background synthesis of raw memories into compact, high-utility representations.
- **Selective Forgetting**: Controlled pruning and forgetting mechanisms to preserve context budget and retrieval precision.
- **Adaptive Retrieval**: Context-aware retrieval strategies conditioned on task requirements, uncertainty, and temporal relevance.
- **Long-Horizon Evaluation**: Rigorous benchmark methodologies and diagnostic tasks for assessing memory evolution over extended horizons.

---

## 4. Current Status

**Phase 0 — Repository Initialization & Literature Review**

- [x] Repository environment, tooling, and quality gates established.
- [ ] Systematic literature review of agent memory systems, continual learning, and belief revision.
- [ ] Formalization of research gaps, baseline definitions, and empirical hypotheses.
- [ ] Controlled experimental design and diagnostic benchmark selection.
- [ ] Method design, ablation studies, and empirical evaluation.

---

## 5. Scientific Principles & Reproducibility

This project prioritizes rigorous empirical science over feature accumulation:

1. **Controlled Experiments**: Every empirical claim must be evaluated against clear, reproducible baselines.
2. **Deterministic & Reproducible Configurations**: All runs require explicit configurations, pinned dependencies, fixed random seeds, and full environment captures.
3. **Systematic Ablations**: Each proposed mechanism must be individually isolated to measure its marginal contribution.
4. **Traceable Results**: Experimental logs, raw evaluation outputs, and configuration artifacts must be documented and auditable.
5. **Separation of Concerns**: We maintain strict boundaries between established literature, speculative hypotheses, implementation code, and verified empirical evidence.

---

## 6. Repository Layout

```text
Evolving-agent-memory/
├── README.md                  # Project overview, research scope & principles
├── LICENSE                    # MIT License
├── pyproject.toml             # Python package metadata and dev tooling config
├── .python-version            # Pinned Python version (3.11)
├── .gitignore                 # Research and Python gitignore rules
├── src/
│   └── evomem/                # Core Python package (minimal Phase 0 setup)
│       ├── __init__.py        # Version and top-level exports
│       └── config.py          # Typed configuration and seed control
├── tests/
│   └── test_smoke.py          # Smoke tests verifying imports and determinism
├── research/                  # Research workspace
│   ├── README.md              # Research workflow guide
│   ├── literature/            # Structured literature review & paper templates
│   ├── hypotheses/            # Formal hypothesis declarations
│   └── notes/                 # Research notes and design reasoning
├── experiments/               # Experiment design protocols and configs
│   └── README.md              # Experiment documentation conventions
└── results/                   # Evaluation results, logs, and summary tables
    └── README.md              # Result archiving guidelines
```

---

## 7. Getting Started

### Prerequisites
- Python `>= 3.11`
- [uv](https://github.com/astral-sh/uv) (recommended) or standard `pip`

### Installation & Environment Setup
```bash
# Sync dependencies with uv
uv sync --dev

# Run smoke tests
uv run pytest

# Run linter and type checks
uv run ruff check .
uv run mypy src tests
```
