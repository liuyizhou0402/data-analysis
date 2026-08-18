-- ===========================================================================
-- Schema: advertising revenue & sales performance
--
-- Engine: DuckDB (analytical, zero-config, reads CSV natively).
-- The SQL is standard enough to port to Postgres/Snowflake/BigQuery with only
-- minor changes; DuckDB-specific syntax is flagged where used.
--
--   Run:  duckdb ads.duckdb < sql/01_schema.sql
--   or:   python analysis/run_analysis.py   (does this for you)
--
-- Star schema: one fact table at campaign-day grain, three dimensions.
--
--   dim_sales_rep ──┐
--                   ├── dim_advertiser ──┐
--                   ┘                    ├── fact_daily_performance
--                        dim_campaign ───┘
-- ===========================================================================

DROP TABLE IF EXISTS fact_daily_performance;
DROP TABLE IF EXISTS dim_campaign;
DROP TABLE IF EXISTS dim_advertiser;
DROP TABLE IF EXISTS dim_sales_rep;


-- ---------------------------------------------------------------------------
-- Dimensions
-- ---------------------------------------------------------------------------

CREATE TABLE dim_sales_rep (
    rep_id      VARCHAR PRIMARY KEY,
    rep_name    VARCHAR NOT NULL,
    region      VARCHAR NOT NULL,
    seniority   VARCHAR NOT NULL,   -- Associate | Account Manager | Senior Account Manager
    hire_date   DATE    NOT NULL
);

CREATE TABLE dim_advertiser (
    advertiser_id   VARCHAR PRIMARY KEY,
    advertiser_name VARCHAR NOT NULL,
    region          VARCHAR NOT NULL,
    vertical        VARCHAR NOT NULL,
    account_tier    VARCHAR NOT NULL,   -- SMB | Mid-Market | Enterprise
    signup_date     DATE    NOT NULL,
    rep_id          VARCHAR NOT NULL REFERENCES dim_sales_rep(rep_id),
    -- NULL means still active at the end of the observation window. Every
    -- retention query below depends on that convention.
    churn_date      DATE
);

CREATE TABLE dim_campaign (
    campaign_id   VARCHAR PRIMARY KEY,
    advertiser_id VARCHAR NOT NULL REFERENCES dim_advertiser(advertiser_id),
    objective     VARCHAR NOT NULL,   -- Conversions | App Installs | Traffic | Video Views | Reach
    start_date    DATE    NOT NULL,
    end_date      DATE    NOT NULL
);


-- ---------------------------------------------------------------------------
-- Fact: one row per campaign per delivering day
--
-- Grain note: a campaign does not necessarily have a row for every day between
-- its start and end dates -- budget pacing and pauses mean some days do not
-- deliver. Any query that needs a continuous daily series must therefore build
-- a date spine rather than assume one row per campaign-day.
-- ---------------------------------------------------------------------------

CREATE TABLE fact_daily_performance (
    date               DATE    NOT NULL,
    campaign_id        VARCHAR NOT NULL REFERENCES dim_campaign(campaign_id),
    advertiser_id      VARCHAR NOT NULL REFERENCES dim_advertiser(advertiser_id),
    impressions        BIGINT  NOT NULL,
    clicks             BIGINT  NOT NULL,
    conversions        BIGINT  NOT NULL,
    spend_usd          DECIMAL(12, 2) NOT NULL,  -- advertiser spend = platform revenue
    attributed_gmv_usd DECIMAL(14, 2) NOT NULL   -- merchandise value attributed to the ads
);


-- ---------------------------------------------------------------------------
-- Load from CSV. read_csv_auto is DuckDB-specific; the Postgres equivalent is
-- COPY ... FROM ... WITH (FORMAT csv, HEADER true).
-- ---------------------------------------------------------------------------

INSERT INTO dim_sales_rep
    SELECT * FROM read_csv_auto('data/sales_reps.csv');

INSERT INTO dim_advertiser
    SELECT advertiser_id, advertiser_name, region, vertical, account_tier,
           signup_date, rep_id, churn_date
    FROM read_csv_auto('data/advertisers.csv');

INSERT INTO dim_campaign
    SELECT * FROM read_csv_auto('data/campaigns.csv');

INSERT INTO fact_daily_performance
    SELECT * FROM read_csv_auto('data/daily_performance.csv');


-- ---------------------------------------------------------------------------
-- A denormalised view. Every analysis query starts here, so the joins and the
-- guarded rate calculations are written once.
--
-- NULLIF guards every denominator: a campaign-day with impressions but zero
-- clicks is normal, and an unguarded clicks/impressions ratio would divide by
-- zero somewhere in 195k rows.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE VIEW v_performance AS
SELECT
    f.date,
    DATE_TRUNC('month', f.date)          AS month,
    f.campaign_id,
    c.objective,
    f.advertiser_id,
    a.advertiser_name,
    a.region,
    a.vertical,
    a.account_tier,
    a.signup_date,
    a.churn_date,
    DATE_TRUNC('month', a.signup_date)   AS cohort_month,
    r.rep_id,
    r.rep_name,
    r.seniority,
    r.hire_date,
    f.impressions,
    f.clicks,
    f.conversions,
    f.spend_usd,
    f.attributed_gmv_usd
FROM fact_daily_performance f
JOIN dim_campaign   c ON c.campaign_id   = f.campaign_id
JOIN dim_advertiser a ON a.advertiser_id = f.advertiser_id
JOIN dim_sales_rep  r ON r.rep_id        = a.rep_id;
