# 🎬 教学动画创意脚本 · Lesson 2B — Proteins and DNA
> Edexcel IAL Biology · Topic 2 · 配套 `2B-proteins-and-dna.md`
> 每个创意含：🎯 难点 · 🎬 分镜 · 🎙️ 中英旁白 · 🎨 风格与工具

---

## 🎬 创意 1：诱导契合——酶不是"死锁"（Induced Fit, not Lock-and-Key）

🎯 **难点**：学生背"lock and key"，却误以为活性位点完全刚性。动画展示底物结合时活性位点**微调变形**、降低活化能，区分两种模型。

🎬 **分镜**
1. 左屏"lock-and-key"：刚性钥匙插入刚性锁孔（旧模型）。
2. 右屏"induced fit"：底物靠近，活性位点像手套**慢慢包裹**手指，形状微调。
3. 形成 enzyme-substrate complex，键被拉扯→**activation energy 能垒下降**（能量曲线同步降低）。
4. 产物释放，酶恢复原形，循环再来。

🎙️ **旁白（约 60s）**
> "The old idea was 'lock and key' — a rigid substrate fitting a rigid active site. But enzymes are smarter: as the substrate approaches, the active site **moulds around it** — the **induced-fit** model. This puts strain on the substrate's bonds and **lowers the activation energy**, so the reaction happens far faster. Products leave, the enzyme springs back, ready again."
> 「旧观点是'锁与钥匙'——刚性底物配刚性活性位点。但酶更聪明：底物靠近时，活性位点会**主动包裹**它，这就是**诱导契合**。这会拉扯底物的键、**降低活化能**，反应因此快得多。产物离开后，酶弹回原形，准备下一轮。」

🎨 **风格/工具**：分子手套质感 + 同步能量曲线（双屏）。**Blender** 形变；能量曲线用 **Manim** 叠加。

---

## 🎬 创意 2：半保留复制——Meselson–Stahl 一镜读懂（Semi-conservative Replication）

🎯 **难点**：半保留 vs 全保留 vs 分散式三种假说，以及 ¹⁵N/¹⁴N 密度梯度离心证据，纯文字极难想象。动画把"重链/轻链"用颜色区分，离心管条带位置一目了然。

🎬 **分镜**
1. 双螺旋（两条都是"重"¹⁵N，深色）。helicase 解旋，两条链分开。
2. 每条母链作模板，DNA polymerase 加上"轻"¹⁴N 新链（浅色）→ 两个杂合双链（半深半浅）。
3. 离心管：第 0 代条带在底部（重），第 1 代条带上移到中间（hybrid）。
4. 第 2 代：一半 hybrid、一半全轻→出现两条带（中 + 上）。对照"全保留"预测（底+上）被排除。

🎙️ **旁白（约 80s）**
> "How does DNA copy itself? **Helicase** unwinds the helix; each old strand is a **template**. New nucleotides pair up — A with T, C with G — and DNA polymerase joins them. Each new molecule has **one old strand and one new** — that's **semi-conservative**. Meselson and Stahl proved it: grow cells in heavy nitrogen-15, switch to light nitrogen-14, and spin. Generation one gives a single **hybrid** band — ruling out conservative replication. Generation two gives **two** bands — confirming semi-conservative."
> 「DNA 如何自我复制？**解旋酶**打开双螺旋，每条旧链作**模板**，新核苷酸按 A–T、C–G 配对，DNA 聚合酶连接成链。每个新分子都是**一旧一新**——这就是**半保留复制**。Meselson 与 Stahl 用 ¹⁵N→¹⁴N 离心证明：第一代只出现一条**杂合**带，排除全保留；第二代出现**两条**带，确证半保留。」

🎨 **风格/工具**：深/浅色链对比 + 离心管条带动画。**Manim**（条带位置精确）最适合；DNA 解旋用 **Blender**。

---

## 🎬 创意 3：从基因到蛋白——转录 + 翻译双车间（Transcription & Translation）

