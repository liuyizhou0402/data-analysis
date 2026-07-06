# -*- coding: utf-8 -*-
"""Build full 60-minute STAT3888 PowerPoint lectures 01-04."""
import os
from pptx_deck import Deck, HERE

F = lambda name: os.path.join(HERE, "figures", name)

# ================================================================= LECTURE 01
def lecture01():
    d = Deck(1, "Introduction to Statistical Machine Learning")
    n = [0]
    def i(): n[0]+=1; return f"{n[0]}"

    d.title("Introduction to Statistical Machine Learning",
            "What machine learning is, the two big families of methods, the analysis workflow, "
            "and the interdisciplinary nutrition project you will tackle this semester.")
    i()
    d.section("Part 1", "Welcome & orientation")
    d.bullets("Agenda", "What we will cover today", [
        ("What statistical machine learning is — and is not", 0),
        ("Supervised vs unsupervised learning", 0),
        ("Regression vs classification; the model 'zoo'", 0),
        ("The end-to-end data-analysis workflow", 0),
        ("Overfitting and why we hold out test data", 0),
        ("Tools: R, the tidyverse and tidymodels", 0),
        ("The NUTM3888 joint project, teams and assessment", 0),
        ("How to succeed in this unit", 0),
    ], i())
    d.bullets("Orientation", "The shape of the unit", [
        ("**13 weeks**: Weeks 1–3 unsupervised learning, Weeks 4–7 supervised learning, "
         "Weeks 8–13 project work", 0),
        ("Three **1-hour lectures** + a **tutorial/computer lab** + a **2-hour workshop** each week", 0),
        ("Assessment is dominated by a **team project** on a real nutrition data set (65%) plus a "
         "final exam (35%)", 0),
        ("Coordinator: **John Ormerod** — questions on the Ed forum or in consultation", 0),
        ("Prerequisite thinking: probability, linear algebra, regression, and R", 1),
    ], i())

    d.section("Part 2", "What is statistical machine learning?")
    d.bullets("Definitions", "Machine learning in one sentence", [
        ("**Machine learning** builds algorithms that **learn patterns from data** to predict or "
         "discover structure — without being explicitly programmed for the task", 0),
        ("**Statistical** ML keeps the statistician's questions in view: uncertainty, assumptions, "
         "and whether the pattern is **real** or noise", 0),
        ("Contrast with classical statistics:", 0),
        ("Classical statistics asks *'is this effect real?'* → **inference**", 1),
        ("Machine learning asks *'how well can I predict the next case?'* → **prediction**", 1),
        ("This unit lives deliberately at their **intersection**", 0),
    ], i())
    d.figure("The field", "Data science = statistics + computing + domain", F("L01_venn.png"),
             i(), bullet_head="Why it matters",
             bullets=["ML sits where **statistics** meets **computer science**",
                      "**Data science** adds the third circle: **domain knowledge**",
                      "Your project literally builds this Venn diagram: you supply the stats/CS, "
                      "Nutrition students supply the domain",
                      "The hardest problems live in the **overlaps**"])
    d.two_col("Two cultures", "Statistics vs machine learning: a false dichotomy",
              left_head="Data-modelling culture",
              left=["Assume a **stochastic model** generated the data",
                    "Estimate parameters, test hypotheses",
                    "Prize **interpretability** and inference",
                    "e.g. linear & logistic regression"],
              right_head="Algorithmic culture",
              right=["Treat the mechanism as **unknown**",
                     "Optimise **predictive accuracy** directly",
                     "Prize **flexibility** and performance",
                     "e.g. random forests, neural nets"],
              idx=i())
    d.bullets("Breiman (2001)", "The 'two cultures' — and why you need both", [
        ("Leo Breiman warned that statisticians ignoring algorithmic models were missing powerful "
         "tools", 0),
        ("But pure prediction with **no** model understanding is dangerous in health and nutrition", 0),
        ("**Good data scientists move fluidly between both** — predict well, *and* explain why", 0),
        ("In this unit you learn interpretable methods (regression, LDA, trees) **and** flexible ones "
         "(forests, SVMs, neural nets)", 0),
    ], i())

    d.section("Part 3", "The two families of learning")
    d.figure("Supervised vs unsupervised", "The single most important distinction",
             F("L01_super_vs_unsuper.png"), i(),
             caption="Left: unsupervised — only the points, find the groups. "
                     "Right: supervised — every point carries a known label, learn the rule.",
             bullet_head="How to tell them apart",
             bullets=["Ask: **is there a target variable Y?**",
                      "**Yes** → supervised learning",
                      "**No** → unsupervised learning",
                      "If Y is a **number** → regression",
                      "If Y is a **category** → classification"])
    d.figure("Supervised sub-types", "Regression vs classification", F("L01_reg_vs_class.png"), i(),
             caption="Regression predicts a continuous outcome; classification predicts a discrete label. "
                     "Same framework, different loss.")
    d.table("Examples", "The same tools, many nutrition questions",
            ["Question", "Y variable", "Task"],
            [["Predict fasting glucose from diet", "glucose (mg/dL)", "**Regression**"],
             ["Is this participant at metabolic risk?", "risk / no-risk", "**Classification**"],
             ["Group people into dietary patterns", "none", "**Clustering**"],
             ["Summarise 200 nutrients into a few indices", "none", "**Dimension reduction**"],
             ["Flag implausible food-diary entries", "valid / error", "**Classification**"]],
            i(), col_widths=[5.4,3.1,3.0])
    d.bullets("Unsupervised", "What can you do without labels?", [
        ("**Clustering** — partition observations into groups (Weeks 1–2)", 0),
        ("**Dimension reduction** — compress many correlated variables (PCA, Week 3)", 0),
        ("**Graphical models** — map which variables are conditionally related (Week 12)", 0),
        ("These are **exploratory**: they generate hypotheses you then test", 0),
        ("Crucial when labelling is expensive — which is almost always in health data", 1),
    ], i())

    d.section("Part 4", "The machine-learning workflow")
    d.figure("The loop", "Every project follows this cycle", F("L01_pipeline.png"), i(),
             caption="Real projects iterate — insights at 'evaluate' send you back to 'clean' or 're-model'.")
    d.bullets("Steps", "The workflow, stage by stage", [
        ("**Define the question** with your domain partner — narrow and answerable", 0),
        ("**Clean & explore** — the unglamorous 80% (Lecture 2)", 0),
        ("**Model** — pick methods suited to the question and data", 0),
        ("**Evaluate & select** — honest performance on unseen data", 0),
        ("**Communicate** — a decision-maker must understand and trust the result", 0),
        ("Iterate: the loop rarely runs cleanly once", 0),
    ], i())
    d.bullets("Generalisation", "The one idea that separates ML from curve-fitting", [
        ("We do **not** care how well a model fits the data it was trained on", 0),
        ("We care how well it predicts **new, unseen** cases — **generalisation**", 0),
        ("So we split data: **train** the model on one part, **test** it on another", 0),
        ("A model that memorises training data but fails on test data is **overfitting**", 0),
        ("Cross-validation (Lecture 10) makes this estimate reliable", 1),
    ], i())
    d.figure("The central tension", "Underfitting vs overfitting", F("L01_overfit.png"), i(),
             caption="Too simple (grey) misses the signal; too complex (red) chases the noise. "
                     "The goal is the sweet spot (teal) — the bias–variance trade-off.")
    d.table("The model zoo", "No single method wins everywhere ('no free lunch')",
            ["Unsupervised (Wks 1–3)", "Supervised (Wks 4–7)"],
            [["k-means, GMM, hierarchical clustering", "Logistic & penalised regression"],
             ["Principal component analysis", "Discriminant analysis, k-NN"],
             ["Dimension reduction (MDS, t-SNE)", "Trees, random forests, boosting"],
             ["Graphical / log-linear models", "Neural networks, support vector machines"]],
            i(), note="For every method ask the same three questions: **what does it assume, "
                      "how is it fit, and how do we know it worked?**")

    d.section("Part 5", "Tools & the project")
    d.code("Tools", "You will work in R", [
        "# Core stack for this unit",
        'library(tidyverse)    # data wrangling & ggplot2',
        'library(tidymodels)   # modelling workflows, resampling',
        'library(cluster)      # silhouette, PAM',
        'library(factoextra)   # visualising clusters & PCA',
        "",
        "# A first taste: read, peek, plot",
        'diet <- read_csv("nutrition.csv")',
        'glimpse(diet)',
        'ggplot(diet, aes(fibre, glucose)) + geom_point()',
    ], i(), caption="R + the tidyverse is the lingua franca of applied statistics at USYD.")
    d.two_col("The project", "The joint project with NUTM3888",
              left_head="What it is",
              left=["Teams of **Statistics/Data Science + Nutrition** students",
                    "A real **nutrition & metabolomics** data set",
                    "Answer a genuine question using statistical ML",
                    "Runs Weeks 3–13"],
              right_head="Why it matters",
              right=["**Interdisciplinary** practice (graduate quality GQ7)",
                     "You bring the **methods**; they bring the **question**",
                     "Neither discipline succeeds alone",
                     "Mirrors real data-science teams"],
              idx=i())
    d.bullets("The data", "What the nutrition data looks like", [
        ("Participants (rows) measured on **dietary intake, anthropometrics and metabolites** "
         "(columns)", 0),
        ("**Wide and correlated** — many nutrients move together → dimension reduction shines", 0),
        ("**Messy** — missing values, implausible entries, mixed units → cleaning matters", 0),
        ("Both **unsupervised** (find dietary patterns) and **supervised** (predict a health "
         "outcome) questions are natural", 0),
    ], i())
    d.table("Assessment", "How you are graded",
            ["Component", "Weight", "Due"],
            [["Final written exam", "**35%**", "Exam period"],
             ["Disciplinary assignment (individual)", "**15%**", "Week 11"],
             ["Major project — presentation", "**15%**", "Week 12"],
             ["Major project — manuscript", "**25%**", "Week 13"],
             ["Contribution / reflection / peer review", "**10%**", "Week 13"]],
            i(), note="Project **pitch** (Wk 6) and optional **quiz** (Wk 9) are worth 0% but are "
                      "essential rehearsals — take them seriously.", col_widths=[7.0,2.2,2.3])
    d.bullets("Learning outcomes", "What you should be able to do by Week 13", [
        ("Apply statistics & data science to an **interdisciplinary** (nutrition) problem", 0),
        ("**Formulate, apply, interpret and compare** statistical ML methods", 0),
        ("Judge **model appropriateness** and evaluation procedures", 0),
        ("**Collaborate** across cultural and disciplinary boundaries", 0),
        ("**Communicate** findings to a broad audience", 0),
    ], i())

    d.exercise("Warm-up: name that task", [
        "Predict a person's fasting glucose from 30 dietary-intake variables.",
        "Group 500 participants into dietary **patterns** with no pre-defined labels.",
        "Flag whether a food-diary entry is plausible or a data-entry error.",
        "Compress 200 correlated nutrient measurements into a handful of indices.",
        "For each: supervised or unsupervised? If supervised, regression or classification?",
    ], i(), hint="First ask whether there is a target Y; then ask if Y is numeric or categorical.")
    d.bullets("How to succeed", "Advice from previous cohorts", [
        ("**Start the project early** — cleaning always takes longer than you think", 0),
        ("**Communicate weekly** with your Nutrition teammates", 0),
        ("**Version-control** your code and write it to be re-run, not re-typed", 0),
        ("**Ask on Ed** — if you're stuck, others are too", 0),
        ("**Understand** methods, don't just call functions — the exam tests this", 0),
    ], i())
    d.summary([
        "ML **learns patterns from data**; statistical ML keeps uncertainty and assumptions in view.",
        "**Supervised** = labelled Y (regression/classification); **unsupervised** = structure discovery.",
        "We optimise **generalisation** to unseen data, not fit — beware **overfitting**.",
        "The **workflow** is an iterative loop, and your project is fundamentally **interdisciplinary**.",
    ], i(), nextup="Lecture 02 — Data cleaning: the unglamorous 80% of every project.")

    out = os.path.join(HERE, "Lecture01_Introduction.pptx"); d.save(out); return out


