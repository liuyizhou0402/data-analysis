# Data — synthetic, reproducible

All CSVs here are produced by [`generate_data.py`](generate_data.py) from a
fixed random seed (`42`), so results are fully reproducible.

**The data is 100% synthetic. It contains no real patient records.** Distributions
are loosely calibrated to publicly reported Australian ED patterns (triage mix,
4-hour target performance, winter respiratory surge, 28-day readmission rates)
purely to make the analysis realistic for a portfolio.

| File | Grain | Rows |
|:-----|:------|-----:|
| `patients.csv` | one row per patient (dimension) | 12,000 |
| `ed_presentations.csv` | one row per ED presentation (fact) | 54,837 |
| `admissions.csv` | one row per inpatient admission (fact) | 11,045 |

Regenerate with:

```bash
pip install -r ../requirements.txt
python generate_data.py
```
