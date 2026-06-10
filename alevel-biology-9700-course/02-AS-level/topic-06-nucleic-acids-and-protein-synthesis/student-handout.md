# Topic 6 — 核酸与蛋白质合成 / Nucleic Acids & Protein Synthesis｜学生讲义

## 本主题你要拿下 / What you'll master
- ✅ 描述**核苷酸结构**，对比 DNA 与 RNA（成对作答）
- ✅ 解释 **DNA 双螺旋结构**（碱基配对、氢键、antiparallel 方向、糖磷酸骨架）
- ✅ 描述 **DNA 半保留复制**的机制与 Meselson-Stahl 证据
- ✅ 说出遗传密码**四个特征**，会用密码表读取氨基酸
- ✅ 逐步描述**转录（transcription）**与**翻译（translation）**的过程
- ✅ 区分**基因突变**三类替换及移码突变，分析对蛋白质的影响
- ✅ 用**镰刀型贫血**实例连通"基因→蛋白→功能"全链路

> 🎯 **A\* 提示**：本主题最常考的三类丢分：①转录/翻译步骤写不全或顺序乱；②codon 和 anticodon 混淆；③突变类型分析不精确（尤其 frameshift 的碱基数判断）。把这三点拿稳，本主题基本满分。

---

## 1. 核苷酸结构 / Nucleotide Structure

### 1.1 核苷酸三组成
每个核苷酸（nucleotide）含三部分：

```
磷酸基团（phosphate group）
        |
   五碳糖（pentose sugar）
        |
  含氮碱基（nitrogenous base）
```

相邻核苷酸之间通过**磷酸二酯键（phosphodiester bond）**相连，形成核酸链。

### 1.2 DNA vs RNA — 完整对比表（必背成对）
| 特征 | DNA | RNA |
|---|---|---|
| 五碳糖 | **脱氧核糖（deoxyribose）**（2'位缺—OH） | **核糖（ribose）**（2'位有—OH） |
| 碱基种类 | A、T、G、C | A、**U（尿嘧啶）**、G、C（U 替代 T） |
| 链数 | **双链（double-stranded）** | **单链（single-stranded）** |
| 螺旋 | **双螺旋（double helix）** | 无（mRNA/tRNA/rRNA 各有不同折叠） |
| 功能 | **储存遗传信息** | **传递、转录、翻译遗传信息** |
| 位置（真核） | 主要在细胞核（少量在线粒体/叶绿体） | 细胞核及细胞质 |

> 🎯 **Compare 题必须成对**：
> *"DNA contains deoxyribose **whereas** RNA contains ribose; DNA contains thymine **whereas** RNA contains uracil…"*

### 1.3 ATP — 核苷酸衍生物（简述）
ATP（三磷酸腺苷）由**腺嘌呤（adenine）+ 核糖 + 三个磷酸基团**构成，是核苷酸的一种衍生物。水解末端磷酸键释放能量（见 Topic 12）。

---

## 2. DNA 双螺旋结构 / DNA Double Helix

### 2.1 结构要点（Watson-Crick 模型，1953）
1. **两条多核苷酸链（polynucleotide strands）**，**反向平行（antiparallel）**：
   - 一条链从 **5'→3'**，另一条从 **3'→5'**（方向相反）。
2. **糖-磷酸骨架（sugar-phosphate backbone）** 在外侧，碱基朝向内侧。
3. 两链之间通过**碱基互补配对（complementary base pairing）**，由**氢键（hydrogen bonds）**维系：
   - **A—T**：**2 个氢键**（双氢键，相对较弱）
   - **G—C**：**3 个氢键**（三氢键，更稳定）
4. 整体扭曲成**双螺旋（double helix）**形状。

### 2.2 碱基互补规则（速记）

| DNA 一链 | → 互补链碱基 |
|---|---|
| A | T |
| T | A |
| G | C |
| C | G |

> ⚠️ 注意：转录时模板链上的 A 对应 mRNA 的 **U**（不是 T）——见第4节。

### 2.3 Chargaff 规律（支持 DNA 结构）
由 Erwin Chargaff 测量大量生物体 DNA 碱基比例后发现：**[A]=[T]，[G]=[C]**。这正是双链互补配对的化学证据。

---

## 3. DNA 复制 / DNA Replication

### 3.1 半保留复制（Semi-conservative Replication）
> 定义：每个子代 DNA 分子含**一条亲代旧链 + 一条新合成互补链**。

**复制步骤（按序）**：

