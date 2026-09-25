# Model and judge plan — availability checked 2026-09-25

Candidate, not an execution configuration. No model calls, keys, weights or GPU provisioning in this phase.

| Role | Candidate and pin | Feasibility and limits |
|---|---|---|
| API backbone | `claude-sonnet-5`, Anthropic native API | Official documentation lists a 1M context, 128K maximum output and structured-output guidance. Release IDs from generation 4.6 onward are pinned snapshots, not rolling aliases. Current advertised base rates are $2 input/$10 output per million tokens; archive a pricing table at execution, do not embed these in scoring. Account access/quota remains untested. |
| Open-weight backbone | `Qwen/Qwen3.5-9B`, HF revision `c202236235762e1c871ad0ccb60c8ee5ba337b9a` | Official instruction model, Apache-2.0; native 262,144 context. Pin weights/tokenizer/config/chat template plus serving runtime. Schema-constrained decoding is a serving feature to verify, not a guarantee inferred from model branding. No hardware throughput/fit measured here. |

Sources: [Sonnet 5 official model page](https://platform.claude.com/docs/en/models/sonnet-5/overview), [structured-output changes](https://platform.claude.com/docs/en/models/sonnet-5/whats-new-sonnet-5), [snapshot versioning](https://platform.claude.com/docs/en/about-claude/models/model-ids-and-versions), [Qwen official card](https://huggingface.co/Qwen/Qwen3.5-9B), [pinned Qwen revision](https://huggingface.co/Qwen/Qwen3.5-9B/tree/c202236235762e1c871ad0ccb60c8ee5ba337b9a).

This replaces the earlier provisional Sonnet 4.6 selection with a currently documented family release before any pilot output. Do not claim either model is the strongest available. Qwen-9B is an accessibility/cost candidate, not capacity-matched to the API model. A larger open-weight family member or stronger API model must be considered as a development/sensitivity threat; if the phenomenon disappears with capability, bound or abandon the method claim.

Freeze effective common context, output cap, reasoning effort, decoding, cache policy, tokenizer and timeout on development-only adapter checks. Do not assume temperature=0 or identical numeric seeds are supported across providers. Sonnet 5 disallows non-default sampling parameters according to its release documentation; log actual supported settings rather than sending invalid controls. Open model local compute is not free: publish device, precision, throughput, latency and hardware accounting separately from API dollars. A nominal 1M model window is not a study allocation.

## Judging

Deterministic evaluation suffices for IDs, status changes, fixed support operations, interval/scope constraints, explicit action constraints, budgets and fixed structured propositions. It cannot adjudicate natural-language entailment, independence or hidden implicit premise use. Those labels need the independent humans and adjudicator.

Use a blinded semantic-equivalence judge only for free-text mapping to already adjudicated acceptable answers. Avoid same-family generator/sole-judge loops: cross-family judging and a human tie-break are required, with deterministic scoring retained where possible. Do not invent a third judge model ID until its availability/cost is verified. Freeze judge prompt/examples and independence assumptions before evaluation.

Human spot-check candidate: all model/human disagreements and all positive-gain cases, plus a stratified random 10% of agreements per family/condition, minimum 20 items if available. Report this as an audit sample, not a random population accuracy estimate. Preserve disputed/ambiguous labels, publish judge disagreement and sensitivity of policy ordering to human-only versus model-assisted mappings. Human review workload and judge costs are separate ledger phases and part of total study cost.
