# Sample-size plan — hypothetical planning, not observations

The 30 exposed authored cases are ontology/development material. Thirty revisions or hundreds of policy trajectories do not create more independent families. Twelve proposed NEW pilot families estimate feasibility, cluster variance, missingness and real cost; they cannot credibly establish a small method gain or equivalence. The earlier “60 cases” is not a power calculation.

Let D_s be a paired scenario-family difference in trajectory SDRR; average dependent seeds/conditions within the family according to the estimand. For an illustrative two-sided normal test with alpha .05 and power .80, `MDE ≈ (1.96 + .84) σ_D / sqrt(n)` and `n ≈ ceil(7.84 σ_D² / δ²)`. These approximations ignore small-sample t corrections, bounded/zero-inflated rates and multiple comparisons, so can be optimistic. σ_D values below are hypothetical sensitivity inputs, not pilot estimates.

| Independent families n | MDE if σ_D=.10 | σ_D=.20 | σ_D=.30 |
|---|---|---|---|
| 12 | 8.1 percentage points | 16.2 pp | 24.2 pp |
| 30 | 5.1 pp | 10.2 pp | 15.3 pp |
| 60 | 3.6 pp | 7.2 pp | 10.8 pp |

For δ=.05, the same illustrative approximation gives about 32, 126 or 283 independent families, respectively. These are not recommendations to collect those sample sizes. FIR/task guardrails may require more data than the primary SDRR contrast, and alternative-support-only strata reduce eligible n further. A zero eligible denominator contributes no information to SDRR.

After pilot: estimate paired between-family dispersion separately per backbone/regime; give uncertainty on that dispersion; inspect skew, floor/ceiling, missingness and cluster-size imbalance. Plan full-study size using conservative variance ranges, fixed practical margins approved before comparison, and simulations that retain the real nested design. Use entirely new confirmation families; do not treat a pilot-selected favorable effect estimate as the design effect. If costs make adequate precision impossible, narrow the claim or publish exploratory analysis rather than fabricate power.

Bootstrap whole source families with all within-family outputs retained; do not resample probes as independent. At n=12, publish raw paired family differences and leave-one-family-out sensitivity alongside the planned 10,000-draw percentile interval. Non-significance is not equivalence; equivalence needs a separately approved margin and enough precision. Adaptive expansion rules must depend on variance/cost/feasibility, not repeated peeking for significance. No power simulation or empirical effect estimate was generated in this phase; the table is arithmetic on declared hypothetical inputs.
