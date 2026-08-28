---
name: amazon-ops-greeting
description: Generate platform-specific job-application greeting messages (Boss直聘 / 拉勾 / 微信 / 邮件) for Amazon operations roles. Produces concise, evidence-grounded openers that request a resume exchange or further conversation; does not invent candidate facts or metrics.
---

# Amazon Ops Greeting — v0.3.0-alpha.5

Generate Chinese greeting / opener messages for job-application platforms, tailored to Amazon operations roles (运营 / 高级运营 / 运营主管 / 运营助理).

## When to use

- User asks to "写个打招呼语" / "Boss直聘开场白" / "给HR发消息" / "求职打招呼"
- User has a target role and wants a first-contact message
- User wants multiple versions (稳妥版 / 进取版 / 简短版)

## Input required

Minimum:
- `target_role`: 目标岗位（如"亚马逊运营"）
- `candidate_name`: 姓名（可留空，输出时用"您好"开头）
- `highlights`: 1-3 条核心亮点（经历/成果/技能），必须是真实可核验的

Optional:
- `platform`: boss / lagou / wechat / email（默认 boss）
- `company`: 目标公司名称（用于个性化）
- `jd_summary`: 岗位描述摘要（用于匹配关键词）
- `tone`: safe / aggressive / short（默认 safe）
- `years_exp`: 工作年限

## Output

For each requested version, output a single paragraph of 60-120 字，结构为：

1. **问候 + 身份**：您好，我是 XXX / 您好，我有 X 年亚马逊运营经验
2. **核心匹配**：1-2 句与目标岗位最相关的经历或成果（带数据）
3. **求职意向 + 行动请求**：对贵司 XX 岗位很感兴趣，可否发份简历交流 / 期待进一步沟通

## Platform tone

| 平台 | 字数 | 语气 | 特点 |
|------|------|------|------|
| Boss直聘 | 60-100字 | 直接、自信 | 第一句抓眼球，可带 emoji，结尾请求"发简历" |
| 拉勾 | 80-120字 | 专业、完整 | 可稍详细，突出技能匹配 |
| 微信 | 50-80字 | 礼貌、简洁 | 适合已有联系人介绍，说明来意 |
| 邮件 | 100-150字 | 正式、完整 | 含主题行，正文分段，附件简历说明 |

## Constraints

- **不编造数据**：所有成果数据必须来自用户提供的 highlights；信息不足时标记【待补】
- **不夸大**：不用"精通""专家"等无法验证的词；有数据用数据，没数据用定性描述
- **区分团队/个人**：团队成果要说明个人角色，不把团队成果冒领为个人
- **平台适配**：Boss直聘不要太长（HR 手机阅读），邮件要有主题行
- **结尾必须有行动请求**：不要只自我介绍，要明确请求下一步（发简历/加微信/约电话）

## Typical usage

```
$amazon-ops-greeting

目标岗位：亚马逊高级运营
平台：Boss直聘
核心亮点：
- 3年北美站运营经验，负责年销2000万产品组合
- ACoS从32.4%降至28.1%，高龄库存占比下降8.5个百分点
- 熟悉广告投放、库存治理、Listing优化全链路

请生成稳妥版和进取版两个打招呼语。
```

## Handoff

- 生成的打招呼语可直接复制使用
- 如需基于完整简历生成，先调用 `$amazon-ops-resume` 或读取已有简历
- 如需岗位匹配分析，先调用 `$amazon-ops-jd`
