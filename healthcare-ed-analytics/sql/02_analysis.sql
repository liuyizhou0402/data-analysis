-- =====================================================================
-- Emergency Department & Patient Flow Analytics — Business Queries
-- =====================================================================
-- Each query answers a question a health-service planning / performance
-- team actually asks. Written for SQLite/PostgreSQL. Where date handling
-- differs, the SQLite form is shown and the PostgreSQL form noted inline.
-- =====================================================================


-- ---------------------------------------------------------------------
-- Q1. Monthly ED presentation volume & 4-hour (NEAT) target performance
--     "Are we keeping up with demand, and are patients moving through
--      within the 4-hour national target?"
-- Skills: date bucketing, conditional aggregation (AVG of a 0/1 flag).
-- ---------------------------------------------------------------------
SELECT
    strftime('%Y-%m', arrival_datetime)                 AS month,     -- PG: to_char(arrival_datetime,'YYYY-MM')
    COUNT(*)                                             AS presentations,
    ROUND(AVG(ed_los_minutes), 0)                        AS avg_los_min,
    ROUND(100.0 * AVG(met_4hr_target), 1)                AS pct_within_4hr,
    ROUND(100.0 * AVG(left_without_being_seen), 2)       AS pct_lwbs
FROM ed_presentations
GROUP BY month
ORDER BY month;


-- ---------------------------------------------------------------------
-- Q2. Performance by triage acuity vs the ATS recommended assessment time
--     "Which acuity groups are we failing, and does the sickest cohort
--      wait longest?"  (The 4-hour target and quality risk concentrate in
--      higher-acuity patients.)
-- Skills: CASE mapping, multi-metric aggregation, ordering.
-- ---------------------------------------------------------------------
SELECT
    triage_category,
    CASE triage_category
        WHEN 1 THEN 'T1 Resuscitation'
        WHEN 2 THEN 'T2 Emergency'
        WHEN 3 THEN 'T3 Urgent'
        WHEN 4 THEN 'T4 Semi-urgent'
        ELSE        'T5 Non-urgent'
    END                                                  AS acuity,
    COUNT(*)                                             AS presentations,
    ROUND(AVG(ed_los_minutes), 0)                        AS avg_los_min,
    ROUND(100.0 * AVG(met_4hr_target), 1)                AS pct_within_4hr,
    ROUND(100.0 * AVG(admitted), 1)                      AS admission_rate
FROM ed_presentations
GROUP BY triage_category
ORDER BY triage_category;


-- ---------------------------------------------------------------------
-- Q3. Hourly arrival profile by arrival mode — a staffing view
--     "When do patients arrive, and when do ambulances peak, so we can
--      roster to demand?"
-- Skills: hour extraction, pivot via conditional SUM.
-- ---------------------------------------------------------------------
SELECT
    CAST(strftime('%H', arrival_datetime) AS INTEGER)    AS hour_of_day,  -- PG: EXTRACT(HOUR FROM arrival_datetime)
    COUNT(*)                                             AS total_arrivals,
    SUM(CASE WHEN arrival_mode = 'Ambulance' THEN 1 ELSE 0 END) AS ambulance,
    SUM(CASE WHEN arrival_mode = 'Self'      THEN 1 ELSE 0 END) AS self_present
FROM ed_presentations
GROUP BY hour_of_day
ORDER BY hour_of_day;


-- ---------------------------------------------------------------------
-- Q4. Left-Without-Being-Seen (LWBS) hotspots — a quality/access metric
--     "Which low-acuity groups walk out when the department is busy?"
-- Skills: filtering, ratio of flags, HAVING on volume.
-- ---------------------------------------------------------------------
SELECT
    presenting_group,
    COUNT(*)                                             AS presentations,
    SUM(left_without_being_seen)                         AS lwbs_count,
    ROUND(100.0 * AVG(left_without_being_seen), 2)       AS lwbs_rate_pct
FROM ed_presentations
GROUP BY presenting_group
HAVING COUNT(*) > 500
ORDER BY lwbs_rate_pct DESC;


-- ---------------------------------------------------------------------
-- Q5. 28-day readmission rate by diagnosis group (with avg inpatient LOS)
--     "Where are avoidable readmissions concentrated? These drive cost
--      and signal discharge-quality problems."
-- Skills: aggregation on the admissions fact, rate + LOS side by side.
-- ---------------------------------------------------------------------
SELECT
    diagnosis_group,
    COUNT(*)                                             AS admissions,
    ROUND(AVG(los_days), 1)                              AS avg_los_days,
    SUM(readmitted_28d)                                  AS readmissions,
    ROUND(100.0 * AVG(readmitted_28d), 1)                AS readmission_rate_pct
FROM admissions
GROUP BY diagnosis_group
ORDER BY readmission_rate_pct DESC;


-- ---------------------------------------------------------------------
-- Q6. Frequent presenters ("high utilisers") — top 1% of patients by visits
--     "A small cohort drives a large share of demand; who are they and
--      how much volume do they represent?"  Candidate for care-coordination.
-- Skills: CTE, window function (running share), ranking.
-- ---------------------------------------------------------------------
WITH visits_per_patient AS (
    SELECT patient_id, COUNT(*) AS visits
    FROM ed_presentations
    GROUP BY patient_id
),
ranked AS (
    SELECT
        v.patient_id,
        v.visits,
        p.age,
        p.chronic_conditions,
        NTILE(100) OVER (ORDER BY v.visits) AS visit_percentile
    FROM visits_per_patient v
    JOIN patients p ON p.patient_id = v.patient_id
)
SELECT
    'Top 1% of patients' AS cohort,
    COUNT(*)                                             AS n_patients,
    SUM(visits)                                          AS total_visits,
    ROUND(AVG(visits), 1)                                AS avg_visits,
    ROUND(AVG(chronic_conditions), 1)                    AS avg_comorbidities,
    ROUND(100.0 * SUM(visits) /
          (SELECT COUNT(*) FROM ed_presentations), 1)    AS pct_of_all_visits
FROM ranked
WHERE visit_percentile = 100;


-- ---------------------------------------------------------------------
-- Q7. Month-over-month change in presentation volume (seasonality signal)
--     "Quantify the winter surge so bed & staffing plans can pre-empt it."
-- Skills: CTE + LAG() window function for period-over-period growth.
-- ---------------------------------------------------------------------
WITH monthly AS (
    SELECT strftime('%Y-%m', arrival_datetime) AS month, COUNT(*) AS presentations
    FROM ed_presentations
    GROUP BY month
)
SELECT
    month,
    presentations,
    presentations - LAG(presentations) OVER (ORDER BY month)      AS mom_change,
    ROUND(100.0 * (presentations - LAG(presentations) OVER (ORDER BY month))
          / LAG(presentations) OVER (ORDER BY month), 1)          AS mom_pct
FROM monthly
ORDER BY month;
