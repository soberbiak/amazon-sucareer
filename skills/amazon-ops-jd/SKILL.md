---
name: amazon-ops-jd
description: Map an Amazon operations job description to a Career Evidence Ledger and career profile. This alpha skeleton is for structured JD requirements and evidence mapping; it does not score fit or alter candidate facts.
---

# Amazon Ops JD — alpha scope

This skill is intentionally lightweight in v0.3.0-alpha.5. Read [Career Evidence Ledger v2.0](../../shared/evidence-schema.md) and accept positioning only from `$amazon-ops-profile`.

Extract role level, responsibilities, hard requirements, preferred qualifications, business KPIs, Amazon knowledge, leadership needs, data needs, ATS terms, implicit expectations, and required evidence. Map each requirement to claim IDs as `strong_match`, `supported_match`, `partial_match`, `no_evidence`, or `mismatch`.

Do not invent numerical match scores. JD adaptation must not alter facts. Return the evidence map, missing evidence, and neutral handoff notes for `$amazon-ops-resume`.
