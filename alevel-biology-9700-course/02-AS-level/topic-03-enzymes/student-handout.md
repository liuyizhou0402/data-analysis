# Topic 3 — 酶 / Enzymes｜学生讲义

## 本主题你要拿下 / What you'll master
- ✅ **定义**酶并解释其降低活化能的作用方式（英文精准措辞）
- ✅ **对比** lock-and-key 与 induced-fit 模型（成对，说清 active site 的区别）
- ✅ **描述并解释**四个影响因素（温度/pH/底物浓度/酶浓度）对反应速率的影响——图像+文字双通道
- ✅ **成对比较**竞争性与非竞争性抑制剂（结合位点、Vmax/Km 变化、能否被底物浓度克服）
- ✅ **解释** Vmax 与 Km 的含义，并读图判断
- ✅ **解释**固定化酶的原理与优点，及其工业应用
- ✅ 描述酶活性实验的设计要点（catalase / amylase 实验）

> 🎯 **A\* 提示**：本主题最常考、最易丢分的是 ①induced-fit 的措辞（"active site **changes shape** to fit substrate"）；②图像解释题必须"描述趋势 + 引用数据 + 讲原因"三步全做；③竞争性抑制**Vmax 不变**但非竞争性**Vmax 降低**——这两个组合是高频陷阱。

---

## 1. 酶的本质 / What Are Enzymes?

### 1.1 定义（必背英文）

> **Enzyme（酶）**：A **biological catalyst** that **speeds up a chemical reaction** without being used up (consumed), by **lowering the activation energy** of the reaction.
>
> 中文理解：酶是生物体内的化学催化剂，通过降低反应所需的活化能来加速反应，自身不被消耗、可反复利用。

**关键特征**：
- 化学本质：**球状蛋白（globular protein）**
- 具有**专一性（specificity）**：一种酶通常只能催化一种或一类化学反应
- 不改变反应的**平衡点**（反应物与产物的能量差不变）
- 反应后酶**恢复原状**，可被再次利用

### 1.2 活化能（Activation Energy）

**活化能**：反应物需要吸收的最小能量，才能开始发生化学反应（好比要"翻过一座山"才能到达产物那侧）。

```
能量
 │      ← 活化能（无酶）
 │     ╱╲
 │    ╱  ╲   ← 活化能（有酶，更低）
 │   ╱    ╲─╲
 │  ╱       ╲──
 │─╱
 └──────────────────→ 反应进程
   反应物       产物
```

> 酶**不改变反应物和产物的能量**（起点和终点不变），只**降低中间的活化能山峰**，使更多分子在同一温度下就能"翻过"这座山，从而加快反应速率。

---

## 2. 作用机制 / Mechanism of Enzyme Action

### 2.1 活性位点（Active Site）

- **Active site（活性位点）**：酶分子上一个特定的**三维立体区域**，由少数几个氨基酸残基构成。
- 形状由蛋白质的**三级结构**决定（主要靠氢键、疏水相互作用、二硫键维持）。
- 底物进入活性位点，形成**enzyme-substrate complex（酶-底物复合物）**。

### 2.2 两个模型对比（重点，成对记忆）

| | Lock-and-key 锁钥模型 | Induced-fit 诱导契合模型 |
|---|---|---|
| 活性位点形状 | **固定不变**（rigid） | **随底物结合而改变**（flexible, changes shape） |
| 底物与活性位点关系 | **原本就互补**，好比"钥匙原本就合锁" | 底物与活性位点**初步接触**后，活性位点**弯曲/调整形状**以更紧密契合底物 |
| ESC 形成 | 直接形成 | 活性位点形状改变后形成更稳定的 ESC |
| 被接受程度 | 较早提出的模型 | **目前更被接受**的模型（更好解释实验数据） |
| 关键英文措辞 | "active site is complementary to substrate / rigid" | "**active site changes shape** to fit the substrate / moulds around substrate" |

> ⚠️ 高频易错：很多同学写 induced-fit 时忘写"active site **changes shape**"——这是这个模型的**核心**，不写不得分。

### 2.3 ESC 形成完整流程

```
底物靠近活性位点
    ↓
（Induced-fit）活性位点形状改变以契合底物
    ↓
enzyme-substrate complex (ESC) 形成
    ↓
活化能降低 → 底物化学键断裂/形成
    ↓
enzyme-product complex → 产物脱离
    ↓
酶的活性位点恢复原状，游离，可再利用
```

