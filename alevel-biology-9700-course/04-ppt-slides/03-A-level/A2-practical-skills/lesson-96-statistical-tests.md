---
marp: true
theme: default
paginate: true
backgroundColor: '#ffffff'
---

<!-- _class: lead -->
# Lesson 96: Statistical Tests
## 统计检验
Cambridge CIE 9700 | A-Level Biology | A2 Practical

---

## Learning Objectives 学习目标

完成本课后，你能够：

- 决定何时使用卡方检验 vs 相关系数
- 计算 Spearman 等级相关系数
- 正确解读统计显著性

---

## When to Use Which Test 选择检验方法

| 数据类型 | 检验方法 |
|---|---|
| 分类数据（频率/比例） | **Chi-squared test（卡方检验）** |
| 两连续变量的相关性 | **Spearman's rank correlation** |
| 比较两组均值（大样本） | Student's t-test |
| 比较两样本（非参数） | Mann-Whitney U test |

**CIE A2 考纲主要考**：Chi-squared + Spearman's rank

---

## Chi-squared Review 卡方检验回顾

$$\chi^2 = \sum \frac{(O-E)^2}{E}$$

**步骤**：
1. 陈述零假设（H₀）
2. 计算预期值 E
3. 计算各类别 (O-E)²/E
4. 求和得 χ²
5. 计算自由度：df = 类别数 - 1
6. 查临界值表（p=0.05）
7. 与临界值比较，接受/拒绝 H₀

---

## Spearman's Rank Correlation 斯皮尔曼等级相关系数

**用途**：检验两个变量之间是否存在**相关性**

**适用条件**：数据可以排序（等级）

**公式**：
$$r_s = 1 - \frac{6\sum d^2}{n(n^2-1)}$$

- d = 每对数据的等级差
- n = 数据对数
- r_s 范围：-1 到 +1

---

## Spearman's Worked Example 计算示例

**数据**：5个样地的物种多样性与植被高度

| 样地 | 多样性 | 高度 | 多样性等级 | 高度等级 | d | d² |
|---|---|---|---|---|---|---|
| A | 0.8 | 45 | 5 | 5 | 0 | 0 |
| B | 0.6 | 38 | 3 | 3 | 0 | 0 |
| C | 0.7 | 42 | 4 | 4 | 0 | 0 |
| D | 0.3 | 22 | 1 | 1 | 0 | 0 |
| E | 0.5 | 31 | 2 | 2 | 0 | 0 |

Σd² = 0; r_s = 1 - 0 = **1.0**（完全正相关）

---

## Interpreting Spearman's rs 解读相关系数

| r_s 值 | 含义 |
|---|---|
| +1.0 | 完全正相关 |
| +0.7 to +0.9 | 强正相关 |
| +0.3 to +0.6 | 弱正相关 |
| 0 | 无相关 |
| -0.3 to -0.6 | 弱负相关 |
| -1.0 | 完全负相关 |

**需查临界值表（n和p=0.05）确认显著性**

---

## Critical Values 临界值查表

**Spearman's 临界值（p=0.05，双尾）**：

| n（数据对数） | 临界 r_s |
|---|---|
| 5 | 0.900 |
| 8 | 0.738 |
| 10 | 0.648 |
| 20 | 0.450 |

**|r_s| > 临界值** → 相关性显著（拒绝 H₀）

---

## Correlation vs Causation 相关 vs 因果

**重要区分**：
- 统计相关性**不等于因果关系**
- 两变量相关 → 可能有第三变量（混淆变量）
- 需要**控制实验**证明因果

**示例**：
- 冰淇淋销量与溺水死亡人数相关 → 第三变量：夏季温度

---

## Key Terms 必背术语

| Term | 含义 |
|---|---|
| Spearman's rank | 斯皮尔曼等级相关系数 |
| Correlation | 相关性（正/负/无） |
| Null hypothesis | 零假设（无相关） |
| r_s | 相关系数（-1到+1） |
| Confounding variable | 混淆变量 |

---

## Practice Question

> Explain how you would test whether there is a **significant correlation** between soil pH and plant species diversity using **Spearman's rank correlation**. **[4]**

**A\* 答法**：
1. Rank both **pH values** and **diversity values** separately (1 = lowest).
2. Calculate **d** (difference in ranks) for each site; calculate d².
3. Apply formula: r_s = 1 – 6Σd² / n(n²–1).
4. Compare |r_s| with **critical value** at p=0.05 for given n; if |r_s| > critical value, **reject H₀** (significant correlation).

---

## Summary 本课小结

✅ 卡方：分类数据，比较观测vs预期频率
✅ 斯皮尔曼：连续/等级数据，检验两变量相关性
✅ r_s公式：1 - 6Σd²/n(n²-1)
✅ 解读：|r_s| > 临界值→显著相关，拒绝H₀
✅ 相关≠因果！需注意混淆变量
