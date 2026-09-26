# Parametric knowledge and readout separation — engineering candidate

The new `ReadoutProbe` contains only target, question, checkpoint and requested time view. It never contains an expected answer or state label. `ReadoutResult` records answer, retrieved IDs, cited IDs, completion and reader mode. Evaluator-only `assess_readout` produces three separate fields: memory_state_correct (supplied by the independent state evaluator), retrieval_correct (required-evidence coverage), answer_correct (exact-match fixture outcome). Unknown state/evidence labels remain null; a failed null response is not a correct abstention. Citation validity does not establish entailment.

StructuredReadout wraps the existing immutable Trace and preserves current, historical-then and historical-now behavior, including its permission/correction logic. ModelReadout operates only on a projected current view and rejects historical requests explicitly. It reads active, time-valid records, charges readout calls, validates cited IDs and never writes state. Historical model readout remains a declared unsupported scope; deterministic historical readout remains available. The fixed-proposition experiment runner is not silently converted into generative evaluation.

## Controlled inputs

`experiment/observable_fixtures.py` uses fictional Zorvia, Tovren and Velkin names, arbitrary permit/protocol values and explicit visible semantic evidence. The same nonce case can be run with K17 versus K29 while keeping the old stored belief unchanged. That lets a test distinguish corrected source context from stale storage. Counterfactuals and blank-evidence conditions test whether answers track supplied evidence; nonce names alone do not guarantee absence of training overlap or world-knowledge influence.

The support fixture has five assessable claims: necessary, alternative, conjunctive, association-only and copied evidence. Unlike earlier canonical records with different hidden rules but identical text, these distinctions appear in visible evidence. No formal support gold is inserted into prompts. This tiny engineering set checks execution, not inference accuracy or G1 prevalence. Never train on its outputs and then call it held-out evidence.

## Interpretation boundary

A stale active memory plus a correct answer is **state failure / answer success**, not successful repair. Correct state plus a hallucinated answer is state success / answer failure. Retrieval coverage is evaluated separately from citation correctness and answer correctness. Tests cover both counterexamples. Model prior knowledge can still produce unsupported answers; prompts saying “no outside knowledge” are not a proof. A later pilot needs adjudicated evidence, predeclared counterfactual/nonce controls, explicit context access, readout budget matching and separate state/answer tables.

B10 is an audit reader, deliberately able to use corrected current sources to counter stale beliefs. Its answer must never overwrite the persistent-state outcome. Repeated queries pay again by default, and later unaudited reads still expose stale storage. No claim about B10 superiority follows from this implementation.
