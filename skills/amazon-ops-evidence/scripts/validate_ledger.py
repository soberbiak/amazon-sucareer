#!/usr/bin/env python3
"""Validate the Career Evidence Ledger v2.0 structural contract."""

from __future__ import annotations

import json
import sys
from pathlib import Path


TOP_LEVEL = {
    "schema_version", "fictional", "candidate_ref", "target_track",
    "sources", "claims", "open_questions",
}
CLAIM_FIELDS = {
    "claim_id", "claim_type", "source_fact", "candidate_interpretation",
    "resume_candidate_statement", "source_ids", "evidence_status",
    "responsibility", "scope", "period", "metrics", "dependencies",
    "attribution", "causality", "confidence", "confidentiality",
    "operating_mechanisms", "competencies", "business_values",
    "jd_relevance", "interview_risk", "notes",
}
CLAIM_TYPES = {"scope", "problem", "action", "mechanism", "result", "skill", "context"}
STATUSES = {"verified", "derivable", "unverified", "excluded"}
RESPONSIBILITIES = {"owner", "co_owner", "contributor", "observer"}
TARGET_TRACKS = {"campus", "experienced", "undecided"}
CONFIDENTIALITY = {"public_safe", "generalize", "private_only"}
ATTRIBUTION = {"delivered", "enabled", "contributed", "observed"}
CAUSALITY = {"supported", "plausible", "correlated", "unknown", "not_applicable"}
CONFIDENCE = {"high", "medium", "low"}
INTERVIEW_RISK = {"low", "medium", "high"}


def require_object(label: str, value: object, fields: set[str], errors: list[str]) -> bool:
    if not isinstance(value, dict):
        errors.append(f"{label} must be an object")
        return False
    missing = fields - value.keys()
    if missing:
        errors.append(f"{label} missing: {', '.join(sorted(missing))}")
        return False
    return True


def validate(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["top level must be a JSON object"]
    missing = TOP_LEVEL - data.keys()
    if missing:
        return [f"missing top-level fields: {', '.join(sorted(missing))}"]

    if data["schema_version"] != "2.0":
        errors.append("schema_version must be '2.0'")
    if not isinstance(data["fictional"], bool):
        errors.append("fictional must be true or false")
    if data["target_track"] not in TARGET_TRACKS:
        errors.append(f"target_track must be one of {sorted(TARGET_TRACKS)}")
    for field in ("sources", "claims", "open_questions"):
        if not isinstance(data[field], list):
            errors.append(f"{field} must be a list")
    if not isinstance(data["sources"], list) or not isinstance(data["claims"], list):
        return errors

    known_sources = {
        item.get("source_id") for item in data["sources"]
        if isinstance(item, dict) and item.get("source_id")
    }
    seen_claims: set[str] = set()
    for index, claim in enumerate(data["claims"]):
        label = f"claims[{index}]"
        if not require_object(label, claim, CLAIM_FIELDS, errors):
            continue
        claim_id = claim["claim_id"]
        if not isinstance(claim_id, str) or not claim_id.strip():
            errors.append(f"{label}.claim_id must be a non-empty string")
        elif claim_id in seen_claims:
            errors.append(f"duplicate claim_id: {claim_id}")
        else:
            seen_claims.add(claim_id)
        if claim["claim_type"] not in CLAIM_TYPES:
            errors.append(f"{label}.claim_type is invalid")
        if claim["evidence_status"] not in STATUSES:
            errors.append(f"{label}.evidence_status is invalid")
        if claim["responsibility"] not in RESPONSIBILITIES:
            errors.append(f"{label}.responsibility is invalid")
        if claim["confidentiality"] not in CONFIDENTIALITY:
            errors.append(f"{label}.confidentiality is invalid")
        if claim["interview_risk"] not in INTERVIEW_RISK:
            errors.append(f"{label}.interview_risk is invalid")
        for field in ("source_ids", "metrics", "dependencies", "operating_mechanisms",
                      "competencies", "business_values", "jd_relevance"):
            if not isinstance(claim[field], list):
                errors.append(f"{label}.{field} must be a list")
        if isinstance(claim["source_ids"], list):
            unknown = set(claim["source_ids"]) - known_sources
            if unknown:
                errors.append(f"{label} references unknown sources: {sorted(unknown)}")
            if claim["evidence_status"] == "verified" and not claim["source_ids"]:
                errors.append(f"{label} is verified but has no source_ids")
        if require_object(f"{label}.attribution", claim["attribution"],
                          {"strength", "alternative_drivers"}, errors):
            if claim["attribution"]["strength"] not in ATTRIBUTION:
                errors.append(f"{label}.attribution.strength is invalid")
            if not isinstance(claim["attribution"]["alternative_drivers"], list):
                errors.append(f"{label}.attribution.alternative_drivers must be a list")
        if require_object(f"{label}.causality", claim["causality"],
                          {"status", "mechanism", "confounders"}, errors):
            if claim["causality"]["status"] not in CAUSALITY:
                errors.append(f"{label}.causality.status is invalid")
            if not isinstance(claim["causality"]["confounders"], list):
                errors.append(f"{label}.causality.confounders must be a list")
        if require_object(f"{label}.confidence", claim["confidence"],
                          {"level", "reason"}, errors):
            if claim["confidence"]["level"] not in CONFIDENCE:
                errors.append(f"{label}.confidence.level is invalid")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_ledger.py CAREER_EVIDENCE_LEDGER.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors = validate(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {path} ({len(data['claims'])} claims, schema 2.0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