# ================================================================= LECTURE 02
def lecture02():
    d = Deck(2, "Data Cleaning & Preprocessing")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Data Cleaning & Preprocessing",
            "Garbage in, garbage out. How to turn a messy nutrition survey into a trustworthy, "
            "analysis-ready data matrix — reproducibly.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("Why cleaning dominates real projects", 0),
        ("Tidy data and variable types", 0),
        ("Missing data: mechanisms and remedies", 0),
        ("Outliers and robust sanity checks", 0),
        ("Transformations: scaling, logs, encoding", 0),
        ("A reproducible cleaning pipeline in R", 0),
        ("Data leakage — the silent killer", 0),
    ], i())

    d.section("Part 1", "Why cleaning matters")
    d.bullets("Reality", "Real data is never tidy", [
        ("Surveys and lab instruments produce **typos, impossible values, mixed units**", 0),
        ("**Duplicate rows**, free text where numbers belong, and gaps everywhere", 0),
        ("Data scientists routinely spend **~80% of their time** cleaning and preparing data", 0),
        ("It is unglamorous — but a brilliant model on dirty data is **worthless**", 0),
    ], i())
    d.two_col("Principles", "Two commitments before you touch the data",
              left_head="Tidy data",
              left=["Each **row** = one observation",
                    "Each **column** = one variable",
                    "Each **cell** = one value",
                    "This shape makes every downstream tool 'just work'"],
              right_head="Reproducibility",
              right=["**Never** edit the raw file by hand",
                     "Every fix lives in a **script**",
                     "So it can be re-run, reviewed and trusted (GQ4)",
                     "Keep raw data **read-only**"],
              idx=i())
    d.table("Types", "Know your variable types — they dictate the treatment",
            ["Type", "Example", "Typical handling"],
            [["Continuous numeric", "energy (kJ), BMI", "scale, maybe log-transform"],
             ["Count", "servings of veg", "often log(x+1)"],
             ["Nominal categorical", "sex, food group", "factor → dummy variables"],
             ["Ordinal categorical", "Likert 1–5", "ordered factor / integer score"],
             ["Date / time", "survey date", "parse to Date, derive features"],
             ["Free text", "'other, please specify'", "recode or set aside"]],
            i(), col_widths=[3.3,3.6,4.6])

    d.section("Part 2", "Missing data")
    d.figure("Diagnose first", "Visualise the pattern of missingness", F("L02_missingness.png"), i(),
             caption="A missing-data map. Variable V5 has a structured block (skip-logic?), "
                     "while others are scattered — the pattern is a clue to the mechanism.",
             bullet_head="Always start here",
             bullets=["**Count** missing per variable and per row",
                      "**Look** for blocks and stripes — they reveal structure",
                      "Structured missingness is often **informative**",
                      "Tools: `naniar::vis_miss()`, `visdat::vis_dat()`"])
    d.two_col("Mechanisms", "Why is it missing? Rubin's three mechanisms",
              left_head="MCAR / MAR",
              left=["**MCAR** — missing completely at random; benign but rare",
                    "**MAR** — missingness depends on **observed** variables",
                    "MAR is handleable by conditioning on what you see"],
              right_head="MNAR — the dangerous one",
              right=["Missingness depends on the **unobserved value itself**",
                     "e.g. heavy eaters under-report intake",
                     "Cannot be fixed by imputation alone",
                     "Must be reasoned about with domain experts"],
              idx=i())
    d.table("Remedies", "What to do about missing values",
            ["Strategy", "When appropriate", "Risk"],
            [["Complete-case (drop rows)", "few missing, MCAR", "bias + lost power if not MCAR"],
             ["Mean / median imputation", "quick baseline", "shrinks variance, distorts correlation"],
             ["kNN / model-based imputation", "MAR", "needs care, can leak"],
             ["Multiple imputation (`mice`)", "principled inference", "more complex"]],
            i(), note="Golden rule: **fit imputation on the training data only**, then apply the same "
                      "rule to test data — otherwise you leak information.", col_widths=[3.9,3.8,3.8])
    d.code("In R", "Exploring and imputing missingness", [
        "library(naniar); library(mice)",
        "",
        "# 1. See it",
        "vis_miss(diet)",
        "gg_miss_var(diet)          # missing count per variable",
        "",
        "# 2. Simple median imputation (baseline)",
        "diet <- diet %>% mutate(fibre = ifelse(is.na(fibre),",
        "                                        median(fibre, na.rm = TRUE), fibre))",
        "",
        "# 3. Principled: multiple imputation",
        "imp <- mice(diet, m = 5, method = 'pmm', seed = 1)",
    ], i())

    d.section("Part 3", "Outliers & errors")
    d.figure("Detection", "Boxplots and the IQR rule", F("L02_boxplot.png"), i(),
             caption="The 1.5×IQR rule flags points far from the middle 50%. "
                     "Robust to the very outliers it is trying to find.",
             bullet_head="Robust statistics",
             bullets=["Use **median & IQR**, not mean & SD",
                      "The mean is itself **dragged** by outliers",
                      "**MAD** (median abs. deviation) is a robust spread",
                      "Then **investigate** — don't blindly delete"])
    d.bullets("Judgement", "An outlier is not automatically an error", [
        ("**Range checks**: energy of 80,000 kJ/day? age of 200? negative weight? → flag", 0),
        ("**Logic checks**: pregnant + male? end date before start date? → flag", 0),
        ("A genuine extreme may be the **most interesting participant** in the study", 0),
        ("**Document** every point you remove and **why** — reproducibly", 0),
        ("When unsure, run the analysis **with and without** and report both", 1),
    ], i())

    d.section("Part 4", "Transformations")
    d.figure("Scaling", "Put variables on comparable scales", F("L02_scaling.png"), i(),
             caption="Energy (kJ) and Vitamin C (mg) live on wildly different scales. "
                     "Distance-based methods are dominated by the big-number variable until you standardise.",
             bullet_head="Why it matters",
             bullets=["k-means, PCA, k-NN, SVM all use **distances**",
                      "Unscaled, **energy** would swamp **vitamin C**",
                      "Standardising gives every variable equal footing",
                      "Fit the scaler on **training data only**"])
    d.formula("Standardisation", "The z-score",
              "zᵢ = ( xᵢ − x̄ ) / s",
              ["Subtract the mean **x̄**, divide by the standard deviation **s**",
               "Result has **mean 0, standard deviation 1** for every variable",
               "In R: `scale(x)`; in tidymodels: `step_normalize()`"],
              i(), note="Alternatives: **min–max** scaling to [0,1] (`step_range`), or robust scaling "
                        "using the median and IQR when outliers remain.")
    d.figure("Skew", "Log-transform heavy-tailed variables", F("L02_logtx.png"), i(),
             caption="Nutrient and supplement intakes are often right-skewed. "
                     "A log transform tames the tail and stabilises variance.")
    d.bullets("Categoricals", "Encoding non-numeric variables", [
        ("**Nominal** (sex, food group) → **dummy / one-hot** variables (`step_dummy`)", 0),
        ("**Ordinal** (Likert) → keep the order (ordered factor or integer score)", 0),
        ("Beware **high-cardinality** categories (e.g. 'food name') — group rare levels", 0),
        ("Trim whitespace and standardise case: `\"F \"`, `\"f\"`, `\"Female\"` are one level", 0),
    ], i())

    d.section("Part 5", "Putting it together")
    d.code("Pipeline", "A reproducible cleaning pipeline", [
        "library(tidyverse)",
        "",
        "clean <- raw %>%",
        "  janitor::clean_names() %>%              # tidy column names",
        "  distinct() %>%                          # drop duplicate rows",
        "  mutate(sex = factor(str_trim(sex)),",
        "         energy_kj = na_if(energy_kj, 0)) %>%   # 0 = not recorded",
        "  filter(between(age, 18, 100),           # logic checks",
        "         veg_serves >= 0) %>%",
        "  mutate(across(where(is.numeric),        # standardise numerics",
        "                ~ as.numeric(scale(.))))",
        "",
        "skimr::skim(clean)   # profile the cleaned result",
    ], i(), caption="Chain each fix with %>% so the whole pipeline is one auditable object.")
    d.bullets("Leakage", "Data leakage — the silent killer", [
        ("**Leakage** = using information at training time that won't be available at prediction time", 0),
        ("Classic mistake: **standardise or impute using the whole data set**, then split", 0),
        ("The test set 'sees' the training statistics → **optimistic, dishonest** performance", 0),
        ("**Fix**: split first, then fit every transform inside a **recipe** on the training fold", 0),
        ("tidymodels' `recipe()` + `workflow()` enforce this automatically", 1),
    ], i())
    d.exercise("Clean this record", [
        "A dietary record reads: age = 24, sex = \"F \", energy_kj = 0, "
        "veg_serves = −1, vitc_mg = 4200, height_cm = 168.",
        "Identify **three** data-quality problems.",
        "For each, state whether it is likely an **error** or a **genuine extreme**, and how you'd confirm.",
        "Write the mutate()/filter() lines that would handle them.",
    ], i(), hint="Whitespace in a factor, a structural zero, an impossible negative, and an "
                 "implausible vitamin C value (RDI ≈ 45 mg).")
    d.summary([
        "Cleaning is **most** of the work — do it in a **script**, never by hand.",
        "Diagnose missingness first; the **mechanism (MCAR/MAR/MNAR)** dictates the fix.",
        "Detect outliers with **robust** statistics, then **investigate** before deleting.",
        "**Standardise** before any distance-based method, and fit all transforms on **training data only**.",
    ], i(), nextup="Lecture 03 — Unsupervised learning: introduction to clustering.")

    out = os.path.join(HERE, "Lecture02_DataCleaning.pptx"); d.save(out); return out


