# Error decomposition and attribution contract

Use multi-label diagnostic events with `stage`, `checkpoint`, `item/probe`, `evidence_refs`, `candidate_codes`, `certainty` (observed/mechanistically_verified/ambiguous), and `counterfactual_run_id`. An outcome error and its causes are different records. Gold comparisons are evaluator-only. Do not force a single root cause when several upstream faults interact.

| Code | Definition | Deterministic evidence / limits |
|---|---|---|
| E1 | Fault identification failure | Predicted diagnosis differs from adjudicated faulty ID, only on determinate diagnosis tasks; missing source cue alone is not evidence of failure |
| E2 | Support incidence inference failure | Missing/spurious member incidence versus adjudicated prefix gold; no proof it caused answer error |
| E3 | Support type/scope/origin classification failure | AND/OR, permission, copy independence or scope differs from adjudication; unknown gold excluded from binary mismatch |
| E4 | Alternative-support reasoning failure | Correct visible alternatives and valid members, yet valid claim lost; confirm with a controlled support-set replay |
| E5 | Repair decision failure | Correct inputs to decision layer but incorrect state mutation; distinguishes E4 subtype from generic mistake |
| E6 | Recompute/replay failure | Common derivation operation returns wrong state or fails to commit; distinguish budget interruption |
| E7 | Retrieval failure | Required admissible evidence existed in allowed pool but not selected; needs retrieval traces, cannot infer from wrong answer alone |
| E8 | Answer generation failure | Correct accessible state/evidence but wrong answer; structured readout ceiling helps isolate it |
| E9 | History/time failure | Wrong valid-time/known-time binding, supersession mistaken for falsehood, or present permission ignored |
| E10 | Budget exhaustion | Explicit cap exception/completion; records blocked resource and unfinished items. May co-occur with E1–E9 |

Existing logs contain immutable states/actions, completion, ledger, observed corruption masks and fixed answers/used IDs. These support E10 and controlled E2 incidence checks now. They do not record natural-language retrieval/proposal/verifier prompts, so E1/E7/E8 causal assignment remains unavailable. Add these records with real adapters before freeze; no post-hoc gold feedback to policies.

Attribution procedure: retain all wrong outcomes; label directly observed stage failures; run only prespecified component-replacement oracle contrasts on a separate diagnostic budget; have two blinded reviewers assess ambiguous semantic failures and adjudicate disagreement. Report unassigned and multi-cause counts. Error-table denominator is all attempted probes, with an additional conditional denominator among errors. Overlapping categories need not sum to 100%. A cap-induced stale answer is not proof of bad inference; a bad edge that never affects any decision is not a causal failure.
