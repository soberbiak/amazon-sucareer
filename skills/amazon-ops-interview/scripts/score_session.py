#!/usr/bin/env python3
"""Aggregate a structured interview coaching session."""

from __future__ import annotations

import json
import sys
from pathlib import Path


DIMENSIONS = (
    "specificity",
    "evidence",
    "ownership",
    "mechanism",
    "trade_offs",
    "reflection",
    "communication",
)
GAP_TYPES = {
    "evidence_gap",
    "mechanism_gap",
    "ownership_gap",
    "metric_gap",
    "communication_gap",
    "claim_risk",
}


def band(total: int) -> str:
    if total >= 24:
        return "strong"
    if total >= 18:
        return "repair"
    if total >= 11:
        return "high_risk"
    return "remove_or_rewrite"


def score(data: object) -> tuple[list[dict[str, object]], list[str]]:
    errors: list[str] = []
    results: list[dict[str, object]] = []
    if not isinstance(data, dict) or not isinstance(data.get("claims"), list):
        return results, ["top level must contain a claims list"]

    for index, claim in enumerate(data["claims"]):
        label = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{label} must be an object")
            continue
        claim_id = claim.get("claim_id")
        scores = claim.get("scores")
        gaps = claim.get("gaps", [])
        if not isinstance(claim_id, str) or not claim_id:
            errors.append(f"{label}.claim_id must be a non-empty string")
            continue
        if not isinstance(scores, dict):
            errors.append(f"{label}.scores must be an object")
            continue
        missing = set(DIMENSIONS) - scores.keys()
        if missing:
            errors.append(f"{label}.scores missing: {', '.join(sorted(missing))}")
            continue
        invalid = [name for name in DIMENSIONS if not isinstance(scores[name], int) or not 0 <= scores[name] <= 4]
        if invalid:
            errors.append(f"{label} has scores outside integer range 0..4: {invalid}")
            continue
        if not isinstance(gaps, list) or any(gap not in GAP_TYPES for gap in gaps):
            errors.append(f"{label}.gaps contains an invalid gap type")
            continue
        total = sum(scores[name] for name in DIMENSIONS)
        zero_gate = scores["evidence"] == 0 or scores["ownership"] == 0
        results.append({
            "claim_id": claim_id,
            "total": total,
            "band": band(total),
            "zero_gate": zero_gate,
            "gaps": gaps,
        })
    return results, errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: score_session.py SESSION.json", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    results, errors = score(data)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    for item in results:
        gate = " evidence/ownership-zero" if item["zero_gate"] else ""
        gaps = ",".join(item["gaps"]) or "none"
        print(f"{item['claim_id']}: {item['total']}/28 {item['band']}{gate}; gaps={gaps}")
    print(f"OK: scored {len(results)} claims")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
