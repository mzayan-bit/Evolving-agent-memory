# Baseline-only pilot design — NOT RUN

## Stage 0: the existing 30

Complete two independent human passes and adjudication before any model evaluation. The 30 openly inspected drafts are development material only. Correct support semantics, ambiguity labels and source provenance; run schema checks. Do not count them as held-out evidence. No new controller, classifier or memory application is authorized by this plan.

## Stage 1: deliberately smaller than 720 trajectories

After the annotation gate, avoid multiplying every regime/seed before estimating costs. Instead begin with **12 new scenarios × 8 policies × 2 families × 1 paired seed × 2 regimes = 384 trajectories**, each with three revisions and a fixed current/historical/action/reuse probe schedule. This exceeds neither a preapproved cost cap nor model context limits; exact dollar cap must be approved after dry-run token estimation. Do not run it in this phase.

The eight policies are the seven requested simple policies plus point-estimate support-set truth maintenance/rederive, required by classical prior art. No future uncertainty method is included. First eight calibration/debug scenarios and four held-out domain/template cases yield only a small transfer sanity check, not a generalization claim. Freeze splits before seeing outputs. All variants of a source scenario stay together. These 12 are **new**, not selected from the 30 after seeing behavior.

Regimes: complete observed support versus a combined missing/spurious stress regime (target 70% true incidence retention, .30 false/true incidence; report actual rates). This initial contrast tests existence/headroom, not separate causal effects. If headroom exists, next stage separates missing-only, spurious-only, combined and source-correlation changes. Avoid attributing the combined contrast to either omission or false links. Three revisions include an independent-support survival opportunity and a delayed reuse opportunity; not every scenario must include every family.

## Objectives and ordering

First run serialization/visibility/scoring checks without LLMs. Then a cost-estimation batch of at most two new scenarios for one backbone and the no-repair/full-replay/point-support/conservative policies, counted as development only. Record actual tokens/calls/errors before approving the remainder. Stop on budget exhaustion, invalid gold, hidden oracle fields, or failure to represent provenance correctly. Randomize policy execution order; share initial histories and corruption masks.

Establish phenomenon size, variance, baseline strength, protocol defects and real costs. Do not select scenarios, prompts or model settings based on which favors a future method. Bootstrap at scenario level; 12 scenarios cannot support a strong null/generalization conclusion. Expand only under [kill/expansion rules](KILL_CRITERIA.md), with independent confirmation material and two additional seeds if warranted. The earlier ~60×6×2=720 reference omitted a necessary classical baseline and corruption/seed dimensions; it is not a fixed commitment.

## Model plan

One proprietary family: **Claude Sonnet**, provisionally a frozen Sonnet 4.6 snapshot where available; [official release](https://www.anthropic.com/news/claude-sonnet-4-6). One accessible open-weight family: **Qwen3.5-9B**, [official model card](https://huggingface.co/Qwen/Qwen3.5-9B). Families are chosen for contrasting deployment/access, not expected G1 advantage. The small open model is not capacity-matched to Sonnet, so compare policy effects within each backbone rather than model leaderboard scores.

Before execution record exact API model ID/version/date/provider, open-weight commit and weight/tokenizer hashes, license, precision/quantization, serving runtime, device, context limits, system/user prompts, decoding parameters, seed behavior and cache setting. Freeze common maximum input/output tokens to the smaller feasible setting after a dry run; no silent truncation. If a provider snapshot disappears, restart affected comparisons or treat versions as separate cohorts. No training is required. Model/version/pricing availability must be rechecked at execution.

## Judge and contamination design

Use structured per-revision current/historical/action labels and deterministic support/provenance checks where possible. Human adjudication is primary for semantic ambiguity. LLM judging can map natural-language equivalence only, blinded to policy names and expected ranking. Rejudge a balanced disagreement/error sample with a distinct model family and humans; publish disagreement and rank sensitivity. No single self-judge determines success.

Public STALE examples may be familiar to models; they are development only. Hold out new human-authored domains/templates/entities and source phrasings. Do not generate and judge with the same evaluated model family. Keep judge rubric independent from method prompts. Similarity/de-duplication checks detect exact/template leakage but cannot certify absence of training contamination. Runtime sees only the past prefix; evaluator gold, later revisions, corruption masks and benchmark explanations are inaccessible. Delayed summaries/reuse are fixed probes, not hints announcing what was repaired.

## Persistence and counterfactual controls

Every arm has identical initial state. Compare answer-only audit versus explicit persistent-store updates through a declared adapter; charge adapter writes and verification. Source-only and full-replay semantics must preserve historical facts when required. Include a full-reset-with-archive variant to avoid making reset lose history by construction. Add oracle lineage only as a separate upper bound, not counted in the eight main policies. The 384 is planned trajectory count, not executed work.
