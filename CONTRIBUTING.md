# Contributing

感谢你愿意改进 Amazon Ops Career Skills。这个项目的首要目标是让职业材料**更可核验，而不是更夸张**；因此，贡献质量与数据边界和代码质量同样重要。

## 可以贡献的内容

- 可复现的 bug 报告和修复；
- Amazon 运营指标定义、证据校验、归因或置信度规则的改进；
- 证据优先的 JD 映射、简历审计、面试追问或开场语工作流；
- 原创、可编辑且不包含第三方受限内容的简历模板；
- 从零构造、明确标记为 `fictional: true` 的示例与回归测试；
- 文档、翻译与无障碍改进。

## 提交前的硬性边界

请勿提交真实或可反推的候选人、雇主或商业数据，包括但不限于：真实简历、联系方式、公司 / 店铺 / 品牌名称、ASIN、SKU、供应商、截图、聊天记录、业务报表、账号、凭证与本地路径。

以下做法也不符合要求：

- 只替换真实姓名或公司名；
- 平移真实日期或微调真实指标；
- 复刻第三方付费模板、课程材料、专有文案或品牌识别；
- 将团队成果写成个人成果，或把 `contributor` 改成 `owner`；
- 用新文案掩盖缺失的证据、指标口径或归因边界。

请先阅读 [PRIVACY.md](PRIVACY.md)。如不确定某项资料能否公开，请不要提交，改用从零构造的最小 synthetic fixture。

## 贡献流程

1. 先阅读相关 `SKILL.md`、`shared/` 规则和现有测试，避免在多个位置复制同一规则。
2. 从当前默认分支创建一个聚焦的改动；一个 PR 尽量只解决一个问题。
3. 为行为变化补充或更新测试。示例 JSON 必须包含 `"fictional": true`。
4. 运行下方验证命令，并在 PR 描述中说明已运行的项目与结果。
5. 清楚说明：问题、改动、影响范围、未解决限制；涉及文案或模板时，说明证据与隐私边界如何保持不变。

## 内容与架构规则

- 以下规则适用于全部七个 Skill。
- `shared/` 是公共规则的唯一来源。不要在单个 Skill 中复制一套独立的指标、归因、因果、置信度或保密规则。
- Career Evidence Ledger v2.0 是唯一 Claim / Evidence 记录；不要新增并行 ledger。
- Profile 必须由证据推导，不能创建证据；定位遵循 Ownership，不按年限自动升级。
- JD Mapping、Resume、Audit、Interview 与 Greeting 不得修改候选人事实。
- 只有证据支持时，才能加强 Ownership、因果或结果表达；不完整信息应标记、软化或移除。
- 任何新模板必须保持原创、可编辑，并兼容现有的 Resume Expression Contract。

## 本地验证

从仓库根目录运行：

```bash
python3 skills/amazon-ops-evidence/scripts/validate_ledger.py \
  examples/fictional-experienced/claim-ledger.json

python3 skills/amazon-ops-profile/scripts/validate_profile.py \
  examples/fictional-experienced/profile.json \
  examples/fictional-experienced/claim-ledger.json

python3 skills/amazon-ops-resume/scripts/build_resume.py \
  examples/fictional-experienced/resume.json /tmp/experienced-resume.html

python3 skills/amazon-ops-interview/scripts/score_session.py \
  examples/fictional-interview/session.json

python3 -m unittest tests/test_alpha5.py
```

同时检查：

- 所有本地 Markdown 链接有效；
- `.codex-plugin/plugin.json` 仍是合法 JSON，版本与发布包一致；
- 打包内容不含 `.DS_Store`、`__MACOSX`、`__pycache__`、`.pyc`、个人文件或凭证；
- 示例和测试中没有行业硬编码、真实身份信息或可识别商业数据。

## Issue 与 Pull Request

Issue 请提供最小、完全虚构的复现步骤与预期 / 实际行为；不要粘贴真实简历、JD、报表或截图。

Pull Request 描述建议包含：

```text
## Problem

## Change

## Validation

## Privacy / evidence review
```

维护者可能要求缩小范围、补充 synthetic fixture、软化无证据表述，或移除任何可能泄露个人和商业信息的材料。

## 行为准则

请保持尊重、建设性与事实导向。讨论候选人材料时，避免人身评价、歧视性表达、羞辱式反馈或将未验证推断当作事实。

提交贡献即表示你有权按 [MIT License](LICENSE) 授权该贡献。
