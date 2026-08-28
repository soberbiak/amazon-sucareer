#!/usr/bin/env python3
"""Regression checks for the repository contract."""

from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContract(unittest.TestCase):
    def test_manifest_and_frozen_structure(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertEqual(manifest["name"], "amazon-ops-career-skills")
        version = manifest["version"]
        self.assertRegex(version, r"^0\.3\.0-alpha\.\d+$")
        self.assertIn(f"当前版本：`{version}`", readme)
        expected_skills = {
            "amazon-ops-evidence", "amazon-ops-profile", "amazon-ops-jd",
            "amazon-ops-resume", "amazon-ops-resume-audit", "amazon-ops-interview",
            "amazon-ops-greeting",
        }
        actual_skills = {path.name for path in (ROOT / "skills").iterdir() if path.is_dir()}
        self.assertEqual(actual_skills, expected_skills)
        expected_shared = {
            "experience-reframing-framework.md", "competency-framework.md",
            "evidence-schema.md", "amazon-metrics-dictionary.md", "attribution-rules.md",
            "causality-rules.md", "confidence-rules.md", "confidentiality-rules.md",
        }
        self.assertEqual({path.name for path in (ROOT / "shared").iterdir()}, expected_shared)

    def test_resume_preview_layout_contract(self) -> None:
        for mode in ("experienced", "campus"):
            template = (ROOT / f"skills/amazon-ops-resume/assets/templates/{mode}.html").read_text(encoding="utf-8")
            self.assertIn("A4 预览线", template)
            self.assertNotIn("min-height: 297mm", template)
            self.assertIn(".record { margin:", template)
            self.assertIn("break-inside: auto", template)
            self.assertIn("--resume-size", template)
            self.assertIn("--resume-color", template)
            self.assertIn("amazon_ops_resume_", template)
            self.assertIn("amazon-ops-resume-clean-v1", template)
            self.assertIn("payload.version === VERSION", template)
            self.assertIn(".page-guide-layer", template)
            self.assertIn("refreshGuides", template)
            self.assertIn("@media print", template)
            self.assertIn("identity--plain", template)
            self.assertIn("identity--photo", template)
            self.assertIn("portrait-picker", template)

    def test_clean_frontend_uses_new_surface_contract(self) -> None:
        forbidden_tokens = [
            "class=\"toolbar\"",
            "class=\"sheet\"",
            "profile-photo-slot",
            "header-grid",
            "header-plain",
            "summary-block",
            "section-title",
            "company-name",
            "save-status",
            "page-mode-select",
        ]
        required_tokens = [
            "editor-panel",
            "resume-canvas",
            "identity--plain",
            "identity--photo",
            "overview-card",
            "record-head",
            "achievement-list",
            "page-guide-layer",
        ]
        for mode in ("experienced", "campus"):
            template = (ROOT / f"skills/amazon-ops-resume/assets/templates/{mode}.html").read_text(encoding="utf-8")
            for token in forbidden_tokens:
                self.assertNotIn(token, template)
            for token in required_tokens:
                self.assertIn(token, template)

    def test_user_onboarding_contract(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        getting_started = (ROOT / "docs/getting-started.md").read_text(encoding="utf-8")
        self.assertIn("## 7 个 Skill", readme)
        for skill in (
            "amazon-ops-evidence", "amazon-ops-profile", "amazon-ops-jd",
            "amazon-ops-resume", "amazon-ops-resume-audit",
            "amazon-ops-interview", "amazon-ops-greeting",
        ):
            self.assertIn(skill, readme)
        self.assertIn("## 最快开始", readme)
        self.assertIn("## 安装 / 加载", readme)
        self.assertIn("## 简历 HTML 怎么用", readme)
        self.assertIn("A4 预览线只是编辑时的分页参考", readme)
        self.assertIn("docs/getting-started.md", readme)
        self.assertIn("Evidence：先建立事实底座", getting_started)
        self.assertIn("Greeting：最后再压缩成第一句话", getting_started)
        self.assertIn("Evidence first", getting_started)

    def test_github_community_docs_are_present_and_current(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        contributing = (ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")
        acknowledgements = (ROOT / "ACKNOWLEDGEMENTS.md").read_text(encoding="utf-8")
        license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
        upstream_license = (ROOT / "licenses/ASu-skills-MIT.txt").read_text(encoding="utf-8")
        self.assertIn("ACKNOWLEDGEMENTS.md", readme)
        self.assertIn("CONTRIBUTING.md", readme)
        self.assertIn("MIT License", readme)
        self.assertIn("七个 Skill", contributing)
        self.assertIn("fictional: true", contributing)
        self.assertIn("独立开源项目", acknowledgements)
        self.assertIn("Permission is hereby granted, free of charge", license_text)
        self.assertIn("Copyright (c) 2026 Hisn00w", upstream_license)
        for path in (
            ROOT / "skills/amazon-ops-jd/SKILL.md",
            ROOT / "skills/amazon-ops-resume-audit/SKILL.md",
            ROOT / "skills/amazon-ops-greeting/SKILL.md",
        ):
            self.assertNotIn("alpha.4", path.read_text(encoding="utf-8"), path.as_posix())

    def test_reframing_model_and_profile_invariants(self) -> None:
        reframing = (ROOT / "shared/experience-reframing-framework.md").read_text(encoding="utf-8")
        order = [
            "RAW EXPERIENCE", "TASK", "OPERATING MECHANISM", "CAPABILITY",
            "BUSINESS VALUE", "EVIDENCE & OWNERSHIP", "ROLE-ALIGNED EXPRESSION",
        ]
        offsets = [reframing.index(item) for item in order]
        self.assertEqual(offsets, sorted(offsets))
        self.assertIn("Level A — Task Expression", reframing)
        self.assertIn("Level B — Capability Expression", reframing)
        self.assertIn("Level C — Business Ownership Expression", reframing)
        profile_skill = (ROOT / "skills/amazon-ops-profile/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Profile is derived from evidence. Profile never creates evidence.", profile_skill)
        self.assertIn("Positioning follows ownership, not tenure.", profile_skill)

    def test_single_ledger_v2_and_claim_references(self) -> None:
        ledger = json.loads((ROOT / "examples/fictional-experienced/claim-ledger.json").read_text(encoding="utf-8"))
        profile = json.loads((ROOT / "examples/fictional-experienced/profile.json").read_text(encoding="utf-8"))
        self.assertEqual(ledger["schema_version"], "2.0")
        required = {"operating_mechanisms", "competencies", "business_values"}
        for claim in ledger["claims"]:
            self.assertTrue(required.issubset(claim))
        known = {claim["claim_id"] for claim in ledger["claims"]}
        serialized = json.dumps(profile, ensure_ascii=False)
        referenced = set(re.findall(r'"(C-\d{3})"', serialized))
        self.assertTrue(referenced)
        self.assertTrue(referenced.issubset(known))

    def test_repository_examples_are_explicitly_synthetic(self) -> None:
        for path in (ROOT / "examples").glob("**/*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertIs(data.get("fictional"), True, path.as_posix())

        example_text = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (ROOT / "examples").glob("**/*")
            if path.is_file()
        )
        for hardcoded_category in ("汽配", "汽车配件", "家居收纳", "桌面收纳", "厨房配件"):
            self.assertNotIn(hardcoded_category, example_text)

    def test_resume_expression_contract_is_routed_and_concise(self) -> None:
        skill = (ROOT / "skills/amazon-ops-resume/SKILL.md").read_text(encoding="utf-8")
        qa = (ROOT / "skills/amazon-ops-resume/references/resume-qa.md").read_text(encoding="utf-8")
        contract_path = ROOT / "skills/amazon-ops-resume/references/resume-expression-contract.md"
        contract = contract_path.read_text(encoding="utf-8")
        self.assertIn("resume-expression-contract.md", skill)
        self.assertIn("Resume Expression Contract", qa)
        self.assertIn("Two-layer rule", contract)
        self.assertIn("Metric result clause", contract)
        self.assertIn("percentage points", contract)
        self.assertIn("do not relabel it as 环比", contract)
        self.assertIn("Role summary and priority order", contract)
        self.assertIn("Visual emphasis", contract)
        self.assertIn("Terminal punctuation", contract)

    def test_summary_lines_omit_terminal_punctuation(self) -> None:
        script_path = ROOT / "skills/amazon-ops-resume/scripts/build_resume.py"
        spec = importlib.util.spec_from_file_location("resume_builder", script_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        with self.assertRaises(ValueError):
            module.validate_summary(["正常的一句话。"])
        with self.assertRaises(ValueError):
            module.validate_summary(["正常的一句话；"])
        module.validate_summary(["正常的一句话", "第二句也没有标点"])

        for path in (ROOT / "examples").glob("**/resume.json"):
            resume = json.loads(path.read_text(encoding="utf-8"))
            for line in resume["summary"]:
                self.assertFalse(line.endswith(("。", "；")), path.as_posix())

    def test_emphasis_is_safe_and_example_bullets_follow_the_contract(self) -> None:
        script_path = ROOT / "skills/amazon-ops-resume/scripts/build_resume.py"
        spec = importlib.util.spec_from_file_location("resume_builder", script_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        rendered = module.render_emphasis("主题：结果<验证>", ["主题", "结果<验证>"])
        self.assertEqual(rendered, "<strong>主题</strong>：<strong>结果&lt;验证&gt;</strong>")
        with self.assertRaises(ValueError):
            module.parse_bullet({"text": "结论。", "emphasis": []})
        with self.assertRaises(ValueError):
            module.parse_bullet({"text": "同一词同一词", "emphasis": ["同一词"]})

        for path in (ROOT / "examples").glob("**/resume.json"):
            resume = json.loads(path.read_text(encoding="utf-8"))
            for section in resume["sections"]:
                for item in section["items"]:
                    for bullet in item.get("bullets", []):
                        text, emphasis = module.parse_bullet(bullet)
                        self.assertFalse(text.endswith(("。", "；")), path.as_posix())
                        self.assertLessEqual(len(emphasis), 2, path.as_posix())
                        for phrase in emphasis:
                            self.assertEqual(text.count(phrase), 1, path.as_posix())


if __name__ == "__main__":
    unittest.main()
