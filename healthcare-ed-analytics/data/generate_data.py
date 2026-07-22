"""
Synthetic Emergency Department (ED) & Patient Flow dataset generator.

IMPORTANT: This data is 100% synthetic. It is generated from statistical
distributions loosely calibrated to publicly reported NSW / Australian ED
patterns (triage mix, 4-hour target performance, winter respiratory surge,
28-day readmission rates). It contains NO real patient information.

Running this script reproducibly (fixed seed) writes three CSVs into ./ :
    patients.csv        - patient master (demographics)
    ed_presentations.csv- one row per ED presentation (fact table)
    admissions.csv      - inpatient admissions arising from ED (fact table)

Usage:
    python generate_data.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)

N_PATIENTS = 12_000
DATE_START = pd.Timestamp("2024-07-01")
DATE_END = pd.Timestamp("2025-06-30")  # one Australian financial year

# Sydney Local Health District-style catchment regions (synthetic labels)
REGIONS = [
    "Inner West", "Eastern Suburbs", "Northern Sydney", "South West Sydney",
    "Western Sydney", "Sutherland", "Northern Beaches", "Blacktown",
]
REGION_WEIGHTS = np.array([0.14, 0.11, 0.13, 0.17, 0.16, 0.09, 0.08, 0.12])

TRIAGE_TARGETS_MIN = {1: 0, 2: 10, 3: 30, 4: 60, 5: 120}  # ATS recommended times
TRIAGE_MIX = {1: 0.01, 2: 0.10, 3: 0.34, 4: 0.40, 5: 0.15}

PRESENTING_GROUPS = [
    "Respiratory", "Cardiac", "Injury/Trauma", "Abdominal/GI",
    "Neurological", "Mental Health", "Infection/Sepsis", "Other",
]
GROUP_WEIGHTS = np.array([0.18, 0.12, 0.20, 0.13, 0.08, 0.09, 0.08, 0.12])


def make_patients() -> pd.DataFrame:
    ages = np.clip(RNG.normal(48, 22, N_PATIENTS).round(), 0, 99).astype(int)
    return pd.DataFrame({
        "patient_id": np.arange(1, N_PATIENTS + 1),
        "age": ages,
        "sex": RNG.choice(["Female", "Male"], N_PATIENTS, p=[0.51, 0.49]),
        "region": RNG.choice(REGIONS, N_PATIENTS, p=REGION_WEIGHTS),
        # older patients carry more chronic conditions -> more readmission risk
        "chronic_conditions": np.clip(
            RNG.poisson(np.clip(ages / 30, 0.2, 3.0)), 0, 8
        ).astype(int),
        "insurance_type": RNG.choice(
            ["Medicare only", "Private health"], N_PATIENTS, p=[0.62, 0.38]
        ),
    })


def _seasonal_multiplier(day: pd.Timestamp) -> float:
    """Winter (Jun-Aug in AU) respiratory surge -> more presentations."""
    # peak around mid-July (day-of-year ~196)
    doy = day.dayofyear
    return 1.0 + 0.35 * np.cos((doy - 196) / 365 * 2 * np.pi)


def make_presentations(patients: pd.DataFrame) -> pd.DataFrame:
    days = pd.date_range(DATE_START, DATE_END, freq="D")
    rows = []
    pres_id = 1
    base_daily = 150

    for day in days:
        n = int(RNG.poisson(base_daily * _seasonal_multiplier(day)))
        # sample which patients present today (frequent-flyer patients repeat)
        weights = 1.0 + (patients["chronic_conditions"].to_numpy() ** 1.5)
        weights = weights / weights.sum()
        pid = RNG.choice(patients["patient_id"].to_numpy(), size=n, p=weights)

        for p in pid:
            triage = int(RNG.choice(list(TRIAGE_MIX), p=list(TRIAGE_MIX.values())))
            group = str(RNG.choice(PRESENTING_GROUPS, p=GROUP_WEIGHTS))

            # arrival hour: bimodal peaks late morning + evening
            hour = int(RNG.choice(
                np.arange(24),
                p=_arrival_hour_dist(),
            ))
            arrival = day + pd.Timedelta(hours=hour, minutes=int(RNG.integers(0, 60)))

            arrival_mode = "Ambulance" if RNG.random() < _ambulance_prob(triage) else "Self"

            # ED length of stay (minutes): worse for higher acuity & winter load
            base_los = {1: 240, 2: 210, 3: 180, 4: 130, 5: 95}[triage]
            load_penalty = 55 * (_seasonal_multiplier(day) - 1.0)
            los = max(20, RNG.normal(base_los + load_penalty, 55))

            lwbs = (RNG.random() < _lwbs_prob(triage, load_penalty))
            if lwbs:
                los = min(los, RNG.uniform(30, 120))

            admitted = (not lwbs) and (RNG.random() < _admit_prob(triage))

            rows.append((
                pres_id, int(p), arrival, triage, group, arrival_mode,
                round(los, 1), int(lwbs), int(admitted),
            ))
            pres_id += 1

    df = pd.DataFrame(rows, columns=[
        "presentation_id", "patient_id", "arrival_datetime", "triage_category",
        "presenting_group", "arrival_mode", "ed_los_minutes",
        "left_without_being_seen", "admitted",
    ])
    df["departure_datetime"] = (
        df["arrival_datetime"] + pd.to_timedelta(df["ed_los_minutes"], unit="m")
    )
    # met_4hr_target: departed within 240 min (NEAT / 4-hour rule)
    df["met_4hr_target"] = (df["ed_los_minutes"] <= 240).astype(int)
    return df


def _arrival_hour_dist() -> np.ndarray:
    base = np.array([
        2, 1.5, 1, 1, 1, 1.5, 3, 5, 7, 8.5, 9, 8.5,   # 0-11
        8, 7.5, 7, 6.5, 6.5, 7, 7.5, 7, 6, 5, 4, 3,     # 12-23
    ])
    return base / base.sum()


def _ambulance_prob(triage: int) -> float:
    return {1: 0.85, 2: 0.55, 3: 0.30, 4: 0.12, 5: 0.06}[triage]


def _admit_prob(triage: int) -> float:
    return {1: 0.80, 2: 0.55, 3: 0.30, 4: 0.10, 5: 0.03}[triage]


def _lwbs_prob(triage: int, load_penalty: float) -> float:
    # low-acuity patients leave when the department is busy
    base = {1: 0.0, 2: 0.005, 3: 0.02, 4: 0.05, 5: 0.09}[triage]
    return min(0.25, base + max(0, load_penalty) / 400)


def make_admissions(pres: pd.DataFrame, patients: pd.DataFrame) -> pd.DataFrame:
    adm = pres[pres["admitted"] == 1].copy().reset_index(drop=True)
    adm = adm.merge(patients[["patient_id", "age", "chronic_conditions"]],
                    on="patient_id", how="left")

    # inpatient length of stay in days: driven by acuity, age, comorbidity
    base = np.select(
        [adm["triage_category"] <= 2, adm["triage_category"] == 3],
        [6.0, 3.5], default=2.0,
    )
    los_days = np.clip(
        RNG.normal(base + adm["age"] / 40 + adm["chronic_conditions"] * 0.4, 1.5),
        0.5, 45,
    )
    admit_dt = adm["departure_datetime"]
    discharge_dt = admit_dt + pd.to_timedelta(los_days, unit="D")

    # 28-day readmission risk rises with comorbidity & age
    readmit_p = np.clip(
        0.04 + adm["chronic_conditions"] * 0.02 + (adm["age"] > 65) * 0.05, 0, 0.4
    )
    readmit = (RNG.random(len(adm)) < readmit_p).astype(int)

    discharge_dest = RNG.choice(
        ["Home", "Home with services", "Residential aged care", "Transfer", "Rehab"],
        len(adm), p=[0.55, 0.20, 0.10, 0.08, 0.07],
    )

    return pd.DataFrame({
        "admission_id": np.arange(1, len(adm) + 1),
        "presentation_id": adm["presentation_id"],
        "patient_id": adm["patient_id"],
        "admit_datetime": admit_dt.values,
        "discharge_datetime": discharge_dt.values,
        "los_days": los_days.round(2),
        "diagnosis_group": adm["presenting_group"].values,
        "discharge_destination": discharge_dest,
        "readmitted_28d": readmit,
    })


def main() -> None:
    patients = make_patients()
    pres = make_presentations(patients)
    adm = make_admissions(pres, patients)

    patients.to_csv("patients.csv", index=False)
    pres.to_csv("ed_presentations.csv", index=False)
    adm.to_csv("admissions.csv", index=False)

    print(f"patients.csv          {len(patients):>7,} rows")
    print(f"ed_presentations.csv  {len(pres):>7,} rows")
    print(f"admissions.csv        {len(adm):>7,} rows")
    print(f"4-hour target met:    {pres['met_4hr_target'].mean():.1%}")
    print(f"LWBS rate:            {pres['left_without_being_seen'].mean():.2%}")
    print(f"Admission rate:       {pres['admitted'].mean():.1%}")
    print(f"28-day readmission:   {adm['readmitted_28d'].mean():.1%}")


if __name__ == "__main__":
    main()
