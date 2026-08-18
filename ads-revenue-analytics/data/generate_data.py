"""
Generate a synthetic advertising-business dataset for the GBS-style analysis.

WHY SYNTHETIC
-------------
Real advertiser-level revenue data is commercially confidential and never
public. This generator produces a dataset with the same *shape* and the same
*business dynamics* an ads sales organisation actually sees, so the SQL and
dashboard exercise realistic questions rather than toy ones.

The dataset is not random noise. Six business patterns are deliberately built
in, each of which the analysis in sql/02_analysis.sql is designed to surface:

  1. Q4 seasonality      — Nov/Dec retail peak lifts spend across commerce
                            verticals.
  2. A segment shock     — Gaming in Southeast Asia declines steeply from
                            month 11 onward. Total revenue keeps growing, so
                            this is only visible if you decompose by segment.
                            This is the "diagnose the miss" story.
  3. Tiered churn        — SMB advertisers churn far faster than Enterprise,
                            so logo retention and revenue retention tell
                            different stories.
  4. Rep ramp            — new sales hires reach full productivity over
                            roughly five months.
  5. Book-size penalty   — reps carrying more than ~25 accounts show worse
                            retention on their book.
  6. Under-invested win  — Beauty & Personal Care returns high ROAS on a small
                            share of spend: a growth opportunity.

Everything is seeded, so the numbers in the README and the recommendations
document are exactly reproducible.

    python data/generate_data.py
"""

from __future__ import annotations

import numpy as np
import pandas as pd

SEED = 20260218
rng = np.random.default_rng(SEED)

START = pd.Timestamp("2024-07-01")
END = pd.Timestamp("2025-12-31")
ALL_DAYS = pd.date_range(START, END, freq="D")
N_MONTHS = 18

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

REGIONS = {
    "Southeast Asia":  0.30,
    "Australia & NZ":  0.16,
    "Japan & Korea":   0.15,
    "North America":   0.24,
    "Europe":          0.15,
}

# Vertical -> (share of advertisers, baseline ROAS, spend scale multiplier)
VERTICALS = {
    "E-commerce & Retail":  (0.26, 3.4, 1.35),
    "Gaming":               (0.16, 2.6, 1.20),
    "Beauty & Personal Care": (0.13, 4.6, 0.75),   # story 6: high ROAS, small spend
    "Finance & Fintech":    (0.11, 2.2, 1.10),
    "Travel & Hospitality": (0.10, 3.0, 0.85),
    "Food & Beverage":      (0.10, 2.8, 0.70),
    "Education":            (0.08, 2.4, 0.55),
    "Automotive":           (0.06, 2.0, 0.95),
}

# Tier -> (share, spend multiplier, monthly churn hazard)
TIERS = {
    "SMB":         (0.58, 0.35, 0.075),   # story 3: high churn
    "Mid-Market":  (0.30, 1.60, 0.028),
    "Enterprise":  (0.12, 6.50, 0.008),
}

OBJECTIVES = {
    "Conversions":   (0.40, 0.0145, 0.052),   # (share, base CTR, base CVR)
    "App Installs":  (0.18, 0.0165, 0.068),
    "Traffic":       (0.20, 0.0195, 0.019),
    "Video Views":   (0.13, 0.0240, 0.008),
    "Reach":         (0.09, 0.0090, 0.005),
}

FIRST_NAMES = [
    "Aisha", "Ben", "Chloe", "Daniel", "Elena", "Farid", "Grace", "Hiroshi",
    "Isabel", "Jason", "Kiara", "Liam", "Mei", "Nikhil", "Olivia", "Pedro",
    "Qing", "Ravi", "Sofia", "Tomas", "Uma", "Viktor", "Wendy", "Xin",
    "Yara", "Zach", "Amara", "Bao", "Camila", "Dmitri", "Ethan", "Freya",
    "Gabriel", "Hana", "Ines", "Jonas", "Keiko", "Lucas", "Maya", "Noah",
]
LAST_NAMES = [
    "Abbott", "Bennett", "Chen", "Dawson", "Evans", "Fischer", "Garcia",
    "Hoffman", "Ibrahim", "Jensen", "Kowalski", "Lindqvist", "Moreau",
    "Nakamura", "Oyelaran", "Petrov", "Quintero", "Rossi", "Silva", "Tanaka",
    "Ueda", "Vargas", "Whitfield", "Xu", "Yilmaz", "Zhang", "Almeida",
    "Brennan", "Costa", "Duarte", "Eriksen", "Fontaine", "Grant", "Haddad",
    "Iversen", "Jamil", "Kaur", "Lombardi", "Moreno", "Novak",
]

