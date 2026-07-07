# -*- coding: utf-8 -*-
"""STAT3888 lectures 09 (dimension reduction) & 10 (supervised intro) — 60+ slide decks."""
import os
from pptx_deck import Deck, HERE
from pptx import Presentation
F = lambda name: os.path.join(HERE, "figures", name)

# ================================================================= LECTURE 09
def lecture09():
    d = Deck(9, "Dimension Reduction Beyond PCA")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Dimension Reduction Beyond PCA: MDS, t-SNE & UMAP",
            "When linear PCA isn't enough — reducing dimensions that preserve distances or reveal "
            "non-linear structure, and how to read (and misread) the pictures.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("Recap: what PCA does and where it stops", 0),
        ("Multidimensional scaling (MDS): preserve distances", 0),
        ("t-SNE: reveal non-linear neighbourhoods", 0),
        ("UMAP: the modern alternative", 0),
        ("Choosing and comparing methods", 0),
        ("Practice in R, pitfalls and honest interpretation", 0),
    ], i())
    d.bullets("Recap", "PCA in one breath", [
        ("PCA finds orthogonal directions of **maximum variance**", 0),
        ("It is **linear** — new axes are straight-line combinations of variables", 0),
        ("Great for compression, denoising and visualising **linear** structure", 0),
        ("But real data often bends…", 0),
    ], i())
    d.checkpoint("PCA is fundamentally a … method.",
        ["Non-linear", "Supervised", "Linear", "Probabilistic"], 2, i(),
        explain="PCA builds components as linear combinations of the original variables — it can only "
                "capture linear structure.")

    d.section("Part 1", "Why go beyond PCA?")
    d.big_point("The limitation", "PCA can only rotate and stretch — it cannot 'unroll' data that "
                "lies on a curved surface.",
                i(), sub="If the interesting structure is non-linear, PCA's flat projection smears it "
                         "together.")
    d.figure("Curved data", "Data on a manifold", F("L09_manifold.png"), i(),
             caption="The 'Swiss roll': points live on a curved 2-D sheet embedded in 3-D. The true "
                     "structure (right) is only revealed by 'unrolling' it — PCA can't.")
    d.definition("Definition", "Manifold",
                 "A **manifold** is a lower-dimensional surface (possibly curved) on which the data "
                 "approximately lies within a higher-dimensional space.",
                 i(), extra=["The 'manifold hypothesis': real data often lies near a low-dim manifold",
                             "Non-linear methods try to recover its intrinsic coordinates",
                             "PCA sees only the flat, linear shadow"])
    d.figure("The payoff", "Linear vs non-linear on real data", F("L09_pca_vs_tsne.png"), i(),
             caption="64-D handwritten digits in 2-D: PCA (left) overlaps the classes; t-SNE (right) "
                     "pulls them into clear islands.")
    d.two_col("Two goals, two tools", "What are you reducing for?",
              left_head="Faithful geometry",
              left=["Preserve **actual distances**",
                    "Good for quantitative structure",
                    "→ MDS (and PCA)"],
              right_head="Reveal groupings",
              right=["Preserve **local neighbourhoods**",
                     "Great for spotting clusters",
                     "→ t-SNE, UMAP"],
              idx=i())

    d.section("Part 2", "Multidimensional scaling (MDS)")
    d.definition("Definition", "Multidimensional scaling",
                 "**MDS** places points in a low-dimensional space so that their pairwise distances "
                 "match the original distances as closely as possible.",
                 i(), extra=["Input: a distance / dissimilarity matrix",
                             "Output: coordinates (e.g. 2-D) that reproduce those distances",
                             "Classical (metric) MDS on Euclidean distance ≈ PCA"])
    d.figure("The idea", "Reconstruct a map from distances", F("L09_mds.png"), i(),
             caption="Given only pairwise distances, MDS recovers a configuration that preserves them — "
                     "like rebuilding a map from a table of city-to-city distances.")
    d.formula("Objective", "MDS minimises stress",
              "Stress = Σ_{i<j} ( d_{ij} − ‖zᵢ − zⱼ‖ )²",
              ["**d_{ij}** — original dissimilarity between i and j",
               "**‖zᵢ − zⱼ‖** — distance in the low-dim embedding",
               "Minimising stress = matching the two as well as possible"],
              i(), note="Low stress = a faithful low-dimensional picture.")
    d.bullets("Flavours", "Metric vs non-metric MDS", [
        ("**Metric MDS** — preserves the actual distance values", 0),
        ("**Non-metric MDS** — preserves only the **rank order** of distances", 0),
        ("Use non-metric when only ordinal dissimilarities are meaningful", 0),
        ("Works with **any** distance — a big advantage over raw PCA", 0),
    ], i())
    d.checkpoint("MDS takes as its input primarily…",
        ["The raw data matrix only", "A matrix of pairwise distances/dissimilarities",
         "Class labels", "Principal components"], 1, i(),
        explain="MDS works from a dissimilarity matrix, arranging points to reproduce those "
                "dissimilarities in low dimensions.")

    d.section("Part 3", "t-SNE")
    d.definition("Definition", "t-SNE",
                 "**t-distributed Stochastic Neighbour Embedding** places points so that **near "
                 "neighbours stay near**, emphasising local structure for visualisation.",
                 i(), extra=["Converts distances into neighbour **probabilities**",
                             "Matches those probabilities in 2-D using a heavy-tailed (t) distribution",
                             "Superb at revealing clusters; a visualisation tool, not a general reducer"])
    d.steps("How it works", "t-SNE in four ideas", [
        ("Neighbours", "for each point, define probabilities of picking each other point as a neighbour"),
        ("Low-dim mirror", "define similar probabilities in the 2-D map"),
        ("Match", "move points to make the two probability sets agree (minimise KL divergence)"),
        ("Heavy tails", "the t-distribution stops distant points crowding the centre"),
    ], i())
    d.figure("Tuning", "Perplexity changes the picture", F("L09_perplexity.png"), i(),
             caption="Perplexity ≈ the effective number of neighbours. Too small fragments clusters; "
                     "too large merges them. Always try several values.")
    d.bullets("Reading t-SNE", "What you may and may NOT conclude", [
        ("**Do** trust: which points form tight local groups", 0),
        ("**Don't** trust: the **sizes** of clusters — they're distorted", 0),
        ("**Don't** trust: **distances between** clusters — not meaningful", 0),
        ("**Don't** trust: the **global** layout — it can be arbitrary", 0),
    ], i())
    d.big_point("A famous warning", "In t-SNE, cluster sizes and between-cluster distances are "
                "essentially meaningless — only local neighbourhoods are reliable.",
                i(), sub="Beautiful plots invite over-interpretation. Report it as exploratory.")
    d.checkpoint("In a t-SNE plot, two clusters are far apart. You may conclude…",
        ["They are very different", "Nothing reliable — t-SNE distorts between-cluster distance",
         "One is larger", "They will never merge"], 1, i(),
        explain="t-SNE preserves local neighbourhoods, not global distances, so the gap between two "
                "clusters carries little meaning.")

    d.section("Part 4", "UMAP & the modern toolkit")
    d.definition("Definition", "UMAP",
                 "**Uniform Manifold Approximation and Projection** is a newer non-linear reducer that "
                 "is faster than t-SNE and better preserves some global structure.",
                 i(), extra=["Built on manifold theory and graph layout",
                             "Scales to large data; increasingly the default",
                             "Still a visualisation tool — read with the same caution"])
    d.table("Compare", "The dimension-reduction toolkit",
            ["Method", "Type", "Preserves", "Main use"],
            [["PCA", "linear", "variance / global", "compress, preprocess"],
             ["MDS", "linear*", "distances", "faithful geometry"],
             ["t-SNE", "non-linear", "local neighbours", "cluster visualisation"],
             ["UMAP", "non-linear", "local + some global", "fast visualisation"]],
            i(), col_widths=[1.9,2.0,3.4,4.2])
    d.two_col("t-SNE vs UMAP", "Choosing between the two",
              left_head="t-SNE",
              left=["Excellent local structure",
                    "Slower on big data",
                    "Global layout unreliable",
                    "Very widely cited"],
              right_head="UMAP",
              right=["Fast, scales well",
                     "Keeps more global structure",
                     "Can embed new points",
                     "Now often preferred"],
              idx=i())

    d.section("Part 5", "In practice")
    d.code("R", "Dimension reduction in a few lines", [
        "X <- scale(diet_numeric)",
        "",
        "# MDS",
        "mds <- cmdscale(dist(X), k = 2)",
        "",
        "# t-SNE",
        "library(Rtsne)",
        "ts <- Rtsne(X, perplexity = 30)$Y",
        "",
        "# UMAP",
        "library(umap); um <- umap(X)$layout",
    ], i())
    d.steps("Workflow", "A sensible reduction pipeline", [
        ("Clean & standardise", "as always for distance-based methods"),
        ("PCA first", "reduce noise; often feed ~30 PCs into t-SNE/UMAP"),
        ("Non-linear embed", "t-SNE or UMAP for the 2-D picture"),
        ("Colour by metadata", "overlay a known group to interpret"),
        ("Cross-check", "does clustering on the data agree with the picture?"),
    ], i(), note="Running t-SNE/UMAP on PCA scores is standard — faster and less noisy.")
    d.bullets("Interpreting honestly", "Rules for your report", [
        ("Label the axes as **arbitrary** for t-SNE/UMAP", 0),
        ("State the **perplexity / parameters** you used", 0),
        ("Show that clusters are **stable** across runs / settings", 0),
        ("Back up visual clusters with a **quantitative** method", 0),
    ], i())

    d.section("Part 6", "Pitfalls, applications & wrap-up")
    d.bullets("Pitfalls", "Where students go wrong", [
        ("Treating a t-SNE plot as **quantitative** truth", 0),
        ("Forgetting to **standardise** or to set a **seed**", 0),
        ("Reading meaning into cluster **sizes / gaps**", 0),
        ("Using non-linear embeddings as model **features** (they don't generalise well)", 0),
    ], i())
    d.two_col("When to use which", "A quick decision guide",
              left_head="Reach for PCA/MDS",
              left=["You need faithful distances",
                    "You'll model on the output",
                    "Interpretability matters"],
              right_head="Reach for t-SNE/UMAP",
              right=["You're **exploring** for clusters",
                     "Structure looks non-linear",
                     "The output is a **picture**, not features"],
              idx=i())
    d.bullets("Applications", "Non-linear reduction in the wild", [
        ("**Single-cell genomics** — UMAP of thousands of cell types", 0),
        ("**Metabolomics** — visualising participant subtypes", 0),
        ("**Image / text embeddings** — mapping high-dim features", 0),
        ("Relevant to your project's **exploratory** phase", 0),
    ], i())
    d.definition("Definition", "Intrinsic dimension",
                 "The **intrinsic dimension** is the true number of coordinates needed to describe the "
                 "data, often far smaller than the number of variables.",
                 i(), extra=["The manifold hypothesis says this is usually small",
                             "Dimension reduction tries to recover it",
                             "Estimating it guides how many components to keep"])
    d.checkpoint("You need reduced features to feed into a classifier that must work on new data. Best choice?",
        ["t-SNE", "UMAP", "PCA", "A random projection"], 2, i(),
        explain="PCA gives a fixed, reproducible linear map you can apply to new data. t-SNE has no "
                "clean out-of-sample mapping and is meant for visualisation.")
    d.exercise("Reduce and interpret", [
        "Standardise the nutrition data and run PCA, t-SNE (perplexity 5, 30, 50) and UMAP.",
        "Which methods show clear participant groups? Are they stable across t-SNE settings?",
        "Colour the embeddings by a health outcome — do groups align with it?",
        "Write one sentence you could defend about the structure, and one you could NOT.",
    ], i(), hint="Defensible: 'points form tight local neighbourhoods'. Not defensible: 'cluster A is "
                 "twice as big / far from B' in t-SNE.")
    d.bullets("Key ideas recap", "Hold onto these", [
        ("**MDS** preserves distances; **t-SNE/UMAP** preserve local neighbourhoods", 0),
        ("Non-linear methods reveal structure PCA **can't**", 0),
        ("Their plots are **exploratory** — sizes & gaps are unreliable", 0),
        ("**PCA-then-t-SNE/UMAP**, standardise, set seeds, validate", 0),
    ], i())
    d.bullets("Further reading", "To go deeper", [
        ("van der Maaten & Hinton (2008) — the t-SNE paper", 0),
        ("McInnes et al. (2018) — UMAP", 0),
        ("*Distill.pub* — 'How to Use t-SNE Effectively'", 0),
    ], i())

    d.section("Part 7", "More methods & diagnostics")
    d.definition("Definition", "Isomap",
                 "**Isomap** is MDS on **geodesic** distances — distances measured *along* the manifold "
                 "rather than straight through space.",
                 i(), extra=["Builds a neighbour graph, then shortest paths approximate geodesics",
                             "Unrolls curved manifolds like the Swiss roll",
                             "A bridge between MDS and non-linear methods"])
    d.bullets("The wider family", "Manifold-learning methods", [
        ("**LLE** (Locally Linear Embedding) — preserve local linear reconstructions", 0),
        ("**Kernel PCA** — PCA in a transformed feature space", 0),
        ("**Spectral embedding** — eigenvectors of a similarity graph", 0),
        ("**Autoencoders** — neural networks that learn a compressed code (preview of NNs)", 0),
    ], i())
    d.definition("Definition", "Shepard diagram",
                 "A **Shepard diagram** plots embedded distances against original distances to judge how "
                 "faithfully an embedding preserves them.",
                 i(), extra=["Points near the diagonal = distances well preserved",
                             "Scatter = distortion",
                             "A quick honesty check for MDS"])
    d.bullets("Goodness of fit", "Is the picture trustworthy?", [
        ("**Stress** (MDS) — lower is better; report it", 0),
        ("**Shepard diagram** — visual check of distance preservation", 0),
        ("**Stability** — rerun with new seeds; do groups persist?", 0),
        ("**Agreement** — does clustering confirm the visual groups?", 0),
    ], i())
    d.bullets("Computational cost", "Practical considerations", [
        ("Classical MDS & PCA — fast (linear algebra)", 0),
        ("t-SNE — **O(n²)** naively; slow for large n", 0),
        ("UMAP — much faster, scales to big data", 0),
        ("**PCA-first** cuts cost and noise for all of them", 0),
    ], i())
    d.checkpoint("Which method is designed to 'unroll' a curved manifold using distances along it?",
        ["PCA", "Isomap", "Classical MDS", "Random projection"], 1, i(),
        explain="Isomap uses geodesic (along-manifold) distances, letting it unroll curved structures "
                "that straight-line methods cannot.")

    d.section("Part 8", "Consolidation & a worked case")
    d.big_point("The mental model", "PCA asks 'which directions vary most?'; MDS asks 'can I preserve "
                "distances?'; t-SNE/UMAP ask 'who are each point's neighbours?'",
                i(), sub="Three different questions — pick the one your problem is really asking.")
    d.table("Decision guide", "Picking a reducer, expanded",
            ["Goal", "Data", "Use"],
            [["Compress / preprocess", "linear-ish", "PCA"],
             ["Preserve distances", "any distance", "MDS / Isomap"],
             ["Explore clusters (viz)", "non-linear", "t-SNE / UMAP"],
             ["Features for a model", "any", "PCA (reproducible map)"]],
            i(), col_widths=[3.3,2.8,5.4])
    d.bullets("Case study", "Metabolite subtypes, exploratory phase", [
        ("Standardise 40 metabolites; run **PCA** → keep 15 PCs (90% variance)", 0),
        ("Feed PCs into **UMAP**; colour by a clinical variable", 0),
        ("See 3 apparent groups → **confirm** with GMM on the PCs", 0),
        ("Report UMAP as **exploratory**, GMM clusters as the quantitative claim", 0),
    ], i())
    d.two_col("Do & don't", "Non-linear reduction hygiene",
              left_head="Do",
              left=["PCA-first, standardise, set seeds",
                    "Try several perplexities",
                    "Validate with clustering",
                    "Report parameters"],
              right_head="Don't",
              right=["Read sizes/gaps as real",
                     "Use t-SNE coords as features",
                     "Trust one run",
                     "Skip the honesty checks"],
              idx=i())
    d.exercise("Critique a figure", [
        "A paper shows a t-SNE plot and claims 'group A is far more diverse than group B'.",
        "Why is that claim unsupportable from t-SNE alone?",
        "What analysis *would* support a claim about within-group diversity?",
        "Rewrite the caption to be defensible.",
    ], i(), hint="t-SNE distorts cluster size/spread; measure diversity with variance/pairwise distances "
                 "in the original (or PCA) space.")
    d.definition("Definition", "Out-of-sample extension",
                 "The ability to project **new** points into an existing embedding without refitting.",
                 i(), extra=["PCA & UMAP support it cleanly (a reusable mapping)",
                             "Standard t-SNE does **not** — a key limitation for pipelines",
                             "Matters when you'll see new data (almost always)"])
    d.checkpoint("You need to embed NEW participants into an existing 2-D map next month. Avoid…",
        ["PCA", "UMAP", "Standard t-SNE", "Isomap with a mapping"], 2, i(),
        explain="Standard t-SNE has no clean out-of-sample extension; PCA and UMAP provide reusable "
                "mappings for new points.")
    d.bullets("Chapter checklist", "Before moving on, you can…", [
        ("Explain why PCA fails on curved manifolds", 0),
        ("Describe MDS, t-SNE and UMAP and their goals", 0),
        ("List what you may NOT read from a t-SNE plot", 0),
        ("Give a PCA-first, seed-set, validated workflow", 0),
    ], i())
    d.definition("Definition", "Autoencoder (preview)",
                 "An **autoencoder** is a neural network trained to compress data to a small 'code' and "
                 "reconstruct it — a non-linear generalisation of PCA.",
                 i(), extra=["The bottleneck layer is the reduced representation",
                             "Linear autoencoder ≈ PCA; non-linear ones capture curved structure",
                             "We meet neural networks in Lectures 17–18"])
    d.bullets("Applications recap", "Where reduction pays off", [
        ("**Visualisation** of high-dim participant data", 0),
        ("**Preprocessing** before clustering / classification", 0),
        ("**Denoising** by dropping low-variance directions", 0),
        ("**Compression** for storage and speed", 0),
    ], i())
    d.big_point("One line to remember", "Reduce dimensions to *see* and to *simplify* — but always "
                "check that the reduced picture tells the truth.",
                i(), sub="A pretty embedding is a hypothesis, not a result.")
    d.summary([
        "PCA is linear; **MDS, t-SNE and UMAP** handle distances and non-linear structure.",
        "**MDS** preserves distances; **t-SNE/UMAP** preserve local neighbourhoods for visualisation.",
        "t-SNE/UMAP plots are **exploratory** — cluster sizes and gaps are not trustworthy.",
        "Standardise, often **PCA-first**, set a seed, and **validate** visual structure quantitatively.",
    ], i(), nextup="Lecture 10 — Introduction to supervised learning: prediction, error and validation.")
    out=os.path.join(HERE,"Lecture09_DimReduction.pptx"); d.save(out); return out


