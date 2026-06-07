"""
Generates synthetic data based on real AIHW (Australian Institute of Health
and Welfare) statistics published in:
- AIHW 2023 Chronic Disease report
- AIHW Australia's Health 2022
- AIHW Burden of Disease Study 2022

Sources:
- https://www.aihw.gov.au/reports/chronic-disease/chronic-condition-multimorbidity
- https://www.aihw.gov.au/reports/australias-health/australias-health-2022-data-insights
"""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

STATES = ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"]
YEARS = list(range(2013, 2024))
AGE_GROUPS = ["0-14", "15-24", "25-44", "45-64", "65-74", "75+"]
SEX = ["Male", "Female"]

# AIHW-based prevalence rates (% of population, 2022 estimates)
# Source: AIHW Chronic Conditions 2023
BASE_PREVALENCE = {
    "diabetes_type2": 5.3,
    "cardiovascular_disease": 5.7,
    "mental_health_condition": 20.1,
    "chronic_respiratory": 8.5,
    "arthritis": 15.1,
    "obesity": 31.3,
    "hypertension": 23.6,
    "chronic_kidney_disease": 10.0,
}

# State population proportions (ABS 2022)
STATE_POP = {
    "NSW": 8153600,
    "VIC": 6613700,
    "QLD": 5322100,
    "WA": 2785000,
    "SA": 1820300,
    "TAS": 571500,
    "ACT": 456700,
    "NT": 249200,
}

# Age-specific relative risk multipliers for diabetes type 2 (AIHW data)
AGE_RISK_DIABETES = {
    "0-14": 0.05, "15-24": 0.15, "25-44": 0.40,
    "45-64": 1.80, "65-74": 3.50, "75+": 4.20
}
AGE_RISK_CVD = {
    "0-14": 0.02, "15-24": 0.08, "25-44": 0.30,
    "45-64": 1.60, "65-74": 4.00, "75+": 6.50
}
AGE_RISK_MENTAL = {
    "0-14": 0.60, "15-24": 1.80, "25-44": 1.40,
    "45-64": 0.90, "65-74": 0.60, "75+": 0.50
}

# Year trend: slight increase in diabetes/obesity, mental health awareness rising
def year_trend(base, year, condition):
    delta = year - 2013
    trends = {
        "diabetes_type2": 0.015,
        "obesity": 0.008,
        "mental_health_condition": 0.025,
        "cardiovascular_disease": -0.005,  # improving with treatment
        "hypertension": 0.010,
        "chronic_respiratory": 0.002,
        "arthritis": 0.003,
        "chronic_kidney_disease": 0.006,
    }
    return base * (1 + trends.get(condition, 0) * delta)


# --- Build prevalence dataset ---
rows = []
for year in YEARS:
    for state in STATES:
        for age in AGE_GROUPS:
            for sex in SEX:
                pop_base = STATE_POP[state] / (len(AGE_GROUPS) * 2)
                noise = rng.normal(1.0, 0.04)

                diabetes_rate = (
                    year_trend(BASE_PREVALENCE["diabetes_type2"], year, "diabetes_type2")
                    * AGE_RISK_DIABETES[age]
                    * (1.15 if sex == "Male" else 0.88)
                    * noise / 100
                )
                cvd_rate = (
                    year_trend(BASE_PREVALENCE["cardiovascular_disease"], year, "cardiovascular_disease")
                    * AGE_RISK_CVD[age]
                    * (1.30 if sex == "Male" else 0.75)
                    * noise / 100
                )
                mental_rate = (
                    year_trend(BASE_PREVALENCE["mental_health_condition"], year, "mental_health_condition")
                    * AGE_RISK_MENTAL[age]
                    * (0.85 if sex == "Male" else 1.18)
                    * noise / 100
                )
                obesity_rate = (
                    year_trend(BASE_PREVALENCE["obesity"], year, "obesity")
                    * (0.6 if age == "0-14" else 1.0)
                    * (1.05 if sex == "Male" else 0.96)
                    * noise / 100
                )

                rows.append({
                    "year": year,
                    "state": state,
                    "age_group": age,
                    "sex": sex,
                    "population_estimate": int(pop_base * rng.normal(1.0, 0.02)),
                    "diabetes_prevalence_pct": round(min(diabetes_rate * 100, 25), 2),
                    "cvd_prevalence_pct": round(min(cvd_rate * 100, 30), 2),
                    "mental_health_prevalence_pct": round(min(mental_rate * 100, 45), 2),
                    "obesity_prevalence_pct": round(min(obesity_rate * 100, 55), 2),
                })

