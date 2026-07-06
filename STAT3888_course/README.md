# STAT3888 — Statistical Machine Learning · Lecture PowerPoints

Full **60-minute PowerPoint (.pptx)** lectures for **STAT3888 (Statistical Machine
Learning)**, University of Sydney, built to support the interdisciplinary NUTM3888
nutrition project. Open the `.pptx` files directly in PowerPoint, Keynote or Google Slides.

## Ready now (Lectures 01–04)

| File | Slides | Topic |
|------|:------:|-------|
| `Lecture01_Introduction.pptx` | 29 | Introduction to Statistical ML & the project |
| `Lecture02_DataCleaning.pptx` | 24 | Data cleaning & preprocessing |
| `Lecture03_IntroClustering.pptx` | 26 | Introduction to clustering |
| `Lecture04_Kmeans.pptx` | 25 | K-means clustering |

Each deck is a genuine 60-minute lecture: title, agenda, section dividers, concept
build-up, **custom matplotlib figures**, formulae, R code, in-class exercises, and a
summary with a look-ahead. Consistent USYD theme (16:9).

## 24-lecture plan

**Part I — Foundations & Unsupervised Learning (L1–9):** intro, data cleaning,
clustering (k-means, GMM, hierarchical), PCA & dimension reduction.
**Part II — Supervised Learning (L10–20):** logistic & penalised regression,
discriminant analysis, k-NN, trees, random forests/boosting, neural networks, SVMs.
**Part III — Evaluation & Communication (L21–24):** model evaluation, graphical
models, the project workflow, and writing/presenting results.

## How it's built

| File | Purpose |
|------|---------|
| `pptx_deck.py` | Reusable PowerPoint framework (theme, layouts, helpers) |
| `figs_01_04.py`, `figs_pptx_01_04.py` | matplotlib figure generators |
| `build_pptx_01_04.py` | Lecture content + deck assembly |
| `slides.py` | Shared palette + figure-save helpers |
| `figures/` | Generated PNG figures |

### Rebuilding

```bash
pip install python-pptx matplotlib numpy scikit-learn scipy pillow
python figs_01_04.py         # base figures
python figs_pptx_01_04.py    # extra figures for the full decks
python build_pptx_01_04.py   # -> Lecture01..04 .pptx
```

**Status:** Lectures 01–04 complete. Lectures 05–24 to follow in batches.