COMPANY_PREFIX = [
    "Northwind", "Lumen", "Aster", "Vertex", "Cobalt", "Harbour", "Kestrel",
    "Solstice", "Meridian", "Anvil", "Juniper", "Quartz", "Ember", "Beacon",
    "Nimbus", "Sable", "Onyx", "Pinnacle", "Cascade", "Vector", "Halcyon",
    "Ridge", "Zephyr", "Terra", "Lyra", "Onward", "Foundry", "Copper",
    "Delta", "Summit", "Orchid", "Basalt", "Cedar", "Drift", "Lantern",
]
COMPANY_SUFFIX = [
    "Retail", "Studios", "Labs", "Group", "Digital", "Commerce", "Brands",
    "Collective", "Co", "Works", "Interactive", "Partners", "Holdings",
    "Ventures", "Media",
]


def weighted_choice(mapping: dict, n: int) -> np.ndarray:
    keys = list(mapping.keys())
    weights = np.array([
        v[0] if isinstance(v, tuple) else v for v in mapping.values()
    ], dtype=float)
    return rng.choice(keys, size=n, p=weights / weights.sum())


# Regions do not buy the same mix. These multipliers tilt each region's vertical
# distribution away from the global average -- SEA over-indexes on mobile
# gaming, Europe on travel and automotive, and so on.
#
# This is not decoration. Without it, "Southeast Asia x Gaming" is only about
# 5% of advertisers, which is too thin a slice for its monthly revenue to be
# readable: an early version of this generator produced a segment whose month-
# over-month index swung 100 -> 258 -> 34 -> (no data) -> 25, so the decline
# planted in it (story 2) was buried in sampling noise. Concentrating the
# vertical where it realistically concentrates gives the segment enough mass
# to show a trend.
REGION_VERTICAL_TILT = {
    "Southeast Asia":  {"Gaming": 2.80, "E-commerce & Retail": 1.20,
                        "Finance & Fintech": 0.75, "Automotive": 0.55},
    "Japan & Korea":   {"Gaming": 1.55, "Beauty & Personal Care": 1.35,
                        "Automotive": 0.80},
    "North America":   {"Finance & Fintech": 1.35, "E-commerce & Retail": 1.15,
                        "Gaming": 0.70, "Education": 1.10},
    "Europe":          {"Travel & Hospitality": 1.35, "Automotive": 1.30,
                        "Gaming": 0.70},
    "Australia & NZ":  {"E-commerce & Retail": 1.25, "Travel & Hospitality": 1.25,
                        "Gaming": 0.60},
}


def vertical_for_region(region: str) -> str:
    """Draw a vertical using that region's tilted distribution."""
    keys = list(VERTICALS.keys())
    weights = np.array([VERTICALS[k][0] for k in keys], dtype=float)
    tilt = REGION_VERTICAL_TILT.get(region, {})
    weights = weights * np.array([tilt.get(k, 1.0) for k in keys])
    return str(rng.choice(keys, p=weights / weights.sum()))


# ---------------------------------------------------------------------------
# Sales reps
# ---------------------------------------------------------------------------

def build_sales_reps(n: int = 42) -> pd.DataFrame:
    """Reps have staggered hire dates so the ramp curve (story 4) is observable."""
    names = set()
    while len(names) < n:
        names.add(f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}")
    names = sorted(names)

    # Two thirds are tenured (hired before the window opens), one third are
    # hired during the window -- that mix is what makes a ramp curve visible.
    hire_dates = []
    for i in range(n):
        if i < int(n * 0.62):
            hire_dates.append(START - pd.Timedelta(days=int(rng.integers(400, 1800))))
        else:
            hire_dates.append(START + pd.Timedelta(days=int(rng.integers(10, 400))))

    regions = weighted_choice(REGIONS, n)
    seniority = rng.choice(
        ["Associate", "Account Manager", "Senior Account Manager"],
        size=n, p=[0.31, 0.45, 0.24])

    return pd.DataFrame({
        "rep_id": [f"REP{i + 1:03d}" for i in range(n)],
        "rep_name": names,
        "region": regions,
        "seniority": seniority,
        "hire_date": [d.date() for d in hire_dates],
    })


