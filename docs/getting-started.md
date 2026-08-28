# Getting Started

这是一份面向第一次使用 `amazon-ops-career-skills` 的端到端示例。目标不是让你机械地跑完 7 个 Skill，而是展示：**旧简历 + 业务资料 + 目标 JD，如何一步步变成可核验的求职材料。**

> 示例中的人物、公司、数据和业务情境均为 synthetic，不代表真实候选人。

## 0. 你手里可能有什么

常见输入包括：

```text
旧简历.docx / pdf
年度或季度业务复盘
项目复盘
广告报表或指标汇总
库存 / 利润 / 销售分析
周报、月报、述职材料
目标 JD
你自己补充的职责范围和决策背景
```

不要求一次性把所有材料整理得很干净。第一步的目的就是把这些东西变成结构化证据。

---

## 1. Evidence：先建立事实底座

调用：

```text
$amazon-ops-evidence
```

示例提示词：

```text
我准备更新亚马逊运营简历。

我会上传：
1. 一份旧简历
2. 两份业务复盘
3. 一份年度指标汇总

请先不要直接写简历。
请把材料整理成 Career Evidence Ledger v2.0，并完成 Experience Reframing。

要求：
- 区分事实、推导和不确定信息
- 区分团队成果与我的个人 Ownership
- 所有强指标保留口径和来源
- 不要补写我没有提供的职责、预算、管理范围或业务结果
- 有冲突的数据单独列出，不要自动替我选择
```

你应该得到的不是“漂亮文案”，而是一组可追溯 claims，例如：

```text
C-001 负责某业务单元的日常经营分析
C-002 识别广告效率问题并调整投放结构
C-003 某指标从 A 变为 B，但结果同时受季节性和价格策略影响
...
```

### 什么时候不要跳过这一步

如果你的原始材料里同时存在：

- 多个版本的指标；
- 团队成果和个人贡献混在一起；
- “负责 / 主导 / 协助”边界不清；
- 业务复盘比旧简历详细很多；
- 你准备使用比较强的量化结果；

就应该先跑 Evidence。

---

## 2. Profile：判断你真正能投到哪里

调用：

```text
$amazon-ops-profile
```

示例提示词：

```text
基于刚才的 Career Evidence Ledger，给我做职业定位。

请输出：
- current positioning
- stretch positioning
- unsupported positioning
- 六维能力画像
- 当前最大的证据缺口

不要只根据“工作 X 年”判断资深程度。
优先看 operating unit、decision rights、KPI ownership、time horizon、mechanisms 和 cross-functional influence。
```

这一步的作用是回答：

```text
我现在“能证明”的层级是什么？
我稍微 stretch 可以投什么？
哪些岗位标题看起来接近，但实际责任已经超过我的证据？
```

Profile 不应该创造新经历。如果 Profile 中出现 Ledger 没有的事实，应回到 Evidence 修正。

---

## 3. JD：把招聘要求翻译成证据需求

当你找到目标职位后调用：

```text
$amazon-ops-jd
```

示例提示词：

```text
这是目标公司的亚马逊高级运营 JD。

请不要只提取关键词。
请拆成：
- 业务范围
- 核心能力
- Ownership / 决策权
- KPI / 结果要求
- 跨团队协作要求
- 隐含 seniority 信号

然后映射到我的 Career Evidence Ledger：
- covered
- partially covered
- unsupported

最后告诉我：这份 JD 对我属于 current、stretch 还是 unsupported。
```

这里的输出应该形成 JD Evidence Map，而不是简单的“匹配度 85%”。

---

## 4. Resume：先写可证明的简历，再做版式

调用：

```text
$amazon-ops-resume
```

示例提示词：

```text
基于我的 Profile、JD Evidence Map 和 Career Evidence Ledger，生成社招简历。

要求：
- 面向亚马逊高级运营岗位
- 只使用 verified 或我已经确认可以使用的 derivable claims
- 每条 bullet 只表达一个主结论
- 优先体现 operating mechanism、判断逻辑和业务结果
- 不要把团队结果冒领成个人结果
- 不要为了显得 senior 加“统筹、主导、全面负责”等无证据词
- 同时输出可编辑 HTML
- 默认无照片版
```

