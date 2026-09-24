# Portfolio PDFs

Submission-ready PDF write-ups of the two analytics projects in this repository —
for job applications that ask for a work sample rather than a repository link.

| Document | Project | Pages | Size |
|:---|:---|:---:|:---:|
| [**ED_Patient_Flow_Analytics_Yizhou_Liu.pdf**](ED_Patient_Flow_Analytics_Yizhou_Liu.pdf) | [healthcare-ed-analytics](../healthcare-ed-analytics) | 12 | 0.79 MB |
| [**Ads_Revenue_Analytics_Yizhou_Liu.pdf**](Ads_Revenue_Analytics_Yizhou_Liu.pdf) | [ads-revenue-analytics](../ads-revenue-analytics) | 7 | 0.35 MB |

Both are well under the 3 MB limit most application portals impose, and each is
self-contained: headline finding, the evidence behind it, every chart with its
interpretation, costed recommendations, and a stated list of what the analysis
*cannot* tell you.

## Rebuilding them

The PDFs are generated, not hand-made — every number and figure comes from the
committed analysis output, so they stay in sync with the projects.

```bash
pip install reportlab
python portfolio/build_ed_report.py     # → ED_Patient_Flow_Analytics_Yizhou_Liu.pdf
python portfolio/build_ads_report.py    # → Ads_Revenue_Analytics_Yizhou_Liu.pdf
```

| File | What |
|:---|:---|
| [`pdfkit.py`](pdfkit.py) | Shared layout toolkit — palette, type scale, tables, figures, callouts, page chrome. Owns every visual decision so both documents read as one set. |
| [`build_ed_report.py`](build_ed_report.py) | ED & patient flow document — content only |
| [`build_ads_report.py`](build_ads_report.py) | Advertising revenue document — content only |

Figures are read directly from each project's `analysis/figures/` and
`dashboard/` directories. Re-run a project's `eda.py` / `build_dashboard.py` and
rebuild to pick up new output.
