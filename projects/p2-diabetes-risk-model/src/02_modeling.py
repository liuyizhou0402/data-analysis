"""
阶段2+3: 数据预处理 → 逻辑回归基线 → XGBoost → SHAP 可解释性
=================================================================
这个脚本是 P2 项目的核心，完整走完 ML pipeline：

  预处理  → 编码分类变量，标准化数值变量，划分数据集
  基线    → 逻辑回归（Logistic Regression）
  提升    → XGBoost（梯度提升树）
  评估    → ROC-AUC, PR-AUC, F1, 混淆矩阵
  解释    → SHAP（SHapley Additive exPlanations）

运行方式: python3 src/02_modeling.py
"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    roc_auc_score, average_precision_score,
    classification_report, confusion_matrix,
    RocCurveDisplay, PrecisionRecallDisplay,
)
from xgboost import XGBClassifier

# ── 路径 ───────────────────────────────────────────────────────────────────────
DATA_PATH  = Path("data/raw/diabetes_risk_cohort.csv")
MODEL_DIR  = Path("outputs/models");   MODEL_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR = Path("outputs/reports"); REPORT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")
plt.rcParams.update({"figure.dpi": 120, "font.size": 11})

# =============================================================================
# 第1步：加载 + 特征工程
# =============================================================================
print("=" * 60)
print("第1步：特征工程 & 预处理")
print("=" * 60)

df = pd.read_csv(DATA_PATH)

# 分类特征 vs 数值特征
CATEGORICAL = ["sex", "ethnicity", "smoking_status", "remoteness"]
NUMERIC = [
    "age", "bmi", "waist_cm", "systolic_bp",
    "fasting_glucose_mmol", "hba1c_pct", "cholesterol_mmol",
    "physical_activity_days_pw", "diet_quality_score",
    "family_history_diabetes", "prev_gestational_dm",
    "hypertension", "cvd_history", "depression_anxiety",
    "seifa_decile", "alcohol_risk_level",
]
TARGET = "diabetes_diagnosis"

X = df[CATEGORICAL + NUMERIC]
y = df[TARGET]

print(f"\n特征数量: {len(CATEGORICAL)} 分类 + {len(NUMERIC)} 数值 = {len(CATEGORICAL)+len(NUMERIC)} 总计")
print(f"样本数量: {len(X):,}")
print(f"正例 (糖尿病): {y.sum():,} ({y.mean()*100:.1f}%)")

# 划分训练集/测试集 — stratify 保证两组类别比例一致
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42, stratify=y
)
print(f"\n训练集: {len(X_train):,} | 测试集: {len(X_test):,}")
print(f"  训练集患病率: {y_train.mean()*100:.1f}%")
print(f"  测试集患病率: {y_test.mean()*100:.1f}%  ← stratify 确保比例一致")

# ColumnTransformer：对不同列做不同处理
#   数值列 → StandardScaler（均值0，标准差1）
#   分类列 → OneHotEncoder（0/1 虚拟变量，drop='first'避免多重共线性）
preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(),                            NUMERIC),
    ("cat", OneHotEncoder(drop="first", sparse_output=False), CATEGORICAL),
], remainder="drop")

print("\n预处理流程:")
print("  数值特征 → StandardScaler（z-score 标准化）")
print("  分类特征 → OneHotEncoder（drop='first' 避免虚拟变量陷阱）")

# =============================================================================
# 第2步：逻辑回归基线
# =============================================================================
print("\n" + "=" * 60)
print("第2步：逻辑回归基线 (Logistic Regression)")
print("=" * 60)
print("  为什么先做逻辑回归？")
print("  → 简单、可解释，是临床模型的首选基线")
print("  → 如果简单模型表现足够好，不需要复杂模型")
print("  → class_weight='balanced' 处理18:1类别不平衡\n")

lr_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        class_weight="balanced",   # 自动对少数类上权重
        max_iter=1000,
        random_state=42,
        C=0.1,                     # L2正则化强度（越小越强）
    )),
])

# 5折交叉验证（用训练集）
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
cv_auc = cross_val_score(lr_pipeline, X_train, y_train,
                          scoring="roc_auc", cv=cv)
print(f"  5折交叉验证 ROC-AUC: {cv_auc.mean():.4f} ± {cv_auc.std():.4f}")

# 在全训练集上拟合
lr_pipeline.fit(X_train, y_train)
y_prob_lr = lr_pipeline.predict_proba(X_test)[:, 1]

lr_auc = roc_auc_score(y_test, y_prob_lr)
lr_pr  = average_precision_score(y_test, y_prob_lr)
print(f"\n  测试集 ROC-AUC:  {lr_auc:.4f}")
print(f"  测试集 PR-AUC:   {lr_pr:.4f}  ← 更重要！不平衡数据用这个")
print(f"\n  分类报告 (threshold=0.5):")
y_pred_lr = (y_prob_lr >= 0.5).astype(int)
print(classification_report(y_test, y_pred_lr,
                             target_names=["No Diabetes", "Diabetes"]))

# =============================================================================
# 第3步：XGBoost
# =============================================================================
print("=" * 60)
print("第3步：XGBoost 梯度提升树")
print("=" * 60)
print("  为什么用 XGBoost？")
print("  → 处理非线性关系（年龄×BMI 的交互效应）")
print("  → 自动处理特征交互")
print("  → 澳洲健康数据竞赛（如 MIMIC challenge）常用基础模型\n")

# scale_pos_weight 替代 class_weight='balanced'：正负样本比
neg_pos_ratio = (y_train == 0).sum() / (y_train == 1).sum()
print(f"  scale_pos_weight = {neg_pos_ratio:.1f}  （负例:正例比例）\n")

xgb_pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        scale_pos_weight=neg_pos_ratio,   # 处理类别不平衡
        eval_metric="aucpr",
        random_state=42,
        verbosity=0,
    )),
])

cv_auc_xgb = cross_val_score(xgb_pipeline, X_train, y_train,
                               scoring="roc_auc", cv=cv)
print(f"  5折交叉验证 ROC-AUC: {cv_auc_xgb.mean():.4f} ± {cv_auc_xgb.std():.4f}")

xgb_pipeline.fit(X_train, y_train)
y_prob_xgb = xgb_pipeline.predict_proba(X_test)[:, 1]

xgb_auc = roc_auc_score(y_test, y_prob_xgb)
xgb_pr  = average_precision_score(y_test, y_prob_xgb)
print(f"\n  测试集 ROC-AUC: {xgb_auc:.4f}  （vs LR: {lr_auc:.4f}）")
print(f"  测试集 PR-AUC:  {xgb_pr:.4f}  （vs LR: {lr_pr:.4f}）")

y_pred_xgb = (y_prob_xgb >= 0.5).astype(int)
print(f"\n  分类报告:")
print(classification_report(y_test, y_pred_xgb,
                             target_names=["No Diabetes", "Diabetes"]))

# =============================================================================
# 第4步：模型对比图
# =============================================================================
print("=" * 60)
print("第4步：模型对比可视化")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# --- ROC 曲线 ---
for y_prob, label, colour in [
    (y_prob_lr,  f"Logistic Regression (AUC={lr_auc:.3f})",  "#3498db"),
    (y_prob_xgb, f"XGBoost             (AUC={xgb_auc:.3f})", "#e74c3c"),
]:
    disp = RocCurveDisplay.from_predictions(y_test, y_prob, name=label, ax=axes[0])
    disp.line_.set_color(colour)
axes[0].plot([0,1],[0,1], "k--", alpha=0.4, label="Random (AUC=0.5)")
axes[0].set_title("ROC Curve Comparison", fontweight="bold")
axes[0].legend(fontsize=9)

# --- Precision-Recall 曲线 ---
for y_prob, label, colour in [
    (y_prob_lr,  f"Logistic Regression (PR-AUC={lr_pr:.3f})",  "#3498db"),
    (y_prob_xgb, f"XGBoost             (PR-AUC={xgb_pr:.3f})", "#e74c3c"),
]:
    disp = PrecisionRecallDisplay.from_predictions(y_test, y_prob, name=label, ax=axes[1])
    disp.line_.set_color(colour)
axes[1].set_title("Precision-Recall Curve\n(more informative for imbalanced data)",
                  fontweight="bold")
axes[1].legend(fontsize=9)

# --- 混淆矩阵（XGBoost）---
cm = confusion_matrix(y_test, y_pred_xgb)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=["Pred: No DM", "Pred: DM"],
            yticklabels=["True: No DM", "True: DM"],
            ax=axes[2], linewidths=1)
axes[2].set_title("XGBoost Confusion Matrix\n(threshold = 0.5)", fontweight="bold")
axes[2].set_ylabel("Actual")

plt.suptitle("Model Comparison: Logistic Regression vs XGBoost",
             fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(REPORT_DIR / "06_model_comparison.png", bbox_inches="tight")
plt.close()
print("  → 图已保存: outputs/reports/06_model_comparison.png")

# =============================================================================
# 第5步：SHAP 可解释性
# =============================================================================
print("\n" + "=" * 60)
print("第5步：SHAP 可解释性分析")
print("=" * 60)
print("""
  SHAP (SHapley Additive exPlanations) 解释:
  → 每个特征对"这位患者"预测结果的贡献值
  → SHAP=+0.5 表示该特征使预测糖尿病概率上升
  → SHAP=-0.3 表示该特征使预测糖尿病概率下降
  → 基于博弈论，在临床AI中被监管机构接受
  → 澳洲 TGA 对AI医疗器械要求可解释性