### 如果你要带照片

明确说：

```text
请生成带照片版 HTML，保留证件照上传区域。
```

如果没有明确要求，默认使用无照片版。

### HTML 预览怎么理解

HTML 是编辑和检查层，不是独立的排版引擎。

当前模板使用：

```text
连续编辑画布
+ A4 预览参考线
+ 浏览器 Print Preview 负责最终真实分页
```

因此：

- 页面中的 A4 线用来预估哪里可能换页；
- 最终 PDF 以浏览器打印预览为准；
- 长工作经历允许自然跨页；
- 不应该为了“网页里正好一页”强行删掉有价值内容。

### 导出 PDF

```text
Open HTML
→ 检查内容 / 字号 / 照片
→ Print
→ 检查 A4 Print Preview
→ Save as PDF
```

---

## 5. Audit：生成以后再攻击自己的简历

调用：

```text
$amazon-ops-resume-audit
```

示例提示词：

```text
审计刚才这份简历。

请逐条检查：
- 证据是否足够
- 指标口径是否容易误读
- 因果是不是说得过满
- 团队成果有没有被写成个人成果
- Ownership 是否超出事实
- 是否存在面试一追问就讲不清的 bullet

给出：keep / soften / remove / recover。
```

`recover` 的意思不是“帮我编完整”，而是指出：**如果想保留这条强声明，还缺什么真实证据。**

---

## 6. Interview：围绕强声明追问，而不是背 STAR

调用：

```text
$amazon-ops-interview
```

示例提示词：

```text
基于最终简历和 Career Evidence Ledger，模拟面试。

不要只问泛泛的 STAR。
优先攻击我简历里最强的 5 条声明：
- 指标口径
- baseline
- 我的具体动作
- 为什么这么判断
- 还有哪些备选方案
- 团队和我的贡献怎么拆
- 结果受哪些外部因素影响
- 如果重做会改什么

每轮回答后给我评分，并指出还需要补什么证据。
```

这样准备出来的面试材料会和简历共用同一套事实，而不是另起一套“故事”。

---

## 7. Greeting：最后再压缩成第一句话

调用：

```text
$amazon-ops-greeting
```

示例：

```text
目标岗位：亚马逊高级运营
平台：Boss直聘

请基于最终简历中已经确认的 2-3 个最强亮点，生成：
- 稳妥版
- 进取版

要求控制在手机端容易读完的长度，不要新增指标。
```

Greeting 是求职材料链路的最外层，不应该反过来创造新的职业事实。

---

## 常见捷径

### 我已经有一份不错的简历，只想改表达

可以从 `$amazon-ops-resume-audit` 开始。如果 Audit 发现很多声明无法追溯，再回到 Evidence。

### 我没有目标 JD，只想先整理自己

先跑：

```text
Evidence → Profile → Resume
```

等有具体 JD 后再：

```text
JD → Resume rewrite / Audit
```

### 我只有目标 JD，还没有整理业务材料

不要直接让 Resume 按 JD “补齐”。正确顺序仍然是：

```text
Raw Materials → Evidence → Profile → JD → Resume
```

### 我只是想写一句 Boss 打招呼语

可以直接用 Greeting，但所有亮点仍必须来自你真实提供的内容。若要更稳定，先提供最终简历。

---

## 使用原则

记住四句话即可：

1. **Evidence first**：先知道什么能证明，再决定怎么写
2. **Positioning follows ownership**：定位跟实际责任走，不跟工龄自动走
3. **Resume is a compressed evidence surface**：简历是证据的压缩表达，不是证据本身
4. **Interview must survive claim-level probing**：简历里越强的声明，越应该能经得起逐层追问

如果你不确定下一步该用哪个 Skill，可以直接描述你目前手里有什么材料，以及你现在要解决什么求职问题，再选择最短入口。
