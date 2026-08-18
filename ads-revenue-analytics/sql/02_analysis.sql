-- ===========================================================================
-- Business analysis: 12 questions an ads sales organisation actually asks.
--
-- Each block is a self-contained query answering one question, ordered the way
-- a monthly business review runs: what happened -> why -> who -> what next.
--
-- Techniques used across the file: chained CTEs, LAG/LEAD, SUM/AVG OVER,
-- RANK/ROW_NUMBER/NTILE, conditional aggregation, cohort self-joins, date
-- spines, and NULLIF-guarded rate maths.
--
--   Run:  duckdb ads.duckdb < sql/02_analysis.sql
--   or:   python analysis/run_analysis.py   (runs each block, writes CSVs)
-- ===========================================================================


-- ---------------------------------------------------------------------------
-- Q1. Executive summary — headline KPIs for the most recent full month,
--     with month-over-month movement.
--
-- LAG over an ordered monthly aggregate is the cheapest way to get MoM without
-- a self-join. The CASE guards the first month, where LAG returns NULL.
-- ---------------------------------------------------------------------------
WITH monthly AS (
    SELECT
        month,
        SUM(spend_usd)                      AS revenue,
        SUM(attributed_gmv_usd)             AS gmv,
        SUM(impressions)                    AS impressions,
        SUM(clicks)                         AS clicks,
        SUM(conversions)                    AS conversions,
        COUNT(DISTINCT advertiser_id)       AS active_advertisers
    FROM v_performance
    GROUP BY month
),
with_movement AS (
    SELECT
        month,
        revenue,
        LAG(revenue) OVER (ORDER BY month)  AS prev_revenue,
        active_advertisers,
        LAG(active_advertisers) OVER (ORDER BY month) AS prev_advertisers,
        gmv / NULLIF(revenue, 0)            AS roas,
        clicks::DOUBLE / NULLIF(impressions, 0) AS ctr,
        conversions::DOUBLE / NULLIF(clicks, 0) AS cvr,
        revenue / NULLIF(conversions, 0)    AS cpa,
        revenue / NULLIF(active_advertisers, 0) AS arpa
    FROM monthly
)
SELECT
    month,
    ROUND(revenue, 0)                                        AS revenue_usd,
    ROUND(100.0 * (revenue - prev_revenue)
          / NULLIF(prev_revenue, 0), 1)                      AS revenue_mom_pct,
    active_advertisers,
    active_advertisers - prev_advertisers                    AS advertiser_delta,
    ROUND(arpa, 0)                                           AS revenue_per_advertiser,
    ROUND(roas, 2)                                           AS roas,
    ROUND(100 * ctr, 2)                                      AS ctr_pct,
    ROUND(100 * cvr, 2)                                      AS cvr_pct,
    ROUND(cpa, 2)                                            AS cpa_usd
FROM with_movement
ORDER BY month;