```
① 解旋酶（helicase）沿 DNA 移动
   → 断开碱基对间的氢键 → 双链解开，形成两条模板链

② 游离脱氧核苷酸（free DNA nucleotides）
   按碱基互补配对原则与模板链配对

③ DNA 聚合酶（DNA polymerase）
   → 以模板为基础，将游离核苷酸连接成新链
   → 只能沿 5'→3' 方向合成（形成磷酸二酯键）

④ 结果：两个子代 DNA 分子，每个含
   一条旧链（来自亲代）+ 一条新链
```

> ⚠️ **关键细节**：
> - Helicase 断的是**氢键**（碱基对间），不是磷酸二酯键。
> - DNA 聚合酶方向：**5'→3'**（只能从 5' 端向 3' 端延伸新链）。

### 3.2 Meselson-Stahl 实验（证明半保留）
| 实验步骤 | 离心结果 | 说明 |
|---|---|---|
| 1. 在 **¹⁵N** 培养基中多代培养细菌 | 全重 DNA（¹⁵N-¹⁵N） | 所有 DNA 为全重链 |
| 2. 转移到 **¹⁴N** 培养基，复制**一代** | **中间密度** 单一条带（¹⁵N-¹⁴N） | 每个分子各含一条旧¹⁵N + 一条新¹⁴N → 只有半保留能解释 |
| 3. 继续在 ¹⁴N 中复制**第二代** | **一半中间密度 + 一半轻密度**（¹⁴N-¹⁴N） | 旧链继续作模板；新分子全为¹⁴N-¹⁴N |

> 🎯 关键逻辑：若是**全保留复制**（conservative），第一代应有"全重"和"全轻"两条带——实验结果**只有一条中间带**，排除了全保留。

---

## 4. 遗传密码与转录 / Genetic Code & Transcription

### 4.1 遗传密码（Genetic Code）四特征（必背）

| 特征 | 英文 | 含义 |
|---|---|---|
| **三联体（triplet）** | Triplet code | 每 **3 个碱基** = 1 个密码子（codon），编码 1 个氨基酸 |
| **不重叠（non-overlapping）** | Non-overlapping | 相邻密码子不共用碱基，阅读框逐段读取 |
| **简并（degenerate）** | Degenerate | 多数氨基酸由**多个密码子**编码（如亮氨酸 Leu 有 6 个密码子） |
| **（近乎）通用** | (Nearly) Universal | 几乎所有生物使用同一套密码子——支持共同祖先（common ancestry） |

> ⚠️ 注意方向："简并"是**多→一**（多个密码子 → 同一氨基酸），不是"一密码子 → 多氨基酸"。

### 4.2 如何使用遗传密码表
读表三步：**第一碱基（行）→ 第二碱基（列）→ 第三碱基（细分）**

示例：密码子 **GAG**
- G（第一列）→ A（第二列）→ G（第三列）→ **Glutamic acid（Glu，谷氨酸）**

### 4.3 转录（Transcription）步骤

```
场所：细胞核（nucleus）

① RNA 聚合酶（RNA polymerase）结合 DNA 特定区域
   → 解开局部 DNA 双链

② 以 DNA template strand（模板链）为模板（3'→5' 读取）

③ 游离核糖核苷酸（free ribonucleotides）按互补配对：
   A→U, T→A, G→C, C→G（注意：RNA 用 U，不用 T）

④ RNA pol 将核苷酸连接成 mRNA（5'→3' 方向合成）

⑤ mRNA 从 DNA 上释放 → 通过核孔（nuclear pore）进入细胞质
```

| | 模板链 DNA（template strand） | mRNA（转录产物） |
|---|---|---|
| 碱基对应 | A | U |
| | T | A |
| | G | C |
| | C | G |

> ⚠️ **Coding strand vs Template strand**：
> - **Template strand**（模板链）：RNA pol 读取它合成 mRNA。
> - **Coding strand**（编码链/有义链）：序列与 mRNA 相同（只是 T 换成 U）。

---

## 5. 翻译 / Translation

### 5.1 翻译步骤（完整版）

```
场所：细胞质中的核糖体（ribosome, 80S）

① mRNA 从核孔出来，与核糖体小亚基结合
② 核糖体识别起始密码子 AUG（编码 Met/蛋氨酸）
③ 携带氨基酸的 tRNA 进入核糖体：
     其 anticodon（反密码子）与 mRNA codon（密码子）互补配对
④ 核糖体催化相邻两氨基酸之间形成肽键（peptide bond）
     （缩合反应，脱水）
⑤ 核糖体沿 mRNA 5'→3' 方向移动（移动一个密码子距离）
⑥ 重复步骤③④⑤，多肽链逐渐延伸
⑦ 当核糖体到达终止密码子（UAA/UAG/UGA）：
     无对应 tRNA → 释放因子结合 → 多肽链释放
⑧ 核糖体两亚基解离，可被重新利用
```

