# Resume Expression Contract

Use this contract when drafting or auditing candidate-facing resume text. It controls expression density; it does not create evidence or replace the Career Evidence Ledger.

## Two-layer rule

Keep the resume concise and the evidence record complete.

- **Resume layer:** show the action, relevant operating mechanism or scope, and the most decision-useful result.
- **Evidence layer:** retain metric definitions, exact periods, attribution windows, dependencies, confidence, confidentiality, and ownership boundaries.

Do not force every ledger field into the resume sentence. Move detail to the ledger or interview preparation unless omitting it would make the claim misleading.

## Bullet contract

Each bullet should communicate one main claim:

```text
optional short topic + supported action + relevant scope or mechanism + result or concrete output
```

- A short topic such as `广告结构：` or `库存治理：` may improve scanning, but is optional.
- Prefer concrete actions, numbers, and conventional Amazon terms when they carry information.
- Do not force a number, abbreviation, or keyword into every bullet.
- Keep explanatory detail in the same bullet only when it clarifies method, scope, or result.
- Avoid a separate slogan followed by a paragraph that repeats the slogan.

Campus bullets should emphasize method, artifacts, validation, and honest project labels. Experienced-hire bullets should emphasize operating mechanisms, decision scope, defensible business results, and actual ownership.

## Role summary and priority order

The one-line description beneath a company or project is an operating-scope statement, not an evidence disclaimer. It should say what the candidate mainly owns or contributes to:

```text
responsibility verb + operating unit or scope + core operating rhythm + related module
```

Keep authorization limits, dependency caveats, and exclusions in the ledger, relevant bullet, or interview material unless they are required to keep the summary truthful.

Within a work entry, order bullets by recruiter value:

1. the primary operating mechanism or work rhythm;
2. the clearest defensible result or business output;
3. the collaboration, diagnostic, or review method that shows how the work is sustained.

## Visual emphasis

Use bold as a scanning aid, not as decoration. A bullet may have zero, one, or two bold anchors:

- the short topic label when it improves scanning;
- one result, scope, count, or concrete deliverable that carries the most decision value.

Do not bold an entire bullet, a list of tools, unsupported ownership language, or more than two fragments. Evidence still governs what may be emphasized.

For structured HTML inputs, use an approved `emphasis` array on a bullet object instead of raw HTML or free-form Markdown:

```json
{
  "text": "广告分析：完成搜索词分层并提出否词建议；ACoS由34.0%降至29.5%，下降4.5个百分点",
  "emphasis": ["广告分析", "ACoS由34.0%降至29.5%，下降4.5个百分点"]
}
```

Each phrase must appear exactly once in `text`; the renderer escapes all text before applying `<strong>`.

## Terminal punctuation

Resume bullets and personal summary lines are scanable entries rather than prose paragraphs. By default, omit terminal `。` and `；` from work, internship, and project bullets, as well as from every personal summary line. Keep punctuation inside a line when it is needed to separate clauses or preserve meaning.

## Personal summary

Keep the personal summary concise: one to two short lines that state the candidate's core operating scope and one differentiating strength or method. Do not repeat details that belong in bullets, skills, or the role summary. Each line is a scanable fragment, not a full prose sentence.

## Metric result clause

The default candidate-facing form is:

```text
metric baseline → result + absolute change + only the context needed to interpret it
```

For rate metrics, express absolute change in percentage points. Use relative percentage change only when it adds real meaning and label it explicitly.

- Add month-over-month, quarter-over-quarter, or year-over-year only when the baseline truly uses that comparison and seasonality or trend makes it useful.
- Call an intervention comparison `优化前后` or state the actual windows; do not relabel it as 环比.
- Do not stack both sequential and year-over-year comparisons unless each answers a different material question.
- Add a guardrail metric when the headline result could otherwise be produced by an obvious trade-off, but only when the evidence supports it.
- Preserve the metric's business scope, denominator, period, attribution window, and candidate responsibility in the ledger.

Synthetic illustration:

```text
广告结构：基于搜索词分层与否词规则优化 SP 流量结构，推动成熟产品组合 ACoS 由 34.0% 降至 29.5%，下降 4.5 个百分点（优化前后各四周、同口径）
```

If the candidate contributed but did not own execution, preserve that boundary:

```text
广告分析：完成 SP 搜索词分层并提出否词建议，配合广告负责人落地；相关产品组合 ACoS 由 34.0% 降至 29.5%（优化前后各四周、同口径）
```

## Readability gate

Before accepting a bullet, check:

1. Can a recruiter identify the main claim in one pass?
2. Does every number have an understandable comparison or scope?
3. Are Amazon terms conventional, necessary, and used correctly?
4. Does the wording preserve actual ownership and causality?
5. Can supporting detail move to the ledger or interview notes without changing the truth?

If the answer to the last question is yes, shorten the resume bullet.
