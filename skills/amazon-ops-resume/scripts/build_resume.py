#!/usr/bin/env python3
"""Render a self-contained editable resume from structured JSON."""

from __future__ import annotations

import html
import json
import sys
from pathlib import Path


REQUIRED = {"mode", "name", "target_role", "contact", "summary", "skills", "sections"}
MODES = {"campus", "experienced"}
TERMINAL_PUNCTUATION = ("。", "；")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def ensure_string_list(value: object, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a list of strings")
    return value


def render_emphasis(text: str, emphasis: list[str]) -> str:
    spans: list[tuple[int, int]] = []
    for phrase in emphasis:
        start = text.find(phrase)
        if start < 0 or text.find(phrase, start + 1) >= 0:
            raise ValueError("each emphasis phrase must occur exactly once in its bullet text")
        end = start + len(phrase)
        if any(start < other_end and end > other_start for other_start, other_end in spans):
            raise ValueError("emphasis phrases must not overlap")
        spans.append((start, end))

    pieces: list[str] = []
    cursor = 0
    for start, end in sorted(spans):
        pieces.append(esc(text[cursor:start]))
        pieces.append(f"<strong>{esc(text[start:end])}</strong>")
        cursor = end
    pieces.append(esc(text[cursor:]))
    return "".join(pieces)


def parse_bullet(value: object) -> tuple[str, list[str]]:
    if isinstance(value, str):
        text, emphasis = value, []
    elif isinstance(value, dict):
        if set(value) - {"text", "emphasis"}:
            raise ValueError("bullet objects only allow text and emphasis fields")
        text = value.get("text")
        emphasis = value.get("emphasis", [])
        if not isinstance(text, str):
            raise ValueError("bullet.text must be a string")
        emphasis = ensure_string_list(emphasis, "bullet.emphasis")
    else:
        raise ValueError("each bullet must be a string or an object")

    if not text.strip():
        raise ValueError("bullet text must not be empty")
    if text.rstrip().endswith(TERMINAL_PUNCTUATION):
        raise ValueError("resume bullets must not end with Chinese full stops or semicolons")
    if len(emphasis) > 2:
        raise ValueError("each bullet may contain at most two emphasis phrases")
    if not all(phrase.strip() for phrase in emphasis):
        raise ValueError("emphasis phrases must be non-empty strings")
    render_emphasis(text, emphasis)
    return text, emphasis


def validate_summary(lines: list[str]) -> None:
    for index, line in enumerate(lines):
        if not line.strip():
            raise ValueError("summary lines must not be empty")
        if line.rstrip().endswith(TERMINAL_PUNCTUATION):
            raise ValueError(
                f"summary line {index + 1} must not end with Chinese full stops or semicolons"
            )


def build_identity(data: dict[str, object], contact: list[str]) -> str:
    has_photo = bool(data.get("photo", False))
    core = (
        '<div class="identity-core">'
        f'<h1 class="candidate-name">{esc(data["name"])}</h1>'
        f'<div class="role-line">{esc(data["target_role"])}</div>'
        '</div>'
    )
    contact_html = ''.join(f'<div class="contact-line">{esc(item)}</div>' for item in contact)
    contacts = f'<div class="contact-stack">{contact_html}</div>'

    if not has_photo:
        return f'<header class="identity identity--plain">{core}{contacts}</header>'

    portrait = (
        '<label class="portrait-picker" contenteditable="false" aria-label="选择或替换证件照">'
        '<span class="portrait-placeholder">证件照</span>'
        '<img class="portrait-image" alt="证件照" hidden>'
        '<input class="portrait-input" type="file" accept="image/*">'
        '</label>'
    )
    left = f'<div class="identity-left">{core}{contacts}</div>'
    return f'<header class="identity identity--photo">{left}{portrait}</header>'


def render(data: dict[str, object], template: str) -> str:
    missing = REQUIRED - data.keys()
    if missing:
        raise ValueError(f"missing required fields: {', '.join(sorted(missing))}")

    mode = data["mode"]
    if mode not in MODES:
        raise ValueError("mode must be 'campus' or 'experienced'")

    contact = ensure_string_list(data["contact"], "contact")
    summary = ensure_string_list(data["summary"], "summary")
    validate_summary(summary)
    skills = ensure_string_list(data["skills"], "skills")
    sections = data["sections"]
    if not isinstance(sections, list):
        raise ValueError("sections must be a list")

    identity = build_identity(data, contact)

    summary_html = (
        '<section class="overview-card" aria-label="个人摘要">'
        + ''.join(f'<p>{esc(line)}</p>' for line in summary)
        + '</section>'
    )

    skills_html = (
        '<section class="resume-block competency-block">'
        '<h2 class="block-title">核心能力</h2>'
        '<div class="competency-list">'
        + ''.join(f'<span class="competency-chip">{esc(skill)}</span>' for skill in skills)
        + '</div></section>'
    )

    rendered_sections: list[str] = []
    for section_index, section in enumerate(sections):
        if not isinstance(section, dict) or not isinstance(section.get("title"), str):
            raise ValueError(f"sections[{section_index}] needs a string title")
        items = section.get("items")
        if not isinstance(items, list):
            raise ValueError(f"sections[{section_index}].items must be a list")

        records: list[str] = []
        for item_index, item in enumerate(items):
            if not isinstance(item, dict) or not isinstance(item.get("heading"), str):
                raise ValueError(f"sections[{section_index}].items[{item_index}] needs heading")
            raw_bullets = item.get("bullets", [])
            if not isinstance(raw_bullets, list):
                raise ValueError("bullets must be a list")
            bullets = [parse_bullet(bullet) for bullet in raw_bullets]
            subheading = item.get("subheading", "")
            if not isinstance(subheading, str):
                raise ValueError("subheading must be a string")

            heading = item["heading"]
            if " · " in heading:
                organization, role = heading.split(" · ", 1)
                heading_html = (
                    f'<span class="record-org">{esc(organization)}</span>'
                    f'<span class="record-role">{esc(role)}</span>'
                )
            else:
                heading_html = f'<span class="record-org">{esc(heading)}</span>'

            meta = esc(item.get("meta", ""))
            record_head = (
                '<div class="record-head">'
                f'<div class="record-heading">{heading_html}</div>'
                f'<div class="record-meta">{meta}</div>'
                '</div>'
            )
            sub = f'<div class="record-note">{esc(subheading)}</div>' if subheading else ''
            bullet_list = (
                '<ul class="achievement-list">'
                + ''.join(
                    f'<li>{render_emphasis(text, emphasis)}</li>' for text, emphasis in bullets
                )
                + '</ul>'
                if bullets else ''
            )
            records.append(f'<article class="record">{record_head}{sub}{bullet_list}</article>')

        rendered_sections.append(
            '<section class="resume-block">'
            f'<h2 class="block-title">{esc(section["title"])}</h2>'
            + ''.join(records)
            + '</section>'
        )

    footer = ''
    if data.get("fictional") is True:
        footer = '<div class="demo-note">全合成演示样例 · 不对应任何真实候选人、公司或商业数据</div>'

    content = identity + summary_html + skills_html + ''.join(rendered_sections) + footer
    return template.replace("{{TITLE}}", esc(data["name"])).replace("{{CONTENT}}", content)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: build_resume.py INPUT.json OUTPUT.html", file=sys.stderr)
        return 2
    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    try:
        data = json.loads(input_path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("input must be a JSON object")
        mode = data.get("mode")
        if mode not in MODES:
            raise ValueError("mode must be 'campus' or 'experienced'")
        template_path = Path(__file__).resolve().parent.parent / "assets" / "templates" / f"{mode}.html"
        output_path.write_text(render(data, template_path.read_text(encoding="utf-8")), encoding="utf-8")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"OK: wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