### 5.2 关键分子对比
| 分子 | 位置 | 作用 |
|---|---|---|
| **mRNA** | 模板，细胞质 | 携带密码子（codon），信息载体 |
| **tRNA** | 细胞质 | 含 **anticodon**（反密码子），携带并搬运特定氨基酸 |
| **rRNA + 蛋白质** | 核糖体（80S） | 组成核糖体，催化肽键形成 |

> 🎯 **Codon（密码子）在 mRNA 上；Anticodon（反密码子）在 tRNA 上**——两者反向互补配对。

### 5.3 转录 vs 翻译 完整对比（必背）
| | 转录（Transcription） | 翻译（Translation） |
|---|---|---|
| **场所** | 细胞核 | 细胞质（核糖体） |
| **模板** | DNA template strand | mRNA |
| **酶** | RNA polymerase | 核糖体（含 rRNA）；氨酰-tRNA 合成酶 |
| **原料** | 核糖核苷酸（A/U/G/C） | 氨基酸（由 tRNA 搬运） |
| **产物** | mRNA | 多肽（polypeptide） |
| **方向** | mRNA 合成 5'→3' | 核糖体移动 5'→3' |
| **碱基配对** | A-U, T-A, G-C, C-G | codon-anticodon 互补配对 |

---

## 6. 基因突变 / Gene Mutation

### 6.1 突变类型汇总（必背表）

| 突变类型 | 碱基变化 | 对密码子 | 对氨基酸 | 对蛋白质 |
|---|---|---|---|---|
| **Silent（沉默）** | 单碱基替换 | 变了，但仍编码**同一氨基酸** | **不变** | **不变**（因密码子简并） |
| **Missense（错义）** | 单碱基替换 | 变了，编码**不同氨基酸** | **改变** | 结构/功能可能改变 |
| **Nonsense（无义）** | 单碱基替换 | 变成**终止密码子** | 翻译**提前终止** | 多肽缩短，功能多丧失 |
| **Frameshift 移码（插入/缺失）** | 插入或缺失**非3的倍数**个碱基 | **所有后续密码子全改变** | 突变点之后**全部改变** | 极严重，常无功能 |

> ⚠️ **移码计数关键**：
> - 插入/缺失 **1个、2个、4个、5个…**（不是3的倍数）→ **移码（frameshift）**
> - 插入/缺失 **3个、6个…**（3的倍数）→ **不移码**，只增删整数个氨基酸，其余序列不变

### 6.2 实例：镰刀型贫血 / Sickle Cell Anaemia（synoptic 热点）

**突变链：**
```
正常 HbA：DNA 碱基  →  CTC  →  mRNA codon GAG  →  氨基酸 Glu（谷氨酸）
               ↓ 单碱基替换（A→T）
突变 HbS：DNA 碱基  →  CAC  →  mRNA codon GUG  →  氨基酸 Val（缬氨酸）
```

**后果链：**
1. **Glu（谷氨酸，亲水极性）→ Val（缬氨酸，疏水非极性）**
2. HbS 分子在低氧时互相聚合（非极性 Val 暴露在外，形成纤维）
3. 红细胞变镰刀形（sickle-shaped）→ 易破裂（溶血）/ 堵塞毛细血管
4. 导致**贫血、疼痛危象（pain crises）、器官损伤**

> 🎯 这是 missense 突变（错义替换）导致蛋白功能改变的经典 synoptic 实例，常与 Topic 2（蛋白质结构）、Topic 16（遗传）、Topic 17（选择）连题。

---

## 必背定义 / Must-know definitions（英文背诵）