# ================================================================= LECTURE 10
def lecture10():
    d = Deck(10, "Introduction to Supervised Learning")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Introduction to Supervised Learning",
            "The framework behind every prediction method: inputs and targets, loss, training vs "
            "generalisation, the bias–variance trade-off, and cross-validation.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("From unsupervised to supervised learning", 0),
        ("The setup: features, target, and the function f", 0),
        ("Regression vs classification; loss functions", 0),
        ("Training error vs test error", 0),
        ("Overfitting and the bias–variance trade-off", 0),
        ("Cross-validation and honest model assessment", 0),
        ("The tidymodels workflow", 0),
    ], i())
    d.bullets("Where we are", "A turning point in the unit", [
        ("Weeks 1–3: **unsupervised** — structure without labels (clustering, PCA)", 0),
        ("Weeks 4–7: **supervised** — predicting a known target Y", 0),
        ("Today builds the **framework** every later method plugs into", 0),
        ("Master this and logistic regression, trees, SVMs all make sense", 0),
    ], i())
    d.checkpoint("What defines a supervised learning problem?",
        ["Many variables", "A known target/label Y to predict", "No labels", "Only numeric data"], 1, i(),
        explain="Supervised learning has a target variable Y; the goal is to learn to predict it from "
                "features X.")

    d.section("Part 1", "The supervised setup")
    d.definition("Definition", "Supervised learning",
                 "Learn a function **f** mapping input features **X** to a target **Y**, using labelled "
                 "examples, so that f predicts Y well on **new** data.",
                 i(), extra=["**X** — predictors / features (the columns you know)",
                             "**Y** — target / label (what you want to predict)",
                             "**f** — the fitted model; Ŷ = f(X)"])
    d.formula("The model", "Signal plus noise",
              "Y = f(X) + ε",
              ["**f(X)** — the true systematic relationship we try to learn",
               "**ε** — irreducible noise (measurement error, randomness)",
               "We can shrink error toward, but never below, the noise floor"],
              i())
    d.two_col("Two tasks", "Regression vs classification",
              left_head="Regression",
              left=["Y is **numeric**",
                    "e.g. predict fasting glucose",
                    "Error: squared / absolute",
                    "Output: a number"],
              right_head="Classification",
              right=["Y is **categorical**",
                     "e.g. diabetic / not",
                     "Error: misclassification, log-loss",
                     "Output: a class or probability"],
              idx=i())
    d.bullets("Examples in nutrition", "Same framework, many questions", [
        ("**Regression**: body-fat % from intake variables", 0),
        ("**Classification**: metabolic-syndrome yes/no", 0),
        ("**Probability**: chance of high cholesterol", 0),
        ("**Ranking**: which foods most raise glucose", 0),
    ], i())

    d.section("Part 2", "Measuring error: loss")
    d.definition("Definition", "Loss function",
                 "A **loss function** measures how wrong a prediction is; fitting a model means "
                 "**minimising average loss**.",
                 i(), extra=["Regression: squared error (y − ŷ)²",
                             "Classification: 0/1 misclassification, or log-loss",
                             "The loss encodes what 'a good prediction' means"])
    d.formula("Regression loss", "Mean squared error",
              "MSE = (1/n) Σᵢ ( yᵢ − ŷᵢ )²",
              ["Averages the squared prediction errors",
               "Squaring punishes **large** errors heavily",
               "Its square root, RMSE, is on the original scale"],
              i())
    d.bullets("Classification loss", "Ways to be wrong", [
        ("**Misclassification rate** — fraction predicted into the wrong class", 0),
        ("**Log-loss / cross-entropy** — punishes confident wrong probabilities", 0),
        ("**Cost-sensitive** — some errors matter more (missing a disease!)", 0),
        ("Choose the loss to match the **real-world cost**", 0),
    ], i())

    d.section("Part 3", "Training vs test error")
    d.figure("The split", "Train on some, test on the rest", F("L10_train_test.png"), i(),
             caption="Fit the model on the training set; estimate real-world performance on a held-out "
                     "test set it never saw.")
    d.definition("Definition", "Generalisation",
                 "**Generalisation** is a model's performance on **new, unseen** data — the only "
                 "performance that actually matters.",
                 i(), extra=["Training error is optimistic — the model has seen that data",
                             "Test error estimates generalisation",
                             "The gap between them signals overfitting"])
    d.big_point("The cardinal rule", "Never evaluate a model on data it was trained on — and never let "
                "test data influence training.",
                i(), sub="Break this and every performance number becomes a fantasy.")
    d.bullets("Why training error misleads", "The optimism of hindsight", [
        ("A flexible model can **memorise** the training data → ~0 training error", 0),
        ("That says nothing about **new** data", 0),
        ("Test error can be far worse — the honest number", 0),
        ("More flexibility always lowers **training** error, not always **test** error", 0),
    ], i())

    d.section("Part 4", "Overfitting & bias–variance")
    d.figure("Complexity", "Underfit, good fit, overfit", F("L10_complexity_fit.png"), i(),
             caption="Too simple misses the pattern (bias); too complex chases noise (variance). The "
                     "middle generalises best.")
    d.definition("Definition", "Bias & variance",
                 "**Bias** is error from wrong assumptions (too simple); **variance** is error from "
                 "sensitivity to the particular training sample (too complex).",
                 i(), extra=["High bias → underfitting",
                             "High variance → overfitting",
                             "Total error = bias² + variance + irreducible noise"])
    d.figure("The trade-off", "Bias–variance decomposition", F("L10_bias_variance.png"), i(),
             caption="As complexity grows, bias falls but variance rises. Test error is U-shaped — the "
                     "minimum is the sweet spot.")
    d.formula("Decomposition", "Expected test error splits three ways",
              "E[error] = bias² + variance + σ²",
              ["**bias²** — systematic error from an over-simple model",
               "**variance** — instability across training samples",
               "**σ²** — irreducible noise you can never remove"],
              i(), note="Model selection is the art of balancing bias against variance.")
    d.checkpoint("A very flexible model has near-zero training error but poor test error. It suffers from…",
        ["High bias", "High variance (overfitting)", "Irreducible noise", "Underfitting"], 1, i(),
        explain="Low training but high test error = the model fits noise in the training sample: high "
                "variance / overfitting.")

    d.section("Part 5", "Cross-validation")
    d.definition("Definition", "Cross-validation",
                 "**k-fold cross-validation** splits data into k parts, trains on k−1 and validates on "
                 "the held-out part, rotating through all k.",
                 i(), extra=["Every observation is used for both training and validation",
                             "Average the k validation scores for a stable estimate",
                             "Common choices: k = 5 or 10"])
    d.figure("How it works", "5-fold cross-validation", F("L10_cv.png"), i(),
             caption="Each fold takes a turn as the validation set (red). Averaging the five scores "
                     "gives a reliable estimate of generalisation.")
    d.bullets("Why cross-validate", "Better than a single split", [
        ("A single train/test split is **noisy** — depends on luck of the draw", 0),
        ("CV **reuses** data efficiently for a stable estimate", 0),
        ("Essential for **tuning** settings (e.g. how much to regularise — Lecture 12)", 0),
        ("Still keep a final **untouched test set** for the last word", 0),
    ], i())
    d.bullets("Variants", "Flavours of CV", [
        ("**k-fold** — the standard (k = 5 or 10)", 0),
        ("**Stratified** — keep class proportions per fold (imbalanced Y)", 0),
        ("**Leave-one-out** — k = n; low bias, high variance, expensive", 0),
        ("**Repeated** — average over several k-fold runs for stability", 0),
    ], i())
    d.checkpoint("Why use cross-validation instead of a single train/test split?",
        ["It's faster", "It gives a more stable, less luck-dependent performance estimate",
         "It avoids standardising", "It removes the need for a test set"], 1, i(),
        explain="Averaging over folds reduces the variance of the estimate compared with one arbitrary "
                "split — though a final held-out test set is still wise.")

    d.section("Part 6", "Assessment, workflow & pitfalls")
    d.table("Metrics", "How we score models",
            ["Task", "Metric", "Meaning"],
            [["Regression", "RMSE / MAE", "typical prediction error"],
             ["Regression", "R²", "variance explained"],
             ["Classification", "accuracy", "fraction correct"],
             ["Classification", "AUC", "ranking quality (Lecture 11)"],
             ["Classification", "precision/recall", "for imbalanced classes"]],
            i(), col_widths=[2.6,2.8,5.9])
    d.definition("Definition", "Model selection vs assessment",
                 "**Selection** chooses among models/settings (use CV); **assessment** estimates the "
                 "final model's real-world error (use a held-out test set).",
                 i(), extra=["Don't use the test set to choose — that leaks and inflates scores",
                             "Train → validate (CV) → test, in that order",
                             "The test set is touched **once**, at the very end"])
    d.code("tidymodels", "The supervised workflow in R", [
        "library(tidymodels)",
        "split <- initial_split(data, prop = 0.8, strata = outcome)",
        "folds <- vfold_cv(training(split), v = 5)",
        "",
        "rec  <- recipe(outcome ~ ., training(split)) |> step_normalize(all_numeric_predictors())",
        "spec <- logistic_reg() |> set_engine('glm')",
        "wf   <- workflow() |> add_recipe(rec) |> add_model(spec)",
        "",
        "fit_resamples(wf, folds) |> collect_metrics()   # CV estimate",
    ], i())
    d.big_point("The workflow in one line", "Split → preprocess on training → cross-validate to select "
                "→ evaluate once on test.",
                i(), sub="This discipline is what separates trustworthy results from wishful ones.")
    d.bullets("Pitfalls", "Classic ways to fool yourself", [
        ("**Leakage** — preprocessing before the split", 0),
        ("**Peeking** — tuning on the test set", 0),
        ("**Ignoring imbalance** — 95% accuracy when 95% are one class", 0),
        ("**No baseline** — always compare to a trivial model", 0),
    ], i())
    d.definition("Definition", "No free lunch theorem",
                 "**No single model is best for all problems** — performance depends on the data, so we "
                 "compare candidates empirically.",
                 i(), extra=["Justifies trying several methods and cross-validating",
                             "Simplicity and interpretability are legitimate tie-breakers",
                             "Domain knowledge narrows the search"])
    d.checkpoint("You tuned a model's settings using the test set and now report its test accuracy. The number is…",
        ["Trustworthy", "Optimistically biased — the test set influenced the model",
         "Too low", "Irrelevant"], 1, i(),
        explain="Using the test set for tuning leaks information; its accuracy no longer reflects "
                "genuine generalisation. Tune with CV, test once.")
    d.exercise("Design an evaluation", [
        "You must predict metabolic-syndrome (yes/no) from 25 intake variables.",
        "Describe the full split → preprocess → CV → test workflow you'd use.",
        "Which metric(s) would you report, and why (the classes are imbalanced)?",
        "Name two forms of leakage you'll actively guard against.",
    ], i(), hint="For imbalanced classes prefer AUC / precision-recall over raw accuracy; guard against "
                 "preprocessing-before-split and tuning-on-test leakage.")
    d.bullets("Key ideas recap", "The framework in brief", [
        ("Supervised learning fits **f: X → Y** to generalise to new data", 0),
        ("Minimise a **loss**; judge by **test**, not training, error", 0),
        ("Balance **bias vs variance**; avoid over/under-fitting", 0),
        ("**Cross-validate** to select; **hold out** to assess", 0),
    ], i())
    d.bullets("Further reading", "To go deeper", [
        ("James et al., *An Introduction to Statistical Learning*, Ch. 2 & 5", 0),
        ("Hastie et al., *The Elements of Statistical Learning*, Ch. 7", 0),
        ("The **tidymodels** documentation and *Tidy Modeling with R*", 0),
    ], i())

    d.section("Part 7", "Evaluating classifiers properly")
    d.definition("Definition", "Confusion matrix",
                 "A **confusion matrix** cross-tabulates predicted vs actual classes: true/false "
                 "positives and negatives.",
                 i(), extra=["TP, TN — correct; FP (false alarm), FN (missed case)",
                             "Every classification metric is built from these four counts",
                             "Always look at it before trusting a single accuracy number"])
    d.table("From the matrix", "The metrics that matter",
            ["Metric", "Formula", "Answers"],
            [["Accuracy", "(TP+TN)/all", "overall correctness"],
             ["Precision", "TP/(TP+FP)", "of predicted positives, how many right?"],
             ["Recall (sens.)", "TP/(TP+FN)", "of actual positives, how many caught?"],
             ["Specificity", "TN/(TN+FP)", "of actual negatives, how many caught?"],
             ["F1", "harmonic mean P&R", "balance of precision & recall"]],
            i(), col_widths=[2.4,3.0,5.9])
    d.big_point("The accuracy paradox", "If 95% of people are healthy, a model that predicts "
                "'healthy' for everyone scores 95% accuracy — and is useless.",
                i(), sub="With imbalanced classes, accuracy lies. Use recall, precision, F1 or AUC.")
    d.bullets("Worked example", "Reading a confusion matrix", [
        ("100 patients: 20 diseased, 80 healthy", 0),
        ("Model catches 15 diseased (TP=15, FN=5) and flags 10 healthy wrongly (FP=10, TN=70)", 0),
        ("**Accuracy** = 85/100 = 85%; **Recall** = 15/20 = 75%; **Precision** = 15/25 = 60%", 0),
        ("Accuracy looks fine, but it **misses 1 in 4** diseased patients", 0),
    ], i())
    d.checkpoint("A rare-disease test has 99% accuracy but recall 10%. In practice it…",
        ["Works well", "Misses 90% of actual cases — dangerous", "Has no false positives",
         "Is perfectly calibrated"], 1, i(),
        explain="High accuracy with low recall means it rarely predicts the disease and misses most "
                "true cases — accuracy is dominated by the healthy majority.")

    d.section("Part 8", "Model families, curves & pitfalls")
    d.definition("Definition", "Parameters vs hyperparameters",
                 "**Parameters** are learned from data (e.g. regression coefficients); "
                 "**hyperparameters** are set before fitting (e.g. penalty strength, k in k-NN).",
                 i(), extra=["Parameters: fit by minimising loss",
                             "Hyperparameters: chosen by cross-validation",
                             "Confusing the two is a common exam slip"])
    d.two_col("Model spectrum", "Parametric vs non-parametric",
              left_head="Parametric",
              left=["Fixed form & #parameters",
                    "e.g. linear/logistic regression",
                    "Efficient, interpretable",
                    "Risk: wrong-shape bias"],
              right_head="Non-parametric",
              right=["Flexibility grows with data",
                     "e.g. k-NN, trees, splines",
                     "Adapts to complex shapes",
                     "Risk: overfitting, needs more data"],
              idx=i())
    d.definition("Definition", "Learning curve",
                 "A **learning curve** plots error against training-set size, revealing whether more "
                 "data would help.",
                 i(), extra=["High bias: train & test errors both high and close → more data won't help",
                             "High variance: big train–test gap → more data may help",
                             "A cheap diagnostic before collecting more data"])
    d.bullets("Baselines", "Always compare against something trivial", [
        ("Classification: predict the **majority class**", 0),
        ("Regression: predict the **mean**", 0),
        ("A model that can't beat the baseline is worthless", 0),
        ("Baselines keep you honest about 'good' performance", 0),
    ], i())
    d.definition("Definition", "Nested cross-validation",
                 "**Nested CV** uses an inner CV loop to tune hyperparameters and an outer loop to "
                 "assess performance — avoiding optimistic bias from tuning.",
                 i(), extra=["Inner loop: select settings",
                             "Outer loop: estimate generalisation of the whole procedure",
                             "The gold standard when you both tune and report"])
    d.bullets("Ethics & fairness", "Responsible supervised learning", [
        ("A model can be **accurate yet unfair** across groups", 0),
        ("Biased training data → biased, harmful predictions", 0),
        ("In health, **false negatives** can be dangerous — weigh error costs", 0),
        ("Interpretability supports **accountability**", 0),
    ], i())
    d.checkpoint("Which is a hyperparameter, not a parameter?",
        ["A logistic-regression coefficient", "The regularisation strength λ",
         "A fitted cluster mean", "A PCA loading"], 1, i(),
        explain="λ is set before fitting and chosen by cross-validation — a hyperparameter. "
                "Coefficients, means and loadings are learned from data.")
    d.big_point("The road ahead", "Every supervised method in Weeks 4–7 — logistic regression, "
                "discriminant analysis, trees, forests, SVMs, neural nets — plugs into this framework.",
                i(), sub="Fit f, control bias vs variance, cross-validate, evaluate honestly.")
    d.exercise("Diagnose from a learning curve", [
        "Model A: training and test error are both 30% and nearly equal.",
        "Model B: training error 3%, test error 25%.",
        "Diagnose each (bias vs variance). Would more data help either?",
        "Suggest one concrete fix for each model.",
    ], i(), hint="A: high bias (both high, close) → more data won't help; use a richer model. "
                 "B: high variance (big gap) → more data / regularisation / simpler model.")
    d.bullets("Key ideas recap", "The evaluation toolkit", [
        ("Read the **confusion matrix**, not just accuracy", 0),
        ("For imbalance use **precision, recall, F1, AUC**", 0),
        ("Tune **hyperparameters** by CV; assess with a **test set**", 0),
        ("Always beat a **baseline**; watch fairness", 0),
    ], i())
    d.bullets("Further reading", "To go deeper", [
        ("James et al., *ISLR*, Ch. 4 (classification) & Ch. 5 (resampling)", 0),
        ("Hastie et al., *ESL*, Ch. 7 (model assessment & selection)", 0),
        ("*Tidy Modeling with R* — practical resampling & metrics", 0),
    ], i())
    d.summary([
        "Supervised learning fits **f: X → Y** and is judged by **generalisation** to new data.",
        "Fitting minimises a **loss**; training error is optimistic, so we rely on **test error**.",
        "The **bias–variance trade-off** explains under- and over-fitting.",
        "**Cross-validate** to select and tune; keep an untouched **test set** to assess.",
    ], i(), nextup="Lecture 11 — Logistic regression: the workhorse classifier.")
    out=os.path.join(HERE,"Lecture10_SupervisedIntro.pptx"); d.save(out); return out


if __name__ == "__main__":
    for f in (lecture09, lecture10):
        p=f(); print(f"{os.path.basename(p)}  —  {len(Presentation(p).slides._sldIdLst)} slides")
