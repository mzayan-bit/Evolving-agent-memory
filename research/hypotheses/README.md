# Research Hypotheses Workspace

This directory tracks the formulation, refinement, and testing of formal empirical hypotheses for EvoMem.

> [!NOTE]
> **Status**: Finalized hypotheses will only be authored after completing the initial literature review and gap analysis. Pre-mature hypotheses risk solving artificial or already-solved problems.

---

## Hypothesis Definition Template

Each hypothesis investigated in EvoMem must be structured as follows:

```markdown
# Hypothesis H[ID]: [Descriptive Title]

### 1. Research Question
[State the exact scientific question this hypothesis aims to address.]

### 2. Formal Hypothesis Statement
[State a precise, falsifiable claim. Example: "Condition A achieves higher retention accuracy than Baseline B under condition C when knowledge updates occur at frequency F."]

### 3. Variables
- **Independent Variables (Manipulated)**: [e.g., memory invalidation policy, update frequency, context window size]
- **Dependent Variables (Measured)**: [e.g., retrieval precision, downstream task accuracy, token overhead, latency]
- **Control Variables**: [e.g., base LLM, temperature, context budget, evaluation seed]

### 4. Baselines & Comparators
- [Baseline 1: e.g., Standard dense semantic retrieval without invalidation]
- [Baseline 2: e.g., Recency-filtered sliding window]
- [Baseline 3: e.g., Naive full-history append]

### 5. Evaluation Metrics
- [Metric 1: e.g., Fact-updating accuracy (%)]
- [Metric 2: e.g., Stale-memory recall rate (lower is better)]
- [Metric 3: e.g., Token and computational efficiency]

### 6. Expected Failure Modes
- [Scenario A: Where might this hypothesis break down?]
- [Scenario B: Potential edge cases or vulnerability to noisy observations]

### 7. Decision Criteria (Evidence Required)
- **Evidence to Accept**: [Explicit quantitative criteria or statistical significance required to validate the hypothesis]
- **Evidence to Reject**: [Observations that would conclusively falsify the hypothesis]
```

---

## Active & Candidate Hypotheses Index

| ID | Title | Status | Primary Metric | Associated Experiment |
|---|---|---|---|---|
| *H0* | *Literature review & baseline calibration* | *In Progress* | *Baseline error rate* | *Exp-000* |
