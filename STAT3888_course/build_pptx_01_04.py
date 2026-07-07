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

    d.section("Part 6", "Data, roles & a little history")
    d.definition("Definition", "Statistical machine learning",
                 "A set of methods that use **data and probability** to learn predictive or descriptive "
                 "models, with explicit attention to **uncertainty and generalisation**.",
                 i(), extra=["'Statistical' = we quantify uncertainty and assumptions",
                             "'Machine learning' = the algorithm improves with data",
                             "The blend is exactly what employers and researchers need"])
    d.bullets("A little history", "How we got here", [
        ("**1900s–50s** — regression, Fisher's discriminant, the foundations of statistics", 0),
        ("**1960s–80s** — perceptrons, decision trees, early neural networks", 0),
        ("**1990s–2000s** — SVMs, boosting, random forests; the statistical-learning synthesis", 0),
        ("**2010s–now** — deep learning, big data, and ML everywhere", 0),
    ], i())
    d.table("Types of data", "Know what you're working with",
            ["Kind", "Example (nutrition)", "Note"],
            [["Continuous", "energy (kJ), BMI", "most ML assumes this"],
             ["Count", "servings per day", "often skewed"],
             ["Categorical", "sex, food group", "encode as factors"],
             ["Ordinal", "Likert 1–5", "order matters"],
             ["Text / other", "free-text notes", "needs special handling"]],
            i(), col_widths=[2.4,4.6,4.5])
    d.two_col("The team", "Roles in a data-science project",
              left_head="You may play",
              left=["**Data engineer** — clean & wrangle",
                    "**Analyst / modeller** — fit & compare",
                    "**Communicator** — explain results"],
              right_head="Your partners bring",
              right=["**Domain framing** — the real question",
                     "**Interpretation** — is it plausible?",
                     "**Impact** — what to do about it"],
              idx=i())
    d.checkpoint("A variable records 'breakfast: yes/no'. What kind is it?",
        ["Continuous", "Ordinal", "Nominal categorical", "Count"], 2, i(),
        explain="Yes/no is a two-level nominal (unordered) category — encode it as a factor / dummy.")

    d.section("Part 7", "Generalisation, ethics & tools")
    d.definition("Definition", "Overfitting",
                 "**Overfitting** is when a model captures noise specific to the training data and so "
                 "predicts new data poorly.",
                 i(), extra=["Symptom: great training accuracy, poor test accuracy",
                             "Cause: too much flexibility for too little data",
                             "Cure: simpler models, regularisation, cross-validation"])
    d.bullets("Train / validate / test", "The three-way split", [
        ("**Training** set — fit the model", 0),
        ("**Validation** set — tune settings and compare models", 0),
        ("**Test** set — a final, untouched estimate of real-world performance", 0),
        ("Cross-validation reuses data cleverly to do this reliably (Lecture 10)", 0),
    ], i())
    d.big_point("Golden rule", "Never let information from the test set influence training — "
                "that is data leakage, and it makes results a lie.",
                i(), sub="This single principle underlies honest machine learning.")
    d.bullets("Using AI responsibly", "This unit's policy", [
        ("Generative AI is **allowed** for open assessments (project, assignment)", 0),
        ("It is **prohibited** in the supervised final exam", 0),
        ("You must always **acknowledge** AI use — undisclosed use breaches academic integrity", 0),
        ("Use it to **learn and draft**, not to replace understanding", 0),
    ], i())
    d.bullets("Ethics in nutrition ML", "Think before you model", [
        ("Health data is **sensitive** — privacy and consent matter", 0),
        ("Biased data → biased conclusions that can harm real people", 0),
        ("A model that predicts well can still be **unfair** or **uninterpretable**", 0),
        ("Always ask: *should* we, not just *can* we", 0),
    ], i())
    d.code("Your toolkit", "The R commands you'll live in", [
        "library(tidyverse)   # wrangle & visualise",
        "read_csv('diet.csv') |> glimpse()      # load & peek",
        "diet |> summarise(across(where(is.numeric), mean, na.rm=TRUE))",
        "diet |> ggplot(aes(fibre, glucose)) + geom_point() + geom_smooth()",
        "",
        "library(tidymodels) # split, model, resample, evaluate",
    ], i())
    d.checkpoint("A model scores 99% on training data but 62% on test data. This is a classic sign of…",
        ["Underfitting", "Overfitting", "Data leakage in the test set", "A perfect model"], 1, i(),
        explain="A large train-minus-test gap is the signature of overfitting: the model memorised "
                "training noise that doesn't generalise.")

    d.section("Part 8", "The project, up close")
    d.steps("Project timeline", "How the semester unfolds", [
        ("Weeks 1–3", "learn unsupervised methods; choose a research topic"),
        ("Weeks 4–7", "learn supervised methods; form teams, draft the pitch"),
        ("Week 6–7", "project pitch for early feedback (0% but vital)"),
        ("Weeks 8–12", "analysis, manuscript, presentation"),
        ("Week 13", "submit manuscript, reflection & peer review"),
    ], i())
    d.bullets("What makes a good question", "Framing the project", [
        ("**Specific** — 'which dietary pattern predicts insulin resistance?' beats 'study diet'", 0),
        ("**Answerable** with the data you have", 0),
        ("**Interesting** to your nutrition partners", 0),
        ("Matched to a **method** you're learning", 0),
    ], i())
    d.two_col("Teamwork", "Working across disciplines",
              left_head="Do",
              left=["Meet weekly; keep minutes",
                    "Agree on roles early",
                    "Explain your stats plainly",
                    "Version-control shared code"],
              right_head="Avoid",
              right=["Siloing 'stats' vs 'nutrition'",
                     "Last-minute integration",
                     "Jargon without translation",
                     "One person doing everything"],
              idx=i())
    d.bullets("Communicating results", "The skill that gets you hired", [
        ("Lead with the **answer**, not the method", 0),
        ("One **clear figure** beats a table of p-values", 0),
        ("State **uncertainty** honestly", 0),
        ("Tailor depth to the **audience** (GQ3, GQ7)", 0),
    ], i())
    d.exercise("Frame a project question", [
        "Pick a plausible nutrition outcome (e.g. fasting glucose, BMI category).",
        "Write a **specific, answerable** question about it.",
        "Decide: is it supervised or unsupervised? Which method from the syllabus fits?",
        "What would a convincing **result figure** look like?",
    ], i(), hint="If there's a target Y it's supervised; match numeric Y → regression, categorical Y → "
                 "classification.")
    d.bullets("Glossary", "Words we'll use all semester", [
        ("**Feature / predictor** — an input variable (a column)", 0),
        ("**Label / target** — the output we predict (supervised only)", 0),
        ("**Model** — the fitted rule mapping inputs to outputs", 0),
        ("**Generalisation** — performance on unseen data", 0),
    ], i())
    d.checkpoint("Which best describes the goal of this unit's major project?",
        ["Get the highest training accuracy", "Apply ML to answer a real nutrition question and "
         "communicate it", "Use as many methods as possible", "Avoid using R"], 1, i(),
        explain="The project is about applying appropriate methods to a genuine interdisciplinary "
                "question and communicating the findings — not maximising a metric.")

    d.section("Part 9", "The bigger picture")
    d.two_col("A key trade-off", "Interpretability vs flexibility",
              left_head="Interpretable models",
              left=["Linear & logistic regression, trees",
                    "Easy to explain **why**",
                    "Preferred in health & policy",
                    "May underfit complex patterns"],
              right_head="Flexible models",
              right=["Random forests, SVMs, neural nets",
                     "Often more **accurate**",
                     "Harder to explain ('black box')",
                     "Risk overfitting without care"],
              idx=i())
    d.big_point("Choose deliberately", "More complex is not automatically better — the right model "
                "balances accuracy, interpretability, data size and the question.",
                i(), sub="In nutrition, being able to *explain* a finding often matters as much as "
                         "predicting it.")
    d.bullets("More examples: unsupervised", "Spot the structure task", [
        ("Grouping foods by **nutrient profile** → clustering", 0),
        ("Summarising 40 metabolites into a few axes → dimension reduction", 0),
        ("Mapping which nutrients are **conditionally related** → graphical models", 0),
        ("Finding unusual food diaries → anomaly detection", 0),
    ], i())
    d.bullets("More examples: supervised", "Spot the prediction task", [
        ("Predict **body-fat %** from intake → regression", 0),
        ("Classify **diabetic / not** → classification", 0),
        ("Rank features driving an outcome → interpretable models", 0),
        ("Forecast weight change over time → regression", 0),
    ], i())
    d.checkpoint("Grouping foods purely by their nutrient profiles, with no labels, is…",
        ["Regression", "Classification", "Clustering", "Feature engineering"], 2, i(),
        explain="No target variable + finding groups = clustering, an unsupervised task.")
    d.bullets("Where to get help", "Support in this unit", [
        ("**Ed forum** — post questions (anonymously if you prefer)", 0),
        ("**Tutorials & computer labs** — hands-on practice", 0),
        ("**Consultation** — the lecturer's office hours", 0),
        ("Always include your **name and SID** in emails", 0),
    ], i())
    d.bullets("Assessment, up close", "Turning weights into a plan", [
        ("The **project (65%)** is where most marks live — start early", 0),
        ("The **exam (35%)** tests conceptual understanding, not coding", 0),
        ("0%-weighted **pitch & quiz** are your safety rehearsals", 0),
        ("Individual **contribution** is assessed — pull your weight", 0),
    ], i())
    d.bullets("Exam success", "How to prepare from Week 1", [
        ("For each method learn: **assumptions, fitting, evaluation**", 0),
        ("Practise **interpreting output**, not just producing it", 0),
        ("Redo tutorial questions **without** the solutions", 0),
        ("Explain each concept aloud as if teaching it", 0),
    ], i())
    d.big_point("Welcome aboard", "By Week 13 you'll take messy nutrition data and turn it into a "
                "clear, defensible, machine-learning-driven answer.",
                i(), sub="That is exactly what a professional data scientist does. Let's begin.")

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

    d.section("Part 6", "Duplicates, joins & structural checks")
    d.bullets("Duplicates", "More common than you'd think", [
        ("**Exact duplicates** — the same row entered twice (drop with `distinct()`)", 0),
        ("**Near duplicates** — same person, tiny differences (needs a key to detect)", 0),
        ("A hidden duplicate **doubles a participant's weight** in every analysis", 0),
        ("Always check row counts before and after de-duplication", 0),
    ], i())
    d.definition("Definition", "Primary key",
                 "A **primary key** is a column (or set) that uniquely identifies each row — e.g. a "
                 "participant ID.",
                 i(), extra=["Verify it's truly unique: `n_distinct(id) == nrow(data)`",
                             "Keys let you safely **join** datasets (intake + labs)",
                             "A duplicated key is a red flag to investigate"])
    d.code("Joining", "Combining survey and lab tables", [
        "combined <- intake %>%",
        "  inner_join(labs, by = 'participant_id')   # keep matched rows",
        "",
        "# Sanity-check the join",
        "nrow(intake); nrow(labs); nrow(combined)     # did rows explode or vanish?",
        "combined %>% count(participant_id) %>% filter(n > 1)  # duplicates?",
    ], i(), caption="A careless join can silently multiply or drop rows — always check counts.")
    d.checkpoint("After an inner_join, your row count is HIGHER than either input table. Most likely…",
        ["The join worked perfectly", "The join key is duplicated in one table",
         "You lost data", "R is broken"], 1, i(),
        explain="A one-to-many match on a non-unique key multiplies rows. Verify the key is unique "
                "before joining.")

    d.section("Part 7", "Feature engineering")
    d.definition("Definition", "Feature engineering",
                 "**Feature engineering** creates new, more informative variables from the raw data "
                 "using domain knowledge.",
                 i(), extra=["Often more impactful than the choice of model",
                             "Encodes what experts know into the data",
                             "Do it reproducibly, inside your pipeline"])
    d.bullets("Examples", "Useful features for nutrition data", [
        ("**Ratios** — protein-to-energy, sodium-to-potassium", 0),
        ("**Indices** — a diet-quality score from several intakes", 0),
        ("**Derived categories** — BMI bands from height & weight", 0),
        ("**Per-kg** intakes — normalise by body weight", 0),
    ], i())
    d.two_col("Good vs risky", "Feature engineering judgement",
              left_head="Good features",
              left=["Grounded in **domain knowledge**",
                    "Reduce noise or redundancy",
                    "Interpretable to your partners"],
              right_head="Watch out",
              right=["Features built using the **outcome** → leakage",
                     "Too many features → overfitting",
                     "Opaque transforms → hard to explain"],
              idx=i())
    d.bullets("Encoding revisited", "Turning categories into numbers", [
        ("**One-hot / dummy** — one 0/1 column per category level", 0),
        ("**Ordinal** — integer scores when order is meaningful", 0),
        ("**Frequency / target encoding** — powerful but leakage-prone; use with care", 0),
        ("Group **rare levels** into 'other' to avoid tiny, noisy dummies", 0),
    ], i())

    d.section("Part 8", "EDA & a reproducible mindset")
    d.definition("Definition", "Exploratory data analysis (EDA)",
                 "**EDA** is the open-ended visual and numerical exploration of data to understand its "
                 "structure before modelling.",
                 i(), extra=["Histograms, boxplots, scatterplots, correlation heatmaps",
                             "Reveals errors, skew, outliers and relationships",
                             "Every project should start here"])
    d.code("EDA toolkit", "First looks in R", [
        "skimr::skim(diet)                 # per-variable summary",
        "diet %>% ggplot(aes(energy_kj)) + geom_histogram()",
        "diet %>% ggplot(aes(sex, bmi)) + geom_boxplot()",
        "diet %>% select(where(is.numeric)) %>% cor(use='pairwise') %>%",
        "  corrplot::corrplot()            # correlation heatmap",
    ], i())
    d.bullets("What EDA reveals", "Reading your plots", [
        ("**Skew** → consider a log transform", 0),
        ("**Bimodality** → possible subgroups (foreshadows clustering!)", 0),
        ("**Strong correlations** → redundancy (foreshadows PCA!)", 0),
        ("**Isolated points** → outliers to investigate", 0),
    ], i())
    d.big_point("The cleaning mindset", "Treat data cleaning as a documented, re-runnable pipeline — "
                "not a one-off cleanup you can't reproduce.",
                i(), sub="If you can't re-run it from raw data with one command, it isn't reproducible.")
    d.steps("Cleaning checklist", "A repeatable order of operations", [
        ("Load raw (read-only)", "never overwrite the original file"),
        ("Fix structure", "tidy names, types, de-duplicate, join"),
        ("Handle missing", "diagnose mechanism, then impute or drop"),
        ("Handle outliers", "detect robustly, investigate, document"),
        ("Transform", "scale, log, encode — inside a training-only recipe"),
    ], i())
    d.checkpoint("Which step must happen AFTER the train/test split to avoid leakage?",
        ["Fixing column names", "De-duplicating rows", "Fitting the standardisation scaler",
         "Parsing dates"], 2, i(),
        explain="Scaling uses statistics (mean, SD) that must be learned from training data only, then "
                "applied to test data — so it comes after the split.")
    d.exercise("Design a cleaning pipeline", [
        "You receive a raw nutrition survey (CSV) plus a separate lab-results table.",
        "List, in order, the cleaning steps you'd apply from raw files to a modelling-ready table.",
        "Mark which steps must go **after** the train/test split, and why.",
        "Name the R functions you'd use at each step.",
    ], i(), hint="Structural fixes and de-duplication can precede the split; imputation and scaling "
                 "should be fit on training data only.")
    d.bullets("Common mistakes recap", "Avoid these", [
        ("Editing the **raw file** by hand", 0),
        ("Imputing / scaling **before** splitting → leakage", 0),
        ("Deleting outliers **without investigating**", 0),
        ("Ignoring **duplicates** and non-unique keys", 0),
    ], i())

    d.section("Part 9", "Missing data, deeper")
    d.bullets("Why the mechanism matters", "Consequences of getting it wrong", [
        ("Assuming **MCAR** when it's **MNAR** biases every estimate", 0),
        ("Under-reported high intakes (MNAR) make the diet look healthier than it is", 0),
        ("You can **test** for MCAR (e.g. Little's test) but never fully rule out MNAR", 0),
        ("Domain knowledge is essential — ask *why* is it missing?", 0),
    ], i())
    d.definition("Definition", "Multiple imputation",
                 "**Multiple imputation** fills each gap several times to reflect uncertainty, analyses "
                 "each completed dataset, then pools the results.",
                 i(), extra=["Single imputation pretends we know the missing value — MI doesn't",
                             "`mice` is the standard R implementation",
                             "Pooling propagates imputation uncertainty into your estimates"])
    d.code("Multiple imputation", "The mice workflow", [
        "library(mice)",
        "imp  <- mice(diet, m = 5, method = 'pmm', seed = 1)  # 5 imputations",
        "fits <- with(imp, lm(glucose ~ fibre + energy_kj))   # analyse each",
        "pool(fits)                                           # combine results",
    ], i())
    d.table("Decision guide", "Choosing a missing-data strategy",
            ["% missing", "Mechanism", "Suggested approach"],
            [["< 5%", "MCAR", "complete-case or simple imputation"],
             ["5–30%", "MAR", "multiple imputation (mice)"],
             ["> 30%", "any", "consider dropping the variable"],
             ["any", "MNAR", "model the mechanism; consult domain experts"]],
            i(), col_widths=[2.2,2.8,6.5])
    d.checkpoint("Heavy eaters systematically under-report intake, so their high values are missing. "
                 "This is…",
        ["MCAR", "MAR", "MNAR", "Not missing data"], 2, i(),
        explain="Missingness depends on the unobserved value itself (the true high intake) — that is "
                "MNAR, the hardest case.")

    d.section("Part 10", "Scaling, dates & text")
    d.table("Scaling methods", "Beyond the z-score",
            ["Method", "Formula idea", "Use when"],
            [["Standardise (z)", "(x − mean) / SD", "roughly symmetric data"],
             ["Min–max", "(x − min)/(max − min)", "need a [0,1] range"],
             ["Robust", "(x − median)/IQR", "outliers remain"],
             ["Log", "log(x) or log(x+1)", "right-skewed / multiplicative"]],
            i(), col_widths=[2.8,4.2,4.5])
    d.bullets("Dates & times", "A common source of pain", [
        ("Parse strings to real **Date/POSIXct** objects (`lubridate`)", 0),
        ("Derive features: **day of week**, month, season, time since baseline", 0),
        ("Watch for **timezones** and inconsistent formats", 0),
        ("Impossible dates (end before start) are logic-check flags", 0),
    ], i())
    d.bullets("Free text", "When numbers hide in words", [
        ("'2 cups', 'a handful', '~200g' — inconsistent units to reconcile", 0),
        ("Standardise case and whitespace; map synonyms to one label", 0),
        ("Recode common responses; set genuinely free text aside", 0),
        ("Document every recoding decision", 0),
    ], i())
    d.definition("Definition", "Recipe (tidymodels)",
                 "A **recipe** is a reusable specification of preprocessing steps that is *fit on "
                 "training data* and applied identically to new data.",
                 i(), extra=["Prevents leakage by design — steps learn only from training folds",
                             "Chains impute → scale → dummy → … in order",
                             "Slots directly into a modelling `workflow()`"])
    d.code("A leakage-safe recipe", "Preprocessing the right way", [
        "library(tidymodels)",
        "split <- initial_split(diet, prop = 0.8, strata = outcome)",
        "",
        "rec <- recipe(outcome ~ ., data = training(split)) %>%",
        "  step_impute_median(all_numeric_predictors()) %>%",
        "  step_normalize(all_numeric_predictors()) %>%   # scale (train stats)",
        "  step_dummy(all_nominal_predictors())",
        "",
        "# rec is fit on training data, then applied to test data automatically",
    ], i())
    d.checkpoint("Why does putting scaling inside a tidymodels recipe prevent leakage?",
        ["It runs faster", "The scaler learns statistics only from the training fold",
         "It removes outliers", "It imputes automatically"], 1, i(),
        explain="A recipe estimates its parameters (means, SDs) from training data only, then applies "
                "the same transform to test data — no test information leaks in.")
    d.exercise("Fix a leaky pipeline", [
        "A colleague standardises the whole dataset, then splits into train/test and reports 95% accuracy.",
        "Explain precisely where the leakage occurs.",
        "Rewrite the workflow (in words or a recipe) so it's leakage-free.",
        "Would you expect the honest accuracy to be higher or lower? Why?",
    ], i(), hint="Standardising before the split lets the test set's statistics influence training; "
                 "honest accuracy is usually lower.")
    d.big_point("Cleaning is a first-class analysis", "How you clean shapes every result that follows "
                "— it deserves the same rigor and documentation as your modelling.",
                i(), sub="A reproducible, leakage-free pipeline is the mark of a professional.")
    d.bullets("Documenting decisions", "Make your cleaning auditable", [
        ("Keep a **data dictionary**: what each variable is, its units and valid range", 0),
        ("Log every **exclusion** (how many rows, and why)", 0),
        ("Comment non-obvious recodings in the script", 0),
        ("Reviewers (and future-you) must be able to **reconstruct** the clean data", 0),
    ], i())
    d.bullets("Further reading", "To go deeper", [
        ("Wickham & Grolemund, *R for Data Science* — wrangling & tidy data", 0),
        ("van Buuren, *Flexible Imputation of Missing Data* (mice)", 0),
        ("The **tidymodels** and **naniar** package documentation", 0),
    ], i())

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

    d.section("Part 6", "Distances, deeper")
    d.formula("Generalising", "The Minkowski distance",
              "d(x,y) = ( Σⱼ |xⱼ − yⱼ|ᵖ )^(1/p)",
              ["**p = 2** → Euclidean (straight line)",
               "**p = 1** → Manhattan (city-block, more robust)",
               "**p → ∞** → Chebyshev (max coordinate difference)"],
              i(), note="One formula, a family of distances — the exponent p tunes how differences add up.")
    d.definition("Definition", "Dissimilarity vs similarity",
                 "A **dissimilarity** grows as objects differ (like a distance); a **similarity** grows "
                 "as they resemble each other (like a correlation).",
                 i(), extra=["Clustering usually works from **dissimilarities**",
                             "Similarity s and dissimilarity d often relate by d = 1 − s",
                             "Correlation-based clustering compares **shapes**, not magnitudes"])
    d.two_col("Metric choice", "Match the distance to the data",
              left_head="Continuous data",
              left=["Euclidean (after standardising)",
                    "Manhattan for robustness",
                    "Correlation for profiles"],
              right_head="Other data",
              right=["**Gower** for mixed types",
                     "**Jaccard** for presence/absence",
                     "**Hamming** for categorical strings"],
              idx=i())
    d.checkpoint("You want to cluster metabolite **profiles** by shape, ignoring overall magnitude. Best distance?",
        ["Euclidean", "Manhattan", "Correlation-based", "Hamming"], 2, i(),
        explain="Correlation-based dissimilarity compares the pattern/shape of profiles regardless of "
                "their absolute level.")
    d.bullets("Standardising, revisited", "Why it's the #1 clustering mistake", [
        ("Distance-based methods are **dominated** by high-variance variables", 0),
        ("Energy (~thousands) vs vitamin C (~tens) → energy wins by default", 0),
        ("Standardising gives each variable an **equal vote**", 0),
        ("Occasionally you *want* to weight variables — do it **deliberately**", 0),
    ], i())

    d.section("Part 7", "Validation & interpretation")
    d.definition("Definition", "Silhouette width",
                 "The **silhouette** of a point compares its average distance to its own cluster (a) "
                 "with the nearest other cluster (b): s = (b − a)/max(a,b).",
                 i(), extra=["s near +1 → well clustered; near 0 → on a boundary; < 0 → misassigned",
                             "Average silhouette scores a whole clustering",
                             "A model-free way to compare different k"])
    d.table("Validation types", "Three ways to judge clusters",
            ["Type", "Question", "Example"],
            [["Internal", "compact & separated?", "silhouette, WSS/BSS"],
             ["Stability", "reproducible?", "resampling, bootstrap"],
             ["External", "match known groups?", "compare to held-out label"]],
            i(), col_widths=[2.4,4.6,4.5])
    d.bullets("Interpreting clusters", "Turning groups into insight", [
        ("**Profile** each cluster by its variable means", 0),
        ("**Name** it in domain terms ('high-fibre, low-sugar')", 0),
        ("Check **sizes** — a tiny cluster may be outliers", 0),
        ("Relate to a **held-out outcome** to argue relevance", 0),
    ], i())
    d.big_point("Clusters are hypotheses", "Clustering proposes structure; it does not prove it. "
                "Always validate statistically and biologically before you believe it.",
                i(), sub="A pattern in noise is still noise — the discipline is in the checking.")
    d.bullets("Applications in nutrition", "Where clustering earns its keep", [
        ("**Dietary patterns** from intake surveys", 0),
        ("**Metabolic subtypes** from blood metabolites", 0),
        ("**Food grouping** by nutrient composition", 0),
        ("**Participant segmentation** for tailored advice", 0),
    ], i())
    d.checkpoint("A clustering has average silhouette 0.08. This suggests…",
        ["Excellent, well-separated clusters", "Weak, overlapping structure",
         "Perfectly nested clusters", "An error in the code"], 1, i(),
        explain="Average silhouette near 0 means points sit close to the boundary between clusters — "
                "the structure is weak.")
    d.exercise("Plan a clustering study", [
        "You have 30 standardised intake variables for 400 participants.",
        "Which distance and which method family would you try first, and why?",
        "How will you choose the number of clusters?",
        "How will you convince a nutritionist the clusters are **real**, not noise?",
    ], i(), hint="Standardised continuous data → Euclidean + k-means/Ward; choose k by silhouette; "
                 "validate with stability and a held-out outcome.")
    d.bullets("Looking ahead", "The methods to come", [
        ("**k-means** (next) — fast partitioning", 0),
        ("**GMM** — soft, probabilistic clusters", 0),
        ("**Hierarchical** — a tree at every scale", 0),
        ("Each makes different **assumptions** — choose to match your data", 0),
    ], i())

    d.section("Part 8", "The method families in detail")
    d.definition("Definition", "Density-based clustering (DBSCAN)",
                 "**DBSCAN** defines clusters as **dense regions** of points separated by sparser "
                 "regions, and labels low-density points as noise.",
                 i(), extra=["Finds **arbitrary shapes** — not just blobs",
                             "Does **not** need k specified in advance",
                             "Sensitive to its density parameters (eps, minPts)"])
    d.bullets("More families", "Beyond the big three", [
        ("**Spectral clustering** — cluster using a graph of similarities; great for complex shapes", 0),
        ("**Fuzzy clustering** — soft memberships, like a simple GMM", 0),
        ("**Self-organising maps** — neural-network-based clustering + visualisation", 0),
        ("The right family depends on cluster **shape, size and density**", 0),
    ], i())
    d.table("Big picture", "Which family when?",
            ["Family", "Needs k?", "Shapes", "Scales?"],
            [["k-means", "yes", "round", "very well"],
             ["GMM", "yes", "elliptical", "moderately"],
             ["Hierarchical", "no", "any (linkage)", "poorly (O(n²))"],
             ["DBSCAN", "no", "arbitrary", "well"]],
            i(), col_widths=[2.6,1.8,3.6,3.5])
    d.checkpoint("Your clusters are long, curved bands of varying density. Best first choice?",
        ["k-means", "GMM with spherical covariance", "DBSCAN or spectral clustering",
         "None can work"], 2, i(),
        explain="Density-based (DBSCAN) and spectral methods handle arbitrary, curved shapes that "
                "centroid-based methods carve up incorrectly.")
    d.bullets("Curse of dimensionality", "Clustering's hidden enemy", [
        ("In high dimensions, **all points become nearly equidistant**", 0),
        ("Distance-based clustering then loses its power to discriminate", 0),
        ("**Reduce dimensions first** (PCA — Lectures 7–8) or select features", 0),
        ("Fewer, informative variables often cluster **better** than many noisy ones", 0),
    ], i())
    d.definition("Definition", "Clustering tendency",
                 "**Clustering tendency** asks whether the data has any cluster structure *at all* "
                 "before you try to find clusters.",
                 i(), extra=["The **Hopkins statistic** tests for it (≈0.5 means random)",
                             "Any algorithm will *return* clusters — even from noise",
                             "Check tendency so you don't chase phantom groups"])

    d.section("Part 9", "A worked example & consolidation")
    d.formula("By hand", "Euclidean distance, two participants",
              "d = √[ (8000−16000)² + (60−60)² ] = 8000",
              ["On raw scales the energy gap of 8000 swamps everything",
               "Vitamin C contributes **nothing** to the distance here",
               "After standardising, both variables contribute on equal footing"],
              i(), note="This is the single most important practical lesson: standardise first.")
    d.bullets("The standardised version", "Same points, fair comparison", [
        ("Energy gap: 8000 kJ ÷ 4000 SD = **2 SD units**", 0),
        ("Vitamin C gap: 0 mg ÷ 30 SD = **0 SD units**", 0),
        ("Now compare with pairs that differ in vitamin C — they finally 'count'", 0),
        ("Standardising changed which points look **closest**", 0),
    ], i())
    d.two_col("Do & don't", "Clustering hygiene",
              left_head="Do",
              left=["Standardise first",
                    "Check clustering tendency",
                    "Try several methods & k",
                    "Validate and name clusters"],
              right_head="Don't",
              right=["Cluster raw, unscaled data",
                     "Trust one run blindly",
                     "Over-interpret tiny clusters",
                     "Confuse noise for structure"],
              idx=i())
    d.bullets("Case study", "Dietary patterns, end to end", [
        ("Standardise 30 intake variables for 400 participants", 0),
        ("Check the **Hopkins statistic** — is there structure?", 0),
        ("Run k-means and Ward; compare with the **silhouette**", 0),
        ("Profile & **name** the patterns; relate them to a health outcome", 0),
    ], i())
    d.checkpoint("Before clustering, the Hopkins statistic is ≈ 0.5. You should…",
        ["Proceed — strong clusters exist", "Be cautious — the data may be essentially random",
         "Use more clusters", "Standardise again"], 1, i(),
        explain="A Hopkins statistic near 0.5 indicates the data is close to uniformly random — there "
                "may be little real cluster structure to find.")
    d.exercise("Choose distance and method", [
        "For each scenario pick a distance and a method family, with a one-line justification:",
        "(a) 400 participants, 25 standardised continuous intakes, expect round groups.",
        "(b) Metabolite **profiles** where shape matters more than level.",
        "(c) Data with curved, variable-density structure and unknown k.",
    ], i(), hint="(a) Euclidean + k-means; (b) correlation + hierarchical; (c) DBSCAN/spectral.")
    d.bullets("Key terms recap", "Own this vocabulary", [
        ("**Distance / dissimilarity** — how far apart two objects are", 0),
        ("**Within / between** variation — compactness vs separation", 0),
        ("**Silhouette** — a validation score for clusterings", 0),
        ("**Clustering tendency** — is there structure at all?", 0),
    ], i())
    d.code("R preview", "The clustering toolkit you'll use", [
        "X <- scale(diet_numeric)                 # standardise",
        "get_clust_tendency(X, n = 50)            # Hopkins statistic",
        "fviz_nbclust(X, kmeans, method='silhouette')",
        "km <- kmeans(X, 3, nstart = 25); hc <- hclust(dist(X), 'ward.D2')",
    ], i())
    d.big_point("The mindset", "Clustering is a conversation with your data, not a button you press "
                "— you propose structure, then interrogate it.",
                i(), sub="Distance, method and validation are all your choices to justify.")
    d.checkpoint("What is the single most common practical mistake in distance-based clustering?",
        ["Using too many colours", "Forgetting to standardise the variables",
         "Choosing k = 2", "Using R"], 1, i(),
        explain="Failing to standardise lets high-variance variables dominate the distance and hijack "
                "the entire clustering.")
    d.bullets("Further reading", "To go deeper", [
        ("James et al., *An Introduction to Statistical Learning*, Ch. 12", 0),
        ("Hastie et al., *The Elements of Statistical Learning*, Ch. 14", 0),
        ("R: `factoextra`, `cluster` vignettes", 0),
    ], i())

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

    d.section("Part 6", "The mathematics, a little deeper")
    d.formula("Why the mean?", "The centroid minimises squared distance",
              "μₖ = argmin_c  Σ_{x∈Cₖ} ‖x − c‖²  =  mean(Cₖ)",
              ["For squared Euclidean distance, the best single summary point is the **mean**",
               "That's why the update step sets each centroid to its cluster's average",
               "Use a different distance and the best 'centre' changes (e.g. medoid for k-medoids)"],
              i())
    d.definition("Definition", "k-medoids (PAM)",
                 "**k-medoids** is like k-means but each cluster is represented by an actual data point "
                 "(the medoid), not a mean.",
                 i(), extra=["More **robust to outliers** than k-means",
                             "Works with any distance, not just Euclidean",
                             "Slower; implemented as `pam()` in R's cluster package"])
    d.bullets("Why squared distance?", "Consequences of the objective", [
        ("Squaring **penalises large deviations** heavily → sensitive to outliers", 0),
        ("Makes the mean the optimal centre (nice math)", 0),
        ("Biases toward **equal-size, spherical** clusters", 0),
        ("If that's wrong for your data, choose another method", 0),
    ], i())
    d.checkpoint("Why does the k-means update step use the mean of each cluster?",
        ["Tradition", "The mean minimises within-cluster squared distance",
         "It's the fastest to compute", "To avoid outliers"], 1, i(),
        explain="Given squared Euclidean distance, the point minimising total squared distance to a set "
                "is exactly its mean — so the mean is the optimal centroid.")

    d.section("Part 7", "Choosing k, in depth")
    d.definition("Definition", "The gap statistic",
                 "The **gap statistic** compares your clustering's within-SS to the within-SS expected "
                 "under a null model with no clusters.",
                 i(), extra=["Large gap = structure well beyond random",
                             "Chooses k where the gap is largest (with a standard-error rule)",
                             "`cluster::clusGap()` in R"])
    d.table("Methods for k", "Four ways, compared",
            ["Method", "Idea", "Note"],
            [["Elbow", "where WSS flattens", "subjective"],
             ["Silhouette", "separation quality", "clear peak, popular"],
             ["Gap statistic", "vs random null", "principled, slower"],
             ["Domain sense", "interpretable k", "breaks ties"]],
            i(), col_widths=[2.6,4.4,4.5])
    d.bullets("When methods disagree", "A practical protocol", [
        ("Compute **all** the criteria — don't rely on one", 0),
        ("Prefer a k that is **stable** across methods and resamples", 0),
        ("Among near-ties, choose the **most interpretable** k", 0),
        ("Report *how* you chose — reproducibility matters", 0),
    ], i())
    d.checkpoint("Adding more clusters ALWAYS reduces within-cluster SS. Why can't we just minimise WSS?",
        ["WSS is hard to compute", "It would pick k = n (one point per cluster)",
         "WSS ignores distance", "It only works for k = 2"], 1, i(),
        explain="WSS keeps falling as k grows, hitting zero at k = n. So we need criteria (elbow, "
                "silhouette, gap) that penalise complexity or reward separation.")

    d.section("Part 8", "Practice, pitfalls & extensions")
    d.two_col("Strengths & weaknesses", "k-means in balance",
              left_head="Strengths",
              left=["**Fast** and scales to big data",
                    "Simple to implement & explain",
                    "Works well on round, separated blobs"],
              right_head="Weaknesses",
              right=["Must **pre-specify k**",
                     "Assumes spherical, equal-size clusters",
                     "Sensitive to **scale, outliers, init**"],
              idx=i())
    d.bullets("Preprocessing checklist", "Before you run k-means", [
        ("**Standardise** every variable", 0),
        ("Handle **outliers** (they drag centroids)", 0),
        ("Consider **PCA first** if there are many variables", 0),
        ("Set a **seed** and use `nstart ≥ 25`", 0),
    ], i())
    d.bullets("Extensions", "The k-means family", [
        ("**k-means++** — smarter initialisation", 0),
        ("**Mini-batch k-means** — scales to millions of points", 0),
        ("**k-medoids (PAM)** — robust, any distance", 0),
        ("**Fuzzy c-means** — soft memberships (a bridge to GMM)", 0),
    ], i())
    d.big_point("The honest summary", "k-means is the fast, popular first thing to try — and the "
                "method whose assumptions you must most actively check.",
                i(), sub="When the blobs aren't round, reach for GMM or hierarchical clustering next.")
    d.exercise("Diagnose a failure", [
        "You run k-means (k = 2) on clearly crescent-shaped data and the clusters look wrong.",
        "Explain, using k-means' assumptions, **why** it failed.",
        "Which two alternative methods might succeed, and why?",
        "What preprocessing, if any, would *not* have fixed this?",
    ], i(), hint="k-means draws linear (Voronoi) boundaries and assumes convex blobs; scaling won't fix "
                 "a non-convex shape.")
    d.bullets("Further reading", "To go deeper", [
        ("James et al., *An Introduction to Statistical Learning*, §12.4", 0),
        ("Hastie et al., *The Elements of Statistical Learning*, §14.3", 0),
        ("R: `cluster`, `factoextra` package vignettes", 0),
    ], i())

    d.section("Part 9", "K-means by hand")
    d.bullets("Setup", "A tiny 1-D example", [
        ("Points: 1, 2, 3, 10, 11, 12 — clearly two groups", 0),
        ("We'll run k-means with k = 2 from a **bad** start to see it recover", 0),
        ("Initial centroids: c₁ = 2, c₂ = 4", 0),
    ], i())
    d.steps("Iteration 1", "Assign, then update", [
        ("Assign", "1,2,3 → c₁ (nearer 2); 10,11,12 → c₂ (nearer 4)"),
        ("Update", "c₁ = mean(1,2,3) = 2; c₂ = mean(10,11,12) = 11"),
        ("Reassign", "assignments unchanged → converged"),
        ("Result", "clusters {1,2,3} and {10,11,12}, centroids 2 and 11"),
    ], i(), note="Even from a poor c₂ = 4, one pass snaps to the right answer here.")
    d.formula("Track the objective", "Within-cluster SS falls",
              "WSS = Σ (x − μₖ)²  :  before ≫ after each step",
              ["Start WSS is large (centroids misplaced)",
               "Each assign/update step **cannot increase** WSS",
               "Convergence = WSS stops changing"],
              i())
    d.bullets("Edge case", "What if a cluster goes empty?", [
        ("A centroid can end up with **no points assigned**", 0),
        ("Implementations **re-seed** it (e.g. to the farthest point)", 0),
        ("More restarts make this rare", 0),
        ("Another reason `nstart` matters", 0),
    ], i())
    d.checkpoint("In the worked example, what guaranteed k-means stopped after one full pass?",
        ["It ran out of time", "The assignments didn't change between steps",
         "k was too small", "The data was sorted"], 1, i(),
        explain="k-means converges exactly when an iteration produces no change in assignments — the "
                "objective can't improve further.")

    d.section("Part 10", "Applications & wrap-up")
    d.definition("Definition", "Colour quantisation",
                 "**Colour quantisation** compresses an image by clustering its pixels' colours with "
                 "k-means and keeping only k representative colours.",
                 i(), extra=["Each pixel is a point in 3-D (R,G,B) space",
                             "k-means finds k 'average' colours",
                             "A vivid, everyday demonstration of clustering"])
    d.bullets("Where k-means shows up", "Real uses", [
        ("**Customer / patient segmentation**", 0),
        ("**Image compression** (colour quantisation)", 0),
        ("**Document / topic grouping** on embeddings", 0),
        ("**Vector quantisation** in signal processing", 0),
    ], i())
    d.two_col("k-means vs GMM (preview)", "A taste of next week",
              left_head="k-means",
              left=["Hard labels", "Spherical, equal size", "Fast", "Distance-based"],
              right_head="GMM",
              right=["Soft probabilities", "Elliptical, varying size",
                     "Slower (EM)", "Probability model"],
              idx=i())
    d.bullets("Exam pointers", "What's commonly tested", [
        ("State the **objective** and the **two steps** of the algorithm", 0),
        ("Explain **local optima** and the role of `nstart`", 0),
        ("Choose k from an **elbow / silhouette** plot", 0),
        ("Name the **assumptions** and a failure mode", 0),
    ], i())
    d.big_point("You can now cluster", "Standardise → choose k → run k-means with restarts → "
                "validate → name the clusters. That's a complete, defensible workflow.",
                i(), sub="Next we make the clusters soft and probabilistic with Gaussian mixtures.")
    d.exercise("Consolidation", [
        "State the k-means objective in one line.",
        "Explain why k-means can give different answers on different runs, and the fix.",
        "Given an elbow at k = 3 but a silhouette peak at k = 4, how would you decide?",
        "Name one dataset shape where k-means fails and what you'd use instead.",
    ], i(), hint="Use interpretability and stability to break elbow-vs-silhouette ties; non-convex "
                 "shapes → DBSCAN/spectral.")
    d.definition("Definition", "Inertia (within-cluster SS)",
                 "**Inertia** is k-means' objective value — the total squared distance of points to "
                 "their assigned centroids. Lower is tighter.",
                 i(), extra=["Reported as `tot.withinss` in R / `inertia_` in Python",
                             "Compare inertia only for the **same k** across restarts",
                             "It always decreases as k increases — hence the elbow method"])
    d.table("Cheat-sheet", "k-means at a glance",
            ["Question", "Answer"],
            [["Objective", "minimise within-cluster SS (inertia)"],
             ["Algorithm", "Lloyd's: assign → update → repeat"],
             ["Choose k", "elbow, silhouette, gap statistic"],
             ["Guard against", "local optima (nstart), scale, outliers"],
             ["Assumes", "round, comparable, convex clusters"]],
            i(), col_widths=[3.0,8.5])
    d.checkpoint("`tot.withinss` for k = 4 is lower than for k = 3. Does that prove k = 4 is better?",
        ["Yes, lower is always better", "No — inertia always falls with k; use silhouette/elbow",
         "Only if standardised", "Yes, if nstart is high"], 1, i(),
        explain="Inertia decreases monotonically with k, so a lower value at higher k is expected and "
                "proves nothing — judge with the elbow/silhouette instead.")
    d.bullets("One-line recap", "Carry this out the door", [
        ("**Standardise, restart, choose k with care, validate, name.**", 0),
    ], i())
    d.bullets("Further reading", "To go deeper", [
        ("James et al., *An Introduction to Statistical Learning*, §12.4.1", 0),
        ("Hastie et al., *The Elements of Statistical Learning*, §14.3.6", 0),
        ("R: `stats::kmeans`, `cluster::pam`, `factoextra` vignettes", 0),
    ], i())

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