# ---------------------------------------------------------------------------
# Advertisers
# ---------------------------------------------------------------------------

def build_advertisers(reps: pd.DataFrame, n: int = 340) -> pd.DataFrame:
    """Advertisers sign up over time and may churn; SMB churns fastest (story 3)."""
    names = set()
    while len(names) < n:
        names.add(f"{rng.choice(COMPANY_PREFIX)} {rng.choice(COMPANY_SUFFIX)}")
    names = sorted(names)

    regions = weighted_choice(REGIONS, n)
    verticals = np.array([vertical_for_region(r) for r in regions])
    tiers = weighted_choice(TIERS, n)

    # 55% are already active at window open; the rest sign up during it, which
    # is what makes cohort retention analysis meaningful.
    signup_dates = []
    for i in range(n):
        if rng.random() < 0.55:
            signup_dates.append(START - pd.Timedelta(days=int(rng.integers(30, 900))))
        else:
            signup_dates.append(START + pd.Timedelta(days=int(rng.integers(0, 460))))

    # Assign each advertiser to a rep in the same region, weighted by a per-rep
    # "capacity" draw so books are unevenly sized -- which is what real coverage
    # models look like, and what makes book size analysable at all.
    #
    # An even split does not work here: with 340 advertisers over 42 reps, a
    # uniform assignment gives every rep ~8 accounts and a spread far too narrow
    # to relate book size to retention. An earlier version left only two reps
    # above the 25-account threshold this generator was penalising, so story 5
    # rested on a two-rep comparison and had to be either fixed or dropped.
    rep_capacity = {
        rid: float(rng.lognormal(0.0, 0.62))
        for rid in reps["rep_id"]
    }
    rep_ids = []
    for region in regions:
        pool = reps.loc[reps["region"] == region, "rep_id"].to_numpy()
        if len(pool) == 0:
            pool = reps["rep_id"].to_numpy()
        weights = np.array([rep_capacity[r] for r in pool])
        rep_ids.append(rng.choice(pool, p=weights / weights.sum()))

    advertisers = pd.DataFrame({
        "advertiser_id": [f"ADV{i + 1:04d}" for i in range(n)],
        "advertiser_name": names,
        "region": regions,
        "vertical": verticals,
        "account_tier": tiers,
        "signup_date": [d.date() for d in signup_dates],
        "rep_id": rep_ids,
    })

    # ---- churn ----
    # Each advertiser draws a monthly churn hazard from its tier, then we walk
    # months forward until it churns (or survives the window).
    churn_dates = []
    for _, row in advertisers.iterrows():
        hazard = TIERS[row["account_tier"]][2]

        # Story 5: retention degrades progressively as a rep's book grows past
        # the point where they can service it. A smooth penalty rather than a
        # cliff at an arbitrary account count -- the relationship is then
        # detectable as a correlation across all 42 reps instead of depending on
        # how many happen to sit above a hard threshold.
        book_size = int((advertisers["rep_id"] == row["rep_id"]).sum())
        hazard *= 1.0 + 0.055 * max(0, book_size - 8)

        signup = pd.Timestamp(row["signup_date"])
        churn = None
        cursor = max(signup, START)
        while cursor < END:
            cursor = cursor + pd.Timedelta(days=30)
            if rng.random() < hazard:
                churn = cursor
                break
        churn_dates.append(churn.date() if churn is not None and churn < END else None)

    advertisers["churn_date"] = churn_dates
    return advertisers


# ---------------------------------------------------------------------------
# Campaigns
# ---------------------------------------------------------------------------

