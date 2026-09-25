# Experimental harness — engineering v1

This implementation is authorized infrastructure only. **The real G1 pilot remains disabled.** Fixture runs are engineering validation, not research findings. Human annotation files and authored scenario labels are neither modified nor used by the runner. The earlier draft protocol's interface-only instructions describe the preceding phase; the subsequent implementation request authorizes this baseline phase without changing the scientific question.

## Architecture and contracts

Plain standard-library Python, no service or provider dependency. The requested nested layout is compressed into cohesive modules:

- `src/evomem/model.py`: immutable `Memory`, typed `Relation`/`Status`/`Action`, `Support`, `Revision`, `InformationAccess`, `Snapshot`, `PolicyView`, `Decision`, `Scenario`.
- `policies.py`: `RepairPolicy` and separate `InferenceProvider` protocols; eight baselines, default frozen proposal provider, deterministic cosine.
- `simulation.py`: chronology, access projection, immutable archives, corruption, fixed reader and trace.
- `evaluation.py`: evaluator-only `Gold`, `CheckpointGold`, fixed `Probe`, numerator/denominator `Rate`, scoring and cluster macro aggregation.
- `cost.py`: per-operation `CostEvent`, `Ledger`, hard `Budget` constraints.
- `data.py`: future adjudicated interchange import and validation. `fixtures.py`: seven tiny independent engineering examples.
- `experiment/run.py`: fixture CLI, manifests, JSONL results, aggregate and full operation/answer logs.

Memory stores identity, content, scope, half-open valid interval, status, source refs, creation checkpoint, kind, origins and authority. A memory can be an assumption/artifact rather than a fact. The first adapter repairs the status of fixed propositions, including reactivating a legitimate returning value. It does not generate replacement natural-language content. New source versions append records; source supersession closes present validity but does not mutate earlier snapshots.

Support records contain a justification ID, target, nonempty unique member set, relation type, scope, interval, origins and explicit sufficiency. Members are AND; multiple records for a target are OR. All twelve ontology types are representable. Association, partial, contradiction and unknown are not sufficient entailments. Empty/unknown support is never an axiom. Fixed-point evaluation begins only from active base sources, so ungrounded cycles cannot certify themselves. Copies must have explicit upstream derivations; origin sets with overlap or unknown origins do not establish independent confirmations. The independent-retention denominator is evaluator adjudication, not an origin heuristic promoted to gold.

## Scientific isolation

Runtime `Scenario` and evaluator `Gold` are separate values. Policies receive a newly constructed frozen `PolicyView`, not a scenario/evaluator object or callback that can query expected answers. Projection excludes future source versions and future rule incidences. Fault identity, dependencies, provenance, authority and archived snapshots have explicit switches. Hidden fault cues also redact the revision's explicit before-ID; ordinary visible evidence may still permit diagnosis. Hidden provenance removes both source refs and origin groups, including archived snapshots and new revision records.

Oracle dependency access requires an explicitly supplied oracle bundle and a true flag; oracle flags appear in manifests. Gold affected sets and query answers never enter any policy view. External-evidence access is rejected because no adapter is installed. `full_history` controls past snapshots, not removal of inactive records from the current persistent store. These boundaries prevent accidental data flow; Python objects are not a security sandbox against malicious introspection or arbitrary user-supplied code.

Fixtures provide explicit executable domain rules as common evidence, separate from the observed/inferred lineage proposal. No rule is extracted from adjudicated gold at runtime. These intentionally tractable fixtures cannot assess natural-language inference. A natural-language pilot requires a common verified evidence/derivation adapter before it can use B2/B6 meaningfully.

## Corruption and reproducibility

Synthetic interventions: seeded member-incidence removal without replacement; explicit spurious support insertion; seeded support-type change to non-sufficient association; hide provenance; hide change/fault cue. Corruption returns new observed records and never modifies evaluator gold. When a removed AND member leaves a nonempty group, the policy sees that ordinary reduced point estimate without a hidden incompleteness warning; empty groups disappear, never become axioms.

Logs record original true incidence counts, retained and inserted counts, and the exact removed/inserted masks. Rates can be computed from these counts; zero-gold-incidence rates are undefined. Counts rather than fractional corruption settings are used for tiny fixtures. Spurious insertion is a Python API accepting explicitly reviewed false incidences; the minimal CLI supports the other scalar switches. Random corruption is explicitly synthetic and does not substitute for natural annotation.

## Budgets and costs

Each trajectory gets the same independent caps for verification, replay steps, model calls, total input+output tokens, and retrieval. Unlimited means null. Ledger events have unique physical operation IDs, phase/checkpoint, token counts, cached-input subset, model/verification/retrieval/embedding/tool/replay counters, latency, status, usage provenance, model and retry parent IDs. Failures and retries are distinct charged operations. Synthetic token tests are labeled synthetic; missing actual usage stays null. Unknown token usage cannot certify compliance with a binding cap.

Deterministic operations preflight the ledger. Exceeding a cap raises `BudgetExceededError`; built-in policies convert expected exhaustion to explicit `budget_exhausted` completion. Full replay preserves the last fully committed derived state when incomplete. Conservative reverify retains unchecked records with an explicit checked-ID list. No cap exception is silently treated as successful completion. Unused model/embedding resources are zero, not fabricated estimates of paid work. Real wall-clock maintenance and readout/scoring latency is recorded; fixture wall time is not a model-price or hardware-cost estimate.

