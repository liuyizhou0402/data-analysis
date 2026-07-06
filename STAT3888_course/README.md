# STAT3888 — Statistical Machine Learning · Lecture Series

Self-contained HTML lecture decks for **STAT3888 (Statistical Machine Learning)**,
University of Sydney. Built to support the interdisciplinary NUTM3888 nutrition project.

**Open `index.html`** to browse all 24 lectures. Each deck opens in any browser
— navigate with the ← → arrow keys, and use the browser's *Print → Save as PDF*
to produce handouts.

## Structure

| File | Purpose |
|------|---------|
| `index.html` | Landing page / lecture index |
| `lessonNN.html` | Individual lecture decks (self-contained) |
| `figures/` | Generated figures (matplotlib) |
| `slides.py` | Slide-deck framework (theme, layout helpers) |
| `figs_*.py` | Figure generators per lecture batch |
| `build_*.py` | Deck content + assembly per lecture batch |

## 24-lecture plan

**Part I — Foundations & Unsupervised Learning (L1–9):** intro, data cleaning,
clustering (k-means, GMM, hierarchical), PCA & dimension reduction.
**Part II — Supervised Learning (L10–20):** logistic & penalised regression,
discriminant analysis, k-NN, trees, random forests/boosting, neural networks, SVMs.
**Part III — Evaluation & Communication (L21–24):** model evaluation, graphical
models, the project workflow, and writing/presenting results.

## Rebuilding

```bash
pip install matplotlib numpy scikit-learn
python figs_01_04.py     # regenerate figures
python build_01_04.py    # rebuild lesson01–04.html
```

**Status:** Lectures 01–04 complete. Remaining lectures in progress.
