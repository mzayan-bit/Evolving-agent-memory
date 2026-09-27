# Qwen structured-output failure record

**ENGINEERING FIXTURES — NOT RESEARCH EVALUATION.** No human evaluation labels.

## Original `copies` failure (main 84ab65c)

The original five-call legacy phase never dispatched `copies`: the preceding
semantic-bystander case used one schema retry and exhausted that phase. The
separate two-call follow-up actually dispatched `copies` twice. Its visible
records included literal target IDs `s2` (a copied belief despite its prefix) and
`b1`; memory text is not a unique ID. Both outputs instead filled `target_id` with
claim text. They are not manually repaired or semantically matched to IDs.

| Possible cause | Finding |
|---|---|
| Model instruction failure | Yes: exact IDs were visible, but claim text was returned. |
| Prompt ambiguity | Contributing: no separate target/candidate list or explicit prohibition on claim-text IDs. |
| Schema ambiguity | Contributing: `target_id`/`members` were unconstrained strings. The grammar therefore allowed invalid references. |
| Parser weakness | Rejection was correct. Generic `structured_output_invalid` hid the specific reason; diagnostics were weak, not acceptance permissive. |
| Unsupported structured output | No: the corrected nested llama.cpp schema generated nonempty grammar; the output satisfied its broad string types. |
| Target-ID visibility | IDs and kind were visible. Prefix `s2` is not a reliable kind; the field says belief. |
| Serialization | No evidence of corruption; raw prompts contain the IDs and returned token IDs decode correctly. |
| Legacy incompatibility | AND/OR gold is not fully identified by some legacy text. That limits semantic interpretation, but does not excuse wrong ID format. |
| Quantization/backend | No controlled evidence attributes this failure to quantization or CPU execution. |

Failure class: **UNKNOWN_TARGET_ID**, a protocol-invalid output, not a semantic
support judgment. Original retry: one fixed schema reminder; the second output
repeated the same invalid target strings. Two real calls; 1,600 input tokens,
628 output tokens, 88.348 seconds client latency. Some member IDs were valid,
but intended targets were ambiguous/nonunique, so that information was unusable
as a complete support structure. No partial salvage occurs.

The previously observed `assoc <- e` sufficient support is different: it passed
the schema but office-paint evidence does not entail protocol authorization.
It remains **VALID_WRONG_SEMANTICS** in the old immutable receipt. One incorrect
fixture is not scientific evidence. It never triggers protocol repair or retry.

## Expected original schema and exact sanitized raw responses

Only fictional fixture content is shown; transport headers and machine paths
are omitted. The model response strings below are otherwise unchanged.

```json
{
  "additionalProperties": false,
  "properties": {
    "assessments": {
      "items": {
        "additionalProperties": false,
        "properties": {
          "decision": {
            "enum": [
              "specified",
              "none",
              "unknown"
            ],
            "type": "string"
          },
          "groups": {
            "items": {
              "additionalProperties": false,
              "properties": {
                "confidence": {
                  "description": "Finite number from 0 to 1",
                  "type": "number"
                },
                "members": {
                  "items": {
                    "type": "string"
                  },
                  "minItems": 1,
                  "type": "array"
                },
                "relation": {
                  "enum": [
                    "necessary",
                    "conjunctive",
                    "alternative",
                    "partial",
                    "copied",
                    "correlated",
                    "temporal",
                    "scope",
                    "policy",
                    "association",
                    "contradiction",
                    "unknown"
                  ],
                  "type": "string"
                },
                "sufficient": {
                  "type": "boolean"
                }
              },
              "required": [
                "members",
                "relation",
                "sufficient",
                "confidence"
              ],
              "type": "object"
            },
            "type": "array"
          },
          "target_id": {
            "type": "string"
          }
        },
        "required": [
          "target_id",
          "decision",
          "groups"
        ],
        "type": "object"
      },
      "type": "array"
    }
  },
  "required": [
    "assessments"
  ],
  "type": "object"
}
```

### Attempt 1

```json
{
  "assessments": [
    {
      "decision": "specified",
      "groups": [
        {
          "confidence": 0.9,
          "members": ["s3"],
          "relation": "necessary",
          "sufficient": true
        }
      ],
      "target_id": "production capacity eight"
    },
    {
      "decision": "specified",
      "groups": [
        {
          "confidence": 0.9,
          "members": ["s1"],
          "relation": "necessary",
          "sufficient": true
        }
      ],
      "target_id": "production capacity four"
    },
    {
      "decision": "specified",
      "groups": [
        {
          "confidence": 0.8,
          "members": ["s2"],
          "relation": "copied",
          "sufficient": true
        }
      ],
      "target_id": "independent test four"
    },
    {
      "decision": "specified",
      "groups": [
        {
          "confidence": 0.8,
          "members": ["b1"],
          "relation": "copied",
          "sufficient": true
        }
      ],
      "target_id": "production capacity four"
    }
  ]
}
```

### Attempt 2

```json
{
  "assessments": [
    {
      "decision": "specified",
      "groups": [
        {
          "confidence": 0.9,
          "members": ["s3"],
          "relation": "necessary",
          "sufficient": true
        }
      ],
      "target_id": "production capacity eight"
    },
    {
      "decision": "specified",
      "groups": [
        {
          "confidence": 0.9,
          "members": ["s1"],
          "relation": "necessary",
          "sufficient": true
        }
      ],
      "target_id": "production capacity four"
    },
    {
      "decision": "specified",
      "groups": [
        {
          "confidence": 0.8,
          "members": ["s2"],
          "relation": "copied",
          "sufficient": true
        }
      ],
      "target_id": "independent test four"
    },
    {
      "decision": "specified",
      "groups": [
        {
          "confidence": 0.8,
          "members": ["b1"],
          "relation": "copied",
          "sufficient": true
        }
      ],
      "target_id": "production capacity four"
    }
  ]
}
```

## Protocol hardening fixed before new live outputs

- Keep the existing ontology/system instruction and threshold unchanged; append
  generic ID-contract instructions, with no examples or case-specific hints.
- Add `candidate_memory_ids` and `required_target_ids` derived only from visible
  records and `kind`, never from gold, source-prefix spelling or claim text.
- Restrict wire-schema target/member enums to those lists. Keep required fields,
  strict objects, enum relations, AND/OR semantics and complete target checks.
- One protocol-only retry, carrying the same visible payload and contract plus
  the exact malformed response as untrusted JSON data and a fixed reminder.
  No semantic critique/gold enters the retry. Every physical call/token/latency
  remains charged. Refusal, timeout, truncation and budget failures do not retry.
- Parser accepts JSON whitespace only; no prose extraction, enum case folding,
  text-to-ID mapping, missing-ID inference or logical repair. Duplicate JSON
  keys are now explicitly rejected rather than silently overwritten.
- Runtime `VALID_CORRECT_FORMAT` says nothing about semantics. Only the separate
  engineering evaluator may attach `VALID_WRONG_SEMANTICS` after inference ends.
- Under the user's requested B5a distinction, live B5a now separately elicits
  singleton links from the SAME evidence; B5b retains support sets. Historical
  shared-proposal projection remains supported for recorded/frozen experiments,
  explicitly distinct from the new elicitation path. No uncertainty controls
  verification, replay or quarantine.

Exact constants and schema version: `models/inference.py` development-v2.
New live results and exact per-attempt categories are in the companion engineering
error audit; this historical failure record is not overwritten by later success.
