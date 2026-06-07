# Australian Chronic Disease Trends Dashboard

An interactive data dashboard analysing the prevalence of major chronic conditions across Australian states and territories from 2013 to 2023, built with Python and Streamlit.

## Live Demo

> Deploy via [Streamlit Community Cloud](https://streamlit.io/cloud) — free for public GitHub repos.

## Overview

Australia's chronic disease burden costs the health system over **$27 billion annually** (AIHW, 2023). This dashboard provides public health analysts, policy teams, and researchers with an at-a-glance view of:

- Prevalence trends for **Type 2 Diabetes, Cardiovascular Disease, Mental Health Conditions, and Obesity**
- State-by-state comparisons and relative disease burden
- Age and sex breakdowns for targeted public health planning
- Hospital admission patterns and health expenditure analysis

## Key Findings

| Finding | Data |
|---------|------|
| Mental health conditions affect ~20% of Australians, with the highest burden in the 15–24 age group | AIHW 2023 |
| Type 2 diabetes prevalence in the 65–74 age group is **14× higher** than in 15–24-year-olds | AIHW 2023 |
| Average hospital length of stay declined from 4.5 to 3.8 days (2013–2023), reflecting efficiency gains | AIHW Hospital Statistics |
| Per-capita health expenditure grew ~55% over the decade, driven by aged care and hospital costs | AIHW Health Expenditure |

## Dashboard Features

```
📊 National Overview    — KPI cards, trend lines, all-conditions area chart
🗺️ State Comparison    — Bar charts, radar chart, heatmap by state
👥 Demographics        — Age×sex grouped bars, population pyramid, age trends
🏥 Hospitals & Spend   — Admissions, ALOS, expenditure, diagnosis mix
```

All charts are interactive (hover, zoom, filter by state/year/sex via sidebar).

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.11 | Core language |
| pandas | Data wrangling |
| Plotly Express | Interactive visualisations |
| Streamlit | Web app framework |
| NumPy | Numerical operations |

## Data Source

Synthetic dataset generated from published summary statistics in:
- [AIHW Chronic Conditions](https://www.aihw.gov.au/reports-data/health-conditions-disability-deaths/chronic-disease) (2023)
- [AIHW Australia's Health 2022](https://www.aihw.gov.au/reports/australias-health/australias-health-2022-data-insights)
- [AIHW Hospital Statistics 2021–22](https://www.aihw.gov.au/reports-data/myhospitals)
- [AIHW Health Expenditure Australia 2021–22](https://www.aihw.gov.au/reports/health-welfare-expenditure)

> Real unit-record AIHW data requires a formal data access application. This project demonstrates analytical methodology that transfers directly to working with the real datasets.

## Getting Started

```bash
git clone https://github.com/liuyizhou0402/data-analysis.git
cd data-analysis/projects/p1-chronic-disease-dashboard

pip install -r requirements.txt

# Generate the data
python data/raw/generate_aihw_data.py

# Launch the dashboard
streamlit run app.py
```

## Project Structure

```
p1-chronic-disease-dashboard/
├── app.py                        # Streamlit dashboard (main entry point)
├── requirements.txt
├── data/
│   └── raw/
│       ├── generate_aihw_data.py            # Data generation script
│       ├── prevalence_by_state_age_sex.csv  # Chronic disease prevalence
│       ├── hospital_admissions_by_state.csv # Hospital activity data
│       └── health_expenditure_by_state.csv  # Health expenditure data
└── notebooks/
    └── 01_eda.ipynb              # Exploratory data analysis walkthrough
```

## Skills Demonstrated

- **Health data literacy**: Understanding AIHW data structure, Australian health system KPIs (ALOS, admission rates, per-capita expenditure)
- **EDA & data wrangling**: Cleaning, reshaping, and aggregating multi-dimensional health datasets
- **Interactive visualisation**: 10+ chart types (line, bar, heatmap, radar, pyramid, pie, area) with Plotly
- **Dashboard design**: Multi-tab layout, sidebar filters, KPI cards, responsive layout
- **Storytelling with data**: Framing findings in terms of public health impact, not just numbers

---

*Part of a digital health AI portfolio targeting Australian health data analyst / data scientist roles.*