-- ---------------------------------------------------------------------------
-- Q2. Revenue trend with running total and a 3-month moving average.
--
-- The moving average smooths the Q4 spike so the underlying trend is legible.
-- ROWS BETWEEN 2 PRECEDING AND CURRENT ROW is the explicit frame -- without it
-- the default frame (RANGE UNBOUNDED PRECEDING) would give a running mean,
-- which is a different and usually unintended statistic.
-- ---------------------------------------------------------------------------
WITH monthly AS (
    SELECT month, SUM(spend_usd) AS revenue
    FROM v_performance
    GROUP BY month
)
SELECT
    month,
    ROUND(revenue, 0)                                          AS revenue_usd,
    ROUND(AVG(revenue) OVER (ORDER BY month
          ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0)        AS revenue_3mo_avg,
    ROUND(SUM(revenue) OVER (ORDER BY month), 0)               AS revenue_cumulative,
    ROUND(100.0 * revenue / SUM(revenue) OVER (), 2)           AS pct_of_total_period
FROM monthly
ORDER BY month;


-- ---------------------------------------------------------------------------
-- Q3. REVENUE DIAGNOSIS — the core question.
--
-- Headline revenue grew over the last two quarters. Which region x vertical
-- segments actually drove that, and which ones went backwards while the total
-- was still rising?
--
-- Compares the most recent 3 months against the preceding 3 months, then
-- expresses each segment's change as a share of the total change. A segment
-- can be shrinking meaningfully while the company still reports growth --
-- that is exactly what this finds, and it is invisible in Q1 and Q2.
-- ---------------------------------------------------------------------------
WITH bounds AS (
    SELECT
        MAX(month)                              AS latest_month,
        MAX(month) - INTERVAL 2 MONTH           AS recent_start,
        MAX(month) - INTERVAL 5 MONTH           AS prior_start,
        MAX(month) - INTERVAL 3 MONTH           AS prior_end
    FROM v_performance
),
segment_periods AS (
    SELECT
        p.region,
        p.vertical,
        SUM(CASE WHEN p.month >= b.recent_start
                 THEN p.spend_usd ELSE 0 END)   AS recent_revenue,
        SUM(CASE WHEN p.month >= b.prior_start AND p.month <= b.prior_end
                 THEN p.spend_usd ELSE 0 END)   AS prior_revenue
    FROM v_performance p
    CROSS JOIN bounds b
    WHERE p.month >= b.prior_start
    GROUP BY p.region, p.vertical
),
scored AS (
    SELECT
        region,
        vertical,
        prior_revenue,
        recent_revenue,
        recent_revenue - prior_revenue                          AS abs_change,
        100.0 * (recent_revenue - prior_revenue)
              / NULLIF(prior_revenue, 0)                        AS pct_change,
        -- Each segment's contribution to the company-wide change. Segments
        -- with a negative contribution are dragging the total down.
        100.0 * (recent_revenue - prior_revenue)
              / NULLIF(SUM(recent_revenue - prior_revenue) OVER (), 0)
                                                                AS pct_of_total_change
    FROM segment_periods
)
SELECT
    region,
    vertical,
    ROUND(prior_revenue, 0)      AS prior_3mo_usd,
    ROUND(recent_revenue, 0)     AS recent_3mo_usd,
    ROUND(abs_change, 0)         AS change_usd,
    ROUND(pct_change, 1)         AS change_pct,
    ROUND(pct_of_total_change, 1) AS contribution_to_total_change_pct,
    -- A percentage change is only meaningful on a base worth acting on. A
    -- segment falling from $14k to $0 is -100% and completely irrelevant next
    -- to one falling 34% on a $3.6m base, so materiality gates the flag rather
    -- than the sort -- small segments still appear, they just aren't escalated.
    CASE
        WHEN prior_revenue < 250000            THEN 'Immaterial'
        WHEN pct_change <= -15                 THEN 'DECLINING — investigate'
        WHEN pct_change <    0                 THEN 'Soft'
        WHEN pct_change >   25                 THEN 'Outperforming'
        ELSE 'Stable'
    END                          AS flag
FROM scored
WHERE prior_revenue > 0
ORDER BY abs_change ASC;   -- biggest decliners first: the diagnosis view


-- ---------------------------------------------------------------------------
-- Q4. Advertiser cohort retention (logo retention).
--
-- Groups advertisers by signup month, then measures how many are still
-- spending N months later. Conditional aggregation pivots months-since-signup
-- into columns, which is the shape a retention triangle needs.
--
-- Only cohorts that signed up inside the observation window are included --
-- advertisers who joined before it have no observable month 0 here, and
-- including them would understate early retention.
-- ---------------------------------------------------------------------------
WITH first_month AS (
    SELECT MIN(month) AS window_start FROM v_performance
),
cohorts AS (
    SELECT
        p.advertiser_id,
        p.cohort_month,
        p.month,
        DATE_DIFF('month', p.cohort_month, p.month) AS months_since_signup
    FROM v_performance p
    CROSS JOIN first_month f
    WHERE p.cohort_month >= f.window_start
    GROUP BY p.advertiser_id, p.cohort_month, p.month
),
-- The cohort denominator is every advertiser who SIGNED UP that month, taken
-- from the dimension -- not the count who happened to spend in month 0.
--
-- Basing it on month-0 spenders is the obvious shortcut and it is wrong: an
-- advertiser who signs up on the 28th and whose first campaign delivers in the
-- following month is absent from month 0 but present in month 1, so the ratio
-- exceeds 1. An earlier version of this query reported retention of 117% and
-- 114% for exactly that reason.
cohort_sizes AS (
    SELECT
        DATE_TRUNC('month', a.signup_date) AS cohort_month,
        COUNT(*)                           AS cohort_size
    FROM dim_advertiser a
    CROSS JOIN first_month f
    WHERE DATE_TRUNC('month', a.signup_date) >= f.window_start
    GROUP BY 1
)
-- NOTE ON THE METRIC: this is *activity* retention -- the share of the cohort
-- still spending in month N. It is not "share not yet churned": an advertiser
-- with a gap between campaign flights drops out and can return, so a later
-- month can read higher than an earlier one. That is a property of the
-- definition, not an error.
--
-- Months the cohort has not yet reached return NULL rather than 0. A cohort
-- that signed up three months before the data ends has no month-6 value, and
-- printing 0% there would read as total churn -- the opposite of the truth.
SELECT
    c.cohort_month,
    s.cohort_size,
    CASE WHEN DATE_DIFF('month', c.cohort_month, MAX(w.last_month)) >= 1
         THEN ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.months_since_signup = 1
              THEN c.advertiser_id END) / NULLIF(s.cohort_size, 0), 0) END AS m1_pct,
    CASE WHEN DATE_DIFF('month', c.cohort_month, MAX(w.last_month)) >= 3
         THEN ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.months_since_signup = 3
              THEN c.advertiser_id END) / NULLIF(s.cohort_size, 0), 0) END AS m3_pct,
    CASE WHEN DATE_DIFF('month', c.cohort_month, MAX(w.last_month)) >= 6
         THEN ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.months_since_signup = 6
              THEN c.advertiser_id END) / NULLIF(s.cohort_size, 0), 0) END AS m6_pct,
    CASE WHEN DATE_DIFF('month', c.cohort_month, MAX(w.last_month)) >= 9
         THEN ROUND(100.0 * COUNT(DISTINCT CASE WHEN c.months_since_signup = 9
              THEN c.advertiser_id END) / NULLIF(s.cohort_size, 0), 0) END AS m9_pct
