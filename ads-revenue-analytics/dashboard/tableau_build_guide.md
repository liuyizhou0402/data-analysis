# Tableau build guide

Reproduces the dashboard in `ads_performance_dashboard.png` as an interactive
Tableau workbook. Everything here is buildable in **Tableau Public** (free), so
the finished dashboard can be published to a shareable URL.

Total build time: about 60–90 minutes.

---

## 0. Before you start

Run the analysis so the extracts exist:

```bash
python analysis/run_analysis.py
```

That writes twelve CSVs into `dashboard/extracts/`. Each sheet below names the
one file it connects to. They are pre-aggregated by design — the heavy lifting
happens in SQL, and Tableau does presentation. That split matters: it is the
same division of labour a production BI stack uses, and it keeps the workbook
fast because no sheet is scanning 195,000 fact rows.

---

## 1. Connect the data

Tableau Public → **Connect → Text file** → select a CSV from
`dashboard/extracts/`.

Add each of these as a *separate* data source (do not join them — they are
different grains, and joining a monthly table to a per-rep table would fan out
rows and inflate every measure):

| Data source | File | Grain |
|---|---|---|
| Executive Summary | `q01_executive_summary.csv` | one row per month |
| Revenue Trend | `q02_revenue_trend.csv` | one row per month |
| Revenue Diagnosis | `q03_revenue_diagnosis.csv` | one row per region × vertical |
| Cohort Retention | `q04_cohort_retention.csv` | one row per signup cohort |
| Tier Performance | `q05_tier_performance.csv` | one row per account tier |
| Advertiser Deciles | `q06_advertiser_deciles.csv` | one row per revenue decile |
| Rep Scorecard | `q07_rep_scorecard.csv` | one row per sales rep |
| New Hire Ramp | `q08_new_hire_ramp.csv` | one row per tenure month |
| Book Size Retention | `q09_book_size_retention.csv` | one row per book-size band |
| Funnel by Objective | `q10_funnel_by_objective.csv` | one row per objective |
| Growth Opportunities | `q11_growth_opportunities.csv` | one row per vertical |
| Churn Watchlist | `q12_churn_watchlist.csv` | one row per at-risk advertiser |

**Check the `month` fields parse as dates, not strings.** Tableau usually gets
this right from the ISO format, but if a `month` column arrives as text, click
its data-type icon in the data pane and change it to Date. Every time-series
sheet depends on it.

---

## 2. Build the sheets

Field names below match the CSV headers exactly.

### Sheet 1 — `Revenue Trend`
*Source: Revenue Trend*

- **Columns:** `Month` → set to **Month (continuous)**, the green pill version
- **Rows:** `SUM(Revenue Usd)` → Bar
- Drag `AVG(Revenue 3mo Avg)` to **Rows** as a second axis → right-click →
  **Dual Axis** → right-click either axis → **Synchronize Axis**
- Change the second mark type to **Line**, width 3
- Colour: bars `#A8C8DC`, line `#1F5F8B`
- Title: *Revenue is growing — but the growth is not evenly distributed*

### Sheet 2 — `Account Base vs ARPA`
*Source: Executive Summary*

- **Columns:** `Month` (continuous)
- **Rows:** `SUM(Active Advertisers)`, then `SUM(Revenue Per Advertiser)` as a
  second row → **Dual Axis**, do **not** synchronise (different units)
- Both as Line, colour `#C1553B` and `#1F5F8B`
- Title: *The account base is shrinking while revenue per account rises*

### Sheet 3 — `Revenue Diagnosis` ← the headline sheet
*Source: Revenue Diagnosis*

- **Rows:** `Region`, `Vertical`
- **Columns:** `SUM(Change Usd)`
- **Sort** Rows by `SUM(Change Usd)` ascending, so declines sit at the bottom
- **Colour:** create the calculated field `Change Direction` (see
  `calculated_fields.md`) → drag to Colour → green `#3D7A5A` / coral `#C1553B`
- **Filter:** drag `Flag` to Filters → exclude `Immaterial`
- **Tooltip:** add `Change Pct` and `Contribution To Total Change Pct`
- Title: *Which segments moved — last 3 months vs prior 3 months*

### Sheet 4 — `Tier Performance`
*Source: Tier Performance*

- **Columns:** `Account Tier`
- **Rows:** `SUM(Pct Of Revenue)` as Bar, `AVG(Churn Rate Pct)` as Line on a
  **Dual Axis** (not synchronised)
