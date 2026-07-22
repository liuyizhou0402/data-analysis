# Business Recommendations — Emergency Department & Patient Flow

*Analysis of 54,837 synthetic ED presentations and 11,045 inpatient admissions,
Australian financial year 2024–25. Figures below are drawn directly from the
SQL in [`../sql/02_analysis.sql`](../sql/02_analysis.sql) and the dashboard in
[`../dashboard/`](../dashboard).*

---

## Executive summary

The department meets the 4-hour National Emergency Access Target (NEAT) for
**90%** of presentations overall — but that headline hides three actionable
problems: **the sickest patients breach most**, a **predictable winter surge**
erodes performance by ~5 percentage points, and a **small frequent-presenter
cohort** consumes disproportionate capacity. Four recommendations follow, each
tied to a measurable target.

---

## Finding 1 — The sickest patients wait the longest

| Triage | Acuity | % within 4hr | Avg ED LOS (min) |
|:-----:|:-------|:-----------:|:----------------:|
| T1 | Resuscitation | **52.6%** | 236 |
| T2 | Emergency | **67.8%** | 212 |
| T3 | Urgent | 85.1% | 178 |
| T4 | Semi-urgent | 97.2% | 129 |
| T5 | Non-urgent | 99.4% | 96 |

The 90% headline is carried by low-acuity patients who are quick to process.
The clinically urgent T1–T2 cohort — where delay carries real risk — sits far
below target.

> **Recommendation.** Report NEAT **stratified by triage**, not as a single
> blended number, and set an internal T1–T2 sub-target of ≥80%. Investigate the
> access-block / bed-availability step that keeps admitted high-acuity patients
> in ED beyond four hours (admission rate is 79% for T1 vs 3% for T5, so T1–T2
> flow is an *inpatient bed* problem, not a triage-speed problem).

## Finding 2 — Winter demand is predictable and under-resourced

| Period | Presentations | % within 4hr |
|:-------|:-------------:|:-----------:|
| Winter (Jun–Aug) | 18,229 | **86.5%** |
| Rest of year | 36,608 | 91.7% |

Winter respiratory demand lifts volume and drops 4-hour performance by
**5.2 percentage points**. This is a recurring, forecastable pattern — not a
surprise.

> **Recommendation.** Pre-load winter capacity: seasonal staffing roster,
> short-stay/observation beds, and a respiratory fast-track from June. A
> LAG()-based month-over-month model (query Q7) gives 4–6 weeks of lead time to
> act on the ramp.

## Finding 3 — Arrivals cluster mid-morning; rosters should follow

Presentations peak **09:00–13:00** (top hour ~3,970 arrivals), yet ambulance
arrivals — the higher-acuity stream — are spread differently. Staffing rostered
to a flat profile leaves the morning peak under-covered.

> **Recommendation.** Align senior-clinician and triage-nurse rostering to the
> hourly arrival curve (dashboard, "Arrivals by hour"). Target the 09:00–13:00
> block first — it is where queueing and LWBS risk compound.

## Finding 4 — A small cohort drives outsized demand

The **top 1% of patients (107 people)** account for **4.9% of all presentations**
— averaging **25 visits/year** and **6.3 chronic conditions** each.

> **Recommendation.** Stand up a **care-coordination / Hospital-in-the-Home**
> pathway for this cohort. Even a 20% reduction in their avoidable presentations
> removes ~540 ED visits per year. Combine with the **28-day readmission** lens
> (11.7% overall, highest in Cardiac & Respiratory at ~12.3%) — the same
> high-comorbidity patients drive both metrics, so one intervention moves two
> KPIs.

---

## Suggested KPI scorecard (for ongoing monitoring)

| KPI | Current | Target | Owner |
|:----|:-------:|:------:|:------|
| NEAT % within 4hr (T1–T2) | ~60% | ≥80% | ED Director |
| LWBS rate | 5.9% | <5% | Nursing Unit Manager |
| 28-day readmission | 11.7% | <10% | Discharge / HITH team |
| Frequent-presenter visits | 4.9% of vol | −20% | Care coordination |

*All recommendations are illustrative, based on synthetic data, and intended to
demonstrate the analytical workflow — not to describe any real health service.*
