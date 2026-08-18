"""
Render the summary dashboard image used in the README.

This is a static preview of the same views the Tableau workbook builds -- it
gives the repository visual proof without requiring a reader to open Tableau,
and it doubles as the layout target for dashboard/tableau_build_guide.md.

    python analysis/build_dashboard.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.gridspec import GridSpec

ROOT = Path(__file__).resolve().parent.parent
EXTRACTS = ROOT / "dashboard" / "extracts"
OUT = ROOT / "dashboard" / "ads_performance_dashboard.png"

# Palette: a single blue accent with a warm counter-colour for declines, so
# "growth" and "decline" read instantly without a legend.
INK = "#1b2430"
MUTED = "#6b7a8a"
BLUE = "#1f5f8b"
BLUE_LT = "#a8c8dc"
CORAL = "#c1553b"
GREEN = "#3d7a5a"
GRID = "#dfe5ea"

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
    "text.color": INK,
    "axes.labelcolor": INK,
    "axes.edgecolor": GRID,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "xtick.labelsize": 8.5,
    "ytick.labelsize": 8.5,
})


def style(ax, title: str, subtitle: str | None = None) -> None:
    ax.set_title(title, loc="left", pad=14 if subtitle else 8)
    if subtitle:
        ax.text(0, 1.035, subtitle, transform=ax.transAxes,
                fontsize=8.5, color=MUTED, va="bottom")
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def money(x, _pos=None) -> str:
    if abs(x) >= 1e9:
        return f"${x / 1e9:.1f}B"
    if abs(x) >= 1e6:
        return f"${x / 1e6:.0f}M"
    if abs(x) >= 1e3:
        return f"${x / 1e3:.0f}K"
    return f"${x:.0f}"


def main() -> None:
    q1 = pd.read_csv(EXTRACTS / "q01_executive_summary.csv", parse_dates=["month"])
    q2 = pd.read_csv(EXTRACTS / "q02_revenue_trend.csv", parse_dates=["month"])
    q3 = pd.read_csv(EXTRACTS / "q03_revenue_diagnosis.csv")
    q5 = pd.read_csv(EXTRACTS / "q05_tier_performance.csv")
    q8 = pd.read_csv(EXTRACTS / "q08_new_hire_ramp.csv")
    q9 = pd.read_csv(EXTRACTS / "q09_book_size_retention.csv")
    q10 = pd.read_csv(EXTRACTS / "q10_funnel_by_objective.csv")
    q11 = pd.read_csv(EXTRACTS / "q11_growth_opportunities.csv")

    fig = plt.figure(figsize=(17, 13.5))
    fig.patch.set_facecolor("white")
    gs = GridSpec(4, 3, figure=fig, hspace=0.62, wspace=0.26,
                  top=0.905, bottom=0.05, left=0.055, right=0.975)

    # ---- header -----------------------------------------------------------
    total_rev = q1["revenue_usd"].sum()
    blended_roas = (q1["revenue_usd"] * q1["roas"]).sum() / q1["revenue_usd"].sum()
    period = f"{q1['month'].min():%b %Y} – {q1['month'].max():%b %Y}"
    fig.text(0.055, 0.968, "Advertising Revenue & Sales Performance",
             fontsize=21, fontweight="bold", color=INK)
    fig.text(0.055, 0.945,
             f"{period}  ·  {len(q1)} months  ·  {money(total_rev)} revenue  ·  "
             f"{blended_roas:.2f}x blended ROAS  ·  synthetic data",
             fontsize=10.5, color=MUTED)

    # ---- 1. revenue trend --------------------------------------------------
    ax = fig.add_subplot(gs[0, :2])
    ax.bar(q2["month"], q2["revenue_usd"], width=22, color=BLUE_LT, label="Monthly revenue")
    ax.plot(q2["month"], q2["revenue_3mo_avg"], color=BLUE, linewidth=2.4,
            label="3-month average")
    style(ax, "Revenue is growing — but the growth is not evenly distributed",
          "Q4 peaks in both years; the flat 3-month average through mid-2025 is the real trend")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(money))
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")

    # ---- 2. active advertisers vs ARPA ------------------------------------
    ax = fig.add_subplot(gs[0, 2])
    ax.plot(q1["month"], q1["active_advertisers"], color=CORAL, linewidth=2.2,
            marker="o", markersize=3)
    ax.set_ylabel("Active advertisers", color=CORAL)
    ax.tick_params(axis="y", labelcolor=CORAL)
    ax2 = ax.twinx()
    ax2.plot(q1["month"], q1["revenue_per_advertiser"], color=BLUE,
             linewidth=2.2, marker="s", markersize=3)
    ax2.set_ylabel("Revenue per advertiser", color=BLUE)
    ax2.tick_params(axis="y", labelcolor=BLUE)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(money))
    ax2.spines["top"].set_visible(False)
    style(ax, "The account base is shrinking",
          "Growth is coming from fewer, larger accounts")

    # ---- 3. revenue diagnosis ---------------------------------------------
    ax = fig.add_subplot(gs[1, :2])
    material = q3[q3["flag"] != "Immaterial"].copy()
    movers = pd.concat([material.nsmallest(6, "change_usd"),
                        material.nlargest(6, "change_usd")]).drop_duplicates()
    movers = movers.sort_values("change_usd")
    labels = movers["region"] + " · " + movers["vertical"]
    colors = [CORAL if v < 0 else GREEN for v in movers["change_usd"]]
    ax.barh(range(len(movers)), movers["change_usd"], color=colors, height=0.72)
    ax.set_yticks(range(len(movers)), labels, fontsize=8)
    ax.axvline(0, color=INK, linewidth=0.9)
    style(ax, "Revenue diagnosis: last 3 months vs prior 3 months",
          "Southeast Asia Gaming is the single largest drag — invisible in the headline trend")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(money))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)

    # ---- 4. tier: revenue vs churn ----------------------------------------
    ax = fig.add_subplot(gs[1, 2])
    x = np.arange(len(q5))
    ax.bar(x, q5["pct_of_revenue"], width=0.55, color=BLUE, label="% of revenue")
    ax.set_xticks(x, q5["account_tier"], fontsize=8.5)
    ax.set_ylabel("% of revenue")
    ax2 = ax.twinx()
    ax2.plot(x, q5["churn_rate_pct"], color=CORAL, marker="o", linewidth=2.2)
    ax2.set_ylabel("Churn rate %", color=CORAL)
    ax2.tick_params(axis="y", labelcolor=CORAL)
    ax2.spines["top"].set_visible(False)
    style(ax, "Churn is concentrated where revenue isn't",
          "SMB: 83% churn, 3% of revenue")

    # ---- 5. growth opportunity matrix -------------------------------------
    ax = fig.add_subplot(gs[2, 0])
    avg_roas = q11["roas"].mean()
    for _, row in q11.iterrows():
        grow = row["recommended_action"].startswith("GROW")
        ax.scatter(row["spend_share_pct"], row["roas"],
                   s=row["advertisers"] * 7,
                   color=GREEN if grow else BLUE_LT,
                   edgecolor=INK if grow else MUTED,
                   linewidth=1.4 if grow else 0.6, zorder=3)
        if grow or row["spend_share_pct"] > 15:
            ax.annotate(row["vertical"].split(" &")[0],
                        (row["spend_share_pct"], row["roas"]),
                        textcoords="offset points", xytext=(7, 5),
                        fontsize=8, color=INK,
                        fontweight="bold" if grow else "normal")
    ax.axhline(avg_roas, color=MUTED, linestyle="--", linewidth=1)
    ax.set_xlabel("Share of total spend (%)")
    ax.set_ylabel("ROAS")
    style(ax, "Where return is high but investment isn't",
          "Beauty: best ROAS, only 11% of spend")

    # ---- 6. new hire ramp --------------------------------------------------
    ax = fig.add_subplot(gs[2, 1])
    ax.plot(q8["months_tenure"], q8["pct_of_full_productivity"],
            color=BLUE, linewidth=2.4, marker="o", markersize=4)
    ax.axhline(100, color=MUTED, linestyle="--", linewidth=1)
    ax.axvspan(0, 5, color=CORAL, alpha=0.10)
    ax.text(2.5, 32, "ramp period", fontsize=8.5, color=CORAL,
            ha="center", fontweight="bold")
    ax.set_xlabel("Months since hire")
    ax.set_ylabel("% of tenured-rep productivity")
    style(ax, "New reps take ~5 months to ramp",
          "Reaching 91% of a tenured rep's monthly revenue by month 4")

    # ---- 7. book size vs retention ----------------------------------------
    ax = fig.add_subplot(gs[2, 2])
    x = np.arange(len(q9))
    w = 0.38
    ax.bar(x - w / 2, q9["avg_book_churn_pct"], width=w, color=BLUE_LT,
           label="All accounts")
    ax.bar(x + w / 2, q9["smb_only_churn_pct"], width=w, color=CORAL,
           label="SMB accounts only")
    ax.set_xticks(x, q9["book_size_band"], fontsize=8.5)
    ax.set_ylabel("Churn rate (%)")
    style(ax, "Bigger books, worse retention",
          "Holds after controlling for account-tier mix")
    ax.legend(frameon=False, fontsize=8)

    # ---- 8. funnel by objective -------------------------------------------
    ax = fig.add_subplot(gs[3, 0])
    q10s = q10.sort_values("spend_usd", ascending=True)
    ax.barh(q10s["objective"], q10s["spend_usd"], color=BLUE, height=0.62)
    for i, (_, row) in enumerate(q10s.iterrows()):
        ax.text(row["spend_usd"], i, f"  {row['roas']:.2f}x",
                va="center", fontsize=8.5, color=MUTED)
    style(ax, "Spend by campaign objective", "Labels show ROAS")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(money))
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)

    # ---- 9. efficiency by objective ---------------------------------------
    ax = fig.add_subplot(gs[3, 1])
    ax.scatter(q10["ctr_pct"], q10["cvr_pct"], s=q10["pct_of_spend"] * 22,
               color=BLUE, alpha=0.72, edgecolor=INK, linewidth=0.8, zorder=3)
    for _, row in q10.iterrows():
        ax.annotate(row["objective"], (row["ctr_pct"], row["cvr_pct"]),
                    textcoords="offset points", xytext=(8, 4), fontsize=8)
    ax.set_xlabel("CTR (%)")
    ax.set_ylabel("CVR (%)")
    style(ax, "Click rate vs conversion rate",
          "Bubble size = share of spend; the two trade off")

    # ---- 10. monthly ROAS stability ---------------------------------------
    ax = fig.add_subplot(gs[3, 2])
    ax.plot(q1["month"], q1["roas"], color=GREEN, linewidth=2.4, marker="o",
            markersize=3)
    ax.set_ylim(q1["roas"].min() - 0.15, q1["roas"].max() + 0.15)
    ax.set_ylabel("ROAS")
    style(ax, "Returns are stable while volume moves",
          "ROAS held 3.17x–3.37x across the period")

    fig.savefig(OUT, dpi=115, facecolor="white", bbox_inches="tight")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
