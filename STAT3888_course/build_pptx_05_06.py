# -*- coding: utf-8 -*-
"""STAT3888 lectures 05 (GMM) & 06 (Hierarchical) — full 60+ slide decks."""
import os
from pptx_deck import Deck, HERE
from pptx import Presentation
F = lambda name: os.path.join(HERE, "figures", name)

# ================================================================= LECTURE 05
def lecture05():
    d = Deck(5, "Model-based Clustering")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Model-based Clustering: Gaussian Mixture Models",
            "From hard partitions to soft, probabilistic clusters — the mixture model, the EM "
            "algorithm, and choosing the number of components with the BIC.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("Why k-means is not enough: soft vs hard clustering", 0),
        ("The Gaussian mixture model (GMM)", 0),
        ("Fitting a GMM with the EM algorithm", 0),
        ("Covariance structures and model flexibility", 0),
        ("Choosing the number of components with the BIC", 0),
        ("GMM vs k-means; fitting in R with mclust", 0),
        ("Diagnostics, pitfalls and worked example", 0),
    ], i())
    d.bullets("Recap", "Where we've been", [
        ("**Lecture 3** — clustering finds groups without labels using a distance", 0),
        ("**Lecture 4** — k-means minimises within-cluster sum of squares", 0),
        ("k-means gives every point a **hard** label and assumes **round, equal-size** blobs", 0),
        ("Today we relax both assumptions with a **probability model**", 0),
    ], i())
    d.checkpoint("Recap: what does k-means assume about cluster shape?",
        ["Arbitrary shapes are fine", "Roughly spherical, similar-size clusters",
         "Only elongated clusters", "It makes no assumptions"], 1, i(),
        explain="k-means uses squared Euclidean distance to a centroid, which implicitly assumes "
                "convex, roughly spherical, comparable-variance clusters.")

    d.section("Part 1", "Why we need soft clustering")
    d.big_point("The limitation", "k-means forces every point into exactly one cluster — "
                "even points sitting on the boundary between two groups.",
                i(), sub="Real data is rarely so tidy. A participant's diet may be 60% 'prudent', "
                         "40% 'Western'. Hard labels throw that nuance away.")
    d.figure("The difference", "Hard labels vs soft probabilities", F("L05_soft_vs_hard.png"), i(),
             caption="k-means (left) draws a crisp line. A GMM (right) reports P(cluster) for every "
                     "point — colour fades through the overlap zone.")
    d.bullets("Soft assignment", "What 'soft' buys us", [
        ("Each point gets a **probability of membership** in every cluster", 0),
        ("Points in overlaps are honestly reported as **uncertain**", 0),
        ("Clusters can be **elliptical** and have **different sizes / orientations**", 0),
        ("We get a full **generative model** — we can simulate new data", 0),
    ], i())
    d.two_col("Motivation", "Why this matters for the nutrition project",
              left_head="The science",
              left=["Metabolic subtypes rarely have sharp edges",
                    "A person can partly belong to two dietary patterns",
                    "Uncertainty is information, not a nuisance"],
              right_head="The statistics",
              right=["A model lets us use **likelihood**",
                     "Likelihood gives principled **model selection**",
                     "We can compare 2, 3, 4… clusters fairly"],
              idx=i())

    d.section("Part 2", "The Gaussian mixture model")
    d.definition("Definition", "Mixture model",
                 "A **mixture model** assumes each observation is drawn from one of K underlying "
                 "distributions (the **components**), but we don't observe which one.",
                 i(), extra=["Each component k has a weight **πₖ** (mixing proportion), with Σπₖ = 1",
                             "For a **Gaussian** mixture, each component is a normal distribution",
                             "The observed data is the weighted blend of all components"])
    d.figure("One dimension", "A mixture is a weighted sum of bells", F("L05_1d_mixture.png"), i(),
             caption="Two Gaussian components (dashed) with weights 0.4 and 0.6 add up to the "
                     "mixture density (black) that generated the histogram.")
    d.formula("The model", "Gaussian mixture density",
              "p(x) = Σₖ  πₖ · N( x | μₖ , Σₖ )",
              ["**πₖ** — mixing weight of component k (how common it is)",
               "**μₖ** — mean vector (centre) of component k",
               "**Σₖ** — covariance matrix (shape & orientation) of component k"],
              i(), note="Fitting a GMM means estimating all the πₖ, μₖ and Σₖ from data.")
    d.formula("Building block", "The multivariate Gaussian",
              "N(x | μ, Σ) ∝ exp( −½ (x−μ)ᵀ Σ⁻¹ (x−μ) )",
              ["The term (x−μ)ᵀΣ⁻¹(x−μ) is the **Mahalanobis distance** — a scale-aware distance",
               "Σ controls the **shape**: circular, stretched, or tilted",
               "k-means secretly uses the special case Σ = σ²I (a circle)"],
              i())
    d.figure("Two dimensions", "GMM fits elliptical clusters", F("L05_ellipses.png"), i(),
             caption="Each component is an ellipse defined by its covariance matrix — far more flexible "
                     "than k-means' circles.")
    d.bullets("Covariance", "What the covariance matrix controls", [
        ("**Diagonal entries** — variance along each axis (width & height)", 0),
        ("**Off-diagonal entries** — covariance (tilt / correlation)", 0),
        ("A full Σ can capture a cluster stretched along any direction", 0),
        ("Restricting Σ trades flexibility for fewer parameters", 0),
    ], i())
    d.figure("Flexibility dial", "Covariance types", F("L05_covtypes.png"), i(),
             caption="From spherical (like k-means) to full (any ellipse). More flexible models fit "
                     "better but need more data and can overfit.")
    d.table("Trade-off", "Common covariance structures",
            ["Type", "What's shared", "Parameters"],
            [["Spherical", "one variance, circular", "fewest (≈ k-means)"],
             ["Diagonal", "axis-aligned ellipse", "few"],
             ["Tied", "same Σ for all clusters", "moderate"],
             ["Full", "any ellipse per cluster", "most / most flexible"]],
            i(), note="mclust automatically tries a whole family of these and picks the best by BIC.")
    d.checkpoint("Which covariance type most resembles k-means?",
        ["Full", "Tied", "Spherical", "Diagonal"], 2, i(),
        explain="Spherical, equal-variance components with equal weights reduce a GMM to (essentially) "
                "k-means.")

    d.section("Part 3", "Fitting a GMM: the EM algorithm")
    d.bullets("The obstacle", "A chicken-and-egg problem", [
        ("If we **knew** which component each point came from, estimating πₖ, μₖ, Σₖ would be easy", 0),
        ("If we **knew** the parameters, computing each point's component would be easy", 0),
        ("But we know **neither** — the component labels are **latent** (hidden)", 0),
        ("**EM** breaks the deadlock by alternating between the two", 0),
    ], i())
    d.definition("Definition", "Responsibility",
                 "The **responsibility** γᵢₖ is the posterior probability that point i was generated "
                 "by component k, given the current parameters.",
                 i(), extra=["It is the 'soft label' — a number between 0 and 1",
                             "For each point, responsibilities across components sum to 1",
                             "Computed by Bayes' rule from the weighted component densities"])
    d.formula("E-step", "Compute responsibilities (Bayes' rule)",
              "γᵢₖ = πₖ N(xᵢ|μₖ,Σₖ)  /  Σⱼ πⱼ N(xᵢ|μⱼ,Σⱼ)",
              ["Numerator: how well component k explains point i, weighted by πₖ",
               "Denominator: total across all components (normalises to a probability)",
               "This is the **Expectation** step — filling in soft labels"],
              i())
    d.figure("Soft labels", "Responsibilities shared across clusters", F("L05_responsibility.png"), i(),
             caption="Each observation (column) is split between clusters. Points near a centre are "
                     "almost pure; points between are shared.")
    d.formula("M-step", "Re-estimate parameters (weighted MLE)",
              "μₖ = Σᵢ γᵢₖ xᵢ / Σᵢ γᵢₖ ,   πₖ = (1/n) Σᵢ γᵢₖ",
              ["Each parameter is a **responsibility-weighted** average",
               "Points that 'belong' more to k count more toward its mean/covariance",
               "This is the **Maximisation** step — refitting given the soft labels"],
              i())
    d.steps("The loop", "EM in four steps", [
        ("Initialise", "guess parameters (often from k-means)"),
        ("E-step", "compute responsibilities γᵢₖ for every point"),
        ("M-step", "update πₖ, μₖ, Σₖ using weighted averages"),
        ("Repeat", "until the log-likelihood stops increasing"),
    ], i(), note="Each iteration is guaranteed **not to decrease** the log-likelihood.")
    d.figure("Convergence", "EM refines the components each pass", F("L05_em.png"), i(),
             caption="From a poor start, the component means and widths adjust until they explain the "
                     "data — here recovering the two true groups.")
    d.bullets("Properties", "What to know about EM", [
        ("**Monotone**: log-likelihood increases (or stays) each iteration", 0),
        ("Converges to a **local** optimum — like k-means, use several restarts", 0),
        ("**Initialisation** matters; k-means is a common warm start", 0),
        ("Can be **slow** near convergence, but reliable", 0),
    ], i())
    d.checkpoint("In EM, what does the E-step compute?",
        ["Updated cluster means", "Soft responsibilities for each point",
         "The number of clusters", "The BIC"], 1, i(),
        explain="The E (Expectation) step fixes the parameters and computes each point's posterior "
                "probability of belonging to each component.")

    d.section("Part 4", "How many components?")
    d.bullets("The temptation", "Why we can't just maximise likelihood", [
        ("Adding components **always** increases the training log-likelihood", 0),
        ("Taken to the extreme, one component per point fits perfectly — and is useless", 0),
        ("We need to **penalise complexity** — reward fit, punish extra parameters", 0),
    ], i())
    d.formula("Model selection", "Bayesian Information Criterion",
              "BIC = −2 · log L  +  d · log(n)",
              ["**log L** — maximised log-likelihood (fit)",
               "**d** — number of free parameters (complexity)",
               "**n** — sample size; the penalty grows with data",
               "**Lower BIC is better** — choose the model that minimises it"],
              i())
    d.figure("In practice", "BIC across candidate models", F("L05_bic.png"), i(),
             caption="Fit GMMs for a range of k and pick the k with the lowest BIC. Here BIC bottoms "
                     "out at the true number of clusters.")
    d.bullets("AIC vs BIC", "A note on criteria", [
        ("**AIC** = −2 log L + 2d — lighter penalty, tends to pick **more** components", 0),
        ("**BIC** penalises complexity more as n grows — tends to be **more parsimonious**", 0),
        ("For clustering/interpretation, **BIC** is the usual default (and mclust's)", 0),
    ], i())

    d.section("Part 5", "GMM vs k-means")
    d.table("Head to head", "Two clustering philosophies",
            ["Aspect", "k-means", "GMM"],
            [["Assignment", "hard (one label)", "soft (probabilities)"],
             ["Cluster shape", "spherical", "any ellipse"],
             ["Cluster size", "similar", "can differ"],
             ["Basis", "distance", "probability model"],
             ["Choose k by", "elbow / silhouette", "BIC / likelihood"],
             ["Speed", "very fast", "slower (EM)"]],
            i(), col_widths=[2.8,4.2,4.5])
    d.big_point("Key insight", "k-means is a special case of a Gaussian mixture — "
                "equal weights, spherical equal covariances, and hard assignments.",
                i(), sub="So GMM is the more general model. Use k-means for speed and simplicity; "
                         "reach for GMM when clusters overlap or aren't round.")
    d.two_col("Judgement", "When to use which",
              left_head="Prefer k-means when",
              left=["Data is large and you need speed",
                    "Clusters look roughly round & separated",
                    "You just need a quick partition"],
              right_head="Prefer GMM when",
              right=["Clusters overlap or are elliptical",
                     "You want membership **uncertainty**",
                     "You want principled selection of k (BIC)"],
              idx=i())

    d.section("Part 6", "GMM in R")
    d.bullets("Package", "The mclust package", [
        ("**mclust** fits Gaussian mixtures and does model selection automatically", 0),
        ("It searches over **covariance types** and **number of components**", 0),
        ("Reports the **best model by BIC** with a three-letter code (e.g. VVV, EEI)", 0),
    ], i())
    d.code("Fitting", "A GMM in a few lines", [
        "library(mclust)",
        "",
        "X <- scale(diet_numeric)          # standardise first",
        "fit <- Mclust(X)                  # searches covariance types & k by BIC",
        "",
        "summary(fit)                      # best model, k, BIC",
        "fit$G                             # chosen number of components",
        "fit$classification               # hard labels (argmax responsibility)",
        "head(fit$z)                       # soft responsibilities",
    ], i())
    d.code("Visualising", "Plots that explain the fit", [
        "plot(fit, what = 'BIC')           # BIC vs k for each model type",
        "plot(fit, what = 'classification')# clusters with ellipses",
        "plot(fit, what = 'uncertainty')   # highlight uncertain points",
        "",
        "# Profile the clusters, as with k-means",
        "aggregate(diet_numeric, list(fit$classification), mean)",
    ], i())
    d.table("Decoding", "mclust's covariance codes (E=equal, V=varying)",
            ["Code", "Meaning"],
            [["EII", "spherical, equal volume"],
             ["VII", "spherical, varying volume"],
             ["EEE", "ellipsoidal, all equal (tied)"],
             ["VVV", "ellipsoidal, all varying (most flexible)"]],
            i(), col_widths=[2.2,9.3])
    d.bullets("Worked example", "A nutrition workflow", [
        ("Standardise intake & metabolite variables", 0),
        ("Run **Mclust(X)** — say it selects VEV with k = 3", 0),
        ("Inspect **uncertainty** — flag participants on cluster boundaries", 0),
        ("Profile each cluster's mean intake → name the **dietary subtypes**", 0),
        ("Relate subtypes to a held-out health outcome to check they matter", 0),
    ], i())

    d.section("Part 7", "Diagnostics & pitfalls")
    d.bullets("Pitfall 1", "Singularities and degeneracy", [
        ("A component can collapse onto a single point → variance → 0, likelihood → ∞", 0),
        ("This is a **degenerate** solution, not a real cluster", 0),
        ("Remedies: **regularise** the covariance, or restrict the covariance type", 0),
    ], i())
    d.bullets("Pitfall 2", "High dimensions", [
        ("A full covariance needs ~p²/2 parameters **per component**", 0),
        ("With many variables this explodes — you run out of data", 0),
        ("Remedies: **reduce dimensions first** (PCA — Lectures 7–8) or use diagonal Σ", 0),
    ], i())
    d.bullets("Pitfall 3", "Label switching & interpretation", [
        ("Component labels are **arbitrary** — 'cluster 1' can swap with 'cluster 2' between runs", 0),
        ("Interpret clusters by their **profiles**, not their numbers", 0),
        ("Always **standardise** and set a seed for reproducibility", 0),
    ], i())
    d.checkpoint("Your GMM returns one component with almost-zero variance around a single point. This is…",
        ["The best cluster", "A degenerate/singular solution to guard against",
         "Proof you need more clusters", "Expected and fine"], 1, i(),
        explain="A component shrinking onto one point sends the likelihood to infinity — a degeneracy. "
                "Regularise the covariance or constrain the model.")
    d.exercise("Fit and compare", [
        "Fit **Mclust(X)** on the standardised nutrition data. What model and k does BIC choose?",
        "Compare its k to the k you chose for **k-means** last week. Do they agree?",
        "Identify the 5 participants with the **highest uncertainty**. Where do they sit?",
        "Profile the components — can you name each dietary subtype?",
    ], i(), hint="fit$uncertainty gives 1 − max responsibility for each point; sort it descending.")
    d.exercise("Reason about the model", [
        "Write down how many parameters a **full**-covariance GMM needs for k = 3, p = 10.",
        "Why might that be a problem with only n = 150 participants?",
        "What two remedies would you try, and what does each give up?",
    ], i(), hint="Per component: k−1 weights + p means + p(p+1)/2 covariance terms. Multiply and compare to n.")
    d.bullets("Practical tips", "Getting good results", [
        ("**Standardise** every variable before fitting", 0),
        ("Consider **PCA first** if p is large", 0),
        ("Let mclust choose the covariance type — don't force **full** blindly", 0),
        ("Report **uncertainty**, not just hard labels", 0),
    ], i())
    d.bullets("Key formulas recap", "The three you must know", [
        ("**Model**: p(x) = Σ πₖ N(x | μₖ, Σₖ)", 0),
        ("**E-step**: γᵢₖ ∝ πₖ N(xᵢ | μₖ, Σₖ)", 0),
        ("**Selection**: BIC = −2 log L + d log n (minimise)", 0),
    ], i())

    d.section("Part 8", "Deeper understanding & applications")
    d.definition("Definition", "Likelihood",
                 "The **likelihood** is the probability of the observed data under the model, viewed "
                 "as a function of the parameters. We fit by **maximising** it.",
                 i(), extra=["For a GMM: log L = Σᵢ log( Σₖ πₖ N(xᵢ|μₖ,Σₖ) )",
                             "EM increases this quantity every iteration",
                             "It is the 'fit' term that BIC then penalises for complexity"])
    d.bullets("Generative view", "A GMM can create data, not just cluster it", [
        ("To simulate a point: **pick a component** k with probability πₖ, then **draw** from N(μₖ,Σₖ)", 0),
        ("This 'generative' nature is what makes likelihood and BIC available", 0),
        ("It also powers **density estimation** — a smooth model of where data lives", 0),
        ("Contrast: k-means is purely **algorithmic**, with no generative story", 0),
    ], i())
    d.bullets("Application", "GMMs beyond clustering", [
        ("**Density estimation** — flexible model of a variable's distribution", 0),
        ("**Anomaly detection** — points with very low p(x) are outliers", 0),
        ("**Soft segmentation** — image, market or patient segmentation with uncertainty", 0),
        ("**Semi-supervised learning** — components can align with partial labels", 0),
    ], i())
    d.bullets("Initialisation", "Strategies that help EM", [
        ("**k-means warm start** — run k-means, use its clusters to seed EM (mclust's default idea)", 0),
        ("**Multiple random restarts** — keep the fit with the highest log-likelihood", 0),
        ("**Hierarchical seeding** — mclust initialises from model-based hierarchical clustering", 0),
        ("A good start avoids poor local optima and speeds convergence", 0),
    ], i())
    d.big_point("Remember", "EM never decreases the log-likelihood — but 'never decreasing' only "
                "guarantees a local optimum, not the global best.",
                i(), sub="That's why initialisation and restarts matter, exactly as with k-means.")
    d.checkpoint("You compare GMMs with k = 2, 3, 4 and get BIC = 980, 940, 965. Which do you pick?",
        ["k = 2", "k = 3", "k = 4", "The one with highest BIC"], 1, i(),
        explain="BIC is minimised at k = 3 (940). Lower BIC balances fit against complexity, so k = 3 "
                "is preferred.")
    d.two_col("Context", "Where GMMs sit in the bigger picture",
              left_head="Related ideas",
              left=["Latent-variable models (the hidden component)",
                    "The EM algorithm generalises far beyond GMMs",
                    "Mixtures of other distributions are possible too"],
              right_head="What's next",
              right=["Overlapping, high-dimensional data → reduce first",
                     "PCA (Lectures 7–8) tames dimensionality",
                     "Then cluster in the reduced space"],
              idx=i())
    d.summary([
        "A **GMM** models data as a weighted mixture of Gaussians, giving **soft** cluster probabilities.",
        "**EM** fits it by alternating responsibilities (E) and weighted re-estimation (M).",
        "The **covariance type** dials flexibility from spherical (k-means-like) to full ellipses.",
        "Choose the number of components with the **BIC**; k-means is the GMM's simplest special case.",
    ], i(), nextup="Lecture 06 — Hierarchical clustering: building a tree of nested groups.")

    out = os.path.join(HERE, "Lecture05_GMM.pptx"); d.save(out); return out