# ================================================================= LECTURE 03
def lecture03():
    d = Deck(3, "Introduction to Clustering")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("Unsupervised Learning: Introduction to Clustering",
            "Finding groups in data when nobody gives you the labels — the ideas of distance, "
            "within/between variation, and the main families of methods.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("The clustering problem and nutrition motivation", 0),
        ("Distance and dissimilarity measures", 0),
        ("What makes a clustering 'good': within vs between variation", 0),
        ("The families of clustering methods", 0),
        ("Validating and interpreting clusters", 0),
        ("Common pitfalls", 0),
    ], i())

    d.section("Part 1", "The clustering problem")
    d.figure("The idea", "From an unlabelled cloud to proposed groups", F("L03_clusters.png"), i(),
             caption="Clustering takes points with no labels (left) and proposes a partition (right). "
                     "There is no 'true' answer to check against — it is exploratory.")
    d.bullets("Definition", "What clustering is", [
        ("**Clustering** partitions observations into groups so that members of a group are "
         "**similar**, and different groups are **dissimilar**", 0),
        ("It is **unsupervised**: there is no target Y to predict or check against", 0),
        ("The goal is to **discover and describe** structure, then validate it", 0),
        ("Unlike classification, we don't know the groups in advance — or even how many", 0),
    ], i())
    d.two_col("Motivation", "Why cluster nutrition data?",
              left_head="Dietary patterns",
              left=["Instead of 50 nutrients one at a time…",
                    "…group people into a few **eating patterns**",
                    "e.g. 'prudent' vs 'Western' diets",
                    "Simpler to study and communicate"],
              right_head="Metabolic subtypes",
              right=["Cluster participants by **metabolite profile**",
                     "Reveal **subgroups** that respond differently",
                     "A powerful **hypothesis generator**",
                     "Exactly the kind of project finding that impresses"],
              idx=i())
    d.bullets("Reminder", "Clustering is discovery, not prediction", [
        ("Supervised learning **learns a known label**; clustering **proposes** labels", 0),
        ("Results are **not unique** — different methods and settings give different groupings", 0),
        ("So we must **validate**: are the clusters stable, separated, and **biologically meaningful**?", 0),
    ], i())

    d.section("Part 2", "Distance — the heart of clustering")
    d.figure("Geometry", "Two ways to measure how far apart points are", F("L03_distances.png"), i(),
             caption="Euclidean distance is the straight line; Manhattan distance sums the "
                     "coordinate-wise gaps. The metric encodes what you mean by 'similar'.",
             bullet_head="Key point",
             bullets=["Every algorithm needs a **distance**",
                      "The choice is a **modelling decision**",
                      "It defines the shape of your clusters",
                      "Choose it deliberately, not by default"])
    d.formula("Euclidean distance", "The default metric",
              "d(x, y) = √ Σⱼ ( xⱼ − yⱼ )²",
              ["Straight-line distance in p-dimensional space",
               "Squared version underlies **k-means** (Lecture 4)",
               "Sensitive to **scale** — standardise first!"],
              i())
    d.table("Choices", "Common distance / dissimilarity measures",
            ["Measure", "Idea", "Good for"],
            [["Euclidean", "straight-line", "standardised continuous data"],
             ["Manhattan", "sum of |differences|", "robust, high-dimensional"],
             ["Correlation", "shape, not magnitude", "profiles (gene/metabolite)"],
             ["Gower", "mixed variable types", "numeric + categorical mix"],
             ["Jaccard", "set overlap", "presence/absence data"]],
            i(), col_widths=[2.7,4.3,4.5])
    d.bullets("Scaling", "Why standardising is non-negotiable here", [
        ("Distance is **dominated by large-scale variables**", 0),
        ("Energy (~8000 kJ) vs vitamin C (~75 mg): energy's numbers are ~100× larger", 0),
        ("Without scaling, clustering effectively **ignores** vitamin C", 0),
        ("Standardise (z-scores) so every variable contributes fairly — recall Lecture 2", 0),
    ], i())

    d.section("Part 3", "What makes a clustering good?")
    d.figure("The objective", "Small within, large between", F("L03_withinbetween.png"), i(),
             caption="We want points close to their own cluster centre (small within-cluster variation) "
                     "and centres far apart (large between-cluster variation).",
             bullet_head="The trade-off",
             bullets=["**Within**: spread inside each cluster (minimise)",
                      "**Between**: separation of clusters (maximise)",
                      "Total variation = within + between",
                      "Most algorithms drive **within** down"])
    d.formula("Decomposition", "Total sum of squares splits cleanly",
              "TSS = WSS + BSS",
              ["**WSS** = within-cluster sum of squares (compactness)",
               "**BSS** = between-cluster sum of squares (separation)",
               "Minimising WSS ⇔ maximising BSS, since TSS is fixed"],
              i(), note="Adding clusters **always** lowers WSS — so WSS alone can't choose the number "
                        "of clusters. We need principled criteria (Lecture 4).")

    d.section("Part 4", "Families of methods")
    d.table("Overview", "Four ways to think about clusters",
            ["Family", "Core idea", "In this unit"],
            [["Partitioning", "split into k groups, minimise within-SS", "**k-means** (L04)"],
             ["Model-based", "data from a mixture of distributions", "**GMM** (L05)"],
             ["Hierarchical", "build a tree of nested groups", "**agglomerative** (L06)"],
             ["Density-based", "clusters = dense regions", "DBSCAN (mentioned)"]],
            i(), col_widths=[2.6,5.4,3.5])
    d.bullets("Partitioning", "Partitioning methods (k-means, PAM)", [
        ("Choose **k** up front; each cluster summarised by a **centroid** or **medoid**", 0),
        ("Fast and scalable; assumes roughly **spherical, equal-size** clusters", 0),
        ("The workhorse — our entire next lecture", 0),
    ], i())
    d.figure("Hierarchical", "Hierarchical clustering builds a tree", F("L03_dendro.png"), i(),
             caption="A dendrogram shows nested groupings at every scale. Cut it at a chosen height "
                     "to obtain a clustering. Full treatment in Lecture 6.")
    d.bullets("Model-based & density", "Two more families", [
        ("**Model-based (GMM)**: assume data come from a mixture of Gaussians; gives **soft** "
         "(probabilistic) assignments and a principled way to choose k via the BIC — Lecture 5", 0),
        ("**Density-based (DBSCAN)**: clusters are dense regions separated by sparse ones; finds "
         "**arbitrary shapes** and labels noise, but is sensitive to its distance threshold", 0),
    ], i())

    d.section("Part 5", "Validation & pitfalls")
    d.bullets("Validation", "How do you know the clusters are real?", [
        ("**Internal**: silhouette width, within/between ratios — separation & compactness", 0),
        ("**Stability**: do clusters persist under resampling or small perturbations?", 0),
        ("**External**: do they align with a known variable you held out (e.g. a health outcome)?", 0),
        ("**Domain**: can your Nutrition partners give each cluster a meaningful **name**?", 0),
    ], i())
    d.bullets("Pitfalls", "Where clustering goes wrong", [
        ("Forgetting to **standardise** → one variable dominates", 0),
        ("Reading meaning into clusters that are just **noise** — always validate", 0),
        ("Choosing a method whose **shape assumptions** don't match the data", 0),
        ("Reporting **one** k without justifying it", 0),
    ], i())
    d.code("Preview", "Clustering in R (next lecture goes deep)", [
        "# Standardise first!",
        "X <- scale(diet_numeric)",
        "",
        "d  <- dist(X)                    # distance matrix",
        "km <- kmeans(X, centers = 3, nstart = 25)   # partitioning",
        "hc <- hclust(d, method = 'ward.D2')          # hierarchical",
        "",
        "library(factoextra)",
        "fviz_cluster(km, data = X)       # visualise",
    ], i())
    d.exercise("Reason about distance", [
        "Two participants have (energy kJ, vitamin C mg): A = (8000, 60), B = (8000, 120), "
        "C = (16000, 60).",
        "Compute the Euclidean distance A–B and A–C on the **raw** scale.",
        "Which pair looks 'closer'? Is that the answer you actually want?",
        "Recompute after standardising (assume SD = 4000 kJ and 30 mg). What changes, and why?",
    ], i(), hint="Raw distances are dominated by energy because its numbers are ~100× larger than "
                 "vitamin C's.")
    d.summary([
        "Clustering finds **groups without labels** — exploratory and hypothesis-generating.",
        "A **distance measure** defines 'similar'; it is scale-sensitive, so **standardise** first.",
        "Good clusterings have **small within, large between** variation.",
        "Method families encode different **shape assumptions** — validate before you believe.",
    ], i(), nextup="Lecture 04 — K-means clustering: the workhorse partitioning method.")

    out = os.path.join(HERE, "Lecture03_IntroClustering.pptx"); d.save(out); return out


