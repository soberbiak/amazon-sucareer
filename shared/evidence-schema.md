# Career Evidence Ledger v2.0

The Career Evidence Ledger is the only Claim/Evidence system in this plugin. Downstream skills must reference its claim IDs and must not maintain a second ledger.

## Top-level contract

```yaml
schema_version: "2.0"
fictional: false
candidate_ref: Candidate
target_track: undecided
sources: []
claims: []
open_questions: []
```

`fictional: true` is required for repository fixtures. Private candidate work uses `false`. `candidate_ref` is a local label, not a public identifier. `target_track` is `campus`, `experienced`, or `undecided`.

## Claim contract

```yaml
claim_id: C-001
claim_type: action
source_fact: ""
candidate_interpretation: ""
resume_candidate_statement: ""
source_ids: []
evidence_status: unverified
responsibility: contributor
scope: ""
period: ""
metrics: []
dependencies: []
attribution:
  strength: observed
  alternative_drivers: []
causality:
  status: unknown
  mechanism: ""
  confounders: []
confidence:
  level: low
  reason: ""
confidentiality: public_safe
operating_mechanisms: []
competencies: []
business_values: []
jd_relevance: []
interview_risk: medium
notes: ""
```

### Controlled values

- `claim_type`: `scope`, `problem`, `action`, `mechanism`, `result`, `skill`, or `context`.
- `evidence_status`: `verified`, `derivable`, `unverified`, or `excluded`.
- `responsibility`: `owner`, `co_owner`, `contributor`, or `observer`.
- `attribution.strength`: `delivered`, `enabled`, `contributed`, or `observed`.
- `causality.status`: `supported`, `plausible`, `correlated`, `unknown`, or `not_applicable`.
- `confidence.level`: `high`, `medium`, or `low`.
- `confidentiality`: `public_safe`, `generalize`, or `private_only`.
- `interview_risk`: `low`, `medium`, or `high`.

`source_fact` preserves what the source says. `candidate_interpretation` records an explicitly labeled inference. `resume_candidate_statement` is optional candidate wording and is never treated as evidence.

## Metric object

Each metric object uses `name`, `unit`, `baseline`, `result`, `direction`, `window`, `scope`, and `method`. Use `null` for unavailable values. A derivable value must show reproducible arithmetic. Do not interchange percentage-point and relative-percent changes.

## Invariants

- A `verified` claim has at least one known `source_id`.
- A `derivable` claim records its formula in `notes` or the metric `method`.
- `operating_mechanisms`, `competencies`, and `business_values` are interpretations attached to evidence; they do not upgrade evidence status.
- `resume_candidate_statement` cannot be stronger than responsibility, attribution, causality, confidence, or confidentiality permits.
- Excluded or private-only claims are never sent to a public resume.
