# P2: Australian Diabetes Risk Prediction Model

A machine learning pipeline for identifying adults at elevated risk of Type 2 diabetes, designed for GP clinic decision-support in the Australian primary care setting.

**ROC-AUC: 0.91 (Logistic Regression) | 0.90 (XGBoost) — tested on 1,600 held-out patients**

---

## Clinical Context

Australia has **1.3 million people living with Type 2 diabetes** (AIHW, 2023), with a further estimated 500,000 undiagnosed. Early identification through GP screening is a national priority, underpinned by the **AUSDRISK** (Australian Type 2 Diabetes Risk Assessment Tool) framework.

This model operationalises AUSDRISK-aligned risk factors as a machine learning classifier, adding SHAP-based individual explanations to support GP clinical reasoning.

---

## Key Results

| Model | ROC-AUC | PR-AUC | CV (5-fold) |
|-------|---------|--------|-------------|
| Logistic Regression (baseline) | **0.911** | **0.414** | 0.897 ± 0.016 |
| XGBoost | 0.895 | 0.377 | 0.879 ± 0.014 |

> **Why Logistic Regression performs comparably to XGBoost:** The risk factors in this dataset have predominantly linear relationships with the outcome — a common finding in clinical prediction models validated against structured screening tools. This supports using the more interpretable LR model in lower-stakes screening contexts.

### Top Risk Factors (SHAP-ranked)

| Rank | Feature | Clinical Interpretation |
|------|---------|------------------------|
| 1 | `age` | Risk increases markedly after 45 |
| 2 | `family_history_diabetes` | ~1.4× relative risk (AIHW validated) |
| 3 | `bmi` | Strongest modifiable risk factor |
| 4 | `waist_cm` | Central obesity — metabolic syndrome proxy |
| 5 | `physical_activity_days_pw` | Inverse relationship; ≥4 days protective |

---

## Sample Risk Report

Three archetypal patients are included to demonstrate the output format:

| Patient | Age | Key Risk Factors | Predicted Risk | Level |
|---------|-----|-----------------|----------------|-------|
| PT-001 | 28F | Healthy BMI, active, no family history | 0.04% | 🟢 Low |
| PT-002 | 52M | Family history, Asian ethnicity, elevated HbA1c | 59.5% | 🔴 High |
| PT-003 | 67M | Indigenous, obese, hypertensive, sedentary | 99.0% | 🔴 High |

Individual SHAP waterfall charts explain *why* each prediction was made.

---

## Model Card

```
Model name:     XGBoost Diabetes Risk Classifier v1.0
Intended use:   Support GP-led T2DM screening in Australian primary care
Target pop:     Adults 18–79, excluding current pregnancy
Not for:        Clinical diagnosis (requires HbA1c / fasting glucose test)

Training data:  Synthetic cohort (N=8,000, 5.2% prevalence)
                Generated from AIHW & ABS 2022 published statistics
Test set:       N=1,600 (20% stratified hold-out)

Performance:
  ROC-AUC       0.895   (target: >0.80)
  PR-AUC        0.377   (imbalanced dataset — preferred metric)
  Sensitivity   63%     at 0.5 threshold
  Specificity   91%     at 0.5 threshold

Known limitations:
  - Training data is synthetic; requires validation on real clinical cohort
  - Performance on ages <25 or >75 is less certain (small subgroups)
  - Model requires retraining as population risk profiles change

Fairness:
  - Indigenous Australian elevated risk is represented in training data
  - Subgroup performance should be audited quarterly
  - SEIFA decile included to capture socioeconomic risk

Explainability:
  - SHAP TreeExplainer provides per-prediction feature contributions
  - Aligned with TGA AI/ML-based Software as a Medical Device (SaMD) guidance
```

---

## Pipeline Structure

```
src/
├── 01_eda.py          # 6-step EDA — class imbalance, distributions, correlations
├── 02_modeling.py     # Preprocessing → LR baseline → XGBoost → evaluation → SHAP
└── 03_risk_predictor.py  # Single-patient risk scoring + clinical report generation

data/raw/
├── generate_cohort.py            # Reproducible synthetic data generator
└── diabetes_risk_cohort.csv      # 8,000 patients × 20 features

outputs/
├── models/
│   ├── xgb_diabetes_risk_model.pkl
│   └── lr_diabetes_risk_baseline.pkl
└── reports/
    ├── 01–05_eda_*.png            # EDA visualisations
    ├── 06_model_comparison.png    # ROC + PR curves + confusion matrix
    ├── 07_shap_summary.png        # Global SHAP beeswarm
    ├── 08_shap_importance.png     # Mean |SHAP| bar chart
    ├── 09_shap_waterfall.png      # Highest-risk patient explanation
    └── 10_patient_*_risk_report.png  # Per-patient clinical reports
```

---

## Running the Pipeline

```bash
git clone https://github.com/liuyizhou0402/data-analysis.git
cd data-analysis/projects/p2-diabetes-risk-model

pip install -r requirements.txt

# Step 1 — generate synthetic cohort
python3 data/raw/generate_cohort.py

# Step 2 — EDA (outputs 5 charts)
python3 src/01_eda.py

# Step 3 — train models + SHAP (outputs 4 charts + 2 .pkl files)
python3 src/02_modeling.py

# Step 4 — run clinical risk reports for 3 example patients
python3 src/03_risk_predictor.py
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| pandas / numpy | Data manipulation |
| scikit-learn | Preprocessing, Logistic Regression, evaluation |
| XGBoost | Gradient boosting classifier |
| SHAP | Model explainability (TreeExplainer) |
| matplotlib / seaborn | Visualisation |
| joblib | Model serialisation |

---

## Skills Demonstrated

- **Clinical ML design**: AUSDRISK-aligned feature selection, clinically meaningful risk stratification thresholds
- **Handling class imbalance**: `class_weight='balanced'`, `scale_pos_weight`, PR-AUC as primary metric
- **Model explainability**: SHAP beeswarm, waterfall, and importance plots for both global and individual explanations
- **Pipeline engineering**: `ColumnTransformer` + `Pipeline` for reproducible preprocessing
- **Model governance**: Model Card documenting intended use, limitations, and fairness considerations — aligned with Australian TGA SaMD guidance
- **Clinical communication**: Structured risk reports with actionable GP recommendations

---

*Part of a digital health AI portfolio for Australian health data analyst / data scientist roles.*
*Portfolio: [github.com/liuyizhou0402/data-analysis](https://github.com/liuyizhou0402/data-analysis)*