| 概念 | 英文定义（考试级措辞） | 中文 |
|---|---|---|
| **Semi-conservative replication** | *Each new DNA molecule consists of one original (parental) strand and one newly synthesised strand.* | 半保留复制：每个新 DNA 分子含一条旧链一条新链 |
| **Transcription** | *The process by which the base sequence of a gene (DNA template strand) is used to produce a complementary mRNA molecule, catalysed by RNA polymerase.* | 以 DNA 为模板合成 mRNA 的过程 |
| **Translation** | *The process by which the base sequence of an mRNA molecule is decoded at the ribosome to produce a specific sequence of amino acids (polypeptide).* | 在核糖体以 mRNA 为模板合成多肽的过程 |
| **Codon** | *A sequence of three (adjacent, non-overlapping) bases on an mRNA molecule that codes for one amino acid (or a start/stop signal).* | 密码子：mRNA 上编码一个氨基酸的三联体碱基 |
| **Anticodon** | *A sequence of three bases on a tRNA molecule that is complementary to a codon on mRNA.* | 反密码子：tRNA 上与密码子互补配对的三联体 |
| **Gene mutation** | *A change in the sequence of bases in a DNA molecule.* | 基因突变：DNA 碱基序列的改变 |
| **Frameshift mutation** | *A mutation caused by insertion or deletion of a number of bases not divisible by three, causing all codons downstream to be read differently.* | 移码突变：插入/缺失非3整数倍碱基，导致后续所有密码子改变 |
| **Degenerate (genetic code)** | *Most amino acids are coded for by more than one codon.* | 简并性：大多数氨基酸由多于一个密码子编码 |

---

## 速记图表 / Quick-reference diagrams

### 核苷酸速记比较
```
DNA 核苷酸                    RNA 核苷酸
磷酸—脱氧核糖—碱基(A/T/G/C)   磷酸—核糖—碱基(A/U/G/C)
           ↑                              ↑
      2'位无—OH                      2'位有—OH
```

### 中心法则速记
```
DNA ──[复制 Replication: DNA pol]──→ DNA
  ↓
[转录 Transcription: RNA pol, 核内]
  ↓
mRNA ──[翻译 Translation: 核糖体, 细胞质]──→ 多肽 Polypeptide
```

### 突变严重程度（由轻到重）
```
Silent（沉默）< Missense（错义）< Nonsense（无义）< Frameshift（移码）
```

---

## A* 拓展 / Stretch to A*

### synoptic 连接
- **Topic 2（蛋白质结构）**：镰刀型贫血的 Glu→Val 改变了蛋白质的三级结构（影响侧链相互作用）→ 功能改变。
- **Topic 1（细胞器）**：转录在**细胞核**，翻译在**核糖体（细胞质）**——mRNA 通过核孔运出。
- **Topic 5（细胞周期）**：S 期（合成期）= DNA 复制期——helicase/DNA pol 大量活跃。
- **Topic 16（遗传）**：基因突变是遗传变异的来源之一；突变可传代。
- **Topic 17（进化）**：HbS 在疟疾流行区有**杂合子优势（heterozygote advantage）**——这是 missense 突变在进化中"有利"的典范。
- **Topic 19（基因技术）**：PCR、基因工程都依赖 DNA 互补配对原则和 DNA 聚合酶——与本主题直接相连。

### 多聚核糖体 Polysome（延伸了解）
多个核糖体同时附在同一 mRNA 上滑动，可同时合成多条相同多肽——**提高翻译效率**。在分泌蛋白旺盛的细胞（如胰腺细胞）中尤为明显。

### RNA 三种类型
| 类型 | 全名 | 功能 |
|---|---|---|
| mRNA | messenger RNA | 携带遗传信息（密码子），由转录产生 |
| tRNA | transfer RNA | 携带并运输氨基酸，含 anticodon |
| rRNA | ribosomal RNA | 组成核糖体（结合蛋白质），催化肽键 |

---

## 自测清单 / Self-check
- [ ] 我能画出核苷酸结构图，标出三组成，并说出 DNA/RNA 的差异
- [ ] 我能默写 DNA 双链结构的要点：antiparallel、糖磷酸骨架在外、A-T 两氢键、G-C 三氢键
- [ ] 我能按步骤描述 DNA 半保留复制（helicase→DNA pol→5'→3'→一旧一新）
- [ ] 我能用英文说出 Meselson-Stahl 实验结果并解释其证明了什么
- [ ] 我能说出遗传密码四特征（triplet/non-overlapping/degenerate/universal）
- [ ] 我能逐步描述转录（场所/RNA pol/模板链/产物 mRNA）
- [ ] 我能逐步描述翻译（mRNA/核糖体/tRNA+anticodon/肽键/终止）
- [ ] 我能区分 silent/missense/nonsense/frameshift 突变并分析其对蛋白影响
- [ ] 我能用镰刀型贫血实例串联"DNA碱基→密码子→氨基酸→蛋白功能"全链路