""")

# 提取 XGBoost 分类器和已转换的特征矩阵
xgb_clf   = xgb_pipeline.named_steps["classifier"]
preproc   = xgb_pipeline.named_steps["preprocessor"]
X_test_tr = preproc.transform(X_test)

# 获取转换后的特征名（用于图表标签）
num_names = NUMERIC
cat_names = (preproc.named_transformers_["cat"]
             .get_feature_names_out(CATEGORICAL).tolist())
feature_names = num_names + cat_names

# 计算 SHAP 值（TreeExplainer 专为树模型优化，速度快）
explainer  = shap.TreeExplainer(xgb_clf)
shap_vals  = explainer.shap_values(X_test_tr)

# --- 图1: SHAP Summary Plot（所有特征重要性）---
plt.figure(figsize=(10, 8))
shap.summary_plot(
    shap_vals, X_test_tr,
    feature_names=feature_names,
    show=False, max_display=16,
)
plt.title("SHAP Feature Importance — XGBoost Diabetes Risk Model\n"
          "(each dot = one patient; colour = feature value; x-axis = impact on prediction)",
          fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(REPORT_DIR / "07_shap_summary.png", bbox_inches="tight")
plt.close()
print("  → 图已保存: outputs/reports/07_shap_summary.png")

# --- 图2: SHAP Bar Plot（平均特征重要性排序）---
plt.figure(figsize=(10, 7))
shap.summary_plot(
    shap_vals, X_test_tr,
    feature_names=feature_names,
    plot_type="bar",
    show=False, max_display=16,
)
plt.title("Mean |SHAP Value| — Overall Feature Importance",
          fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(REPORT_DIR / "08_shap_importance.png", bbox_inches="tight")
plt.close()
print("  → 图已保存: outputs/reports/08_shap_importance.png")

# --- 图3: 单个患者解释（Waterfall Plot）---
# 找一个高风险患者（预测概率最高的那个）
high_risk_idx = np.argmax(y_prob_xgb)
shap_exp = shap.Explanation(
    values=shap_vals[high_risk_idx],
    base_values=explainer.expected_value,
    data=X_test_tr[high_risk_idx],
    feature_names=feature_names,
)
plt.figure(figsize=(12, 6))
shap.waterfall_plot(shap_exp, max_display=12, show=False)
plt.title(f"Individual Patient Explanation — Highest Risk Patient\n"
          f"(True label: {'Diabetes' if y_test.iloc[high_risk_idx]==1 else 'No Diabetes'}, "
          f"Predicted probability: {y_prob_xgb[high_risk_idx]:.1%})",
          fontweight="bold")
plt.tight_layout()
plt.savefig(REPORT_DIR / "09_shap_waterfall.png", bbox_inches="tight")
plt.close()
print("  → 图已保存: outputs/reports/09_shap_waterfall.png")

# 打印 SHAP 全局特征重要性
mean_shap = pd.Series(
    np.abs(shap_vals).mean(axis=0),
    index=feature_names
).sort_values(ascending=False).head(12)

print(f"\n  SHAP 全局特征重要性 (Top 12):")
print(f"  {'特征':<35} {'平均|SHAP|':>10}")
print("  " + "-" * 48)
for feat, val in mean_shap.items():
    bar = "█" * int(val * 200)
    print(f"  {feat:<35} {val:>10.4f}  {bar}")

# =============================================================================
# 第6步：保存模型
# =============================================================================
print("\n" + "=" * 60)
print("第6步：保存模型")
print("=" * 60)

joblib.dump(xgb_pipeline, MODEL_DIR / "xgb_diabetes_risk_model.pkl")
joblib.dump(lr_pipeline,  MODEL_DIR / "lr_diabetes_risk_baseline.pkl")
print(f"  → XGBoost 模型: outputs/models/xgb_diabetes_risk_model.pkl")
print(f"  → LR 基线模型:  outputs/models/lr_diabetes_risk_baseline.pkl")

# =============================================================================
# 总结
# =============================================================================
print("\n" + "=" * 60)
print("建模总结")
print("=" * 60)
print(f"""
  模型性能对比:
  ┌─────────────────────┬───────────┬───────────┐
  │ 模型                │ ROC-AUC   │ PR-AUC    │
  ├─────────────────────┼───────────┼───────────┤
  │ Logistic Regression │  {lr_auc:.4f}  │  {lr_pr:.4f}  │
  │ XGBoost             │  {xgb_auc:.4f}  │  {xgb_pr:.4f}  │
  └─────────────────────┴───────────┴───────────┘

  关键学习点:
  1. ROC-AUC > 0.8 被认为是"良好"的临床预测模型
  2. PR-AUC 更适合评估不平衡数据集
  3. SHAP 值让"黑盒"模型变得可解释 → 临床接受度高
  4. 模型已保存为 .pkl，可以部署到 API 服务

  → 下一步: python3 src/03_risk_predictor.py
     （构建单个患者风险评分函数，模拟真实部署场景）
""")
