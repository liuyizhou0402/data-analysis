# 🎬 教学动画创意脚本 · Lesson 3C — Development of Organisms
> Edexcel IAL Biology · Topic 3 · 配套 `3C-development-of-organisms.md`
> 每个创意含：🎯 难点 · 🎬 分镜 · 🎙️ 中英旁白 · 🎨 风格与工具

---

## 🎬 创意 1：lac 操纵子——细菌的"按需开关"（The lac Operon）

🎯 **难点**：repressor、operator、promoter、诱导物之间的逻辑关系抽象，学生难记"有/无乳糖时基因开还是关"。动画用"开关电路"演示。

🎬 **分镜**
1. **无乳糖**：repressor 蛋白结合 **operator**，挡住 RNA polymerase →基因**关闭**，不产生分解乳糖的酶。
2. **乳糖出现**：乳糖（allolactose）结合 repressor →repressor 变形脱离 operator。
3. RNA polymerase 得以从 **promoter** 前进，转录结构基因→产生 **β-galactosidase** 等酶。
4. 乳糖被分解殆尽→repressor 重新结合 operator→基因再次关闭（负反馈式节能）。

🎙️ **旁白（约 80s）**
> "Bacteria don't waste energy making enzymes they don't need — watch the **lac operon**. With **no lactose**, a **repressor** protein binds the **operator**, blocking RNA polymerase, so the genes are **off**. When **lactose** appears, it binds the repressor, changing its shape so it lets go of the operator. Now RNA polymerase moves from the **promoter** and transcribes the genes — making the enzymes that digest lactose. Once the lactose is used up, the repressor binds again and switches the genes off. A gene controlled on demand."
> 「细菌不会浪费能量去合成用不上的酶——看 **lac 操纵子**。**没有乳糖**时，**阻遏蛋白**结合在 **operator** 上，挡住 RNA 聚合酶，基因**关闭**。当**乳糖**出现，它结合阻遏蛋白使其变形、脱离 operator；RNA 聚合酶便能从 **promoter** 前进，转录结构基因，合成分解乳糖的酶。乳糖耗尽后，阻遏蛋白再次结合、基因关闭。这就是按需调控的基因。」

🎨 **风格/工具**：电路开关/红绿灯隐喻 + DNA 轨道。**Manim**（DNA 轨道 + 蛋白结合）最佳。

---

## 🎬 创意 2：同一套基因，不同的细胞——差异基因表达（Differential Gene Expression）

🎯 **难点**：学生误以为不同细胞有不同基因。动画展示**同一基因组**在不同细胞中**开启不同基因**而分化。

🎬 **分镜**
1. 一个受精卵的基因组（一排"灯"代表所有基因，全可用）。
2. 分裂出多个细胞；不同细胞中**不同的灯亮起**（不同基因被表达）。
3. 灯亮组合 A→红细胞（表达血红蛋白基因）；组合 B→神经元；组合 C→肌细胞。
4. 强调：DNA 相同，**表达不同**→形态功能不同。

🎙️ **旁白（约 60s）**
> "Every cell in your body carries the **same genes** — so why is a red blood cell so different from a neurone? The answer is **differential gene expression**. From one genome, each cell switches **on** a different set of genes. Turn on the haemoglobin genes and you get a red blood cell; a different combination gives a neurone, or a muscle cell. Same DNA, different genes expressed — that's how one fertilised egg builds a whole, varied body."
> 「你体内每个细胞都带有**相同的基因**——那为什么红细胞和神经元如此不同？答案是**差异基因表达**。同一套基因组中，每种细胞**开启**不同的基因组合：开启血红蛋白基因就成为红细胞，另一种组合则成为神经元或肌细胞。DNA 相同，表达不同——这就是一个受精卵如何造就一个多样化的身体。」

🎨 **风格/工具**：基因组"灯阵"亮灭隐喻最直观。**After Effects**（灯阵）+ 细胞分化树。

---

## 🎬 创意 3：干细胞的"潜能之树"（Stem Cell Potency Tree）

