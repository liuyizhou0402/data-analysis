# SQL Analysis — ED & Patient Flow

Portable SQL (tested on **SQLite 3.40+** and **PostgreSQL 15**) over a small
star schema: two fact tables (`ed_presentations`, `admissions`) and one
dimension (`patients`).

| File | Purpose |
|:-----|:--------|
| [`01_schema.sql`](01_schema.sql) | DDL — tables, keys, indexes |
| [`02_analysis.sql`](02_analysis.sql) | 7 business queries (each with the question it answers) |

## Run it in 60 seconds (SQLite)

```bash
# from the project root, after running data/generate_data.py
sqlite3 ed.db < sql/01_schema.sql
sqlite3 ed.db <<'EOF'
.mode csv
.import --skip 1 data/patients.csv patients
.import --skip 1 data/ed_presentations.csv ed_presentations
.import --skip 1 data/admissions.csv admissions
EOF

# then run any query, e.g. performance by triage:
sqlite3 -header -column ed.db < sql/02_analysis.sql
```

## What each query demonstrates

| # | Business question | SQL technique |
|:-:|:------------------|:--------------|
| Q1 | Monthly demand & 4-hour (NEAT) performance | date bucketing, conditional AVG |
| Q2 | Which triage acuity groups fail the target | `CASE` mapping, multi-metric aggregation |
| Q3 | Hourly arrival profile for staffing | hour extraction, conditional `SUM` pivot |
| Q4 | Left-without-being-seen hotspots | ratios, `HAVING` on volume |
| Q5 | 28-day readmission by diagnosis | aggregation on admissions fact |
| Q6 | Frequent presenters (top 1%) | CTE + `NTILE()` window function |
| Q7 | Month-over-month seasonality | CTE + `LAG()` window function |

## Headline result (Q2)

The overall 90% "within 4 hours" figure masks the fact that the **sickest
patients breach most**:

| Triage | % within 4hr |
|:------:|:-----------:|
| T1 Resuscitation | 52.6% |
| T2 Emergency | 67.8% |
| T5 Non-urgent | 99.4% |

→ reported as a single blended KPI, this would hide a real clinical-risk problem.
See [`../docs/business_recommendations.md`](../docs/business_recommendations.md).

> **Dialect note.** Date formatting is the only dialect difference. SQLite uses
> `strftime('%Y-%m', col)`; PostgreSQL uses `to_char(col,'YYYY-MM')` /
> `EXTRACT(HOUR FROM col)`. Both forms are noted inline in `02_analysis.sql`.
