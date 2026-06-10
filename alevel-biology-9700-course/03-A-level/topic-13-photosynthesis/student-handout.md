# Topic 13 — 光合作用 / Photosynthesis｜学生讲义

## 本主题你要拿下 / What you'll master
- ✅ 描述叶绿体结构如何适应光反应与暗反应
- ✅ 描述**光反应**：光解水、电子传递、光磷酸化、NADP 还原
- ✅ 描述**卡尔文循环**三阶段（固碳、还原、RuBP 再生）
- ✅ 分析**限制因素**对光合速率的影响（看图判断限制因素）
- ✅ 预测断光/降 CO₂ 时 GP 和 RuBP 浓度的变化

> 🎯 **A\* 提示**：高频丢分 ①O₂ 来自**水的光解**（不是 CO₂）；②暗反应是"光非依赖"不是"在黑暗中"；③断光实验中 GP↑ RuBP↓ 的推理。

---

## 1. 叶绿体结构 / Chloroplast Structure

```
       ┌─────────────────────────┐
       │  双层膜 (envelope)       │
       │   ┌──────┐  基质 stroma  │
       │   │基粒  │ （卡尔文循环）│
       │   │grana │   含 Rubisco  │
       │   │(类囊体│   ATP/NADP    │
       │   │堆叠) │               │
       │   └──────┘               │
       └─────────────────────────┘
```

| 结构 | 功能 |
|---|---|
| **类囊体膜（thylakoid membrane）** | 含光合色素、ETC、ATP 合酶 → **光反应**场所 |
| **基粒（grana）** | 类囊体堆叠，增大膜表面积 → 容纳更多色素 |
| **基质（stroma）** | 含卡尔文循环酶（Rubisco）→ **暗反应**场所 |
| **类囊体腔（lumen）** | 光解水处，积累 H⁺ 形成质子梯度 |

**总反应式**：
$$6CO_2 + 6H_2O \xrightarrow{\text{光能}} C_6H_{12}O_6 + 6O_2$$

---

## 2. 光合色素 / Photosynthetic Pigments

| 色素 | 颜色 | 吸收光 |
|---|---|---|
| 叶绿素 a（chlorophyll a）| 蓝绿 | 红光 + 蓝紫光 |
| 叶绿素 b（chlorophyll b）| 黄绿 | 红光 + 蓝光（辅助）|
| 类胡萝卜素（carotenoids）| 橙黄 | 蓝光（辅助，扩大光谱）|

**吸收光谱 vs 作用光谱**：
- **吸收光谱（absorption spectrum）**：色素吸收各波长光的程度
- **作用光谱（action spectrum）**：各波长光下的光合速率
- 两者大致吻合 → 证明这些色素驱动光合作用
- 植物呈**绿色**：因为绿光被**反射**（吸收最少）

---

## 3. 光反应 / Light-Dependent Reactions（类囊体膜）

### 3.1 核心事件

```
① 光激发：光子被 PSII 叶绿素吸收 → 电子被激发到高能态，离开叶绿素

② 光解水（photolysis）：
   H₂O → 2H⁺ + ½O₂ + 2e⁻
   - 电子（e⁻）补充给 PSII 失去的电子
   - H⁺ 用于还原 NADP⁺
   - O₂ 作为副产物释放

③ 电子传递：激发电子沿类囊体膜 ETC 传递
   → 能量将 H⁺ 泵入类囊体腔 → 质子梯度

④ 光磷酸化（photophosphorylation）：
   H⁺ 顺梯度经 ATP 合酶回流到基质 → 合成 ATP（化学渗透）

⑤ NADP 还原：电子到 PSI → 还原 NADP⁺ + H⁺ → NADPH
```

### 3.2 非循环 vs 循环光合磷酸化

| | 非循环（noncyclic）| 循环（cyclic）|
|---|---|---|
| 参与光系统 | PSII + PSI | 仅 PSI |
| 产物 | ATP + NADPH + O₂ | 仅 ATP |
| 电子来源 | 水（光解）| PSI 自身循环 |

**光反应产物**：**ATP + NADPH**（供卡尔文循环）+ **O₂**（释放）

---

## 4. 卡尔文循环 / Calvin Cycle（基质，光非依赖反应）

```
              CO₂
               ↓
① 固碳：CO₂ + RuBP(5C) —[Rubisco]→ 2 × GP(3C)
               ↓
② 还原：GP + ATP + NADPH → TP(3C, 三碳糖磷酸)
               ↓
        ┌──────┴──────┐
   ③ 再生            合成产物
   大部分 TP          少部分 TP
   + ATP → RuBP       → 葡萄糖/淀粉/氨基酸/脂质
   （循环继续）
```

