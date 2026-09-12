# Literature Review Workspace

This directory contains systematic reviews of relevant literature in continual learning, agent memory systems, temporal reasoning, belief revision, and long-horizon evaluation.

> [!IMPORTANT]
> **Literature Review Policy**:
> - Never invent citations, venues, or performance claims.
> - Every paper entry must be verified against official conference/journal proceedings or arXiv preprints.
> - Identify concrete limitations, failure modes, and open questions in prior work to isolate genuine research gaps for EvoMem.

---

## Paper Review Template

When reviewing a new paper, copy the template below into a new markdown file named `YYYY_<firstauthor>_<short_title>.md` in this directory:

```markdown
# [Paper Title]

- **Paper**: [Full Title and Link/DOI]
- **Year**: [e.g., 2024]
- **Venue**: [e.g., NeurIPS, ICLR, ICML, ACL, EMNLP, arXiv]
- **Authors**: [Author list]

---

### 1. Overview & Problem Formulation
- **Research problem**: What core problem does this paper address?
- **Memory type**: (e.g., Episodic, Semantic, Working, Parametric, Non-parametric, Graph-based, Vector-based)
- **Architecture**: High-level overview of the memory management mechanism and agent framework.

---

### 2. Empirical Methodology
- **Dataset / benchmark**: What benchmarks or environments were evaluated?
- **Baselines**: What standard and competitive baselines were compared against?
- **Metrics**: What quantitative metrics were used?

---

### 3. Key Findings & Contributions
- **Main contribution**: Primary theoretical, algorithmic, or empirical insight.
- **Key results**: Quantitative summary of performance gains over baselines.

---

### 4. Critical Analysis & Gaps
- **Limitations**: In what scenarios does the method fail or degrade?
- **Open questions**: Unresolved theoretical or practical questions.
- **Relation to EvoMem**: How does this relate to continual/evolving agent memory?
- **Potential gap**: Specific unaddressed challenge or opportunity for EvoMem.
```

---

## Literature Tracking Table

| Paper | Year | Venue | Memory Type | Benchmark / Dataset | Key Limitation | Review File |
|---|---|---|---|---|---|---|
| *Template Entry* | *—* | *—* | *—* | *—* | *—* | *Pending* |
