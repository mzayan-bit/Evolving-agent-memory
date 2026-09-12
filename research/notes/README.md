# Research Notes & Design Log

This directory serves as the working log for informal technical notes, theoretical derivations, design reasoning, and unresolved conceptual questions.

---

## Log Organization

Store individual notes as markdown documents using the naming format `YYYY-MM-DD_<topic_slug>.md`.

Each note should ideally document:
- **Context & Motivation**: Why this topic is being examined.
- **Analytical / Conceptual Thoughts**: Core reasoning, architectural sketches, or mathematical modeling.
- **Trade-offs & Alternatives Considered**: Why certain approaches are preferred over others.
- **Unresolved Questions & Next Steps**: What questions must be answered next before moving to implementation.

---

## Unresolved Questions & Open Discussion Log

- **Q1: Granularity of Memory Invalidation**: Should memory units be invalidated at the token, statement, triplet, or document level?
- **Q2: Conflict Detection Overhead**: What is the computational cost of continuous consistency checking versus on-demand conflict resolution during retrieval?
- **Q3: Benchmark Realism**: How do existing benchmarks model naturalistic knowledge drift and multi-hop dependency updates over long horizons?