FROM cohorts c
JOIN cohort_sizes s USING (cohort_month)
CROSS JOIN (SELECT MAX(month) AS last_month FROM v_performance) w
GROUP BY c.cohort_month, s.cohort_size
HAVING s.cohort_size >= 5      -- suppress cohorts too small to read
ORDER BY c.cohort_month;


-- ---------------------------------------------------------------------------
-- Q5. Retention and revenue concentration by account tier.
--
-- Logo retention and revenue retention are different questions. SMB churns
-- heavily but contributes a small revenue share, so a headline churn rate
-- that ignores tier will alarm the wrong people.
-- ---------------------------------------------------------------------------
WITH tier_revenue AS (
    SELECT
        account_tier,
        COUNT(DISTINCT advertiser_id) AS advertisers,
        SUM(spend_usd)                AS revenue
    FROM v_performance
    GROUP BY account_tier
),
tier_churn AS (
    SELECT
        account_tier,
        COUNT(*)                                        AS total_accounts,
        SUM(CASE WHEN churn_date IS NOT NULL THEN 1 ELSE 0 END) AS churned_accounts
    FROM dim_advertiser
    GROUP BY account_tier
)
SELECT
    r.account_tier,
    r.advertisers,
    ROUND(r.revenue, 0)                                         AS revenue_usd,
    ROUND(100.0 * r.revenue / SUM(r.revenue) OVER (), 1)        AS pct_of_revenue,
    ROUND(r.revenue / NULLIF(r.advertisers, 0), 0)              AS revenue_per_advertiser,
    c.churned_accounts,
    ROUND(100.0 * c.churned_accounts
          / NULLIF(c.total_accounts, 0), 1)                     AS churn_rate_pct
