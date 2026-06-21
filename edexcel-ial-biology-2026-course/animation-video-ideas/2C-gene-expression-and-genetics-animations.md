# 🎬 教学动画创意脚本 · Lesson 2C — Gene Expression and Genetics
> Edexcel IAL Biology · Topic 2 · 配套 `2C-gene-expression-and-genetics.md`
> 每个创意含：🎯 难点 · 🎬 分镜 · 🎙️ 中英旁白 · 🎨 风格与工具

---

## 🎬 创意 1：一个碱基的"多米诺"——突变类型对照（Mutation Types）

🎯 **难点**：substitution 可能"沉默"，而 insertion/deletion 引发 **frameshift** 改变后续全部密码子。动画用"阅读框移位"把连锁后果演出来。

🎬 **分镜**
1. 一段 mRNA 按每 3 个碱基分组朗读，下方对应氨基酸链。
2. **Substitution**：改一个碱基→因密码子简并，氨基酸**不变**（silent）；再换一例→变一个氨基酸（missense）；或变成 stop（nonsense，链截断）。
3. **Insertion/Deletion**：插入/删除 1 个碱基→后面所有分组**整体错位**（frameshift），氨基酸链从该点起全错。
4. 并排展示三种结果对蛋白质功能的影响（正常/局部异常/完全失活）。

🎙️ **旁白（约 70s）**
> "Change a single DNA letter and the effect depends on the change. A **substitution** might be **silent** — the code is degenerate, so the amino acid stays the same; or it changes one amino acid (**missense**), or creates a premature **stop** (**nonsense**). But **insert or delete** a base and every codon downstream shifts — a **frameshift** — rewriting the whole protein from that point. One letter; very different consequences."
> 「改动一个 DNA 字母，后果取决于改动方式。**替换**可能是**沉默的**——密码子简并，氨基酸不变；也可能改一个氨基酸（missense），或提前出现**终止密码子**（nonsense）。但**插入或删除**一个碱基，会使下游所有密码子**整体错位**——**移码突变**，从该点起重写整条蛋白。同样一个字母，后果天差地别。」

🎨 **风格/工具**：阅读框用"滑动取词框"演示错位最直观。**Manim**（取词框 + 文字滑动）。

---

## 🎬 创意 2：孟德尔交叉"棋盘"动起来（Monohybrid Punnett Animation）

🎯 **难点**：学生会套 Punnett 格子，却不理解"配子分离→随机组合→比例"的来由。动画把亲本基因型→配子→随机受精→3:1 全程可视化。

🎬 **分镜**
1. 两个杂合亲本 Tt × Tt，染色体上标 T/t。
2. 减数分裂：每个亲本产生 T 和 t 两种配子（各放进圆圈）。
3. 配子随机两两结合，落入 2×2 棋盘：TT, Tt, Tt, tt 四格逐一点亮。
4. 表现型统计条：高∶矮 = 3∶1；基因型 1∶2∶1。

🎙️ **旁白（约 60s）**
> "Cross two heterozygotes, Tt by Tt. In meiosis each parent makes two kinds of gamete — T and t. At fertilisation they combine **at random**: fill the Punnett square and you get TT, Tt, Tt, tt. Count the phenotypes — **three tall to one short**, a 3 to 1 ratio; genotypes are 1 to 2 to 1. The ratio isn't magic — it's just random combination of gametes."
> 「让两个杂合子 Tt × Tt 杂交。减数分裂中每个亲本产生 T 和 t 两种配子，受精时**随机组合**：填满 Punnett 棋盘得到 TT、Tt、Tt、tt。统计表现型——**高∶矮 = 3∶1**；基因型 1∶2∶1。比例并非魔法，只是配子的随机组合。」

🎨 **风格/工具**：棋盘格逐格点亮 + 比例条同步增长。**PPT Morph**（课堂快速版）或 **After Effects**。

---

## 🎬 创意 3：为什么色盲男生更多？——性连锁（Sex Linkage）

