"""
Full exploratory analysis — generates the figures used in
`analysis/analysis_report.md`.

Every figure is rendered from the synthetic CSVs (matplotlib, headless) into
`analysis/figures/`. Running this reproduces all 14 charts and prints the key
statistics quoted in the report.

Usage:
    python analysis/eda.py
"""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "figures")
os.makedirs(FIG, exist_ok=True)

INK, MUTED, ACCENT = "#1f2a37", "#6b7280", "#2563eb"
GOOD, WARN, BAD, GRID = "#059669", "#d97706", "#dc2626", "#e5e7eb"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "figure.dpi": 120,
    "axes.edgecolor": GRID, "axes.linewidth": 0.8, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.6, "axes.axisbelow": True,
    "text.color": INK, "axes.labelcolor": INK,
    "xtick.color": MUTED, "ytick.color": MUTED, "axes.titlecolor": INK,
})

TRIAGE_LBL = {1: "T1 Resus", 2: "T2 Emerg", 3: "T3 Urgent",
              4: "T4 Semi", 5: "T5 Non-urg"}


def save(fig, name):
    path = os.path.join(FIG, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  figures/{name}")


def title(ax, t):
    ax.set_title(t, fontsize=12, fontweight="bold", loc="left", pad=8)


def load():
    pres = pd.read_csv(os.path.join(DATA, "ed_presentations.csv"),
                       parse_dates=["arrival_datetime", "departure_datetime"])
    adm = pd.read_csv(os.path.join(DATA, "admissions.csv"))
    pat = pd.read_csv(os.path.join(DATA, "patients.csv"))
    return pres, adm, pat


def main():
    pres, adm, pat = load()
    pres["date"] = pres["arrival_datetime"].dt.date
    pres["month"] = pres["arrival_datetime"].dt.to_period("M").astype(str)
    pres["hour"] = pres["arrival_datetime"].dt.hour
    pres["dow"] = pres["arrival_datetime"].dt.dayofweek
    print("Rendering figures:")

    # 01 — daily presentation volume (7-day rolling)
    daily = pres.groupby("date").size()
    roll = daily.rolling(7, center=True).mean()
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.plot(pd.to_datetime(daily.index), daily.values, color=GRID, lw=0.8)
    ax.plot(pd.to_datetime(roll.index), roll.values, color=ACCENT, lw=2.2,
            label="7-day average")
    ax.legend(frameon=False)
    ax.set_ylabel("presentations/day")
    title(ax, "01 · Daily ED presentations — winter surge is clearly visible")
    save(fig, "01_daily_volume.png")

    # 02 — monthly volume + 4hr dual axis
    m = pres.groupby("month").agg(v=("presentation_id", "size"),
                                  p=("met_4hr_target", "mean"))
    fig, ax = plt.subplots(figsize=(10, 3.8))
    x = np.arange(len(m))
    ax.bar(x, m["v"], color=ACCENT, alpha=0.85)
    ax.set_xticks(x); ax.set_xticklabels([i[2:] for i in m.index], fontsize=8)
    ax.set_ylabel("presentations")
    ax2 = ax.twinx()
    ax2.plot(x, m["p"] * 100, color=WARN, marker="o", lw=2)
    ax2.axhline(81, color=MUTED, ls="--", lw=1); ax2.set_ylim(50, 100)
    ax2.set_ylabel("% within 4hr"); ax2.grid(False)
    title(ax, "02 · Monthly demand vs 4-hour target (81% benchmark)")
    save(fig, "02_monthly_vs_target.png")

    # 03 — triage mix
    tm = pres["triage_category"].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.bar([TRIAGE_LBL[i] for i in tm.index], tm.values, color=ACCENT, alpha=0.85)
    for i, v in enumerate(tm.values):
        ax.text(i, v + 300, f"{v/tm.sum()*100:.0f}%", ha="center", fontsize=9)
    ax.set_ylabel("presentations"); ax.grid(axis="x")
    title(ax, "03 · Triage acuity mix (ATS categories)")
    save(fig, "03_triage_mix.png")

    # 04 — 4hr performance by triage (headline)
    t4 = pres.groupby("triage_category")["met_4hr_target"].mean().mul(100)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    colors = [BAD if v < 81 else GOOD for v in t4.values]
    ax.bar([TRIAGE_LBL[i] for i in t4.index], t4.values, color=colors)
    ax.axhline(81, color=MUTED, ls="--", lw=1)
    for i, v in enumerate(t4.values):
        ax.text(i, v - 6, f"{v:.0f}%", ha="center", color="white",
                fontweight="bold", fontsize=9)
    ax.set_ylabel("% within 4hr"); ax.set_ylim(0, 105); ax.grid(axis="x")
    title(ax, "04 · The sickest patients breach the 4-hour target most")
    save(fig, "04_target_by_triage.png")

    # 05 — ED LOS distribution
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.hist(pres["ed_los_minutes"], bins=60, color=ACCENT, alpha=0.85)
    ax.axvline(240, color=BAD, ls="--", lw=1.5)
    ax.text(248, ax.get_ylim()[1] * 0.85, "240 min (4hr)", color=BAD, fontsize=9)
    ax.set_xlabel("ED length of stay (minutes)"); ax.set_ylabel("presentations")
    ax.grid(axis="x")
    title(ax, "05 · ED length-of-stay distribution")
    save(fig, "05_los_distribution.png")

    # 06 — ED LOS by triage (boxplot)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    data = [pres.loc[pres["triage_category"] == t, "ed_los_minutes"]
            for t in range(1, 6)]
    bp = ax.boxplot(data, tick_labels=[TRIAGE_LBL[i] for i in range(1, 6)],
                    patch_artist=True, showfliers=False)
    for patch in bp["boxes"]:
        patch.set_facecolor(ACCENT); patch.set_alpha(0.6)
    ax.axhline(240, color=BAD, ls="--", lw=1)
    ax.set_ylabel("ED LOS (min)"); ax.grid(axis="x")
    title(ax, "06 · ED length of stay by triage acuity")
    save(fig, "06_los_by_triage.png")

    # 07 — arrivals by hour
    h = pres.groupby(["hour", "arrival_mode"]).size().unstack(fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 3.6))
    ax.bar(h.index, h.get("Self", 0), color=ACCENT, alpha=0.8, label="Self")
    ax.bar(h.index, h.get("Ambulance", 0), bottom=h.get("Self", 0),
           color=WARN, alpha=0.9, label="Ambulance")
    ax.legend(frameon=False); ax.set_xlabel("hour of day")
    ax.set_ylabel("arrivals"); ax.grid(axis="x")
    title(ax, "07 · Arrivals by hour and mode — mid-morning peak")
    save(fig, "07_arrivals_by_hour.png")

    # 08 — hour x day-of-week heatmap
    hm = pres.pivot_table(index="hour", columns="dow", values="presentation_id",
                          aggfunc="count")
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(hm.values, aspect="auto", cmap="Blues", origin="lower")
    ax.set_xticks(range(7))
    ax.set_xticklabels(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    ax.set_yticks(range(0, 24, 2)); ax.set_yticklabels(range(0, 24, 2))
    ax.set_ylabel("hour of day"); ax.grid(False)
    fig.colorbar(im, ax=ax, label="presentations", shrink=0.8)
    title(ax, "08 · Demand heatmap — hour × day of week")
    save(fig, "08_demand_heatmap.png")

    # 09 — arrival mode share by triage
    mode = (pres.groupby(["triage_category", "arrival_mode"]).size()
            .unstack(fill_value=0))
    mode_pct = mode.div(mode.sum(axis=1), axis=0) * 100
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.bar([TRIAGE_LBL[i] for i in mode_pct.index], mode_pct["Ambulance"],
           color=WARN, alpha=0.9)
    for i, v in enumerate(mode_pct["Ambulance"].values):
        ax.text(i, v + 1.5, f"{v:.0f}%", ha="center", fontsize=9)
    ax.set_ylabel("% arriving by ambulance"); ax.grid(axis="x")
    title(ax, "09 · Ambulance share rises steeply with acuity")
    save(fig, "09_ambulance_by_triage.png")

    # 10 — LWBS by presenting group
    lw = (pres.groupby("presenting_group")["left_without_being_seen"]
          .mean().mul(100).sort_values())
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.barh(lw.index, lw.values, color=BAD, alpha=0.85)
    for i, v in enumerate(lw.values):
        ax.text(v + 0.05, i, f"{v:.1f}%", va="center", fontsize=8.5)
    ax.set_xlabel("LWBS rate %"); ax.grid(axis="y")
    title(ax, "10 · Left-without-being-seen rate by presenting group")
    save(fig, "10_lwbs_by_group.png")

    # 11 — admission rate by triage
    ar = pres.groupby("triage_category")["admitted"].mean().mul(100)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot([TRIAGE_LBL[i] for i in ar.index], ar.values, marker="o",
            color=ACCENT, lw=2)
    ax.fill_between([TRIAGE_LBL[i] for i in ar.index], ar.values, 0,
                    color=ACCENT, alpha=0.1)
    for i, v in enumerate(ar.values):
        ax.text(i, v + 3, f"{v:.0f}%", ha="center", fontsize=9)
    ax.set_ylabel("admission rate %"); ax.set_ylim(0, 90); ax.grid(axis="x")
    title(ax, "11 · Admission rate by triage acuity")
    save(fig, "11_admission_by_triage.png")

    # 12 — inpatient LOS distribution
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.hist(adm["los_days"], bins=40, color=GOOD, alpha=0.8)
    ax.axvline(adm["los_days"].median(), color=BAD, ls="--", lw=1.5,
               label=f"median {adm['los_days'].median():.1f} d")
    ax.legend(frameon=False)
    ax.set_xlabel("inpatient length of stay (days)"); ax.set_ylabel("admissions")
    ax.grid(axis="x")
    title(ax, "12 · Inpatient length-of-stay distribution")
    save(fig, "12_inpatient_los.png")

    # 13 — readmission by diagnosis
    rd = (adm.groupby("diagnosis_group")["readmitted_28d"].mean()
          .mul(100).sort_values())
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.barh(rd.index, rd.values, color=ACCENT)
    for i, v in enumerate(rd.values):
        ax.text(v + 0.1, i, f"{v:.1f}%", va="center", fontsize=8.5)
    ax.set_xlabel("28-day readmission rate %"); ax.grid(axis="y")
    title(ax, "13 · 28-day readmission rate by diagnosis group")
    save(fig, "13_readmission_by_dx.png")

    # 14 — Pareto of frequent presenters
    vpp = pres.groupby("patient_id").size().sort_values(ascending=False)
    cum = np.cumsum(vpp.values) / vpp.sum() * 100
    share_patients = np.arange(1, len(vpp) + 1) / len(vpp) * 100
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.plot(share_patients, cum, color=ACCENT, lw=2.2)
    ax.plot([0, 100], [0, 100], color=MUTED, ls="--", lw=1)
    top1_share = cum[int(len(vpp) * 0.01)]
    ax.axvline(1, color=BAD, ls=":", lw=1.2)
    ax.annotate(f"top 1% of patients\n= {top1_share:.1f}% of visits",
                xy=(1, top1_share), xytext=(18, top1_share - 8),
                fontsize=9, color=BAD,
                arrowprops=dict(arrowstyle="->", color=BAD))
    ax.set_xlabel("% of patients (ranked by visits)")
    ax.set_ylabel("cumulative % of presentations")
    title(ax, "14 · A small cohort drives a large share of demand")
    save(fig, "14_frequent_presenters_pareto.png")

    # ---- print key stats used in the report ----
    print("\nKey statistics:")
    print(f"  presentations: {len(pres):,}  |  admissions: {len(adm):,}")
    print(f"  4-hr target overall: {pres['met_4hr_target'].mean():.1%}")
    print(f"  4-hr target T1/T2:   {pres.loc[pres.triage_category<=2,'met_4hr_target'].mean():.1%}")
    print(f"  LWBS overall:        {pres['left_without_being_seen'].mean():.2%}")
    print(f"  admission rate:      {pres['admitted'].mean():.1%}")
    print(f"  median inpatient LOS:{adm['los_days'].median():.1f} d")
    print(f"  readmission overall: {adm['readmitted_28d'].mean():.1%}")
    print(f"  top1% share of visits:{top1_share:.1f}%")


if __name__ == "__main__":
    main()
