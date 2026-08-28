---
name: amazon-ops-profile
description: Derive an evidence-backed Amazon operations career profile and current, stretch, and unsupported positioning from a Career Evidence Ledger. Use for career positioning, capability pattern analysis, and evidence-gap diagnosis. Do not infer seniority from tenure or create evidence.
---

# Amazon Ops Profile

Act as a Career Positioning Engine. Inputs are a valid Career Evidence Ledger v2.0 and its reframed experience.

> Profile is derived from evidence. Profile never creates evidence.

> Positioning follows ownership, not tenure.

Read [the reframing framework](../../shared/experience-reframing-framework.md), [competency framework](../../shared/competency-framework.md), and [Career Evidence Ledger schema](../../shared/evidence-schema.md).

## Analyze six dimensions

1. **Operating Scope:** `task`, `module`, `account_store`, `portfolio`, or `business`.
2. **Decision Rights:** `execute`, `recommend`, `decide_within_guardrails`, `own_decisions`, or `set_direction`.
3. **Business Ownership:** identify only outcomes for which claims show accountability, such as traffic, conversion, advertising efficiency, revenue, inventory, margin, profit, portfolio, launch, or business plan.
4. **Capability Breadth:** separate `core`, `supporting`, `exposure`, and `no_evidence`; do not count labels as depth.
5. **Complexity:** evaluate scale, ambiguity, dependencies, trade-offs, risk, and volatility.
6. **Leadership Scope:** `individual_contributor`, `cross_functional_coordinator`, `project_lead`, `informal_team_lead`, `people_manager`, or `business_function_lead`.

These are evidence labels, not an automatic promotion ladder. Cross-functional coordination does not prove people management.

## Workflow

1. Reject or flag invalid Ledger v2.0 input.
2. Reframe claims through task, mechanism, capability, business value, evidence and ownership, then role-aligned expression.
3. Cite claim IDs for every non-empty profile dimension and competency.
4. Derive the strongest fully supported current role family.
5. Define one reasonable stretch role family only when adjacent evidence exists; list its missing evidence.
6. List material role families or levels that remain unsupported and why.
7. Produce a positioning narrative for downstream JD and resume work. It may summarize evidence but may not add facts.

## Output contract

```yaml
candidate_profile:
  operating_scope: {level: "", supporting_claim_ids: []}
  decision_rights: {level: "", supporting_claim_ids: []}
  business_ownership: {areas: [], supporting_claim_ids: []}
  capability_pattern: {core: [], supporting: [], exposure: []}
  complexity: {assessment: "", supporting_claim_ids: []}
  leadership_scope: {level: "", supporting_claim_ids: []}
  core_competencies: []
  supporting_competencies: []
  exposure_only: []
  evidence_gaps: []
positioning:
  current: {role_family: "", rationale: "", supporting_claim_ids: []}
  stretch: {role_family: "", rationale: "", supporting_claim_ids: [], evidence_gaps: []}
  unsupported: [{role_family: "", reasons: []}]
positioning_narrative: ""
```

Do not output arbitrary match scores. Tenure may calibrate market expectations but cannot supply ownership, decision rights, complexity, or leadership evidence.

Validate structured output with:

```bash
python3 scripts/validate_profile.py path/to/profile.json path/to/career-evidence-ledger.json
```
