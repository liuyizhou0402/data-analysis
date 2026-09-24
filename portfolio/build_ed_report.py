#!/usr/bin/env python3
"""Emergency Department & Patient Flow — portfolio PDF.

Every figure and number here is produced by healthcare-ed-analytics/analysis/eda.py
from the committed synthetic dataset; this script only lays them out.

    python portfolio/build_ed_report.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Spacer, NextPageTemplate

from pdfkit import (Doc, bind_headings, bullets, callout, cover, figure, h1, h2,
                    metric_row, para, rule, table)

PROJ = ROOT / "healthcare-ed-analytics"
FIG = PROJ / "analysis" / "figures"
OUT = ROOT / "portfolio" / "ED_Patient_Flow_Analytics_Yizhou_Liu.pdf"

story = []

# ------------------------------------------------------------------ cover --
story += cover(
    title="Emergency Department<br/>&amp; Patient Flow Analytics",
    subtitle="Why a 90% access target was hiding a clinical-risk problem",
    author="<b>Yizhou Liu</b> &nbsp;·&nbsp; Health Data Analyst &nbsp;·&nbsp; Sydney, Australia",
    stack="SQL (star schema, CTEs, window functions) &nbsp;·&nbsp; Python (pandas, NumPy, matplotlib) "
          "&nbsp;·&nbsp; Power BI + DAX",
    repo="github.com/liuyizhou0402/data-analysis &nbsp;/&nbsp; healthcare-ed-analytics",
    metrics=[("54,837", "ED presentations"), ("11,045", "inpatient admissions"),
             ("14", "analysis figures"), ("7", "SQL business queries")],
    blurb="An end-to-end analytics project built around the metrics Australian health services "
          "actually report — the NEAT 4-hour target, ATS triage performance, left-without-being-seen, "
          "and 28-day readmissions. It runs the full path a health data analyst owns: data model, "
          "SQL, exploratory analysis, dashboard, and costed recommendations a non-technical "
          "executive can act on. The analytical point of the project is that the department's "
          "headline KPI is <b>arithmetically true and operationally misleading</b>, and the work "
          "shows how to prove that and what to do about it.",
)
story += [Spacer(1, 5 * mm)]
story.append(h2("Three headline insights"))
story.append(bullets([
    "<b>The sickest patients wait the longest.</b> Overall 4-hour (NEAT) performance is 90%, but that "
    "blends away the clinical risk: T1 <i>Resuscitation</i> patients meet the target only "
    "<b>52.6%</b> of the time versus <b>99.4%</b> for non-urgent T5.",
    "<b>Winter demand is predictable and under-resourced.</b> Jun–Aug presentations run ~50% higher and "
    "4-hour performance drops <b>5.2 percentage points</b> — a forecastable surge, not a surprise.",
    "<b>A small cohort drives outsized demand.</b> The top <b>1% of patients (107 people)</b> account "
    "for <b>4.9% of all presentations</b>, averaging 25 visits and 6.3 chronic conditions each — a "
    "clear care-coordination target that also moves the readmission rate.",
]))
story += [Spacer(1, 6 * mm)]
story.append(callout(
    "The dataset is <b>synthetic and seed-reproducible</b> (<font face='Courier'>generate_data.py</font>), "
    "modelled on publicly reported Australian ED patterns. No real patient records are used, and no "
    "conclusion here describes a real health service. Synthetic data is a deliberate choice: "
    "patient-level ED data cannot be published, so the project demonstrates method on data that can be.",
    label="On the data &nbsp;"))

story += [NextPageTemplate("body"), PageBreak()]

# -------------------------------------------------------------- the point --
story.append(h1("The finding, in one page"))
story.append(para(
    "The department meets the 4-hour National Emergency Access Target for <b>90% of presentations</b>. "
    "Reported as a single blended number, that reads as a department comfortably in control. "
    "Disaggregated by triage category, it inverts:", "lead"))

story.append(table(
    [["Triage", "Acuity", "% within 4 hr", "Avg ED LOS (min)", "Admission rate"],
     ["T1", "Resuscitation", "52.6%", "236", "~79%"],
     ["T2", "Emergency", "67.8%", "212", "—"],
     ["T3", "Urgent", "85.1%", "178", "—"],
     ["T4", "Semi-urgent", "97.2%", "129", "—"],
     ["T5", "Non-urgent", "99.4%", "96", "~3%"]],
    widths=[18 * mm, 42 * mm, 34 * mm, 38 * mm, 38 * mm],
    align_center_from=2,
    flag_cells={(1, 2), (2, 2)}))
story.append(Spacer(1, 4 * mm))

story.append(para(
    "The 90% is carried by low-acuity patients who are fast to process and rarely admitted. "
    "The clinically urgent T1–T2 cohort — where delay carries real risk — meets the target only "
    "<b>66.5%</b> of the time. The blended KPI does not merely lose detail; it moves in the "
    "opposite direction to the risk it is meant to govern."))

story.append(callout(
    "<b>And the cause is not where the KPI points.</b> Admission likelihood runs from ~79% at T1 to "
    "~3% at T5, and median ED length of stay rises monotonically with acuity. The patients breaching "
    "four hours are the ones waiting for an <i>inpatient bed</i>. This is access block, not triage "
    "speed — so the intervention belongs on the ward, not the front door. Three further findings "
    "(a forecastable winter surge, an LWBS rate above target, and a 1% cohort driving 5% of demand) "
    "are developed in the report that follows.",
    label="So what &nbsp;"))

story.append(h2("Contents"))
story.append(bullets([
    "<b>Summary dashboard</b> — the whole department on one page",
    "<b>1. Demand</b> — volume, seasonality, acuity mix, and the hour × day signature",
    "<b>2. Access &amp; timeliness</b> — the 4-hour target, and where it breaks",
    "<b>3. Arrival patterns</b> — matching rosters to the curve",
    "<b>4. Quality</b> — patients who leave without being seen",
    "<b>5. Admissions &amp; inpatient flow</b> — the bed-access bottleneck",
    "<b>6. Readmissions</b> — 28-day, by diagnosis group",
    "<b>7. High utilisers</b> — concentration of demand",
    "<b>8. Recommendations</b> — four costed actions and a KPI scorecard",
    "<b>Appendix</b> — data model, SQL techniques, reproduction steps, limitations",
]))

story.append(PageBreak())

# --------------------------------------------------------------- dashboard --
story.append(h1("Summary dashboard"))
story.append(para(
    "Rendered from the dataset by <font face='Courier'>analysis/build_dashboard.py</font> "
    "(Python + matplotlib). A step-by-step Power BI build guide with all DAX measures reproduces "
    "the same views as an interactive <font face='Courier'>.pbix</font> — the repository carries "
    "both so the work is portable to whichever BI stack a team already runs."))
story.append(figure(str(PROJ / "dashboard" / "ed_performance_dashboard.png"),
                    max_h_mm=178))
story.append(PageBreak())

# ------------------------------------------------------------------ §1 ----
story.append(h1("1. Demand — how much, and when"))
story.append(figure(str(FIG / "01_daily_volume.png"),
                    "Daily presentations with a 7-day moving average.", max_h_mm=62))
story.append(para(
    "Presentations average ~150/day but swing seasonally. The 7-day average makes a "
    "<b>winter surge (Jun–Aug)</b> unmistakable — demand rises roughly 50% above the summer "
    "baseline. Because it is seasonal and recurring, it is <i>plannable</i>."))

story.append(figure(str(FIG / "02_monthly_vs_target.png"),
                    "Monthly volume against 4-hour target performance.", max_h_mm=62))
story.append(para(
    "Overlaying monthly volume with 4-hour performance shows the two move in opposition: as winter "
    "volume climbs, the share of patients seen within four hours falls below the 81% benchmark. "
    "Demand is the lever on performance — which is what makes the surge worth pre-empting rather "
    "than absorbing."))

story.append(figure(str(FIG / "03_triage_mix.png"),
                    "Presentation mix by ATS triage category.", max_h_mm=62))
story.append(para(
    "The acuity mix is typical of a mixed metropolitan ED: <b>~75% of presentations are lower-acuity "
    "(T4–T5)</b>, while the smaller high-acuity group (T1–T2, ~11%) drives most of the clinical risk "
    "and nearly all inpatient demand. That asymmetry is exactly why a volume-weighted KPI flatters "
    "the department."))

story.append(figure(str(FIG / "08_demand_heatmap.png"),
                    "Presentations by hour of day × day of week.", max_h_mm=72))
story.append(para(
    "Demand concentrates <b>09:00–20:00 on weekdays</b>, peaking mid-morning; overnight "
    "(00:00–06:00) is consistently quiet. This hour × day signature is the basis for demand-matched "
    "rostering in §3."))


# ------------------------------------------------------------------ §2 ----
story.append(h1("2. Access &amp; timeliness — the 4-hour target"))
story.append(figure(str(FIG / "04_target_by_triage.png"),
                    "NEAT 4-hour compliance by triage category — the headline finding.",
                    max_h_mm=64))
story.append(para(
    "<b>The headline finding, restated against the chart.</b> Overall compliance is 90%; T1 "
    "resuscitation patients meet it only <b>52.6%</b> of the time, against 99.4% for non-urgent T5. "
    "Reported as one number, the KPI hides a clinical-risk problem in precisely the patients who "
    "matter most."))

story.append(figure(str(FIG / "05_los_distribution.png"),
                    "Distribution of ED length of stay against the 240-minute line.", max_h_mm=60))
story.append(para(
    "Most stays cluster under the 240-minute line, but a meaningful right tail breaches it. Those "
    "breaches are not randomly distributed — they concentrate in high-acuity, admitted patients."))

story.append(figure(str(FIG / "06_los_by_triage.png"),
                    "Median ED length of stay by triage category.", max_h_mm=64))
story.append(para(
    "Median ED length of stay rises monotonically with acuity: T1–T2 patients sit near or beyond the "
    "4-hour line while T4–T5 clear quickly. Since high-acuity patients are also the most likely to be "
    "admitted (§5), this points to <b>access block — inpatient bed availability</b> — rather than "
    "triage speed as the binding constraint."))

story.append(callout(
    "This is the analytical hinge of the project. Two facts that each look like an ED performance "
    "story — high-acuity patients breach, and high-acuity patients stay longest — only resolve once "
    "the admission rate is brought alongside them. The bottleneck sits downstream of the department "
    "being measured. An ED-side intervention (more triage nurses, faster streaming) would spend real "
    "money against the wrong constraint.",
    label="Why this matters for the recommendation &nbsp;"))


# ------------------------------------------------------------------ §3 ----
story.append(h1("3. Arrival patterns &amp; staffing"))
story.append(figure(str(FIG / "07_arrivals_by_hour.png"),
                    "Arrivals by hour of day.", max_h_mm=62))
story.append(para(
    "Arrivals ramp from ~07:00, peak <b>09:00–13:00</b> (top hour ~3,970 arrivals), and taper through "
    "the evening. Rostering senior decision-makers to this curve — rather than to a flat shift "
    "pattern — is the cheapest available lever on flow, because it requires no additional headcount."))

story.append(figure(str(FIG / "09_ambulance_by_triage.png"),
                    "Ambulance arrival share by triage category.", max_h_mm=62))
story.append(para(
    "Ambulance share climbs steeply with acuity: <b>~85% of T1 arrivals</b> come by ambulance versus "
    "a small fraction of T5. Ambulance arrival is therefore a usable real-time proxy for incoming "
    "high-acuity load — and, given §2, for ramping and access-block risk a few hours ahead."))


# ------------------------------------------------------------------ §4-5 --
story.append(h1("4. Quality — patients who leave"))
story.append(figure(str(FIG / "10_lwbs_by_group.png"),
                    "Left-without-being-seen rate by presenting group.", max_h_mm=64))
story.append(para(
    "<b>Left-without-being-seen (LWBS)</b> averages <b>5.9%</b>, above the &lt;5% quality target. It "
    "concentrates in lower-acuity presenting groups (Neurological, Other, Injury) that wait longest "
    "when the department is busy. LWBS is both a patient-safety signal and an access-equity one: the "
    "patients absorbing the queue are the patients the blended KPI counts as successes."))

story.append(h1("5. Admissions &amp; inpatient flow"))
story.append(figure(str(FIG / "11_admission_by_triage.png"),
                    "Probability of admission by triage category.", max_h_mm=62))
story.append(para(
    "Admission likelihood scales sharply with acuity — <b>~79% for T1 down to ~3% for T5</b>. This is "
    "the mechanism behind §2: high-acuity patients breach four hours because they need an inpatient "
    "bed, and that depends on ward discharge flow, not on the ED front door."))

story.append(figure(str(FIG / "12_inpatient_los.png"),
                    "Inpatient length-of-stay distribution.", max_h_mm=62))
story.append(para(
    "Inpatient length of stay is right-skewed with a <b>median of 6.5 days</b> and a long tail of "
    "complex, longer-stay patients — the cohort where discharge planning and step-down capacity pay "
    "off most, and the lever that actually moves the T1–T2 access figure."))

story.append(h1("6. Readmissions"))
story.append(figure(str(FIG / "13_readmission_by_dx.png"),
                    "28-day readmission rate by diagnosis group.", max_h_mm=62))
story.append(para(
    "<b>28-day readmission</b> averages <b>11.7%</b>, highest in <b>Cardiac and Respiratory (~12.3%)</b> "
    "— the classic chronic-disease groups where discharge quality, follow-up and community care "
    "determine whether a patient returns."))

story.append(h1("7. High utilisers"))
story.append(figure(str(FIG / "14_frequent_presenters_pareto.png"),
                    "Pareto curve — share of presentations by patient percentile.", max_h_mm=64))
story.append(para(
    "Demand is concentrated: the <b>top 1% of patients (107 people)</b> account for <b>4.9% of all "
    "presentations</b>, averaging 25 visits and 6.3 chronic conditions each. This is the same "
    "high-comorbidity cohort that drives the readmission rate in §6 — so a single care-coordination "
    "intervention moves two KPIs at once, which is what makes it the cheapest of the four "
    "recommendations to justify."))

story.append(h2("What the whole analysis says"))
story.append(table(
    [["Theme", "Evidence", "So what"],
     ["Blended KPI hides risk", "T1 4-hr = 52.6% vs 90% overall", "Report NEAT <b>by triage</b>"],
     ["Winter is plannable", "−5.2pp performance Jun–Aug", "Pre-load seasonal capacity"],
     ["Bottleneck is beds, not triage", "79% admit rate at T1 drives breaches", "Fix access block / ward flow"],
     ["Small cohort, big demand", "Top 1% of patients = 4.9% of visits", "Care-coordination pathway"]],
    widths=[44 * mm, 62 * mm, 64 * mm], align_center_from=99))

story.append(PageBreak())

# -------------------------------------------------------- recommendations --
story.append(h1("8. Recommendations"))
story.append(para(
    "Four actions, each tied to a specific finding and a measurable target. Costs and impacts are "
    "illustrative — the point is that every recommendation names the evidence it rests on and the "
    "metric that would show it working.", "lead"))

story.append(h2("1 &nbsp;· &nbsp;Report NEAT stratified by triage, and fix access block"))
story.append(para(
    "Replace the blended 4-hour number with a triage-stratified view and set an internal T1–T2 "
    "sub-target of <b>≥80%</b> (currently ~66.5%). Because admission rate is 79% at T1 versus 3% at "
    "T5, direct the operational work at the inpatient bed-access step, not at triage throughput."))

story.append(h2("2 &nbsp;· &nbsp;Pre-load winter capacity"))
story.append(table(
    [["Period", "Presentations", "% within 4 hr"],
     ["Winter (Jun–Aug)", "18,229", "86.5%"],
     ["Rest of year", "36,608", "91.7%"]],
    widths=[70 * mm, 50 * mm, 50 * mm], align_center_from=1, flag_cells={(1, 2)}))
story.append(Spacer(1, 3 * mm))
story.append(para(
    "Winter respiratory demand lifts volume and costs <b>5.2 percentage points</b> of 4-hour "
    "performance. Pre-load a seasonal roster, short-stay/observation beds and a respiratory "
    "fast-track from June. A <font face='Courier'>LAG()</font>-based month-over-month model gives "
    "4–6 weeks of lead time on the ramp."))

story.append(h2("3 &nbsp;· &nbsp;Roster to the arrival curve"))
story.append(para(
    "Align senior-clinician and triage-nurse rostering to the hourly arrival curve, targeting the "
    "<b>09:00–13:00</b> block first — where queueing and LWBS risk compound. No additional headcount "
    "required; this is a redistribution of existing shifts."))

story.append(h2("4 &nbsp;· &nbsp;Care-coordination pathway for frequent presenters"))
story.append(para(
    "Stand up a care-coordination / Hospital-in-the-Home pathway for the top-1% cohort. A 20% "
    "reduction in their avoidable presentations removes <b>~540 ED visits per year</b>. Because the "
    "same cohort drives the 11.7% readmission rate, one intervention moves two KPIs."))

story.append(Spacer(1, 4 * mm))
story.append(h2("KPI scorecard for ongoing monitoring"))
story.append(table(
    [["KPI", "Current", "Target", "Owner"],
     ["NEAT % within 4 hr (T1–T2)", "~66.5%", "≥80%", "ED Director"],
     ["LWBS rate", "5.9%", "&lt;5%", "Nursing Unit Manager"],
     ["28-day readmission", "11.7%", "&lt;10%", "Discharge / HITH team"],
     ["Frequent-presenter visits", "4.9% of volume", "−20%", "Care coordination"]],
    widths=[62 * mm, 30 * mm, 26 * mm, 52 * mm], align_center_from=1))

story.append(PageBreak())

# ------------------------------------------------------------- appendix ----
story.append(h1("Appendix — how it was built"))

story.append(h2("Data model"))
story.append(para(
    "A star schema over three tables: <font face='Courier'>patients</font> (demographics, chronic "
    "condition count), <font face='Courier'>ed_presentations</font> (54,837 rows — arrival mode, "
    "triage category, timestamps, disposition, LWBS flag) and "
    "<font face='Courier'>admissions</font> (11,045 rows — ward, LOS, discharge, readmission link). "
    "DDL and constraints are in <font face='Courier'>sql/01_schema.sql</font>."))

story.append(h2("SQL techniques used"))
story.append(table(
    [["Technique", "Where it earns its place"],
     ["Star-schema modelling", "Separates the presentation grain from the patient grain, so "
      "frequent-presenter analysis does not double-count demographics"],
     ["CTEs", "Each of the 7 business queries reads as a sequence of named steps rather than "
      "nested subqueries"],
     ["<font face='Courier'>LAG()</font>", "Month-over-month movement for the seasonal model in §1 "
      "and recommendation 2"],
     ["<font face='Courier'>NTILE()</font> + running totals", "Patient value deciles and the Pareto "
      "curve in §7"],
     ["Conditional aggregation", "Triage-stratified compliance in one pass instead of five "
      "filtered queries"],
     ["<font face='Courier'>NULLIF</font>-guarded denominators", "Rate maths that survives an empty "
      "triage-hour cell rather than failing mid-report"]],
    widths=[52 * mm, 118 * mm], align_center_from=99))

story.append(h2("Reproducing the analysis"))
story.append(para(
    "Everything in this document regenerates from the repository in four commands. All randomness is "
    "seeded, so every number above reproduces exactly.", "note"))
story.append(table(
    [["Step", "Command"],
     ["1. Generate the synthetic dataset", "<font face='Courier'>python data/generate_data.py</font>"],
     ["2. Build the SQLite database", "<font face='Courier'>sqlite3 ed.db &lt; sql/01_schema.sql</font>"],
     ["3. Run the 7 business queries", "<font face='Courier'>sqlite3 -header -column ed.db &lt; sql/02_analysis.sql</font>"],
     ["4. Render the 14 figures + dashboard", "<font face='Courier'>python analysis/eda.py &amp;&amp; python analysis/build_dashboard.py</font>"],
     ["5. Rebuild this PDF", "<font face='Courier'>python portfolio/build_ed_report.py</font>"]],
    widths=[62 * mm, 108 * mm], align_center_from=99))

story.append(Spacer(1, 4 * mm))
story.append(h2("What this analysis cannot tell you"))
story.append(bullets([
    "<b>The data is synthetic.</b> It is generated to exhibit realistic ED dynamics and demonstrates "
    "method; no conclusion is a claim about any real health service.",
    "<b>Access block is inferred, not observed.</b> The analysis establishes that high-acuity admitted "
    "patients drive breaches. Proving the bed-availability mechanism needs ward-level occupancy and "
    "bed-request timestamps, which are not in this dataset.",
    "<b>LWBS is a flag, not an outcome.</b> Whether patients who left were subsequently harmed is not "
    "answerable from ED data alone; it requires linked follow-up records.",
    "<b>The winter effect is described, not decomposed.</b> Respiratory presentations rise, but "
    "separating influenza from RSV from cold-weather injury needs coded diagnosis at a finer grain.",
]))

story += rule(6, 4)
story.append(para(
    "Yizhou Liu &nbsp;·&nbsp; github.com/liuyizhou0402/data-analysis &nbsp;·&nbsp; "
    "Full source, SQL, data generator and Power BI build guide in the repository.", "note"))

# ------------------------------------------------------------------ build --
Doc(str(OUT), "Emergency Department & Patient Flow Analytics  ·  Yizhou Liu").build(
    bind_headings(story))
kb = OUT.stat().st_size / 1024
print(f"built  {OUT.name}  {kb:.0f} KB  ({kb/1024:.2f} MB)")