🎯 **难点**：X 连锁隐性中，男性半合子 (X^a Y) 只要一个隐性等位基因即患病；女性需两个。动画用染色体图 + 家系演示。

🎬 **分镜**
1. 展示 XX（女）与 XY（男）；致病等位基因只在 X 上（Y 无对应基因）。
2. 携带者母亲 X^A X^a × 正常父亲 X^A Y 杂交，画出配子与后代四格。
3. 高亮：儿子若得到 X^a 即患病（无 X^A 掩盖）；女儿多为携带者。
4. 统计：儿子 1/2 患病，女儿 0 患病但 1/2 携带。

🎙️ **旁白（约 65s）**
> "Colour blindness is **X-linked recessive** — the gene sits only on the X chromosome; the Y carries no matching allele. So a male, **XY**, has just one copy: a single recessive allele and he's affected — he's **hemizygous**. A female needs **two** recessive alleles. Cross a carrier mother with an unaffected father: half the **sons** are affected, while daughters are unaffected but half are **carriers**. That's why the condition appears far more often in males."
> 「色盲是 **X 连锁隐性**——基因只在 X 染色体上，Y 上没有对应等位基因。男性 **XY** 只有一份拷贝，**半合子**，一个隐性等位基因就发病；女性则需要**两个**。携带者母亲 × 正常父亲：**儿子**有一半患病，女儿不患病但一半是**携带者**。这就是男性发病率更高的原因。」

🎨 **风格/工具**：染色体高亮 + 家系遗传图。**Manim** 或 **After Effects**；可叠加 Ishihara 色盲测试图做 Hook。

---

## 🎬 创意 4：CFTR 通道坏了会怎样？（Cystic Fibrosis）

🎯 **难点**：把"基因突变→膜蛋白缺陷→黏液变稠→多器官症状"连成一条因果链。

🎬 **分镜**
1. 细胞膜上正常 CFTR 通道转运 Cl⁻，水随之外移→黏液稀薄正常流动。
2. 突变 CFTR 折叠错误/缺失→Cl⁻ 无法外流→水分滞留细胞内→**黏液变稠**。
3. 镜头拉远到肺（黏液堵塞、易感染）、胰管（酶无法到肠道）、生殖道。
4. 隐性遗传小结：两个携带者→1/4 患病。

🎙️ **旁白（约 65s）**
> "The CFTR protein is a **chloride channel** in the cell-surface membrane. Normally it pumps Cl⁻ out and water follows, keeping mucus thin and runny. A mutation gives a faulty CFTR — chloride can't leave, water stays in the cell, and the mucus turns **thick and sticky**. In the lungs it blocks airways and traps bacteria; in the pancreas it stops enzymes reaching the gut. It's **recessive** — two carriers have a one-in-four chance of an affected child."
> 「CFTR 是细胞膜上的**氯离子通道**。正常时它把 Cl⁻ 泵出、水随之外移，使黏液稀薄易流。突变后的 CFTR 失灵——氯离子出不去、水滞留细胞内，黏液变得**又稠又黏**：在肺里堵塞气道、滋生细菌，在胰腺阻止酶进入肠道。它是**隐性**遗传——两个携带者有 1/4 概率生出患病孩子。」

🎨 **风格/工具**：通道转运 + 器官切换。**Blender**（通道）+ **After Effects**（器官地图）。

---

## 📋 制作优先级 / Production priority

| 创意 | 难度 | 课堂价值 | 建议优先级 |
|---|---|---|---|
| 1 突变类型/移码 | 中 | ★★★★★ | **P1** |
| 2 Punnett 动画 | 低 | ★★★★☆ | P2 |
| 3 性连锁 | 中 | ★★★★★ | **P1** |
| 4 CFTR | 中 | ★★★★☆ | P3 |

> 建议先做 **创意 1（移码）** 与 **创意 3（性连锁）**——这两点最能解释"为什么"，也是大题失分重灾区。