FROM tier_revenue r
JOIN tier_churn c USING (account_tier)
ORDER BY revenue_usd DESC;


-- ---------------------------------------------------------------------------
-- Q6. Advertiser value distribution — deciles and a Pareto curve.
--
-- NTILE splits advertisers into revenue deciles; the running share of total
-- revenue shows how concentrated the book is. Concentration is a risk metric:
-- if a handful of accounts carry most of the revenue, losing one is a forecast
-- event, not a rounding error.
-- ---------------------------------------------------------------------------
WITH advertiser_revenue AS (
    SELECT
        advertiser_id,
        advertiser_name,
        account_tier,
        region,
        SUM(spend_usd) AS revenue
    FROM v_performance
    GROUP BY advertiser_id, advertiser_name, account_tier, region
),
deciles AS (
    SELECT
        *,
        NTILE(10) OVER (ORDER BY revenue DESC) AS revenue_decile,
        SUM(revenue) OVER (ORDER BY revenue DESC
              ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_revenue,
        SUM(revenue) OVER ()                                    AS total_revenue
    FROM advertiser_revenue
)
SELECT
    revenue_decile,
    COUNT(*)                                              AS advertisers,
    ROUND(SUM(revenue), 0)                                AS revenue_usd,
    ROUND(100.0 * SUM(revenue) / MAX(total_revenue), 1)   AS pct_of_revenue,
    ROUND(100.0 * MAX(running_revenue) / MAX(total_revenue), 1)
                                                          AS cumulative_pct_of_revenue,
    ROUND(AVG(revenue), 0)                                AS avg_revenue_per_advertiser
FROM deciles
GROUP BY revenue_decile
ORDER BY revenue_decile;


-- ---------------------------------------------------------------------------
-- Q7. Sales rep scorecard.
--
-- Ranks reps on revenue, and compares each against the median of their own
-- region rather than a global average -- regions have very different market
-- sizes, so a global comparison would just rank regions.
--
-- PERCENTILE_CONT is an ordered-set aggregate; used as a window function here
-- to get a per-region median alongside each rep's own row.
-- ---------------------------------------------------------------------------
WITH rep_performance AS (
    SELECT
        p.rep_id,
        p.rep_name,
        p.region,
        p.seniority,
        p.hire_date,
        COUNT(DISTINCT p.advertiser_id) AS accounts_managed,
        SUM(p.spend_usd)                AS revenue,
        SUM(p.attributed_gmv_usd)       AS gmv
    FROM v_performance p
    GROUP BY p.rep_id, p.rep_name, p.region, p.seniority, p.hire_date
),
rep_churn AS (
    SELECT
        rep_id,
        COUNT(*)                                                AS book_size,
        SUM(CASE WHEN churn_date IS NOT NULL THEN 1 ELSE 0 END) AS churned
    FROM dim_advertiser
    GROUP BY rep_id
),
ranked AS (
    SELECT
        rp.*,
        rc.book_size,
        rc.churned,
        100.0 * rc.churned / NULLIF(rc.book_size, 0)      AS churn_rate_pct,
        rp.revenue / NULLIF(rp.accounts_managed, 0)       AS revenue_per_account,
        RANK()       OVER (ORDER BY rp.revenue DESC)      AS revenue_rank_overall,
        RANK()       OVER (PARTITION BY rp.region
                           ORDER BY rp.revenue DESC)      AS revenue_rank_in_region,
        MEDIAN(rp.revenue) OVER (PARTITION BY rp.region)  AS region_median_revenue
    FROM rep_performance rp
    JOIN rep_churn rc USING (rep_id)
)
SELECT
    revenue_rank_overall,
    rep_name,
    region,
    seniority,
    hire_date,
    accounts_managed,
    ROUND(revenue, 0)                                     AS revenue_usd,
    ROUND(revenue_per_account, 0)                         AS revenue_per_account,
    ROUND(churn_rate_pct, 1)                              AS book_churn_pct,
    revenue_rank_in_region,
    ROUND(100.0 * revenue / NULLIF(region_median_revenue, 0) - 100, 0)
                                                          AS pct_vs_region_median
FROM ranked
ORDER BY revenue_rank_overall;


-- ---------------------------------------------------------------------------
-- Q8. New-hire ramp curve.
--
-- How long does a new rep take to reach full productivity? Restricted to reps
-- hired after the window opened, so tenure is measured from a hire date we can
-- actually observe.
--
-- The comparison baseline is the average monthly revenue of tenured reps
-- (hired before the window), which is what "fully ramped" means here.
-- ---------------------------------------------------------------------------
WITH window_start AS (
    SELECT MIN(month) AS m0 FROM v_performance
),
tenured_baseline AS (
    SELECT AVG(monthly_revenue) AS baseline_revenue
    FROM (
        SELECT p.rep_id, p.month, SUM(p.spend_usd) AS monthly_revenue
        FROM v_performance p
        CROSS JOIN window_start w
        WHERE p.hire_date < w.m0
        GROUP BY p.rep_id, p.month
    )
),
new_hire_months AS (
    SELECT
        p.rep_id,
        p.month,
        DATE_DIFF('month', DATE_TRUNC('month', p.hire_date), p.month) AS months_tenure,
        SUM(p.spend_usd) AS monthly_revenue
    FROM v_performance p
    CROSS JOIN window_start w
    WHERE p.hire_date >= w.m0
    GROUP BY p.rep_id, p.month, p.hire_date
)
SELECT
    n.months_tenure,
    COUNT(DISTINCT n.rep_id)                                    AS reps_observed,
    ROUND(AVG(n.monthly_revenue), 0)                            AS avg_monthly_revenue,
    ROUND(MAX(b.baseline_revenue), 0)                           AS tenured_baseline,
    ROUND(100.0 * AVG(n.monthly_revenue)
          / NULLIF(MAX(b.baseline_revenue), 0), 0)              AS pct_of_full_productivity
FROM new_hire_months n
CROSS JOIN tenured_baseline b
WHERE n.months_tenure BETWEEN 0 AND 11
GROUP BY n.months_tenure
ORDER BY n.months_tenure;


-- ---------------------------------------------------------------------------
-- Q9. Does book size hurt retention?
--
-- Two confounds have to be handled or this relationship is misread:
--   (a) reps with very small books have churn rates computed over 1-3 accounts,
--       which is noise, not signal -- so a minimum book size is enforced;
--   (b) book composition varies by tier, and SMB churns far more than
--       Enterprise, so a rep loaded with SMB accounts looks bad for reasons
--       unrelated to book size. The SMB-only column controls for that.
-- ---------------------------------------------------------------------------
WITH rep_books AS (
    SELECT
        rep_id,
        COUNT(*)                                                     AS book_size,
        AVG(CASE WHEN churn_date IS NOT NULL THEN 1.0 ELSE 0.0 END)  AS churn_rate,
        AVG(CASE WHEN account_tier = 'SMB' THEN 1.0 ELSE 0.0 END)    AS smb_share,
        SUM(CASE WHEN account_tier = 'SMB' THEN 1 ELSE 0 END)        AS smb_accounts,
        SUM(CASE WHEN account_tier = 'SMB' AND churn_date IS NOT NULL
                 THEN 1 ELSE 0 END)                                  AS smb_churned
    FROM dim_advertiser
    GROUP BY rep_id
),
bucketed AS (
    SELECT
        CASE
            WHEN book_size <=  8 THEN '1-8 accounts'
            WHEN book_size <= 16 THEN '9-16 accounts'
            ELSE                      '17+ accounts'
        END AS book_size_band,
        book_size, churn_rate, smb_share, smb_accounts, smb_churned
    FROM rep_books
    WHERE book_size >= 4     -- confound (a): drop books too small to measure
)
SELECT
    book_size_band,
    COUNT(*)                                             AS reps,
    ROUND(AVG(book_size), 1)                             AS avg_book_size,
    ROUND(100 * AVG(churn_rate), 1)                      AS avg_book_churn_pct,
    ROUND(100 * AVG(smb_share), 0)                       AS avg_smb_share_pct,
    -- confound (b): churn among SMB accounts only, pooled across the band
    ROUND(100.0 * SUM(smb_churned) / NULLIF(SUM(smb_accounts), 0), 1)
                                                         AS smb_only_churn_pct
FROM bucketed
GROUP BY book_size_band
ORDER BY avg_book_size;


-- ---------------------------------------------------------------------------
-- Q10. Campaign funnel by objective.
--
-- Impressions -> clicks -> conversions, with the efficiency metrics a media
-- buyer reads. Objectives are not comparable on CPA alone: a Reach campaign is
-- not trying to convert, so its CPA is meaningless in isolation. Reporting the
-- whole funnel side by side is what makes the comparison fair.
-- ---------------------------------------------------------------------------
SELECT
    objective,
    COUNT(DISTINCT campaign_id)                                  AS campaigns,
    ROUND(SUM(spend_usd), 0)                                     AS spend_usd,
    ROUND(100.0 * SUM(spend_usd) / SUM(SUM(spend_usd)) OVER (), 1) AS pct_of_spend,
    SUM(impressions)                                             AS impressions,
    ROUND(100.0 * SUM(clicks) / NULLIF(SUM(impressions), 0), 2)  AS ctr_pct,
    ROUND(100.0 * SUM(conversions) / NULLIF(SUM(clicks), 0), 2)  AS cvr_pct,
    ROUND(1000.0 * SUM(spend_usd) / NULLIF(SUM(impressions), 0), 2) AS cpm_usd,
    ROUND(SUM(spend_usd) / NULLIF(SUM(clicks), 0), 2)            AS cpc_usd,
    ROUND(SUM(spend_usd) / NULLIF(SUM(conversions), 0), 2)       AS cpa_usd,
    ROUND(SUM(attributed_gmv_usd) / NULLIF(SUM(spend_usd), 0), 2) AS roas
FROM v_performance
GROUP BY objective
ORDER BY spend_usd DESC;


-- ---------------------------------------------------------------------------
-- Q11. Growth opportunity matrix — where is return high but investment low?
--
-- A vertical with above-average ROAS and below-average spend share is, on the
-- face of it, under-invested: the advertisers there are getting good returns,
-- which usually means they have room to spend more.
-- ---------------------------------------------------------------------------
WITH vertical_stats AS (
    SELECT
        vertical,
        COUNT(DISTINCT advertiser_id)                        AS advertisers,
        SUM(spend_usd)                                       AS revenue,
        SUM(attributed_gmv_usd) / NULLIF(SUM(spend_usd), 0)  AS roas
    FROM v_performance
    GROUP BY vertical
),
benchmarked AS (
    SELECT
        *,
        100.0 * revenue / SUM(revenue) OVER ()  AS spend_share_pct,
        AVG(roas) OVER ()                       AS avg_roas,
        revenue / NULLIF(advertisers, 0)        AS revenue_per_advertiser
    FROM vertical_stats
)
SELECT
    vertical,
    advertisers,
    ROUND(revenue, 0)                    AS revenue_usd,
    ROUND(spend_share_pct, 1)            AS spend_share_pct,
    ROUND(roas, 2)                       AS roas,
    ROUND(revenue_per_advertiser, 0)     AS revenue_per_advertiser,
    CASE
        WHEN roas >= avg_roas AND spend_share_pct < 15 THEN 'GROW — high return, under-invested'
        WHEN roas >= avg_roas                          THEN 'Defend — high return, already scaled'
        WHEN spend_share_pct >= 15                     THEN 'Optimise — large but low return'
        ELSE                                                'Monitor'
    END                                  AS recommended_action
FROM benchmarked
ORDER BY roas DESC;


-- ---------------------------------------------------------------------------
-- Q12. Churn-risk watchlist.
--
-- Flags still-active advertisers whose spend has fallen materially, comparing
-- the most recent 3 months against the 3 before. Declining spend is the
-- earliest observable signal that an account is disengaging, and it is
-- actionable while the account is still open -- which a churn *date* never is.
--
-- WHY 3-MONTH BLOCKS RATHER THAN CONSECUTIVE MONTHS:
-- The obvious version of this query looks for N months of consecutive
-- month-over-month decline. On real campaign data that barely returns
-- anything: advertisers run campaigns in flights with gaps between them, so a
-- month with no delivery is routine scheduling, not disengagement. An earlier
-- version requiring two consecutive declines surfaced 5 accounts totalling
-- $20k of revenue at risk -- too small a list to action and too noisy to
-- trust. Aggregating to quarters absorbs the flight pattern and leaves the
-- trend.
-- ---------------------------------------------------------------------------
WITH bounds AS (
    SELECT
        MAX(month)                    AS latest_month,
        MAX(month) - INTERVAL 2 MONTH AS recent_start,
        MAX(month) - INTERVAL 5 MONTH AS prior_start,
        MAX(month) - INTERVAL 3 MONTH AS prior_end
    FROM v_performance
),
advertiser_periods AS (
    SELECT
        p.advertiser_id,
        p.advertiser_name,
        p.account_tier,
        p.region,
        p.vertical,
        p.rep_name,
        SUM(CASE WHEN p.month >= b.recent_start
                 THEN p.spend_usd ELSE 0 END) AS recent_revenue,
        SUM(CASE WHEN p.month >= b.prior_start AND p.month <= b.prior_end
                 THEN p.spend_usd ELSE 0 END) AS prior_revenue
    FROM v_performance p
    CROSS JOIN bounds b
    WHERE p.churn_date IS NULL          -- still-open accounts only
      AND p.month >= b.prior_start
    GROUP BY p.advertiser_id, p.advertiser_name, p.account_tier, p.region,
             p.vertical, p.rep_name
)
SELECT
    advertiser_name,
    account_tier,
    region,
    vertical,
    rep_name                                                       AS owning_rep,
    ROUND(prior_revenue, 0)                                        AS prior_3mo_usd,
    ROUND(recent_revenue, 0)                                       AS recent_3mo_usd,
    ROUND(100.0 * (recent_revenue - prior_revenue)
          / NULLIF(prior_revenue, 0), 1)                           AS change_pct,
    ROUND(prior_revenue - recent_revenue, 0)                       AS revenue_at_risk_usd,
    CASE
        WHEN recent_revenue = 0            THEN 'Dormant — no spend in 3 months'
        WHEN recent_revenue < prior_revenue * 0.5 THEN 'Severe decline'
        ELSE                                    'Material decline'
    END                                                            AS risk_level
FROM advertiser_periods
WHERE prior_revenue >= 100000                       -- accounts worth a rep's time
  AND recent_revenue < prior_revenue * 0.80         -- 20%+ contraction
ORDER BY revenue_at_risk_usd DESC
LIMIT 25;
