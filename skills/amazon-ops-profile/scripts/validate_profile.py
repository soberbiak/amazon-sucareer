#!/usr/bin/env python3
"""Validate profile structure and ensure every referenced claim exists."""

from __future__ import annotations

import json
import sys
from pathlib import Path


PROFILE_FIELDS = {"candidate_profile", "positioning", "positioning_narrative"}
DIMENSIONS = {
    "operating_scope", "decision_rights", "business_ownership",
    "capability_pattern", "complexity", "leadership_scope",
    "core_competencies", "supporting_competencies", "exposure_only", "evidence_gaps",
}


def collect_claim_refs(value: object, key: str = "") -> list[str]:
    refs: list[str] = []
    if isinstance(value, dict):
        for child_key, child in value.items():
            if child_key == "supporting_claim_ids" and isinstance(child, list):
                refs.extend(item for item in child if isinstance(item, str))
            else:
                refs.extend(collect_claim_refs(child, child_key))
    elif isinstance(value, list):
        for child in value:
            refs.extend(collect_claim_refs(child, key))
    return refs


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: validate_profile.py PROFILE.json CAREER_EVIDENCE_LEDGER.json", file=sys.stderr)
        return 2
    try:
        profile = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        ledger = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors: list[str] = []
    if not isinstance(profile, dict) or PROFILE_FIELDS - profile.keys():
        errors.append("profile is missing required top-level fields")
    candidate_profile = profile.get("candidate_profile", {}) if isinstance(profile, dict) else {}
    if not isinstance(candidate_profile, dict) or DIMENSIONS - candidate_profile.keys():
        errors.append("candidate_profile is missing required dimensions")
    positioning = profile.get("positioning", {}) if isinstance(profile, dict) else {}
    if not isinstance(positioning, dict) or {"current", "stretch", "unsupported"} - positioning.keys():
        errors.append("positioning must contain current, stretch, and unsupported")
    known = {
        claim.get("claim_id") for claim in ledger.get("claims", [])
        if isinstance(claim, dict) and claim.get("claim_id")
    } if isinstance(ledger, dict) else set()
    unknown = sorted(set(collect_claim_refs(profile)) - known)
    if unknown:
        errors.append(f"profile references unknown claim IDs: {unknown}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {sys.argv[1]} (all claim references resolve)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