# ================================================================= LECTURE 04
def lecture04():
    d = Deck(4, "K-means Clustering")
    n=[0]; i=lambda: (n.__setitem__(0,n[0]+1) or f"{n[0]}")

    d.title("K-means Clustering",
            "The workhorse partitioning algorithm: its objective, Lloyd's algorithm, choosing the "
            "number of clusters, and the assumptions that make it succeed — or fail.")
    i()
    d.bullets("Agenda", "Today's roadmap", [
        ("The k-means objective", 0),
        ("Lloyd's algorithm and why it converges", 0),
        ("Local optima and random restarts / k-means++", 0),
        ("Choosing k: elbow, silhouette, gap statistic", 0),
        ("Assumptions, failure modes and alternatives", 0),
        ("Running and interpreting k-means in R", 0),
    ], i())
    d.bullets("Recap", "Where we are", [
        ("Last lecture: clustering finds **groups without labels** using a **distance**", 0),
        ("Good clusterings minimise **within-cluster** variation", 0),
        ("k-means is the **partitioning** method that does exactly this with Euclidean distance", 0),
    ], i())

    d.section("Part 1", "The objective")
    d.formula("Objective", "Minimise within-cluster sum of squares",
              "min  Σₖ Σₓ∈Cₖ  ‖ x − μₖ ‖²",
              ["Partition n points into k clusters C₁,…,Cₖ",
               "Each cluster is summarised by its **centroid** μₖ (the mean)",
               "We want every point **close to its own centroid**"],
              i(), note="Searching all possible partitions is **NP-hard** — so we use a fast, greedy "
                        "approximation: Lloyd's algorithm.")
    d.figure("Geometry", "K-means carves space into Voronoi cells", F("L04_voronoi.png"), i(),
             caption="Each point is assigned to the nearest centroid, so cluster boundaries are "
                     "straight lines (Voronoi cells). This is a strong geometric assumption.",
             bullet_head="Consequences",
             bullets=["Boundaries are **linear**",
                      "Clusters are implicitly **convex**",
                      "Works best for **round, similar-size** blobs",
                      "We'll see where this breaks"])

    d.section("Part 2", "The algorithm")
    d.figure("In action", "Lloyd's algorithm: assign → update → repeat", F("L04_iterations.png"), i(),
             caption="Assign each point to the nearest centroid, then move each centroid to its points' "
                     "mean; repeat. Here a poor start converged to a sub-optimal split — motivating restarts.")
    d.bullets("Steps", "Lloyd's algorithm, step by step", [
        ("**Input**: data X, number of clusters k", 0),
        ("**Initialise** k centroids (randomly, or with k-means++)", 0),
        ("**Assign** each point to its nearest centroid", 1),
        ("**Update** each centroid to the mean of its assigned points", 1),
        ("**Repeat** assign–update until assignments stop changing", 1),
        ("**Output**: cluster labels and final centroids", 0),
    ], i())
    d.bullets("Convergence", "Why it always converges (but not always to the best answer)", [
        ("Each **assign** step can only **decrease** the within-SS (points move to nearer centroids)", 0),
        ("Each **update** step can only **decrease** it (the mean minimises squared distance)", 0),
        ("The objective is **bounded below by 0** and keeps decreasing → it **converges**", 0),
        ("But possibly to a **local** minimum depending on the starting centroids", 0),
    ], i())
    d.bullets("Complexity", "How expensive is it?", [
        ("Per iteration: **O(n · k · p)** — n points, k clusters, p features", 0),
        ("Usually converges in a **handful** of iterations", 0),
        ("**Scales well** to large data — a big reason for its popularity", 0),
    ], i())

    d.section("Part 3", "Local optima")
    d.figure("Initialisation", "Random vs k-means++ starts", F("L04_kmeanspp.png"), i(),
             caption="Random initialisation can place centroids close together (left), risking a poor "
                     "local optimum. k-means++ spreads initial centroids apart (right).",
             bullet_head="The fix",
             bullets=["Run from **many random starts**, keep the best",
                      "'Best' = **lowest** total within-SS",
                      "**k-means++** chooses spread-out starts",
                      "In R: set `nstart = 25` or more"])
    d.code("Restarts", "Always use multiple restarts", [
        "set.seed(1)",
        "km <- kmeans(X, centers = 3, nstart = 25)   # 25 random restarts",
        "",
        "km$tot.withinss    # objective value (lower is better)",
        "km$cluster         # cluster label for each observation",
        "km$centers         # cluster centroids (in scaled units)",
        "km$size            # number of points per cluster",
    ], i(), caption="Without nstart, a single unlucky start can give a badly sub-optimal clustering.")

    d.section("Part 4", "Choosing the number of clusters")
    d.figure("Diagnostics", "Elbow and silhouette methods", F("L04_elbow.png"), i(),
             caption="Left: within-SS always falls with k — look for the 'elbow' where gains flatten. "
                     "Right: the silhouette rewards well-separated clusters and often peaks more clearly.")
    d.formula("Silhouette", "Measuring how well each point is clustered",
              "s(i) = ( bᵢ − aᵢ ) / max(aᵢ, bᵢ)",
              ["**aᵢ** = mean distance from i to points in **its own** cluster",
               "**bᵢ** = mean distance from i to points in the **nearest other** cluster",
               "**s ≈ +1**: well clustered · **s ≈ 0**: on a boundary · **s < 0**: likely misassigned"],
              i(), note="Average s over all points to score a whole clustering; pick the k with the "
                        "**highest** average silhouette.")
    d.bullets("More options", "Other ways to choose k", [
        ("**Gap statistic** — compares within-SS to that expected under no clustering", 0),
        ("**Information criteria** — natural in the model-based approach (BIC, Lecture 5)", 0),
        ("**Stability** — choose k giving reproducible clusters under resampling", 0),
        ("**Interpretability** — a k your Nutrition partners can **name** often wins ties", 0),
    ], i())

    d.section("Part 5", "Assumptions & limits")
    d.figure("Failure mode", "K-means assumes round blobs", F("L04_failure.png"), i(),
             caption="On two interleaving 'moons', k-means carves a straight boundary and splits them "
                     "the wrong way. Its convex, equal-variance assumptions simply don't hold here.",
             bullet_head="When it struggles",
             bullets=["Non-convex / elongated shapes",
                      "Very different cluster **sizes** or **densities**",
                      "**Unscaled** variables",
                      "Many irrelevant / noisy features"])
    d.two_col("Know the assumptions", "K-means in a nutshell",
              left_head="It assumes",
              left=["Clusters are roughly **spherical**",
                    "Clusters have **similar size / variance**",
                    "**Euclidean** distance is meaningful",
                    "You have chosen a sensible **k**"],
              right_head="If that fails, consider",
              right=["**GMM** — elliptical, soft clusters (L05)",
                     "**Hierarchical** — no fixed shape (L06)",
                     "**DBSCAN** — arbitrary shapes, noise",
                     "Always **standardise** first"],
              idx=i())
    d.bullets("In practice", "Interpreting your clusters — the payoff", [
        ("Profile each cluster by its **centroid** across the original variables", 0),
        ("Give each cluster a **name** ('high-fibre / low-sugar', 'Western pattern')", 0),
        ("Check cluster **sizes** — a tiny cluster may be outliers, not a real group", 0),
        ("Relate clusters to **held-out** variables to check they're meaningful", 0),
        ("**This is exactly what you'll do in the project.**", 0),
    ], i())
    d.code("End to end", "A complete k-means analysis in R", [
        "library(tidyverse); library(cluster); library(factoextra)",
        "",
        "X <- scale(diet_numeric)                 # 1. standardise",
        "fviz_nbclust(X, kmeans, method = 'wss')  # 2. elbow plot",
        "fviz_nbclust(X, kmeans, method = 'silhouette')",
        "",
        "set.seed(1)",
        "km <- kmeans(X, centers = 3, nstart = 25)   # 3. fit",
        "fviz_cluster(km, data = X)                  # 4. visualise",
        "",
        "# 5. profile & name the clusters",
        "aggregate(diet_numeric, by = list(km$cluster), FUN = mean)",
    ], i())
    d.exercise("Run and diagnose k-means", [
        "Using the standardised nutrition data, fit k-means for k = 2,…,8 with nstart = 25 and record "
        "tot.withinss.",
        "Plot within-SS vs k. Where is the elbow?",
        "Compute the mean silhouette for each k. Do the two methods agree?",
        "For your chosen k, profile the cluster means — can you give each cluster a nutrition **name**?",
    ], i(), hint="Naming clusters from their centroid profiles is exactly the deliverable your project "
                 "team will need.")
    d.summary([
        "K-means minimises **within-cluster sum of squares** via assign–update iterations.",
        "It converges to a **local** optimum — always use many **restarts** / k-means++.",
        "Choose k with the **elbow** and **silhouette**; let interpretability break ties.",
        "It assumes **round, comparable** clusters — standardise, and switch methods when that fails.",
    ], i(), nextup="Lecture 05 — Model-based clustering: soft assignments with Gaussian mixtures.")

    out = os.path.join(HERE, "Lecture04_Kmeans.pptx"); d.save(out); return out


if __name__ == "__main__":
    for f in (lecture01, lecture02, lecture03, lecture04):
        p = f();
        from pptx import Presentation
        print(f"{os.path.basename(p)}  —  {len(Presentation(p).slides.__iter__.__self__._sldIdLst)} slides")
