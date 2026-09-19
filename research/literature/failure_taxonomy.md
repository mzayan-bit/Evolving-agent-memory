# Failure taxonomy for evolving agent memory

This is a synthesis of the inspected papers, not a claim to invent these failure categories. A final wrong answer can have several causes. An error taxonomy is not, by itself, causal attribution. See [AgingBench](https://arxiv.org/abs/2605.26302), [MemFail](https://arxiv.org/abs/2605.26667), [MemOps](https://arxiv.org/abs/2607.12893), [HaluMem](https://arxiv.org/abs/2511.03506) and [Causal Agent Replay](https://arxiv.org/abs/2606.08275).

| Stage | Failure and observable symptom | Closest evidence | Diagnostic intervention | Important ambiguity |
|---|---|---|---|---|
| Formation | Relevant fact omitted; irrelevant or unsupported fact persisted | HaluMem extraction; MCB erroneous persistence | Supply gold extracted entries while preserving later stages | Extra oracle information changes more than the writer unless controlled |
| Binding | Fact attached to wrong person, scope, slot or target | MemFail Persona-Retrieval; MemOps target probes | Correct entity/scope IDs only | Identity resolution and retrieval can interact |
| Retrieval | Relevant current fact missed; distractor or stale fact selected | LongMemEval retrieval/reading; MemStrata | Inject gold evidence with matched token count | Gold recall does not imply reader correctness |
| Revision | Compatible facts incorrectly overwritten; changed fact not superseded | MemFail Coexisting-Facts; STALE; StateMem | Correct only the affected state transition | Newer evidence can be wrong or describe a different scope |
| Temporal interpretation | Event time confused with ingestion time; current/historical intent confused | Zep, TOKI, RD-Forget | Hold content constant, vary query time and arrival order | Historical truth is not a contradiction in the same temporal scope |
| Conflict adjudication | Wrong source selected; recency or majority mistaken for authority | BeliefMem, CAMA, Memory Trust Gap | Factor source authority, independent support and recency | Source authority does not ensure factual truth |
| Consolidation | Qualifier lost, unsupported generalization, identity drift | HaluMem, MemFail Conditional-Facts, TRUSTMEM, MemOps Reflect | Compare raw evidence with summary under matched answer budget | An answer gain can hide corrupted persistent state |
| Provenance/authority | Unendorsed source becomes an apparently authorized durable instruction | AuthMem-Bench; provenance laundering | Preserve source labels through the same transformation | A writer that drops everything avoids upgrades but destroys utility |
| Evidence dependence | Copied traces counted as independent confirmation | GovMem; CAMA | Vary lineage while holding proposition frequency fixed | Shared language is neither necessary nor sufficient for shared source |
| Forgetting | Invalid information survives; useful unrelated information removed | Memora; MemSecBench; MemOps Forget | Evaluate removal and benign retention from the same initial state | Suppression in retrieval differs from physical erasure |
| Dependency propagation | Descendant not reconsidered; irrelevant branch unnecessarily invalidated | CUPMem, StateMem, MemTX, rollback repair | Remove a prerequisite; retain an independent sufficient support set | Association is not entailment; support may be conjunctive or alternative |
| Behavior after update | Store is correct, response or pending plan still uses old premises | StateAuditor; PlanFence | Change state after planning and inspect action authorization | A fresh read need not refresh the plan |
| Execution-state retention | Deleted record survives in summary, plan, transcript or KV cache | Execution-state Unlearning | Restore clean prefix/replay, compare leakage and behavior | Hosted APIs may not expose runtime state; external actions may be irreversible |
| Enforcement | Record marked revoked still retrieved or acted upon | Revoked but Still Authoritative | Inspect retrieval before downstream generation | A status field is not an enforced policy |
| Control | Wrong operation, unnecessary retrieval, premature stopping or failure to ask | AgeMem, BudgetMem, MemCon, Router-Mem, MCB | Fixed-budget operation ablations and actual tool-call evaluation | Stated policy/action label can differ from selected tool |
| Resource accounting | Context shrinks while archive, indexes or write-call costs grow | TierMem, RD-Forget, OAS, SkillZip Pro | Account for all retained bytes and all paid calls | Active context, storage, cache, latency and dollars are not interchangeable |
| Evaluation | Apparent gain caused by stronger answerer, evidence leakage, unequal budget or adapted baseline | LightMem reproduction; MemoryLake matched study | Fix model, data, information access and accounting boundary | “Same framework” is weaker than cost-matched and representation-only |

## Distinctions that must survive an implementation

- **False:** never supported as true in the relevant world/time/scope.
- **Historical:** supported at an earlier valid time, not necessarily true now.
- **Superseded:** replaced within a defined slot/scope; old value may remain historically useful.
- **Contradicted:** competing evidence exists; not automatically resolved by deleting the older item.
- **Uncertain:** insufficient evidence to determine validity; an uncertainty label needs operational meaning.
- **Revoked:** use is no longer authorized under a policy, even if the factual statement remains true.
- **Forgotten:** specify whether the goal is answer-time suppression, store erasure, execution-state counterfactual behavior or parameter unlearning.

These are analytical definitions, informed by [Zep](https://arxiv.org/abs/2501.13956), [MemTX](https://arxiv.org/abs/2607.23929), [BeliefMem](https://arxiv.org/abs/2605.05583), [AuthMem](https://arxiv.org/abs/2608.01679) and [execution-state unlearning](https://arxiv.org/abs/2609.04875). They are not proposed new state names.

## The motivating dependency example needs an explicit rule

“Alice leads Team X” and “Team X owns Project Y” do **not** logically entail “Alice approves Project Y releases.” A policy such as “the current team lead approves releases for projects owned by the team” is additionally required. A change in leadership justifies **reconsideration**, not unconditional deletion of Alice's approval authority: she may retain independent authorization. The leading direction must distinguish logical prerequisites, statistical relevance, copied evidence and alternative support. Otherwise an impressive propagation graph can simply spread false invalidations.

## Measurement discipline

Report both stale-error rate among all eligible cases and conditional error among answered cases; also report coverage/abstention. Report false invalidation among gold-unaffected items, plus absolute damage counts. A method that abstains on everything or deletes all memory must not win. Cluster uncertainty intervals by underlying scenario/user/trace, not by repeated paraphrase or probe. Use oracle interventions as upper bounds, and separate them from deployable evidence-inference policies. Do not infer a unique cause from one intervention when multiple operations can compensate for each other.
