# Topic 12 — 能量与呼吸作用 / Energy and Respiration｜学生讲义

## 本主题你要拿下 / What you'll master
- ✅ 描述**糖酵解、丙酮酸脱氢、克雷布斯循环、氧化磷酸化**四个阶段，说出各阶段发生部位和产物
- ✅ 解释**化学渗透（chemiosmosis）**机制，理解 H⁺ 梯度→ATP 合成的原理
- ✅ 比较**有氧与无氧呼吸**的 ATP 产量和产物，解释无氧呼吸为何能维持糖酵解
- ✅ 计算**呼吸商（RQ）**，判断呼吸底物类型

> 🎯 **A\* 提示**：最容易丢分处 ①克雷布斯循环在**基质**（不是内膜上）；②无氧呼吸的目的是**再生 NAD⁺**而非直接产 ATP；③FADH₂ 进入 ETC 的位置（复合体 II，比 NADH 少产约 1 ATP）。

---

## 1. ATP——能量货币 / ATP: Energy Currency

**ATP（腺苷三磷酸）**：细胞内通用能量转移分子。

```
ATP  ⇌  ADP + Pᵢ   ΔG ≈ -30 kJ/mol（水解）
      ATP 合成酶 / 磷酸化酶
```

**ATP 的优势**：
- 可溶于细胞质，可立即用于反应
- 每次水解只释放一小包能量（适合精确控制）
- 可从多种来源再合成（磷酸化）

**合成 ATP 的三种方式**：
| 方式 | 发生位置 | 能量来源 |
|---|---|---|
| 底物磷酸化 | 细胞质（糖酵解）/ 线粒体基质（克雷布斯）| 直接从底物转移磷酸基团 |
| 氧化磷酸化 | 线粒体内膜 | 电子传递链 + 化学渗透 |
| 光磷酸化 | 叶绿体类囊体膜 | 光能（Topic 13）|

---

## 2. 有氧呼吸的四个阶段 / Four Stages of Aerobic Respiration

```
葡萄糖
  ↓ 阶段①：糖酵解（细胞质）
2 丙酮酸 + 2 ATP（净）+ 2 NADH
  ↓ 阶段②：丙酮酸脱氢（线粒体基质）
2 乙酰 CoA + 2 CO₂ + 2 NADH
  ↓ 阶段③：克雷布斯循环（线粒体基质）
4 CO₂ + 6 NADH + 2 FADH₂ + 2 ATP（底物磷酸化）
  ↓ 阶段④：氧化磷酸化（线粒体内膜）
~26 ATP  +  H₂O
```

---

## 3. 阶段①：糖酵解 / Glycolysis（细胞质）

**不需要氧气**（有氧/无氧均发生）。

```
葡萄糖（C6H₁₂O₆）
    ↓ 磷酸化（消耗 2 ATP）
磷酸果糖（6C）
    ↓ 裂解
2 × 3-磷酸甘油醛（G3P，C3）
    ↓ 氧化（NADH产生）+ 底物磷酸化（产生 ATP）
2 × 丙酮酸（pyruvate，C3）
```

**净产物（每葡萄糖）**：
- **2 ATP**（消耗 2，产生 4）
- **2 NADH**（NAD⁺ + H⁺ + e⁻ → NADH）
- **2 丙酮酸**

---

## 4. 阶段②：丙酮酸脱氢 / Pyruvate Decarboxylation（线粒体基质）

```
丙酮酸（C3）→ 乙酰辅酶 A（acetyl-CoA，C2）+ CO₂ + NADH
（每葡萄糖：2 × 以上反应）
```

关键点：丙酮酸从细胞质**转运进线粒体**，才能进行此步骤。

---

## 5. 阶段③：克雷布斯循环 / Krebs Cycle（线粒体基质）

**每轮（处理 1 个乙酰 CoA）**：

```
乙酰 CoA（2C）+ 草酰乙酸 OAA（4C）→ 柠檬酸（6C）
    ↓ 脱羧 + 脱氢（×2）
4C 中间产物 ——— 脱羧 ×1 → CO₂ ×2
              ——— 脱氢 ×3 → 3 NADH
                         ×1 → 1 FADH₂
              ——— 底物磷酸化 → 1 ATP
    ↓
草酰乙酸（OAA，4C）再生 → 循环继续
```

**每轮产物**：3 NADH + 1 FADH₂ + 1 ATP + 2 CO₂

**每葡萄糖（2 轮）**：6 NADH + 2 FADH₂ + 2 ATP + 4 CO₂

> 🎯 克雷布斯循环的 CO₂ 就是有氧呼吸呼出的 CO₂ 来源。

---

## 6. 阶段④：氧化磷酸化与化学渗透 / Oxidative Phosphorylation & Chemiosmosis（线粒体内膜）

### 6.1 电子传递链（ETC）

```
NADH → [复合体 I] → 辅酶 Q → [复合体 III] → 细胞色素 c → [复合体 IV] → ½O₂ + 2H⁺ → H₂O
FADH₂ → [复合体 II] → 辅酶 Q → ...（跳过复合体 I）
```

- 电子沿链传递，**能量逐步释放**
- 能量用于将 **H⁺（质子）泵出**内膜进入膜间隙

