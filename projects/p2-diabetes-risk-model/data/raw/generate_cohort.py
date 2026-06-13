"""
Generates a synthetic Australian diabetes risk dataset based on:
- AIHW Diabetes report 2023 (prevalence, risk factors)
- ABS National Health Survey 2022 (BMI, physical activity, smoking)
- RACGP diabetes risk factors (clinical features)

The dataset simulates a GP (general practitioner) screening cohort:
one row = one adult patient, features = routinely collected clinical
and lifestyle data, target = Type 2 diabetes diagnosis (0/1).

Clinical features chosen to match the Australian Type 2 Diabetes
Risk Assessment Tool (AUSDRISK) factors.
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(2024)
N = 8000  # realistic GP cohort size

# ── Demographics ──────────────────────────────────────────────────────────────
age = rng.integers(18, 80, N).astype(float)

# ABS 2022: ~25% Indigenous Australians have higher diabetes prevalence
# Simplified: 3% Indigenous, 30% Asian background, 67% other
ethnicity = rng.choice(
    ["European", "Asian", "Indigenous_Australian", "Other"],
    N, p=[0.62, 0.20, 0.03, 0.15]
)

sex = rng.choice(["Male", "Female"], N, p=[0.495, 0.505])

# ── Anthropometrics ───────────────────────────────────────────────────────────
# ABS 2022: mean BMI ~27.5, higher in older groups
bmi_mean = 26 + (age - 18) * 0.06
bmi_std  = 4.5
bmi = rng.normal(bmi_mean, bmi_std).clip(16, 55)

# Waist circumference (cm) — correlated with BMI
# AUSDRISK uses ≥90cm (M) or ≥80cm (F) as risk threshold
waist_base = np.where(sex == "Male", 88, 80) + (bmi - 27) * 1.4
waist_cm = (waist_base + rng.normal(0, 6, N)).clip(55, 140)

# ── Clinical measurements ─────────────────────────────────────────────────────
# Blood pressure: higher with age and BMI
sbp_mean = 115 + age * 0.45 + (bmi - 25) * 0.8
systolic_bp = (sbp_mean + rng.normal(0, 12, N)).clip(90, 200)

# Fasting glucose (mmol/L) — partially revealed (not always measured at GP)
# Normal: 3.9-5.5, impaired: 5.6-6.9, diabetic: ≥7.0
glucose_base = 4.8 + (bmi - 25) * 0.08 + (age - 40) * 0.015
fasting_glucose = (glucose_base + rng.normal(0, 0.7, N)).clip(3.5, 14.0)

# HbA1c % — correlated with glucose
hba1c = (fasting_glucose * 0.55 + 2.5 + rng.normal(0, 0.4, N)).clip(4.0, 12.0)

# Total cholesterol (mmol/L)
cholesterol = (4.8 + (age - 18) * 0.015 + rng.normal(0, 0.8, N)).clip(2.5, 9.0)

# ── Lifestyle factors ─────────────────────────────────────────────────────────
# ABS 2022: 67% insufficient physical activity
physical_activity_days_pw = rng.choice(
    [0, 1, 2, 3, 4, 5, 6, 7], N,
    p=[0.25, 0.18, 0.15, 0.13, 0.12, 0.09, 0.05, 0.03]
)
# Smoking: ABS 2022 ~12% current daily smokers
smoking_status = rng.choice(
    ["Never", "Ex-smoker", "Current"], N, p=[0.57, 0.31, 0.12]
)
# Alcohol: NHMRC guidelines — 0 = none, 1 = low, 2 = risky
alcohol_risk = rng.choice([0, 1, 2], N, p=[0.23, 0.56, 0.21])

# Fruit & veg servings per day (ABS: most Australians under-eat vegetables)
diet_quality_score = rng.integers(1, 11, N)  # 1=poor, 10=excellent

# ── Medical history ───────────────────────────────────────────────────────────
# Family history of T2DM (AUSDRISK factor — ~30% of Australians)
family_history_diabetes = rng.choice([0, 1], N, p=[0.68, 0.32])

# History of gestational diabetes (females only)
prev_gestational_dm = np.where(
    sex == "Female",
    rng.choice([0, 1], N, p=[0.92, 0.08]),
    0
)

# Hypertension diagnosis
hypertension = (systolic_bp >= 140).astype(int)
# Add some undiagnosed HTN noise
hypertension = np.where(rng.random(N) < 0.05, 1 - hypertension, hypertension)

# Cardiovascular disease history
cvd_history = rng.choice([0, 1], N, p=[0.91, 0.09])

# ── Mental health ─────────────────────────────────────────────────────────────
# AIHW: depression linked to ~60% higher T2DM risk
depression_anxiety = rng.choice([0, 1], N, p=[0.79, 0.21])

# ── Socioeconomic ─────────────────────────────────────────────────────────────
# SEIFA decile 1=most disadvantaged, 10=least (ABS)
seifa_decile = rng.integers(1, 11, N)
# Remoteness: ARIA classification
remoteness = rng.choice(
    ["Major City", "Inner Regional", "Outer Regional", "Remote"],
    N, p=[0.72, 0.18, 0.07, 0.03]
)

# ── Derive diabetes label ─────────────────────────────────────────────────────
# Based on AUSDRISK risk factors (without lab values — mirrors real screening).
# Fasting glucose / HbA1c are included as features in the ML model but not
# used to generate the label (they would leak the target in a real setting).

# Compute log-odds components (no intercept yet)
log_odds_raw = (
      0.07  * age
    + 0.15  * bmi
    + 0.04  * waist_cm
    + 1.40  * family_history_diabetes
    + 1.10  * prev_gestational_dm
    + 0.70  * hypertension
    - 0.20  * physical_activity_days_pw
    + 0.50  * (smoking_status == "Current").astype(float)
    + 0.25  * (smoking_status == "Ex-smoker").astype(float)
    - 0.08  * diet_quality_score
    + 0.40  * depression_anxiety
    - 0.06  * seifa_decile
    + np.where(ethnicity == "Indigenous_Australian", 1.8, 0)
    + np.where(ethnicity == "Asian", 0.60, 0)
)

# Binary-search intercept so that mean(P) ≈ 5.3% (AIHW national prevalence)
TARGET_PREV = 0.053
lo, hi = -40.0, 0.0
for _ in range(60):
    mid = (lo + hi) / 2
    mean_p = (1 / (1 + np.exp(-(log_odds_raw + mid)))).mean()
    if mean_p > TARGET_PREV:
        hi = mid
    else:
        lo = mid
intercept = (lo + hi) / 2

prob_diabetes = 1 / (1 + np.exp(-(log_odds_raw + intercept)))
diabetes = rng.binomial(1, prob_diabetes).astype(int)

# ── Assemble DataFrame ────────────────────────────────────────────────────────
df = pd.DataFrame({
    "age":                      age.astype(int),
    "sex":                      sex,
    "ethnicity":                ethnicity,
    "bmi":                      bmi.round(1),
    "waist_cm":                 waist_cm.round(1),
    "systolic_bp":              systolic_bp.round(0).astype(int),
    "fasting_glucose_mmol":     fasting_glucose.round(2),
    "hba1c_pct":                hba1c.round(2),
    "cholesterol_mmol":         cholesterol.round(2),
    "physical_activity_days_pw": physical_activity_days_pw,
    "smoking_status":           smoking_status,
    "alcohol_risk_level":       alcohol_risk,
    "diet_quality_score":       diet_quality_score,
    "family_history_diabetes":  family_history_diabetes,
    "prev_gestational_dm":      prev_gestational_dm,
    "hypertension":             hypertension,
    "cvd_history":              cvd_history,
    "depression_anxiety":       depression_anxiety,
    "seifa_decile":             seifa_decile,
    "remoteness":               remoteness,
    "diabetes_diagnosis":       diabetes,   # ← target variable
})

df.to_csv("diabetes_risk_cohort.csv", index=False)

print(f"Dataset saved: {len(df):,} rows × {df.shape[1]} columns")
print(f"Diabetes prevalence: {df['diabetes_diagnosis'].mean()*100:.1f}%  "
      f"(AIHW target: ~5.3%)")
print(f"\nFeature summary:")
print(df.describe(include="all").T[["count","mean","std","min","max"]].to_string())