---

## 3. 影响酶活性的因素 / Factors Affecting Enzyme Activity

> 核心思维：所有因素都通过**影响底物与酶碰撞的频率**或**改变活性位点形状**来影响速率。

### 3.1 温度 / Temperature

**机制理解（分两段）**：

**① 最适温度以下：温度↑ → 速率↑**
- 温度升高 → 分子**动能（kinetic energy）**增大
- 底物与酶**碰撞频率↑**，更多分子具有足够能量形成 ESC
- **有效碰撞↑** → 反应速率↑

**② 超过最适温度：速率骤降 → 变性**
- 过多热能破坏维持蛋白质三级结构的**氢键（hydrogen bonds）**及其他弱键
- 活性位点**形状改变（permanently changes shape）**→ 底物不再能与活性位点结合
- → **变性（denaturation）**，且为**不可逆**反应（不可逆，区别于低温！）

```
反应速率
    │       ●
    │     ●   ●
    │   ●       ●
    │  ●           ●
    │●               ●
    └──────────────────→ 温度 °C
              ↑
         最适温度（optimum）
```

> ⚠️ 低温 ≠ 变性：低温只是**降低碰撞频率**（活性位点形状不变），**升温可恢复活性**；高温变性是**不可逆的（irreversible）**。

### 3.2 pH

**机制**：
- pH 影响活性位点附近氨基酸残基的**电荷状态**
- 偏离最适 pH → **离子键（ionic bonds）和氢键（hydrogen bonds）断裂**
- → active site 形状改变 → 底物不能结合 → 速率下降
- 极端 pH → 完全**变性（denaturation）**

> 不同酶有不同的最适 pH：胃蛋白酶（pepsin）最适 pH ≈ 2（胃酸环境）；胰蛋白酶（trypsin）最适 pH ≈ 8（小肠碱性）。

### 3.3 底物浓度 / Substrate Concentration

```
反应速率 (Vmax)─────────────────────────
    │            ●────────────●
    │          ●
    │        ●
    │      ●
    │    ●
    │  ●
    └──────────────────────────→ 底物浓度 [S]
                         ↑
                    酶饱和（全部活性位点被占）
```

| 阶段 | 解释 |
|---|---|
| 上升阶段（斜率段） | [S]↑ → 更多底物与活性位点碰撞 → 有效碰撞频率↑ → 速率↑ |
| 平台（Plateau / Vmax） | 所有酶的活性位点都被占满（**saturated**）→ 酶成为**限制因素（limiting factor）** → 底物再增多也无法再提速 |

> 🎯 平台原因的标准答法：*"All enzyme active sites are occupied / saturated, so the enzyme is the limiting factor."*

### 3.4 酶浓度 / Enzyme Concentration

- 底物充足时，酶浓度↑ → 可用活性位点↑ → 速率**线性**↑
- 若底物不足，速率受底物限制，不随酶浓度继续上升

---

## 4. 必背定义 / Must-know Definitions（英文背诵）

| 概念 | 英文定义（贴官方措辞） | 中文 |
|---|---|---|
| Enzyme | *A biological catalyst that speeds up a chemical reaction without being used up, by lowering the activation energy.* | 酶 |
| Activation energy | *The minimum amount of energy required for a reaction to occur / the energy needed to start a chemical reaction.* | 活化能 |
| Active site | *The region of an enzyme molecule, with a specific three-dimensional shape, to which a substrate molecule binds (forming an enzyme-substrate complex).* | 活性位点 |
| Enzyme-substrate complex | *The complex formed when a substrate molecule binds to the active site of an enzyme.* | 酶-底物复合物 |
| Induced-fit model | *A model of enzyme action in which the active site changes shape to fit the substrate as it binds.* | 诱导契合模型 |
| Denaturation | *A permanent change in the three-dimensional structure (tertiary structure) of a protein, caused by the disruption of bonds (hydrogen bonds, ionic bonds, etc.) maintaining its shape.* | 变性 |
| Competitive inhibitor | *A molecule with a similar shape to the substrate that binds to the active site of the enzyme, preventing the substrate from binding.* | 竞争性抑制剂 |
| Non-competitive inhibitor | *A molecule that binds to an allosteric site on an enzyme (not the active site), causing the shape of the active site to change so the substrate can no longer bind or react.* | 非竞争性抑制剂 |
| Vmax | *The maximum rate of reaction of an enzyme-catalysed reaction, achieved when all active sites are saturated with substrate.* | 最大反应速率 |
| Km | *The substrate concentration at which the rate of reaction is half the maximum rate (½Vmax); an indicator of the enzyme's affinity for its substrate.* | 米氏常数 |
| Immobilised enzyme | *An enzyme that is attached to or enclosed within an inert, insoluble material, allowing it to be reused and easily separated from the product.* | 固定化酶 |