def build_campaigns(advertisers: pd.DataFrame) -> pd.DataFrame:
    """Tile each advertiser's active life with back-to-back campaign "lanes".

    Managed advertisers run always-on: as one campaign ends the next begins,
    with several running concurrently for larger accounts. Modelling that as
    continuous lanes (rather than scattering N campaigns at random points in
    the advertiser's lifetime) matters for more than realism.

    An earlier version scattered campaigns randomly, which left advertisers
    dark for months at a time. In aggregate that made the number of active
    campaigns in a segment swing by 2-3x month to month, and that composition
    noise completely buried the segment-level trends this dataset exists to
    demonstrate -- the Southeast Asia Gaming decline (story 2) was not merely
    hidden but appeared to *invert*, with the segment indexing at 288 during
    the months its planted shock factor had fallen to 0.74. Continuous lanes
    hold the active-campaign count roughly stable, so a change in spend
    reflects a change in spend rather than a change in how many campaigns
    happened to be scheduled.
    """
    rows = []
    campaign_counter = 1

    for _, adv in advertisers.iterrows():
        tier = adv["account_tier"]
        n_lanes = {
            "SMB": int(rng.integers(1, 3)),
            "Mid-Market": int(rng.integers(2, 4)),
            "Enterprise": int(rng.integers(3, 6)),
        }[tier]

        signup = pd.Timestamp(adv["signup_date"])
        active_to = pd.Timestamp(adv["churn_date"]) if adv["churn_date"] else END

        # Campaigns may begin BEFORE the observation window and still be running
        # when it opens -- an advertiser who joined in 2023 does not pause on
        # 1 July 2024. Allowing this and then clipping to START is what keeps the
        # first month from looking artificially empty: an earlier version began
        # every campaign at or after START, which made July 2024 spend ($2.1M)
        # look like a collapse next to August ($6.3M) purely as a generation
        # artifact rather than a business pattern.
        earliest = min(signup, START - pd.Timedelta(days=120))
        if active_to <= earliest:
            continue

        for _ in range(n_lanes):
            # Stagger each lane's first campaign so lanes don't all flip on the
            # same day, then run campaigns back to back down the lane.
            cursor = earliest + pd.Timedelta(days=int(rng.integers(0, 45)))

            while cursor < active_to:
                duration = int(rng.integers(45, 165))
                c_start = cursor
                c_end = min(c_start + pd.Timedelta(days=duration), active_to)

                visible_start = max(c_start, START)
                visible_end = min(c_end, END)

                if (visible_end - visible_start).days >= 7:
                    rows.append({
                        "campaign_id": f"CMP{campaign_counter:05d}",
                        "advertiser_id": adv["advertiser_id"],
                        "objective": weighted_choice(OBJECTIVES, 1)[0],
                        "start_date": visible_start.date(),
                        "end_date": visible_end.date(),
                    })
                    campaign_counter += 1

                # Short gap between flights, then the next campaign starts.
                cursor = c_end + pd.Timedelta(days=int(rng.integers(0, 18)))
                if visible_start >= END:
                    break

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Daily performance facts
# ---------------------------------------------------------------------------

def seasonality_factor(day: pd.Timestamp) -> float:
    """Q4 retail peak plus a mild weekly cycle (story 1)."""
    month = day.month
    factor = 1.0
    if month == 11:
        factor *= 1.42          # peak shopping build-up
    elif month == 12:
        factor *= 1.30
    elif month in (1, 2):
        factor *= 0.86          # post-holiday trough
    elif month in (6, 7):
        factor *= 1.05
    # Weekends run slightly cheaper/lighter for B2B-managed accounts.
    if day.dayofweek >= 5:
        factor *= 0.92
    return factor


def gaming_sea_shock(day: pd.Timestamp, region: str, vertical: str) -> float:
    """Story 2: SEA Gaming declines steeply from May 2025 onward.

    Total revenue keeps growing over the window, so this is invisible in a
    headline trend and only appears once revenue is decomposed by
    region x vertical. That is the point of the diagnosis query.
    """
    if region != "Southeast Asia" or vertical != "Gaming":
        return 1.0
    shock_start = pd.Timestamp("2025-04-01")
    if day < shock_start:
        return 1.0
    months_in = (day - shock_start).days / 30.0
    # Decays toward ~22% of the original level over ~7 months.
    return float(max(0.22, 1.0 - 0.115 * months_in))


def rep_ramp_factor(day: pd.Timestamp, hire_date: pd.Timestamp) -> float:
    """Story 4: a new rep's book underperforms for roughly five months."""
    months_tenure = (day - hire_date).days / 30.0
    if months_tenure >= 5:
        return 1.0
    if months_tenure < 0:
        return 0.0
    return float(0.35 + 0.13 * months_tenure)