No network/model adapter is present. Before introducing one, add reservation/reconciliation of worst-case output capacity, physical-call accounting, retry/timeouts, per-call context limits, and the frozen pilot's per-revision released credits. Current integer trajectory caps implement matched deterministic fixture resources, **not the complete six-credit model schedule**. No claim of matched real-model compute is possible yet. The ledger can represent multi-call replay and unknown usage, but the installed runner cannot execute such calls.

## Metrics and interpretation

Every per-trajectory metric includes count, eligible, rate; zero denominator is null. SDRR uses fixed affected-item probe opportunities, independent of retrieval. FIR counts valid items inactivated/superseded; valid quarantine and combined nonavailability are separate. Repair recall measures correct deactivation of formerly valid affected fixed propositions; precision counts active→inactive content availability changes, excluding quarantine/provenance-only retention. Fixed-proposition status repair cannot claim successful generated replacements.

Independent support retention uses the supplied I subset of V. Recurrence requires an immediate repaired/unusable stale proposition and later affected current probes, stopping at legitimate reinstatement. Current and historical accuracy use fixed expected answers, including required abstention. Historical-then and historical-now remain separate query views. Abstention, unresolved-current abstention and unique-item/revision reverify coverage are also emitted. Unknown support relations remain unknown/quarantined; they are not automatically scored as factual falsity.

The shared reader emits structured answers and used-item IDs; active identity lookup is reliance in these fixtures. An LLM adapter will need separate exposure/reliance traces and human review of implicit premise use. Present historical permissions are applied from observed permission revisions. Correction replay is based on explicit rules, retaining independent historical alternatives.

Aggregation first averages eligible variants within a base scenario cluster, then equally across clusters; exact duplicate cluster/variant keys fail. Eligible and total cluster counts are reported. No bootstrap inference, p-values, calibration, power estimate, empirical ranking or hypothesis test is produced here. Failed API runs and free-text action correctness await real adapters; they must not be silently excluded in a later pilot.

## Future adjudicated import

`load_adjudicated(Path(...))` accepts JSON only, schema `g1-adjudicated-1`, status `ADJUDICATED`, and nonempty adjudication metadata: reviewer, agreement_report, protocol_version. The top-level fields are exactly `schema_version`, `status`, `adjudication`, `scenario`, `gold`. Nested field names match the dataclasses; include every declared field, serialize tuple/set values as arrays and enums as their lowercase strings. The roundtrip unit test is an executable schema example using **synthetic test provenance**, not human labels.

Scenario contains initial memories, ordered revisions, observed lineage and explicit runtime evidence rules. Gold contains support assessments, checkpoint A/V/I/U sets and fixed probes. Probes declare current/historical_then/historical_now plus as_of, expected content or null. Unknown relations use `relation=unknown, sufficient=false`; genuinely unresolved items belong to U. A null answer expectation means required withholding and does not itself mean the underlying fact is false.

Import rejects pending/raw author data, missing/extra fields, invalid typed labels, duplicate memory/justification/probe IDs, duplicate measurement IDs, impossible/future references, invalid intervals, overlapping gold strata, and invalid checkpoint/query ordering. This is a format validator, not authentication of a person's adjudication. It does not automatically translate raw A/B forms, resolve disagreements or manufacture executable rules from semantic labels. Human-reviewed conversion must establish both evidence semantics and fixed probe expectations. The CLI deliberately cannot run this data yet.

## Commands and artifacts

From the repository root:

```bash
uv sync
uv run pytest
uv run ruff check .
uv run mypy src tests
uv run python -m evomem.experiment.run --config experiments/configs/fixtures.json
```

If the environment blocks the default uv cache, prefix each command with `UV_CACHE_DIR=/private/tmp/evomem-uv-cache`. The lockfile fixes dependencies. Change experiment_id for a second run; existing directories are never overwritten. Dirty trees are rejected unless the configuration explicitly says `allow_dirty: true`, recorded in the manifest. Non-engineering modes are always rejected.

Each `results/<id>/` contains `manifest.json`, `per_scenario.jsonl`, `aggregate.json`, `logs/*.json`. Manifest includes commit, dirty state, UTC time, Python/scenario version, complete policy configuration, model IDs (empty here), seed, access flags, budgets, metrics/costs and artifact SHA-256 hashes. Logs contain state/action snapshots, fixed answers/used IDs, corruption audit and cost events. Generated results are gitignored. Timing and timestamp fields are naturally variable; deterministic inputs/state/metrics are reproducible.

## Validation and readiness

Scientific tests cover all seven fixtures: necessary, independent alternatives, conjunction, semantic bystander, repeated 4→8→4, copied support and retrospective correction. Tests cover all eight policies' immutable history; AND/OR/copies; omission/oracle separation; false edges; corruption determinism; unsupported cycles; atomic replay exhaustion; retained unchecked records; exact multi-call synthetic ledger and retries; fixed denominators; recurrence versus reinstatement; cluster aggregation; importer validation; artifact writing and pilot gate.

This phase is ready for deterministic engineering integration. **It is not ready to execute the real pilot.** Still required: independent human annotations, agreement and qualitative review, adjudicated/versioned evidence and gold, reviewed executable/evidence adapters, held-out scenarios, frozen protocol and budgets/model snapshots, and pilot approval. No human annotation files were filled and no API credits were spent.
