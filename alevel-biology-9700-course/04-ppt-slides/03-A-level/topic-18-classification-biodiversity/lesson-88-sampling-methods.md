---
marp: true
theme: default
paginate: true
backgroundColor: '#ffffff'
---

<!-- _class: lead -->
# Lesson 88: Sampling Methods
## 取样方法
Cambridge CIE 9700 | A-Level Biology | Topic 18

---

## Learning Objectives 学习目标

完成本课后，你能够：

- 描述随机取样和系统取样的方法
- 解释样方法（quadrat）和截线样条法（transect）的适用场景
- 分析取样误差和改进方法

---

## Why Sample? 为何取样？

**不可能调查所有个体**（太耗时、破坏性）

**取样目的**：
- 估计种群大小
- 测量物种多样性
- 监测种群变化

**好的取样**：
- 有代表性（representative）
- 无偏差（unbiased）
- 样本量足够大

---

## Random Sampling 随机取样

**方法**：
1. 用网格覆盖研究区域
2. 用随机数表/计算机生成随机坐标
3. 在该坐标放置样方（quadrat）
4. 记录样方内物种数量

**优点**：消除研究者偏见
**用于**：均匀分布的生境，无明显环境梯度

---

## Quadrat Method 样方法

**样方（quadrat）**：固定面积（通常0.25m² 或 1m²）的框架

**记录方式**：
- **物种数（species count）**
- **百分比覆盖度（% cover）**
- **频度（frequency）**：在多少样方中出现

**适用于**：植物、缓慢移动动物（如蜗牛）

---

## Line/Belt Transect 截线/带状样条

**截线样条（line transect）**：
- 沿环境梯度拉直线
- 记录与线接触的所有物种

**带状样条（belt transect）**：
- 沿梯度拉带状区域（通常0.5–1m宽）
- 在规则间隔放置连续样方
- 更全面

**用于**：研究沿环境梯度的物种变化
（海岸带、高度梯度、污染梯度）

---

## Mark-Release-Recapture 标志重捕法

**用于估计动物种群大小**：

$$N = \frac{M \times C}{R}$$

- N = 种群估计大小
- M = 第一次捕获并标记数量
- C = 第二次捕获总数
- R = 第二次捕获中已标记数量

**假设**：
- 标记不影响存活/行为
- 标记不脱落
- 两次捕获之间无大量出生/死亡/迁徙

---

## Worked Example 标志重捕计算

**数据**：
- 第一次捕获标记：M = 50只蜥蜴
- 第二次捕获：C = 60只（其中 R = 10只有标记）

$$N = \frac{50 \times 60}{10} = \mathbf{300}$$

估计该地区蜥蜴种群约 **300 只**

---

## Key Terms 必背术语

| Term | 含义 |
|---|---|
| Quadrat | 样方（固定面积调查框） |
| Transect | 样条（沿梯度调查带） |
| Random sampling | 随机取样 |
| Mark-release-recapture | 标志重捕法 |
| % cover | 百分比覆盖度 |

---

## Practice Question

> Describe how you would use a **random sampling** method with quadrats to estimate the **species diversity** of a grassland. **[4]**

**A\* 答法**：
1. Place a **numbered grid** over the map of the grassland.
2. Use **random numbers** (e.g. from a calculator) to select coordinates.
3. Place a **quadrat** at each coordinate; record the **number of individuals of each species**.
4. Repeat for an appropriate number of quadrats; calculate **Simpson's index D** using the data.

---

## Summary 本课小结

✅ 随机取样：随机坐标+样方，消除研究者偏见
✅ 样方：记录物种数、覆盖度、频度
✅ 样条法：研究沿梯度的物种变化（海岸/污染梯度）
✅ 标志重捕：N = MC/R，假设行为不受影响
✅ 取样误差：样本量小、非随机取样→代表性差