---

## 5. 抑制剂 / Inhibitors

### 5.1 竞争性抑制（Competitive Inhibition）

- **抑制剂结构与底物类似**（structural analogue），与底物**争夺 active site**
- 占据活性位点后底物无法结合 → 速率降低
- **可被底物浓度克服**：增大底物浓度 → 底物"抢回"活性位点 → 高 [S] 时速率恢复至接近正常 Vmax
- 效果：**Vmax 不变（unchanged）；表观 Km 升高（increased）**

### 5.2 非竞争性抑制（Non-competitive Inhibition）

- 结合酶的**别构位点（allosteric site，非活性位点）**
- 导致 active site 形状改变 → 底物不能正常结合/反应
- **不可被底物浓度克服**（inhibitor 不在活性位点，增加底物无效）
- 效果：**Vmax 降低（decreased）；Km 不变（unchanged）**

### 5.3 图像对比（速率-底物浓度图）

```
速率
 │         无抑制剂 ─────── Vmax (原始)
 │        ●─────────
 │      ●●          竞争性 ── Vmax (相同)
 │    ●  ●───────────
 │   ●  ●        非竞争性 ─── Vmax (降低)
 │  ● ●  ●──────────
 │ ●●
 └──────────────────────→ [S]
   ↑
  Km      Km'(竞争性)
         （右移，表观Km↑）
```

| | 无抑制剂 | 竞争性 | 非竞争性 |
|---|---|---|---|
| Vmax | 正常 | **不变** | **降低** |
| Km（表观）| 正常 | **升高（右移）** | **不变** |
| 高 [S] 时速率 | 正常 | 趋近正常 Vmax | 仍低于正常 Vmax |

### 5.4 Vmax 与 Km 的含义

- **Vmax**：所有活性位点饱和时的最大反应速率；与酶浓度成正比（酶越多，Vmax 越高）。
- **Km**：达到 **½Vmax** 时的底物浓度。
  - Km **越小** → 酶对底物**亲和力越高**（只需少量底物就能达到半最大速率）
  - Km **越大** → 亲和力越低
  - Km 是酶的固有属性（与酶浓度无关）

---

## 6. 固定化酶 / Immobilised Enzymes

### 6.1 什么是固定化酶

将酶**固定或包埋**于惰性、不溶性的载体材料上，底物溶液可流过酶而不带走它。

**常见方式**：
| 方式 | 说明 |
|---|---|
| **包埋（Entrapment）** | 酶包裹在凝胶珠（如海藻酸钙珠）内，底物可渗入 |
| **共价结合（Covalent bonding）** | 酶通过共价键结合到载体表面 |
| **物理吸附（Adsorption）** | 酶吸附在不溶性载体表面 |

### 6.2 优点（与游离酶对比）

| 优点 | 原因 |
|---|---|
| **可重复使用（Reusable）** | 酶固定在载体上，不随产物溶液流走（not lost with product） |
| **产物纯净（Pure product）** | 产物中不含酶，无需后续除酶步骤 |
| **稳定性更高（More stable）** | 对温度和 pH 的耐受范围更宽 |
| **连续批次生产（Continuous production）** | 底物可以连续流过固定化酶柱 |

### 6.3 应用实例：乳糖酶（Lactase）

```
生牛奶（含乳糖 lactose）
        ↓
 流过固定化乳糖酶柱
        ↓
乳糖水解 → 葡萄糖 + 半乳糖
        ↓
无乳糖牛奶（lactose-free milk）
（乳糖不耐受 lactose intolerance 患者可饮用）
```

> 乳糖酶固定化后，牛奶流过不带走酶 → 酶可反复使用 → 降低生产成本。

---

## 7. 实验技能 / Practical Skills

### 7.1 过氧化氢酶实验（Catalase + H₂O₂）

