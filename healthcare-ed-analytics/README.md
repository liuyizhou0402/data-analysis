# 🏥 Emergency Department & Patient Flow Analytics

**An end-to-end healthcare analytics project** — from raw data to SQL analysis
to an interactive dashboard to costed business recommendations. Built to mirror
the questions a **health data analyst** answers for an Australian hospital or
health service (NEAT 4-hour target, LWBS, 28-day readmissions, patient flow).

> **Data is 100% synthetic** (reproducible, seed-controlled) and models publicly
> reported Australian ED patterns. No real patient records are used.

---

## 📊 Dashboard

![ED Performance Dashboard](dashboard/ed_performance_dashboard.png)

*Rendered from the data by [`analysis/build_dashboard.py`](analysis/build_dashboard.py)
(Python + matplotlib). A step-by-step [**Power BI build guide**](dashboard/powerbi_build_guide.md)
with all [**DAX measures**](dashboard/dax_measures.md) reproduces the same views
as an interactive `.pbix`.*

> 📖 **[Read the full 14-figure analysis report →](analysis/analysis_report.md)**
> — every chart with written interpretation, from demand and the 4-hour target
> through readmissions and high utilisers.

---

## 🔎 Three headline insights

1. **The sickest patients wait the longest.** Overall 4-hour (NEAT) performance
   is 90%, but that blends away the clinical risk: T1 *Resuscitation* patients
   meet the target only **52.6%** of the time vs **99.4%** for non-urgent T5.
2. **Winter demand is predictable and under-resourced.** Jun–Aug presentations
   are ~50% higher and 4-hour performance drops **5.2 percentage points** — a
   forecastable surge, not a surprise.
3. **A small cohort drives outsized demand.** The top **1% of patients (107
   people)** account for **4.9% of all presentations** — averaging 25 visits and
   6.3 chronic conditions each — a clear care-coordination target.

Full analysis and four costed recommendations →
[**docs/business_recommendations.md**](docs/business_recommendations.md)

---

## 🗂️ What's in here

```
healthcare-ed-analytics/
├── data/            synthetic data + reproducible generator
├── sql/             star-schema DDL + 7 business analysis queries
├── analysis/        14-figure analysis report + EDA & dashboard scripts
│   ├── analysis_report.md   ← the full written walkthrough
│   └── figures/             ← 14 rendered charts
├── dashboard/       dashboard image + Power BI build guide + DAX measures
└── docs/            business recommendations & KPI scorecard
```

## 🛠️ Skills demonstrated

| Area | Detail |
|:-----|:-------|
| **SQL** | star-schema modelling, CTEs, window functions (`LAG`, `NTILE`), conditional aggregation — [`sql/`](sql) |
| **Python** | reproducible data engineering (`pandas`/`numpy`), dashboard rendering (`matplotlib`) — [`analysis/`](analysis) |
| **BI** | Power BI data model, DAX measures, conditional formatting — [`dashboard/`](dashboard) |
| **Domain** | Australian ED metrics: NEAT 4-hour target, ATS triage, LWBS, 28-day readmission, patient flow |
| **Communication** | turning metrics into targeted, costed recommendations for a non-technical stakeholder |

## ▶️ Reproduce it end-to-end

```bash
pip install -r requirements.txt

# 1. generate the synthetic data
python data/generate_data.py

# 2. run the SQL analysis (SQLite)
sqlite3 ed.db < sql/01_schema.sql
sqlite3 ed.db <<'EOF'
.mode csv
.import --skip 1 data/patients.csv patients
.import --skip 1 data/ed_presentations.csv ed_presentations
.import --skip 1 data/admissions.csv admissions
EOF
sqlite3 -header -column ed.db < sql/02_analysis.sql

# 3. regenerate the 14 analysis figures + the summary dashboard
python analysis/eda.py
python analysis/build_dashboard.py
```

---

*Portfolio project. Synthetic data only — illustrative of analytical workflow,
not descriptive of any real health service.*
