---
name: amazon-ops-resume-audit
description: Audit an Amazon operations resume against Career Evidence Ledger v2.0. This alpha skeleton identifies unsupported claims, attribution, metric, causality, confidentiality, and interview risks; it does not create missing evidence.
---

# Amazon Ops Resume Audit — alpha scope

This skill is intentionally lightweight in v0.3.0-alpha.5. Read the shared [evidence schema](../../shared/evidence-schema.md), [attribution rules](../../shared/attribution-rules.md), [causality rules](../../shared/causality-rules.md), and [confidentiality rules](../../shared/confidentiality-rules.md).

Map every material resume statement to claim IDs. Classify findings as unsupported fact, over-attribution, missing metric context, weak causality, confidentiality risk, vague task-only language, or interview risk. Return `keep`, `soften`, `remove`, or `recover_evidence` with reasons. Never repair a finding by inventing a fact.