🎯 **难点**：totipotent / pluripotent / multipotent 三级潜能区别，以及来源（胚胎/成体/iPSC）。动画用"分化树"分层展开。

🎬 **分镜**
1. 顶端：受精卵 = **totipotent**（能形成所有细胞 + 胎盘等胚外组织）。
2. 向下：胚胎干细胞 = **pluripotent**（能形成几乎所有体细胞类型，但不含胚外）。
3. 再向下：成体干细胞 = **multipotent**（只能形成有限几种，如造血干细胞→各类血细胞）。
4. 侧支：成体细胞经重编程→ **iPSC**（人工诱导多能干细胞），箭头回到 pluripotent 层。

🎙️ **旁白（约 65s）**
> "Stem cells differ in how many cell types they can become. At the top, a fertilised egg is **totipotent** — it can form every cell type, including the placenta. Embryonic stem cells are **pluripotent** — almost any body cell, but not the placenta. Adult stem cells are **multipotent** — only a limited range, like blood stem cells making all blood cells. And we can reprogram an ordinary adult cell back into a pluripotent state — an **induced pluripotent stem cell**, avoiding the ethics of using embryos."
> 「干细胞按'能变成多少种细胞'分级。顶端的受精卵是**全能的**——可形成所有细胞类型，包括胎盘；胚胎干细胞是**多能的**——几乎任何体细胞，但不含胎盘；成体干细胞是**专能的**——只能形成有限几种，如造血干细胞生成各类血细胞。我们还能把普通成体细胞**重编程**回多能状态——**诱导多能干细胞 iPSC**，从而避开使用胚胎的伦理争议。」

🎨 **风格/工具**：分化树自上而下展开 + 潜能范围用"可达细胞"高亮。**Manim** 或 **After Effects**。

---

## 🎬 创意 4：暹罗猫的"温度画笔"——基因 × 环境（Temperature-sensitive Enzyme）

🎯 **难点**：phenotype = genotype + environment 抽象。用暹罗猫/喜马拉雅兔的"低温处毛色深"作可视化案例。

🎬 **分镜**
1. 一只暹罗猫，身体核心温暖、四肢/耳/尾较冷。
2. 控制色素的酶在**低温**才有活性→冷的部位（耳尾爪）产生深色素。
3. 温暖部位酶失活→浅色。形成经典"重点色"花纹。
4. 对照实验：同基因型小猫养在不同温度→毛色分布不同（环境改变表现型）。

🎙️ **旁白（约 60s）**
> "Phenotype isn't genes alone — it's genes **plus** environment. Meet the Siamese cat. Its pigment-making enzyme only works in the **cold**. The warm core of the body stays pale, but the cooler ears, paws and tail run the enzyme and turn dark — the classic 'points'. Same genotype, raised warmer or cooler, gives a different coat pattern. The environment paints the phenotype the genes make possible."
> 「表现型不只由基因决定，而是基因**加上**环境。看这只暹罗猫：它合成色素的酶只在**低温**下有活性。身体温暖的核心保持浅色，而较冷的耳朵、爪子和尾巴让酶工作、变成深色——经典的'重点色'。同样的基因型，养在更暖或更冷的环境，毛色分布就不同。环境，为基因许可的表现型上色。」

🎨 **风格/工具**：温度热力图叠加猫体 + 毛色随温度变化。**After Effects**（热力图 + 渐变上色）。

---

## 📋 制作优先级 / Production priority

| 创意 | 难度 | 课堂价值 | 建议优先级 |
|---|---|---|---|
| 1 lac 操纵子 | 高 | ★★★★★ | **P1（机制必考）** |
| 2 差异基因表达 | 中 | ★★★★★ | **P1（破误区）** |
| 3 干细胞潜能树 | 中 | ★★★★☆ | P2 |
| 4 温度敏感酶 | 中 | ★★★★☆ | P3 |

> 建议先做 **创意 2（差异基因表达）**——它一举破除"不同细胞有不同基因"的核心误区；再做 **创意 1（lac 操纵子）** 攻克机制大题。
