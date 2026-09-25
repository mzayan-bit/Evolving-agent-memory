# Experiment Workspace

This directory will house experimental configurations, run manifests, evaluation scripts, and orchestration workflows.

> [!NOTE]
> **Status**: No experiments are implemented yet. Experimental design and execution will commence in Phase 1 following literature review and hypothesis formalization.

---

## Experiment Protocol & Conventions

Every experiment conducted in EvoMem must be fully reproducible and document the following attributes in its experiment report (`experiments/exp_XXX_<name>/README.md`):

1. **Objective**: Concrete scientific objective of the run.
2. **Hypothesis**: Reference to the specific hypothesis ID in `research/hypotheses/`.
3. **Dataset & Version**: Exact dataset identifier, version hash, or synthetic generator parameters.
4. **Model(s)**: Exact backbone model, temperature, top-p, context window limits, and prompt templates.
5. **Configuration**: Complete serialized configuration (hyperparameters, memory capacity limits, update thresholds).
6. **Random Seed(s)**: Pinned random seed(s) evaluated across multiple runs to estimate variance.
7. **Baseline(s)**: Identical evaluation environment executed with baseline memory strategies.
8. **Metrics**: Quantitative metrics recorded (accuracy, precision, recall, stale-retrieval rate, latency, token consumption).
9. **Result Artifacts**: Pointers to raw log files and structured outputs in `results/`.
10. **Conclusion**: Objective synthesis of whether the evidence supports or rejects the hypothesis.

---

## Directory Organization (Planned)

```text
experiments/
├── README.md               # Experiment protocol & index (this file)
├── configs/                # Shared configuration definitions
└── exp_000_template/       # Standard experiment directory template
    ├── README.md           # Experiment specification & summary report
    ├── run.py              # Self-contained run entrypoint (pinned config)
    └── params.json         # Exact execution parameters
```

---

## Experiments Index

| ID | Name | Hypothesis | Status | Date | Primary Metric Result |
|---|---|---|---|---|---|
| *EXP-000* | *Phase 0 Environment & Smoke Test* | *Setup* | *Completed* | *2026-09-12* | *All smoke tests passing* |

## Model engineering phase (2026-09-26)

`configs/model-engineering-fixtures.json` runs the deterministic B0–B9 inventory
(legacy B5 uses recorded fixture inference; live B5 is a separate smoke). From a
clean committed checkout:

```sh
uv run python -m evomem.experiment.run --config experiments/configs/model-engineering-fixtures.json
```

Opt-in live plumbing checks are documented in
[the model prompt protocol](../research/g1/MODEL_PROMPT_PROTOCOL.md). They use at
most five model dispatches, seven target assessments from five canonical fixture
prefixes, and no human annotations. Missing credentials/server yields SKIPPED.
Outputs are create-only; select a new output directory for each attempt. Default
pytest uses offline doubles and never requires secrets. Pinned embedding weights
and Qwen are not downloaded automatically. Current readiness remains R0; see
[the engineering report](../research/g1/ENGINEERING_PHASE_REPORT.md).
