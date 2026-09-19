# Research Workspace

## September 2026 review

Start with [RESEARCH_GAP_REPORT.md](RESEARCH_GAP_REPORT.md). Supporting decisions are in [candidate_gaps.md](candidate_gaps.md) and [novelty_threat_matrix.md](novelty_threat_matrix.md). The [literature index](literature/README.md) links the evidence. This phase produced research artifacts only; no method implementation or empirical results.

This directory structures the conceptual, scientific, and literature-driven foundation of the **EvoMem** project.

---

## 1. Research Lifecycle

To avoid premature implementation and ungrounded engineering, all work in EvoMem follows a disciplined scientific pipeline:

```text
[ Literature Review ] ──> [ Gap Analysis ] ──> [ Falsifiable Hypothesis ]
                                                       │
                                                       ▼
[ Reproducible Findings ] <── [ Controlled Experiment & Ablation ]
```

1. **Literature Review (`research/literature/`)**: Systematically review prior work across continual learning, agent memory architectures, belief revision, and temporal reasoning. Identify specific benchmark limitations and architectural gaps.
2. **Hypothesis Formulation (`research/hypotheses/`)**: Define clear, falsifiable hypotheses with explicit independent/dependent variables, failure modes, and acceptance/rejection thresholds.
3. **Research Notes & Design Log (`research/notes/`)**: Maintain an open log of design reasoning, analytical derivations, architectural discussions, and unresolved questions.

---

## 2. Directory Structure

- `literature/`: Standardized reviews of relevant literature. Includes the master review template.
- `hypotheses/`: Documented hypotheses mapped to specific planned empirical evaluations.
- `notes/`: Technical notes, mathematical formulations, and conceptual explorations.

---

## 3. Core Research Principles

- **Literature First**: No architectural abstraction is implemented without grounding in prior work or a clear gap analysis.
- **Explicit Baselines**: Every novel mechanism must be contrasted against established, unaugmented baselines (e.g., standard dense retrieval, recency-windowed buffers).
- **Separation of Evidence from Speculation**: Distinguish between peer-reviewed literature, internal hypotheses, preliminary empirical observations, and proven findings.