### 6.2 化学渗透（Mitchell 假说）

```
H⁺ 积累在膜间隙 → 质子梯度（[H⁺]膜间隙 >> [H⁺]基质）
    ↓
H⁺ 通过 ATP 合酶（ATP synthase）旋转回流到基质
    ↓
ATP 合酶旋转 → ADP + Pᵢ → ATP
    ↓
O₂ 作为最终电子受体（接受电子 + H⁺ → H₂O）
```

**ATP 产量**（每葡萄糖，理论值）：
- NADH（10 个）× 2.5 = 25 ATP
- FADH₂（2 个）× 1.5 = 3 ATP
- 底物磷酸化（糖酵解 2 + 克雷布斯 2）= 4 ATP
- **总计 ≈ 30 ATP**

---

## 7. 无氧呼吸 / Anaerobic Respiration

**为何需要无氧呼吸？**  
无氧时，ETC 无法运作，NADH 积累 → **NAD⁺ 耗尽** → 糖酵解停止。

**解决方案**：利用丙酮酸重新氧化 NADH，再生 NAD⁺，让糖酵解继续（仅产 2 ATP）。

### 7.1 乳酸发酵（动物、某些细菌）

```
丙酮酸 + NADH  →  乳酸（lactate）+ NAD⁺
           （乳酸脱氢酶 LDH）
```

- 乳酸可运至肝脏转化回葡萄糖（科里循环）

### 7.2 酒精发酵（酵母菌、植物）

```
丙酮酸  →  乙醛（acetaldehyde）+ CO₂  （丙酮酸脱羧酶）
乙醛 + NADH  →  乙醇（ethanol）+ NAD⁺   （醇脱氢酶）
```

- 酒精有毒性，酵母菌在乙醇浓度约 15% 时死亡

### 7.3 有氧 vs 无氧对比

| | 有氧呼吸 | 无氧（乳酸）| 无氧（酒精）|
|---|---|---|---|
| ATP 产量 | ~30 | 2 | 2 |
| 最终产物 | CO₂ + H₂O | 乳酸 | 乙醇 + CO₂ |
| O₂ 需要 | 是 | 否 | 否 |
| 发生位置 | 细胞质 + 线粒体 | 细胞质 | 细胞质 |

---

## 8. 呼吸商（RQ）/ Respiratory Quotient

$$RQ = \frac{\text{CO}_2 \text{ 产生量（mol）}}{\text{O}_2 \text{ 消耗量（mol）}}$$

| 呼吸底物 | RQ 值 |
|---|---|
| 纯碳水化合物（葡萄糖） | **1.0** |
| 纯脂肪 | **~0.7**（含更多 H，需更多 O₂ 氧化）|
| 纯蛋白质 | **~0.8** |
| 无氧呼吸（酒精发酵）| **∞**（产 CO₂ 但不耗 O₂）|

> 实际生物体 RQ 介于 0.7–1.0 之间（混合底物）。运动后 RQ 升高（更多碳水）。

---

## 必背定义 / Must-know Definitions

| 概念 | 英文定义 | 中文 |
|---|---|---|
| Glycolysis | *The splitting of glucose (6C) into two pyruvate molecules (3C each) in the cytoplasm, producing a net 2 ATP and 2 NADH.* | 糖酵解 |
| Krebs cycle | *A cyclic series of reactions in the mitochondrial matrix in which acetyl-CoA is oxidised, producing NADH, FADH₂, ATP, and CO₂.* | 克雷布斯循环 |
| Chemiosmosis | *The movement of H⁺ ions down an electrochemical gradient through ATP synthase, driving ATP synthesis.* | 化学渗透 |
| Respiratory quotient (RQ) | *The ratio of CO₂ produced to O₂ consumed during respiration.* | 呼吸商 |

---

## A* 拓展 / Stretch to A*
- **Topic 13 连接**：光合作用产生的 ATP（光磷酸化）机制与化学渗透相同——类囊体膜上的 ATP 合酶。
- **抑制剂实验**：氰化物（cyanide）阻断复合体 IV → ETC 停止 → ATP 急剧减少；DNP（解偶联剂）使 H⁺ 漏回基质 → ATP↓、热量↑（用于部分减肥药研究，但有毒）。
- **底物水平磷酸化 vs 氧化磷酸化**：前者无需 O₂，后者依赖 O₂ 作为最终电子受体。
- **脂肪酸 β-氧化**：长链脂肪酸先在线粒体基质经 β-氧化，每轮产生 1 乙酰 CoA + 1 NADH + 1 FADH₂，最终进入克雷布斯。

---

## 自测清单 / Self-check
- [ ] 我能说出有氧呼吸四阶段的名称、发生部位和净产物
- [ ] 我能解释化学渗透：H⁺ 梯度如何驱动 ATP 合酶合成 ATP
- [ ] 我能解释无氧呼吸为何只产 2 ATP，以及其目的（再生 NAD⁺）
- [ ] 我能计算 RQ 并判断底物类型
- [ ] 我能说出 FADH₂ 比 NADH 少产 ~1 ATP 的原因（进入 ETC 位置不同）
