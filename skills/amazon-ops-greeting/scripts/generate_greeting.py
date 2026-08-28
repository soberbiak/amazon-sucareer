#!/usr/bin/env python3
"""Amazon Ops Greeting Generator — v0.3.0-alpha.5

Generate platform-specific job-application greeting messages for Amazon
operations roles. Template-based generator for common cases; for nuanced
or personalized greetings, use the SKILL.md guidance with an LLM.

Usage:
    python3 generate_greeting.py input.json [--platform boss] [--tone safe]
    cat input.json | python3 generate_greeting.py -
"""
import argparse
import json
import sys
from typing import Any


def validate_input(data: dict[str, Any]) -> None:
    if not isinstance(data.get("target_role"), str) or not data["target_role"]:
        raise ValueError("target_role is required (string)")
    if not isinstance(data.get("highlights"), list) or not data["highlights"]:
        raise ValueError("highlights is required (non-empty list)")
    for i, h in enumerate(data["highlights"]):
        if not isinstance(h, str) or not h.strip():
            raise ValueError(f"highlights[{i}] must be a non-empty string")


def pick_highlights(highlights: list[str], n: int = 2) -> list[str]:
    """Pick the top N highlights, preferring ones with numbers."""
    scored = []
    for h in highlights:
        has_number = any(c.isdigit() for c in h)
        scored.append((has_number, len(h), h))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [h for _, _, h in scored[:n]]


def generate_boss(data: dict[str, Any], tone: str) -> str:
    name = data.get("candidate_name", "")
    years = data.get("years_exp", "")
    site = data.get("site", "")
    role = data["target_role"]
    company = data.get("company", "贵司")
    highlights = pick_highlights(data["highlights"], 1 if tone == "short" else 2)

    prefix = f"您好！我是{name}，" if name else "您好！"
    exp = f"有{years}年{site}亚马逊运营经验，" if years else ""

    if tone == "aggressive":
        hl_text = "，".join(highlights[:2])
        emoji = "💼"
        action = f"{company}这个岗位我能直接上手，发份简历您看看？{emoji}"
    else:
        hl_text = "，".join(highlights[:1])
        emoji = "📊"
        action = f"对{company}{role}岗位很感兴趣，可否发份简历交流？{emoji}"

    return f"{prefix}{exp}{hl_text}。{action}"


def generate_wechat(data: dict[str, Any], tone: str) -> str:
    name = data.get("candidate_name", "")
    years = data.get("years_exp", "")
    site = data.get("site", "")
    role = data["target_role"]
    referrer = data.get("referrer", "")
    highlights = pick_highlights(data["highlights"], 1)

    intro = f"我是{referrer}推荐的{name}，" if referrer else f"我是{name}，"
    exp = f"有{years}年{site}亚马逊运营经验。" if years else ""
    hl = f"{highlights[0]}。" if highlights else ""
    return f"您好，{intro}{exp}{hl}听说贵司在招{role}，方便的话我发份简历给您看看？"


def generate_email(data: dict[str, Any], tone: str) -> dict[str, str]:
    name = data.get("candidate_name", "")
    years = data.get("years_exp", "")
    site = data.get("site", "")
    role = data["target_role"]
    company = data.get("company", "贵司")
    highlights = pick_highlights(data["highlights"], 3)
    phone = data.get("contact", {}).get("phone", "")
    source = data.get("source", "Boss直聘")

    label = f"{years}年{site}经验" if years else "亚马逊运营"
    subject = f"应聘{role}-{name}-{label}"

    hl_lines = "\n".join(f"- {h}" for h in highlights)
    body = (
        f"HR 您好，\n\n"
        f"我在{source}看到{company}{role}岗位，{name if name else '我'}有{years}年{site}运营经验，特来应聘。\n\n"
        f"核心经历：\n{hl_lines}\n\n"
        f"简历附在附件，期待有机会进一步沟通。\n\n"
        f"{name}\n{phone}"
    )
    return {"subject": subject, "body": body}


def generate(data: dict[str, Any]) -> dict[str, Any]:
    validate_input(data)
    platform = data.get("platform", "boss").lower()
    tone = data.get("tone", "safe").lower()
    versions = data.get("output_versions", [tone])

    results = {}
    for v in versions:
        v = v.lower()
        if platform == "boss":
            results[v] = generate_boss(data, v)
        elif platform == "wechat":
            results[v] = generate_wechat(data, v)
        elif platform == "email":
            results[v] = generate_email(data, v)
        elif platform in ("lagou", "liepin"):
            # 拉勾/猎聘: use boss generator but longer (no emoji)
            results[v] = generate_boss(data, v).replace("📊", "").replace("💼", "")
        else:
            results[v] = generate_boss(data, v)

    return {"platform": platform, "greetings": results}


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Amazon Ops greeting messages")
    parser.add_argument("input", help="JSON input file or - for stdin")
    parser.add_argument("--platform", default=None, help="Override platform")
    parser.add_argument("--tone", default=None, help="Override tone")
    args = parser.parse_args()

    if args.input == "-":
        data = json.load(sys.stdin)
    else:
        with open(args.input, encoding="utf-8") as f:
            data = json.load(f)

    if args.platform:
        data["platform"] = args.platform
    if args.tone:
        data["tone"] = args.tone

    result = generate(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
