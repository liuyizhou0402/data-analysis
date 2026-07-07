# STAT3888 — Statistical Machine Learning · Lecture PowerPoints

Full **60-minute PowerPoint (.pptx)** lectures for **STAT3888 (Statistical Machine
Learning)**, University of Sydney, built to support the interdisciplinary NUTM3888
nutrition project. Open the `.pptx` files directly in PowerPoint, Keynote or Google Slides.

## Ready now (Lectures 01–08) — every deck 60+ slides

| File | Slides | Topic |
|------|:------:|-------|
| `Lecture01_Introduction.pptx` | 61 | Introduction to Statistical ML & the project |
| `Lecture02_DataCleaning.pptx` | 60 | Data cleaning & preprocessing |
| `Lecture03_IntroClustering.pptx` | 60 | Introduction to clustering |
| `Lecture04_Kmeans.pptx` | 60 | K-means clustering |
| `Lecture05_GMM.pptx` | 62 | Model-based clustering (Gaussian mixtures) |
| `Lecture06_Hierarchical.pptx` | 60 | Hierarchical clustering |
| `Lecture07_PCA_Background.pptx` | 60 | PCA background (linear algebra) |
| `Lecture08_PCA.pptx` | 60 | Principal component analysis |

Each deck is a genuine 60-minute lecture (**60+ slides**): title, agenda, section
dividers, definitions, concept build-up, **custom matplotlib figures**, formulae, R
code, in-class MCQ checkpoints, worked examples, exercises, and a summary with a
look-ahead. Consistent USYD theme (16:9).

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
| `pptx_deck.py` | Reusable PowerPoint framework (theme, layouts, slide types) |
| `figs_01_04.py`, `figs_pptx_01_04.py`, `figs_05_08.py` | matplotlib figure generators |
| `build_pptx_01_04.py`, `build_pptx_05_06.py`, `build_pptx_07_08.py` | Lecture content + deck assembly |
| `slides.py` | Shared palette + figure-save helpers |
| `figures/` | Generated PNG figures |

### Rebuilding

```bash
pip install python-pptx matplotlib numpy scikit-learn scipy pillow
python figs_01_04.py         # base figures (L1-4)
python figs_pptx_01_04.py    # extra figures (L1-4)
python figs_05_08.py         # figures for L5-8
python build_pptx_01_04.py   # -> Lecture01..04 .pptx
python build_pptx_05_06.py   # -> Lecture05..06 .pptx
python build_pptx_07_08.py   # -> Lecture07..08 .pptx
```

**Status:** Lectures 01–08 complete (all 60+ slides). Lectures 09–24 to follow in batches.