**原理**：过氧化氢酶（catalase）催化 H₂O₂ → H₂O + O₂↑，通过测量**产生 O₂ 的体积**来衡量反应速率。

**实验设计要点**：
- **自变量（Independent variable）**：所研究的因素（如温度/pH/[S]）
- **因变量（Dependent variable）**：单位时间内产生的 O₂ 体积（cm³/min）
- **控制变量（Control variables）**：
  - H₂O₂ 的体积和浓度
  - 酶提取液的体积和浓度
  - 反应时间
  - 容器大小/密封程度
- **测量速率**：收集 O₂（量气管/注射器），记录一定时间内体积；速率 = 体积 ÷ 时间

### 7.2 淀粉酶实验（Amylase + 淀粉 + 碘液）

**原理**：淀粉（amylase 的底物）被水解后碘液不变蓝；用碘液变色程度（比色法）或变蓝消失时间来衡量反应速率。

**方法**：
- 每隔固定时间取样，滴于点滴板上加碘液
- **蓝黑色消失**的时间 → 反应终点 → 速率 = 1 / 时间
- 或用**分光光度计（colorimetry）**在特定波长测吸光度变化（更精确）

> ⚠️ 实验控制变量务必具体（"same concentration of starch solution"）而非笼统写"其他条件不变"。

---

## 8. A* 拓展 / Stretch to A*（Synoptic 联系）

- **联系 Topic 2（蛋白质结构）**：酶是球状蛋白，活性位点由三级结构中的特定氨基酸决定；变性是三级结构破坏。理解这一点，酶的所有性质都能从蛋白质结构推导。
- **联系 Topic 10（抗生素）**：青霉素（penicillin）是**竞争性抑制**细菌细胞壁合成酶（transpeptidase）的抑制剂——inhibitor 结构类似底物，占据活性位点。
- **联系 Topic 12（呼吸）**：氧化磷酸化中的**ATP 合酶（ATP synthase）**本身就是酶；抑制剂（如氰化物 cyanide）可非竞争性抑制电子传递链上的酶，导致 ATP 合成停止。
- **联系 Topic 14（内稳态）**：胰岛素与受体结合后通过级联反应激活酶（如糖原合成酶）——酶活性调控是内稳态的分子基础。
- **Km 的比较应用**：比较两种酶对同一底物的 Km，可判断哪种酶亲和力更高；在代谢调控中，低 Km 的酶在底物浓度低时就能高效工作。

---

## 速记图 / Quick-reference Summary

```
酶
├── 本质：球状蛋白 | 活性位点：互补形状 | 作用：降低活化能
├── 模型
│   ├── Lock-and-key：active site 固定
│   └── Induced-fit：active site 随底物结合改变形状 ★
├── 影响因素
│   ├── 温度 ↑→↑ | 过高→变性（不可逆！）
│   ├── pH 偏离→键断→active site 变形→速率↓
│   ├── [S] ↑→↑ | 酶饱和→平台（Vmax）
│   └── [酶] ↑→↑（底物充足时线性）
├── 抑制剂
│   ├── 竞争性：占active site | 底物↑可克服 | Vmax不变, Km↑
│   └── 非竞争性：占allosteric site | 不可克服 | Vmax↓, Km不变
├── Vmax & Km
│   ├── Vmax = 最大速率（所有活性位点饱和）
│   └── Km = 达½Vmax时的[S]；Km越小→亲和力越高
└── 固定化酶
    ├── 包埋/共价结合/吸附
    ├── 优点：可重复使用、产物纯、稳定性高、可连续生产
    └── 实例：lactase → 无乳糖奶
```

---

## 自测清单 / Self-check
- [ ] 我能用英文默写 enzyme 和 denaturation 的完整定义
- [ ] 我能清楚说出 induced-fit 与 lock-and-key 的**一个核心区别**（active site changes shape）
- [ ] 我能解释温度曲线两段（上升段原因 + 下降段原因），并提到氢键/动能
- [ ] 我知道底物浓度平台的原因：**all active sites saturated / enzyme is limiting factor**
- [ ] 我能成对对比竞争性与非竞争性抑制（结合位点 / 能否克服 / Vmax / Km）
- [ ] 我能用 Km 判断两种酶对底物的亲和力
- [ ] 我能列出固定化酶的**至少 3 个**优点并给出原因
- [ ] 我能描述 catalase 实验如何测量反应速率并列出控制变量
