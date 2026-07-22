"""
Build the Emergency Department performance dashboard as a single PNG.

This renders REAL charts from the generated CSVs using matplotlib (Agg,
headless). The output `dashboard/ed_performance_dashboard.png` is an honest
artefact of this code — it is a Python/matplotlib dashboard, NOT a Power BI
export. (A Power BI build guide that reproduces the same views lives in
`dashboard/powerbi_build_guide.md`.)

Usage:
    python analysis/build_dashboard.py
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
OUT = os.path.join(HERE, "..", "dashboard", "ed_performance_dashboard.png")

# --- palette (accessible, print-safe) --------------------------------
INK = "#1f2a37"
MUTED = "#6b7280"
ACCENT = "#2563eb"
GOOD = "#059669"
WARN = "#d97706"
BAD = "#dc2626"
GRID = "#e5e7eb"
CARD = "#f8fafc"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.edgecolor": GRID,
    "axes.linewidth": 0.8,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "figure.dpi": 130,
})


def load():
    pres = pd.read_csv(os.path.join(DATA, "ed_presentations.csv"),
                       parse_dates=["arrival_datetime", "departure_datetime"])
    adm = pd.read_csv(os.path.join(DATA, "admissions.csv"))
    return pres, adm


def kpi_card(ax, value, label, sub, color=ACCENT):
    ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, transform=ax.transAxes,
                               facecolor=CARD, edgecolor=GRID, lw=1))
    ax.text(0.06, 0.62, value, fontsize=25, fontweight="bold", color=color,
            transform=ax.transAxes)
    ax.text(0.06, 0.34, label, fontsize=11.5, fontweight="bold",
            transform=ax.transAxes)
    ax.text(0.06, 0.13, sub, fontsize=8.6, color=MUTED, transform=ax.transAxes)


def main():
    pres, adm = load()
    pres["month"] = pres["arrival_datetime"].dt.to_period("M").astype(str)
    pres["hour"] = pres["arrival_datetime"].dt.hour

    total = len(pres)
    pct_4hr = pres["met_4hr_target"].mean() * 100
    lwbs = pres["left_without_being_seen"].mean() * 100
    readmit = adm["readmitted_28d"].mean() * 100

    fig = plt.figure(figsize=(15, 9.6))
    fig.patch.set_facecolor("white")
    gs = gridspec.GridSpec(
        4, 4, figure=fig,
        height_ratios=[0.34, 1.0, 1.0, 0.06],
        hspace=0.55, wspace=0.28,
        left=0.05, right=0.97, top=0.90, bottom=0.05,
    )

    # header
    fig.text(0.05, 0.955, "Emergency Department — Performance & Patient Flow",
             fontsize=20, fontweight="bold", color=INK)
    fig.text(0.05, 0.925,
             "Synthetic dataset · FY2024–25 · 54,837 presentations · built with Python + matplotlib",
             fontsize=10.5, color=MUTED)

    # KPI row
    kpi_card(fig.add_subplot(gs[0, 0]), f"{total:,}", "ED Presentations",
             "financial year 2024–25", ACCENT)
    kpi_card(fig.add_subplot(gs[0, 1]), f"{pct_4hr:.1f}%", "Met 4-hour target",
             "NEAT benchmark 81%", GOOD if pct_4hr >= 81 else WARN)
    kpi_card(fig.add_subplot(gs[0, 2]), f"{lwbs:.1f}%", "Left without being seen",
             "target < 5%", BAD if lwbs >= 5 else GOOD)
    kpi_card(fig.add_subplot(gs[0, 3]), f"{readmit:.1f}%", "28-day readmission",
             "of inpatient admissions", WARN)

    # Chart 1: monthly volume + 4hr performance (dual axis) -----------
    ax1 = fig.add_subplot(gs[1, 0:2])
    m = pres.groupby("month").agg(vol=("presentation_id", "size"),
                                  p4=("met_4hr_target", "mean")).reset_index()
    x = np.arange(len(m))
    ax1.bar(x, m["vol"], color=ACCENT, alpha=0.85, width=0.62, label="Presentations")
    ax1.set_ylabel("Presentations", fontsize=9)
    ax1.set_xticks(x)
    ax1.set_xticklabels([mm[2:] for mm in m["month"]], fontsize=7.5)
    ax1b = ax1.twinx()
    ax1b.plot(x, m["p4"] * 100, color=WARN, marker="o", lw=2, label="% within 4hr")
    ax1b.axhline(81, color=MUTED, ls="--", lw=1)
    ax1b.set_ylim(40, 100)
    ax1b.set_ylabel("% within 4hr", fontsize=9)
    ax1.set_title("Monthly demand vs 4-hour target (winter surge)",
                  fontsize=11.5, fontweight="bold", loc="left", pad=8)
    ax1.grid(axis="y", color=GRID, lw=0.6)
    ax1.set_axisbelow(True)

    # Chart 2: 4hr performance by triage ------------------------------
    ax2 = fig.add_subplot(gs[1, 2])
    t = pres.groupby("triage_category")["met_4hr_target"].mean().mul(100)
    labels = ["T1", "T2", "T3", "T4", "T5"]
    colors = [BAD if v < 81 else GOOD for v in t.values]
    ax2.barh(labels[::-1], t.values[::-1], color=colors[::-1])
    ax2.axvline(81, color=MUTED, ls="--", lw=1)
    ax2.set_xlim(0, 100)
    for i, v in enumerate(t.values[::-1]):
        ax2.text(v - 4, i, f"{v:.0f}%", va="center", ha="right",
                 color="white", fontsize=8.5, fontweight="bold")
    ax2.set_title("% within 4hr by triage acuity",
                  fontsize=11.5, fontweight="bold", loc="left", pad=8)
    ax2.set_xlabel("% within 4hr", fontsize=9)

    # Chart 3: hourly arrivals by mode --------------------------------
    ax3 = fig.add_subplot(gs[1, 3])
    h = pres.groupby(["hour", "arrival_mode"]).size().unstack(fill_value=0)
    ax3.fill_between(h.index, 0, h.get("Self", 0), color=ACCENT, alpha=0.7, label="Self")
    ax3.fill_between(h.index, h.get("Self", 0),
                     h.get("Self", 0) + h.get("Ambulance", 0),
                     color=WARN, alpha=0.8, label="Ambulance")
    ax3.set_title("Arrivals by hour", fontsize=11.5, fontweight="bold",
                  loc="left", pad=8)
    ax3.set_xlabel("hour of day", fontsize=9)
    ax3.set_xlim(0, 23)
    ax3.legend(fontsize=7.5, frameon=False, loc="upper left")

    # Chart 4: readmission rate by diagnosis --------------------------
    ax4 = fig.add_subplot(gs[2, 0:2])
    r = adm.groupby("diagnosis_group")["readmitted_28d"].mean().mul(100).sort_values()
    ax4.barh(r.index, r.values, color=ACCENT)
    for i, v in enumerate(r.values):
        ax4.text(v + 0.15, i, f"{v:.1f}%", va="center", fontsize=8.5, color=INK)
    ax4.set_title("28-day readmission rate by diagnosis group",
                  fontsize=11.5, fontweight="bold", loc="left", pad=8)
    ax4.set_xlabel("readmission rate %", fontsize=9)
    ax4.set_xlim(0, r.max() * 1.25)

    # Chart 5: avg ED LOS by triage -----------------------------------
    ax5 = fig.add_subplot(gs[2, 2])
    los = pres.groupby("triage_category")["ed_los_minutes"].mean()
    ax5.plot(labels, los.values, marker="o", color=BAD, lw=2)
    ax5.axhline(240, color=MUTED, ls="--", lw=1)
    ax5.text(0.02, 245, "240 min (4hr)", fontsize=7.5, color=MUTED)
    ax5.fill_between(labels, los.values, 0, color=BAD, alpha=0.08)
    ax5.set_title("Avg ED length of stay (min)", fontsize=11.5,
                  fontweight="bold", loc="left", pad=8)
    ax5.grid(axis="y", color=GRID, lw=0.6)
    ax5.set_axisbelow(True)

    # Chart 6: presentations by region --------------------------------
    ax6 = fig.add_subplot(gs[2, 3])
    reg = (pres.merge(pd.read_csv(os.path.join(DATA, "patients.csv"))
                      [["patient_id", "region"]], on="patient_id")
           .groupby("region").size().sort_values())
    ax6.barh(reg.index, reg.values, color=GOOD, alpha=0.85)
    ax6.set_title("Presentations by catchment", fontsize=11.5,
                  fontweight="bold", loc="left", pad=8)
    ax6.tick_params(axis="y", labelsize=7.5)

    fig.text(0.05, 0.018,
             "Synthetic data for portfolio demonstration — no real patient records. "
             "Metrics modelled on publicly reported Australian ED indicators.",
             fontsize=8, color=MUTED, style="italic")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    fig.savefig(OUT, bbox_inches="tight", facecolor="white")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
