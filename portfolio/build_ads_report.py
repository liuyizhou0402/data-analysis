#!/usr/bin/env python3
"""Advertising Revenue & Sales Performance — portfolio PDF.

Every figure here is produced by ads-revenue-analytics/sql/02_analysis.sql and
reproducible with analysis/run_analysis.py; this script only lays them out.

    python portfolio/build_ads_report.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from reportlab.lib.units import mm
from reportlab.platypus import PageBreak, Spacer, NextPageTemplate

from pdfkit import (Doc, bind_headings, bullets, callout, cover, figure, h1, h2,
                    metric_row, para, rule, table)

PROJ = ROOT / "ads-revenue-analytics"
OUT = ROOT / "portfolio" / "Ads_Revenue_Analytics_Yizhou_Liu.pdf"

story = []

# ------------------------------------------------------------------ cover --
story += cover(
    title="Advertising Revenue<br/>&amp; Sales Performance",
    subtitle="Revenue is growing 9.9% — so why is that a problem?",
    author="<b>Yizhou Liu</b> &nbsp;·&nbsp; Data Analyst &nbsp;·&nbsp; Sydney, Australia",
    stack="SQL (DuckDB — CTEs, window functions, cohort analysis) &nbsp;·&nbsp; "
          "Python (pandas, matplotlib) &nbsp;·&nbsp; Tableau",
    repo="github.com/liuyizhou0402/data-analysis &nbsp;/&nbsp; ads-revenue-analytics",
    metrics=[("$566.3M", "revenue analysed"), ("340", "advertisers"),
             ("195,488", "campaign-days"), ("12", "SQL business queries")],
    blurb="An end-to-end business analysis of a digital advertising sales organisation over 18 "
          "months — 340 advertisers, 42 sales reps, 3,143 campaigns. Twelve SQL queries run in the "
          "order a monthly business review runs: <i>what happened → why → who → what next</i>. The "
          "project demonstrates one analytical habit: the headline number said the business was "
          "healthy, and the job was to check whether that was true.",
)
story += [Spacer(1, 3 * mm)]
story.append(h2("Four headline findings"))
story.append(bullets([
    "<b>Growth is masking contraction.</b> Revenue rose 9.9% half-over-half while active advertisers "
    "fell <b>31%</b> and revenue per advertiser rose <b>93%</b> — expansion on a shrinking base.",
    "<b>One segment is in structural decline, invisible in the trend.</b> SEA Gaming contracted "
    "<b>33.7%</b>, and an independent churn query returns 5 SEA Gaming accounts in its top 10 at-risk list.",
    "<b>Book size measurably damages retention.</b> Reps with 17+ accounts lose <b>71%</b> of their "
    "book versus 43% for reps with 1–8 — and the effect survives controlling for tier mix.",
    "<b>The highest-return vertical is under-invested.</b> Beauty &amp; Personal Care returns "
    "<b>4.75x ROAS</b> on 10.7% of spend, against a 2.95x book average.",
]))
story += [Spacer(1, 4 * mm)]
story.append(callout(
    "The dataset is <b>synthetic and seeded</b> (<font face='Courier'>SEED = 20260218</font>) — "
    "advertiser-level revenue is commercially confidential and never public. The generator builds in "
    "six business patterns for the analysis to find rather than producing noise. Getting those "
    "patterns to survive into the data took more work than generating it did; see the appendix.",
    label="On the data &nbsp;"))

story += [NextPageTemplate("body"), PageBreak()]

# --------------------------------------------------------------- the point --
story.append(h1("The headline is hiding two problems"))
story.append(para(
    "Revenue grew <b>9.9%</b> half-over-half — $184.0M in the first six months to $202.2M in the last "
    "six. On that number alone the business looks healthy. It is not the whole picture.", "lead"))

story.append(table(
    [["", "First month", "Last month", "Change"],
     ["Active advertisers", "199", "138", "−31%"],
     ["Revenue per advertiser", "$144,681", "$278,565", "+93%"]],
    widths=[58 * mm, 38 * mm, 38 * mm, 36 * mm], align_center_from=1,
    flag_cells={(1, 3), (2, 3)}))
story.append(para("<i>(Q1 — executive summary)</i>", "note"))

story.append(para(
    "<b>All of the growth is coming from existing accounts spending more, on a base that is "
    "contracting by roughly a third.</b> ARPA nearly doubling is not a success story on its own — it "
    "is what revenue concentration looks like while it is happening. The top revenue decile (31 "
    "advertisers) now carries <b>66.8%</b> of revenue, and the top two deciles carry <b>83.2%</b> "
    "<i>(Q6)</i>."))

story.append(callout(
    "That is the single most important thing in this report, and no single-number dashboard would "
    "have surfaced it. Blended growth averaged a rising E-commerce book against a falling Gaming one "
    "and reported the difference as health. Two specific problems sit underneath it — a declining "
    "segment (§1) and broken retention in the tiers that feed the base (§2).",
    label="Why it matters &nbsp;"))

story.append(h1("Summary dashboard"))
story.append(para(
    "Rendered from the query extracts by <font face='Courier'>analysis/build_dashboard.py</font>. "
    "Twelve Tableau-ready CSVs, a step-by-step build guide and every calculated field (with its "
    "reasoning) ship in <font face='Courier'>dashboard/</font> so the interactive workbook "
    "reproduces from the same source."))
story.append(figure(str(PROJ / "dashboard" / "ads_performance_dashboard.png"), max_h_mm=170))

# ----------------------------------------------------------------- §1 ------
story.append(h1("1. Gaming is in structural decline, and it is being masked"))
story.append(para(
    "Comparing the most recent three months against the prior three, total revenue rose $17.2M. "
    "Within that, declining segments removed $4.9M — and the largest single drag is Southeast Asia "
    "Gaming: <b>−$1.21M, −33.7%</b>, taking <b>7.0 percentage points</b> off the total change on its "
    "own <i>(Q3)</i>. Gaming declines are not confined to one market:"))

story.append(table(
    [["Segment", "Change", "% change"],
     ["Southeast Asia · Gaming", "−$1,205,536", "−33.7%"],
     ["North America · Gaming", "−$685,522", "−31.7%"],
     ["Australia &amp; NZ · Gaming", "−$444,877", "−65.4%"],
     ["Japan &amp; Korea · Gaming", "−$180,646", "−14.5%"],
     ["Europe · Gaming", "growth", "+47.1%"]],
    widths=[80 * mm, 45 * mm, 45 * mm], align_center_from=1,
    flag_cells={(1, 2), (3, 2)}))
story.append(Spacer(1, 3 * mm))

story.append(callout(
    "<b>Corroborated by a query that did not know about it.</b> The churn watchlist <i>(Q12)</i> was "
    "built independently of the segment analysis and returns 10 at-risk accounts carrying $2.84M — "
    "<b>6 of the 10 are Gaming advertisers, 5 of them in Southeast Asia</b>. Two unrelated cuts of "
    "the data landing on the same root cause is a far stronger signal than either alone, and it is "
    "the reason this finding is reported as a conclusion rather than a hypothesis.",
    label="The check that makes it credible &nbsp;"))

story.append(h2("Recommendation"))
story.append(bullets([
    "Treat the Gaming book as a <b>retention</b> problem, not a performance one — Gaming ROAS is "
    "2.68x against a 2.95x vertical average, so advertisers are getting weaker returns and "
    "responding rationally.",
    "Commission a competitive review specifically for SEA Gaming <b>before</b> next quarter's targets "
    "are set. A −34% segment trend that continues removes roughly <b>$2.4M annualised</b>.",
    "Do not set regional targets from the blended growth rate — it will over-target exactly the "
    "markets where Gaming concentrates.",
]))

# ----------------------------------------------------------------- §2 ------
story.append(h1("2. The account base is shrinking because SMB retention is broken"))
story.append(para("Churn is severe and heavily tiered <i>(Q5)</i>:"))
story.append(table(
    [["Tier", "Advertisers", "% of revenue", "Churn rate", "Revenue / advertiser"],
     ["Enterprise", "42", "72.5%", "16.3%", "$9,770,015"],
     ["Mid-Market", "103", "24.2%", "44.4%", "$1,329,444"],
     ["SMB", "162", "3.4%", "82.5%", "$117,601"]],
    widths=[32 * mm, 30 * mm, 34 * mm, 32 * mm, 42 * mm], align_center_from=1,
    flag_cells={(3, 3)}))
story.append(Spacer(1, 3 * mm))
story.append(para("SMB is 48% of the account base and 3.4% of revenue, churning at 82.5%."))

story.append(callout(
    "<b>The obvious read is wrong.</b> \"Fix SMB retention\" is the natural response, and the number "
    "that kills it is the third column: SMB is <b>3.4% of revenue</b>. A programme that halves SMB "
    "churn is worth about $1.7M annually in the best case and would consume disproportionate service "
    "capacity. The better use of the same finding is <b>coverage design</b> — move SMB to pooled or "
    "self-serve, freeing named reps for Mid-Market, where churn is still 44.4% but each account is "
    "worth <b>11x more</b>. Mid-Market is where retention spend earns its return.",
    label="Recommendation — and a caution &nbsp;"))

story.append(PageBreak())

# ----------------------------------------------------------------- §3 ------
story.append(h1("3. Rep book sizes are set too high, and it is costing retention"))
story.append(para("Churn on a rep's book rises with the size of that book <i>(Q9)</i>:"))
story.append(table(
    [["Book size", "Reps", "Avg book", "Book churn", "SMB-only churn"],
     ["1–8 accounts", "14", "5.1", "42.8%", "65.0%"],
     ["9–16 accounts", "8", "11.5", "56.1%", "75.0%"],
     ["17+ accounts", "5", "30.6", "71.3%", "93.8%"]],
    widths=[38 * mm, 26 * mm, 30 * mm, 36 * mm, 40 * mm], align_center_from=1,
    flag_cells={(3, 3), (3, 4)}))
story.append(Spacer(1, 3 * mm))

story.append(para(
    "<b>The relationship survives the obvious objection.</b> Reps carrying more accounts might simply "
    "hold more SMB accounts, which churn more for unrelated reasons — a confound that would make the "
    "finding meaningless. The SMB-only column controls for exactly that, and the effect is "
    "<i>stronger</i> within SMB alone (65.0% → 93.8%) than across all accounts. Book size is doing "
    "the work, not tier mix. Reps above the line hold <b>38% of total revenue</b>, so this is not a "
    "marginal group."))

story.append(h2("Recommendation"))
story.append(para(
    "Cap named-coverage books at roughly <b>16 accounts</b>. The five reps above that line average "
    "30.6 accounts and lose 71% of their book. Rebalancing requires either redistributing accounts to "
    "reps below the line or moving their SMB tail to pooled coverage — which is the same action "
    "recommended in §2. Doing both together is what makes either affordable."))

# ----------------------------------------------------------------- §4 ------
story.append(h1("4. Beauty &amp; Personal Care is under-invested"))
story.append(para(
    "Beauty &amp; Personal Care returns <b>4.75x ROAS</b> — the highest of any vertical, against a "
    "2.95x average — on only <b>10.7% of spend</b>, across 29 advertisers generating $60.4M "
    "<i>(Q11)</i>. For comparison, E-commerce &amp; Retail takes 40.8% of spend at 3.50x."))
story.append(bullets([
    "Set an upsell target on the existing 29 Beauty accounts <b>before</b> pursuing new logos — "
    "expanding a book that already returns 4.75x is cheaper than acquiring into it.",
    "Prioritise Beauty in acquisition for the next two quarters, particularly in Europe, where the "
    "vertical grew 21.1% and is not yet saturated.",
]))
story.append(callout(
    "<b>ROAS here is attributed, not incremental.</b> High attributed ROAS can partly reflect "
    "purchases that would have happened anyway, and beauty is a category where that risk is real. "
    "The upsell recommendation is safe either way; a large acquisition bet should be validated with "
    "an incrementality test first. Stating this is not hedging — it is the difference between a "
    "recommendation a business can act on and one that quietly transfers risk to whoever acts on it.",
    label="Caveat &nbsp;"))

# ----------------------------------------------------------------- §5 ------
story.append(h1("5. New reps take five months to ramp — plan hiring accordingly"))
story.append(para("Reps hired inside the observation window reach <i>(Q8)</i>:"))
story.append(table(
    [["Months since hire", "0", "1", "2", "3", "4", "5"],
     ["% of tenured productivity", "25%", "49%", "54%", "76%", "91%", "93%"]],
    widths=[52 * mm, 19.6 * mm, 19.6 * mm, 19.6 * mm, 19.6 * mm, 19.6 * mm, 19.6 * mm],
    align_center_from=1, flag_cells={(1, 5)}))
story.append(Spacer(1, 3 * mm))
story.append(para(
    "15 of 38 reps were hired during the window, so this is measured on a substantial group rather "
    "than a handful. Hiring decisions need a five-month lead time against revenue targets: headcount "
    "to support a Q4 peak must be hired by <b>Q2, not Q3</b>. And given §3, the accounts freed by "
    "capping book sizes should go to <i>tenured</i> reps, not to new hires."))

story.append(PageBreak())

# ------------------------------------------------------------- summary -----
story.append(h1("Summary of recommended actions"))
story.append(table(
    [["#", "Action", "Evidence", "Expected impact"],
     ["1", "Competitive review of SEA Gaming before next targets are set", "Q3, Q12",
      "Protects ~$2.4M annualised"],
     ["2", "Move SMB to pooled / self-serve coverage", "Q5, Q9",
      "Frees capacity; SMB is 3.4% of revenue"],
     ["3", "Cap named books at ~16 accounts", "Q9",
      "Addresses 38% of revenue held by over-loaded reps"],
     ["4", "Upsell the 29 existing Beauty accounts", "Q11",
      "Highest-ROAS vertical, on 10.7% of spend"],
     ["5", "Hire five months ahead of target periods", "Q8",
      "Removes the ramp gap from capacity planning"],
     ["6", "Report growth by segment, not blended", "Q1, Q3",
      "Blended growth is currently masking a −34% segment"]],
    widths=[10 * mm, 62 * mm, 24 * mm, 74 * mm], align_center_from=2))

story.append(h1("Appendix — how it was built"))

story.append(h2("The twelve queries"))
story.append(para(
    "Ordered the way a monthly business review runs — <i>what happened → why → who → what next</i>.",
    "note"))
story.append(table(
    [["", "Question", "Techniques"],
     ["Q1", "Executive KPI summary with MoM movement", "CTEs, <font face='Courier'>LAG</font>, guarded rate maths"],
     ["Q2", "Revenue trend, moving average, running total", "<font face='Courier'>AVG OVER</font> with explicit frame, <font face='Courier'>SUM OVER</font>"],
     ["Q3", "<b>Revenue diagnosis</b> — which segments moved", "Conditional aggregation, contribution-to-change"],
     ["Q4", "Advertiser cohort retention", "Cohort self-join, <font face='Courier'>DATE_DIFF</font>, pivot via <font face='Courier'>CASE</font>"],
     ["Q5", "Retention and revenue by account tier", "Multi-CTE join, share-of-total window"],
     ["Q6", "Advertiser value deciles and Pareto curve", "<font face='Courier'>NTILE</font>, running total window"],
     ["Q7", "Sales rep scorecard", "<font face='Courier'>RANK</font>, partitioned rank, <font face='Courier'>MEDIAN</font> as window"],
     ["Q8", "New-hire ramp curve", "Date arithmetic, cross-join baseline"],
     ["Q9", "Does book size hurt retention?", "Conditional aggregation with confound controls"],
     ["Q10", "Campaign funnel by objective", "Nested aggregate windows, funnel rates"],
     ["Q11", "Growth opportunity matrix", "Window benchmarks, <font face='Courier'>CASE</font>-based classification"],
     ["Q12", "Churn-risk watchlist", "Period comparison, materiality thresholds"]],
    widths=[12 * mm, 72 * mm, 86 * mm], align_center_from=99))

story.append(h2("Two things the queries do deliberately"))
story.append(bullets([
    "<b>Every denominator is <font face='Courier'>NULLIF</font>-guarded.</b> A campaign-day with "
    "impressions and zero clicks is normal; an unguarded CTR divides by zero somewhere in 195,000 rows.",
    "<b>Confounds are handled, not ignored.</b> Q9's book-size finding would be meaningless without "
    "controlling for tier mix, and Q4's cohort denominator is taken from the advertiser dimension "
    "rather than from month-0 spenders — the shortcut version reports retention above 100%.",
]))

story.append(h2("Engine"))
story.append(para(
    "<b>DuckDB</b> — zero-config, reads CSV natively, and its SQL dialect is close enough to "
    "Postgres / Snowflake / BigQuery to port with minor changes. DuckDB-specific syntax "
    "(<font face='Courier'>QUALIFY</font>, <font face='Courier'>read_csv_auto</font>) is flagged in "
    "comments wherever it appears."))

story.append(PageBreak())

story.append(h1("Appendix — on the data, honestly"))
story.append(para(
    "The dataset is synthetic, and deliberately so: advertiser-level revenue is commercially "
    "confidential and never public. The generator builds in six business patterns for the analysis "
    "to find — Q4 seasonality, a segment-level demand shock, tier-differentiated churn, a sales-rep "
    "ramp curve, a book-size retention penalty, and an under-invested high-return vertical — rather "
    "than producing random noise.", "lead"))

story.append(callout(
    "Getting those patterns to survive into the data took more work than generating it did. "
    "<b>Two rounds of the generator produced statistically dead findings</b> — a segment too thin to "
    "carry a trend, and a book-size effect resting on a two-rep comparison. Both were diagnosed and "
    "fixed rather than written up as results. The reasoning is documented in the generator's "
    "comments, because it is the part of the process that matters most: <b>an analysis is only as "
    "trustworthy as the check that its finding is real.</b>",
    label="The part worth reading &nbsp;"))

story.append(h2("What this analysis cannot tell you"))
story.append(bullets([
    "<b>The data is synthetic.</b> It demonstrates method rather than describing a real market. No "
    "conclusion here is a claim about any actual company.",
    "<b>ROAS is attributed, not incremental.</b> Every return figure inherits whatever attribution "
    "model produced it. Incrementality requires a holdout test, not a query.",
    "<b>The declines are described, not explained.</b> The analysis establishes <i>that</i> SEA "
    "Gaming contracted and <i>how much</i> it cost. Whether the cause is competitive, regulatory or "
    "seasonal is not answerable from spend data alone — which is why recommendation 1 is a review, "
    "not a fix.",
    "<b>Churn is defined as an account closing.</b> Advertisers who cut spend by 90% but stay open "
    "are counted as retained. Q12 partly covers that gap; the tier churn rates in §2 read the strict "
    "definition.",
]))

story.append(h2("Reproducing it"))
story.append(table(
    [["Step", "Command"],
     ["1. Install (Python 3.11+)", "<font face='Courier'>pip install -r requirements.txt</font>"],
     ["2. Regenerate the dataset (optional)", "<font face='Courier'>python data/generate_data.py</font>"],
     ["3. Build DuckDB, run 12 queries, export extracts", "<font face='Courier'>python analysis/run_analysis.py</font>"],
     ["4. Render the dashboard", "<font face='Courier'>python analysis/build_dashboard.py</font>"],
     ["5. Rebuild this PDF", "<font face='Courier'>python portfolio/build_ads_report.py</font>"]],
    widths=[74 * mm, 96 * mm], align_center_from=99))
story.append(para(
    "All randomness is seeded (<font face='Courier'>SEED = 20260218</font>), so every number in this "
    "document reproduces exactly.", "note"))

story += rule(6, 4)
story.append(para(
    "Yizhou Liu &nbsp;·&nbsp; github.com/liuyizhou0402/data-analysis &nbsp;·&nbsp; "
    "Full source, SQL, data generator and Tableau build guide in the repository.", "note"))

Doc(str(OUT), "Advertising Revenue & Sales Performance  ·  Yizhou Liu").build(
    bind_headings(story))
kb = OUT.stat().st_size / 1024
print(f"built  {OUT.name}  {kb:.0f} KB  ({kb/1024:.2f} MB)")