# ================================================================= LECTURE 06
def lecture06():
    d = Deck(6, "Hierarchical Clustering")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Hierarchical Clustering",
            "Building a whole tree of nested clusterings — no need to fix k in advance. Linkages, "
            "dendrograms, and how to read them.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("Why a hierarchy? The limits of fixing k", 0),
        ("Agglomerative vs divisive strategies", 0),
        ("The dendrogram: reading nested clusters", 0),
        ("Linkage criteria: single, complete, average, Ward", 0),
        ("Distance matrices and cutting the tree", 0),
        ("Strengths, pitfalls and R practice", 0),
    ], i())
    d.bullets("Recap", "Two clustering methods so far", [
        ("**k-means** — fast, hard, spherical, needs k up front", 0),
        ("**GMM** — soft, elliptical, chooses k by BIC, needs k range", 0),
        ("Both require you to **commit to a number of clusters**", 0),
        ("What if you want to see structure at **every** scale?", 0),
    ], i())
    d.checkpoint("What do k-means and GMM have in common?",
        ["Both give soft labels", "Both require choosing the number of clusters",
         "Both build a tree", "Both ignore distance"], 1, i(),
        explain="Both are partitioning-style: you must specify (or search) k. Hierarchical clustering "
                "instead produces clusterings for all k at once.")

    d.section("Part 1", "Why a hierarchy?")
    d.big_point("The idea", "Instead of one clustering, build a tree that contains a clustering "
                "for every possible number of groups — from one big cluster to n singletons.",
                i(), sub="You choose k afterwards by cutting the tree at a height that makes sense.")
    d.figure("The output", "A dendrogram", F("L06_dendro_big.png"), i(),
             caption="The tree records the order and distance of every merge. Cut it horizontally to "
                     "read off a clustering — lower cut = more clusters.")
    d.two_col("Two directions", "Agglomerative vs divisive",
              left_head="Agglomerative (bottom-up)",
              left=["Start: every point its own cluster",
                    "Repeatedly **merge** the two closest",
                    "End: one cluster containing all",
                    "The common, default approach"],
              right_head="Divisive (top-down)",
              right=["Start: all points in one cluster",
                     "Repeatedly **split** a cluster",
                     "End: every point alone",
                     "Rarer, more expensive"],
              idx=i())
    d.definition("Definition", "Dendrogram",
                 "A **dendrogram** is a tree diagram showing the sequence of merges and the "
                 "**distance (height)** at which each occurred.",
                 i(), extra=["Leaves = individual observations",
                             "Height of a join = dissimilarity of the merged groups",
                             "Points that merge low down are very similar"])

    d.section("Part 2", "The agglomerative algorithm")
    d.figure("Merging", "Building the tree from the bottom up", F("L06_agglo_steps.png"), i(),
             caption="Each step fuses the two nearest clusters, reducing the count by one, until a "
                     "single cluster remains.")
    d.steps("Algorithm", "Agglomerative clustering", [
        ("Start", "each of the n points is its own cluster"),
        ("Find", "the two clusters with the smallest linkage distance"),
        ("Merge", "combine them; record the merge height"),
        ("Repeat", "until only one cluster remains — you now have the full tree"),
    ], i(), note="The result is independent of k — you cut the finished tree wherever you like.")
    d.bullets("The key question", "How far apart are two clusters?", [
        ("For single points, distance is clear (e.g. Euclidean)", 0),
        ("But how far apart are two **groups** of points?", 0),
        ("The answer is the **linkage criterion** — and it changes everything", 0),
    ], i())

    d.section("Part 3", "Linkage criteria")
    d.figure("Definitions", "Three ways to measure inter-cluster distance", F("L06_linkage_defs.png"), i(),
             caption="Single = closest pair; complete = farthest pair; average = mean over all "
                     "cross-cluster pairs.")
    d.table("The four", "Linkage criteria compared",
            ["Linkage", "Distance between clusters", "Tendency"],
            [["Single", "closest pair (min)", "long, chained clusters"],
             ["Complete", "farthest pair (max)", "compact, equal-diameter"],
             ["Average", "mean of all pairs", "a compromise"],
             ["Ward", "increase in within-SS when merged", "compact, similar-size (popular)"]],
            i(), col_widths=[2.2,5.3,4.0])
    d.figure("Same data, different trees", "Linkage reshapes the dendrogram", F("L06_linkages.png"), i(),
             caption="The identical 30 points give four different hierarchies. Linkage is a genuine "
                     "modelling choice, not a technicality.")
    d.bullets("Single linkage", "Strengths and its Achilles heel", [
        ("Can capture **elongated, non-convex** shapes", 0),
        ("Suffers from **chaining**: a bridge of points merges two real clusters", 0),
        ("Sensitive to noise and outliers", 0),
    ], i())
    d.figure("Chaining vs compact", "Single linkage follows shape; Ward prefers blobs",
             F("L06_chaining.png"), i(),
             caption="On the moons, single linkage traces each arc; Ward carves compact regions and "
                     "gets them 'wrong' — the right choice depends on your goal.")
    d.bullets("Ward's method", "The common default", [
        ("Merges the pair that **least increases** total within-cluster variance", 0),
        ("Tends to produce **compact, similar-size** clusters", 0),
        ("Closely related to the k-means objective", 0),
        ("Use with **Euclidean** distance (ward.D2 in R)", 0),
    ], i())
    d.checkpoint("Which linkage is most prone to 'chaining'?",
        ["Complete", "Ward", "Single", "Average"], 2, i(),
        explain="Single linkage joins clusters via their closest pair, so a thin bridge of points can "
                "chain two otherwise-separate clusters together.")

    d.section("Part 4", "Distances & cutting the tree")
    d.figure("Starting point", "It all begins with a distance matrix", F("L06_distmat.png"), i(),
             caption="Hierarchical clustering works from the n×n matrix of pairwise distances. Block "
                     "structure already hints at the clusters.")
    d.bullets("Distance choice", "Two decisions, not one", [
        ("**Distance** between points: Euclidean, Manhattan, correlation… (Lecture 3)", 0),
        ("**Linkage** between clusters: single, complete, average, Ward", 0),
        ("Together they define the whole clustering — choose both deliberately", 0),
        ("**Standardise** first, as always for distance-based methods", 0),
    ], i())
    d.bullets("Cutting", "From tree to clusters", [
        ("Cut the dendrogram **horizontally** at a chosen height", 0),
        ("Each branch crossing the cut becomes one cluster", 0),
        ("**Lower** cut → more, smaller clusters; **higher** cut → fewer, larger", 0),
        ("Choose the height at a **big vertical gap** — a natural break", 0),
    ], i())
    d.formula("Reading heights", "Merge height = dissimilarity",
              "big vertical gap  ⇒  natural number of clusters",
              ["A long branch means the two groups below it are quite different",
               "Cutting just below a long branch separates well-distinguished clusters",
               "The **cophenetic distance** is the merge height for a pair of points"],
              i())
    d.bullets("Validation", "How many clusters, revisited", [
        ("Look for the **largest gap** between successive merge heights", 0),
        ("Cross-check with the **silhouette** (Lecture 4) at each candidate k", 0),
        ("The **cophenetic correlation** measures how faithfully the tree preserves distances", 0),
        ("Ultimately: does the clustering make **domain sense**?", 0),
    ], i())

    d.section("Part 5", "Hierarchical clustering in R")
    d.code("Fitting", "From data to dendrogram", [
        "X <- scale(diet_numeric)          # standardise",
        "d <- dist(X, method = 'euclidean')# distance matrix",
        "",
        "hc <- hclust(d, method = 'ward.D2')",
        "plot(hc, hang = -1)               # draw the dendrogram",
        "",
        "clusters <- cutree(hc, k = 3)     # cut into 3 clusters",
        "table(clusters)",
    ], i())
    d.code("Comparing", "Try several linkages and validate", [
        "library(factoextra); library(cluster)",
        "",
        "for (m in c('single','complete','average','ward.D2'))",
        "  print(cor(cophenetic(hclust(d, m)), d))   # cophenetic corr.",
        "",
        "fviz_dend(hc, k = 3, rect = TRUE)  # coloured dendrogram",
        "fviz_nbclust(X, hcut, method = 'silhouette')",
    ], i())
    d.two_col("Pros & cons", "Hierarchical clustering in balance",
              left_head="Strengths",
              left=["**No need to fix k** in advance",
                    "The dendrogram is **interpretable**",
                    "Reveals structure at **all scales**",
                    "Works from any distance matrix"],
              right_head="Weaknesses",
              right=["**O(n²)** memory — hard for very large n",
                     "Merges are **greedy & irreversible**",
                     "Sensitive to distance & linkage choice",
                     "Single linkage prone to chaining"],
              idx=i())
    d.bullets("Worked example", "Dietary patterns via a tree", [
        ("Standardise intake variables and compute Euclidean distances", 0),
        ("Run **Ward** linkage; inspect the dendrogram for a clear gap", 0),
        ("Cut into k clusters; check the **silhouette** agrees", 0),
        ("Profile and **name** each cluster with your Nutrition partners", 0),
        ("Compare the partition with last week's k-means / GMM result", 0),
    ], i())

    d.section("Part 6", "Pitfalls & practice")
    d.bullets("Common mistakes", "What trips students up", [
        ("Forgetting to **standardise** before computing distances", 0),
        ("Reading the dendrogram **horizontal** order as meaningful — it isn't", 0),
        ("Using **Ward** with a non-Euclidean distance", 0),
        ("Picking k without checking a validation measure", 0),
    ], i())
    d.checkpoint("On a dendrogram, what does the height of a merge represent?",
        ["The number of points", "The dissimilarity between the merged clusters",
         "The cluster's variance", "Nothing — it's decorative"], 1, i(),
        explain="Merge height = the linkage distance at which two clusters joined. Big heights mean "
                "very different groups.")
    d.exercise("Build and read a tree", [
        "Compute a Euclidean distance matrix on the standardised data and run **complete** and "
        "**Ward** linkage.",
        "Plot both dendrograms. Where is the largest vertical gap in each?",
        "Cut each at k = 3 and cross-tabulate the two labelings. Do they agree?",
        "Compute the **cophenetic correlation** for each linkage — which preserves distances better?",
    ], i(), hint="cutree(hc, k=3) gives labels; table(a, b) cross-tabulates; cor(cophenetic(hc), d) "
                 "gives the cophenetic correlation.")
    d.exercise("Choose a linkage", [
        "Your clusters are expected to be **compact and similar-sized**. Which linkage fits that prior?",
        "Your clusters may be **elongated** (e.g. a metabolic gradient). Which linkage might capture that, "
        "and what risk does it carry?",
        "Justify a final choice for the project and note how you'd validate it.",
    ], i(), hint="Ward → compact/equal size; single → shapes but risks chaining.")
    d.bullets("Key ideas recap", "Hold onto these", [
        ("A **dendrogram** encodes clusterings at every k", 0),
        ("**Linkage** defines inter-cluster distance and shapes the tree", 0),
        ("**Ward** is a solid default; **single** captures shape but chains", 0),
        ("**Cut** at a large gap; validate with silhouette / cophenetic correlation", 0),
    ], i())

    d.section("Part 7", "Divisive methods & complexity")
    d.two_col("The other direction", "Divisive (top-down) clustering",
              left_head="How it works",
              left=["Begin with **all points in one cluster**",
                    "Repeatedly **split** the least-cohesive cluster",
                    "DIANA is the classic algorithm"],
              right_head="Why it's rarer",
              right=["Choosing the best split is **expensive**",
                     "Naively exponential in cluster size",
                     "Agglomerative is usually preferred"],
              idx=i())
    d.bullets("Scalability", "The cost of a full tree", [
        ("Needs the **n×n distance matrix** → **O(n²)** memory", 0),
        ("Runtime is typically **O(n² log n)** or **O(n³)** depending on implementation", 0),
        ("Fine for hundreds–thousands of points; hard for millions", 0),
        ("For big data: cluster a **sample**, or use k-means/mini-batch instead", 0),
    ], i())
    d.definition("Definition", "Cophenetic distance",
                 "The **cophenetic distance** between two observations is the merge height at which "
                 "they first fall into the same cluster.",
                 i(), extra=["Comparing it to the original distances measures tree faithfulness",
                             "The **cophenetic correlation** is that comparison as a single number",
                             "Higher (→1) means the dendrogram preserves the real distances well"])
    d.checkpoint("Why is hierarchical clustering hard to run on 5 million points?",
        ["The tree is uninterpretable", "It needs an O(n²) distance matrix",
         "It can't use Euclidean distance", "It requires labels"], 1, i(),
        explain="Storing all pairwise distances is O(n²) memory — 5M points would need ~10¹³ entries, "
                "which is infeasible.")

    d.section("Part 8", "Heatmaps, bioinformatics & method choice")
    d.bullets("Clustered heatmaps", "A favourite in genomics & metabolomics", [
        ("Combine a **dendrogram** on rows (samples) and columns (variables)", 0),
        ("Reorder both by their trees so **blocks of colour** reveal patterns", 0),
        ("Ubiquitous for gene-expression and **metabolite** data — relevant to your project", 0),
        ("In R: `pheatmap()` or `heatmap()` do the clustering and drawing together", 0),
    ], i())
    d.code("Heatmap", "A clustered heatmap in one call", [
        "library(pheatmap)",
        "pheatmap(scale(metabolites),          # standardise",
        "         clustering_distance_rows = 'euclidean',",
        "         clustering_method = 'ward.D2',",
        "         cutree_rows = 3)              # annotate 3 clusters",
    ], i())
    d.table("All three so far", "Choosing a clustering method",
            ["Method", "Fix k?", "Shape", "Best when"],
            [["k-means", "yes", "spherical", "large, round, quick"],
             ["GMM", "yes (BIC)", "elliptical", "overlap, want uncertainty"],
             ["Hierarchical", "no (cut later)", "any (via linkage)", "want structure at all scales"]],
            i(), col_widths=[2.5,2.0,2.3,4.7])
    d.big_point("No universal winner", "The 'best' clustering method depends on your data's shape, "
                "your sample size, and what question you're asking.",
                i(), sub="A mature analyst runs several, compares them, and validates against domain "
                         "knowledge — never trusts one blindly.")
    d.bullets("Reproducibility", "Make your clustering trustworthy", [
        ("Record the **distance** and **linkage** you used", 0),
        ("**Standardise** and set a seed where randomness enters", 0),
        ("Report **how you chose k** (gap in heights, silhouette)", 0),
        ("Show the **dendrogram** so readers can judge for themselves", 0),
    ], i())
    d.checkpoint("You want structure at multiple scales without committing to one k. Best choice?",
        ["k-means", "GMM", "Hierarchical clustering", "None can do this"], 2, i(),
        explain="Only hierarchical clustering produces a full tree, letting you inspect and choose "
                "clusterings at every granularity after the fact.")
    d.bullets("Interpreting clusters", "The deliverable, again", [
        ("Cut the tree, then **profile** each cluster's variable means", 0),
        ("Give each a **name** meaningful to nutrition (e.g. 'high-protein pattern')", 0),
        ("Check cluster **sizes** — a tiny branch may be outliers", 0),
        ("Relate clusters to a **held-out** outcome to argue they're real", 0),
    ], i())
    d.exercise("Compare all three methods", [
        "On the standardised nutrition data, produce clusterings from **k-means (k=3)**, **Mclust**, and "
        "**Ward hierarchical (cut at 3)**.",
        "Cross-tabulate the three labelings pairwise. Where do they agree and disagree?",
        "For the points where methods **disagree**, describe where they sit geometrically.",
        "Which method would you report to your Nutrition partners, and why?",
    ], i(), hint="Use table() for pairwise agreement; disagreements often sit in overlap/boundary regions.")
    d.bullets("Further reading", "To go deeper", [
        ("James, Witten, Hastie & Tibshirani — *An Introduction to Statistical Learning*, Ch. 12", 0),
        ("Hastie, Tibshirani & Friedman — *The Elements of Statistical Learning*, §14.3", 0),
        ("R: the **cluster**, **factoextra** and **pheatmap** package vignettes", 0),
    ], i())

    d.section("Part 9", "A worked calculation")
    d.bullets("Setup", "Merge distances by hand", [
        ("Four 1-D points: A = 1, B = 2, C = 6, D = 8", 0),
        ("Euclidean distances: |A−B| = 1, |C−D| = 2, |B−C| = 4", 0),
        ("We'll agglomerate step by step under **single** linkage", 0),
    ], i())
    d.steps("Trace", "Single-linkage merges", [
        ("Merge A & B", "closest pair, distance 1 → cluster {A,B}"),
        ("Merge C & D", "next closest, distance 2 → cluster {C,D}"),
        ("Merge {A,B} & {C,D}", "single linkage = min pair distance = |B−C| = 4"),
        ("Done", "one cluster; heights recorded are 1, 2, 4"),
    ], i(), note="Under complete linkage the last merge height would be |A−D| = 7, not 4.")
    d.checkpoint("For the last merge above, what height does COMPLETE linkage use?",
        ["4 (|B−C|)", "7 (|A−D|)", "2 (|C−D|)", "1 (|A−B|)"], 1, i(),
        explain="Complete linkage uses the farthest pair between clusters: |A−D| = |1−8| = 7.")
    d.bullets("Lesson", "Same data, different heights", [
        ("**Single** linkage last-merge height = 4 (nearest pair)", 0),
        ("**Complete** linkage last-merge height = 7 (farthest pair)", 0),
        ("The tree's **shape and cut points** change with linkage", 0),
        ("This is why linkage is a genuine modelling decision", 0),
    ], i())
    d.big_point("The takeaway", "Hierarchical clustering doesn't give you one answer — it gives you a "
                "whole family, and you choose from it with judgement.",
                i(), sub="Distance + linkage + cut height are three levers. Own all three.")
    d.summary([
        "Hierarchical clustering builds a **tree** — a clustering for every k, no k fixed up front.",
        "**Agglomerative** merging is driven by a **linkage** criterion (single/complete/average/Ward).",
        "Read clusters by **cutting** the dendrogram at a natural gap in merge heights.",
        "It's interpretable and shape-aware, but **O(n²)** and sensitive to distance & linkage choices.",
    ], i(), nextup="Lecture 07 — PCA background: the linear algebra behind dimension reduction.")

    out = os.path.join(HERE, "Lecture06_Hierarchical.pptx"); d.save(out); return out


if __name__ == "__main__":
    for f in (lecture05, lecture06):
        p=f(); print(f"{os.path.basename(p)}  —  {len(Presentation(p).slides._sldIdLst)} slides")
