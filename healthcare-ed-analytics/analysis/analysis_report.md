# Emergency Department & Patient Flow — Analysis Report

A walkthrough of 54,837 ED presentations and 11,045 inpatient admissions
(synthetic, FY2024–25). Every figure is reproduced by
[`eda.py`](eda.py) from the data in [`../data`](../data). Numbers in the text
are computed directly from the dataset.

**Contents**
1. [Demand — how much, and when](#1-demand--how-much-and-when)
2. [Access & timeliness — the 4-hour target](#2-access--timeliness--the-4-hour-target)
3. [Arrival patterns & staffing](#3-arrival-patterns--staffing)
4. [Quality — patients who leave](#4-quality--patients-who-leave)
5. [Admissions & inpatient flow](#5-admissions--inpatient-flow)
6. [Readmissions](#6-readmissions)
7. [High utilisers](#7-high-utilisers)
8. [Conclusions](#8-conclusions)

---

## 1. Demand — how much, and when

![Daily volume](figures/01_daily_volume.png)

Presentations average ~150/day but swing seasonally. The 7-day average makes a
**winter surge (Jun–Aug)** unmistakable — demand rises roughly 50% above the
summer baseline. Because it is seasonal and recurring, it is *plannable*.

![Monthly vs target](figures/02_monthly_vs_target.png)

Overlaying monthly volume with the 4-hour target performance shows the two move
in opposition: as winter volume climbs, the share of patients seen within four
hours **falls below the 81% benchmark**. Demand is the lever on performance.

![Triage mix](figures/03_triage_mix.png)

The acuity mix is typical of a mixed metropolitan ED: **~75% of presentations are
lower-acuity (T4–T5)**, but the smaller high-acuity group (T1–T2, ~11%) drives
most of the clinical risk and inpatient demand (see §5).

![Demand heatmap](figures/08_demand_heatmap.png)

Demand concentrates **09:00–20:00 on weekdays**, peaking mid-morning. Overnight
(00:00–06:00) is consistently quiet. This hour × day signature is the basis for
demand-matched rostering.

## 2. Access & timeliness — the 4-hour target

![Target by triage](figures/04_target_by_triage.png)

**The headline finding.** Overall 4-hour performance is 90%, but broken down by
acuity it inverts: **T1 resuscitation patients are seen within four hours only
53% of the time**, versus 99% for non-urgent T5. Reported as one blended number,
the KPI *hides* a clinical-risk problem in exactly the patients who matter most.
The combined T1–T2 figure is **66.5%**.

![LOS distribution](figures/05_los_distribution.png)

Most stays cluster under the 240-minute line, but a meaningful right tail breaches
it. Those breaches are not random — they concentrate in high-acuity, admitted
patients (next figure).

![LOS by triage](figures/06_los_by_triage.png)

Median ED length of stay rises monotonically with acuity: T1–T2 patients sit near
or beyond the 4-hour line, while T4–T5 clear quickly. Since high-acuity patients
are also the most likely to be admitted (§5), this points to **access block /
inpatient bed availability**, not triage speed, as the bottleneck.

## 3. Arrival patterns & staffing

![Arrivals by hour](figures/07_arrivals_by_hour.png)

Arrivals ramp from ~07:00, peak **09:00–13:00**, and taper through the evening.
Rostering senior decision-makers to this curve — rather than a flat shift
pattern — is the cheapest lever on flow.

![Ambulance by triage](figures/09_ambulance_by_triage.png)

Ambulance share climbs steeply with acuity: **~85% of T1** arrivals are by
ambulance versus a small fraction of T5. Ambulance arrival is therefore a useful
real-time proxy for incoming high-acuity load and ramping risk.

## 4. Quality — patients who leave

![LWBS by group](figures/10_lwbs_by_group.png)

**Left-without-being-seen (LWBS)** averages 5.9% — above the <5% quality target.
It is concentrated in lower-acuity presenting groups (Neurological, Other,
Injury) that wait longest when the department is busy. LWBS is both a patient-
safety and an access-equity signal.

## 5. Admissions & inpatient flow

![Admission by triage](figures/11_admission_by_triage.png)

Admission likelihood scales sharply with acuity — **~79% for T1 down to ~3% for
T5**. This is why the 4-hour breaches sit with high-acuity patients: they need an
inpatient bed, and flow depends on the *ward*, not the ED front door.

![Inpatient LOS](figures/12_inpatient_los.png)

Inpatient length of stay is right-skewed with a **median of 6.5 days** and a long
tail of complex, longer-stay patients — the cohort where discharge planning and
step-down capacity pay off most.

## 6. Readmissions

![Readmission by diagnosis](figures/13_readmission_by_dx.png)

**28-day readmission** averages 11.7%, highest in **Cardiac and Respiratory**
(~12.3%). These are the classic chronic-disease groups where discharge quality,
follow-up, and community care most affect whether a patient comes back.

## 7. High utilisers

![Frequent presenters](figures/14_frequent_presenters_pareto.png)

Demand is concentrated: the **top 1% of patients account for 5.0% of all
presentations**, averaging 25 visits and 6.3 chronic conditions each. The same
high-comorbidity cohort drives readmissions (§6), so a single care-coordination
intervention moves two KPIs at once.

## 8. Conclusions

| Theme | Evidence | So what |
|:------|:---------|:--------|
| Blended KPI hides risk | T1 4-hr = 53% vs 90% overall | Report NEAT **by triage** |
| Winter is plannable | −5.2pp performance Jun–Aug | Pre-load seasonal capacity |
| Bottleneck is beds, not triage | admit rate 79% (T1) drives breaches | Fix access block / bed flow |
| Small cohort, big demand | top 1% = 5% of visits | Care-coordination pathway |

Four costed recommendations with a KPI scorecard →
[**docs/business_recommendations.md**](../docs/business_recommendations.md)

---

*Synthetic data for portfolio demonstration — no real patient records. Metrics
modelled on publicly reported Australian ED indicators.*
