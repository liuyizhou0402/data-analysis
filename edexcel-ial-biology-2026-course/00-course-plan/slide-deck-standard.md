# Slide-Deck Standard — 每节课 PPT 制作规范（≥100 页）
# The contract every lesson deck (1A–8C) must follow

> 目的：保证 **24 节课**的 PPT 在**深度、结构、考试导向**上完全统一，且每份 **≥100 张幻灯片**且无注水。
> 格式：**Marp Markdown**（`marp: true`），用 `---` 分页，可在 VS Code + Marp 插件一键导出 PPTX/PDF。

---

## 0. 技术规范 / Technical

- 文件头（front-matter）固定：
```markdown
---
marp: true
theme: default
paginate: true
backgroundColor: '#ffffff'
header: 'Edexcel IAL Biology · Topic X · Lesson XA'
---
```
- 每张幻灯片之间用 `---` 分隔。**一张幻灯片只讲一个要点**（避免一页塞满）。
- 封面用 `<!-- _class: lead -->`。
- 数学/化学式用 `$...$`（行内）或 `$$...$$`（独立），如 $6CO_2 + 6H_2O \rightarrow C_6H_{12}O_6 + 6O_2$。
- 图无法插入图片时，用 **ASCII 示意图 / 表格 / 文字分镜**清楚描述"这里应画什么图"（标注 `🖼️ 图示：...`），方便老师后期配图。
- 双语原则：**讲解、记忆法、思路用中文；术语、定义、答题模板、mark points 用英文**（考试全英文作答）。

---

## 1. 强制结构与页数下限 / Mandatory structure & minimum slide budget

> 下面是**最低**配置，合计 **≥100 页**。内容多的 sub-unit 自然超过，不得低于。

### A. 开篇模块 Opening（6 页）
1. 封面（中英标题 + Unit 归属 + 本课 sub-unit 代号）
2. 本课在 Edexcel IAL 考纲中的位置（属于哪个 Unit、考哪张卷、占比）
3. Learning Objectives 学习目标（逐条列出对应 spec statements，英文动词开头）
4. 本课路线图 Lesson Roadmap（列出本课覆盖的所有教材小节）
5. 先修知识快速回顾 Prior Knowledge（衔接前一课）
6. 课前小测 Starter Quiz（3–4 题，下一页给答案）

### B. 内容模块 Content（主体，按教材每个小节展开）
> **每个教材小节 ≥14 页**。一个 sub-unit 通常 5–8 个小节 → 70–112 页。
> 小节不足 5 个的课（如 4B、8C），把每节深度提到 ≥20 页以补足总量。

每个教材小节内部固定含：
- (1) **小节分隔页** Section divider（中英小节标题 + 本节要点预告）
- (2) **真实情境导入** Hook（1 页，生活/医学/科研实例引入）
- (3) **核心概念页 × 4–6**（每页一个概念，含 🖼️ 图示描述、关键机制、为什么）
- (4) **必背术语表** Key Terms（1–2 页表格：English term | 中文 | 一句话定义）
- (5) **A\* 深化页** Going Deeper（1 页，超纲衔接/常考高阶点）
- (6) **易错点 & 命令词** Misconceptions & Command Words（1 页：学生常错 + 本节高频命令词如何作答）
- (7) **当堂检测** Check Your Understanding（1–2 页，2–4 题 Edexcel 风格）+ **答案与评分点页**（1 页）
- (8) **本节小结** Mini-Summary（1 页，✅ 要点清单）

### C. 实验与数学技能模块 Skills（6–8 页）
- Core Practical / 关键实验：步骤、变量、风险评估、结果处理（2–3 页）
- Maths Skills 数学技能：本课相关计算的方法 + 例题 + 解答（2–3 页）
- 实验数据分析示范（描述—引用数据—解释 三步法）（1–2 页）

### D. 综合与考试冲刺模块 Exam Prep（10–14 页）
- Synoptic Links 跨主题联系（1–2 页）
- "Thinking Bigger" 拓展应用（如教材有该模块，1–2 页 AO3 训练）
- Exam Practice — 选择题 MCQ ×5（1–2 页）+ 答案解析（1 页）
- Exam Practice — 结构题/简答 ×2–3（含分值，2–3 页）+ **官方风格 mark scheme**（2 页）
- A\* 答题技巧总结（1 页）
- 高频失分点 Top Pitfalls（1 页）

### E. 收尾模块 Wrap-up（5 页）
- 知识结构图 Knowledge Organiser（1 页，本课全图）
- 必背清单 Must-Know Checklist（1 页）
- 自我评估 Self-Assessment（1 页，"我能…"清单 + 信心打分）
- 课后作业 Homework（1 页）
- 下节课预告 + 本课金句（1 页）

> **合计下限：6 + 70 + 6 + 10 + 5 = 97**，加上各小节富余，**稳定 ≥100 页**。

---

## 2. 每张内容页的写法 / How each content slide reads

- 标题用"问题式"或"要点式"（如 `## 为什么磷脂会自发形成双分子层？`）。
- 正文 3–6 个要点，**每个要点是一个可考的知识点**，不写废话。
- 凡机制必答"**所以呢**"（因果链写全：A → 因为 B → 导致 C）。
- 关键英文术语**加粗**，首次出现给中文。
- 适当用表格做对比（结构 vs 功能、A vs B）。

## 3. 练习题与答案规范 / Practice & mark schemes

- 题目标注**分值** `[3]` 与**命令词**。
- 答案给**逐条 mark points**（每分一个要点），并说明"为什么这样写才得分"。
- MCQ 给出正确选项 + **为什么其他选项错**（干扰项分析）。
- 至少出现一次：data-response（给数据/图，要求 describe + explain）。

## 4. 动画创意脚本规范 / Animation companion file

每节课另出一个 `animation-video-ideas/XA-....md`，含 **3–5 个**动画/短视频创意，每个写明：
- 🎯 针对的难点概念（为什么动画比静态图更有效）
- 🎬 分镜（3–6 个镜头，逐镜描述画面）
- 🎙️ 旁白脚本（中英，30–90 秒）
- 🎨 视觉风格建议 + 可用工具（如 Manim / PPT Morph / After Effects / 剪映）

---

## 5. 质量红线 / Hard rules

1. **页数 ≥100**（用 `grep -c '^---$'` 自查分隔符数量应 ≥101）。
2. 覆盖该 sub-unit 教材**全部小节**，不漏知识点。
3. 每个小节都必须有**当堂练习 + 答案**。
4. 术语、定义、答题模板必须**英文**且对标 Edexcel mark scheme 语言。
5. 不复制任何出版社版权文字；依据**公开考纲与学科知识原创**。