def build_daily_performance(advertisers: pd.DataFrame, campaigns: pd.DataFrame,
                            reps: pd.DataFrame) -> pd.DataFrame:
    adv_lookup = advertisers.set_index("advertiser_id").to_dict("index")
    rep_hire = {r["rep_id"]: pd.Timestamp(r["hire_date"]) for _, r in reps.iterrows()}

    # A stable per-advertiser quality multiplier creates realistic spread:
    # some accounts simply perform better than their segment average.
    adv_quality = {
        aid: float(rng.lognormal(0.0, 0.42))
        for aid in advertisers["advertiser_id"]
    }
    # Per-campaign daily budget scale.
    camp_scale = {
        cid: float(rng.lognormal(0.0, 0.55))
        for cid in campaigns["campaign_id"]
    }

    records = []
    for _, camp in campaigns.iterrows():
        adv = adv_lookup[camp["advertiser_id"]]
        region, vertical, tier = adv["region"], adv["vertical"], adv["account_tier"]
        base_roas = VERTICALS[vertical][1]
        vertical_scale = VERTICALS[vertical][2]
        tier_scale = TIERS[tier][1]
        base_ctr = OBJECTIVES[camp["objective"]][1]
        base_cvr = OBJECTIVES[camp["objective"]][2]
        hire_date = rep_hire.get(adv["rep_id"], START)

        days = pd.date_range(camp["start_date"], camp["end_date"], freq="D")
        # Campaigns don't deliver every single day (budget pacing, pauses).
        active_mask = rng.random(len(days)) < 0.88

        for day, active in zip(days, active_mask):
            if not active:
                continue

            factor = (seasonality_factor(day)
                      * gaming_sea_shock(day, region, vertical)
                      * rep_ramp_factor(day, hire_date))
            if factor <= 0:
                continue

            # ---- spend ----
            base_daily = 780.0 * tier_scale * vertical_scale
            spend = (base_daily
                     * adv_quality[camp["advertiser_id"]]
                     * camp_scale[camp["campaign_id"]]
                     * factor
                     * rng.lognormal(0.0, 0.22))
            spend = float(np.round(max(spend, 12.0), 2))

            # ---- delivery ----
            # CPM varies by region (auction density) and season.
            region_cpm = {
                "North America": 9.4, "Europe": 7.1, "Japan & Korea": 8.2,
                "Australia & NZ": 8.8, "Southeast Asia": 3.6,
            }[region]
            cpm = region_cpm * seasonality_factor(day) * rng.lognormal(0.0, 0.18)
            impressions = int(max(spend / cpm * 1000, 1))

            ctr = base_ctr * rng.lognormal(0.0, 0.22)
            clicks = int(rng.binomial(impressions, min(ctr, 0.35)))

            cvr = base_cvr * rng.lognormal(0.0, 0.28)
            conversions = int(rng.binomial(clicks, min(cvr, 0.6))) if clicks > 0 else 0

            # ---- attributed GMV ----
            roas = base_roas * rng.lognormal(0.0, 0.24)
            attributed_gmv = float(np.round(spend * roas, 2)) if conversions > 0 else 0.0

            records.append((
                day.date(), camp["campaign_id"], camp["advertiser_id"],
                impressions, clicks, conversions, spend, attributed_gmv,
            ))

    return pd.DataFrame(records, columns=[
        "date", "campaign_id", "advertiser_id",
        "impressions", "clicks", "conversions", "spend_usd", "attributed_gmv_usd",
    ])


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    print("Generating sales reps ...")
    reps = build_sales_reps()

    print("Generating advertisers ...")
    advertisers = build_advertisers(reps)

    print("Generating campaigns ...")
    campaigns = build_campaigns(advertisers)

    print("Generating daily performance (this is the slow part) ...")
    performance = build_daily_performance(advertisers, campaigns, reps)

    here = __file__.rsplit("/", 1)[0]
    reps.to_csv(f"{here}/sales_reps.csv", index=False)
    advertisers.to_csv(f"{here}/advertisers.csv", index=False)
    campaigns.to_csv(f"{here}/campaigns.csv", index=False)
    performance.to_csv(f"{here}/daily_performance.csv", index=False)

    print()
    print(f"  sales_reps.csv        {len(reps):>8,} rows")
    print(f"  advertisers.csv       {len(advertisers):>8,} rows "
          f"({advertisers['churn_date'].notna().sum()} churned)")
    print(f"  campaigns.csv         {len(campaigns):>8,} rows")
    print(f"  daily_performance.csv {len(performance):>8,} rows")
    print()
    print(f"  date range   {performance['date'].min()} to {performance['date'].max()}")
    print(f"  total spend  ${performance['spend_usd'].sum():,.0f}")
    print(f"  total GMV    ${performance['attributed_gmv_usd'].sum():,.0f}")
    print(f"  blended ROAS {performance['attributed_gmv_usd'].sum() / performance['spend_usd'].sum():.2f}x")


if __name__ == "__main__":
    main()
