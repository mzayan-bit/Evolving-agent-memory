# Results Workspace

This directory stores structured summaries, evaluation tables, metric curves, and pointers to raw experiment artifacts.

---

## Results Storage Guidelines

1. **Aggregated Summaries**: Store human-readable markdown summaries, performance tables, and high-level metric comparisons directly in git-tracked documentation.
2. **Raw Artifacts & Logs**: Raw run outputs (JSONL trace files, model prediction dumps, full prompt logs) should be placed in `results/raw/` or `results/runs/` which are excluded from git by `.gitignore`.
3. **Reproducibility Manifest**: Every reported table in this directory must link back to the exact experiment configuration, git commit hash, and random seeds in `experiments/`.

---

## Results Directory Layout

```text
results/
├── README.md               # Results storage guide and master comparison table
├── raw/                    # Raw evaluation logs and prediction outputs (git-ignored)
└── runs/                   # Serialized metric summaries and run artifacts (git-ignored)
```

---

## Master Benchmark & Evaluation Table

| Experiment ID | Method / Variant | Benchmark / Dataset | Primary Metric | Baseline Delta | Status | Commit Hash |
|---|---|---|---|---|---|---|
| *Pending Phase 1* | *—* | *—* | *—* | *—* | *Planned* | *—* |
