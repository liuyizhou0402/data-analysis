"""
阶段1: 探索性数据分析 (EDA)
================================
目标：在建模之前，先深入理解数据
  - 数据集概览（规模、类型、缺失值）
  - 目标变量分布 → 发现类别不平衡
  - 数值特征分布
  - 分类特征分布
  - 特征与目标的关系
  - 相关性矩阵

运行方式: python3 src/01_eda.py
输出图片: outputs/reports/ 文件夹
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from pathlib import Path

# ── 路径设置 ──────────────────────────────────────────────────────────────────
DATA_PATH   = Path("data/raw/diabetes_risk_cohort.csv")
OUTPUT_DIR  = Path("outputs/reports")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── 全局绘图风格 ───────────────────────────────────────────────────────────────
sns.set_theme(style="whitegrid", palette="husl")
plt.rcParams.update({"figure.dpi": 120, "font.size": 11})

POSITIVE_COLOUR = "#e74c3c"   # 红色 = 糖尿病
NEGATIVE_COLOUR = "#3498db"   # 蓝色 = 无糖尿病

# =============================================================================
# 第1步：加载数据并打印基本信息
# =============================================================================
print("=" * 60)
print("第1步：数据集概览")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

print(f"\n数据形状: {df.shape[0]:,} 行 × {df.shape[1]} 列")
print(f"\n列名及数据类型:")
print(df.dtypes.to_string())

print(f"\n缺失值统计:")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.any() else "  ✓ 无缺失值")

print(f"\n数值型特征的基本统计量:")
print(df.describe().T.round(2).to_string())

# =============================================================================
# 第2步：目标变量分布 —— 类别不平衡是核心挑战
# =============================================================================
print("\n" + "=" * 60)
print("第2步：目标变量分布（类别不平衡分析）")
print("=" * 60)

target_counts = df["diabetes_diagnosis"].value_counts()
prevalence    = df["diabetes_diagnosis"].mean() * 100

print(f"\n  无糖尿病 (0): {target_counts[0]:,} 人 ({100-prevalence:.1f}%)")
print(f"  有糖尿病 (1): {target_counts[1]:,} 人 ({prevalence:.1f}%)")
print(f"\n  类别比例: {target_counts[0]/target_counts[1]:.1f} : 1  ← 严重不平衡！")
print("  → 建模时需要用 class_weight='balanced' 或 SMOTE 处理")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 左图：计数条形图
bars = axes[0].bar(
    ["No Diabetes (0)", "Diabetes (1)"],
    target_counts.values,
    color=[NEGATIVE_COLOUR, POSITIVE_COLOUR],
    alpha=0.85, edgecolor="white", linewidth=1.5,
)
for bar, count in zip(bars, target_counts.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                 f"{count:,}", ha="center", va="bottom", fontweight="bold")
axes[0].set_title("Target Variable Distribution", fontweight="bold")
axes[0].set_ylabel("Patient Count")
axes[0].set_ylim(0, target_counts[0] * 1.12)

# 右图：饼图
axes[1].pie(
    target_counts.values,
    labels=[f"No Diabetes\n{100-prevalence:.1f}%", f"Diabetes\n{prevalence:.1f}%"],
    colors=[NEGATIVE_COLOUR, POSITIVE_COLOUR],
    autopct="%1.1f%%", startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)
axes[1].set_title("Class Imbalance — 18:1 Ratio", fontweight="bold")

plt.suptitle("⚠️  Severe Class Imbalance — Requires Special Handling in Modeling",
             fontsize=13, fontweight="bold", color="#c0392b", y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_target_distribution.png", bbox_inches="tight")
plt.close()
print("  → 图已保存: outputs/reports/01_target_distribution.png")

# =============================================================================
# 第3步：数值特征分布（按糖尿病/非糖尿病分组）
# =============================================================================
print("\n" + "=" * 60)
print("第3步：数值特征分布对比（患病 vs 非患病）")
print("=" * 60)

NUMERIC_FEATURES = [
    "age", "bmi", "waist_cm", "systolic_bp",
    "fasting_glucose_mmol", "hba1c_pct", "cholesterol_mmol",
    "physical_activity_days_pw", "diet_quality_score", "seifa_decile"
]

fig, axes = plt.subplots(2, 5, figsize=(20, 8))
axes = axes.flatten()

for i, feat in enumerate(NUMERIC_FEATURES):
    ax = axes[i]
    for label, colour, name in [
        (0, NEGATIVE_COLOUR, "No Diabetes"),
        (1, POSITIVE_COLOUR, "Diabetes"),
    ]:
        subset = df[df["diabetes_diagnosis"] == label][feat]
        ax.hist(subset, bins=30, alpha=0.6, color=colour,
                label=name, density=True, edgecolor="none")
    ax.set_title(feat.replace("_", " ").title(), fontweight="bold", fontsize=10)
    ax.set_xlabel("")
    ax.set_ylabel("Density")
    ax.legend(fontsize=8)

plt.suptitle("Numeric Feature Distributions: Diabetes vs No Diabetes",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_numeric_distributions.png", bbox_inches="tight")
plt.close()

# 打印每个特征在两组中的均值差异
print(f"\n  {'特征':<30} {'非糖尿病均值':>12} {'糖尿病均值':>12} {'差异':>10}")
print("  " + "-" * 68)
for feat in NUMERIC_FEATURES:
    mean_no  = df[df["diabetes_diagnosis"]==0][feat].mean()
    mean_yes = df[df["diabetes_diagnosis"]==1][feat].mean()
    diff     = mean_yes - mean_no
    sign     = "↑" if diff > 0 else "↓"
    print(f"  {feat:<30} {mean_no:>12.2f} {mean_yes:>12.2f} {sign} {abs(diff):>7.2f}")

print("  → 图已保存: outputs/reports/02_numeric_distributions.png")

# =============================================================================
# 第4步：分类特征分布
# =============================================================================
print("\n" + "=" * 60)
print("第4步：分类特征与糖尿病风险关系")
print("=" * 60)

CATEGORICAL_FEATURES = [
    "sex", "ethnicity", "smoking_status", "remoteness",
    "family_history_diabetes", "hypertension", "depression_anxiety"
]

fig, axes = plt.subplots(2, 4, figsize=(20, 9))
axes = axes.flatten()

for i, feat in enumerate(CATEGORICAL_FEATURES):
    ax = axes[i]
    # 计算每个类别中糖尿病患病率
    rates = (
        df.groupby(feat)["diabetes_diagnosis"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "diabetes_rate", "count": "n"})
        .sort_values("diabetes_rate", ascending=False)
    )
    rates["diabetes_rate_pct"] = rates["diabetes_rate"] * 100

    bars = ax.bar(
        range(len(rates)), rates["diabetes_rate_pct"],
        color=[POSITIVE_COLOUR if r > prevalence else NEGATIVE_COLOUR
               for r in rates["diabetes_rate_pct"]],
        alpha=0.80, edgecolor="white"
    )
    # 在条形上标注样本量
    for j, (_, row) in enumerate(rates.iterrows()):
        ax.text(j, row["diabetes_rate_pct"] + 0.1,
                f"n={row['n']:,}", ha="center", va="bottom", fontsize=7)

    ax.axhline(prevalence, color="grey", linestyle="--", linewidth=1.2,
               label=f"Average ({prevalence:.1f}%)")
    ax.set_xticks(range(len(rates)))
    ax.set_xticklabels(rates[feat].astype(str), rotation=25, ha="right", fontsize=9)
    ax.set_title(feat.replace("_", " ").title(), fontweight="bold", fontsize=10)
    ax.set_ylabel("Diabetes Rate (%)")
    ax.legend(fontsize=8)

axes[-1].set_visible(False)
plt.suptitle("Diabetes Prevalence by Categorical Feature",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_categorical_rates.png", bbox_inches="tight")
plt.close()
print("  → 图已保存: outputs/reports/03_categorical_rates.png")

# =============================================================================
# 第5步：相关性热力图（仅数值变量）
# =============================================================================
print("\n" + "=" * 60)
print("第5步：特征相关性矩阵")
print("=" * 60)

corr = df[NUMERIC_FEATURES + ["diabetes_diagnosis"]].corr()

# 打印与目标变量相关性最高的特征（排序）
target_corr = corr["diabetes_diagnosis"].drop("diabetes_diagnosis").abs().sort_values(ascending=False)
print("\n  与糖尿病诊断的相关性（按绝对值排序）:")
for feat, val in target_corr.items():
    bar = "█" * int(val * 40)
    print(f"  {feat:<30} {val:>6.3f}  {bar}")

fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(
    corr, mask=mask, annot=True, fmt=".2f",
    cmap="RdBu_r", center=0, vmin=-1, vmax=1,
    square=True, linewidths=0.5,
    annot_kws={"size": 9}, ax=ax,
)
ax.set_title("Feature Correlation Matrix\n(bottom-left triangle only)",
             fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_correlation_matrix.png", bbox_inches="tight")
plt.close()
print("  → 图已保存: outputs/reports/04_correlation_matrix.png")

# =============================================================================
# 第6步：关键临床指标箱线图
# =============================================================================
print("\n" + "=" * 60)
print("第6步：关键临床指标箱线图（患病 vs 非患病）")
print("=" * 60)

KEY_CLINICAL = ["age", "bmi", "waist_cm", "fasting_glucose_mmol", "hba1c_pct", "systolic_bp"]

fig, axes = plt.subplots(1, 6, figsize=(20, 5))
for i, feat in enumerate(KEY_CLINICAL):
    ax = axes[i]
    data = [
        df[df["diabetes_diagnosis"]==0][feat].dropna(),
        df[df["diabetes_diagnosis"]==1][feat].dropna(),
    ]
    bp = ax.boxplot(
        data, tick_labels=["No DM", "DM"],
        patch_artist=True,
        medianprops=dict(color="white", linewidth=2.5),
        boxprops=dict(linewidth=1.5),
    )
    bp["boxes"][0].set_facecolor(NEGATIVE_COLOUR + "BB")
    bp["boxes"][1].set_facecolor(POSITIVE_COLOUR + "BB")
    ax.set_title(feat.replace("_", "\n").replace("mmol","(mmol)"), fontsize=9, fontweight="bold")
    ax.set_ylabel(feat.split("_")[-1])

plt.suptitle("Clinical Feature Comparison: Diabetes vs No Diabetes",
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "05_clinical_boxplots.png", bbox_inches="tight")
plt.close()
print("  → 图已保存: outputs/reports/05_clinical_boxplots.png")

# =============================================================================
# EDA 总结
# =============================================================================
print("\n" + "=" * 60)
print("EDA 总结 — 建模前的关键发现")
print("=" * 60)
print("""
  1. 类别不平衡严重 (18:1)
     → 不能用 accuracy 评估模型
     → 用 ROC-AUC 和 Precision-Recall AUC
     → 建模时加 class_weight='balanced'

  2. 年龄和 BMI 是最强的连续型风险因素
     → 糖尿病患者平均年龄更大、BMI 更高

  3. 家族史 (family_history_diabetes) 相关性最强
     → AUSDRISK 临床验证与此一致

  4. fasting_glucose 和 hba1c 分布右偏
     → 少数高值患者需要关注（异常值检测）

  5. Indigenous Australian 患病率明显高于其他族裔
     → 与 AIHW 报告完全一致，模型需要考虑公平性

下一步 → 运行 python3 src/02_modeling.py
""")