| 阶段 | 反应 | 关键 |
|---|---|---|
| **① 固碳 Fixation** | CO₂ + RuBP(5C) → 2 GP(3C) | 酶为 **Rubisco** |
| **② 还原 Reduction** | GP → TP，消耗 **ATP + NADPH** | 用掉光反应产物 |
| **③ 再生 Regeneration** | 5/6 的 TP → RuBP，消耗 ATP | 维持循环 |

**碳计量**：固定 **6 个 CO₂**（6 轮）才能净产 **1 个葡萄糖**（C6）。

> 🎯 "光非依赖"不等于"在黑暗中进行"——它需要光反应的 ATP 和 NADPH，所以断光后很快停止。

---

## 5. 断光/降 CO₂ 实验（高频推理题）

### 5.1 突然断光（light off）
- 光反应停止 → ATP 和 NADPH **不再产生**
- ② 还原阶段停止 → GP **不能转化为 TP** → **GP 积累（↑）**
- ① 固碳仍短暂进行（消耗 RuBP）→ **RuBP 减少（↓）**

### 5.2 突然降低 CO₂（CO₂ off）
- ① 固碳减少 → GP **不再生成** → **GP 减少（↓）**
- RuBP 仍在再生但不被消耗 → **RuBP 积累（↑）**

> 记忆：**断光 GP↑ RuBP↓**；**降 CO₂ GP↓ RuBP↑**（两者相反）。

---

## 6. 限制因素 / Limiting Factors

**限制因素定律（Blackman）**：光合速率受当下供应最不足（最限制）的因素决定。

三大限制因素：
| 因素 | 影响 |
|---|---|
| **光照强度** | 影响光反应（ATP/NADPH 产量）|
| **CO₂ 浓度** | 影响固碳速率（Rubisco 底物）|
| **温度** | 影响酶活性（过高则变性）|

**图形解读**：
```
光合速率
   |        ___________ ← 平台：光不再是限制因素
   |      /                 （CO₂ 或温度成为限制）
   |    /
   |  /  ← 上升段：光照是限制因素
   |/________________
        光照强度
```

- 上升段：增加光照→速率上升 → **光是限制因素**
- 平台段：增加光照无效 → **CO₂/温度成为限制因素**
- 高 CO₂ 曲线整体更高 → 证明 CO₂ 在高光照时是限制因素

**温室应用**：补光、补 CO₂、控温 → 突破限制因素，提高产量。

---

## 必背定义 / Must-know Definitions

| 概念 | 英文定义 | 中文 |
|---|---|---|
| Photophosphorylation | *The synthesis of ATP using light energy during the light-dependent reactions.* | 光合磷酸化 |
| Photolysis | *The splitting of water using light energy, producing H⁺, electrons, and oxygen.* | 光解（水）|
| Calvin cycle | *The light-independent reactions in the stroma in which CO₂ is fixed and reduced to form carbohydrate.* | 卡尔文循环 |
| Limiting factor | *The factor that, at a given moment, is in shortest supply and therefore limits the rate of a process.* | 限制因素 |

---

## A* 拓展 / Stretch to A*
- **Topic 12 连接**：光磷酸化与氧化磷酸化机制相同——都是化学渗透（H⁺ 经 ATP 合酶）。区别：电子来源（光 vs NADH）和最终受体（NADP⁺ vs O₂）。
- **同位素实验（Hill / Calvin）**：用 ¹⁸O 标记证明光合 O₂ 来自水；用 ¹⁴C 追踪卡尔文循环碳路径。
- **Rubisco 的双重性**：高温/低 CO₂ 时 Rubisco 也催化光呼吸（与 O₂ 反应），降低效率——C4/CAM 植物演化出避免机制。
- **Hill reaction（离体实验）**：分离叶绿体 + DCPIP（人工电子受体），光照下 DCPIP 由蓝变无色——证明光反应产生还原力。

---

## 自测清单 / Self-check
- [ ] 我能说出光反应/暗反应分别在叶绿体的哪个部位进行
- [ ] 我能说明光解水的三个产物及各自去向（e⁻、H⁺、O₂）
- [ ] 我能按三阶段描述卡尔文循环，标出 ATP/NADPH 的使用位置
- [ ] 我能预测断光和降 CO₂ 时 GP/RuBP 的变化并解释
- [ ] 我能看图判断不同点的限制因素