🎯 **难点**：转录在核内、翻译在核糖体；模板链、密码子、反密码子、肽键形成多步骤连贯，学生易混。动画做成"两车间流水线"。

🎬 **分镜**
1. 核内：RNA polymerase 沿 template strand 滑动，合成 mRNA（A→U 配对高亮）。
2. mRNA 经核孔离开核 → 进入细胞质核糖体。
3. 核糖体读取 codon；tRNA 带着 anticodon + 氨基酸进站，密码子-反密码子配对。
4. 相邻氨基酸间形成 peptide bond，多肽链延伸；遇 stop codon 释放。
5. 多肽折叠成功能蛋白（呼应一/二/三级结构）。

🎙️ **旁白（约 80s）**
> "A gene is a recipe — but the kitchen is the ribosome, outside the nucleus. First, **transcription**: RNA polymerase reads the **template strand** and builds a complementary **mRNA**, using U instead of T. The mRNA leaves through a nuclear pore. Now **translation**: the ribosome reads the mRNA three bases at a time — each **codon**. A **tRNA** with the matching **anticodon** delivers the right amino acid; **peptide bonds** link them into a growing chain. A **stop codon** ends it, and the polypeptide folds into a working protein."
> 「基因是食谱，而'厨房'是核外的核糖体。先**转录**：RNA 聚合酶读取**模板链**，合成互补的 **mRNA**（用 U 代替 T），mRNA 经核孔离开细胞核。再**翻译**：核糖体每次读三个碱基（一个**密码子**），带有对应**反密码子**的 **tRNA** 送来正确氨基酸，相邻氨基酸间形成**肽键**；遇到**终止密码子**结束，多肽折叠成有功能的蛋白质。」

🎨 **风格/工具**：核内/核外分区配色，tRNA 进站像"快递配送"。**After Effects** 流水线动画；分子细节用 **Blender**。

---

## 🎬 创意 4：竞争性 vs 非竞争性抑制（Enzyme Inhibition）

🎯 **难点**：两类抑制剂结合位点不同、能否被高浓度底物"挤掉"不同。动画并排对照最清楚。

🎬 **分镜**
1. 左屏 competitive：抑制剂长得像底物，抢占 active site；加大底物浓度→把抑制剂"挤走"，反应恢复。
2. 右屏 non-competitive：抑制剂结合 allosteric site（别构位点），活性位点变形→底物再多也无法恢复。
3. 双屏速率-底物浓度曲线对照：competitive 的 Vmax 不变（曲线右移），non-competitive 的 Vmax 下降。

🎙️ **旁白（约 60s）**
> "Inhibitors slow enzymes in two ways. A **competitive** inhibitor mimics the substrate and blocks the active site — but flood the cell with substrate and you out-compete it, so **Vmax is unchanged**. A **non-competitive** inhibitor binds elsewhere, at an **allosteric site**, distorting the active site — more substrate can't rescue it, so **Vmax falls**."
> 「抑制剂以两种方式减慢酶。**竞争性**抑制剂形似底物，抢占活性位点——但底物浓度足够大就能把它'挤走'，所以 **Vmax 不变**。**非竞争性**抑制剂结合在别处的**别构位点**，使活性位点变形——再多底物也救不回，所以 **Vmax 下降**。」

🎨 **风格/工具**：双屏对照 + 同步速率曲线。**Manim**（曲线 + 分子）。

---

## 📋 制作优先级 / Production priority

| 创意 | 难度 | 课堂价值 | 建议优先级 |
|---|---|---|---|
| 1 诱导契合 | 中 | ★★★★☆ | P2 |
| 2 半保留复制 | 高 | ★★★★★ | **P1（证据型必考）** |
| 3 转录+翻译 | 高 | ★★★★★ | **P1** |
| 4 两类抑制 | 中 | ★★★★☆ | P3 |

> 建议先做 **创意 3（转录+翻译）** 与 **创意 2（复制+证据）**——这两条是 2B 的命脉，也是大题高频。