- Title: *Churn is concentrated where revenue is not*

### Sheet 5 — `Growth Opportunity Matrix`
*Source: Growth Opportunities*

- **Columns:** `AVG(Spend Share Pct)`
- **Rows:** `AVG(Roas)`
- **Marks:** Circle; `SUM(Advertisers)` → Size; `Vertical` → Label
- `Recommended Action` → Colour
- Add a **Reference Line** on the ROAS axis at **Average** — this is what makes
  "above-average return, below-average investment" readable as a quadrant
- Title: *Where return is high but investment is not*

### Sheet 6 — `New Hire Ramp`
*Source: New Hire Ramp*

- **Columns:** `Months Tenure` (continuous)
- **Rows:** `AVG(Pct Of Full Productivity)` → Line, size 3
- Add a **Reference Line** at constant **100**
- Title: *New reps reach ~90% productivity by month 4*

### Sheet 7 — `Book Size vs Retention`
*Source: Book Size Retention*

- **Columns:** `Book Size Band`
- **Rows:** `AVG(Avg Book Churn Pct)` and `AVG(Smb Only Churn Pct)` → use
  **Measure Names / Measure Values** to get side-by-side bars
- Title: *Larger books, worse retention — and it holds within SMB alone*

### Sheet 8 — `Objective Funnel`
*Source: Funnel by Objective*

- **Rows:** `Objective`, sorted by `SUM(Spend Usd)` descending
- **Columns:** `SUM(Spend Usd)`
- **Label:** `AVG(Roas)`
- Title: *Spend and return by campaign objective*

### Sheet 9 — `Churn Watchlist`
*Source: Churn Watchlist*

- A **text table**: `Advertiser Name`, `Account Tier`, `Region`, `Owning Rep`
  on Rows; `Revenue Latest`, `Decline Pct 2mo`, `Revenue At Risk Usd` as measures
- Sort by `Revenue At Risk Usd` descending
- Colour `Decline Pct 2mo` on a red gradient
- Title: *Active accounts declining two months running*

---

## 3. Assemble the dashboard

**Dashboard → New Dashboard.** Size: **1400 × 1250** (Fixed size — floating
layouts break when a recruiter opens it at a different resolution).

Layout, top to bottom:

```
┌──────────────────────────────────────────────────────────────┐
│  Title:  Advertising Revenue & Sales Performance             │
├───────────────────────────────────┬──────────────────────────┤
│  Sheet 1  Revenue Trend           │  Sheet 2  Base vs ARPA   │
├───────────────────────────────────┼──────────────────────────┤
│  Sheet 3  Revenue Diagnosis       │  Sheet 4  Tier           │
├──────────────┬────────────────────┼──────────────────────────┤
│  Sheet 5     │  Sheet 6           │  Sheet 7                 │
│  Opportunity │  Ramp              │  Book size               │
├──────────────┴────────────────────┴──────────────────────────┤
│  Sheet 9  Churn Watchlist (full width)                       │
└──────────────────────────────────────────────────────────────┘
```

Add a **Text** object at the top for the title, and a second smaller line
underneath: *Jul 2024 – Dec 2025 · $566M revenue · 3.30x blended ROAS ·
synthetic data*.

### Make it interactive

This is the part that separates a dashboard from a set of charts, and it is
worth doing before publishing:

1. Select Sheet 3 → **Use as Filter** (the funnel icon). Clicking a segment
   filters the sheets that share its data source.
2. **Dashboard → Actions → Add Action → Highlight**: source Sheet 5, target
   Sheet 8, on **Hover**, field `Vertical`.
3. Add a **Region** filter as a dropdown: on any sheet, right-click `Region` →
   **Show Filter**, then **Apply to Worksheets → All Using This Data Source**.

---

## 4. Publish

**File → Save to Tableau Public As…** — this requires a free Tableau Public
account and makes the workbook publicly viewable, which is the point: the URL
goes in your CV and in the repository README.

After publishing:

- Open the public URL and check it renders at a normal browser width.
- Under the workbook's settings, **enable "Allow workbook and its data to be
  downloaded"** if you want reviewers to inspect your calculations. For a
  portfolio piece this is usually worth it — it lets a hiring manager verify
  the work is yours.
- Paste the URL into the project `README.md`, replacing the placeholder.

> **Note on data:** the extracts contain only synthetic data generated by
> `data/generate_data.py`, so there is nothing confidential to worry about when
> publishing publicly.