prevalence_df = pd.DataFrame(rows)

# --- Build hospital admissions dataset ---
# Based on AIHW Hospital Statistics 2021-22
# Average: 11.4M admissions/year nationally
admission_rows = []
for year in YEARS:
    for state in STATES:
        state_pop = STATE_POP[state]
        # admission rate per 1000 population, AIHW benchmark ~450
        base_rate = rng.normal(450, 20)
        admissions = int(state_pop * base_rate / 1000)

        # ALOS (average length of stay) declining trend: AIHW shows ~4.5 days 2013 -> ~3.8 days 2022
        alos = round(4.5 - (year - 2013) * 0.07 + rng.normal(0, 0.15), 1)

        # Emergency vs elective split (AIHW: ~40% emergency)
        emergency_pct = round(rng.normal(40, 3), 1)

        # Top diagnosis categories (proportions from AIHW principal diagnosis data)
        admission_rows.append({
            "year": year,
            "state": state,
            "total_admissions": admissions,
            "avg_length_of_stay_days": alos,
            "emergency_admissions_pct": emergency_pct,
            "cardiovascular_admissions_pct": round(rng.normal(13.5, 1.2), 1),
            "mental_health_admissions_pct": round(rng.normal(6.8, 0.8), 1),
            "diabetes_related_admissions_pct": round(rng.normal(4.2, 0.5), 1),
            "respiratory_admissions_pct": round(rng.normal(8.1, 0.9), 1),
            "cancer_admissions_pct": round(rng.normal(9.4, 0.7), 1),
        })

admissions_df = pd.DataFrame(admission_rows)

# --- Build Medicare expenditure dataset ---
# Based on AIHW Health Expenditure Australia 2021-22
# Total health expenditure: ~$220B (2021-22)
expenditure_rows = []
for year in YEARS:
    base_exp_billion = 140 + (year - 2013) * 7.2  # rough growth
    for state in STATES:
        state_share = STATE_POP[state] / sum(STATE_POP.values())
        state_exp = base_exp_billion * state_share * rng.normal(1.0, 0.03)

        expenditure_rows.append({
            "year": year,
            "state": state,
            "total_health_expenditure_billion_aud": round(state_exp, 3),
            "per_capita_expenditure_aud": round(state_exp * 1e9 / STATE_POP[state], 0),
            "hospitals_pct": round(rng.normal(40, 2), 1),
            "primary_care_pct": round(rng.normal(22, 1.5), 1),
            "medications_pct": round(rng.normal(14, 1.2), 1),
            "aged_care_pct": round(rng.normal(11, 1.0), 1),
            "other_pct": round(rng.normal(13, 1.5), 1),
        })

expenditure_df = pd.DataFrame(expenditure_rows)

# Save
prevalence_df.to_csv("prevalence_by_state_age_sex.csv", index=False)
admissions_df.to_csv("hospital_admissions_by_state.csv", index=False)
expenditure_df.to_csv("health_expenditure_by_state.csv", index=False)

print("Datasets generated:")
print(f"  prevalence_by_state_age_sex.csv  — {len(prevalence_df):,} rows")
print(f"  hospital_admissions_by_state.csv — {len(admissions_df):,} rows")
print(f"  health_expenditure_by_state.csv  — {len(expenditure_df):,} rows")
