---
marp: true
theme: default
paginate: true
backgroundColor: '#ffffff'
---

<!-- _class: lead -->
# Lesson 80: Chi-squared Test
## 卡方检验
Cambridge CIE 9700 | A-Level Biology | Topic 16

---

## Learning Objectives 学习目标

完成本课后，你能够：

- 说明卡方检验的目的
- 计算卡方值并对照临界值表
- 正确陈述结论（接受/拒绝零假设）

---

## Purpose of Chi-squared 卡方检验目的

**问题**：观测到的遗传比例与理论比例是否存在**显著差异**？

**假设（Null hypothesis，H₀）**：
> 观测值与预期值之间的差异**纯属偶然**，没有显著差异

**用途**：判断偏差是由随机取样误差引起，还是真实差异

---

## Formula 公式

$$\chi^2 = \sum \frac{(O - E)^2}{E}$$

- **O** = Observed（观测值）
- **E** = Expected（预期值，根据理论比例计算）

---

## Worked Example 计算示例

**实验**：豌豆 F₂ 代，观测到：
- 圆粒：240，皱粒：60，共 300

**预期（3:1）**：
- 圆粒预期：300 × 3/4 = **225**
- 皱粒预期：300 × 1/4 = **75**

**计算**：

| 性状 | O | E | O-E | (O-E)² | (O-E)²/E |
|---|---|---|---|---|---|
| 圆粒 | 240 | 225 | 15 | 225 | 1.00 |
| 皱粒 | 60 | 75 | -15 | 225 | 3.00 |

$$\chi^2 = 1.00 + 3.00 = \mathbf{4.00}$$

---

## Degrees of Freedom 自由度

$$\text{df} = n - 1$$

（n = 分类数，类别数减1）

**本例**：2 类（圆粒 + 皱粒） → df = 2 - 1 = **1**

---

## Critical Value 临界值

**使用 p = 0.05（5% 显著性水平）**：

| df | p=0.05 临界值 |
|---|---|
| 1 | **3.841** |
| 2 | 5.991 |
| 3 | 7.815 |

**判断**：
- χ² < 临界值 → **接受 H₀**（差异不显著，可能是随机）
- χ² > 临界值 → **拒绝 H₀**（差异显著）

**本例**：χ² = 4.00 > 3.841 → **拒绝 H₀**（差异显著）

---

## Stating Conclusions 如何陈述结论

**A\* 标准表达**：

> "The calculated χ² value (4.00) is **greater than** the critical value (3.841) at **p = 0.05** with 1 degree of freedom. Therefore, we **reject** the null hypothesis. The difference between observed and expected values is **statistically significant** and is unlikely to be due to chance."

---

## Key Terms 必背术语

| Term | 含义 |
|---|---|
| Chi-squared (χ²) | 卡方值（统计量） |
| Null hypothesis | 零假设（差异仅由偶然引起） |
| Degrees of freedom | 自由度（类别数-1） |
| Critical value | 临界值（对应p=0.05） |
| p = 0.05 | 5%显著性水平 |

---

## Practice Question

> A dihybrid cross produces 280 offspring with ratios: 162 : 52 : 54 : 12. Calculate χ² and determine whether the results fit a 9:3:3:1 ratio. **[5]**

**预期（9:3:3:1，总280）**：158 : 52 : 52 : 18

**χ² = (162-158)²/158 + (52-52)²/52 + (54-52)²/52 + (12-18)²/18**
**= 0.10 + 0 + 0.08 + 2.00 = 2.18**

df = 3; 临界值 = 7.815; 2.18 < 7.815 → **接受H₀**，符合9:3:3:1

---

## Summary 本课小结

✅ 卡方检验：判断观测与预期比例差异是否显著
✅ 公式：Σ(O-E)²/E
✅ 自由度：df = 类别数 - 1
✅ 对照p=0.05临界值判断是否拒绝零假设
✅ 结论表达：比较χ²与临界值，说明是否显著
